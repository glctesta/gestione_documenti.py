#!/usr/bin/env python3
# Script per generare TUTTE le traduzioni NPI basate sulle chiavi trovate

from pathlib import Path

# Leggi le chiavi trovate
keys_file = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\npi_keys_found.txt")
keys = keys_file.read_text(encoding='utf-8').strip().split('\n')

print(f"Generazione traduzioni per {len(keys)} chiavi...")

# Dizionario completo delle traduzioni
translations = {
    'add_dependency_label': {'it': 'Aggiungi Dipendenza:', 'ro': 'Adaugă Dependență:', 'en': 'Add Dependency:', 'de': 'Abhängigkeit hinzufügen:', 'sv': 'Lägg till beroende:'},
    'btn_add_dependency': {'it': 'Aggiungi', 'ro': 'Adaugă', 'en': 'Add', 'de': 'Hinzufügen', 'sv': 'Lägg till'},
    'btn_create_npi_project': {'it': 'Crea Progetto NPI', 'ro': 'Creează Proiect NPI', 'en': 'Create NPI Project', 'de': 'NPI-Projekt erstellen', 'sv': 'Skapa NPI-projekt'},
    'btn_delete': {'it': 'Elimina', 'ro': 'Șterge', 'en': 'Delete', 'de': 'Löschen', 'sv': 'Radera'},
    'btn_export_excel': {'it': 'Export Excel', 'ro': 'Export Excel', 'en': 'Export Excel', 'de': 'Excel exportieren', 'sv': 'Exportera Excel'},
    'btn_export_overview': {'it': 'Export Rapporto Panoramico', 'ro': 'Export Raport General', 'en': 'Export Overview Report', 'de': 'Übersichtsbericht exportieren', 'sv': 'Exportera översiktsrapport'},
    'btn_add_document': {'it': 'Aggiungi Documento', 'ro': 'Adaugă Document', 'en': 'Add Document', 'de': 'Dokument hinzufügen', 'sv': 'Lägg till dokument'},
    'btn_create': {'it': 'Crea', 'ro': 'Creează', 'en': 'Create', 'de': 'Erstellen', 'sv': 'Skapa'},
    'btn_delete_task': {'it': 'Elimina Task', 'ro': 'Șterge Sarcină', 'en': 'Delete Task', 'de': 'Aufgabe löschen', 'sv': 'Radera uppgift'},
    'btn_manage_dependencies': {'it': 'Gestisci Dipendenze', 'ro': 'Gestionează Dependențe', 'en': 'Manage Dependencies', 'de': 'Abhängigkeiten verwalten', 'sv': 'Hantera beroenden'},
    'btn_sync_catalog': {'it': 'Sincronizza Catalogo', 'ro': 'Sincronizează Catalog', 'en': 'Sync Catalog', 'de': 'Katalog synchronisieren', 'sv': 'Synkronisera katalog'},
    'all_categories': {'it': 'Tutte le categorie', 'ro': 'Toate categoriile', 'en': 'All categories', 'de': 'Alle Kategorien', 'sv': 'Alla kategorier'},
    'all_owners': {'it': 'Tutti i responsabili', 'ro': 'Toți responsabilii', 'en': 'All owners', 'de': 'Alle Verantwortlichen', 'sv': 'Alla ansvariga'},
    'category_tasks_label': {'it': 'Task della categoria:', 'ro': 'Sarcini din categorie:', 'en': 'Category tasks:', 'de': 'Aufgaben der Kategorie:', 'sv': 'Kategoriuppgifter:'},
    'col_filename': {'it': 'Nome file', 'ro': 'Nume fișier', 'en': 'Filename', 'de': 'Dateiname', 'sv': 'Filnamn'},
    'col_filesize': {'it': 'Dimensione', 'ro': 'Dimensiune', 'en': 'Size', 'de': 'Größe', 'sv': 'Storlek'},
    'col_start_date': {'it': 'Data Inizio', 'ro': 'Data început', 'en': 'Start Date', 'de': 'Startdatum', 'sv': 'Startdatum'},
    'config_sort': {'it': 'Configura Ordinamento', 'ro': 'Configurează Sortarea', 'en': 'Configure Sorting', 'de': 'Sortierung konfigurieren', 'sv': 'Konfigurera sortering'},
    'confirm_delete_task': {'it': 'Confermi eliminazione task?', 'ro': 'Confirmați ștergerea sarcinii?', 'en': 'Confirm task deletion?', 'de': 'Aufgabe löschen bestätigen?', 'sv': 'Bekräfta borttagning av uppgift?'},
    'confirm_title': {'it': 'Conferma', 'ro': 'Confirmare', 'en': 'Confirm', 'de': 'Bestätigen', 'sv': 'Bekräfta'},
    'dependencies_summary': {'it': 'Riepilogo Dipendenze', 'ro': 'Rezumat dependențe', 'en': 'Dependencies Summary', 'de': 'Abhängigkeitsübersicht', 'sv': 'Beroendesammanfattning'},
    'error_cannot_delete_task_has_dependents': {'it': 'Impossibile eliminare: il task ha dipendenze', 'ro': 'Nu se poate șterge: sarcina are dependențe', 'en': 'Cannot delete: task has dependencies', 'de': 'Löschen nicht möglich: Aufgabe hat Abhängigkeiten', 'sv': 'Kan inte ta bort: uppgiften har beroenden'},
    'error_due_after_project_end': {'it': 'Scadenza oltre la fine progetto', 'ro': 'Termen după finalul proiectului', 'en': 'Due date after project end', 'de': 'Fälligkeitsdatum nach Projektende', 'sv': 'Förfallodatum efter projektslut'},
    'error_due_before_dependency': {'it': 'Scadenza prima della dipendenza', 'ro': 'Termen înaintea dependenței', 'en': 'Due date before dependency', 'de': 'Fälligkeitsdatum vor Abhängigkeit', 'sv': 'Förfallodatum före beroende'},
    'error_due_date_before_start': {'it': "Scadenza prima dell'inizio", 'ro': 'Termen înainte de start', 'en': 'Due date before start', 'de': 'Fälligkeitsdatum vor Start', 'sv': 'Förfallodatum före start'},
    'error_start_after_project_end': {'it': 'Inizio dopo la fine progetto', 'ro': 'Start după finalul proiectului', 'en': 'Start after project end', 'de': 'Start nach Projektende', 'sv': 'Start efter projektslut'},
    'error_start_before_dependency': {'it': 'Inizio prima della dipendenza', 'ro': 'Start înainte de dependență', 'en': 'Start before dependency', 'de': 'Start vor Abhängigkeit', 'sv': 'Start före beroende'},
    'filter_category': {'it': 'Filtro categoria', 'ro': 'Filtru categorie', 'en': 'Category filter', 'de': 'Kategorienfilter', 'sv': 'Kategorifilter'},
    'filter_owner': {'it': 'Filtro responsabile', 'ro': 'Filtru responsabil', 'en': 'Owner filter', 'de': 'Verantwortlichen-Filter', 'sv': 'Ansvarig-filter'},
    'msg_no_missing_tasks': {'it': 'Nessun task mancante', 'ro': 'Nicio sarcină lipsă', 'en': 'No missing tasks', 'de': 'Keine fehlenden Aufgaben', 'sv': 'Inga saknade uppgifter'},
    'msg_project_exists_update': {'it': 'Progetto già esistente: aggiornato', 'ro': 'Proiect existent: actualizat', 'en': 'Project already exists: updated', 'de': 'Projekt existiert bereits: aktualisiert', 'sv': 'Projektet finns redan: uppdaterat'},
    'msg_project_updated': {'it': 'Progetto aggiornato', 'ro': 'Proiect actualizat', 'en': 'Project updated', 'de': 'Projekt aktualisiert', 'sv': 'Projekt uppdaterat'},
    'msg_select_document': {'it': 'Seleziona un documento', 'ro': 'Selectează un document', 'en': 'Select a document', 'de': 'Dokument auswählen', 'sv': 'Välj ett dokument'},
    'msg_sync_catalog': {'it': 'Sincronizzazione catalogo in corso', 'ro': 'Sincronizare catalog în curs', 'en': 'Catalog sync in progress', 'de': 'Katalog-Synchronisierung läuft', 'sv': 'Katalogsynk pågår'},
    'msg_tasks_synced': {'it': 'Task sincronizzati', 'ro': 'Sarcini sincronizate', 'en': 'Tasks synced', 'de': 'Aufgaben synchronisiert', 'sv': 'Uppgifter synkroniserade'},
    'no_tasks_in_category': {'it': 'Nessun task in questa categoria', 'ro': 'Nu există sarcini în această categorie', 'en': 'No tasks in this category', 'de': 'Keine Aufgaben in dieser Kategorie', 'sv': 'Inga uppgifter i denna kategori'},
    'project_description': {'it': 'Descrizione Progetto', 'ro': 'Descriere proiect', 'en': 'Project Description', 'de': 'Projektbeschreibung', 'sv': 'Projektbeskrivning'},
    'project_documents': {'it': 'Documenti Progetto', 'ro': 'Documente proiect', 'en': 'Project Documents', 'de': 'Projektdokumente', 'sv': 'Projektdokument'},
    'project_owner': {'it': 'Responsabile Progetto', 'ro': 'Responsabil proiect', 'en': 'Project Owner', 'de': 'Projektverantwortlicher', 'sv': 'Projektansvarig'},
    'reset_sort': {'it': 'Reset Ordinamento', 'ro': 'Resetare sortare', 'en': 'Reset Sorting', 'de': 'Sortierung zurücksetzen', 'sv': 'Återställ sortering'},
    'select_document': {'it': 'Seleziona Documento', 'ro': 'Selectează Document', 'en': 'Select Document', 'de': 'Dokument auswählen', 'sv': 'Välj dokument'},
    'sort_config_saved': {'it': 'Ordinamento salvato', 'ro': 'Sortare salvată', 'en': 'Sorting saved', 'de': 'Sortierung gespeichert', 'sv': 'Sortering sparad'},
    'warning_no_task_selected': {'it': 'Seleziona un task', 'ro': 'Selectează o sarcină', 'en': 'Select a task', 'de': 'Wählen Sie eine Aufgabe', 'sv': 'Välj en uppgift'},
    'active_npi_projects': {'it': 'Progetti NPI Attivi', 'ro': 'Proiecte NPI Active', 'en': 'Active NPI Projects', 'de': 'Aktive NPI-Projekte', 'sv': 'Aktiva NPI-projekt'},
    'btn_analyze': {'it': 'Analisi', 'ro': 'Analiză', 'en': 'Analyze', 'de': 'Analyse', 'sv': 'Analys'},
    'btn_close': {'it': 'Chiudi', 'ro': 'Închide', 'en': 'Close', 'de': 'Schließen', 'sv': 'Stäng'},
    'btn_export_pdf': {'it': 'Esporta PDF in C:\\Temp', 'ro': 'Export PDF în C:\\Temp', 'en': 'Export PDF to C:\\Temp', 'de': 'PDF nach C:\\Temp exportieren', 'sv': 'Exportera PDF till C:\\Temp'},
    'btn_refresh': {'it': 'Aggiorna', 'ro': 'Actualizează', 'en': 'Refresh', 'de': 'Aktualisieren', 'sv': 'Uppdatera'},
    'col_project_end_date': {'it': 'Data Fine Progetto', 'ro': 'Data Sfârșit Proiect', 'en': 'Project End Date', 'de': 'Projekt-Enddatum', 'sv': 'Projektets slutdatum'},
    'col_project_name': {'it': 'Nome Progetto', 'ro': 'Nume Proiect', 'en': 'Project Name', 'de': 'Projektname', 'sv': 'Projektnamn'},
    'manage_project': {'it': 'Gestisci Dettagli Task...', 'ro': 'Gestionează Detalii Sarcini...', 'en': 'Manage Task Details...', 'de': 'Aufgabendetails verwalten...', 'sv': 'Hantera uppgiftsdetaljer...'},
    'no_active_projects': {'it': 'Nessun progetto attivo trovato.', 'ro': 'Nu s-a găsit niciun proiect activ.', 'en': 'No active projects found.', 'de': 'Keine aktiven Projekte gefunden.', 'sv': 'Inga aktiva projekt hittades.'},
    'npi_dashboard_title': {'it': 'Dashboard Progetti NPI', 'ro': 'Panou Proiecte NPI', 'en': 'NPI Projects Dashboard', 'de': 'NPI-Projekt-Dashboard', 'sv': 'NPI-projektdashboard'},
    'npi_view_gantt': {'it': 'Visualizza Gantt...', 'ro': 'Vizualizează Gantt...', 'en': 'View Gantt...', 'de': 'Gantt anzeigen...', 'sv': 'Visa Gantt...'},
    'npi_notifications_config_warning': {
        'it': 'Attenzione: la modifica di questo file può compromettere la funzionalità delle notifiche automatiche.',
        'ro': 'Atenție: modificarea acestui fișier poate afecta funcționalitatea notificărilor automate.',
        'en': 'Warning: editing this file may affect the automatic notification functionality.',
        'de': 'Warnung: Das Bearbeiten dieser Datei kann die automatische Benachrichtigungsfunktion beeinträchtigen.',
        'sv': 'Varning: att redigera den här filen kan påverka funktionen för automatiska notiser.'
    },
    'btn_import_tasks': {'it': 'Importa Task', 'ro': 'Importă Sarcini', 'en': 'Import Tasks', 'de': 'Aufgaben importieren', 'sv': 'Importera uppgifter'},
    'btn_new': {'it': 'Nuovo', 'ro': 'Nou', 'en': 'New', 'de': 'Neu', 'sv': 'Ny'},
    'btn_remove_dependency': {'it': 'Rimuovi', 'ro': 'Elimină', 'en': 'Remove', 'de': 'Entfernen', 'sv': 'Ta bort'},
    'btn_save': {'it': 'Salva', 'ro': 'Salvează', 'en': 'Save', 'de': 'Speichern', 'sv': 'Spara'},
    'category_details_title': {'it': 'Dettagli Categoria', 'ro': 'Detalii Categorie', 'en': 'Category Details', 'de': 'Kategoriedetails', 'sv': 'Kategoridetaljer'},
    'col_category': {'it': 'Categoria', 'ro': 'Categorie', 'en': 'Category', 'de': 'Kategorie', 'sv': 'Kategori'},
    'col_customer': {'it': 'Cliente', 'ro': 'Client', 'en': 'Customer', 'de': 'Kunde', 'sv': 'Kund'},
    'col_due_date': {'it': 'Scadenza', 'ro': 'Termen Limită', 'en': 'Due Date', 'de': 'Fälligkeitsdatum', 'sv': 'Förfallodatum'},
    'col_id': {'it': 'ID', 'ro': 'ID', 'en': 'ID', 'de': 'ID', 'sv': 'ID'},
    'col_item_id': {'it': 'ID Elemento', 'ro': 'ID Element', 'en': 'Item ID', 'de': 'Element-ID', 'sv': 'Element-ID'},
    'col_name_generic': {'it': 'Nome', 'ro': 'Nume', 'en': 'Name', 'de': 'Name', 'sv': 'Namn'},
    'col_order': {'it': 'Ordine', 'ro': 'Ordine', 'en': 'Order', 'de': 'Reihenfolge', 'sv': 'Ordning'},
    'col_owner': {'it': 'Assegnato a', 'ro': 'Atribuit la', 'en': 'Assigned to', 'de': 'Zugewiesen an', 'sv': 'Tilldelad till'},
    'col_product_code': {'it': 'Codice Prodotto', 'ro': 'Cod Produs', 'en': 'Product Code', 'de': 'Produktcode', 'sv': 'Produktkod'},
    'col_product_name': {'it': 'Nome Prodotto', 'ro': 'Nume Produs', 'en': 'Product Name', 'de': 'Produktname', 'sv': 'Produktnamn'},
    'col_status': {'it': 'Stato', 'ro': 'Status', 'en': 'Status', 'de': 'Status', 'sv': 'Status'},
    'col_task': {'it': 'Task', 'ro': 'Sarcină', 'en': 'Task', 'de': 'Aufgabe', 'sv': 'Uppgift'},
    'col_task_name': {'it': 'Nome Task', 'ro': 'Nume Sarcină', 'en': 'Task Name', 'de': 'Aufgabenname', 'sv': 'Uppgiftsnamn'},
    'col_type': {'it': 'Tipo', 'ro': 'Tip', 'en': 'Type', 'de': 'Typ', 'sv': 'Typ'},
    'config_window_title': {'it': 'Configurazione NPI', 'ro': 'Configurare NPI', 'en': 'NPI Configuration', 'de': 'NPI-Konfiguration', 'sv': 'NPI-konfiguration'},
    'confirm_delete_category_text': {'it': 'Sei sicuro di voler eliminare questa categoria?', 'ro': 'Ești sigur că vrei să ștergi această categorie?', 'en': 'Are you sure you want to delete this category?', 'de': 'Sind Sie sicher, dass Sie diese Kategorie löschen möchten?', 'sv': 'Är du säker på att du vill radera denna kategori?'},
    'confirm_delete_product_text': {'it': 'Sei sicuro di voler eliminare questo prodotto?', 'ro': 'Ești sigur că vrei să ștergi acest produs?', 'en': 'Are you sure you want to delete this product?', 'de': 'Sind Sie sicher, dass Sie dieses Produkt löschen möchten?', 'sv': 'Är du säker på att du vill radera denna produkt?'},
    'confirm_delete_subject_text': {'it': 'Sei sicuro di voler eliminare questo soggetto?', 'ro': 'Ești sigur că vrei să ștergi acest subiect?', 'en': 'Are you sure you want to delete this subject?', 'de': 'Sind Sie sicher, dass Sie dieses Subjekt löschen möchten?', 'sv': 'Är du säker på att du vill radera detta ämne?'},
    'confirm_delete_task_text': {'it': 'Sei sicuro di voler eliminare questo task?', 'ro': 'Ești sigur că vrei să ștergi această sarcină?', 'en': 'Are you sure you want to delete this task?', 'de': 'Sind Sie sicher, dass Sie diese Aufgabe löschen möchten?', 'sv': 'Är du säker på att du vill radera denna uppgift?'},
    'confirm_delete_title': {'it': 'Conferma Eliminazione', 'ro': 'Confirmă Ștergerea', 'en': 'Confirm Deletion', 'de': 'Löschen bestätigen', 'sv': 'Bekräfta Radering'},
    'current_dependencies': {'it': 'Dipendenze correnti:', 'ro': 'Dependențe curente:', 'en': 'Current dependencies:', 'de': 'Aktuelle Abhängigkeiten:', 'sv': 'Nuvarande beroenden:'},
    'db_error_delete_category': {'it': 'Errore durante l\'eliminazione della categoria: {error}', 'ro': 'Eroare la ștergerea categoriei: {error}', 'en': 'Error deleting category: {error}', 'de': 'Fehler beim Löschen der Kategorie: {error}', 'sv': 'Fel vid radering av kategori: {error}'},
    'db_error_delete_product': {'it': 'Errore durante l\'eliminazione del prodotto: {error}', 'ro': 'Eroare la ștergerea produsului: {error}', 'en': 'Error deleting product: {error}', 'de': 'Fehler beim Löschen des Produkts: {error}', 'sv': 'Fel vid radering av produkt: {error}'},
    'db_error_delete_subject': {'it': 'Errore durante l\'eliminazione del soggetto: {error}', 'ro': 'Eroare la ștergerea subiectului: {error}', 'en': 'Error deleting subject: {error}', 'de': 'Fehler beim Löschen des Subjekts: {error}', 'sv': 'Fel vid radering av ämne: {error}'},
    'db_error_delete_task': {'it': 'Errore durante l\'eliminazione del task: {error}', 'ro': 'Eroare la ștergerea sarcinii: {error}', 'en': 'Error deleting task: {error}', 'de': 'Fehler beim Löschen der Aufgabe: {error}', 'sv': 'Fel vid radering av uppgift: {error}'},
    'db_error_generic_save': {'it': 'Errore durante il salvataggio: {error}', 'ro': 'Eroare la salvare: {error}', 'en': 'Error during save: {error}', 'de': 'Fehler beim Speichern: {error}', 'sv': 'Fel vid sparande: {error}'},
    'db_error_load_categories': {'it': 'Errore durante il caricamento delle categorie: {error}', 'ro': 'Eroare la încărcarea categoriilor: {error}', 'en': 'Error loading categories: {error}', 'de': 'Fehler beim Laden der Kategorien: {error}', 'sv': 'Fel vid laddning av kategorier: {error}'},
    'db_error_save_task': {'it': 'Errore durante il salvataggio del task: {error}', 'ro': 'Eroare la salvarea sarcinii: {error}', 'en': 'Error saving task: {error}', 'de': 'Fehler beim Speichern der Aufgabe: {error}', 'sv': 'Fel vid sparande av uppgift: {error}'},
    'db_error_title': {'it': 'Errore Database', 'ro': 'Eroare Bază de Date', 'en': 'Database Error', 'de': 'Datenbankfehler', 'sv': 'Databasfel'},
    'dependencies_title': {'it': 'Dipendenze Task', 'ro': 'Dependențe Sarcină', 'en': 'Task Dependencies', 'de': 'Aufgabenabhängigkeiten', 'sv': 'Uppgiftsberoenden'},
    'dependency_added': {'it': 'Dipendenza aggiunta con successo', 'ro': 'Dependență adăugată cu succes', 'en': 'Dependency added successfully', 'de': 'Abhängigkeit erfolgreich hinzugefügt', 'sv': 'Beroende tillagt framgångsrikt'},
    'dependency_removed': {'it': 'Dipendenza rimossa con successo', 'ro': 'Dependență eliminată cu succes', 'en': 'Dependency removed successfully', 'de': 'Abhängigkeit erfolgreich entfernt', 'sv': 'Beroende borttaget framgångsrikt'},
    'doc_due_date': {'it': 'Scadenza Doc:', 'ro': 'Termen Doc:', 'en': 'Doc Due Date:', 'de': 'Dok. Fälligkeitsdatum:', 'sv': 'Dok. Förfallodatum:'},
    'doc_title': {'it': 'Titolo:', 'ro': 'Titlu:', 'en': 'Title:', 'de': 'Titel:', 'sv': 'Titel:'},
    'doc_type': {'it': 'Tipo:', 'ro': 'Tip:', 'en': 'Type:', 'de': 'Typ:', 'sv': 'Typ:'},
    'doc_value': {'it': 'Valore (€):', 'ro': 'Valoare (€):', 'en': 'Value (€):', 'de': 'Wert (€):', 'sv': 'Värde (€):'},
    'documents_title': {'it': 'Documenti', 'ro': 'Documente', 'en': 'Documents', 'de': 'Dokumente', 'sv': 'Dokument'},
    'due_date': {'it': 'Scadenza:', 'ro': 'Termen:', 'en': 'Due:', 'de': 'Fällig:', 'sv': 'Förfaller:'},
    'error_create_project': {'it': 'Errore durante la creazione del progetto: {error}', 'ro': 'Eroare la crearea proiectului: {error}', 'en': 'Error creating project: {error}', 'de': 'Fehler beim Erstellen des Projekts: {error}', 'sv': 'Fel vid skapande av projekt: {error}'},
    'error_dependency_not_satisfied': {'it': 'Dipendenza non soddisfatta: il task "{predecessor}" deve essere completato prima', 'ro': 'Dependență nesatisfăcută: sarcina "{predecessor}" trebuie finalizată mai întâi', 'en': 'Dependency not satisfied: task "{predecessor}" must be completed first', 'de': 'Abhängigkeit nicht erfüllt: Aufgabe "{predecessor}" muss zuerst abgeschlossen werden', 'sv': 'Beroende ej uppfyllt: uppgift "{predecessor}" måste slutföras först'},
    'error_duplicate_title': {'it': 'Titolo Duplicato', 'ro': 'Titlu Duplicat', 'en': 'Duplicate Title', 'de': 'Doppelter Titel', 'sv': 'Duplicerad titel'},
    'error_title': {'it': 'Errore', 'ro': 'Eroare', 'en': 'Error', 'de': 'Fehler', 'sv': 'Fel'},
    'final_client': {'it': 'Cliente Finale:', 'ro': 'Client Final:', 'en': 'Final Client:', 'de': 'Endkunde:', 'sv': 'Slutkund:'},
    'info_project_already_exists': {'it': 'Esiste già un progetto per questo prodotto', 'ro': 'Există deja un proiect pentru acest produs', 'en': 'A project already exists for this product', 'de': 'Für dieses Produkt existiert bereits ein Projekt', 'sv': 'Ett projekt finns redan för denna produkt'},
    'info_project_due_date_aligned': {'it': 'La scadenza del progetto è stata allineata all\'ultimo task', 'ro': 'Termenul limită al proiectului a fost aliniat la ultima sarcină', 'en': 'Project due date has been aligned to the last task', 'de': 'Projektfälligkeitsdatum wurde an die letzte Aufgabe angepasst', 'sv': 'Projektets förfallodatum har anpassats till den sista uppgiften'},
    'info_title': {'it': 'Informazione', 'ro': 'Informație', 'en': 'Information', 'de': 'Information', 'sv': 'Information'},
    'is_replacement': {'it': 'Sostituisce doc esistente', 'ro': 'Înlocuiește doc existent', 'en': 'Replaces existing doc', 'de': 'Ersetzt vorhandenes Dok.', 'sv': 'Ersätter befintligt dok.'},
    'label_category': {'it': 'Categoria:', 'ro': 'Categorie:', 'en': 'Category:', 'de': 'Kategorie:', 'sv': 'Kategori:'},
    'label_completion_date': {'it': 'Data Completamento:', 'ro': 'Data Finalizare:', 'en': 'Completion Date:', 'de': 'Abschlussdatum:', 'sv': 'Slutförandedatum:'},
    'label_description': {'it': 'Descrizione:', 'ro': 'Descriere:', 'en': 'Description:', 'de': 'Beschreibung:', 'sv': 'Beskrivning:'},
    'label_due_date': {'it': 'Data Scadenza:', 'ro': 'Data Termen:', 'en': 'Due Date:', 'de': 'Fälligkeitsdatum:', 'sv': 'Förfallodatum:'},
    'label_estimated_duration': {'it': 'Durata Stimata:', 'ro': 'Durată Estimată:', 'en': 'Estimated Duration:', 'de': 'Geschätzte Dauer:', 'sv': 'Uppskattad varaktighet:'},
    'label_item_id': {'it': 'ID Elemento:', 'ro': 'ID Element:', 'en': 'Item ID:', 'de': 'Element-ID:', 'sv': 'Element-ID:'},
    'label_notes': {'it': 'Note:', 'ro': 'Note:', 'en': 'Notes:', 'de': 'Notizen:', 'sv': 'Anteckningar:'},
    'label_owner': {'it': 'Assegnato a:', 'ro': 'Atribuit la:', 'en': 'Assigned to:', 'de': 'Zugewiesen an:', 'sv': 'Tilldelad till:'},
    'label_start_date': {'it': 'Data Inizio:', 'ro': 'Data Început:', 'en': 'Start Date:', 'de': 'Startdatum:', 'sv': 'Startdatum:'},
    'label_status': {'it': 'Stato:', 'ro': 'Status:', 'en': 'Status:', 'de': 'Status:', 'sv': 'Status:'},
    'label_subject_type': {'it': 'Tipo Soggetto:', 'ro': 'Tip Subiect:', 'en': 'Subject Type:', 'de': 'Subjekttyp:', 'sv': 'Ämnestyp:'},
    'label_task': {'it': 'Task:', 'ro': 'Sarcină:', 'en': 'Task:', 'de': 'Aufgabe:', 'sv': 'Uppgift:'},
    'label_task_name': {'it': 'Nome Task:', 'ro': 'Nume Sarcină:', 'en': 'Task Name:', 'de': 'Aufgabenname:', 'sv': 'Uppgiftsnamn:'},
    'label_version': {'it': 'Versione:', 'ro': 'Versiune:', 'en': 'Version:', 'de': 'Version:', 'sv': 'Version:'},
    'no_dependencies': {'it': 'Nessuna dipendenza definita', 'ro': 'Nicio dependență definită', 'en': 'No dependencies defined', 'de': 'Keine Abhängigkeiten definiert', 'sv': 'Inga beroenden definierade'},
    'no_file_selected': {'it': 'Nessun file', 'ro': 'Niciun fișier', 'en': 'No file', 'de': 'Keine Datei', 'sv': 'Ingen fil'},
    'notes': {'it': 'Note:', 'ro': 'Note:', 'en': 'Notes:', 'de': 'Notizen:', 'sv': 'Anteckningar:'},
    'notification_send_prompt': {'it': 'Vuoi inviare una notifica?', 'ro': 'Vrei să trimiți o notificare?', 'en': 'Do you want to send a notification?', 'de': 'Möchten Sie eine Benachrichtigung senden?', 'sv': 'Vill du skicka en avisering?'},
    'notification_send_title': {'it': 'Invia Notifica', 'ro': 'Trimite Notificare', 'en': 'Send Notification', 'de': 'Benachrichtigung senden', 'sv': 'Skicka avisering'},
    'product_details_title': {'it': 'Dettagli Prodotto', 'ro': 'Detalii Produs', 'en': 'Product Details', 'de': 'Produktdetails', 'sv': 'Produktdetaljer'},
    'project_dates_title': {'it': 'Date Progetto', 'ro': 'Date Proiect', 'en': 'Project Dates', 'de': 'Projektdaten', 'sv': 'Projektdatum'},
    'project_npi_management_title': {'it': 'Gestione Progetti NPI', 'ro': 'Gestionare Proiecte NPI', 'en': 'NPI Projects Management', 'de': 'NPI-Projektverwaltung', 'sv': 'NPI-projekthantering'},
    'project_window_title': {'it': 'Gestione Progetto NPI', 'ro': 'Gestionare Proiect NPI', 'en': 'NPI Project Management', 'de': 'NPI-Projektverwaltung', 'sv': 'NPI-projekthantering'},
    'save_dates': {'it': 'Salva Date', 'ro': 'Salvează Date', 'en': 'Save Dates', 'de': 'Daten speichern', 'sv': 'Spara datum'},
    'save_doc': {'it': 'Carica Documento', 'ro': 'Încarcă Document', 'en': 'Upload Document', 'de': 'Dokument hochladen', 'sv': 'Ladda upp dokument'},
    'select_file': {'it': 'Seleziona File...', 'ro': 'Selectează Fișier...', 'en': 'Select File...', 'de': 'Datei auswählen...', 'sv': 'Välj fil...'},
    'select_file_title': {'it': 'Seleziona File', 'ro': 'Selectează Fișier', 'en': 'Select File', 'de': 'Datei auswählen', 'sv': 'Välj fil'},
    'select_predecessor': {'it': 'Seleziona task prerequisito...', 'ro': 'Selectează sarcină prerequisit...', 'en': 'Select prerequisite task...', 'de': 'Voraussetzungsaufgabe auswählen...', 'sv': 'Välj förutsättningsuppgift...'},
    'show_assigned': {'it': 'Mostra Assegnati', 'ro': 'Arată Atribuite', 'en': 'Show Assigned', 'de': 'Zugewiesene anzeigen', 'sv': 'Visa tilldelade'},
    'start_date': {'it': 'Inizio:', 'ro': 'Început:', 'en': 'Start:', 'de': 'Start:', 'sv': 'Start:'},
    'status_blocked': {'it': 'Bloccato', 'ro': 'Blocat', 'en': 'Blocked', 'de': 'Blockiert', 'sv': 'Blockerad'},
    'status_done': {'it': 'Completato', 'ro': 'Finalizat', 'en': 'Completed', 'de': 'Abgeschlossen', 'sv': 'Slutförd'},
    'status_todo': {'it': 'Da Fare', 'ro': 'De Făcut', 'en': 'To Do', 'de': 'Zu erledigen', 'sv': 'Att göra'},
    'status_wip': {'it': 'In Lavorazione', 'ro': 'În Lucru', 'en': 'In Progress', 'de': 'In Bearbeitung', 'sv': 'Pågående'},
    'subject_details_title': {'it': 'Dettagli Soggetto', 'ro': 'Detalii Subiect', 'en': 'Subject Details', 'de': 'Subjektdetails', 'sv': 'Ämnesdetaljer'},
    'subject_type_customer': {'it': 'Cliente', 'ro': 'Client', 'en': 'Customer', 'de': 'Kunde', 'sv': 'Kund'},
    'subject_type_internal': {'it': 'Interno', 'ro': 'Intern', 'en': 'Internal', 'de': 'Intern', 'sv': 'Intern'},
    'subject_type_supplier': {'it': 'Fornitore', 'ro': 'Furnizor', 'en': 'Supplier', 'de': 'Lieferant', 'sv': 'Leverantör'},
    'success_category_deleted': {'it': 'Categoria eliminata con successo', 'ro': 'Categorie ștearsă cu succes', 'en': 'Category deleted successfully', 'de': 'Kategorie erfolgreich gelöscht', 'sv': 'Kategori raderad framgångsrikt'},
    'success_category_saved': {'it': 'Categoria salvata con successo', 'ro': 'Categorie salvată cu succes', 'en': 'Category saved successfully', 'de': 'Kategorie erfolgreich gespeichert', 'sv': 'Kategori sparad framgångsrikt'},
    'success_category_updated': {'it': 'Categoria aggiornata con successo', 'ro': 'Categorie actualizată cu succes', 'en': 'Category updated successfully', 'de': 'Kategorie erfolgreich aktualisiert', 'sv': 'Kategori uppdaterad framgångsrikt'},
    'success_product_deleted': {'it': 'Prodotto eliminato con successo', 'ro': 'Produs șters cu succes', 'en': 'Product deleted successfully', 'de': 'Produkt erfolgreich gelöscht', 'sv': 'Produkt raderad framgångsrikt'},
    'success_product_saved': {'it': 'Prodotto salvato con successo', 'ro': 'Produs salvat cu succes', 'en': 'Product saved successfully', 'de': 'Produkt erfolgreich gespeichert', 'sv': 'Produkt sparad framgångsrikt'},
    'success_project_created': {'it': 'Progetto creato con successo', 'ro': 'Proiect creat cu succes', 'en': 'Project created successfully', 'de': 'Projekt erfolgreich erstellt', 'sv': 'Projekt skapat framgångsrikt'},
    'success_subject_deleted': {'it': 'Soggetto eliminato con successo', 'ro': 'Subiect șters cu succes', 'en': 'Subject deleted successfully', 'de': 'Subjekt erfolgreich gelöscht', 'sv': 'Ämne raderat framgångsrikt'},
    'success_subject_saved': {'it': 'Soggetto salvato con successo', 'ro': 'Subiect salvat cu succes', 'en': 'Subject saved successfully', 'de': 'Subjekt erfolgreich gespeichert', 'sv': 'Ämne sparat framgångsrikt'},
    'success_task_created': {'it': 'Task creato con successo', 'ro': 'Sarcină creată cu succes', 'en': 'Task created successfully', 'de': 'Aufgabe erfolgreich erstellt', 'sv': 'Uppgift skapad framgångsrikt'},
    'success_task_deleted': {'it': 'Task eliminato con successo', 'ro': 'Sarcină ștearsă cu succes', 'en': 'Task deleted successfully', 'de': 'Aufgabe erfolgreich gelöscht', 'sv': 'Uppgift raderad framgångsrikt'},
    'success_task_saved': {'it': 'Task salvato con successo', 'ro': 'Sarcină salvată cu succes', 'en': 'Task saved successfully', 'de': 'Aufgabe erfolgreich gespeichert', 'sv': 'Uppgift sparad framgångsrikt'},
    'success_task_updated': {'it': 'Task aggiornato con successo', 'ro': 'Sarcină actualizată cu succes', 'en': 'Task updated successfully', 'de': 'Aufgabe erfolgreich aktualisiert', 'sv': 'Uppgift uppdaterad framgångsrikt'},
    'success_title': {'it': 'Successo', 'ro': 'Succes', 'en': 'Success', 'de': 'Erfolg', 'sv': 'Framgång'},
    'tab_categories_title': {'it': 'Categorie', 'ro': 'Categorii', 'en': 'Categories', 'de': 'Kategorien', 'sv': 'Kategorier'},
    'tab_products_title': {'it': 'Prodotti', 'ro': 'Produse', 'en': 'Products', 'de': 'Produkte', 'sv': 'Produkter'},
    'tab_subjects_title': {'it': 'Soggetti', 'ro': 'Subiecte', 'en': 'Subjects', 'de': 'Subjekte', 'sv': 'Ämnen'},
    'tab_task_catalog_title': {'it': 'Catalogo Task', 'ro': 'Catalog Sarcini', 'en': 'Task Catalog', 'de': 'Aufgabenkatalog', 'sv': 'Uppgiftskatalog'},
    'task_catalog_details_title': {'it': 'Dettagli Catalogo Task', 'ro': 'Detalii Catalog Sarcini', 'en': 'Task Catalog Details', 'de': 'Aufgabenkatalogdetails', 'sv': 'Uppgiftskatalogdetaljer'},
    'task_details': {'it': 'Dettagli Task', 'ro': 'Detalii Sarcină', 'en': 'Task Details', 'de': 'Aufgabendetails', 'sv': 'Uppgiftsdetaljer'},
    'task_details_title': {'it': 'Dettagli Task', 'ro': 'Detalii Sarcină', 'en': 'Task Details', 'de': 'Aufgabendetails', 'sv': 'Uppgiftsdetaljer'},
    'validation_error_category_name_required': {'it': 'Il nome della categoria è obbligatorio', 'ro': 'Numele categoriei este obligatoriu', 'en': 'Category name is required', 'de': 'Kategoriename ist erforderlich', 'sv': 'Kategorinamn krävs'},
    'validation_error_duplicate_itemid': {'it': 'ID Elemento duplicato', 'ro': 'ID Element duplicat', 'en': 'Duplicate Item ID', 'de': 'Doppelte Element-ID', 'sv': 'Duplicerad element-ID'},
    'validation_error_end_before_start': {'it': 'La data di fine non può essere precedente alla data di inizio', 'ro': 'Data de sfârșit nu poate fi înainte de data de început', 'en': 'End date cannot be before start date', 'de': 'Enddatum kann nicht vor dem Startdatum liegen', 'sv': 'Slutdatum kan inte vara före startdatum'},
    'validation_error_order_must_be_number': {'it': 'L\'ordine deve essere un numero', 'ro': 'Ordinea trebuie să fie un număr', 'en': 'Order must be a number', 'de': 'Reihenfolge muss eine Zahl sein', 'sv': 'Ordning måste vara ett nummer'},
    'validation_error_product_name_required': {'it': 'Il nome del prodotto è obbligatorio', 'ro': 'Numele produsului este obligatoriu', 'en': 'Product name is required', 'de': 'Produktname ist erforderlich', 'sv': 'Produktnamn krävs'},
    'validation_error_start_date_required': {'it': 'La data di inizio è obbligatoria quando è specificata la data di fine', 'ro': 'Data de început este obligatorie când este specificată data de sfârșit', 'en': 'Start date is required when end date is specified', 'de': 'Startdatum ist erforderlich, wenn Enddatum angegeben ist', 'sv': 'Startdatum krävs när slutdatum anges'},
    'validation_error_subject_required': {'it': 'Il soggetto è obbligatorio', 'ro': 'Subiectul este obligatoriu', 'en': 'Subject is required', 'de': 'Subjekt ist erforderlich', 'sv': 'Ämne krävs'},
    'validation_error_task_required': {'it': 'Il task è obbligatorio', 'ro': 'Sarcina este obligatorie', 'en': 'Task is required', 'de': 'Aufgabe ist erforderlich', 'sv': 'Uppgift krävs'},
    'validation_error_title': {'it': 'Errore di Validazione', 'ro': 'Eroare de Validare', 'en': 'Validation Error', 'de': 'Validierungsfehler', 'sv': 'Valideringsfel'},
    'view_docs': {'it': 'Vedi Documenti Caricati', 'ro': 'Vezi Documente Încărcate', 'en': 'View Uploaded Documents', 'de': 'Hochgeladene Dokumente anzeigen', 'sv': 'Visa uppladdade dokument'},
    'warning_no_selection_title': {'it': 'Nessuna Selezione', 'ro': 'Nicio Selecție', 'en': 'No Selection', 'de': 'Keine Auswahl', 'sv': 'Inget val'},
    'warning_select_category_to_delete': {'it': 'Seleziona una categoria da eliminare', 'ro': 'Selectează o categorie pentru a șterge', 'en': 'Select a category to delete', 'de': 'Wählen Sie eine Kategorie zum Löschen aus', 'sv': 'Välj en kategori att radera'},
    'warning_select_dependency': {'it': 'Seleziona una dipendenza da rimuovere', 'ro': 'Selectează o dependență de eliminat', 'en': 'Select a dependency to remove', 'de': 'Wählen Sie eine Abhängigkeit zum Entfernen aus', 'sv': 'Välj ett beroende att ta bort'},
    'warning_select_predecessor': {'it': 'Seleziona un task prerequisito', 'ro': 'Selectează o sarcină prerequisit', 'en': 'Select a prerequisite task', 'de': 'Wählen Sie eine Voraussetzungsaufgabe aus', 'sv': 'Välj en förutsättningsuppgift'},
    'warning_select_product_to_create_project': {'it': 'Seleziona un prodotto per creare il progetto', 'ro': 'Selectează un produs pentru a crea proiectul', 'en': 'Select a product to create the project', 'de': 'Wählen Sie ein Produkt aus, um das Projekt zu erstellen', 'sv': 'Välj en produkt för att skapa projektet'},
    'warning_select_product_to_delete': {'it': 'Seleziona un prodotto da eliminare', 'ro': 'Selectează un produs pentru a șterge', 'en': 'Select a product to delete', 'de': 'Wählen Sie ein Produkt zum Löschen aus', 'sv': 'Välj en produkt att radera'},
    'warning_select_subject_to_delete': {'it': 'Seleziona un soggetto da eliminare', 'ro': 'Selectează un subiect pentru a șterge', 'en': 'Select a subject to delete', 'de': 'Wählen Sie ein Subjekt zum Löschen aus', 'sv': 'Välj ett ämne att radera'},
    'warning_select_task_to_delete': {'it': 'Seleziona un task da eliminare', 'ro': 'Selectează o sarcină pentru a șterge', 'en': 'Select a task to delete', 'de': 'Wählen Sie eine Aufgabe zum Löschen aus', 'sv': 'Välj en uppgift att radera'},
    'warning_title': {'it': 'Attenzione', 'ro': 'Atenție', 'en': 'Warning', 'de': 'Warnung', 'sv': 'Varning'},
}

# Genera SQL
output_file = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\NPI_COMPLETE_TRANSLATIONS.sql")

with output_file.open('w', encoding='utf-8') as f:
    f.write("-- ============================================================\n")
    f.write("-- SCRIPT COMPLETO TRADUZIONI NPI\n")
    f.write("-- Generato automaticamente da tutte le chiavi trovate nel codice\n")
    f.write("-- Tabella: [Traceability_RS].[dbo].[AppTranslations]\n")
    f.write(f"-- Totale chiavi: {len(translations)}\n")
    f.write("-- ============================================================\n\n")
    
    for key in sorted(translations.keys()):
        trans = translations[key]
        
        # IT
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        # Escape single quotes
        it_val = trans['it'].replace("'", "''")
        f.write(f"    VALUES ('it', '{key}', '{it_val}');\n\n")
        
        # RO (con N davanti)
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        ro_val = trans['ro'].replace("'", "''")
        f.write(f"    VALUES ('ro', '{key}', N'{ro_val}');\n\n")
        
        # EN
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        en_val = trans['en'].replace("'", "''")
        f.write(f"    VALUES ('en', '{key}', '{en_val}');\n\n")
        
        # DE
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        de_val = trans['de'].replace("'", "''")
        f.write(f"    VALUES ('de', '{key}', '{de_val}');\n\n")
        
        # SV
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        sv_val = trans['sv'].replace("'", "''")
        f.write(f"    VALUES ('sv', '{key}', '{sv_val}');\n\n")

print(f"\n✅ Script SQL completo generato: {output_file}")
print(f"✅ Totale chiavi tradotte: {len(translations)}")
print(f"✅ Totale INSERT statements: {len(translations) * 5}")
