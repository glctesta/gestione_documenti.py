# -*- coding: utf-8 -*-
"""Traduzioni mancanti in TUTTE le lingue, trovate con un audit di main.py.

Queste chiavi erano usate con self.lang.get(chiave, 'testo italiano') ma non
esistevano in nessuna lingua: a video compariva sempre il default italiano,
qualunque fosse la lingua impostata sul PC. Riguardano soprattutto le finestre
del flusso di aggiornamento (preparazione, passaggio di consegne) e alcune voci
di menu.

NB: update_handoff_title contiene {0} (numero di versione). Il punto di chiamata
usa App._t_fmt(), NON lang.get(key, default).format(...): con la traduzione
presente get() passerebbe il default a .format() e {0} verrebbe sostituito dal
testo di default. Vedi anche insert_update_dialog_translations.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    # --- finestra "preparazione aggiornamento" -------------------------------
    ('update_prep_title',
     'Aggiornamento', 'Update', 'Actualizare', 'Aktualisierung', 'Uppdatering'),
    ('update_prep_msg',
     "Preparazione dell'aggiornamento in corso...\n"
     'Attendere: caricamento dei dati aggiornati.\n'
     "Non chiudere l'applicazione.",
     'Preparing the update...\n'
     'Please wait: loading the updated data.\n'
     'Do not close the application.',
     'Se pregătește actualizarea...\n'
     'Așteptați: se încarcă datele actualizate.\n'
     'Nu închideți aplicația.',
     'Update wird vorbereitet...\n'
     'Bitte warten: aktualisierte Daten werden geladen.\n'
     'Schließen Sie die Anwendung nicht.',
     'Uppdateringen förbereds...\n'
     'Vänta: uppdaterade data laddas.\n'
     'Stäng inte programmet.'),
    # --- overlay "passaggio di consegne" all'updater -------------------------
    ('update_handoff_title',
     'Avvio aggiornamento alla versione {0}...',
     'Starting update to version {0}...',
     'Se pornește actualizarea la versiunea {0}...',
     'Update auf Version {0} wird gestartet...',
     'Startar uppdatering till version {0}...'),
    ('update_handoff_msg',
     "L'applicazione si chiuderà e ripartirà automaticamente.\n"
     'Non spegnere il PC e non chiudere questa finestra.',
     'The application will close and restart automatically.\n'
     'Do not turn off the PC and do not close this window.',
     'Aplicația se va închide și va reporni automat.\n'
     'Nu opriți PC-ul și nu închideți această fereastră.',
     'Die Anwendung wird geschlossen und automatisch neu gestartet.\n'
     'Schalten Sie den PC nicht aus und schließen Sie dieses Fenster nicht.',
     'Programmet stängs och startar om automatiskt.\n'
     'Stäng inte av datorn och stäng inte detta fönster.'),
    # --- voci di menu / messaggi che restavano in italiano -------------------
    ('menu_version_notes',
     '🆕 Registro modifiche (Novità)', '🆕 Change log (What\'s new)',
     '🆕 Registru modificări (Noutăți)', '🆕 Änderungsprotokoll (Neuigkeiten)',
     '🆕 Ändringslogg (Nyheter)'),
    ('menu_version_notes_editor',
     '📝 Redigi note versione...', '📝 Edit version notes...',
     '📝 Redactează notele versiunii...', '📝 Versionshinweise bearbeiten...',
     '📝 Redigera versionsanteckningar...'),
    ('piano_produzione_responsabili',
     'Piano produzione — Responsabili', 'Production plan — Responsibles',
     'Plan de producție — Responsabili', 'Produktionsplan — Verantwortliche',
     'Produktionsplan — Ansvariga'),
    ('piano_produzione_fasi',
     'Piano produzione — Fasi da giustificare',
     'Production plan — Phases to justify',
     'Plan de producție — Faze de justificat',
     'Produktionsplan — Zu begründende Phasen',
     'Produktionsplan — Faser att motivera'),
    ('menu_consumption_general_report',
     'Report Consumi Generale', 'General Consumption Report',
     'Raport general consumuri', 'Allgemeiner Verbrauchsbericht',
     'Allmän förbrukningsrapport'),
    ('cgr_open_err',
     'Impossibile aprire il report consumi',
     'Cannot open the consumption report',
     'Nu se poate deschide raportul de consumuri',
     'Verbrauchsbericht kann nicht geöffnet werden',
     'Det går inte att öppna förbrukningsrapporten'),
    ('submenu_labels_ei_aros',
     'Etichette EI → Aros', 'EI → Aros labels', 'Etichete EI → Aros',
     'EI → Aros Etiketten', 'EI → Aros-etiketter'),
    ('ei_aros_open_err',
     'Impossibile aprire Etichette EI → Aros',
     'Cannot open EI → Aros labels',
     'Nu se poate deschide Etichete EI → Aros',
     'EI → Aros Etiketten können nicht geöffnet werden',
     'Det går inte att öppna EI → Aros-etiketter'),
    ('error_running_from_source_message',
     "L'applicazione non può essere eseguita direttamente dal percorso sorgente "
     'sul server.\n\nSi prega di lanciare la copia installata localmente.',
     'The application cannot be run directly from the source path on the server.'
     '\n\nPlease launch the locally installed copy.',
     'Aplicația nu poate fi rulată direct din calea sursă de pe server.'
     '\n\nVă rugăm să lansați copia instalată local.',
     'Die Anwendung kann nicht direkt vom Quellpfad auf dem Server ausgeführt '
     'werden.\n\nBitte starten Sie die lokal installierte Kopie.',
     'Programmet kan inte köras direkt från källsökvägen på servern.'
     '\n\nStarta den lokalt installerade kopian.'),
    ('npi_manual_general',
     'NPI Management', 'NPI Management', 'Management NPI',
     'NPI-Management', 'NPI-hantering'),
    ('npi_manual_checklist',
     'NPI Checklist (MD.RAQ.089)', 'NPI Checklist (MD.RAQ.089)',
     'Checklist NPI (MD.RAQ.089)', 'NPI-Checkliste (MD.RAQ.089)',
     'NPI-checklista (MD.RAQ.089)'),
    ('fai_autocheck_manual',
     'FAI Autocheck (Manuale)', 'FAI Autocheck (Manual)',
     'FAI Autocheck (Manual)', 'FAI Autocheck (Handbuch)',
     'FAI Autocheck (Manual)'),
    ('manual_plan_discrepancy',
     'Discrepanze Piano Produzione', 'Production Plan Discrepancies',
     'Discrepanțe Plan Producție', 'Abweichungen Produktionsplan',
     'Avvikelser produktionsplan'),
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
    print(f"[OK] Missing UI translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
