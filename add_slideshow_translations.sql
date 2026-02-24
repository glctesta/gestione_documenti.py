-- ============================================================
-- TRADUZIONI SLIDESHOW - PERCORSO IMMAGINI DINAMICO
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue:  RO, IT, EN, DE, SV
-- Chiavi:  slideshow_path_title, slideshow_path_message,
--          slideshow_select_folder, slideshow_no_folder
-- ============================================================

USE [Traceability_RS];
GO

-- ------------------------------------------------------------
-- slideshow_path_title  (titolo del messagebox)
-- ------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'slideshow_path_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'slideshow_path_title', N'Cale imagini Slideshow');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'slideshow_path_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'slideshow_path_title', N'Percorso Immagini Slideshow');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'slideshow_path_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'slideshow_path_title', N'Slideshow Images Path');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'slideshow_path_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'slideshow_path_title', N'Slideshow Bilderpfad');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'slideshow_path_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'slideshow_path_title', N'Bildv' + NCHAR(228) + N'g f' + NCHAR(246) + N'r Slideshow');
GO

-- ------------------------------------------------------------
-- slideshow_path_message  (corpo del messagebox)
-- ------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'slideshow_path_message')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'slideshow_path_message',
            N'Calea imaginilor pentru slideshow nu este configurat' + NCHAR(259) + N' sau nu a fost g' + NCHAR(259) + N'sit' + NCHAR(259) + N'.' + NCHAR(13) + NCHAR(10) + NCHAR(13) + NCHAR(10) +
            N'Selecta' + NCHAR(539) + N'i folderul care con' + NCHAR(539) + N'ine imaginile de afi' + NCHAR(537) + N'at.');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'slideshow_path_message')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'slideshow_path_message',
            N'Il percorso delle immagini per lo slideshow non ' + NCHAR(232) + N' configurato o non ' + NCHAR(232) + N' stato trovato.' + NCHAR(13) + NCHAR(10) + NCHAR(13) + NCHAR(10) +
            N'Seleziona la cartella contenente le immagini da visualizzare.');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'slideshow_path_message')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'slideshow_path_message',
            N'The slideshow image path is not configured or could not be found.' + NCHAR(13) + NCHAR(10) + NCHAR(13) + NCHAR(10) +
            N'Please select the folder containing the images to display.');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'slideshow_path_message')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'slideshow_path_message',
            N'Der Slideshow-Bildpfad ist nicht konfiguriert oder wurde nicht gefunden.' + NCHAR(13) + NCHAR(10) + NCHAR(13) + NCHAR(10) +
            N'Bitte w' + NCHAR(228) + N'hlen Sie den Ordner mit den anzuzeigenden Bildern.');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'slideshow_path_message')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'slideshow_path_message',
            N'S' + NCHAR(246) + N'kv' + NCHAR(228) + N'gen f' + NCHAR(246) + N'r bildspelsbilder ' + NCHAR(228) + N'r inte konfigurerad eller hittades inte.' + NCHAR(13) + NCHAR(10) + NCHAR(13) + NCHAR(10) +
            N'V' + NCHAR(228) + N'lj mappen som inneh' + NCHAR(229) + N'ller bilderna att visa.');
GO

-- ------------------------------------------------------------
-- slideshow_select_folder  (titolo del dialog di selezione)
-- ------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'slideshow_select_folder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'slideshow_select_folder', N'Selecta' + NCHAR(539) + N'i folderul de imagini pentru slideshow');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'slideshow_select_folder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'slideshow_select_folder', N'Seleziona cartella immagini slideshow');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'slideshow_select_folder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'slideshow_select_folder', N'Select slideshow images folder');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'slideshow_select_folder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'slideshow_select_folder', N'Slideshow-Bilderordner ausw' + NCHAR(228) + N'hlen');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'slideshow_select_folder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'slideshow_select_folder', N'V' + NCHAR(228) + N'lj mapp f' + NCHAR(246) + N'r bildspelsbilder');
GO

-- ------------------------------------------------------------
-- slideshow_no_folder  (label quando nessun percorso trovato)
-- ------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'ro' AND [TranslationKey] = N'slideshow_no_folder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'slideshow_no_folder', N'Niciun folder de imagini selectat.');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'it' AND [TranslationKey] = N'slideshow_no_folder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'slideshow_no_folder', N'Nessuna cartella immagini selezionata.');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'en' AND [TranslationKey] = N'slideshow_no_folder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'slideshow_no_folder', N'No image folder selected.');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'de' AND [TranslationKey] = N'slideshow_no_folder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'slideshow_no_folder', N'Kein Bilderordner ausgew' + NCHAR(228) + N'hlt.');
GO

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = N'sv' AND [TranslationKey] = N'slideshow_no_folder')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'slideshow_no_folder', N'Ingen bildmapp vald.');
GO

-- ------------------------------------------------------------
-- Verifica
-- ------------------------------------------------------------
SELECT [LanguageCode], [TranslationKey], [TranslationValue]
FROM [dbo].[AppTranslations]
WHERE [TranslationKey] IN (
    N'slideshow_path_title',
    N'slideshow_path_message',
    N'slideshow_select_folder',
    N'slideshow_no_folder'
)
ORDER BY [TranslationKey], [LanguageCode];
GO
