-- File: NPI_DEPENDENCIES_TRANSLATIONS.sql
-- Script per caricare le traduzioni per la nuova gestione dipendenze NPI
-- Lingue: IT, EN, RO, DE, SV (Sloveno)

BEGIN TRANSACTION;

-- Inserimento traduzioni
-- Chiave: manage_dependencies_title
IF NOT EXISTS (SELECT 1 FROM Traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'manage_dependencies_title')
BEGIN
    INSERT INTO Traceability_rs.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES 
    ('IT', 'manage_dependencies_title', 'Gestione Dipendenze Task'),
    ('EN', 'manage_dependencies_title', 'Task Dependencies Management'),
    ('RO', 'manage_dependencies_title', 'Gestionare Dependențe Sarcină'),
    ('DE', 'manage_dependencies_title', 'Aufgabenabhängigkeiten verwalten'),
    ('SV', 'manage_dependencies_title', 'Upravljanje odvisnosti nalog');
END

-- Chiave: dependencies_summary
IF NOT EXISTS (SELECT 1 FROM Traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'dependencies_summary')
BEGIN
    INSERT INTO Traceability_rs.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES 
    ('IT', 'dependencies_summary', 'Sommario Dipendenze'),
    ('EN', 'dependencies_summary', 'Dependencies Summary'),
    ('RO', 'dependencies_summary', 'Sumar Dependențe'),
    ('DE', 'dependencies_summary', 'Abhängigkeitsübersicht'),
    ('SV', 'dependencies_summary', 'Povzetek odvisnosti');
END

-- Chiave: btn_manage_dependencies
IF NOT EXISTS (SELECT 1 FROM Traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'btn_manage_dependencies')
BEGIN
    INSERT INTO Traceability_rs.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES 
    ('IT', 'btn_manage_dependencies', 'Gestione Dipendenze...'),
    ('EN', 'btn_manage_dependencies', 'Manage Dependencies...'),
    ('RO', 'btn_manage_dependencies', 'Gestionează Dependențe...'),
    ('DE', 'btn_manage_dependencies', 'Abhängigkeiten verwalten...'),
    ('SV', 'btn_manage_dependencies', 'Upravljanje odvisnosti...');
END

-- Chiave: add_dependency_title
IF NOT EXISTS (SELECT 1 FROM Traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'add_dependency_title')
BEGIN
    INSERT INTO Traceability_rs.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES 
    ('IT', 'add_dependency_title', 'Aggiungi Nuova Dipendenza'),
    ('EN', 'add_dependency_title', 'Add New Dependency'),
    ('RO', 'add_dependency_title', 'Adaugă Dependență Nouă'),
    ('DE', 'add_dependency_title', 'Neue Abhängigkeit hinzufügen'),
    ('SV', 'add_dependency_title', 'Dodaj novo odvisnost');
END

-- Chiave: col_type
IF NOT EXISTS (SELECT 1 FROM Traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'col_type')
BEGIN
    INSERT INTO Traceability_rs.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES 
    ('IT', 'col_type', 'Tipo'),
    ('EN', 'col_type', 'Type'),
    ('RO', 'col_type', 'Tip'),
    ('DE', 'col_type', 'Typ'),
    ('SV', 'col_type', 'Vrsta');
END

-- Chiave: filter_category
IF NOT EXISTS (SELECT 1 FROM Traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'filter_category')
BEGIN
    INSERT INTO Traceability_rs.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES 
    ('IT', 'filter_category', 'Filtra per Categoria:'),
    ('EN', 'filter_category', 'Filter by Category:'),
    ('RO', 'filter_category', 'Filtrează după Categorie:'),
    ('DE', 'filter_category', 'Nach Kategorie filtern:'),
    ('SV', 'filter_category', 'Filtriraj po kategoriji:');
END

-- Chiave: select_task
IF NOT EXISTS (SELECT 1 FROM Traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'select_task')
BEGIN
    INSERT INTO Traceability_rs.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES 
    ('IT', 'select_task', 'Seleziona Task Prerequisito:'),
    ('EN', 'select_task', 'Select Prerequisite Task:'),
    ('RO', 'select_task', 'Selectează Sarcină Prerevizită:'),
    ('DE', 'select_task', 'Voraussetzungsaufgabe auswählen:'),
    ('SV', 'select_task', 'Izberite predhodno nalogo:');
END

-- Chiave: current_dependencies
IF NOT EXISTS (SELECT 1 FROM Traceability_rs.dbo.AppTranslations WHERE TranslationKey = 'current_dependencies')
BEGIN
    INSERT INTO Traceability_rs.dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES 
    ('IT', 'current_dependencies', 'Dipendenze Attuali'),
    ('EN', 'current_dependencies', 'Current Dependencies'),
    ('RO', 'current_dependencies', 'Dependențe Actuale'),
    ('DE', 'current_dependencies', 'Aktuelle Abhängigkeiten'),
    ('SV', 'current_dependencies', 'Trenutne odvisnosti');
END

COMMIT;
PRINT 'Traduzioni NPI (IT, EN, RO, DE, SV) caricate con successo.';
