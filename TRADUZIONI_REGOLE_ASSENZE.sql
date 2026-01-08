-- Traduzioni per il modulo di Regole Assenze
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Da eseguire sul database per aggiungere le traduzioni necessarie

USE [Traceability_RS]
GO

-- ========================================
-- Chiave permesso: Gestione Regole Assenze
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'gestione_regole_assenze')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'gestione_regole_assenze', 'Gestione Regole Assenze');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'gestione_regole_assenze')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'gestione_regole_assenze', 'Absence Rules Management');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'gestione_regole_assenze')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'gestione_regole_assenze', N'Gestionarea Regulilor de Absență');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'gestione_regole_assenze')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'gestione_regole_assenze', 'Abwesenheitsregelverwaltung');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'gestione_regole_assenze')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'gestione_regole_assenze', 'Hantering av Frånvaroregler');

GO

-- ========================================
-- Voce menu: Regole Assenze
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'submenu_absence_rules')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'submenu_absence_rules', 'Regole Assenze');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'submenu_absence_rules')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'submenu_absence_rules', 'Absence Rules');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'submenu_absence_rules')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'submenu_absence_rules', N'Reguli Absență');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'submenu_absence_rules')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'submenu_absence_rules', 'Abwesenheitsregeln');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'submenu_absence_rules')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'submenu_absence_rules', 'Frånvaroregler');

GO

-- ========================================
-- Titolo finestra
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'absence_rules_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'absence_rules_title', 'Regole Assenze');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'absence_rules_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'absence_rules_title', 'Absence Rules');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'absence_rules_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'absence_rules_title', N'Reguli Absență');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'absence_rules_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'absence_rules_title', 'Abwesenheitsregeln');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'absence_rules_title')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'absence_rules_title', 'Frånvaroregler');

GO

-- ========================================
-- Header finestra
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'absence_rules_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'absence_rules_header', 'Configurazione Regole Assenze');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'absence_rules_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'absence_rules_header', 'Absence Rules Configuration');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'absence_rules_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'absence_rules_header', N'Configurarea Regulilor de Absență');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'absence_rules_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'absence_rules_header', 'Konfiguration der Abwesenheitsregeln');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'absence_rules_header')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'absence_rules_header', 'Konfiguration av Frånvaroregler');

GO

-- ========================================
-- Seleziona Tipo Richiesta
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'select_request_type')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'select_request_type', 'Seleziona Tipo Richiesta');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'select_request_type')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'select_request_type', 'Select Request Type');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'select_request_type')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'select_request_type', N'Selectează Tipul de Cerere');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'select_request_type')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'select_request_type', 'Anfragetyp Auswählen');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'select_request_type')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'select_request_type', 'Välj Ansökningstyp');

GO

-- ========================================
-- Aggiungi Regola
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'add_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'add_rule', 'Aggiungi Regola');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'add_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'add_rule', 'Add Rule');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'add_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'add_rule', N'Adaugă Regulă');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'add_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'add_rule', 'Regel Hinzufügen');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'add_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'add_rule', 'Lägg till Regel');

GO

-- ========================================
-- Regole Esistenti
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'existing_rules')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'existing_rules', 'Regole Esistenti');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'existing_rules')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'existing_rules', 'Existing Rules');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'existing_rules')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'existing_rules', N'Reguli Existente');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'existing_rules')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'existing_rules', 'Bestehende Regeln');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'existing_rules')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'existing_rules', 'Befintliga Regler');

GO

-- ========================================
-- Colonne Treeview
-- ========================================

-- ID Tipo Richiesta
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'col_request_type_id')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'col_request_type_id', 'ID Tipo');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'col_request_type_id')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'col_request_type_id', 'Type ID');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'col_request_type_id')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'col_request_type_id', 'ID Tip');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'col_request_type_id')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'col_request_type_id', 'Typ-ID');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'col_request_type_id')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'col_request_type_id', 'Typ-ID');

GO

-- Tipo Richiesta
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'col_request_name')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'col_request_name', 'Tipo Richiesta');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'col_request_name')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'col_request_name', 'Request Type');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'col_request_name')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'col_request_name', N'Tip de Cerere');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'col_request_name')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'col_request_name', 'Anfragetyp');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'col_request_name')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'col_request_name', 'Ansökningstyp');

GO

-- Giorni di Anticipo
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'col_days_advance')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'col_days_advance', 'Giorni di Anticipo');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'col_days_advance')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'col_days_advance', 'Days in Advance');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'col_days_advance')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'col_days_advance', N'Zile în Avans');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'col_days_advance')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'col_days_advance', 'Tage im Voraus');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'col_days_advance')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'col_days_advance', 'Dagar i Förväg');

GO

-- ========================================
-- Bottoni Azioni
-- ========================================

-- Modifica Giorni
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'modify_days')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'modify_days', 'Modifica Giorni');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'modify_days')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'modify_days', 'Modify Days');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'modify_days')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'modify_days', N'Modifică Zilele');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'modify_days')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'modify_days', 'Tage Ändern');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'modify_days')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'modify_days', 'Ändra Dagar');

GO

-- Elimina Regola
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'delete_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'delete_rule', 'Elimina Regola');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'delete_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'delete_rule', 'Delete Rule');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'delete_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'delete_rule', N'Șterge Regula');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'delete_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'delete_rule', 'Regel Löschen');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'delete_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'delete_rule', 'Ta bort Regel');

GO

-- Aggiorna
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'refresh')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'refresh', 'Aggiorna');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'refresh')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'refresh', 'Refresh');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'refresh')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'refresh', N'Actualizare');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'refresh')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'refresh', 'Aktualisieren');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'refresh')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'refresh', 'Uppdatera');

GO

-- ========================================
-- Nota informativa
-- ========================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'absence_rules_note')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'absence_rules_note', 'Queste regole influenzano la possibilità di richiedere giorni di assenza. La data di richiesta inizio assenza in relazione con la data inizio assenza desiderata, non potrà essere minore del valore di DayNoZone (Giorni di anticipo).');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'absence_rules_note')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'absence_rules_note', 'These rules affect the ability to request absence days. The absence request date in relation to the desired absence start date cannot be less than the DayNoZone value (Days in advance).');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'absence_rules_note')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'absence_rules_note', N'Aceste reguli influențează posibilitatea de a solicita zile de absență. Data cererii de început a absenței în raport cu data dorită de început a absenței nu poate fi mai mică decât valoarea DayNoZone (Zile în avans).');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'absence_rules_note')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'absence_rules_note', 'Diese Regeln beeinflussen die Möglichkeit, Abwesenheitstage zu beantragen. Das Abwesenheitsantragsdatum im Verhältnis zum gewünschten Startdatum der Abwesenheit darf nicht kleiner als der DayNoZone-Wert (Tage im Voraus) sein.');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'absence_rules_note')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'absence_rules_note', 'Dessa regler påverkar möjligheten att begära frånvarodagar. Datumet för frånvaroansökan i förhållande till önskat startdatum för frånvaro får inte vara mindre än DayNoZone-värdet (Dagar i förväg).');

GO

-- ========================================
-- Messaggi di avviso e errore
-- ========================================

-- Selezionare prima un tipo di richiesta
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'select_request_type_first')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'select_request_type_first', 'Selezionare prima un tipo di richiesta');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'select_request_type_first')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'select_request_type_first', 'Please select a request type first');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'select_request_type_first')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'select_request_type_first', N'Vă rugăm să selectați mai întâi un tip de cerere');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'select_request_type_first')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'select_request_type_first', 'Bitte wählen Sie zuerst einen Anfragetyp');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'select_request_type_first')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'select_request_type_first', 'Välj först en ansökningstyp');

GO

-- Regola già esistente
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rule_already_exists')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'rule_already_exists', 'Esiste già una regola attiva per questo tipo di richiesta');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rule_already_exists')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'rule_already_exists', 'An active rule already exists for this request type');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rule_already_exists')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'rule_already_exists', N'Există deja o regulă activă pentru acest tip de cerere');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rule_already_exists')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'rule_already_exists', 'Für diesen Anfragetyp existiert bereits eine aktive Regel');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rule_already_exists')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'rule_already_exists', 'En aktiv regel finns redan för denna ansökningstyp');

GO

-- Selezionare prima una regola
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'select_rule_first')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'select_rule_first', 'Selezionare prima una regola dalla lista');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'select_rule_first')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'select_rule_first', 'Please select a rule from the list first');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'select_rule_first')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'select_rule_first', N'Vă rugăm să selectați mai întâi o regulă din listă');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'select_rule_first')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'select_rule_first', 'Bitte wählen Sie zuerst eine Regel aus der Liste');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'select_rule_first')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'select_rule_first', 'Välj först en regel från listan');

GO

-- Conferma eliminazione
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'confirm_delete_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'confirm_delete_rule', 'Confermare l''eliminazione della regola per "{0}"?');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'confirm_delete_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'confirm_delete_rule', 'Confirm deletion of rule for "{0}"?');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'confirm_delete_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'confirm_delete_rule', N'Confirmați ștergerea regulii pentru "{0}"?');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'confirm_delete_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'confirm_delete_rule', 'Löschen der Regel für "{0}" bestätigen?');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'confirm_delete_rule')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'confirm_delete_rule', 'Bekräfta borttagning av regel för "{0}"?');

GO

-- ========================================
-- Messaggi di successo
-- ========================================

-- Regola aggiunta
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rule_added')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'rule_added', 'Regola aggiunta con successo');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rule_added')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'rule_added', 'Rule added successfully');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rule_added')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'rule_added', N'Regula a fost adăugată cu succes');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rule_added')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'rule_added', 'Regel erfolgreich hinzugefügt');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rule_added')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'rule_added', 'Regel tillagd framgångsrikt');

GO

-- Regola aggiornata
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rule_updated')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'rule_updated', 'Regola aggiornata con successo');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rule_updated')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'rule_updated', 'Rule updated successfully');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rule_updated')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'rule_updated', N'Regula a fost actualizată cu succes');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rule_updated')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'rule_updated', 'Regel erfolgreich aktualisiert');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rule_updated')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'rule_updated', 'Regel uppdaterad framgångsrikt');

GO

-- Regola eliminata
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'rule_deleted')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'rule_deleted', 'Regola eliminata con successo');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'rule_deleted')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'rule_deleted', 'Rule deleted successfully');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'rule_deleted')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'rule_deleted', N'Regula a fost ștearsă cu succes');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'rule_deleted')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'rule_deleted', 'Regel erfolgreich gelöscht');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'rule_deleted')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'rule_deleted', 'Regel borttagen framgångsrikt');

GO

-- ========================================
-- Dialog input giorni
-- ========================================

-- Inserire giorni di anticipo
-- Italiano
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'it' AND TranslationKey = 'enter_days_advance')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('it', 'enter_days_advance', 'Inserire i giorni di anticipo:');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'en' AND TranslationKey = 'enter_days_advance')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('en', 'enter_days_advance', 'Enter days in advance:');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'ro' AND TranslationKey = 'enter_days_advance')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('ro', 'enter_days_advance', N'Introduceți zilele în avans:');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'de' AND TranslationKey = 'enter_days_advance')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('de', 'enter_days_advance', 'Tage im Voraus eingeben:');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE LanguageCode = 'sv' AND TranslationKey = 'enter_days_advance')
    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue)
    VALUES ('sv', 'enter_days_advance', 'Ange dagar i förväg:');

GO

PRINT 'Traduzioni per Regole Assenze installate con successo!'
PRINT 'Totale chiavi inserite: 24 x 5 lingue = 120 traduzioni'
GO
