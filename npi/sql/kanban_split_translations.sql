-- Script SQL per nuove traduzioni Kanban Load/Unload Split
-- Eseguire su database TraceabilityRS

-- ========================================
-- Titoli Form
-- ========================================

-- kanban_load_title
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
    (N'it', N'kanban_load_title', N'KanBan - Carico Materiali'),
    (N'en', N'kanban_load_title', N'KanBan - Load Materials'),
    (N'de', N'kanban_load_title', N'KanBan - Materialbeladung'),
    (N'ro', N'kanban_load_title', N'KanBan - Încărcare Materiale'),
    (N'sv', N'kanban_load_title', N'KanBan - Lastning av material');

-- kanban_unload_title
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
    (N'it', N'kanban_unload_title', N'KanBan - Prelievo Materiali'),
    (N'en', N'kanban_unload_title', N'KanBan - Withdraw Materials'),
    (N'de', N'kanban_unload_title', N'KanBan - Materialentnahme'),
    (N'ro', N'kanban_unload_title', N'KanBan - Retragere Materiale'),
    (N'sv', N'kanban_unload_title', N'KanBan - Uttag av material');

-- ========================================
-- Pulsanti
-- ========================================

-- btn_generate_template
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
    (N'it', N'btn_generate_template', N'Genera Template Excel'),
    (N'en', N'btn_generate_template', N'Generate Excel Template'),
    (N'de', N'btn_generate_template', N'Excel-Vorlage generieren'),
    (N'ro', N'btn_generate_template', N'Generează șablon Excel'),
    (N'sv', N'btn_generate_template', N'Generera Excel-mall');

-- ========================================
-- Messaggi
-- ========================================

-- template_generated_msg
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
    (N'it', N'template_generated_msg', N'Template generato: {path}\nAprirlo ora?'),
    (N'en', N'template_generated_msg', N'Template generated: {path}\nOpen it now?'),
    (N'de', N'template_generated_msg', N'Vorlage erstellt: {path}\nJetzt öffnen?'),
    (N'ro', N'template_generated_msg', N'Șablon generat: {path}\nÎl deschideți acum?'),
    (N'sv', N'template_generated_msg', N'Mall skapad: {path}\nÖppna den nu?');

-- template_generation_error
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
    (N'it', N'template_generation_error', N'Errore generazione template: {error}'),
    (N'en', N'template_generation_error', N'Template generation error: {error}'),
    (N'de', N'template_generation_error', N'Fehler beim Erstellen der Vorlage: {error}'),
    (N'ro', N'template_generation_error', N'Eroare la generarea șablonului: {error}'),
    (N'sv', N'template_generation_error', N'Fel vid mallgenerering: {error}');

-- select_area_first
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
    (N'it', N'select_area_first', N'Seleziona prima un''area KanBan per generare il template.'),
    (N'en', N'select_area_first', N'Select a KanBan area first to generate the template.'),
    (N'de', N'select_area_first', N'Wählen Sie zuerst einen KanBan-Bereich aus, um die Vorlage zu erstellen.'),
    (N'ro', N'select_area_first', N'Selectați mai întâi o zonă KanBan pentru a genera șablonul.'),
    (N'sv', N'select_area_first', N'Välj ett KanBan-område först för att skapa mallen.');

GO

-- Verifica traduzioni
SELECT TranslationKey, LanguageCode, TranslationValue
FROM [dbo].[AppTranslations]
WHERE TranslationKey IN (
    'kanban_load_title',
    'kanban_unload_title',
    'btn_generate_template',
    'template_generated_msg',
    'template_generation_error',
    'select_area_first'
)
ORDER BY TranslationKey, LanguageCode;
