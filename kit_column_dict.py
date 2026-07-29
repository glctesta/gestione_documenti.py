# -*- coding: utf-8 -*-
"""
kit_column_dict.py — Dizionario delle intestazioni di colonna per i file di
kitting (T:\\KITTING).

I file Excel di kitting arrivano in formati diversi (multi-job Essegi, D365, e
varianti) con le colonne in posizioni e con nomi differenti. Invece di mappare
posizioni fisse, il parser cerca le intestazioni tramite un DIZIONARIO di alias
per ogni campo logico:
  - unique_number : codice bobina (REEL CODE)
  - material_code : codice materiale (ITEM CODE)
  - quantity      : quantita' (QT / QUANTITY)

Gli alias di default sono nel codice; alias aggiuntivi (per formati nuovi) si
aggiungono dalla maschera di mappatura e vengono salvati in
dbo.KitColumnAliases, così il sistema "impara" i nuovi formati senza bloccarsi.
"""

import logging

logger = logging.getLogger("PlanMonitor")

# Campi logici richiesti in ogni file di kitting.
REQUIRED_FIELDS = ('unique_number', 'material_code', 'quantity')

# Etichette leggibili (per la maschera di mappatura).
FIELD_LABELS = {
    'unique_number': 'Codice bobina (REEL CODE)',
    'material_code': 'Codice materiale (ITEM CODE)',
    'quantity':      'Quantità (QT / QUANTITY)',
}

# Nome canonico usato per il matching fuzzy quando manca l'alias.
FIELD_CANON = {
    'unique_number': 'REEL CODE',
    'material_code': 'ITEM CODE',
    'quantity':      'QUANTITY',
}

# Alias di default (sempre attivi). In MAIUSCOLO, confronto per uguaglianza esatta
# (trim + upper). NB: la quantita' NON deve includere 'UNLOAD Q.TY' / 'REMAINING Q.TY'
# / 'Q.TY' dei file D365: solo la colonna del fabbisogno ('QT' multi-job, 'QUANTITY' D365).
DEFAULT_ALIASES = {
    'unique_number': ['REEL CODE'],
    'material_code': ['ITEM CODE'],
    'quantity':      ['QT', 'QUANTITY', 'QTY'],
}


def ensure_table(conn) -> None:
    """Crea dbo.KitColumnAliases se non esiste (idempotente)."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                IF OBJECT_ID('traceability_rs.dbo.KitColumnAliases', 'U') IS NULL
                CREATE TABLE traceability_rs.dbo.KitColumnAliases (
                    Id           INT IDENTITY(1,1) PRIMARY KEY,
                    LogicalField NVARCHAR(40)  NOT NULL,
                    Alias        NVARCHAR(100) NOT NULL,
                    AddedBy      NVARCHAR(255) NULL,
                    AddedDate    DATETIME NOT NULL DEFAULT GETDATE()
                );
            """)
        conn.commit()
    except Exception as e:
        logger.error(f"kit_column_dict.ensure_table: {e}", exc_info=True)


def load_aliases(conn) -> dict:
    """Ritorna il dizionario field -> lista di alias (MAIUSCOLO), unione di
    DEFAULT_ALIASES e degli alias salvati in DB. Robusto: se il DB non è
    raggiungibile ritorna comunque i default."""
    merged = {k: set(a.upper() for a in v) for k, v in DEFAULT_ALIASES.items()}
    try:
        ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT LogicalField, Alias FROM traceability_rs.dbo.KitColumnAliases")
            for r in cur.fetchall():
                fld = (r.LogicalField or '').strip()
                al = (r.Alias or '').strip().upper()
                if fld and al:
                    merged.setdefault(fld, set()).add(al)
    except Exception as e:
        logger.warning(f"load_aliases: uso i default ({e})")
    return {k: sorted(v) for k, v in merged.items()}


def add_alias(conn, field: str, alias: str, user: str = None) -> bool:
    """Aggiunge un alias per un campo logico (evita duplicati, case-insensitive)."""
    field = (field or '').strip()
    alias = (alias or '').strip()
    if not field or not alias:
        return False
    try:
        ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO traceability_rs.dbo.KitColumnAliases (LogicalField, Alias, AddedBy)
                SELECT ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM traceability_rs.dbo.KitColumnAliases
                    WHERE LogicalField = ? AND UPPER(Alias) = UPPER(?)
                )
            """, (field, alias, user or None, field, alias))
        conn.commit()
        logger.info("KitColumnAliases: aggiunto alias %r per %r (da %s)", alias, field, user)
        return True
    except Exception as e:
        logger.error(f"add_alias: {e}", exc_info=True)
        return False


def list_aliases(conn) -> list:
    """Elenco completo (per una eventuale vista di gestione)."""
    try:
        ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT Id, LogicalField, Alias, AddedBy, AddedDate "
                        "FROM traceability_rs.dbo.KitColumnAliases ORDER BY LogicalField, Alias")
            return [{'id': r.Id, 'field': r.LogicalField, 'alias': r.Alias,
                     'added_by': r.AddedBy, 'added_date': r.AddedDate}
                    for r in cur.fetchall()]
    except Exception as e:
        logger.error(f"list_aliases: {e}", exc_info=True)
        return []
