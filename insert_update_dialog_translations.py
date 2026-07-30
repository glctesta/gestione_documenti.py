# -*- coding: utf-8 -*-
"""Traduzioni mancanti della finestra "Aggiornamento Pronto".

Queste 4 chiavi non esistevano in NESSUNA lingua, quindi la finestra cadeva sul
testo di default italiano hardcoded anche con il PC impostato in rumeno.

I segnaposto {0}/{1} sono voluti: i punti di chiamata usano App._t_fmt(), che
prende il template da lang.get_raw() e lo formatta una sola volta. NON usare
lang.get(key, default) su queste chiavi: se la chiave esiste, get() passa il
default a .format() e il segnaposto verrebbe rimpiazzato dal testo di default.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('update_ready_head',
     'Aggiornamento alla versione {0} pronto.',
     'Update to version {0} is ready.',
     'Actualizarea la versiunea {0} este pregătită.',
     'Update auf Version {0} ist bereit.',
     'Uppdatering till version {0} är klar.'),
    ('update_whatsnew',
     'Novità di questa versione:',
     "What's new in this version:",
     'Noutățile acestei versiuni:',
     'Neuigkeiten dieser Version:',
     'Nyheter i den här versionen:'),
    ('update_countdown_msg',
     "L'aggiornamento partirà automaticamente tra {0:02d}:{1:02d}.\n"
     'Salvare il lavoro nelle finestre aperte.',
     'The update will start automatically in {0:02d}:{1:02d}.\n'
     'Please save your work in any open windows.',
     'Actualizarea va porni automat în {0:02d}:{1:02d}.\n'
     'Salvați lucrul din fereastrele deschise.',
     'Das Update startet automatisch in {0:02d}:{1:02d}.\n'
     'Bitte speichern Sie Ihre Arbeit in offenen Fenstern.',
     'Uppdateringen startar automatiskt om {0:02d}:{1:02d}.\n'
     'Spara ditt arbete i öppna fönster.'),
    ('update_postpone_btn',
     '⏱ Posticipa {0} min ({1} rimasti)',
     '⏱ Postpone {0} min ({1} left)',
     '⏱ Amână {0} min ({1} rămase)',
     '⏱ {0} Min. verschieben ({1} übrig)',
     '⏱ Skjut upp {0} min ({1} kvar)'),
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
    print(f"[OK] Update dialog translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
