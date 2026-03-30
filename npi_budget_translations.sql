-- ============================================================
-- NPI Budget Management System - Translations
-- Languages: IT, RO (N''), EN, SV, DE 
-- ============================================================
USE Traceability_RS
GO

-- ==========================================
-- Budget Window translations
-- ==========================================

-- btn_budget
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='btn_budget')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','btn_budget','💰 Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='btn_budget')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','btn_budget',N'💰 Buget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='btn_budget')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','btn_budget','💰 Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='btn_budget')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','btn_budget','💰 Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='btn_budget')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','btn_budget','💰 Budget');
GO

-- budget_title
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_title','Budget Progetto');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_title',N'Buget Proiect');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_title','Project Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_title','Projektbudget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_title','Projektbudget');
GO

-- budget_header
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_header')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_header','Budget Progetto NPI');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_header')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_header',N'Buget Proiect NPI');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_header')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_header','NPI Project Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_header')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_header','NPI Projektbudget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_header')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_header','NPI Projektbudget');
GO

-- budget_selector
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_selector')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_selector','Seleziona Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_selector')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_selector',N'Selectează Buget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_selector')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_selector','Select Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_selector')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_selector','Välj Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_selector')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_selector','Budget auswählen');
GO

-- budget_btn_new
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_new')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_new','➕ Nuovo Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_new')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_new',N'➕ Buget Nou');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_new')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_new','➕ New Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_new')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_new','➕ Ny Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_new')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_new','➕ Neues Budget');
GO

-- budget_btn_delete
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_delete','🗑️ Elimina Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_delete',N'🗑️ Șterge Buget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_delete','🗑️ Delete Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_delete','🗑️ Ta bort Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_delete','🗑️ Budget löschen');
GO

-- budget_btn_activate
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_activate')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_activate','✅ Imposta Attivo');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_activate')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_activate',N'✅ Setează Activ');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_activate')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_activate','✅ Set Active');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_activate')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_activate','✅ Ställ in Aktiv');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_activate')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_activate','✅ Aktiv setzen');
GO

-- budget_btn_template
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_template')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_template','📥 Scarica Template');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_template')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_template',N'📥 Descarcă Șablon');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_template')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_template','📥 Download Template');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_template')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_template','📥 Ladda ner Mall');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_template')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_template','📥 Vorlage herunterladen');
GO

-- budget_btn_import
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_import')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_import','📤 Importa Excel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_import')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_import',N'📤 Importă Excel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_import')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_import','📤 Import Excel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_import')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_import','📤 Importera Excel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_import')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_import','📤 Excel importieren');
GO

-- budget_btn_export
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_export')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_export','📊 Esporta Excel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_export')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_export',N'📊 Exportă Excel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_export')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_export','📊 Export Excel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_export')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_export','📊 Exportera Excel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_export')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_export','📊 Excel exportieren');
GO

-- budget_col_desc
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_col_desc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_col_desc','Descrizione');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_col_desc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_col_desc',N'Descriere');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_col_desc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_col_desc','Description');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_col_desc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_col_desc','Beskrivning');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_col_desc')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_col_desc','Beschreibung');
GO

-- budget_col_category
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_col_category')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_col_category','Categoria');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_col_category')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_col_category',N'Categorie');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_col_category')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_col_category','Category');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_col_category')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_col_category','Kategori');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_col_category')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_col_category','Kategorie');
GO

-- budget_col_qty
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_col_qty')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_col_qty','Qtà');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_col_qty')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_col_qty',N'Cantitate');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_col_qty')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_col_qty','Qty');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_col_qty')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_col_qty','Antal');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_col_qty')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_col_qty','Menge');
GO

-- budget_col_unit_price
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_col_unit_price')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_col_unit_price','Prezzo Unit.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_col_unit_price')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_col_unit_price',N'Preț Unitar');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_col_unit_price')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_col_unit_price','Unit Price');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_col_unit_price')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_col_unit_price','Enhetspris');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_col_unit_price')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_col_unit_price','Stückpreis');
GO

-- budget_col_total
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_col_total')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_col_total','Totale');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_col_total')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_col_total',N'Total');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_col_total')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_col_total','Total');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_col_total')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_col_total','Totalt');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_col_total')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_col_total','Gesamt');
GO

-- budget_btn_add_item
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_add_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_add_item','➕ Aggiungi Riga');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_add_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_add_item',N'➕ Adaugă Rând');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_add_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_add_item','➕ Add Row');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_add_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_add_item','➕ Lägg till Rad');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_add_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_add_item','➕ Zeile hinzufügen');
GO

-- budget_btn_update_item
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_update_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_update_item','💾 Aggiorna Riga');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_update_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_update_item',N'💾 Actualizează Rând');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_update_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_update_item','💾 Update Row');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_update_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_update_item','💾 Uppdatera Rad');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_update_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_update_item','💾 Zeile aktualisieren');
GO

-- budget_btn_delete_item
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_delete_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_delete_item','🗑️ Elimina Riga');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_delete_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_delete_item',N'🗑️ Șterge Rând');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_delete_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_delete_item','🗑️ Delete Row');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_delete_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_delete_item','🗑️ Ta bort Rad');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_delete_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_delete_item','🗑️ Zeile löschen');
GO

-- budget_new_title / budget_new_prompt
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_new_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_new_title','Nuovo Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_new_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_new_title',N'Buget Nou');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_new_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_new_title','New Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_new_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_new_title','Ny Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_new_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_new_title','Neues Budget');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_new_prompt')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_new_prompt','Nome del budget:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_new_prompt')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_new_prompt',N'Numele bugetului:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_new_prompt')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_new_prompt','Budget name:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_new_prompt')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_new_prompt','Budgetnamn:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_new_prompt')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_new_prompt','Budgetname:');
GO

-- tab_budget_categories
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='tab_budget_categories')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','tab_budget_categories','Categorie Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='tab_budget_categories')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','tab_budget_categories',N'Categorii Buget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='tab_budget_categories')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','tab_budget_categories','Budget Categories');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='tab_budget_categories')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','tab_budget_categories','Budgetkategorier');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='tab_budget_categories')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','tab_budget_categories','Budgetkategorien');
GO

-- budget_cat_name
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_cat_name')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_cat_name','Nome Categoria');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_cat_name')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_cat_name',N'Nume Categorie');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_cat_name')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_cat_name','Category Name');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_cat_name')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_cat_name','Kategorinamn');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_cat_name')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_cat_name','Kategoriename');
GO

-- budget status + detail + other labels
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_status_label')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_status_label','Stato:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_status_label')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_status_label',N'Stare:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_status_label')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_status_label','Status:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_status_label')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_status_label','Status:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_status_label')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_status_label','Status:');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_detail')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_detail','Dettaglio Riga');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_detail')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_detail',N'Detaliu Rând');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_detail')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_detail','Row Detail');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_detail')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_detail','Raddetalj');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_detail')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_detail','Zeilendetail');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_save_status')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_save_status','💾 Salva Stato');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_save_status')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_save_status',N'💾 Salvează Stare');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_save_status')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_save_status','💾 Save Status');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_save_status')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_save_status','💾 Spara Status');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_save_status')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_save_status','💾 Status speichern');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_clear')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_clear','🧹 Pulisci');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_clear')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_clear',N'🧹 Curăță');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_clear')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_clear','🧹 Clear');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_clear')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_clear','🧹 Rensa');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_clear')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_clear','🧹 Leeren');
GO

-- budget_col_status
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_col_status')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_col_status','Stato');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_col_status')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_col_status',N'Stare');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_col_status')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_col_status','Status');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_col_status')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_col_status','Status');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_col_status')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_col_status','Status');
GO

-- budget_col_approval
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_col_approval')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_col_approval','Approvazione');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_col_approval')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_col_approval',N'Aprobare');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_col_approval')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_col_approval','Approval');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_col_approval')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_col_approval','Godkännande');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_col_approval')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_col_approval','Genehmigung');
GO

-- budget_col_note
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_col_note')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_col_note','Note');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_col_note')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_col_note',N'Notă');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_col_note')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_col_note','Notes');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_col_note')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_col_note','Anteckning');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_col_note')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_col_note','Notiz');
GO

-- budget_name
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_name')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_name','Budget:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_name')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_name',N'Buget:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_name')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_name','Budget:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_name')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_name','Budget:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_name')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_name','Budget:');
GO

-- budget_confirm_delete
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_confirm_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_confirm_delete','Eliminare questo budget?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_confirm_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_confirm_delete',N'Ștergeți acest buget?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_confirm_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_confirm_delete','Delete this budget?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_confirm_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_confirm_delete','Ta bort denna budget?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_confirm_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_confirm_delete','Dieses Budget löschen?');
GO

-- budget_confirm_delete_item
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_confirm_delete_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_confirm_delete_item','Eliminare questa riga?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_confirm_delete_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_confirm_delete_item',N'Ștergeți acest rând?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_confirm_delete_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_confirm_delete_item','Delete this row?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_confirm_delete_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_confirm_delete_item','Ta bort denna rad?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_confirm_delete_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_confirm_delete_item','Diese Zeile löschen?');
GO

-- budget_select_first
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_select_first')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_select_first','Selezionare un budget.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_select_first')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_select_first',N'Selectați un buget.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_select_first')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_select_first','Please select a budget.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_select_first')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_select_first','Välj en budget.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_select_first')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_select_first','Bitte wählen Sie ein Budget.');
GO

-- budget_select_item
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_select_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_select_item','Selezionare una riga.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_select_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_select_item',N'Selectați un rând.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_select_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_select_item','Please select a row.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_select_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_select_item','Välj en rad.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_select_item')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_select_item','Bitte wählen Sie eine Zeile.');
GO

-- budget_desc_required
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_desc_required')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_desc_required','La descrizione è obbligatoria.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_desc_required')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_desc_required',N'Descrierea este obligatorie.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_desc_required')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_desc_required','Description is required.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_desc_required')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_desc_required','Beskrivningen är obligatorisk.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_desc_required')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_desc_required','Beschreibung ist erforderlich.');
GO

-- budget_qty_invalid
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_qty_invalid')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_qty_invalid','Quantità non valida.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_qty_invalid')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_qty_invalid',N'Cantitate invalidă.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_qty_invalid')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_qty_invalid','Invalid quantity.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_qty_invalid')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_qty_invalid','Ogiltigt antal.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_qty_invalid')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_qty_invalid','Ungültige Menge.');
GO

-- budget_price_invalid
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_price_invalid')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_price_invalid','Prezzo non valido.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_price_invalid')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_price_invalid',N'Preț invalid.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_price_invalid')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_price_invalid','Invalid price.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_price_invalid')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_price_invalid','Ogiltigt pris.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_price_invalid')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_price_invalid','Ungültiger Preis.');
GO

-- budget_import_title
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_import_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_import_title','Seleziona file Excel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_import_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_import_title',N'Selectați fișierul Excel');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_import_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_import_title','Select Excel file');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_import_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_import_title','Välj Excel-fil');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_import_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_import_title','Excel-Datei auswählen');
GO

-- budget_load_project_first (from project_window.py)
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_load_project_first')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_load_project_first','Carica prima i dati del progetto.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_load_project_first')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_load_project_first',N'Încărcați mai întâi datele proiectului.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_load_project_first')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_load_project_first','Please load the project data first.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_load_project_first')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_load_project_first','Ladda projektdata först.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_load_project_first')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_load_project_first','Bitte laden Sie zuerst die Projektdaten.');
GO

-- budget_cat_detail (from config_window BudgetCategoriesFrame)
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_cat_detail')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_cat_detail','Dettaglio Categoria');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_cat_detail')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_cat_detail',N'Detaliu Categorie');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_cat_detail')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_cat_detail','Category Detail');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_cat_detail')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_cat_detail','Kategoridetalj');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_cat_detail')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_cat_detail','Kategoriedetail');
GO

-- budget_cat_show_deleted
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_cat_show_deleted')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_cat_show_deleted','Mostra eliminate');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_cat_show_deleted')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_cat_show_deleted',N'Afișează șterse');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_cat_show_deleted')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_cat_show_deleted','Show deleted');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_cat_show_deleted')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_cat_show_deleted','Visa borttagna');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_cat_show_deleted')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_cat_show_deleted','Gelöschte anzeigen');
GO

-- budget_cat_name_required
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_cat_name_required')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_cat_name_required','Il nome categoria è obbligatorio.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_cat_name_required')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_cat_name_required',N'Numele categoriei este obligatoriu.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_cat_name_required')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_cat_name_required','Category name is required.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_cat_name_required')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_cat_name_required','Kategorinamn krävs.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_cat_name_required')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_cat_name_required','Kategoriename ist erforderlich.');
GO

-- budget_cat_confirm_delete
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_cat_confirm_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_cat_confirm_delete','Eliminare questa categoria?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_cat_confirm_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_cat_confirm_delete',N'Ștergeți această categorie?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_cat_confirm_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_cat_confirm_delete','Delete this category?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_cat_confirm_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_cat_confirm_delete','Ta bort denna kategori?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_cat_confirm_delete')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_cat_confirm_delete','Diese Kategorie löschen?');
GO

PRINT '✅ Traduzioni Budget NPI completate'
GO
