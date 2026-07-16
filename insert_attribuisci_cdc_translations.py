# -*- coding: utf-8 -*-
"""
insert_attribuisci_cdc_translations.py
Traduzioni per la form "Attribuisci CDC" (attribuisci_cdc_gui) e la voce di menu
Strumenti. 5 lingue (it, en, ro, de, sv). Idempotente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('submenu_attribuisci_cdc', 'Attribuisci cdc', 'Assign cdc', 'Atribuie cdc',
     'CDC zuweisen', 'Tilldela cdc'),
    ('acdc_title', 'Attribuisci CDC', 'Assign CDC', 'Atribuie CDC', 'CDC zuweisen', 'Tilldela CDC'),
    ('acdc_open_error', 'Impossibile aprire Attribuisci CDC', 'Cannot open Assign CDC',
     'Nu se poate deschide Atribuie CDC', 'CDC zuweisen kann nicht geöffnet werden',
     'Kan inte öppna Tilldela CDC'),
    ('acdc_no_head_story',
     'Impossibile determinare reparto/funzione del responsabile loggato.',
     'Cannot determine the logged-in manager\'s department/function.',
     'Nu se poate determina departamentul/funcția managerului conectat.',
     'Abteilung/Funktion des angemeldeten Vorgesetzten kann nicht ermittelt werden.',
     'Kan inte fastställa den inloggade chefens avdelning/funktion.'),
    ('acdc_all_departments', 'Tutti i reparti', 'All departments', 'Toate departamentele',
     'Alle Abteilungen', 'Alla avdelningar'),
    ('acdc_dept_info', 'Reparto: {0}   —   Responsabile: {1}',
     'Department: {0}   —   Manager: {1}', 'Departament: {0}   —   Responsabil: {1}',
     'Abteilung: {0}   —   Vorgesetzter: {1}', 'Avdelning: {0}   —   Chef: {1}'),
    ('acdc_filters', 'Filtri', 'Filters', 'Filtre', 'Filter', 'Filter'),
    ('acdc_filter_name', 'Cognome / Nome:', 'Surname / Name:', 'Nume / Prenume:',
     'Nachname / Vorname:', 'Efternamn / Namn:'),
    ('acdc_filter_subcdc', 'Sotto-reparto:', 'Sub-department:', 'Sub-departament:',
     'Unterabteilung:', 'Underavdelning:'),
    ('acdc_search', '🔍 Cerca', '🔍 Search', '🔍 Caută', '🔍 Suchen', '🔍 Sök'),
    ('acdc_col_employee', 'Dipendente', 'Employee', 'Angajat', 'Mitarbeiter', 'Anställd'),
    ('acdc_col_subcdc', 'Sotto-reparto attuale', 'Current sub-department', 'Sub-departament curent',
     'Aktuelle Unterabteilung', 'Nuvarande underavdelning'),
    ('acdc_col_function', 'Funzione', 'Function', 'Funcție', 'Funktion', 'Funktion'),
    ('acdc_col_fcode', 'Cod.Funz.', 'Func.Code', 'Cod Funcție', 'Funk.Code', 'Funk.kod'),
    ('acdc_reassign', 'Riassegnazione sotto-reparto', 'Sub-department reassignment',
     'Reatribuire sub-departament', 'Neuzuweisung Unterabteilung', 'Omfördelning av underavdelning'),
    ('acdc_current_cdc', 'Reparto (non modificabile):', 'Department (not editable):',
     'Departament (nemodificabil):', 'Abteilung (nicht änderbar):', 'Avdelning (ej redigerbar):'),
    ('acdc_current_function', 'Funzione (non modificabile):', 'Function (not editable):',
     'Funcție (nemodificabilă):', 'Funktion (nicht änderbar):', 'Funktion (ej redigerbar):'),
    ('acdc_new_subcdc', 'Nuovo sotto-reparto:', 'New sub-department:', 'Nou sub-departament:',
     'Neue Unterabteilung:', 'Ny underavdelning:'),
    ('acdc_btn_save', '💾 Salva riassegnazione', '💾 Save reassignment', '💾 Salvează reatribuirea',
     '💾 Neuzuweisung speichern', '💾 Spara omfördelning'),
    ('acdc_select_employee', 'Seleziona un dipendente.', 'Select an employee.',
     'Selectați un angajat.', 'Wählen Sie einen Mitarbeiter.', 'Välj en anställd.'),
    ('acdc_select_new_subcdc', 'Seleziona il nuovo sotto-reparto.', 'Select the new sub-department.',
     'Selectați noul sub-departament.', 'Wählen Sie die neue Unterabteilung.',
     'Välj den nya underavdelningen.'),
    ('acdc_no_change', 'Il sotto-reparto selezionato è già quello attuale.',
     'The selected sub-department is already the current one.',
     'Sub-departamentul selectat este deja cel curent.',
     'Die gewählte Unterabteilung ist bereits die aktuelle.',
     'Den valda underavdelningen är redan den nuvarande.'),
    ('acdc_confirm', 'Spostare {0}\nda "{1}" a "{2}"?', 'Move {0}\nfrom "{1}" to "{2}"?',
     'Mutați {0}\ndin "{1}" în "{2}"?', '{0}\nvon "{1}" nach "{2}" verschieben?',
     'Flytta {0}\nfrån "{1}" till "{2}"?'),
    ('acdc_saved', 'Riassegnazione salvata.', 'Reassignment saved.', 'Reatribuire salvată.',
     'Neuzuweisung gespeichert.', 'Omfördelning sparad.'),
    ('acdc_save_conflict', 'La posizione è cambiata nel frattempo. Aggiorna e riprova.',
     'The position changed in the meantime. Refresh and retry.',
     'Poziția s-a schimbat între timp. Reîmprospătați și reîncercați.',
     'Die Position hat sich zwischenzeitlich geändert. Aktualisieren und erneut versuchen.',
     'Positionen har ändrats under tiden. Uppdatera och försök igen.'),
    ('acdc_email_no_to',
     'Modifica salvata, ma manca la tua email aziendale: notifica non inviata.',
     'Change saved, but your work email is missing: notification not sent.',
     'Modificare salvată, dar lipsește emailul dvs.: notificarea nu a fost trimisă.',
     'Änderung gespeichert, aber Ihre Arbeits-E-Mail fehlt: Benachrichtigung nicht gesendet.',
     'Ändring sparad, men din arbetsmejl saknas: avisering skickades inte.'),
    ('acdc_email_error', 'Modifica salvata, ma invio email non riuscito:\n{0}',
     'Change saved, but email sending failed:\n{0}',
     'Modificare salvată, dar trimiterea emailului a eșuat:\n{0}',
     'Änderung gespeichert, aber E-Mail-Versand fehlgeschlagen:\n{0}',
     'Ändring sparad, men e-postutskick misslyckades:\n{0}'),
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
    print(f"[OK] Attribuisci CDC translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
