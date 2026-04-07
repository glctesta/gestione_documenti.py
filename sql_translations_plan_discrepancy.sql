-- ============================================================
-- Traduzioni per Piano Produzione — Giustificazione Discrepanze
-- Eseguire su database Traceability_RS
-- ============================================================

USE [Traceability_RS]
GO

-- ================================================================
-- MENU
-- ================================================================

-- piano_produzione (menu label)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'piano_produzione' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'piano_produzione', N'Piano produzione')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'piano_produzione' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'piano_produzione', N'Production Plan')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'piano_produzione' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'piano_produzione', N'Plan producție')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'piano_produzione' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'piano_produzione', N'Produktionsplan')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'piano_produzione' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'piano_produzione', N'Produktionsplan')

-- giustifica_discrepanze_piano (chiave autorizzazione)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'giustifica_discrepanze_piano' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'giustifica_discrepanze_piano', N'Giustifica discrepanze piano')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'giustifica_discrepanze_piano' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'giustifica_discrepanze_piano', N'Justify plan discrepancies')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'giustifica_discrepanze_piano' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'giustifica_discrepanze_piano', N'Justificarea discrepanțelor din plan')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'giustifica_discrepanze_piano' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'giustifica_discrepanze_piano', N'Planabweichungen begründen')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'giustifica_discrepanze_piano' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'giustifica_discrepanze_piano', N'Motivera planavvikelser')

-- ================================================================
-- HEADER
-- ================================================================

-- logged_user
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'logged_user' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'logged_user', N'Operatore')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'logged_user' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'logged_user', N'Operator')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'logged_user' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'logged_user', N'Operator')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'logged_user' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'logged_user', N'Bediener')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'logged_user' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'logged_user', N'Operatör')

-- time_remaining
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'time_remaining' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'time_remaining', N'Tempo rimanente:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'time_remaining' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'time_remaining', N'Time remaining:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'time_remaining' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'time_remaining', N'Timp rămas:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'time_remaining' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'time_remaining', N'Verbleibende Zeit:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'time_remaining' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'time_remaining', N'Återstående tid:')

-- ================================================================
-- TOOLBAR BUTTONS
-- ================================================================

-- btn_refresh
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_refresh' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'btn_refresh', N'🔄 Aggiorna')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_refresh' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'btn_refresh', N'🔄 Refresh')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_refresh' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'btn_refresh', N'🔄 Actualizare')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_refresh' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'btn_refresh', N'🔄 Aktualisieren')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_refresh' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'btn_refresh', N'🔄 Uppdatera')

-- btn_select_all
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_select_all' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'btn_select_all', N'☑ Seleziona tutto')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_select_all' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'btn_select_all', N'☑ Select all')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_select_all' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'btn_select_all', N'☑ Selectează tot')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_select_all' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'btn_select_all', N'☑ Alle auswählen')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_select_all' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'btn_select_all', N'☑ Markera alla')

-- btn_deselect_all
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_deselect_all' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'btn_deselect_all', N'☐ Deseleziona tutto')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_deselect_all' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'btn_deselect_all', N'☐ Deselect all')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_deselect_all' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'btn_deselect_all', N'☐ Deselectează tot')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_deselect_all' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'btn_deselect_all', N'☐ Alle abwählen')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_deselect_all' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'btn_deselect_all', N'☐ Avmarkera alla')

-- ================================================================
-- JUSTIFY PANEL
-- ================================================================

-- justify_panel
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_panel' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'justify_panel', N'📝 Giustificazione discrepanze')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_panel' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'justify_panel', N'📝 Justify discrepancies')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_panel' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'justify_panel', N'📝 Justificarea discrepanțelor')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_panel' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'justify_panel', N'📝 Abweichungen begründen')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_panel' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'justify_panel', N'📝 Motivera avvikelser')

-- reason_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'reason_label' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'reason_label', N'Motivazione:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'reason_label' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'reason_label', N'Reason:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'reason_label' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'reason_label', N'Motivație:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'reason_label' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'reason_label', N'Begründung:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'reason_label' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'reason_label', N'Anledning:')

-- notes_label
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'notes_label' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'notes_label', N'Note:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'notes_label' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'notes_label', N'Notes:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'notes_label' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'notes_label', N'Note:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'notes_label' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'notes_label', N'Anmerkungen:')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'notes_label' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'notes_label', N'Anteckningar:')

-- btn_save_justify
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_justify' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'btn_save_justify', N'✅ Salva giustificazione')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_justify' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'btn_save_justify', N'✅ Save justification')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_justify' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'btn_save_justify', N'✅ Salvează justificarea')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_justify' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'btn_save_justify', N'✅ Begründung speichern')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_justify' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'btn_save_justify', N'✅ Spara motivering')

-- btn_close
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_close' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'btn_close', N'Chiudi')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_close' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'btn_close', N'Close')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_close' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'btn_close', N'Închide')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_close' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'btn_close', N'Schließen')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_close' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'btn_close', N'Stäng')

-- ================================================================
-- MESSAGES / DIALOGS
-- ================================================================

-- select_rows
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_rows' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'select_rows', N'Selezionare almeno un allarme dalla lista.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_rows' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'select_rows', N'Please select at least one alert from the list.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_rows' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'select_rows', N'Selectați cel puțin o alertă din listă.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_rows' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'select_rows', N'Bitte mindestens einen Alarm aus der Liste auswählen.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_rows' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'select_rows', N'Välj minst en avisering från listan.')

-- select_reason
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_reason' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'select_reason', N'Selezionare una motivazione.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_reason' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'select_reason', N'Please select a reason.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_reason' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'select_reason', N'Selectați o motivație.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_reason' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'select_reason', N'Bitte eine Begründung auswählen.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_reason' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'select_reason', N'Välj en anledning.')

GO

-- ================================================================
-- MASTER-DETAIL: NUOVE CHIAVI
-- ================================================================

-- justify_group (pannello giustificazione a livello di ordine)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_group' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'justify_group', N'📝 Giustificazione a livello di ordine (applicata a tutte le allerte)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_group' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'justify_group', N'📝 Order-level justification (applies to all alerts)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_group' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'justify_group', N'📝 Justificare la nivel de comandă (se aplică tuturor alertelor)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_group' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'justify_group', N'📝 Begründung auf Auftragsebene (gilt für alle Alarme)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_group' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'justify_group', N'📝 Motivering på ordernivå (gäller alla aviseringar)')

-- btn_save_group
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_group' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'btn_save_group', N'✅ Salva per ordine selezionato')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_group' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'btn_save_group', N'✅ Save for selected order')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_group' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'btn_save_group', N'✅ Salvează pt. comanda selectată')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_group' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'btn_save_group', N'✅ Für ausgewählten Auftrag speichern')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_group' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'btn_save_group', N'✅ Spara för vald order')

-- btn_open_detail
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_open_detail' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'btn_open_detail', N'🔍 Apri dettagli')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_open_detail' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'btn_open_detail', N'🔍 Open details')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_open_detail' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'btn_open_detail', N'🔍 Deschide detalii')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_open_detail' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'btn_open_detail', N'🔍 Details öffnen')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_open_detail' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'btn_open_detail', N'🔍 Öppna detaljer')

-- justify_row (pannello giustificazione a livello di riga)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_row' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'justify_row', N'📝 Giustificazione a livello di riga (solo righe selezionate)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_row' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'justify_row', N'📝 Row-level justification (selected rows only)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_row' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'justify_row', N'📝 Justificare la nivel de rând (se aplică doar rândurilor selectate)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_row' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'justify_row', N'📝 Begründung auf Zeilenebene (nur ausgewählte Zeilen)')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'justify_row' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'justify_row', N'📝 Motivering på radnivå (bara valda rader)')

-- btn_save_rows
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_rows' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'btn_save_rows', N'✅ Salva per righe selezionate')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_rows' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'btn_save_rows', N'✅ Save for selected rows')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_rows' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'btn_save_rows', N'✅ Salvează pt. rândurile selectate')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_rows' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'btn_save_rows', N'✅ Für ausgewählte Zeilen speichern')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'btn_save_rows' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'btn_save_rows', N'✅ Spara för valda rader')

-- select_order (messaggio selezione ordine)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_order' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'it', N'select_order', N'Selezionare un ordine dalla lista.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_order' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'en', N'select_order', N'Please select an order from the list.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_order' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'ro', N'select_order', N'Selectați o comandă din listă.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_order' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'de', N'select_order', N'Bitte einen Auftrag aus der Liste auswählen.')

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'select_order' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES (N'sv', N'select_order', N'Välj en order från listan.')

GO

-- ================================================================
-- COLONNE MASTER (intestazioni tabella riepilogo)
-- ================================================================

-- col_order
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_order' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_order', N'Ordine')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_order' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_order', N'Order')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_order' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_order', N'Comandă')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_order' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_order', N'Auftrag')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_order' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_order', N'Order')

-- col_product
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_product' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_product', N'Prodotto')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_product' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_product', N'Product')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_product' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_product', N'Produs')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_product' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_product', N'Produkt')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_product' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_product', N'Produkt')

-- col_total_disc
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_total_disc' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_total_disc', N'Nr. Discrepanze')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_total_disc' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_total_disc', N'Nr. Discrepancies')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_total_disc' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_total_disc', N'Nr. Discrepanțe')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_total_disc' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_total_disc', N'Anz. Abweichungen')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_total_disc' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_total_disc', N'Antal avvikelser')

-- col_red
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_red' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_red', N'🔴 Ritardo')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_red' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_red', N'🔴 Delay')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_red' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_red', N'🔴 Întârziere')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_red' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_red', N'🔴 Verzögerung')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_red' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_red', N'🔴 Försening')

-- col_out_of_plan
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_out_of_plan' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_out_of_plan', N'🟠 Fuori Piano')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_out_of_plan' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_out_of_plan', N'🟠 Out of Plan')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_out_of_plan' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_out_of_plan', N'🟠 În afara planului')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_out_of_plan' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_out_of_plan', N'🟠 Außerhalb Plan')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_out_of_plan' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_out_of_plan', N'🟠 Utanför plan')

-- col_deficit_total
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_deficit_total' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_deficit_total', N'Deficit Totale')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_deficit_total' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_deficit_total', N'Total Deficit')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_deficit_total' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_deficit_total', N'Deficit Total')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_deficit_total' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_deficit_total', N'Gesamtdefizit')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_deficit_total' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_deficit_total', N'Totalt underskott')

-- col_phases
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_phases' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_phases', N'Fasi')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_phases' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_phases', N'Phases')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_phases' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_phases', N'Faze')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_phases' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_phases', N'Phasen')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_phases' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_phases', N'Faser')

-- col_first_alert
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_first_alert' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_first_alert', N'Prima Allerta')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_first_alert' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_first_alert', N'First Alert')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_first_alert' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_first_alert', N'Prima Alertă')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_first_alert' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_first_alert', N'Erster Alarm')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_first_alert' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_first_alert', N'Första avisering')

-- col_last_alert
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_last_alert' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_last_alert', N'Ultima Allerta')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_last_alert' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_last_alert', N'Last Alert')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_last_alert' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_last_alert', N'Ultima Alertă')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_last_alert' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_last_alert', N'Letzter Alarm')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_last_alert' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_last_alert', N'Senaste avisering')

-- ================================================================
-- COLONNE DETAIL (intestazioni tabella dettaglio)
-- ================================================================

-- col_phase
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_phase' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_phase', N'Fase')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_phase' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_phase', N'Phase')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_phase' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_phase', N'Fază')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_phase' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_phase', N'Phase')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_phase' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_phase', N'Fas')

-- col_qty_plan
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_plan' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_qty_plan', N'Qtà Pianificata')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_plan' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_qty_plan', N'Qty Plan')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_plan' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_qty_plan', N'Cant. Plan')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_plan' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_qty_plan', N'Menge Plan')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_plan' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_qty_plan', N'Antal plan')

-- col_qty_produced
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_produced' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_qty_produced', N'Qtà Prodotta')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_produced' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_qty_produced', N'Qty Produced')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_produced' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_qty_produced', N'Cant. Produsă')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_produced' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_qty_produced', N'Menge produziert')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_produced' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_qty_produced', N'Antal producerat')

-- col_qty_expected
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_expected' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_qty_expected', N'Qtà Prevista')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_expected' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_qty_expected', N'Qty Expected')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_expected' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_qty_expected', N'Cant. Așteptată')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_expected' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_qty_expected', N'Menge erwartet')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_qty_expected' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_qty_expected', N'Antal förväntat')

-- col_deficit
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_deficit' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_deficit', N'Deficit')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_deficit' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_deficit', N'Deficit')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_deficit' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_deficit', N'Deficit')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_deficit' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_deficit', N'Defizit')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_deficit' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_deficit', N'Underskott')

-- col_status
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_status' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_status', N'Stato')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_status' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_status', N'Status')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_status' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_status', N'Status')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_status' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_status', N'Status')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_status' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_status', N'Status')

-- col_alert_date
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_alert_date' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_alert_date', N'Data Allerta')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_alert_date' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_alert_date', N'Alert Date')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_alert_date' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_alert_date', N'Data Alertă')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_alert_date' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_alert_date', N'Alarmdatum')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_alert_date' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_alert_date', N'Aviseringsdatum')

-- col_projected_end
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_projected_end' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_projected_end', N'Fine Prevista')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_projected_end' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_projected_end', N'Projected End')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_projected_end' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_projected_end', N'Sfârșit prevăzut')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_projected_end' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_projected_end', N'Geplantes Ende')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_projected_end' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_projected_end', N'Beräknat slut')

-- col_future
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_future' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'col_future', N'Futuro')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_future' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'col_future', N'Future')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_future' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'col_future', N'Viitor')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_future' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'col_future', N'Zukunft')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'col_future' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'col_future', N'Framtid')

-- ================================================================
-- MESSAGGI E LABEL DINAMICI
-- ================================================================

-- plan_dblclick_hint
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'plan_dblclick_hint' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'plan_dblclick_hint', N'Doppio clic su una riga per vedere i dettagli')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'plan_dblclick_hint' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'plan_dblclick_hint', N'Double-click on a row to see details')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'plan_dblclick_hint' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'plan_dblclick_hint', N'Dublu-clic pe un rând pentru a vedea detaliile')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'plan_dblclick_hint' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'plan_dblclick_hint', N'Doppelklick auf eine Zeile für Details')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'plan_dblclick_hint' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'plan_dblclick_hint', N'Dubbelklicka på en rad för detaljer')

-- orders_with_discrepancies
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'orders_with_discrepancies' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'orders_with_discrepancies', N'ordini con discrepanze')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'orders_with_discrepancies' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'orders_with_discrepancies', N'orders with discrepancies')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'orders_with_discrepancies' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'orders_with_discrepancies', N'comenzi cu discrepanțe')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'orders_with_discrepancies' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'orders_with_discrepancies', N'Aufträge mit Abweichungen')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'orders_with_discrepancies' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'orders_with_discrepancies', N'ordrar med avvikelser')

-- analytical_alerts
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'analytical_alerts' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'analytical_alerts', N'allerte analitiche')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'analytical_alerts' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'analytical_alerts', N'analytical alerts')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'analytical_alerts' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'analytical_alerts', N'alerte analitice')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'analytical_alerts' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'analytical_alerts', N'analytische Alarme')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'analytical_alerts' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'analytical_alerts', N'analytiska aviseringar')

-- confirm_save_group
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'confirm_save_group' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'confirm_save_group', N'Salvare la giustificazione per {orders} ordini ({alerts} allerte totali)?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'confirm_save_group' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'confirm_save_group', N'Save justification for {orders} orders ({alerts} total alerts)?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'confirm_save_group' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'confirm_save_group', N'Salvați justificarea pentru {orders} comenzi ({alerts} alerte totale)?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'confirm_save_group' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'confirm_save_group', N'Begründung für {orders} Aufträge ({alerts} Alarme gesamt) speichern?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'confirm_save_group' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'confirm_save_group', N'Spara motivering för {orders} ordrar ({alerts} aviseringar totalt)?')

-- confirm_save_rows
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'confirm_save_rows' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'confirm_save_rows', N'Salvare la giustificazione per {count} righe?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'confirm_save_rows' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'confirm_save_rows', N'Save justification for {count} rows?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'confirm_save_rows' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'confirm_save_rows', N'Salvați justificarea pentru {count} rânduri?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'confirm_save_rows' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'confirm_save_rows', N'Begründung für {count} Zeilen speichern?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'confirm_save_rows' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'confirm_save_rows', N'Spara motivering för {count} rader?')

-- saved_justifications
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'saved_justifications' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'saved_justifications', N'{count} giustificazioni salvate con successo.')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'saved_justifications' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'saved_justifications', N'{count} justifications saved successfully.')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'saved_justifications' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'saved_justifications', N'{count} justificări salvate cu succes.')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'saved_justifications' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'saved_justifications', N'{count} Begründungen erfolgreich gespeichert.')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'saved_justifications' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'saved_justifications', N'{count} motiveringar sparade.')

-- timer_expired
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'timer_expired' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'timer_expired', N'SCADUTO')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'timer_expired' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'timer_expired', N'EXPIRED')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'timer_expired' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'timer_expired', N'EXPIRAT')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'timer_expired' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'timer_expired', N'ABGELAUFEN')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'timer_expired' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'timer_expired', N'UTGÅNGET')

-- close_with_pending
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'close_with_pending' AND LanguageCode = N'it')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'it', N'close_with_pending', N'Ci sono ancora {count} ordini con discrepanze non giustificate.
Chiudere?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'close_with_pending' AND LanguageCode = N'en')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'en', N'close_with_pending', N'There are still {count} orders with unjustified discrepancies.
Close?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'close_with_pending' AND LanguageCode = N'ro')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'ro', N'close_with_pending', N'Mai sunt {count} comenzi cu discrepanțe nejustificate.
Închideți?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'close_with_pending' AND LanguageCode = N'de')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'de', N'close_with_pending', N'Es gibt noch {count} Aufträge mit unbegründeten Abweichungen.
Schließen?')
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE TranslationKey = N'close_with_pending' AND LanguageCode = N'sv')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) VALUES (N'sv', N'close_with_pending', N'Det finns fortfarande {count} ordrar med omotiverade avvikelser.
Stäng?')

GO

PRINT 'Traduzioni per Piano Produzione — Discrepanze aggiunte con successo!'
