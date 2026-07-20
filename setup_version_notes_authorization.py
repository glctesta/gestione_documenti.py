# -*- coding: utf-8 -*-
"""
setup_version_notes_authorization.py

Registra la chiave di autorizzazione dell'editor note di versione in
AppTranslations con MenuValue valorizzato, così compare nella form permessi e può
essere concessa agli utenti (di norma al programmatore):

  - gestisci_note_versione : redazione/salvataggio note di versione (bozza AI da git)

fetch_available_permissions elenca solo le TranslationKey con MenuValue IS NOT NULL;
grant_permission valida l'esistenza del MenuValue su languagecode='it'. Idempotente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

KEYS = {
    'gestisci_note_versione': {
        'it': ('Redigi note di versione', 'Redigi note di versione'),
        'en': ('Edit version release notes', 'Edit version release notes'),
        'ro': ('Redactează notele de versiune', 'Redactează notele de versiune'),
        'de': ('Versions-Release-Notes bearbeiten', 'Versions-Release-Notes bearbeiten'),
        'sv': ('Redigera versionsanteckningar', 'Redigera versionsanteckningar'),
    },
}


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    ins = upd = 0
    for key, langs in KEYS.items():
        for lang, (tval, mval) in langs.items():
            cur.execute("SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                        "WHERE LanguageCode=? AND TranslationKey=?", (lang, key))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO Traceability_rs.dbo.AppTranslations "
                            "(LanguageCode, TranslationKey, TranslationValue, MenuValue) "
                            "VALUES (?, ?, ?, ?)", (lang, key, tval, mval))
                ins += 1
            else:
                cur.execute("UPDATE Traceability_rs.dbo.AppTranslations SET MenuValue=? "
                            "WHERE LanguageCode=? AND TranslationKey=? AND (MenuValue IS NULL OR MenuValue='')",
                            (mval, lang, key))
                upd += cur.rowcount
    conn.commit()
    conn.close()
    print(f"[OK] Chiave autorizzazione note versione - Inserite: {ins}, MenuValue aggiornati: {upd}")


if __name__ == '__main__':
    main()
