# -*- coding: utf-8 -*-
"""Traduzioni menu/titoli Touch-up (le restanti stringhe dei form usano i default italiani)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('menu_touchup', 'Touch-up', 'Touch-up', 'Touch-up', 'Touch-up', 'Touch-up'),
    ('menu_touchup_problems', 'Problemi rivelati', 'Detected problems', 'Probleme detectate',
     'Erkannte Probleme', 'Upptäckta problem'),
    ('menu_touchup_responses', 'Soluzioni adottate', 'Solutions taken', 'Soluții adoptate',
     'Ergriffene Lösungen', 'Vidtagna lösningar'),
    ('menu_touchup_reports', 'Rapporti', 'Reports', 'Rapoarte', 'Berichte', 'Rapporter'),
    ('menu_touchup_workstation', 'Setup workstation', 'Workstation setup', 'Setare workstation',
     'Workstation-Einrichtung', 'Arbetsstationsinställning'),
    ('menu_touchup_setup', 'Gestione', 'Management', 'Gestionare', 'Verwaltung', 'Hantering'),
    ('tuop_title', 'Touch-Up - Problemi rivelati', 'Touch-Up - Detected problems',
     'Touch-Up - Probleme detectate', 'Touch-Up - Erkannte Probleme', 'Touch-Up - Upptäckta problem'),
    ('ture_title', 'Touch-Up - Soluzioni adottate', 'Touch-Up - Solutions taken',
     'Touch-Up - Soluții adoptate', 'Touch-Up - Ergriffene Lösungen', 'Touch-Up - Vidtagna lösningar'),
    ('tuset_title', 'Touch-Up - Gestione', 'Touch-Up - Management', 'Touch-Up - Gestionare',
     'Touch-Up - Verwaltung', 'Touch-Up - Hantering'),
    ('tuws_title', 'Postazione Touch-Up - Setup', 'Touch-Up Workstation - Setup',
     'Stație Touch-Up - Setare', 'Touch-Up-Arbeitsplatz - Setup', 'Touch-Up-station - inställning'),
    ('touchup_reports_soon', 'Sezione Rapporti Touch-up in arrivo.', 'Touch-up Reports section coming soon.',
     'Secțiunea Rapoarte Touch-up în curând.', 'Touch-up-Berichte folgen in Kürze.',
     'Touch-up-rapporter kommer snart.'),
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
    print(f"[OK] Touch-up translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
