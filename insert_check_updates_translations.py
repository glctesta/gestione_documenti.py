# -*- coding: utf-8 -*-
"""Traduzioni per la voce di menu Aiuto > Verifica nuova versione.

NB: le stringhe NON contengono segnaposto {0}. LanguageManager.get(key, *args)
usa il 2o argomento come testo di fallback solo se la chiave manca, altrimenti
lo passa a .format(): con un segnaposto il messaggio verrebbe corrotto. I numeri
di versione sono concatenati dal codice chiamante.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('menu_check_updates',
     '⬆ Verifica nuova versione...',
     '⬆ Check for a new version...',
     '⬆ Verifică versiune nouă...',
     '⬆ Nach neuer Version suchen...',
     '⬆ Sök efter ny version...'),
    ('check_updates_title',
     'Verifica aggiornamenti', 'Check for updates', 'Verificare actualizări',
     'Nach Updates suchen', 'Sök uppdateringar'),
    ('check_updates_unavailable',
     'Non è stato possibile verificare la disponibilità di aggiornamenti.\n'
     'Nessuna informazione di versione trovata per questo programma.',
     'Could not check for updates.\n'
     'No version information found for this program.',
     'Nu s-a putut verifica disponibilitatea actualizărilor.\n'
     'Nu s-au găsit informații de versiune pentru acest program.',
     'Die Verfügbarkeit von Updates konnte nicht geprüft werden.\n'
     'Keine Versionsinformationen für dieses Programm gefunden.',
     'Det gick inte att kontrollera om det finns uppdateringar.\n'
     'Ingen versionsinformation hittades för detta program.'),
    ('check_updates_up_to_date',
     'Il programma è aggiornato.',
     'The application is up to date.',
     'Programul este actualizat.',
     'Das Programm ist aktuell.',
     'Programmet är uppdaterat.'),
    ('check_updates_installed_label',
     'Versione installata:', 'Installed version:', 'Versiune instalată:',
     'Installierte Version:', 'Installerad version:'),
    ('check_updates_new_label',
     'Nuova versione:', 'New version:', 'Versiune nouă:',
     'Neue Version:', 'Ny version:'),
    ('check_updates_available',
     'È disponibile una nuova versione.',
     'A new version is available.',
     'Este disponibilă o versiune nouă.',
     'Eine neue Version ist verfügbar.',
     'En ny version är tillgänglig.'),
    ('check_updates_download_question',
     'Vuoi scaricarla e installarla adesso?',
     'Do you want to download and install it now?',
     'Doriți să o descărcați și să o instalați acum?',
     'Möchten Sie sie jetzt herunterladen und installieren?',
     'Vill du ladda ner och installera den nu?'),
    ('check_updates_not_ready',
     'I file di aggiornamento non sono ancora pronti sul server.\n'
     'Riprovare più tardi.',
     'The update files are not ready on the server yet.\n'
     'Please try again later.',
     'Fișierele de actualizare nu sunt încă pregătite pe server.\n'
     'Încercați mai târziu.',
     'Die Update-Dateien sind auf dem Server noch nicht bereit.\n'
     'Bitte später erneut versuchen.',
     'Uppdateringsfilerna är inte klara på servern än.\n'
     'Försök igen senare.'),
    ('check_updates_error',
     'Errore durante la verifica degli aggiornamenti:',
     'Error while checking for updates:',
     'Eroare la verificarea actualizărilor:',
     'Fehler bei der Update-Prüfung:',
     'Fel vid kontroll av uppdateringar:'),
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
    print(f"[OK] Check updates translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
