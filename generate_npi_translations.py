#!/usr/bin/env python3
# Script per generare le traduzioni SQL per config_window.py

import re
from pathlib import Path

# Leggi il file config_window.py
config_file = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\npi\windows\config_window.py")
content = config_file.read_text(encoding='utf-8')

# Trova tutte le chiavi di traduzione
pattern = r"lang\.get\(['\"]([^'\"]+)['\"]"
matches = re.findall(pattern, content)

# Rimuovi duplicati e ordina
translation_keys = sorted(set(matches))

print(f"Trovate {len(translation_keys)} chiavi di traduzione uniche\n")

# Dizionario delle traduzioni
translations = {
    # Colonne
    'col_id': {
        'it': 'ID',
        'ro': 'ID',
        'en': 'ID',
        'de': 'ID',
        'sv': 'ID'
    },
    'col_name_generic': {
        'it': 'Nome',
        'ro': 'Nume',
        'en': 'Name',
        'de': 'Name',
        'sv': 'Namn'
    },
    'col_type': {
        'it': 'Tipo',
        'ro': 'Tip',
        'en': 'Type',
        'de': 'Typ',
        'sv': 'Typ'
    },
    'col_product_code': {
        'it': 'Codice Prodotto',
        'ro': 'Cod Produs',
        'en': 'Product Code',
        'de': 'Produktcode',
        'sv': 'Produktkod'
    },
    'col_product_name': {
        'it': 'Nome Prodotto',
        'ro': 'Nume Produs',
        'en': 'Product Name',
        'de': 'Produktname',
        'sv': 'Produktnamn'
    },
    'col_customer': {
        'it': 'Cliente',
        'ro': 'Client',
        'en': 'Customer',
        'de': 'Kunde',
        'sv': 'Kund'
    },
    'col_item_id': {
        'it': 'ID Elemento',
        'ro': 'ID Element',
        'en': 'Item ID',
        'de': 'Element-ID',
        'sv': 'Element-ID'
    },
    'col_task_name': {
        'it': 'Nome Task',
        'ro': 'Nume Sarcină',
        'en': 'Task Name',
        'de': 'Aufgabenname',
        'sv': 'Uppgiftsnamn'
    },
    'col_category': {
        'it': 'Categoria',
        'ro': 'Categorie',
        'en': 'Category',
        'de': 'Kategorie',
        'sv': 'Kategori'
    },
    'col_order': {
        'it': 'Ordine',
        'ro': 'Ordine',
        'en': 'Order',
        'de': 'Reihenfolge',
        'sv': 'Ordning'
    },
    'col_project_name': {
        'it': 'Nome Progetto',
        'ro': 'Nume Proiect',
        'en': 'Project Name',
        'de': 'Projektname',
        'sv': 'Projektnamn'
    },
    'col_status': {
        'it': 'Stato',
        'ro': 'Status',
        'en': 'Status',
        'de': 'Status',
        'sv': 'Status'
    },
    'col_responsible': {
        'it': 'Responsabile',
        'ro': 'Responsabil',
        'en': 'Responsible',
        'de': 'Verantwortlich',
        'sv': 'Ansvarig'
    },
    'col_deadline': {
        'it': 'Scadenza',
        'ro': 'Termen Limită',
        'en': 'Deadline',
        'de': 'Frist',
        'sv': 'Deadline'
    },
    'col_completion': {
        'it': 'Completamento',
        'ro': 'Finalizare',
        'en': 'Completion',
        'de': 'Fertigstellung',
        'sv': 'Slutförande'
    },
    
    # Titoli Frame
    'subject_details_title': {
        'it': 'Dettagli Soggetto',
        'ro': 'Detalii Subiect',
        'en': 'Subject Details',
        'de': 'Subjektdetails',
        'sv': 'Ämnesdetaljer'
    },
    'product_details_title': {
        'it': 'Dettagli Prodotto',
        'ro': 'Detalii Produs',
        'en': 'Product Details',
        'de': 'Produktdetails',
        'sv': 'Produktdetaljer'
    },
    'task_catalog_details_title': {
        'it': 'Dettagli Task Catalogo',
        'ro': 'Detalii Sarcină Catalog',
        'en': 'Task Catalog Details',
        'de': 'Aufgabenkatalog Details',
        'sv': 'Uppgiftskatalog Detaljer'
    },
    'category_details_title': {
        'it': 'Dettagli Categoria',
        'ro': 'Detalii Categorie',
        'en': 'Category Details',
        'de': 'Kategoriedetails',
        'sv': 'Kategoridetaljer'
    },
    'project_npi_management_title': {
        'it': 'Gestione Progetto NPI',
        'ro': 'Gestionare Proiect NPI',
        'en': 'NPI Project Management',
        'de': 'NPI-Projektverwaltung',
        'sv': 'NPI-projekthantering'
    },
    'project_details_title': {
        'it': 'Dettagli Progetto',
        'ro': 'Detalii Proiect',
        'en': 'Project Details',
        'de': 'Projektdetails',
        'sv': 'Projektdetaljer'
    },
    'task_details_title': {
        'it': 'Dettagli Task',
        'ro': 'Detalii Sarcină',
        'en': 'Task Details',
        'de': 'Aufgabendetails',
        'sv': 'Uppgiftsdetaljer'
    },
    
    # Label
    'label_subject_name': {
        'it': 'Nome Soggetto:',
        'ro': 'Nume Subiect:',
        'en': 'Subject Name:',
        'de': 'Subjektname:',
        'sv': 'Ämnesnamn:'
    },
    'label_type': {
        'it': 'Tipo:',
        'ro': 'Tip:',
        'en': 'Type:',
        'de': 'Typ:',
        'sv': 'Typ:'
    },
    'label_email': {
        'it': 'Email:',
        'ro': 'Email:',
        'en': 'Email:',
        'de': 'E-Mail:',
        'sv': 'E-post:'
    },
    'label_msteams_id': {
        'it': 'MS Teams User ID:',
        'ro': 'ID Utilizator MS Teams:',
        'en': 'MS Teams User ID:',
        'de': 'MS Teams Benutzer-ID:',
        'sv': 'MS Teams Användar-ID:'
    },
    'label_product_code': {
        'it': 'Codice Prodotto:',
        'ro': 'Cod Produs:',
        'en': 'Product Code:',
        'de': 'Produktcode:',
        'sv': 'Produktkod:'
    },
    'label_product_name': {
        'it': 'Nome Prodotto:',
        'ro': 'Nume Produs:',
        'en': 'Product Name:',
        'de': 'Produktname:',
        'sv': 'Produktnamn:'
    },
    'label_customer': {
        'it': 'Cliente:',
        'ro': 'Client:',
        'en': 'Customer:',
        'de': 'Kunde:',
        'sv': 'Kund:'
    },
    'label_version': {
        'it': 'Versione:',
        'ro': 'Versiune:',
        'en': 'Version:',
        'de': 'Version:',
        'sv': 'Version:'
    },
    'label_item_id': {
        'it': 'ID Elemento:',
        'ro': 'ID Element:',
        'en': 'Item ID:',
        'de': 'Element-ID:',
        'sv': 'Element-ID:'
    },
    'label_task_name': {
        'it': 'Nome Task:',
        'ro': 'Nume Sarcină:',
        'en': 'Task Name:',
        'de': 'Aufgabenname:',
        'sv': 'Uppgiftsnamn:'
    },
    'label_category': {
        'it': 'Categoria:',
        'ro': 'Categorie:',
        'en': 'Category:',
        'de': 'Kategorie:',
        'sv': 'Kategori:'
    },
    'label_description': {
        'it': 'Descrizione:',
        'ro': 'Descriere:',
        'en': 'Description:',
        'de': 'Beschreibung:',
        'sv': 'Beskrivning:'
    },
    'label_is_title': {
        'it': 'È un Titolo:',
        'ro': 'Este Titlu:',
        'en': 'Is Title:',
        'de': 'Ist Titel:',
        'sv': 'Är Titel:'
    },
    'label_category_name': {
        'it': 'Nome Categoria:',
        'ro': 'Nume Categorie:',
        'en': 'Category Name:',
        'de': 'Kategoriename:',
        'sv': 'Kategorinamn:'
    },
    'label_order_number': {
        'it': 'Numero Ordine:',
        'ro': 'Număr Ordine:',
        'en': 'Order Number:',
        'de': 'Bestellnummer:',
        'sv': 'Ordernummer:'
    },
    'label_project_name': {
        'it': 'Nome Progetto:',
        'ro': 'Nume Proiect:',
        'en': 'Project Name:',
        'de': 'Projektname:',
        'sv': 'Projektnamn:'
    },
    'label_responsible': {
        'it': 'Responsabile:',
        'ro': 'Responsabil:',
        'en': 'Responsible:',
        'de': 'Verantwortlich:',
        'sv': 'Ansvarig:'
    },
    'label_deadline': {
        'it': 'Scadenza:',
        'ro': 'Termen Limită:',
        'en': 'Deadline:',
        'de': 'Frist:',
        'sv': 'Deadline:'
    },
    'label_completion_percentage': {
        'it': 'Percentuale Completamento:',
        'ro': 'Procent Finalizare:',
        'en': 'Completion Percentage:',
        'de': 'Fertigstellungsgrad:',
        'sv': 'Slutförandeprocent:'
    },
    'label_notes': {
        'it': 'Note:',
        'ro': 'Note:',
        'en': 'Notes:',
        'de': 'Notizen:',
        'sv': 'Anteckningar:'
    },
    
    # Tipi Soggetto
    'subject_type_internal': {
        'it': 'Interno',
        'ro': 'Intern',
        'en': 'Internal',
        'de': 'Intern',
        'sv': 'Intern'
    },
    'subject_type_customer': {
        'it': 'Cliente',
        'ro': 'Client',
        'en': 'Customer',
        'de': 'Kunde',
        'sv': 'Kund'
    },
    'subject_type_supplier': {
        'it': 'Fornitore',
        'ro': 'Furnizor',
        'en': 'Supplier',
        'de': 'Lieferant',
        'sv': 'Leverantör'
    },
    
    # Bottoni
    'btn_new': {
        'it': 'Nuovo',
        'ro': 'Nou',
        'en': 'New',
        'de': 'Neu',
        'sv': 'Ny'
    },
    'btn_save': {
        'it': 'Salva',
        'ro': 'Salvează',
        'en': 'Save',
        'de': 'Speichern',
        'sv': 'Spara'
    },
    'btn_delete': {
        'it': 'Elimina',
        'ro': 'Șterge',
        'en': 'Delete',
        'de': 'Löschen',
        'sv': 'Radera'
    },
    'btn_create_npi_project': {
        'it': 'Crea Progetto NPI',
        'ro': 'Creează Proiect NPI',
        'en': 'Create NPI Project',
        'de': 'NPI-Projekt erstellen',
        'sv': 'Skapa NPI-projekt'
    },
    'btn_add_task': {
        'it': 'Aggiungi Task',
        'ro': 'Adaugă Sarcină',
        'en': 'Add Task',
        'de': 'Aufgabe hinzufügen',
        'sv': 'Lägg till uppgift'
    },
    'btn_close': {
        'it': 'Chiudi',
        'ro': 'Închide',
        'en': 'Close',
        'de': 'Schließen',
        'sv': 'Stäng'
    },
    
    # Messaggi di Successo
    'success_title': {
        'it': 'Successo',
        'ro': 'Succes',
        'en': 'Success',
        'de': 'Erfolg',
        'sv': 'Framgång'
    },
    'success_subject_saved': {
        'it': 'Soggetto salvato con successo.',
        'ro': 'Subiect salvat cu succes.',
        'en': 'Subject saved successfully.',
        'de': 'Subjekt erfolgreich gespeichert.',
        'sv': 'Ämne sparat framgångsrikt.'
    },
    'success_subject_deleted': {
        'it': 'Soggetto eliminato con successo.',
        'ro': 'Subiect șters cu succes.',
        'en': 'Subject deleted successfully.',
        'de': 'Subjekt erfolgreich gelöscht.',
        'sv': 'Ämne raderat framgångsrikt.'
    },
    'success_product_saved': {
        'it': 'Prodotto salvato con successo.',
        'ro': 'Produs salvat cu succes.',
        'en': 'Product saved successfully.',
        'de': 'Produkt erfolgreich gespeichert.',
        'sv': 'Produkt sparat framgångsrikt.'
    },
    'success_product_deleted': {
        'it': 'Prodotto eliminato con successo.',
        'ro': 'Produs șters cu succes.',
        'en': 'Product deleted successfully.',
        'de': 'Produkt erfolgreich gelöscht.',
        'sv': 'Produkt raderat framgångsrikt.'
    },
    'success_project_created': {
        'it': 'Progetto NPI creato con successo per il prodotto: {product_name}',
        'ro': 'Proiect NPI creat cu succes pentru produsul: {product_name}',
        'en': 'NPI Project created successfully for product: {product_name}',
        'de': 'NPI-Projekt erfolgreich erstellt für Produkt: {product_name}',
        'sv': 'NPI-projekt skapat framgångsrikt för produkt: {product_name}'
    },
    'success_task_saved': {
        'it': 'Task salvato con successo.',
        'ro': 'Sarcină salvată cu succes.',
        'en': 'Task saved successfully.',
        'de': 'Aufgabe erfolgreich gespeichert.',
        'sv': 'Uppgift sparad framgångsrikt.'
    },
    'success_task_deleted': {
        'it': 'Task eliminato con successo.',
        'ro': 'Sarcină ștearsă cu succes.',
        'en': 'Task deleted successfully.',
        'de': 'Aufgabe erfolgreich gelöscht.',
        'sv': 'Uppgift raderad framgångsrikt.'
    },
    'success_category_saved': {
        'it': 'Categoria salvata con successo.',
        'ro': 'Categorie salvată cu succes.',
        'en': 'Category saved successfully.',
        'de': 'Kategorie erfolgreich gespeichert.',
        'sv': 'Kategori sparad framgångsrikt.'
    },
    'success_category_deleted': {
        'it': 'Categoria eliminata con successo.',
        'ro': 'Categorie ștearsă cu succes.',
        'en': 'Category deleted successfully.',
        'de': 'Kategorie erfolgreich gelöscht.',
        'sv': 'Kategori raderad framgångsrikt.'
    },
    'success_project_saved': {
        'it': 'Progetto salvato con successo.',
        'ro': 'Proiect salvat cu succes.',
        'en': 'Project saved successfully.',
        'de': 'Projekt erfolgreich gespeichert.',
        'sv': 'Projekt sparat framgångsrikt.'
    },
    'success_project_deleted': {
        'it': 'Progetto eliminato con successo.',
        'ro': 'Proiect șters cu succes.',
        'en': 'Project deleted successfully.',
        'de': 'Projekt erfolgreich gelöscht.',
        'sv': 'Projekt raderat framgångsrikt.'
    },
    'success_project_task_saved': {
        'it': 'Task di progetto salvato con successo.',
        'ro': 'Sarcină proiect salvată cu succes.',
        'en': 'Project task saved successfully.',
        'de': 'Projektaufgabe erfolgreich gespeichert.',
        'sv': 'Projektuppgift sparad framgångsrikt.'
    },
    'success_project_task_deleted': {
        'it': 'Task di progetto eliminato con successo.',
        'ro': 'Sarcină proiect ștearsă cu succes.',
        'en': 'Project task deleted successfully.',
        'de': 'Projektaufgabe erfolgreich gelöscht.',
        'sv': 'Projektuppgift raderad framgångsrikt.'
    },
    
    # Messaggi di Errore
    'error_title': {
        'it': 'Errore',
        'ro': 'Eroare',
        'en': 'Error',
        'de': 'Fehler',
        'sv': 'Fel'
    },
    'error_duplicate_title': {
        'it': 'Duplicato',
        'ro': 'Duplicat',
        'en': 'Duplicate',
        'de': 'Duplikat',
        'sv': 'Duplikat'
    },
    'validation_error_subject_required': {
        'it': 'Nome e Tipo sono campi obbligatori.',
        'ro': 'Nume și Tip sunt câmpuri obligatorii.',
        'en': 'Name and Type are required fields.',
        'de': 'Name und Typ sind Pflichtfelder.',
        'sv': 'Namn och Typ är obligatoriska fält.'
    },
    'validation_error_product_name_required': {
        'it': 'Il Nome Prodotto è obbligatorio.',
        'ro': 'Numele Produsului este obligatoriu.',
        'en': 'Product Name is required.',
        'de': 'Produktname ist erforderlich.',
        'sv': 'Produktnamn krävs.'
    },
    'validation_error_task_required': {
        'it': 'ID Elemento e Nome Task sono obbligatori.',
        'ro': 'ID Element și Nume Sarcină sunt obligatorii.',
        'en': 'Item ID and Task Name are required.',
        'de': 'Element-ID und Aufgabenname sind erforderlich.',
        'sv': 'Element-ID och Uppgiftsnamn krävs.'
    },
    'validation_error_duplicate_itemid': {
        'it': 'Esiste già un task con ItemID: {itemid}',
        'ro': 'Există deja o sarcină cu ID Element: {itemid}',
        'en': 'A task with ItemID: {itemid} already exists',
        'de': 'Eine Aufgabe mit Element-ID: {itemid} existiert bereits',
        'sv': 'En uppgift med Element-ID: {itemid} finns redan'
    },
    'validation_error_category_required': {
        'it': 'Il Nome Categoria è obbligatorio.',
        'ro': 'Numele Categoriei este obligatoriu.',
        'en': 'Category Name is required.',
        'de': 'Kategoriename ist erforderlich.',
        'sv': 'Kategorinamn krävs.'
    },
    'validation_error_project_required': {
        'it': 'Seleziona un prodotto e specifica un nome progetto.',
        'ro': 'Selectează un produs și specifică un nume de proiect.',
        'en': 'Select a product and specify a project name.',
        'de': 'Wählen Sie ein Produkt aus und geben Sie einen Projektnamen an.',
        'sv': 'Välj en produkt och ange ett projektnamn.'
    },
    'validation_error_task_fields_required': {
        'it': 'Task, Responsabile e Scadenza sono obbligatori.',
        'ro': 'Sarcină, Responsabil și Termen Limită sunt obligatorii.',
        'en': 'Task, Responsible and Deadline are required.',
        'de': 'Aufgabe, Verantwortlich und Frist sind erforderlich.',
        'sv': 'Uppgift, Ansvarig och Deadline krävs.'
    },
    'error_create_project': {
        'it': 'Errore durante la creazione del progetto: {error}',
        'ro': 'Eroare la crearea proiectului: {error}',
        'en': 'Error creating project: {error}',
        'de': 'Fehler beim Erstellen des Projekts: {error}',
        'sv': 'Fel vid skapande av projekt: {error}'
    },
    
    # Messaggi Database
    'db_error_title': {
        'it': 'Errore Database',
        'ro': 'Eroare Bază de Date',
        'en': 'Database Error',
        'de': 'Datenbankfehler',
        'sv': 'Databasfel'
    },
    'db_error_generic_save': {
        'it': 'Errore durante il salvataggio: {error}',
        'ro': 'Eroare la salvare: {error}',
        'en': 'Error during save: {error}',
        'de': 'Fehler beim Speichern: {error}',
        'sv': 'Fel vid sparande: {error}'
    },
    'db_error_delete_subject': {
        'it': 'Errore durante l\'eliminazione del soggetto: {error}',
        'ro': 'Eroare la ștergerea subiectului: {error}',
        'en': 'Error deleting subject: {error}',
        'de': 'Fehler beim Löschen des Subjekts: {error}',
        'sv': 'Fel vid radering av ämne: {error}'
    },
    'db_error_delete_product': {
        'it': 'Errore durante l\'eliminazione del prodotto: {error}',
        'ro': 'Eroare la ștergerea produsului: {error}',
        'en': 'Error deleting product: {error}',
        'de': 'Fehler beim Löschen des Produkts: {error}',
        'sv': 'Fel vid radering av produkt: {error}'
    },
    'db_error_save_task': {
        'it': 'Errore durante il salvataggio del task: {error}',
        'ro': 'Eroare la salvarea sarcinii: {error}',
        'en': 'Error saving task: {error}',
        'de': 'Fehler beim Speichern der Aufgabe: {error}',
        'sv': 'Fel vid sparande av uppgift: {error}'
    },
    'db_error_delete_task': {
        'it': 'Errore durante l\'eliminazione del task: {error}',
        'ro': 'Eroare la ștergerea sarcinii: {error}',
        'en': 'Error deleting task: {error}',
        'de': 'Fehler beim Löschen der Aufgabe: {error}',
        'sv': 'Fel vid radering av uppgift: {error}'
    },
    'db_error_load_categories': {
        'it': 'Errore durante il caricamento delle categorie: {error}',
        'ro': 'Eroare la încărcarea categoriilor: {error}',
        'en': 'Error loading categories: {error}',
        'de': 'Fehler beim Laden der Kategorien: {error}',
        'sv': 'Fel vid laddning av kategorier: {error}'
    },
    'db_error_delete_category': {
        'it': 'Errore durante l\'eliminazione della categoria: {error}',
        'ro': 'Eroare la ștergerea categoriei: {error}',
        'en': 'Error deleting category: {error}',
        'de': 'Fehler beim Löschen der Kategorie: {error}',
        'sv': 'Fel vid radering av kategori: {error}'
    },
    'db_error_delete_project': {
        'it': 'Errore durante l\'eliminazione del progetto: {error}',
        'ro': 'Eroare la ștergerea proiectului: {error}',
        'en': 'Error deleting project: {error}',
        'de': 'Fehler beim Löschen des Projekts: {error}',
        'sv': 'Fel vid radering av projekt: {error}'
    },
    'db_error_delete_project_task': {
        'it': 'Errore durante l\'eliminazione del task di progetto: {error}',
        'ro': 'Eroare la ștergerea sarcinii proiectului: {error}',
        'en': 'Error deleting project task: {error}',
        'de': 'Fehler beim Löschen der Projektaufgabe: {error}',
        'sv': 'Fel vid radering av projektuppgift: {error}'
    },
    
    # Avvisi
    'warning_no_selection_title': {
        'it': 'Nessuna Selezione',
        'ro': 'Nicio Selecție',
        'en': 'No Selection',
        'de': 'Keine Auswahl',
        'sv': 'Inget Val'
    },
    'warning_select_subject_to_delete': {
        'it': 'Seleziona un soggetto da eliminare.',
        'ro': 'Selectează un subiect pentru a șterge.',
        'en': 'Select a subject to delete.',
        'de': 'Wählen Sie ein Subjekt zum Löschen aus.',
        'sv': 'Välj ett ämne att radera.'
    },
    'warning_select_product_to_delete': {
        'it': 'Seleziona un prodotto da eliminare.',
        'ro': 'Selectează un produs pentru a șterge.',
        'en': 'Select a product to delete.',
        'de': 'Wählen Sie ein Produkt zum Löschen aus.',
        'sv': 'Välj en produkt att radera.'
    },
    'warning_select_product_to_create_project': {
        'it': 'Seleziona un prodotto per creare un progetto NPI.',
        'ro': 'Selectează un produs pentru a crea un proiect NPI.',
        'en': 'Select a product to create an NPI project.',
        'de': 'Wählen Sie ein Produkt aus, um ein NPI-Projekt zu erstellen.',
        'sv': 'Välj en produkt för att skapa ett NPI-projekt.'
    },
    'warning_select_task_to_delete': {
        'it': 'Seleziona un task da eliminare.',
        'ro': 'Selectează o sarcină pentru a șterge.',
        'en': 'Select a task to delete.',
        'de': 'Wählen Sie eine Aufgabe zum Löschen aus.',
        'sv': 'Välj en uppgift att radera.'
    },
    'warning_select_category_to_delete': {
        'it': 'Seleziona una categoria da eliminare.',
        'ro': 'Selectează o categorie pentru a șterge.',
        'en': 'Select a category to delete.',
        'de': 'Wählen Sie eine Kategorie zum Löschen aus.',
        'sv': 'Välj en kategori att radera.'
    },
    'warning_select_project_to_delete': {
        'it': 'Seleziona un progetto da eliminare.',
        'ro': 'Selectează un proiect pentru a șterge.',
        'en': 'Select a project to delete.',
        'de': 'Wählen Sie ein Projekt zum Löschen aus.',
        'sv': 'Välj ett projekt att radera.'
    },
    'warning_select_project_task_to_delete': {
        'it': 'Seleziona un task di progetto da eliminare.',
        'ro': 'Selectează o sarcină de proiect pentru a șterge.',
        'en': 'Select a project task to delete.',
        'de': 'Wählen Sie eine Projektaufgabe zum Löschen aus.',
        'sv': 'Välj en projektuppgift att radera.'
    },
    
    # Conferme
    'confirm_delete_title': {
        'it': 'Conferma Eliminazione',
        'ro': 'Confirmă Ștergerea',
        'en': 'Confirm Deletion',
        'de': 'Löschen bestätigen',
        'sv': 'Bekräfta Radering'
    },
    'confirm_delete_subject_text': {
        'it': 'Sei sicuro di voler eliminare questo soggetto?',
        'ro': 'Ești sigur că vrei să ștergi acest subiect?',
        'en': 'Are you sure you want to delete this subject?',
        'de': 'Sind Sie sicher, dass Sie dieses Subjekt löschen möchten?',
        'sv': 'Är du säker på att du vill radera detta ämne?'
    },
    'confirm_delete_product_text': {
        'it': 'Sei sicuro di voler eliminare questo prodotto?',
        'ro': 'Ești sigur că vrei să ștergi acest produs?',
        'en': 'Are you sure you want to delete this product?',
        'de': 'Sind Sie sicher, dass Sie dieses Produkt löschen möchten?',
        'sv': 'Är du säker på att du vill radera denna produkt?'
    },
    'confirm_delete_task_text': {
        'it': 'Sei sicuro di voler eliminare questo task?',
        'ro': 'Ești sigur că vrei să ștergi această sarcină?',
        'en': 'Are you sure you want to delete this task?',
        'de': 'Sind Sie sicher, dass Sie diese Aufgabe löschen möchten?',
        'sv': 'Är du säker på att du vill radera denna uppgift?'
    },
    'confirm_delete_category_text': {
        'it': 'Sei sicuro di voler eliminare questa categoria?',
        'ro': 'Ești sigur că vrei să ștergi această categorie?',
        'en': 'Are you sure you want to delete this category?',
        'de': 'Sind Sie sicher, dass Sie diese Kategorie löschen möchten?',
        'sv': 'Är du säker på att du vill radera denna kategori?'
    },
    'confirm_delete_project_text': {
        'it': 'Sei sicuro di voler eliminare questo progetto?',
        'ro': 'Ești sigur că vrei să ștergi acest proiect?',
        'en': 'Are you sure you want to delete this project?',
        'de': 'Sind Sie sicher, dass Sie dieses Projekt löschen möchten?',
        'sv': 'Är du säker på att du vill radera detta projekt?'
    },
    'confirm_delete_project_task_text': {
        'it': 'Sei sicuro di voler eliminare questo task di progetto?',
        'ro': 'Ești sigur că vrei să ștergi această sarcină de proiect?',
        'en': 'Are you sure you want to delete this project task?',
        'de': 'Sind Sie sicher, dass Sie diese Projektaufgabe löschen möchten?',
        'sv': 'Är du säker på att du vill radera denna projektuppgift?'
    },
    
    # Info
    'info_title': {
        'it': 'Informazione',
        'ro': 'Informație',
        'en': 'Information',
        'de': 'Information',
        'sv': 'Information'
    },
    'info_project_already_exists': {
        'it': 'Esiste già un progetto NPI attivo per questo prodotto.',
        'ro': 'Există deja un proiect NPI activ pentru acest produs.',
        'en': 'An active NPI project already exists for this product.',
        'de': 'Es existiert bereits ein aktives NPI-Projekt für dieses Produkt.',
        'sv': 'Ett aktivt NPI-projekt finns redan för denna produkt.'
    },
}

# Genera lo script SQL
output_file = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\NPI_CONFIG_TRANSLATIONS.sql")

with output_file.open('w', encoding='utf-8') as f:
    f.write("-- Script di traduzione per NPI Config Window\n")
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
