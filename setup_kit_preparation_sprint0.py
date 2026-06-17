"""
setup_kit_preparation_sprint0.py
Sprint 0 del modulo Kit Preparation (spec docs/PlanRespect_KitPreparation_Spec_v1.2.md):

1. Registra le chiavi di autorizzazione 'verifica_kit_materiale' e
   'conferma_kit_completamento' in AppTranslations (5 lingue) con MenuValue
   valorizzato, cosi' compaiono nella GUI permessi e sono usabili da
   _execute_authorized_action.
2. Crea la setting 'Sys_email_Kit_materiali' in traceability_rs.dbo.settings
   (destinatari email notifiche kit; valore opzionale da riga di comando).
3. Verifica l'accesso a T:\\KITTING e riepiloga lo stato.

Uso:
  .venv\\Scripts\\python.exe setup_kit_preparation_sprint0.py [--dry-run] [--emails "a@x.com;b@x.com"]
"""
import sys, io, os, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager

KITTING_DIR = r"T:\KITTING"
EMAIL_SETTING_ATTRIBUTE = 'Sys_email_Kit_materiali'

LANGS = ['it', 'en', 'ro', 'de', 'sv']

# (key, MenuValue, IT, EN, RO, DE, SV)
AUTH_KEYS = [
    ('verifica_kit_materiale',
        'Verifica Kit Materiali',
        'Verifica Kit Materiali',
        'Material Kit Verification',
        'Verificare Kit Materiale',
        'Materialkit-Prüfung',
        'Verifiering av materialkit'),
    ('conferma_kit_completamento',
        'Conferma Completamento Kit',
        'Conferma Completamento Kit',
        'Kit Completion Confirmation',
        'Confirmare Finalizare Kit',
        'Bestätigung Kit-Fertigstellung',
        'Bekräftelse av kit-slutförande'),
]


def get_conn():
    cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
    conn_str = (f"DRIVER={cfg['driver']};SERVER={cfg['server']};"
                f"DATABASE={cfg['database']};UID={cfg['username']};PWD={cfg['password']};"
                f"MARS_Connection=Yes;TrustServerCertificate=Yes")
    return pyodbc.connect(conn_str)


def setup_auth_keys(cursor, dry_run):
    """Inserisce traduzioni + MenuValue per le chiavi di autorizzazione."""
    inserted, updated, skipped = 0, 0, 0
    for row in AUTH_KEYS:
        key, menu_value = row[0], row[1]
        for i, lang in enumerate(LANGS):
            value = row[i + 2]
            cursor.execute(
                "SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                "WHERE LanguageCode=? AND TranslationKey=?",
                (lang, key)
            )
            if cursor.fetchone()[0] == 0:
                if not dry_run:
                    cursor.execute(
                        "INSERT INTO Traceability_rs.dbo.AppTranslations "
                        "(LanguageCode, TranslationKey, TranslationValue, MenuValue) "
                        "VALUES (?,?,?,?)",
                        (lang, key, value, menu_value)
                    )
                inserted += 1
            else:
                skipped += 1

        # MenuValue su eventuali righe preesistenti senza MenuValue
        # (la GUI permessi mostra solo chiavi con MenuValue IS NOT NULL)
        cursor.execute(
            "SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
            "WHERE TranslationKey=? AND MenuValue IS NULL", (key,)
        )
        to_fix = cursor.fetchone()[0]
        if to_fix:
            if not dry_run:
                cursor.execute(
                    "UPDATE Traceability_rs.dbo.AppTranslations "
                    "SET MenuValue=? WHERE TranslationKey=? AND MenuValue IS NULL",
                    (menu_value, key)
                )
            updated += to_fix
        print(f"  [{key}] MenuValue='{menu_value}'")

    print(f"  Traduzioni: {inserted} inserite, {updated} MenuValue aggiornati, {skipped} gia' presenti")


def setup_email_setting(cursor, dry_run, emails):
    """Crea la setting destinatari email se mancante."""
    cursor.execute(
        "SELECT [value] FROM traceability_rs.dbo.settings WHERE atribute=?",
        (EMAIL_SETTING_ATTRIBUTE,)
    )
    existing = cursor.fetchall()
    if existing:
        values = '; '.join(str(r[0]) for r in existing)
        print(f"  Setting '{EMAIL_SETTING_ATTRIBUTE}' gia' presente: {values}")
        if emails:
            if not dry_run:
                cursor.execute(
                    "UPDATE traceability_rs.dbo.settings SET [value]=? WHERE atribute=?",
                    (emails, EMAIL_SETTING_ATTRIBUTE)
                )
            print(f"  Valore aggiornato a: {emails}")
    else:
        value = emails or ''
        if not dry_run:
            cursor.execute(
                "INSERT INTO traceability_rs.dbo.settings (atribute, [value]) VALUES (?,?)",
                (EMAIL_SETTING_ATTRIBUTE, value)
            )
        print(f"  Setting '{EMAIL_SETTING_ATTRIBUTE}' creata (valore: '{value or 'VUOTO - da compilare!'}')")
        if not emails:
            print("  ATTENZIONE: inserire i destinatari (separatore ';') prima dello Sprint 3 (notifiche).")


def check_kitting_dir():
    """Verifica accesso a T:\\KITTING da questa postazione."""
    if not os.path.isdir(KITTING_DIR):
        print(f"  ERRORE: {KITTING_DIR} non raggiungibile da questa postazione")
        return
    try:
        files = os.listdir(KITTING_DIR)
        xlsx = [f for f in files if f.lower().endswith('.xlsx')]
        pdf = [f for f in files if f.lower().endswith('.pdf')]
        print(f"  {KITTING_DIR} raggiungibile: {len(xlsx)} file .xlsx, {len(pdf)} file .pdf, {len(files)} totali")
        if not xlsx:
            print("  NOTA: nessun file .xlsx presente - raccogliere campioni reali da Essegi "
                  "e validarli con validate_essegi_xlsx.py")
    except OSError as e:
        print(f"  ERRORE lettura {KITTING_DIR}: {e}")


def verify(cursor):
    """Riepilogo finale dello stato su DB."""
    print("\n=== VERIFICA FINALE ===")
    for row in AUTH_KEYS:
        key = row[0]
        cursor.execute(
            "SELECT LanguageCode, TranslationValue, MenuValue "
            "FROM Traceability_rs.dbo.AppTranslations WHERE TranslationKey=? ORDER BY LanguageCode",
            (key,)
        )
        rows = cursor.fetchall()
        langs = ', '.join(f"{r[0]}" for r in rows)
        menu_ok = all(r[2] for r in rows)
        print(f"  {key}: {len(rows)} lingue ({langs}), MenuValue {'OK' if menu_ok else 'MANCANTE'}")
        cursor.execute(
            "SELECT COUNT(*) FROM Traceability_RS.dbo.AutorizedUsers "
            "WHERE TranslationKey=? AND DateOut IS NULL", (key,)
        )
        n_auth = cursor.fetchone()[0]
        print(f"    Utenti autorizzati attivi: {n_auth}"
              + ("  (assegnare dalla GUI permessi)" if n_auth == 0 else ""))
    cursor.execute(
        "SELECT [value] FROM traceability_rs.dbo.settings WHERE atribute=?",
        (EMAIL_SETTING_ATTRIBUTE,)
    )
    r = cursor.fetchone()
    print(f"  {EMAIL_SETTING_ATTRIBUTE}: {'presente, valore=' + repr(r[0]) if r else 'ASSENTE'}")


def main():
    parser = argparse.ArgumentParser(description='Setup Sprint 0 Kit Preparation')
    parser.add_argument('--dry-run', action='store_true', help='mostra le azioni senza scrivere a DB')
    parser.add_argument('--emails', default=None,
                        help="destinatari per Sys_email_Kit_materiali, separati da ';'")
    args = parser.parse_args()

    conn = get_conn()
    cursor = conn.cursor()
    print(f"Connesso al database.{' (DRY-RUN: nessuna scrittura)' if args.dry_run else ''}")

    print("\n[1/3] Chiavi di autorizzazione")
    setup_auth_keys(cursor, args.dry_run)

    print("\n[2/3] Setting destinatari email")
    setup_email_setting(cursor, args.dry_run, args.emails)

    print("\n[3/3] Accesso T:\\KITTING")
    check_kitting_dir()

    if args.dry_run:
        conn.rollback()
        print("\nDRY-RUN: rollback eseguito, nessuna modifica salvata.")
    else:
        conn.commit()
        print("\nCommit eseguito.")
        verify(cursor)
        print("\n=== Setup Sprint 0 completato ===")
        print("Passi manuali rimanenti:")
        print("  1. Assegnare le due chiavi agli utenti dalla GUI permessi (submenu_permissions)")
        print("  2. Compilare i destinatari in Sys_email_Kit_materiali (se non passati con --emails)")
        print("  3. Attivare le postazioni popup con 'WH WorkStation' (wh_workstation_config.py)")
    conn.close()


if __name__ == '__main__':
    main()
