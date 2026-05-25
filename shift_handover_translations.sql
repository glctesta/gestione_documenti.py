-- ============================================================
-- shift_handover_translations.sql
-- Traduzioni per il modulo Cambio Turno
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- 5 lingue: it / en / ro / de / sv
-- ============================================================

USE [Traceability_RS];
GO

DECLARE @keys TABLE (k NVARCHAR(100), it NVARCHAR(500), en NVARCHAR(500), ro NVARCHAR(500), de NVARCHAR(500), sv NVARCHAR(500));
INSERT INTO @keys VALUES
 ('cambio_turni',             N'Cambio Turno',                   N'Shift Handover',               N'Predare Schimb',               N'Schichtwechsel',               N'Skiftbyte'),
 ('shift_handover_title',     N'Cambio Turno — Predare Schimb',  N'Shift Handover',               N'Predare Schimb',               N'Schichtübergabe',              N'Skiftöverlämning'),
 ('sh_tab_compile',           N'Compila Consegna',               N'Fill Handover',                N'Completeaza Predarea',         N'Übergabe ausfüllen',           N'Fyll i överlämning'),
 ('sh_tab_history',           N'Storico / Conferma',             N'History / Confirm',            N'Istoric / Confirmare',         N'Verlauf / Bestätigung',        N'Historik / Bekräfta'),
 ('sh_header',                N'Intestazione turno',             N'Shift header',                 N'Antet schimb',                 N'Schicht-Kopfzeile',            N'Skift rubrik'),
 ('sh_date',                  N'Data:',                          N'Date:',                        N'Data:',                        N'Datum:',                       N'Datum:'),
 ('sh_shift',                 N'Turno:',                         N'Shift:',                       N'Schimb:',                      N'Schicht:',                     N'Skift:'),
 ('sh_dept',                  N'Reparto:',                       N'Department:',                  N'Sectie:',                      N'Abteilung:',                   N'Avdelning:'),
 ('sh_compiled_by',           N'Compilato da:',                  N'Compiled by:',                 N'Completat de:',                N'Ausgefüllt von:',              N'Ifyllt av:'),
 ('sh_field_prod_status',     N'Stare producție',               N'Production status',            N'Stare productie',              N'Produktionsstatus',            N'Produktionsstatus'),
 ('sh_field_lines',           N'Linii / echipamente',           N'Lines / equipment',            N'Linii / echipamente',          N'Linien / Ausrüstung',         N'Linjer / utrustning'),
 ('sh_field_qty',             N'Cantități',                     N'Quantities',                   N'Cantitati',                    N'Mengen',                       N'Kvantiteter'),
 ('sh_qty_plan',              N'Planificat:',                   N'Planned:',                     N'Planificat:',                  N'Geplant:',                     N'Planerat:'),
 ('sh_qty_prod',              N'Realizat:',                     N'Produced:',                    N'Realizat:',                    N'Produziert:',                  N'Producerat:'),
 ('sh_field_quality',         N'Calitate — Probleme + Acțiuni', N'Quality — Issues + Actions',   N'Calitate — Probleme + Actiuni',N'Qualität — Probleme + Aktionen',N'Kvalitet — Problem + Åtgärder'),
 ('sh_field_materials',       N'Materiale (disponibile/lipsă)', N'Materials (available/missing)',N'Materiale (disponibile/lipsa)',N'Materialien (verfügbar/fehlend)',N'Material (tillgängligt/saknas)'),
 ('sh_field_open',            N'Probleme deschise',             N'Open issues',                  N'Probleme deschise',            N'Offene Probleme',              N'Öppna ärenden'),
 ('sh_field_notes',           N'Note libere',                   N'Free notes',                   N'Note libere',                  N'Freie Notizen',                N'Fritext'),
 ('sh_btn_save',              N'Salva Consegna Turno',          N'Save Shift Handover',          N'Salveaza Predarea',            N'Übergabe speichern',           N'Spara skiftöverlämning'),
 ('sh_filter_date',           N'Data:',                         N'Date:',                        N'Data:',                        N'Datum:',                       N'Datum:'),
 ('sh_filter_dept',           N'Reparto:',                      N'Department:',                  N'Sectie:',                      N'Abteilung:',                   N'Avdelning:'),
 ('sh_detail',                N'Dettaglio consegna selezionata',N'Selected handover detail',     N'Detaliu predare selectata',    N'Ausgewählte Übergabe Details', N'Vald överlämning detalj'),
 ('sh_btn_confirm',           N'Ho letto e preso nota',         N'I have read and acknowledged', N'Am citit si luat la cunostinta',N'Gelesen und zur Kenntnis genommen',N'Läst och bekräftat'),
 ('sh_confirm_title',         N'Conferma Lettura',              N'Reading Confirmation',         N'Confirmare citire',            N'Lesebestätigung',              N'Läsbekräftelse'),
 ('sh_confirm_notes',         N'Note aggiuntive (facoltativo):', N'Additional notes (optional):',N'Note suplimentare (optional):',N'Zusätzliche Hinweise (optional):',N'Extra anteckningar (valfritt):'),
 ('sh_btn_confirm_ok',        N'Confermo',                      N'Confirm',                      N'Confirmar',                    N'Bestätigen',                   N'Bekräfta'),
 ('sh_saved_ok',              N'Consegna turno salvata.',       N'Shift handover saved.',        N'Predarea schimbului salvata.',  N'Schichtübergabe gespeichert.', N'Skiftöverlämning sparad.'),
 ('sh_saved_err',             N'Errore durante il salvataggio.',N'Error saving.',                N'Eroare la salvare.',            N'Fehler beim Speichern.',       N'Fel vid sparning.'),
 ('sh_confirmed_ok',          N'Conferma registrata.',          N'Confirmation recorded.',       N'Confirmare inregistrata.',     N'Bestätigung gespeichert.',     N'Bekräftelse registrerad.'),
 ('sh_err_dept',              N'Selezionare un reparto.',       N'Please select a department.',  N'Selectati o sectie.',          N'Bitte Abteilung auswählen.',   N'Välj en avdelning.');

-- Inserimento con IF NOT EXISTS
DECLARE @k NVARCHAR(100), @it NVARCHAR(500), @en NVARCHAR(500),
        @ro NVARCHAR(500), @de NVARCHAR(500), @sv NVARCHAR(500);

DECLARE cur CURSOR FOR SELECT k,it,en,ro,de,sv FROM @keys;
OPEN cur;
FETCH NEXT FROM cur INTO @k, @it, @en, @ro, @de, @sv;
WHILE @@FETCH_STATUS = 0
BEGIN
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE TranslationKey=@k AND LanguageCode='it')
        INSERT INTO dbo.AppTranslations (LanguageCode,TranslationKey,TranslationValue) VALUES ('it',@k,@it);
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE TranslationKey=@k AND LanguageCode='en')
        INSERT INTO dbo.AppTranslations (LanguageCode,TranslationKey,TranslationValue) VALUES ('en',@k,@en);
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE TranslationKey=@k AND LanguageCode='ro')
        INSERT INTO dbo.AppTranslations (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro',@k,@ro);
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE TranslationKey=@k AND LanguageCode='de')
        INSERT INTO dbo.AppTranslations (LanguageCode,TranslationKey,TranslationValue) VALUES ('de',@k,@de);
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE TranslationKey=@k AND LanguageCode='sv')
        INSERT INTO dbo.AppTranslations (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv',@k,@sv);
    FETCH NEXT FROM cur INTO @k, @it, @en, @ro, @de, @sv;
END
CLOSE cur; DEALLOCATE cur;

PRINT 'Traduzioni Cambio Turno inserite con successo.';
GO

-- ============================================================
-- SCT WorkStation config + Report keys
-- ============================================================

USE [Traceability_RS];
GO

DECLARE @keys2 TABLE (k NVARCHAR(100), it NVARCHAR(500), en NVARCHAR(500), ro NVARCHAR(500), de NVARCHAR(500), sv NVARCHAR(500));
INSERT INTO @keys2 VALUES
 -- Voce di menu
 ('sct_config_menu',            N'⚙️ Configura SCT WorkStation',          N'⚙️ Configure SCT WorkStation',        N'⚙️ Configurare SCT WorkStation',       N'⚙️ SCT WorkStation konfigurieren',     N'⚙️ Konfigurera SCT WorkStation'),
 -- Titolo finestra
 ('sct_config_title',           N'Configurazione SCT WorkStation',        N'SCT WorkStation Setup',               N'Configurare SCT WorkStation',          N'SCT WorkStation Einrichtung',          N'SCT WorkStation-konfiguration'),
 -- Header
 ('sct_config_header',          N'Configurazione SCT WorkStation',        N'SCT WorkStation Configuration',       N'Configurare SCT WorkStation',          N'SCT WorkStation Konfiguration',        N'SCT WorkStation Konfiguration'),
 -- Descrizione
 ('sct_config_desc',            N'Identifica questo PC come postazione Capo Turno (SCT Host).'
                                 + char(10) + N'I popup di fine turno appariranno solo su questo PC.',
                                N'Identifies this PC as a Shift Leader workstation (SCT Host).'
                                 + char(10) + N'End-of-shift popups will appear only on this PC.',
                                N'Identifica acest PC ca statie Sef de Schimb (SCT Host).'
                                 + char(10) + N'Popup-urile de sfarsit de schimb vor aparea doar pe acest PC.',
                                N'Kennzeichnet diesen PC als Schichtleiter-Arbeitsstation (SCT Host).'
                                 + char(10) + N'Schichtenende-Popups erscheinen nur auf diesem PC.',
                                N'Identifierar denna PC som skiftledare-arbetsstation (SCT Host).'
                                 + char(10) + N'Skiftslutspopupar visas bara på denna PC.'),
 -- Sezione parametri
 ('sct_config_params',          N'Parametri workstation',                 N'Workstation parameters',              N'Parametri statie',                     N'Arbeitsstation-Parameter',             N'Arbetsparametrar'),
 -- Pulsanti
 ('sct_config_activate',        N'Attiva SCT WorkStation',                N'Activate SCT WorkStation',            N'Activeaza SCT WorkStation',            N'SCT WorkStation aktivieren',           N'Aktivera SCT WorkStation'),
 ('sct_config_deactivate',      N'Disattiva SCT WorkStation',             N'Deactivate SCT WorkStation',          N'Dezactiveaza SCT WorkStation',         N'SCT WorkStation deaktivieren',         N'Inaktivera SCT WorkStation'),
 -- Stato
 ('sct_config_inactive',        N'❌  SCT WorkStation INATTIVA',          N'❌  SCT WorkStation INACTIVE',         N'❌  SCT WorkStation INACTIVA',          N'❌  SCT WorkStation INAKTIV',           N'❌  SCT WorkStation INAKTIV'),
 -- Messaggi attivazione/disattivazione
 ('sct_config_created',         N'SCT WorkStation attivata con successo.',N'SCT WorkStation activated successfully.',N'SCT WorkStation activata cu succes.',N'SCT WorkStation erfolgreich aktiviert.',N'SCT WorkStation aktiverad.'),
 ('sct_config_deleted',         N'SCT WorkStation disattivata con successo.',N'SCT WorkStation deactivated successfully.',N'SCT WorkStation dezactivata cu succes.',N'SCT WorkStation erfolgreich deaktiviert.',N'SCT WorkStation inaktiverad.'),
 -- Conferma eliminazione
 ('sct_config_confirm_delete',  N'Disattivare la SCT WorkStation?'
                                 + char(10) + N'I popup di fine turno non appariranno più su questo PC.',
                                N'Deactivate the SCT WorkStation?'
                                 + char(10) + N'End-of-shift popups will no longer appear on this PC.',
                                N'Dezactivati SCT WorkStation?'
                                 + char(10) + N'Popup-urile de sfarsit de schimb nu vor mai aparea pe acest PC.',
                                N'SCT WorkStation deaktivieren?'
                                 + char(10) + N'Schichtenende-Popups erscheinen nicht mehr auf diesem PC.',
                                N'Inaktivera SCT WorkStation?'
                                 + char(10) + N'Skiftslutspopupar visas inte längre på denna PC.'),
 -- Validazioni
 ('sct_config_err_dept',        N'Selezionare un reparto.',               N'Please select a department.',         N'Selectati o sectie.',                  N'Bitte eine Abteilung auswählen.',      N'Välj en avdelning.'),
 ('sct_config_err_shifts',      N'Selezionare almeno un turno.',          N'Please select at least one shift.',   N'Selectati cel putin un schimb.',        N'Bitte mindestens eine Schicht auswählen.',N'Välj minst ett skift.'),
 -- Voci menu Report Cambio Turno
 ('sh_report_menu',             N'📊 Report Cambio Turno',                N'📊 Shift Handover Report',            N'📊 Raport Predare Schimb',              N'📊 Schichtübergabe-Bericht',           N'📊 Skiftöverlämningsrapport'),
 ('sh_report_title',            N'Report Cambio Turno',                   N'Shift Handover Report',               N'Raport Predare Schimb',                N'Schichtübergabe-Bericht',              N'Skiftöverlämningsrapport'),
 ('sh_rep_filters',             N'Filtri',                                N'Filters',                             N'Filtre',                               N'Filter',                               N'Filter'),
 ('sh_rep_from',                N'Dal:',                                  N'From:',                               N'De la:',                               N'Von:',                                 N'Från:'),
 ('sh_rep_to',                  N'Al:',                                   N'To:',                                 N'Pana la:',                             N'Bis:',                                 N'Till:'),
 ('sh_rep_btn_excel',           N'📥 Export Excel',                       N'📥 Export Excel',                     N'📥 Export Excel',                       N'📥 Excel exportieren',                 N'📥 Exportera Excel'),
 ('sh_rep_no_data',             N'Nessun dato da esportare.',             N'No data to export.',                  N'Nu exista date de exportat.',          N'Keine Daten zum Exportieren.',         N'Inga data att exportera.'),
 ('sh_rep_open_file',           N'File salvato. Aprire il file?',         N'File saved. Open the file?',          N'Fisier salvat. Deschideti fisierul?',  N'Datei gespeichert. Datei öffnen?',     N'Fil sparat. Öppna filen?');

-- Inserimento con IF NOT EXISTS
DECLARE @k2 NVARCHAR(100), @it2 NVARCHAR(500), @en2 NVARCHAR(500),
        @ro2 NVARCHAR(500), @de2 NVARCHAR(500), @sv2 NVARCHAR(500);

DECLARE cur2 CURSOR FOR SELECT k,it,en,ro,de,sv FROM @keys2;
OPEN cur2;
FETCH NEXT FROM cur2 INTO @k2, @it2, @en2, @ro2, @de2, @sv2;
WHILE @@FETCH_STATUS = 0
BEGIN
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE TranslationKey=@k2 AND LanguageCode='it')
        INSERT INTO dbo.AppTranslations (LanguageCode,TranslationKey,TranslationValue) VALUES ('it',@k2,@it2);
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE TranslationKey=@k2 AND LanguageCode='en')
        INSERT INTO dbo.AppTranslations (LanguageCode,TranslationKey,TranslationValue) VALUES ('en',@k2,@en2);
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE TranslationKey=@k2 AND LanguageCode='ro')
        INSERT INTO dbo.AppTranslations (LanguageCode,TranslationKey,TranslationValue) VALUES ('ro',@k2,@ro2);
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE TranslationKey=@k2 AND LanguageCode='de')
        INSERT INTO dbo.AppTranslations (LanguageCode,TranslationKey,TranslationValue) VALUES ('de',@k2,@de2);
    IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE TranslationKey=@k2 AND LanguageCode='sv')
        INSERT INTO dbo.AppTranslations (LanguageCode,TranslationKey,TranslationValue) VALUES ('sv',@k2,@sv2);
    FETCH NEXT FROM cur2 INTO @k2, @it2, @en2, @ro2, @de2, @sv2;
END
CLOSE cur2; DEALLOCATE cur2;

PRINT 'Traduzioni SCT WorkStation config e Report inserite con successo.';
GO
