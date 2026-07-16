# -*- coding: utf-8 -*-
"""
insert_scrap_override_translations.py
Traduzioni per l'azione "Forza conforme" (override supervisore) nel pannello di
convalida scorie (scrap_returns_gui): pulsante, prompt motivazione e messaggi.
5 lingue (it, en, ro, de, sv). Idempotente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('scrap_btn_override', '⚠ Forza conforme', '⚠ Force compliant',
     '⚠ Forțează conform', '⚠ Als konform erzwingen', '⚠ Tvinga överensstämmande'),
    ('scrap_confirmed_override', '✔ Forzato ({0} kg)', '✔ Forced ({0} kg)',
     '✔ Forțat ({0} kg)', '✔ Erzwungen ({0} kg)', '✔ Tvingad ({0} kg)'),
    ('scrap_override_title', 'Forza conforme', 'Force compliant',
     'Forțează conform', 'Als konform erzwingen', 'Tvinga överensstämmande'),
    ('scrap_override_reason', 'Motivazione (obbligatoria):', 'Reason (mandatory):',
     'Motiv (obligatoriu):', 'Begründung (Pflicht):', 'Orsak (obligatorisk):'),
    ('scrap_override_reason_required', 'La motivazione è obbligatoria.',
     'The reason is mandatory.', 'Motivul este obligatoriu.',
     'Die Begründung ist Pflicht.', 'Orsaken är obligatorisk.'),
    ('scrap_override_confirm',
     'Forzare la riga come CONFORME? La richiesta collegata potrà essere rilasciata.',
     'Force the record as COMPLIANT? The linked request will be releasable.',
     'Forțați înregistrarea ca CONFORMĂ? Cererea legată va putea fi eliberată.',
     'Eintrag als KONFORM erzwingen? Die verknüpfte Anforderung wird freigebbar.',
     'Tvinga posten som ÖVERENSSTÄMMANDE? Den kopplade begäran kan då frisläppas.'),
    ('scrap_override_done', 'Override registrato. La riga è ora conforme.',
     'Override recorded. The record is now compliant.',
     'Suprascriere înregistrată. Înregistrarea este acum conformă.',
     'Übersteuerung erfasst. Der Eintrag ist jetzt konform.',
     'Åsidosättning registrerad. Posten är nu överensstämmande.'),
    ('scrap_override_already_ok', 'La riga è già conforme.', 'The record is already compliant.',
     'Înregistrarea este deja conformă.', 'Der Eintrag ist bereits konform.',
     'Posten är redan överensstämmande.'),
    ('scrap_override_only_ko',
     "L'override si applica solo alle righe NON conformi.\nConvalida prima la riga con il peso rilevato.",
     'Override applies only to NON compliant records.\nValidate the record with the measured weight first.',
     'Suprascrierea se aplică doar înregistrărilor NEconforme.\nValidați mai întâi înregistrarea cu greutatea măsurată.',
     'Die Übersteuerung gilt nur für NICHT konforme Einträge.\nValidieren Sie den Eintrag zuerst mit dem gemessenen Gewicht.',
     'Åsidosättning gäller endast EJ överensstämmande poster.\nValidera posten med uppmätt vikt först.'),
    ('scrap_override_no_auth', 'Funzione di autorizzazione non disponibile.',
     'Authorization function not available.', 'Funcția de autorizare nu este disponibilă.',
     'Autorisierungsfunktion nicht verfügbar.', 'Auktoriseringsfunktion ej tillgänglig.'),
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
    print(f"[OK] Scrap override translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
