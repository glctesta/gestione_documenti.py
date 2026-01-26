-- =============================================
-- Script per inserimento traduzioni
-- Funzionalità: Prenotazione Sale Riunioni da Registrazione Ospiti
-- Data: 2026-01-26
-- =============================================

USE [Traceability_RS];
GO

-- Traduzione: "Prenotazione Sala" (titolo dialog)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'book_meeting_room' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'book_meeting_room', N'Prenotazione Sala');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'book_meeting_room' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'book_meeting_room', N'Rezervare Sală');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'book_meeting_room' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'book_meeting_room', N'Room Booking');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'book_meeting_room' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'book_meeting_room', N'Raumbuchung');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'book_meeting_room' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'book_meeting_room', N'Rumbokning');
END

-- Traduzione: "Vuoi prenotare una sala riunioni?" (messaggio dialog)
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'book_meeting_room_question' AND [LanguageCode] = 'it')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'it', N'book_meeting_room_question', N'Vuoi prenotare una sala riunioni?');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'book_meeting_room_question' AND [LanguageCode] = 'ro')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'ro', N'book_meeting_room_question', N'Doriți să rezervați o sală de ședințe?');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'book_meeting_room_question' AND [LanguageCode] = 'en')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'en', N'book_meeting_room_question', N'Do you want to book a meeting room?');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'book_meeting_room_question' AND [LanguageCode] = 'de')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'de', N'book_meeting_room_question', N'Möchten Sie einen Besprechungsraum buchen?');
END

IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [TranslationKey] = 'book_meeting_room_question' AND [LanguageCode] = 'sv')
BEGIN
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
    VALUES (N'sv', N'book_meeting_room_question', N'Vill du boka ett mötesrum?');
END

GO

-- Verifica inserimenti
SELECT [LanguageCode], [TranslationKey], [TranslationValue]
FROM [dbo].[AppTranslations]
WHERE [TranslationKey] IN ('book_meeting_room', 'book_meeting_room_question')
ORDER BY [TranslationKey], [LanguageCode];
GO
