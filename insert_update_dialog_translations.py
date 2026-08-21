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
     "L'aggiornamento partirà automaticamente tra {0}.\n"
     'Salvare il lavoro nelle finestre aperte.',
     'The update will start automatically in {0}.\n'
     'Please save your work in any open windows.',
     'Actualizarea va porni automat în {0}.\n'
     'Salvați lucrul din fereastrele deschise.',
     'Das Update startet automatisch in {0}.\n'
     'Bitte speichern Sie Ihre Arbeit in offenen Fenstern.',
     'Uppdateringen startar automatiskt om {0}.\n'
     'Spara ditt arbete i öppna fönster.'),
    ('update_postpone_btn',
     '⏱ Posticipa {0} min ({1} rimasti)',
     '⏱ Postpone {0} min ({1} left)',
     '⏱ Amână {0} min ({1} rămase)',
     '⏱ {0} Min. verschieben ({1} übrig)',
     '⏱ Skjut upp {0} min ({1} kvar)'),
    # Nuove chiavi dialogo moderno
    ('update_ready_title',
     'Nuova versione pronta!',
     'New version ready!',
     'Versiune nouă pregătită!',
     'Neue Version bereit!',
     'Ny version redo!'),
    ('update_install_now_btn',
     'Installa ora',
     'Install now',
     'Instalează acum',
     'Jetzt installieren',
     'Installera nu'),
    ('update_ready_msg',
     'Tutto pronto: premi "Installa ora" per aggiornare.',
     'Everything is ready: click "Install now" to update.',
     'Totul este pregătit: apăsați "Instalează acum" pentru a actualiza.',
     'Alles bereit: Klicken Sie auf "Jetzt installieren", um zu aktualisieren.',
     'Allt är klart: klicka på "Installera nu" för att uppdatera.'),
    ('update_new_version_title',
     'È disponibile una nuova versione!',
     'New version is available!',
     'O nouă versiune este disponibilă!',
     'Neue Version verfügbar!',
     'Ny version är tillgänglig!'),
    ('update_current_version',
     'Versione corrente:',
     'Current version:',
     'Versiunea curentă:',
     'Aktuelle Version:',
     'Aktuell version:'),
    ('update_new_version',
     'Nuova versione:',
     'New version:',
     'Versiune nouă:',
     'Neue Version:',
     'Ny version:'),
    ('update_whatsnew_link',
     "Cosa c'è di nuovo?",
     "What's New?",
     'Ce este nou?',
     'Was ist neu?',
     'Vad är nytt?'),
    ('update_whatsnew_title',
     'Novità della versione',
     'Version Release Notes',
     'Noutăți ale versiunii',
     'Neuigkeiten der Version',
     'Versionsnyheter'),
    ('update_download_btn',
     'Download', 'Download', 'Descărcare', 'Herunterladen', 'Ladda ner'),
    ('update_skip_later_btn',
     'Skip Later', 'Skip Later', 'Amână', 'Später überspringen', 'Hoppa över'),
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
