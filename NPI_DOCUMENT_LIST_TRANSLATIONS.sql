-- ============================================================
-- NPI Document List Manager — Traduzioni
-- Inserisce le traduzioni per la nuova funzionalità di gestione documenti NPI.
-- Usa IF NOT EXISTS per idempotenza.
-- ============================================================

-- NPI_DOCS_TITLE
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_TITLE' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_TITLE', 'IT', 'Documenti Progetto NPI');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_TITLE' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_TITLE', 'EN', 'NPI Project Documents');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_TITLE' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_TITLE', 'RO', N'Documente Proiect NPI');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_TITLE' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_TITLE', 'SV', 'NPI-projektdokument');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_TITLE' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_TITLE', 'DE', 'NPI-Projektdokumente');

-- NPI_DOCS_SEARCH
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SEARCH' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SEARCH', 'IT', 'Cerca...');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SEARCH' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SEARCH', 'EN', 'Search...');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SEARCH' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SEARCH', 'RO', N'Căutare...');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SEARCH' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SEARCH', 'SV', 'Sök...');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SEARCH' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SEARCH', 'DE', 'Suche...');

-- NPI_DOCS_COL_TYPE
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_TYPE' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_TYPE', 'IT', 'Tipo Documento');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_TYPE' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_TYPE', 'EN', 'Document Type');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_TYPE' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_TYPE', 'RO', N'Tip Document');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_TYPE' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_TYPE', 'SV', 'Dokumenttyp');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_TYPE' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_TYPE', 'DE', 'Dokumenttyp');

-- NPI_DOCS_COL_TASK
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_TASK' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_TASK', 'IT', 'Task');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_TASK' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_TASK', 'EN', 'Task');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_TASK' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_TASK', 'RO', N'Sarcină');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_TASK' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_TASK', 'SV', 'Uppgift');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_TASK' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_TASK', 'DE', 'Aufgabe');

-- NPI_DOCS_COL_DESC
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_DESC' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_DESC', 'IT', 'Titolo Documento');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_DESC' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_DESC', 'EN', 'Document Title');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_DESC' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_DESC', 'RO', N'Titlu Document');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_DESC' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_DESC', 'SV', 'Dokumenttitel');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_DESC' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_DESC', 'DE', 'Dokumenttitel');

-- NPI_DOCS_COL_INSDATE
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_INSDATE' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_INSDATE', 'IT', 'Data Inserimento');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_INSDATE' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_INSDATE', 'EN', 'Upload Date');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_INSDATE' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_INSDATE', 'RO', N'Data Încărcării');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_INSDATE' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_INSDATE', 'SV', 'Uppladdningsdatum');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_INSDATE' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_INSDATE', 'DE', 'Hochladedatum');

-- NPI_DOCS_COL_VALUE
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_VALUE' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_VALUE', 'IT', 'Valore (€)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_VALUE' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_VALUE', 'EN', 'Value (€)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_VALUE' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_VALUE', 'RO', N'Valoare (€)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_VALUE' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_VALUE', 'SV', 'Värde (€)');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_COL_VALUE' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_COL_VALUE', 'DE', 'Wert (€)');

-- NPI_DOCS_SORT_BY
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SORT_BY' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SORT_BY', 'IT', 'Ordina per:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SORT_BY' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SORT_BY', 'EN', 'Sort by:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SORT_BY' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SORT_BY', 'RO', N'Sortare după:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SORT_BY' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SORT_BY', 'SV', 'Sortera efter:');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SORT_BY' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SORT_BY', 'DE', 'Sortieren nach:');

-- NPI_DOCS_SHOW_DELETED
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SHOW_DELETED' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SHOW_DELETED', 'IT', 'Mostra eliminati');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SHOW_DELETED' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SHOW_DELETED', 'EN', 'Show deleted');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SHOW_DELETED' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SHOW_DELETED', 'RO', N'Afișare șterse');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SHOW_DELETED' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SHOW_DELETED', 'SV', 'Visa raderade');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SHOW_DELETED' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SHOW_DELETED', 'DE', 'Gelöschte anzeigen');

-- NPI_DOCS_BTN_NEW
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_NEW' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_NEW', 'IT', 'Nuovo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_NEW' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_NEW', 'EN', 'New');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_NEW' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_NEW', 'RO', N'Nou');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_NEW' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_NEW', 'SV', 'Ny');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_NEW' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_NEW', 'DE', 'Neu');

-- NPI_DOCS_BTN_EDIT
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_EDIT' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_EDIT', 'IT', 'Modifica');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_EDIT' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_EDIT', 'EN', 'Edit');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_EDIT' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_EDIT', 'RO', N'Modificare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_EDIT' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_EDIT', 'SV', 'Redigera');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_EDIT' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_EDIT', 'DE', 'Bearbeiten');

-- NPI_DOCS_BTN_DELETE
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_DELETE' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_DELETE', 'IT', 'Elimina');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_DELETE' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_DELETE', 'EN', 'Delete');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_DELETE' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_DELETE', 'RO', N'Ștergere');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_DELETE' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_DELETE', 'SV', 'Radera');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_DELETE' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_DELETE', 'DE', 'Löschen');

-- NPI_DOCS_BTN_RESTORE
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_RESTORE' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_RESTORE', 'IT', 'Ripristina');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_RESTORE' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_RESTORE', 'EN', 'Restore');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_RESTORE' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_RESTORE', 'RO', N'Restaurare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_RESTORE' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_RESTORE', 'SV', 'Återställ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_RESTORE' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_RESTORE', 'DE', 'Wiederherstellen');

-- NPI_DOCS_BTN_REFRESH
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_REFRESH' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_REFRESH', 'IT', 'Aggiorna');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_REFRESH' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_REFRESH', 'EN', 'Refresh');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_REFRESH' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_REFRESH', 'RO', N'Reîmprospătare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_REFRESH' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_REFRESH', 'SV', 'Uppdatera');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_BTN_REFRESH' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_BTN_REFRESH', 'DE', 'Aktualisieren');

-- NPI_DOCS_STATUS_ACTIVE
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_STATUS_ACTIVE' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_STATUS_ACTIVE', 'IT', 'Attivo');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_STATUS_ACTIVE' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_STATUS_ACTIVE', 'EN', 'Active');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_STATUS_ACTIVE' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_STATUS_ACTIVE', 'RO', N'Activ');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_STATUS_ACTIVE' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_STATUS_ACTIVE', 'SV', 'Aktiv');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_STATUS_ACTIVE' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_STATUS_ACTIVE', 'DE', 'Aktiv');

-- NPI_DOCS_STATUS_DELETED
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_STATUS_DELETED' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_STATUS_DELETED', 'IT', 'Eliminato');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_STATUS_DELETED' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_STATUS_DELETED', 'EN', 'Deleted');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_STATUS_DELETED' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_STATUS_DELETED', 'RO', N'Șters');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_STATUS_DELETED' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_STATUS_DELETED', 'SV', 'Raderat');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_STATUS_DELETED' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_STATUS_DELETED', 'DE', 'Gelöscht');

-- NPI_DOCS_CONFIRM_DELETE
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_CONFIRM_DELETE' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_CONFIRM_DELETE', 'IT', 'Eliminare questo documento? Il documento non verrà cancellato fisicamente ma sarà marcato come eliminato.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_CONFIRM_DELETE' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_CONFIRM_DELETE', 'EN', 'Delete this document? The document will not be physically removed but marked as deleted.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_CONFIRM_DELETE' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_CONFIRM_DELETE', 'RO', N'Ștergeți acest document? Documentul nu va fi șters fizic, ci va fi marcat ca șters.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_CONFIRM_DELETE' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_CONFIRM_DELETE', 'SV', 'Radera detta dokument? Dokumentet raderas inte fysiskt utan markeras som raderat.');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_CONFIRM_DELETE' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_CONFIRM_DELETE', 'DE', 'Dieses Dokument löschen? Das Dokument wird nicht physisch entfernt, sondern als gelöscht markiert.');

-- NPI_DOCS_SUMMARY_TOTAL
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_TOTAL' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_TOTAL', 'IT', 'Totale documenti');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_TOTAL' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_TOTAL', 'EN', 'Total documents');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_TOTAL' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_TOTAL', 'RO', N'Total documente');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_TOTAL' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_TOTAL', 'SV', 'Totalt antal dokument');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_TOTAL' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_TOTAL', 'DE', 'Gesamtdokumente');

-- NPI_DOCS_SUMMARY_WITH_VAL
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_WITH_VAL' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_WITH_VAL', 'IT', 'Documenti con valore');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_WITH_VAL' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_WITH_VAL', 'EN', 'Documents with value');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_WITH_VAL' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_WITH_VAL', 'RO', N'Documente cu valoare');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_WITH_VAL' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_WITH_VAL', 'SV', 'Dokument med värde');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_WITH_VAL' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_WITH_VAL', 'DE', 'Dokumente mit Wert');

-- NPI_DOCS_SUMMARY_TOT_VAL
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_TOT_VAL' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_TOT_VAL', 'IT', 'Valore totale');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_TOT_VAL' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_TOT_VAL', 'EN', 'Total value');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_TOT_VAL' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_TOT_VAL', 'RO', N'Valoare totală');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_TOT_VAL' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_TOT_VAL', 'SV', 'Totalt värde');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_SUMMARY_TOT_VAL' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_SUMMARY_TOT_VAL', 'DE', 'Gesamtwert');

-- NPI_DOCS_DIALOG_NEW
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_DIALOG_NEW' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_DIALOG_NEW', 'IT', 'Nuovo Documento');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_DIALOG_NEW' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_DIALOG_NEW', 'EN', 'New Document');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_DIALOG_NEW' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_DIALOG_NEW', 'RO', N'Document Nou');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_DIALOG_NEW' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_DIALOG_NEW', 'SV', 'Nytt dokument');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_DIALOG_NEW' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_DIALOG_NEW', 'DE', 'Neues Dokument');

-- NPI_DOCS_DIALOG_EDIT
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_DIALOG_EDIT' AND LanguageCode = 'IT')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_DIALOG_EDIT', 'IT', 'Modifica Documento');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_DIALOG_EDIT' AND LanguageCode = 'EN')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_DIALOG_EDIT', 'EN', 'Edit Document');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_DIALOG_EDIT' AND LanguageCode = 'RO')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_DIALOG_EDIT', 'RO', N'Modificare Document');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_DIALOG_EDIT' AND LanguageCode = 'SV')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_DIALOG_EDIT', 'SV', 'Redigera dokument');
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[apptranslations] WHERE LabelKey = 'NPI_DOCS_DIALOG_EDIT' AND LanguageCode = 'DE')
    INSERT INTO [Traceability_RS].[dbo].[apptranslations] (LabelKey, LanguageCode, TranslatedValue) VALUES ('NPI_DOCS_DIALOG_EDIT', 'DE', 'Dokument bearbeiten');

PRINT 'NPI Document List Manager translations inserted successfully.';
