-- ============================================================
-- NPI Budget Documents Translations
-- Languages: IT, RO (N''), EN, SV, DE
-- ============================================================
USE Traceability_RS
GO

-- budget_docs_panel
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_docs_panel')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_docs_panel','📎 Documenti Riga');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_docs_panel')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_docs_panel',N'📎 Documente Rând');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_docs_panel')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_docs_panel','📎 Row Documents');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_docs_panel')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_docs_panel','📎 Rad Dokument');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_docs_panel')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_docs_panel','📎 Zeilen-Dokumente');
GO

-- budget_btn_upload_doc
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_upload_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_upload_doc','📎 Carica Doc.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_upload_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_upload_doc',N'📎 Încarcă Doc.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_upload_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_upload_doc','📎 Upload Doc.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_upload_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_upload_doc','📎 Ladda upp Dok.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_upload_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_upload_doc','📎 Dok. hochladen');
GO

-- budget_btn_link_doc
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_link_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_link_doc','🔗 Collega Esistente');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_link_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_link_doc',N'🔗 Leagă Existent');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_link_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_link_doc','🔗 Link Existing');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_link_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_link_doc','🔗 Koppla Befintlig');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_link_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_link_doc','🔗 Bestehendes verknüpfen');
GO

-- budget_btn_unlink_doc
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_unlink_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_unlink_doc','❌ Scollega');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_unlink_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_unlink_doc',N'❌ Dezleagă');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_unlink_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_unlink_doc','❌ Unlink');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_unlink_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_unlink_doc','❌ Avkoppla');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_unlink_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_unlink_doc','❌ Verknüpfung aufheben');
GO

-- budget_btn_open_doc
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_open_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_open_doc','👁️ Apri');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_open_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_open_doc',N'👁️ Deschide');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_open_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_open_doc','👁️ Open');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_open_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_open_doc','👁️ Öppna');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_open_doc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_open_doc','👁️ Öffnen');
GO

-- budget_doc_col_title / type / date / user
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_doc_col_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_doc_col_title','Titolo');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_doc_col_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_doc_col_title',N'Titlu');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_doc_col_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_doc_col_title','Title');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_doc_col_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_doc_col_title','Titel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_doc_col_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_doc_col_title','Titel');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_doc_col_type')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_doc_col_type','Tipo');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_doc_col_type')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_doc_col_type',N'Tip');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_doc_col_type')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_doc_col_type','Type');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_doc_col_type')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_doc_col_type','Typ');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_doc_col_type')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_doc_col_type','Typ');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_doc_col_date')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_doc_col_date','Data');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_doc_col_date')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_doc_col_date',N'Dată');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_doc_col_date')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_doc_col_date','Date');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_doc_col_date')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_doc_col_date','Datum');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_doc_col_date')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_doc_col_date','Datum');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_doc_col_user')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_doc_col_user','Utente');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_doc_col_user')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_doc_col_user',N'Utilizator');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_doc_col_user')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_doc_col_user','User');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_doc_col_user')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_doc_col_user','Användare');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_doc_col_user')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_doc_col_user','Benutzer');
GO

-- budget_doc_select_existing
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_doc_select_existing')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_doc_select_existing','Seleziona Documento');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_doc_select_existing')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_doc_select_existing',N'Selectează Document');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_doc_select_existing')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_doc_select_existing','Select Document');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_doc_select_existing')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_doc_select_existing','Välj Dokument');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_doc_select_existing')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_doc_select_existing','Dokument auswählen');
GO

-- budget_doc_none
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_doc_none')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_doc_none','Nessun documento disponibile da collegare.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_doc_none')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_doc_none',N'Niciun document disponibil pentru conectare.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_doc_none')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_doc_none','No documents available to link.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_doc_none')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_doc_none','Inga dokument tillgängliga att koppla.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_doc_none')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_doc_none','Keine Dokumente zum Verknüpfen verfügbar.');
GO

-- budget_doc_select
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_doc_select')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_doc_select','Selezionare un documento.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_doc_select')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_doc_select',N'Selectați un document.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_doc_select')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_doc_select','Select a document.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_doc_select')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_doc_select','Välj ett dokument.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_doc_select')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_doc_select','Wählen Sie ein Dokument.');
GO

-- budget_doc_unlink_confirm
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_doc_unlink_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_doc_unlink_confirm','Scollegare il documento dalla riga di budget?
(Il documento non verrà eliminato)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_doc_unlink_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_doc_unlink_confirm',N'Dezlegați documentul de la rândul bugetului?
(Documentul nu va fi șters)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_doc_unlink_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_doc_unlink_confirm','Unlink document from budget row?
(The document will not be deleted)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_doc_unlink_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_doc_unlink_confirm','Koppla bort dokument från budgetraden?
(Dokumentet kommer inte att raderas)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_doc_unlink_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_doc_unlink_confirm','Dokument von Budgetzeile trennen?
(Das Dokument wird nicht gelöscht)');
GO

-- budget_doc_select_type
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_doc_select_type')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_doc_select_type','Tipo Documento');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_doc_select_type')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_doc_select_type',N'Tip Document');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_doc_select_type')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_doc_select_type','Document Type');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_doc_select_type')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_doc_select_type','Dokumenttyp');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_doc_select_type')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_doc_select_type','Dokumenttyp');
GO

PRINT '✅ Traduzioni Documenti Budget NPI completate'
GO
