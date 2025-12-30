-- ============================================================================
-- SCRIPT COMPLETO TRADUZIONI PER GESTIONE DOCUMENTI PROGETTO NPI
-- ============================================================================
-- Database: Traceability_rs
-- Tabella: apptranslation
-- Lingue: it, en, ro, de, sv
-- Nota: Le stringhe rumene (ro) hanno la N davanti per i caratteri speciali
-- ============================================================================

USE Traceability_rs;
GO

-- ============================================================================
-- SEZIONE 1: DOCUMENTI PROGETTO
-- ============================================================================

-- project_documents
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'project_documents')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'project_documents', 'Documenti Progetto');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'project_documents')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'project_documents', 'Project Documents');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'project_documents')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'project_documents', N'Documente Proiect');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'project_documents')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'project_documents', 'Projektdokumente');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'project_documents')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'project_documents', 'Projektdokument');

-- ============================================================================
-- SEZIONE 2: BOTTONI GESTIONE DOCUMENTI
-- ============================================================================

-- btn_add_document
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'btn_add_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'btn_add_document', 'Aggiungi Documento');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'btn_add_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'btn_add_document', 'Add Document');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'btn_add_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'btn_add_document', N'Adaugă Document');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'btn_add_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'btn_add_document', 'Dokument Hinzufügen');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'btn_add_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'btn_add_document', 'Lägg Till Dokument');

-- btn_view_document
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'btn_view_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'btn_view_document', 'Visualizza');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'btn_view_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'btn_view_document', 'View');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'btn_view_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'btn_view_document', N'Vizualizare');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'btn_view_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'btn_view_document', 'Ansehen');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'btn_view_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'btn_view_document', 'Visa');

-- btn_download_document
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'btn_download_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'btn_download_document', 'Scarica');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'btn_download_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'btn_download_document', 'Download');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'btn_download_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'btn_download_document', N'Descarcă');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'btn_download_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'btn_download_document', 'Herunterladen');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'btn_download_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'btn_download_document', 'Ladda Ner');

-- ============================================================================
-- SEZIONE 3: MESSAGGI E DIALOGHI
-- ============================================================================

-- select_document
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'select_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'select_document', 'Seleziona Documento');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'select_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'select_document', 'Select Document');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'select_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'select_document', N'Selectează Document');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'select_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'select_document', 'Dokument Auswählen');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'select_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'select_document', 'Välj Dokument');

-- document_description
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'document_description')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'document_description', 'Descrizione Documento');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'document_description')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'document_description', 'Document Description');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'document_description')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'document_description', N'Descriere Document');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'document_description')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'document_description', 'Dokumentbeschreibung');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'document_description')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'document_description', 'Dokumentbeskrivning');

-- msg_select_document
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_select_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_select_document', 'Seleziona un documento dalla lista');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_select_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_select_document', 'Select a document from the list');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_select_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_select_document', N'Selectați un document din listă');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_select_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_select_document', 'Wählen Sie ein Dokument aus der Liste');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_select_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_select_document', 'Välj ett dokument från listan');

-- msg_document_added
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_document_added')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_document_added', 'Documento aggiunto con successo');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_document_added')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_document_added', 'Document added successfully');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_document_added')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_document_added', N'Document adăugat cu succes');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_document_added')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_document_added', 'Dokument erfolgreich hinzugefügt');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_document_added')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_document_added', 'Dokument tillagt');

-- msg_confirm_delete_document
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_confirm_delete_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_confirm_delete_document', 'Sei sicuro di voler eliminare questo documento?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_confirm_delete_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_confirm_delete_document', 'Are you sure you want to delete this document?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_confirm_delete_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_confirm_delete_document', N'Sigur doriți să ștergeți acest document?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_confirm_delete_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_confirm_delete_document', 'Sind Sie sicher, dass Sie dieses Dokument löschen möchten?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_confirm_delete_document')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_confirm_delete_document', 'Är du säker på att du vill ta bort detta dokument?');

-- ============================================================================
-- SEZIONE 4: AGGIORNAMENTO PROGETTO ESISTENTE
-- ============================================================================

-- msg_project_exists_update
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_project_exists_update')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_project_exists_update', 'Il progetto esiste già. Vuoi aggiornare i dati (owner, descrizione) e aggiungere documenti?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_project_exists_update')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_project_exists_update', 'Project already exists. Do you want to update data (owner, description) and add documents?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_project_exists_update')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_project_exists_update', N'Proiectul există deja. Doriți să actualizați datele (proprietar, descriere) și să adăugați documente?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_project_exists_update')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_project_exists_update', 'Projekt existiert bereits. Möchten Sie Daten (Eigentümer, Beschreibung) aktualisieren und Dokumente hinzufügen?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_project_exists_update')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_project_exists_update', 'Projektet finns redan. Vill du uppdatera data (ägare, beskrivning) och lägga till dokument?');

-- msg_project_updated
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_project_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_project_updated', 'Progetto aggiornato con successo');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_project_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_project_updated', 'Project updated successfully');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_project_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_project_updated', N'Proiect actualizat cu succes');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_project_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_project_updated', 'Projekt erfolgreich aktualisiert');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_project_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_project_updated', 'Projekt uppdaterat');

-- ============================================================================
-- SEZIONE 5: COLONNE TREEVIEW DOCUMENTI
-- ============================================================================

-- col_filename
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'col_filename')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'col_filename', 'Nome File');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'col_filename')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'col_filename', 'File Name');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'col_filename')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'col_filename', N'Nume Fișier');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'col_filename')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'col_filename', 'Dateiname');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'col_filename')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'col_filename', 'Filnamn');

-- col_filetype
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'col_filetype')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'col_filetype', 'Tipo');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'col_filetype')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'col_filetype', 'Type');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'col_filetype')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'col_filetype', 'Tip');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'col_filetype')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'col_filetype', 'Typ');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'col_filetype')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'col_filetype', 'Typ');

-- col_filesize
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'col_filesize')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'col_filesize', 'Dimensione');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'col_filesize')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'col_filesize', 'Size');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'col_filesize')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'col_filesize', 'Dimensiune');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'col_filesize')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'col_filesize', 'Größe');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'col_filesize')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'col_filesize', 'Storlek');

-- col_uploaded_by
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'col_uploaded_by')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'col_uploaded_by', 'Caricato Da');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'col_uploaded_by')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'col_uploaded_by', 'Uploaded By');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'col_uploaded_by')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'col_uploaded_by', N'Încărcat De');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'col_uploaded_by')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'col_uploaded_by', 'Hochgeladen Von');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'col_uploaded_by')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'col_uploaded_by', 'Uppladdad Av');

-- col_upload_date
IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'col_upload_date')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'col_upload_date', 'Data');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'col_upload_date')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'col_upload_date', 'Date');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'col_upload_date')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'col_upload_date', 'Data');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'col_upload_date')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'col_upload_date', 'Datum');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'col_upload_date')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'col_upload_date', 'Datum');

-- ============================================================================
-- VERIFICA INSERIMENTI
-- ============================================================================

PRINT '============================================================================';
PRINT 'VERIFICA TRADUZIONI INSERITE';
PRINT '============================================================================';

SELECT 
    translationkey,
    COUNT(*) as num_languages,
    STRING_AGG(languagecode, ', ') WITHIN GROUP (ORDER BY languagecode) as languages
FROM apptranslation
WHERE translationkey IN (
    'project_documents',
    'btn_add_document',
    'btn_view_document',
    'btn_download_document',
    'select_document',
    'document_description',
    'msg_select_document',
    'msg_document_added',
    'msg_confirm_delete_document',
    'msg_project_exists_update',
    'msg_project_updated',
    'col_filename',
    'col_filetype',
    'col_filesize',
    'col_uploaded_by',
    'col_upload_date'
)
GROUP BY translationkey
ORDER BY translationkey;

PRINT '';
PRINT 'Script completato con successo!';
PRINT 'Totale chiavi tradotte: 16';
PRINT 'Totale lingue: 5 (it, en, ro, de, sv)';
PRINT 'Totale inserimenti: 80';
GO
