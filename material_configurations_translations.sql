-- ============================================================
-- Traduzioni per Material Configurations e Request Rules
-- Lingue: IT, RO (con N''), EN, SV, DE
-- ============================================================
USE Traceability_RS
GO

-- ==========================
-- Menu item
-- ==========================
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='submenu_material_configurations')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','submenu_material_configurations','Configurazione Codici');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='submenu_material_configurations')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','submenu_material_configurations',N'Configurare Coduri');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='submenu_material_configurations')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','submenu_material_configurations','Code Configuration');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='submenu_material_configurations')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','submenu_material_configurations','Kodkonfiguration');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='submenu_material_configurations')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','submenu_material_configurations','Code-Konfiguration');

-- ==========================
-- Material Configurations Window
-- ==========================

-- mat_config_title
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_title')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_title','Configurazione Codici Materiale');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_title')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_title',N'Configurare Coduri Material');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_title')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_title','Material Code Configuration');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_title')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_title','Materialkodskonfiguration');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_title')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_title','Materialcode-Konfiguration');

-- mat_config_header
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_header')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_header','Configurazione Codici Materiale');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_header')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_header',N'Configurare Coduri Material');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_header')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_header','Material Code Configuration');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_header')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_header','Materialkodskonfiguration');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_header')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_header','Materialcode-Konfiguration');

-- mat_config_filters
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_filters')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_filters','Filtri');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_filters')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_filters',N'Filtre');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_filters')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_filters','Filters');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_filters')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_filters','Filter');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_filters')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_filters','Filter');

-- mat_config_filter_code
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_filter_code')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_filter_code','Codice:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_filter_code')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_filter_code',N'Cod:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_filter_code')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_filter_code','Code:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_filter_code')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_filter_code','Kod:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_filter_code')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_filter_code','Code:');

-- mat_config_filter_desc
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_filter_desc')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_filter_desc','Descrizione:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_filter_desc')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_filter_desc',N'Descriere:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_filter_desc')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_filter_desc','Description:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_filter_desc')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_filter_desc','Beskrivning:');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_filter_desc')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_filter_desc','Beschreibung:');

-- mat_config_show_configured
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_show_configured')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_show_configured','Solo configurati');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_show_configured')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_show_configured',N'Doar configurate');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_show_configured')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_show_configured','Configured only');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_show_configured')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_show_configured','Endast konfigurerade');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_show_configured')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_show_configured','Nur konfigurierte');

-- mat_config_col_code
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_col_code')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_col_code','Codice');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_col_code')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_col_code',N'Cod');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_col_code')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_col_code','Code');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_col_code')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_col_code','Kod');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_col_code')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_col_code','Code');

-- mat_config_col_desc
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_col_desc')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_col_desc','Descrizione');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_col_desc')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_col_desc',N'Descriere');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_col_desc')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_col_desc','Description');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_col_desc')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_col_desc','Beskrivning');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_col_desc')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_col_desc','Beschreibung');

-- mat_config_col_fract
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_col_fract')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_col_fract','Frazionabile');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_col_fract')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_col_fract',N'Fracționabil');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_col_fract')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_col_fract','Fractionable');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_col_fract')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_col_fract','Delbar');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_col_fract')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_col_fract','Teilbar');

-- mat_config_col_qty
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_col_qty')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_col_qty',N'Qtà Standard');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_col_qty')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_col_qty',N'Cantitate Standard');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_col_qty')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_col_qty','Standard Qty');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_col_qty')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_col_qty','Standardkvantitet');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_col_qty')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_col_qty','Standardmenge');

-- mat_config_col_status
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_col_status')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_col_status','Stato');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_col_status')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_col_status',N'Stare');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_col_status')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_col_status','Status');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_col_status')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_col_status','Status');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_col_status')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_col_status','Status');

-- mat_config_detail
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_detail')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_detail','Dettaglio Configurazione');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_detail')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_detail',N'Detalii Configurare');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_detail')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_detail','Configuration Detail');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_detail')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_detail','Konfigurationsdetaljer');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_detail')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_detail','Konfigurationsdetails');

-- mat_config_btn_save
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_btn_save')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_btn_save',N'💾 Salva Configurazione');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_btn_save')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_btn_save',N'💾 Salvează Configurare');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_btn_save')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_btn_save',N'💾 Save Configuration');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_btn_save')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_btn_save',N'💾 Spara konfiguration');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_btn_save')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_btn_save',N'💾 Konfiguration speichern');

-- mat_config_btn_delete
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_btn_delete')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_btn_delete',N'🗑️ Disattiva');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_btn_delete')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_btn_delete',N'🗑️ Dezactivează');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_btn_delete')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_btn_delete',N'🗑️ Deactivate');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_btn_delete')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_btn_delete',N'🗑️ Inaktivera');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_btn_delete')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_btn_delete',N'🗑️ Deaktivieren');

-- mat_config_btn_restore
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_btn_restore')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_btn_restore',N'♻️ Riattiva');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_btn_restore')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_btn_restore',N'♻️ Reactivează');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_btn_restore')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_btn_restore',N'♻️ Restore');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_btn_restore')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_btn_restore',N'♻️ Återställ');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_btn_restore')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_btn_restore',N'♻️ Wiederherstellen');

-- mat_config_status_active
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_status_active')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_status_active','Attivo');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_status_active')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_status_active',N'Activ');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_status_active')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_status_active','Active');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_status_active')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_status_active','Aktiv');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_status_active')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_status_active','Aktiv');

-- mat_config_status_none
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_status_none')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_status_none','Non config.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_status_none')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_status_none',N'Neconfigurat');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_status_none')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_status_none','Not configured');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_status_none')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_status_none','Ej konfigurerad');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_status_none')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_status_none','Nicht konfiguriert');

-- mat_config_count
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_count')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_count','Visualizzati: {count} materiali');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_count')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_count',N'Afișate: {count} materiale');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_count')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_count','Showing: {count} materials');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_count')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_count','Visar: {count} material');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_count')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_count','Angezeigt: {count} Materialien');

-- mat_config_select_material
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_select_material')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_select_material','Selezionare un materiale dalla lista.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_select_material')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_select_material',N'Selectați un material din listă.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_select_material')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_select_material','Select a material from the list.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_select_material')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_select_material',N'Välj ett material från listan.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_select_material')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_select_material',N'Wählen Sie ein Material aus der Liste.');

-- mat_config_invalid_qty
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_invalid_qty')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_invalid_qty',N'Inserire una quantità standard valida (numero positivo).');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_invalid_qty')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_invalid_qty',N'Introduceți o cantitate standard validă (număr pozitiv).');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_invalid_qty')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_invalid_qty','Enter a valid standard quantity (positive number).');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_invalid_qty')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_invalid_qty',N'Ange en giltig standardkvantitet (positivt tal).');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_invalid_qty')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_invalid_qty',N'Geben Sie eine gültige Standardmenge ein (positive Zahl).');

-- mat_config_no_config
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_no_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_no_config','Nessuna configurazione attiva da disattivare per questo materiale.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_no_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_no_config',N'Nicio configurare activă de dezactivat pentru acest material.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_no_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_no_config','No active configuration to deactivate for this material.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_no_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_no_config','Ingen aktiv konfiguration att inaktivera.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_no_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_no_config','Keine aktive Konfiguration zum Deaktivieren.');

-- mat_config_confirm_delete
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_confirm_delete')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_confirm_delete','Disattivare la configurazione per questo materiale?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_confirm_delete')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_confirm_delete',N'Dezactivați configurarea pentru acest material?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_confirm_delete')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_confirm_delete','Deactivate configuration for this material?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_confirm_delete')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_confirm_delete','Inaktivera konfigurationen?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_confirm_delete')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_confirm_delete','Konfiguration deaktivieren?');

-- mat_config_no_inactive
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='mat_config_no_inactive')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','mat_config_no_inactive','Nessuna configurazione disattivata trovata per questo materiale.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='mat_config_no_inactive')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','mat_config_no_inactive',N'Nicio configurare dezactivată găsită pentru acest material.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='mat_config_no_inactive')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','mat_config_no_inactive','No deactivated configuration found for this material.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='mat_config_no_inactive')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','mat_config_no_inactive','Ingen inaktiverad konfiguration hittades.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='mat_config_no_inactive')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','mat_config_no_inactive','Keine deaktivierte Konfiguration gefunden.');

-- ==========================
-- Request Form Rules (new keys)
-- ==========================

-- ind_req_fraz_rule_config
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='ind_req_fraz_rule_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','ind_req_fraz_rule_config',N'Quantità editabile, massimo {0}. Deve essere multiplo di {0}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='ind_req_fraz_rule_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','ind_req_fraz_rule_config',N'Cantitate editabilă, maxim {0}. Trebuie să fie multiplu de {0}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='ind_req_fraz_rule_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','ind_req_fraz_rule_config','Editable quantity, max {0}. Must be a multiple of {0}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='ind_req_fraz_rule_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','ind_req_fraz_rule_config',N'Redigerbar kvantitet, max {0}. Måste vara en multipel av {0}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='ind_req_fraz_rule_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','ind_req_fraz_rule_config','Bearbeitbare Menge, max. {0}. Muss ein Vielfaches von {0} sein.');

-- ind_req_nonfraz_rule_config
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='ind_req_nonfraz_rule_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','ind_req_nonfraz_rule_config',N'Quantità fissa: {0} (confezione intera, non frazionabile)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='ind_req_nonfraz_rule_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','ind_req_nonfraz_rule_config',N'Cantitate fixă: {0} (pachet întreg, nefracționabil)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='ind_req_nonfraz_rule_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','ind_req_nonfraz_rule_config','Fixed quantity: {0} (whole package, not fractionable)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='ind_req_nonfraz_rule_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','ind_req_nonfraz_rule_config',N'Fast kvantitet: {0} (hel förpackning, ej delbar)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='ind_req_nonfraz_rule_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','ind_req_nonfraz_rule_config','Feste Menge: {0} (ganze Verpackung, nicht teilbar)');

-- ind_req_nonfraz_error_config
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='ind_req_nonfraz_error_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','ind_req_nonfraz_error_config',N'Materiale non frazionabile. La quantità deve essere esattamente {0}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='ind_req_nonfraz_error_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','ind_req_nonfraz_error_config',N'Material nefracționabil. Cantitatea trebuie să fie exact {0}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='ind_req_nonfraz_error_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','ind_req_nonfraz_error_config','Non-fractionable material. Quantity must be exactly {0}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='ind_req_nonfraz_error_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','ind_req_nonfraz_error_config',N'Ej delbart material. Kvantiteten måste vara exakt {0}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='ind_req_nonfraz_error_config')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','ind_req_nonfraz_error_config','Nicht teilbares Material. Die Menge muss genau {0} betragen.');

-- ind_req_fraz_max_error
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='ind_req_fraz_max_error')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','ind_req_fraz_max_error',N'La quantità {0} supera il massimo consentito ({1}).');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='ind_req_fraz_max_error')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','ind_req_fraz_max_error',N'Cantitatea {0} depășește maximul permis ({1}).');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='ind_req_fraz_max_error')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','ind_req_fraz_max_error','Quantity {0} exceeds maximum allowed ({1}).');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='ind_req_fraz_max_error')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','ind_req_fraz_max_error',N'Kvantiteten {0} överskrider tillåtet maximum ({1}).');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='ind_req_fraz_max_error')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','ind_req_fraz_max_error',N'Menge {0} überschreitet das erlaubte Maximum ({1}).');

-- ind_req_fraz_multiple_error
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='ind_req_fraz_multiple_error')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','ind_req_fraz_multiple_error',N'La quantità {0} deve essere un multiplo di {1}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='ind_req_fraz_multiple_error')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','ind_req_fraz_multiple_error',N'Cantitatea {0} trebuie să fie un multiplu de {1}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='ind_req_fraz_multiple_error')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','ind_req_fraz_multiple_error','Quantity {0} must be a multiple of {1}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='ind_req_fraz_multiple_error')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','ind_req_fraz_multiple_error',N'Kvantiteten {0} måste vara en multipel av {1}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='ind_req_fraz_multiple_error')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','ind_req_fraz_multiple_error','Menge {0} muss ein Vielfaches von {1} sein.');

-- ind_req_stock_insufficient
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='ind_req_stock_insufficient')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','ind_req_stock_insufficient','Stock insufficiente. Disponibile: {0}, richiesto: {1}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='ind_req_stock_insufficient')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','ind_req_stock_insufficient',N'Stoc insuficient. Disponibil: {0}, solicitat: {1}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='ind_req_stock_insufficient')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','ind_req_stock_insufficient','Insufficient stock. Available: {0}, requested: {1}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='ind_req_stock_insufficient')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','ind_req_stock_insufficient',N'Otillräckligt lager. Tillgängligt: {0}, begärt: {1}.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='ind_req_stock_insufficient')
  INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','ind_req_stock_insufficient',N'Unzureichender Bestand. Verfügbar: {0}, angefordert: {1}.');

PRINT '✅ Traduzioni Material Configurations inserite con successo.'
GO
