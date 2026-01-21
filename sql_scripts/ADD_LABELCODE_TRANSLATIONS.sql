-- Script per aggiungere traduzioni LabelCode
-- Data: 2026-01-21
-- Descrizione: Traduzioni per il nuovo campo LabelCode nella form di validazione linea

-- Italiano (it)
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
('it', 'labelcode_label', 'LabelCode:'),
('it', 'labelcode_verify_button', 'Verifica'),
('it', 'labelcode_enter_code', 'Inserire un LabelCode'),
('it', 'labelcode_select_order_first', 'Selezionare prima un ordine'),
('it', 'labelcode_validated', 'Validato (Ordine: {0})'),
('it', 'labelcode_wrong_order', 'Codice appartiene a ordine {0} (IDOrder: {1})'),
('it', 'labelcode_not_found', 'LabelCode non trovato nel database'),
('it', 'labelcode_validation_error', 'Errore validazione: {0}'),
('it', 'labelcode_missing_before_save', 'Inserire un LabelCode prima di salvare'),
('it', 'labelcode_not_validated_before_save', 'Verificare il LabelCode prima di salvare (premere il pulsante Verifica)');

-- Rumeno (ro) - con N prefix
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
('ro', 'labelcode_label', N'Cod etichetă:'),
('ro', 'labelcode_verify_button', N'Verifică'),
('ro', 'labelcode_enter_code', N'Introduceți un LabelCode'),
('ro', 'labelcode_select_order_first', N'Selectați mai întâi o comandă'),
('ro', 'labelcode_validated', N'Validat (Comandă: {0})'),
('ro', 'labelcode_wrong_order', N'Codul aparține comenzii {0} (IDOrder: {1})'),
('ro', 'labelcode_not_found', N'LabelCode nu a fost găsit în baza de date'),
('ro', 'labelcode_validation_error', N'Eroare validare: {0}'),
('ro', 'labelcode_missing_before_save', N'Introduceți un LabelCode înainte de salvare'),
('ro', 'labelcode_not_validated_before_save', N'Verificați LabelCode înainte de salvare (apăsați butonul Verifică)');

-- Inglese (en)
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
('en', 'labelcode_label', 'LabelCode:'),
('en', 'labelcode_verify_button', 'Verify'),
('en', 'labelcode_enter_code', 'Enter a LabelCode'),
('en', 'labelcode_select_order_first', 'Select an order first'),
('en', 'labelcode_validated', 'Validated (Order: {0})'),
('en', 'labelcode_wrong_order', 'Code belongs to order {0} (IDOrder: {1})'),
('en', 'labelcode_not_found', 'LabelCode not found in database'),
('en', 'labelcode_validation_error', 'Validation error: {0}'),
('en', 'labelcode_missing_before_save', 'Enter a LabelCode before saving'),
('en', 'labelcode_not_validated_before_save', 'Verify the LabelCode before saving (press the Verify button)');

-- Tedesco (de)
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
('de', 'labelcode_label', 'Etikettencode:'),
('de', 'labelcode_verify_button', 'Überprüfen'),
('de', 'labelcode_enter_code', 'Geben Sie einen LabelCode ein'),
('de', 'labelcode_select_order_first', 'Wählen Sie zuerst eine Bestellung aus'),
('de', 'labelcode_validated', 'Validiert (Bestellung: {0})'),
('de', 'labelcode_wrong_order', 'Code gehört zu Bestellung {0} (IDOrder: {1})'),
('de', 'labelcode_not_found', 'LabelCode wurde in der Datenbank nicht gefunden'),
('de', 'labelcode_validation_error', 'Validierungsfehler: {0}'),
('de', 'labelcode_missing_before_save', 'Geben Sie vor dem Speichern einen LabelCode ein'),
('de', 'labelcode_not_validated_before_save', 'Überprüfen Sie den LabelCode vor dem Speichern (drücken Sie die Schaltfläche Überprüfen)');

-- Svedese (sv)
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
VALUES 
('sv', 'labelcode_label', 'Etikettkod:'),
('sv', 'labelcode_verify_button', 'Verifiera'),
('sv', 'labelcode_enter_code', 'Ange en LabelCode'),
('sv', 'labelcode_select_order_first', 'Välj en order först'),
('sv', 'labelcode_validated', 'Validerad (Order: {0})'),
('sv', 'labelcode_wrong_order', 'Kod tillhör order {0} (IDOrder: {1})'),
('sv', 'labelcode_not_found', 'LabelCode hittades inte i databasen'),
('sv', 'labelcode_validation_error', 'Valideringsfel: {0}'),
('sv', 'labelcode_missing_before_save', 'Ange en LabelCode innan du sparar'),
('sv', 'labelcode_not_validated_before_save', 'Verifiera LabelCode innan du sparar (tryck på knappen Verifiera)');

GO

-- Verifica inserimenti
SELECT 
    LanguageCode,
    TranslationKey,
    TranslationValue
FROM [Traceability_RS].[dbo].[AppTranslations]
WHERE TranslationKey LIKE 'labelcode%'
ORDER BY TranslationKey, LanguageCode;
