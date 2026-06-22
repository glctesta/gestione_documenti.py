# -*- coding: utf-8 -*-
"""
insert_scrap_validation_translations.py
Traduzioni per: voce menu "Convalida Quantità Dichiarate", pannello di convalida
scorie (scrap_returns_gui) e messaggio di blocco prep/rilascio.
5 lingue (it, en, ro, de, sv). Idempotente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('submenu_validate_scrap',
     '✔ Convalida Quantità Dichiarate', '✔ Validate Declared Quantities',
     '✔ Validare Cantități Declarate', '✔ Deklarierte Mengen validieren',
     '✔ Validera deklarerade kvantiteter'),
    ('ind_req_scrap_not_confirmed',
     'Impossibile procedere: le scorie/rientri collegati a questo materiale non sono stati '
     'confermati dal controllore.\nUsare "Convalida Quantità Dichiarate" per confermarli.',
     'Cannot proceed: the scrap/returns linked to this material have not been confirmed by '
     'the controller.\nUse "Validate Declared Quantities" to confirm them.',
     'Imposibil de continuat: deșeurile/retururile legate de acest material nu au fost '
     'confirmate de controlor.\nFolosiți "Validare Cantități Declarate" pentru a le confirma.',
     'Nicht möglich: Der mit diesem Material verknüpfte Ausschuss/die Rückgaben wurden vom '
     'Prüfer nicht bestätigt.\nVerwenden Sie "Deklarierte Mengen validieren".',
     'Kan inte fortsätta: skrot/returer kopplade till detta material har inte bekräftats av '
     'kontrollanten.\nAnvänd "Validera deklarerade kvantiteter" för att bekräfta dem.'),
    ('scrap_col_confirmed', 'Convalida', 'Validation', 'Validare', 'Validierung', 'Validering'),
    ('scrap_validate_panel',
     'Convalida quantità dichiarata (controllo)', 'Validate declared quantity (control)',
     'Validare cantitate declarată (control)', 'Deklarierte Menge validieren (Kontrolle)',
     'Validera deklarerad kvantitet (kontroll)'),
    ('scrap_confirmed_weight', 'Peso rilevato (kg):', 'Measured weight (kg):',
     'Greutate măsurată (kg):', 'Gemessenes Gewicht (kg):', 'Uppmätt vikt (kg):'),
    ('scrap_btn_validate', '✔ Convalida selezionata', '✔ Validate selected',
     '✔ Validează selectarea', '✔ Auswahl validieren', '✔ Validera vald'),
    ('scrap_to_confirm', 'Da confermare', 'To confirm', 'De confirmat', 'Zu bestätigen',
     'Att bekräfta'),
    ('scrap_confirmed_ok', '✔ OK ({0} kg)', '✔ OK ({0} kg)', '✔ OK ({0} kg)',
     '✔ OK ({0} kg)', '✔ OK ({0} kg)'),
    ('scrap_confirmed_ko', 'X NON conforme ({0} kg)', 'X NOT compliant ({0} kg)',
     'X NEconform ({0} kg)', 'X NICHT konform ({0} kg)', 'X EJ överensstämmande ({0} kg)'),
    ('scrap_select_row', 'Seleziona una registrazione da convalidare.',
     'Select a record to validate.', 'Selectați o înregistrare de validat.',
     'Wählen Sie einen Eintrag zur Validierung.', 'Välj en post att validera.'),
    ('scrap_mismatch_confirm',
     'Il peso rilevato ({0} kg) NON corrisponde al dichiarato ({1} kg).\nRegistrare comunque come NON conforme?',
     'The measured weight ({0} kg) does NOT match the declared one ({1} kg).\nRecord anyway as NOT compliant?',
     'Greutatea măsurată ({0} kg) NU corespunde celei declarate ({1} kg).\nÎnregistrați oricum ca NEconform?',
     'Das gemessene Gewicht ({0} kg) stimmt NICHT mit dem deklarierten ({1} kg) überein.\nTrotzdem als NICHT konform erfassen?',
     'Den uppmätta vikten ({0} kg) matchar INTE den deklarerade ({1} kg).\nRegistrera ändå som EJ överensstämmande?'),
    ('scrap_validated_ok', 'Convalida registrata.', 'Validation recorded.',
     'Validare înregistrată.', 'Validierung erfasst.', 'Validering registrerad.'),
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
    conn.commit()
    conn.close()
    print(f"[OK] Scrap validation translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
