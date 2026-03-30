"""
RMA Data Import — Importa dati storici da Excel nella tabella RmaRecords.
Traduce i campi testuali da italiano a rumeno usando Google Translate (gratuito).

Uso: python rma/rma_import_data.py
     (eseguire dalla directory root del progetto)
"""
import os
import sys
import time
import logging
import pandas as pd
import pyodbc
from deep_translator import GoogleTranslator

# ---------------------------------------------------------------------------
# Aggiungi la directory del progetto al path per importare config_manager
# ---------------------------------------------------------------------------
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

from config_manager import ConfigManager

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
EXCEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Elenco schede EVOCA_ELECTROLUX 01012021_11032026.xls"
)

# Usa la stessa connection string criptata del programma principale
config_mgr = ConfigManager(
    key_file=os.path.join(PROJECT_DIR, 'encryption_key.key'),
    config_file=os.path.join(PROJECT_DIR, 'db_config.enc')
)
db_cred = config_mgr.load_config()
CONN_STR = (
    f"DRIVER={db_cred['driver']};SERVER={db_cred['server']};"
    f"DATABASE={db_cred['database']};UID={db_cred['username']};"
    f"PWD={db_cred['password']};MARS_Connection=Yes;TrustServerCertificate=Yes"
)

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_import_log.txt")
BATCH_SIZE = 50          # commit every N rows
TRANSLATE_DELAY = 0.3    # seconds between Google Translate calls (rate limit)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("rma_import")

# ---------------------------------------------------------------------------
# Translator helper
# ---------------------------------------------------------------------------
_translator = GoogleTranslator(source="it", target="ro")
_cache: dict[str, str] = {}


def translate_it_ro(text: str) -> str:
    """Translate Italian text to Romanian. Returns original if empty or error."""
    if not text or not text.strip():
        return text
    text = text.strip()
    if text in _cache:
        return _cache[text]
    try:
        time.sleep(TRANSLATE_DELAY)
        result = _translator.translate(text)
        _cache[text] = result or text
        return _cache[text]
    except Exception as e:
        log.warning(f"Translation failed for '{text[:60]}...': {e}")
        return text  # fallback: keep Italian


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------
def get_or_create_fault_type(cursor, code: str, description_it: str) -> int | None:
    if not code and not description_it:
        return None
    code = (code or "").strip()
    description_it = (description_it or "").strip()

    if code:
        cursor.execute("SELECT RmaFaultTypeId FROM RmaFaultTypes WHERE Code = ?", code)
    else:
        cursor.execute("SELECT RmaFaultTypeId FROM RmaFaultTypes WHERE DescriptionIT = ?", description_it)
    row = cursor.fetchone()
    if row:
        return row[0]

    desc_ro = translate_it_ro(description_it) if description_it else description_it
    cursor.execute(
        "INSERT INTO RmaFaultTypes (Code, Description, DescriptionIT) OUTPUT INSERTED.RmaFaultTypeId VALUES (?, ?, ?)",
        code or None, desc_ro or description_it, description_it or None,
    )
    row = cursor.fetchone()
    if row and row[0] is not None:
        return int(row[0])
    return None


def get_or_create_fault_detail(cursor, fault_type_id, code: str, description_it: str) -> int | None:
    if not code and not description_it:
        return None
    if not fault_type_id:
        return None
    code = (code or "").strip()
    description_it = (description_it or "").strip()

    if code:
        cursor.execute(
            "SELECT RmaFaultDetailId FROM RmaFaultDetails WHERE Code = ? AND RmaFaultTypeId = ?",
            code, fault_type_id,
        )
    else:
        cursor.execute(
            "SELECT RmaFaultDetailId FROM RmaFaultDetails WHERE DescriptionIT = ? AND RmaFaultTypeId = ?",
            description_it, fault_type_id,
        )
    row = cursor.fetchone()
    if row:
        return row[0]

    desc_ro = translate_it_ro(description_it) if description_it else description_it
    cursor.execute(
        "INSERT INTO RmaFaultDetails (RmaFaultTypeId, Code, Description, DescriptionIT) OUTPUT INSERTED.RmaFaultDetailId VALUES (?, ?, ?, ?)",
        fault_type_id, code or None, desc_ro or description_it, description_it or None,
    )
    row = cursor.fetchone()
    if row and row[0] is not None:
        return int(row[0])
    return None


# ---------------------------------------------------------------------------
# Excel helpers
# ---------------------------------------------------------------------------
def safe_str(val) -> str | None:
    if pd.isna(val):
        return None
    s = str(val).strip()
    return s if s else None


def safe_int(val) -> int | None:
    if pd.isna(val):
        return None
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Main import
# ---------------------------------------------------------------------------
def main():
    log.info("=" * 60)
    log.info("RMA Import avviato")
    log.info(f"Excel: {EXCEL_PATH}")
    log.info("=" * 60)

    if not os.path.exists(EXCEL_PATH):
        log.error(f"File non trovato: {EXCEL_PATH}")
        sys.exit(1)

    log.info("Lettura Excel...")
    df = pd.read_excel(EXCEL_PATH, engine="xlrd")
    log.info(f"Righe trovate: {len(df)}, Colonne: {len(df.columns)}")

    # Column indices (0-based)
    COL = {
        "serial_number": 6,       # G
        "customer_part_code": 7,  # H
        "part_code_producer": 8,  # I
        "production_week": 9,     # J
        "fault_description": 11,  # L — TRANSLATE
        "fault_cause_code": 17,   # R
        "fault_cause": 18,        # S — TRANSLATE
        "part_description": 19,   # T
        "warranty_type": 20,      # U
        "customer_id": 26,        # AA
        "customer_name": 27,      # AB
        "part_code": 28,          # AC
        "reference": 33,          # AH
        "fault_type_desc": 34,    # AI — TRANSLATE (lookup)
        "fault_detail_desc": 35,  # AJ — TRANSLATE (lookup)
        "fault_notes": 36,        # AK — TRANSLATE
        "fault_type_code": 37,    # AL
        "fault_detail_code": 38,  # AM
        "assembly": 39,           # AN
    }

    log.info("Connessione al database...")
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()

    # Check existing imports
    cursor.execute("SELECT COUNT(*) FROM RmaRecords WHERE Source = 'IMPORT'")
    existing = cursor.fetchone()[0]
    if existing > 0:
        log.warning(f"Trovati {existing} record gia importati. Continuare? (s/n)")
        ans = input().strip().lower()
        if ans != "s":
            log.info("Import annullato.")
            conn.close()
            return

    inserted = 0
    errors = 0
    translated_count = 0

    for idx, row in df.iterrows():
        try:
            serial = safe_str(row.iloc[COL["serial_number"]])
            cust_part = safe_str(row.iloc[COL["customer_part_code"]])
            prod_code = safe_str(row.iloc[COL["part_code_producer"]])
            prod_week = safe_str(row.iloc[COL["production_week"]])
            part_desc = safe_str(row.iloc[COL["part_description"]])
            warranty = safe_str(row.iloc[COL["warranty_type"]])
            cust_id = safe_int(row.iloc[COL["customer_id"]])
            cust_name = safe_str(row.iloc[COL["customer_name"]])
            part_code = safe_str(row.iloc[COL["part_code"]])
            reference = safe_str(row.iloc[COL["reference"]])
            assembly = safe_str(row.iloc[COL["assembly"]])
            fault_cause_code = safe_str(row.iloc[COL["fault_cause_code"]])
            fault_type_code = safe_str(row.iloc[COL["fault_type_code"]])
            fault_detail_code = safe_str(row.iloc[COL["fault_detail_code"]])

            # Fields to translate IT -> RO
            fault_desc_it = safe_str(row.iloc[COL["fault_description"]])
            fault_cause_it = safe_str(row.iloc[COL["fault_cause"]])
            fault_notes_it = safe_str(row.iloc[COL["fault_notes"]])
            fault_type_desc_it = safe_str(row.iloc[COL["fault_type_desc"]])
            fault_detail_desc_it = safe_str(row.iloc[COL["fault_detail_desc"]])

            fault_desc_ro = translate_it_ro(fault_desc_it) if fault_desc_it else None
            fault_cause_ro = translate_it_ro(fault_cause_it) if fault_cause_it else None
            fault_notes_ro = translate_it_ro(fault_notes_it) if fault_notes_it else None

            if fault_desc_it or fault_cause_it or fault_notes_it:
                translated_count += 1

            fault_type_id = get_or_create_fault_type(cursor, fault_type_code, fault_type_desc_it)
            fault_detail_id = get_or_create_fault_detail(cursor, fault_type_id, fault_detail_code, fault_detail_desc_it)

            cursor.execute(
                """
                INSERT INTO RmaRecords (
                    SerialNumber, PartCode, CustomerPartCode, PartDescription,
                    CustomerId, CustomerName,
                    FaultDescription, FaultDescriptionIT,
                    FaultCauseCode, FaultCause, FaultCauseIT,
                    RmaFaultTypeId, RmaFaultDetailId,
                    Reference, Assembly,
                    FaultNotes, FaultNotesIT,
                    ProductionWeek, WarrantyType,
                    InsertedBy, Source
                ) VALUES (
                    ?, ?, ?, ?,
                    ?, ?,
                    ?, ?,
                    ?, ?, ?,
                    ?, ?,
                    ?, ?,
                    ?, ?,
                    ?, ?,
                    ?, ?
                )
                """,
                serial, part_code or prod_code, cust_part, part_desc,
                cust_id, cust_name,
                fault_desc_ro, fault_desc_it,
                fault_cause_code, fault_cause_ro, fault_cause_it,
                fault_type_id, fault_detail_id,
                reference, assembly,
                fault_notes_ro, fault_notes_it,
                prod_week, warranty,
                "IMPORT_SCRIPT", "IMPORT",
            )

            inserted += 1

            if inserted % BATCH_SIZE == 0:
                conn.commit()
                log.info(
                    f"  Progresso: {inserted}/{len(df)} "
                    f"({inserted * 100 // len(df)}%) "
                    f"- traduzioni: {translated_count}"
                )

        except Exception as e:
            errors += 1
            import traceback
            log.error(f"Errore riga {idx}: {e}\n{traceback.format_exc()}")
            continue

    conn.commit()
    conn.close()

    log.info("=" * 60)
    log.info(f"Import completato!")
    log.info(f"  Inseriti:  {inserted}")
    log.info(f"  Errori:    {errors}")
    log.info(f"  Traduzioni: {translated_count}")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
