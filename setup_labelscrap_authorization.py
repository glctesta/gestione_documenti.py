# -*- coding: utf-8 -*-
"""
setup_labelscrap_authorization.py

Registra le due chiavi di autorizzazione degli scarti etichette in AppTranslations
con MenuValue valorizzato, così compaiono nella form permessi (permissions_gui) e
possono essere concesse agli utenti:

  - aggiungi_motivo_label_scrap  : gestione motivi scarto etichette (nella form)
  - setta_pc_report_labelscrap   : designazione PC di stampa scarti etichette

fetch_available_permissions elenca solo le TranslationKey con MenuValue IS NOT NULL;
grant_permission valida l'esistenza del MenuValue su languagecode='it'. Idempotente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

# key -> {lang: (TranslationValue, MenuValue)}
KEYS = {
    'aggiungi_motivo_label_scrap': {
        'it': ('Aggiungi motivo scarto etichette', 'Aggiungi motivo scarto etichette'),
        'en': ('Add label scrap reason', 'Add label scrap reason'),
        'ro': ('Adaugă motiv rebut etichete', 'Adaugă motiv rebut etichete'),
        'de': ('Etiketten-Ausschussgrund hinzufügen', 'Etiketten-Ausschussgrund hinzufügen'),
        'sv': ('Lägg till orsak etikettkassation', 'Lägg till orsak etikettkassation'),
    },
    'setta_pc_report_labelscrap': {
        'it': ('Imposta PC stampa scarti etichette', 'Imposta PC stampa scarti etichette'),
        'en': ('Set label scrap print PC', 'Set label scrap print PC'),
        'ro': ('Setează PC tipărire rebuturi etichete', 'Setează PC tipărire rebuturi etichete'),
        'de': ('Etiketten-Ausschussdruck-PC festlegen', 'Etiketten-Ausschussdruck-PC festlegen'),
        'sv': ('Ställ in PC för etikettkassationsutskrift', 'Ställ in PC för etikettkassationsutskrift'),
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
                # assicura che MenuValue sia valorizzato (rende la chiave concedibile)
                cur.execute("UPDATE Traceability_rs.dbo.AppTranslations SET MenuValue=? "
                            "WHERE LanguageCode=? AND TranslationKey=? AND (MenuValue IS NULL OR MenuValue='')",
                            (mval, lang, key))
                upd += cur.rowcount
    conn.commit()
    conn.close()
    print(f"[OK] Chiavi autorizzazione labelscrap - Inserite: {ins}, MenuValue aggiornati: {upd}")


if __name__ == '__main__':
    main()
