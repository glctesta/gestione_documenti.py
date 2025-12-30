#!/usr/bin/env python3
# Script per generare le traduzioni SQL per project_window.py

from pathlib import Path

# Dizionario delle traduzioni per project_window.py
translations = {
    # Titoli finestra
    'project_window_title': {
        'it': 'Gestione Progetto NPI',
        'ro': 'Gestionare Proiect NPI',
        'en': 'NPI Project Management',
        'de': 'NPI-Projektverwaltung',
        'sv': 'NPI-projekthantering'
    },
    
    # Stati
    'status_todo': {
        'it': 'Da Fare',
        'ro': 'De Făcut',
        'en': 'To Do',
        'de': 'Zu erledigen',
        'sv': 'Att göra'
    },
    'status_wip': {
        'it': 'In Lavorazione',
        'ro': 'În Lucru',
        'en': 'In Progress',
        'de': 'In Bearbeitung',
        'sv': 'Pågående'
    },
    'status_done': {
        'it': 'Completato',
        'ro': 'Finalizat',
        'en': 'Completed',
        'de': 'Abgeschlossen',
        'sv': 'Slutförd'
    },
    'status_blocked': {
        'it': 'Bloccato',
        'ro': 'Blocat',
        'en': 'Blocked',
        'de': 'Blockiert',
        'sv': 'Blockerad'
    },
    
    # Bottoni
    'btn_import_tasks': {
        'it': 'Importa Task',
        'ro': 'Importă Sarcini',
        'en': 'Import Tasks',
        'de': 'Aufgaben importieren',
        'sv': 'Importera uppgifter'
    },
    'btn_export_excel': {
        'it': 'Export Excel',
        'ro': 'Export Excel',
        'en': 'Export Excel',
        'de': 'Excel exportieren',
        'sv': 'Exportera Excel'
    },
    'btn_add_dependency': {
        'it': 'Aggiungi',
        'ro': 'Adaugă',
        'en': 'Add',
        'de': 'Hinzufügen',
        'sv': 'Lägg till'
    },
    'btn_remove_dependency': {
        'it': 'Rimuovi',
        'ro': 'Elimină',
        'en': 'Remove',
        'de': 'Entfernen',
        'sv': 'Ta bort'
    },
    
    # Checkbox e opzioni
    'show_assigned': {
        'it': 'Mostra Assegnati',
        'ro': 'Arată Atribuite',
        'en': 'Show Assigned',
        'de': 'Zugewiesene anzeigen',
        'sv': 'Visa tilldelade'
    },
    
    # Titoli sezioni
    'project_dates_title': {
        'it': 'Date Progetto',
        'ro': 'Date Proiect',
        'en': 'Project Dates',
        'de': 'Projektdaten',
        'sv': 'Projektdatum'
    },
    'task_details': {
        'it': 'Dettagli Task',
        'ro': 'Detalii Sarcină',
        'en': 'Task Details',
        'de': 'Aufgabendetails',
        'sv': 'Uppgiftsdetaljer'
    },
    'dependencies_title': {
        'it': 'Dipendenze Task',
        'ro': 'Dependențe Sarcină',
        'en': 'Task Dependencies',
        'de': 'Aufgabenabhängigkeiten',
        'sv': 'Uppgiftsberoenden'
    },
    'documents_title': {
        'it': 'Documenti',
        'ro': 'Documente',
        'en': 'Documents',
        'de': 'Dokumente',
        'sv': 'Dokument'
    },
    
    # Date
    'start_date': {
        'it': 'Inizio:',
        'ro': 'Început:',
        'en': 'Start:',
        'de': 'Start:',
        'sv': 'Start:'
    },
    'due_date': {
        'it': 'Scadenza:',
        'ro': 'Termen:',
        'en': 'Due:',
        'de': 'Fällig:',
        'sv': 'Förfaller:'
    },
    'save_dates': {
        'it': 'Salva Date',
        'ro': 'Salvează Date',
        'en': 'Save Dates',
        'de': 'Daten speichern',
        'sv': 'Spara datum'
    },
    
    # Colonne
    'col_task': {
        'it': 'Task',
        'ro': 'Sarcină',
        'en': 'Task',
        'de': 'Aufgabe',
        'sv': 'Uppgift'
    },
    'col_owner': {
        'it': 'Assegnato a',
        'ro': 'Atribuit la',
        'en': 'Assigned to',
        'de': 'Zugewiesen an',
        'sv': 'Tilldelad till'
    },
    'col_due_date': {
        'it': 'Scadenza',
        'ro': 'Termen Limită',
        'en': 'Due Date',
        'de': 'Fälligkeitsdatum',
        'sv': 'Förfallodatum'
    },
    
    # Label dettagli task
    'label_task': {
        'it': 'Task:',
        'ro': 'Sarcină:',
        'en': 'Task:',
        'de': 'Aufgabe:',
        'sv': 'Uppgift:'
    },
    'label_owner': {
        'it': 'Assegnato a:',
        'ro': 'Atribuit la:',
        'en': 'Assigned to:',
        'de': 'Zugewiesen an:',
        'sv': 'Tilldelad till:'
    },
    'label_status': {
        'it': 'Stato:',
        'ro': 'Status:',
        'en': 'Status:',
        'de': 'Status:',
        'sv': 'Status:'
    },
    'label_start_date': {
        'it': 'Data Inizio:',
        'ro': 'Data Început:',
        'en': 'Start Date:',
        'de': 'Startdatum:',
        'sv': 'Startdatum:'
    },
    'label_due_date': {
        'it': 'Data Scadenza:',
        'ro': 'Data Termen:',
        'en': 'Due Date:',
        'de': 'Fälligkeitsdatum:',
        'sv': 'Förfallodatum:'
    },
    'label_completion_date': {
        'it': 'Data Completamento:',
        'ro': 'Data Finalizare:',
        'en': 'Completion Date:',
        'de': 'Abschlussdatum:',
        'sv': 'Slutförandedatum:'
    },
    
    # Dipendenze
    'current_dependencies': {
        'it': 'Dipendenze correnti:',
        'ro': 'Dependențe curente:',
        'en': 'Current dependencies:',
        'de': 'Aktuelle Abhängigkeiten:',
        'sv': 'Nuvarande beroenden:'
    },
    'add_dependency_label': {
        'it': 'Aggiungi Dipendenza:',
        'ro': 'Adaugă Dependență:',
        'en': 'Add Dependency:',
        'de': 'Abhängigkeit hinzufügen:',
        'sv': 'Lägg till beroende:'
    },
    'no_dependencies': {
        'it': 'Nessuna dipendenza definita',
        'ro': 'Nicio dependență definită',
        'en': 'No dependencies defined',
        'de': 'Keine Abhängigkeiten definiert',
        'sv': 'Inga beroenden definierade'
    },
    'select_predecessor': {
        'it': 'Seleziona task prerequisito...',
        'ro': 'Selectează sarcină prerequisit...',
        'en': 'Select prerequisite task...',
        'de': 'Voraussetzungsaufgabe auswählen...',
        'sv': 'Välj förutsättningsuppgift...'
    },
    
    # Documenti
    'doc_type': {
        'it': 'Tipo:',
        'ro': 'Tip:',
        'en': 'Type:',
        'de': 'Typ:',
        'sv': 'Typ:'
    },
    'doc_title': {
        'it': 'Titolo:',
        'ro': 'Titlu:',
        'en': 'Title:',
        'de': 'Titel:',
        'sv': 'Titel:'
    },
    'final_client': {
        'it': 'Cliente Finale:',
        'ro': 'Client Final:',
        'en': 'Final Client:',
        'de': 'Endkunde:',
        'sv': 'Slutkund:'
    },
    'doc_value': {
        'it': 'Valore (€):',
        'ro': 'Valoare (€):',
        'en': 'Value (€):',
        'de': 'Wert (€):',
        'sv': 'Värde (€):'
    },
    'doc_due_date': {
        'it': 'Scadenza Doc:',
        'ro': 'Termen Doc:',
        'en': 'Doc Due Date:',
        'de': 'Dok. Fälligkeitsdatum:',
        'sv': 'Dok. Förfallodatum:'
    },
    'is_replacement': {
        'it': 'Sostituisce doc esistente',
        'ro': 'Înlocuiește doc existent',
        'en': 'Replaces existing doc',
        'de': 'Ersetzt vorhandenes Dok.',
        'sv': 'Ersätter befintligt dok.'
    },
    'select_file': {
        'it': 'Seleziona File...',
        'ro': 'Selectează Fișier...',
        'en': 'Select File...',
        'de': 'Datei auswählen...',
        'sv': 'Välj fil...'
    },
    'no_file_selected': {
        'it': 'Nessun file',
        'ro': 'Niciun fișier',
        'en': 'No file',
        'de': 'Keine Datei',
        'sv': 'Ingen fil'
    },
    'notes': {
        'it': 'Note:',
        'ro': 'Note:',
        'en': 'Notes:',
        'de': 'Notizen:',
        'sv': 'Anteckningar:'
    },
    'save_doc': {
        'it': 'Carica Documento',
        'ro': 'Încarcă Document',
        'en': 'Upload Document',
        'de': 'Dokument hochladen',
        'sv': 'Ladda upp dokument'
    },
    'view_docs': {
        'it': 'Vedi Documenti Caricati',
        'ro': 'Vezi Documente Încărcate',
        'en': 'View Uploaded Documents',
        'de': 'Hochgeladene Dokumente anzeigen',
        'sv': 'Visa uppladdade dokument'
    },
    
    # Avvisi e messaggi
    'warning_title': {
        'it': 'Attenzione',
        'ro': 'Atenție',
        'en': 'Warning',
        'de': 'Warnung',
        'sv': 'Varning'
    },
    'warning_select_predecessor': {
        'it': 'Seleziona un task prerequisito',
        'ro': 'Selectează o sarcină prerequisit',
        'en': 'Select a prerequisite task',
        'de': 'Wählen Sie eine Voraussetzungsaufgabe aus',
        'sv': 'Välj en förutsättningsuppgift'
    },
    'warning_dependency_exists': {
        'it': 'Questa dipendenza esiste già',
        'ro': 'Această dependență există deja',
        'en': 'This dependency already exists',
        'de': 'Diese Abhängigkeit existiert bereits',
        'sv': 'Detta beroende finns redan'
    },
    'warning_select_dependency': {
        'it': 'Seleziona una dipendenza da rimuovere',
        'ro': 'Selectează o dependență de eliminat',
        'en': 'Select a dependency to remove',
        'de': 'Wählen Sie eine Abhängigkeit zum Entfernen aus',
        'sv': 'Välj ett beroende att ta bort'
    },
    'warning_no_task_selected': {
        'it': 'Seleziona un task',
        'ro': 'Selectează o sarcină',
        'en': 'Select a task',
        'de': 'Wählen Sie eine Aufgabe aus',
        'sv': 'Välj en uppgift'
    },
    'warning_fill_required_fields': {
        'it': 'Compila tutti i campi obbligatori',
        'ro': 'Completează toate câmpurile obligatorii',
        'en': 'Fill all required fields',
        'de': 'Füllen Sie alle Pflichtfelder aus',
        'sv': 'Fyll i alla obligatoriska fält'
    },
    'warning_select_file_first': {
        'it': 'Seleziona prima un file',
        'ro': 'Selectează mai întâi un fișier',
        'en': 'Select a file first',
        'de': 'Wählen Sie zuerst eine Datei aus',
        'sv': 'Välj en fil först'
    },
    
    # Successo
    'success_dates_saved': {
        'it': 'Date progetto salvate con successo',
        'ro': 'Date proiect salvate cu succes',
        'en': 'Project dates saved successfully',
        'de': 'Projektdaten erfolgreich gespeichert',
        'sv': 'Projektdatum sparade framgångsrikt'
    },
    'success_task_saved': {
        'it': 'Task salvato con successo',
        'ro': 'Sarcină salvată cu succes',
        'en': 'Task saved successfully',
        'de': 'Aufgabe erfolgreich gespeichert',
        'sv': 'Uppgift sparad framgångsrikt'
    },
    'success_dependency_added': {
        'it': 'Dipendenza aggiunta',
        'ro': 'Dependență adăugată',
        'en': 'Dependency added',
        'de': 'Abhängigkeit hinzugefügt',
        'sv': 'Beroende tillagt'
    },
    'success_dependency_removed': {
        'it': 'Dipendenza rimossa',
        'ro': 'Dependență eliminată',
        'en': 'Dependency removed',
        'de': 'Abhängigkeit entfernt',
        'sv': 'Beroende borttaget'
    },
    'success_document_uploaded': {
        'it': 'Documento caricato con successo',
        'ro': 'Document încărcat cu succes',
        'en': 'Document uploaded successfully',
        'de': 'Dokument erfolgreich hochgeladen',
        'sv': 'Dokument uppladdat framgångsrikt'
    },
    'success_tasks_imported': {
        'it': 'Task importati con successo',
        'ro': 'Sarcini importate cu succes',
        'en': 'Tasks imported successfully',
        'de': 'Aufgaben erfolgreich importiert',
        'sv': 'Uppgifter importerade framgångsrikt'
    },
    
    # Errori
    'error_save_dates': {
        'it': 'Errore durante il salvataggio delle date: {error}',
        'ro': 'Eroare la salvarea datelor: {error}',
        'en': 'Error saving dates: {error}',
        'de': 'Fehler beim Speichern der Daten: {error}',
        'sv': 'Fel vid sparande av datum: {error}'
    },
    'error_save_task': {
        'it': 'Errore durante il salvataggio del task: {error}',
        'ro': 'Eroare la salvarea sarcinii: {error}',
        'en': 'Error saving task: {error}',
        'de': 'Fehler beim Speichern der Aufgabe: {error}',
        'sv': 'Fel vid sparande av uppgift: {error}'
    },
    'error_add_dependency': {
        'it': 'Errore durante l\'aggiunta della dipendenza: {error}',
        'ro': 'Eroare la adăugarea dependenței: {error}',
        'en': 'Error adding dependency: {error}',
        'de': 'Fehler beim Hinzufügen der Abhängigkeit: {error}',
        'sv': 'Fel vid tillägg av beroende: {error}'
    },
    'error_remove_dependency': {
        'it': 'Errore durante la rimozione della dipendenza: {error}',
        'ro': 'Eroare la eliminarea dependenței: {error}',
        'en': 'Error removing dependency: {error}',
        'de': 'Fehler beim Entfernen der Abhängigkeit: {error}',
        'sv': 'Fel vid borttagning av beroende: {error}'
    },
    'error_upload_document': {
        'it': 'Errore durante il caricamento del documento: {error}',
        'ro': 'Eroare la încărcarea documentului: {error}',
        'en': 'Error uploading document: {error}',
        'de': 'Fehler beim Hochladen des Dokuments: {error}',
        'sv': 'Fel vid uppladdning av dokument: {error}'
    },
    'error_import_tasks': {
        'it': 'Errore durante l\'importazione dei task: {error}',
        'ro': 'Eroare la importarea sarcinilor: {error}',
        'en': 'Error importing tasks: {error}',
        'de': 'Fehler beim Importieren der Aufgaben: {error}',
        'sv': 'Fel vid import av uppgifter: {error}'
    },
    'error_export_excel': {
        'it': 'Errore durante l\'esportazione Excel: {error}',
        'ro': 'Eroare la exportul Excel: {error}',
        'en': 'Error exporting Excel: {error}',
        'de': 'Fehler beim Excel-Export: {error}',
        'sv': 'Fel vid Excel-export: {error}'
    },
}

# Genera lo script SQL
output_file = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\NPI_PROJECT_TRANSLATIONS.sql")

with output_file.open('w', encoding='utf-8') as f:
    f.write("-- Script di traduzione per NPI Project Window\n")
    f.write("-- Generato automaticamente\n")
    f.write("-- Tabella: [Traceability_RS].[dbo].[AppTranslations]\n\n")
    
    for key in sorted(translations.keys()):
        trans = translations[key]
        
        # IT
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        f.write(f"    VALUES ('it', '{key}', '{trans['it']}');\n\n")
        
        # RO (con N davanti)
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        f.write(f"    VALUES ('ro', '{key}', N'{trans['ro']}');\n\n")
        
        # EN
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        f.write(f"    VALUES ('en', '{key}', '{trans['en']}');\n\n")
        
        # DE
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        f.write(f"    VALUES ('de', '{key}', '{trans['de']}');\n\n")
        
        # SV
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        f.write(f"    VALUES ('sv', '{key}', '{trans['sv']}');\n\n")

print(f"\n✅ Script SQL generato: {output_file}")
print(f"✅ Totale chiavi tradotte: {len(translations)}")
print(f"✅ Totale INSERT statements: {len(translations) * 5}")
