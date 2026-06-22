# -*- coding: utf-8 -*-
"""Traduzioni aggiuntive FQC: checkbox 'solo con piano' + filtro Ordine nel report."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('fqc_only_with_plan',
     'Solo codici con piano di verifica caricato', 'Only codes with a verification plan',
     'Doar coduri cu plan de verificare', 'Nur Codes mit Prüfplan',
     'Endast koder med kontrollplan'),
    ('fqc_report_order', 'Ordine:', 'Order:', 'Comandă:', 'Auftrag:', 'Order:'),
]
LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    ins = skip = 0
    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            cur.execute("SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                        "WHERE LanguageCode = ? AND TranslationKey = ?", (lang, key))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO Traceability_rs.dbo.AppTranslations "
                            "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                            (lang, key, row[i + 1]))
                ins += 1
            else:
                skip += 1
    conn.commit(); conn.close()
    print(f"[OK] FQC extra translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
