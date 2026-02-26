-- ============================================================
-- Traduzioni per avviso dipendente con ore straordinarie eccedute
-- Chiave: employee_exceeded_warning
-- ============================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_exceeded_warning' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue])
    VALUES (N'it', N'employee_exceeded_warning', N'Questo dipendente non è eleggibile dato che ha totalizzato più ore di quelle ammesse per legge. La decisione di accettare le ore straordinarie per questa persona è demandata all''amministratore.');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_exceeded_warning' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue])
    VALUES (N'ro', N'employee_exceeded_warning', N'Acest angajat nu este eligibil deoarece a acumulat mai multe ore decât cele permise de lege. Decizia de a accepta orele suplimentare pentru această persoană revine administratorului.');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_exceeded_warning' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue])
    VALUES (N'en', N'employee_exceeded_warning', N'This employee is not eligible as they have accumulated more overtime hours than legally permitted. The decision to accept overtime for this person is delegated to the administrator.');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_exceeded_warning' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue])
    VALUES (N'de', N'employee_exceeded_warning', N'Dieser Mitarbeiter ist nicht berechtigt, da er mehr Überstunden angesammelt hat als gesetzlich zulässig. Die Entscheidung über die Genehmigung der Überstunden für diese Person obliegt dem Administrator.');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_exceeded_warning' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue])
    VALUES (N'sv', N'employee_exceeded_warning', N'Denna anställd är inte berättigad eftersom de har ackumulerat fler övertidstimmar än vad som är lagligt tillåtet. Beslutet att godkänna övertid för denna person överlåts till administratören.');

-- ============================================================
-- Traduzioni per conferma aggiunta dipendente con ore eccedute
-- Chiave: employee_exceeded_hours
-- ============================================================

-- Italiano
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_exceeded_hours' AND LanguageCode = N'it')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue])
    VALUES (N'it', N'employee_exceeded_hours', N'Attenzione: questo dipendente ha superato il limite ore mensili. La decisione verrà valutata in fase di approvazione. Procedere comunque?');

-- Rumeno
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_exceeded_hours' AND LanguageCode = N'ro')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue])
    VALUES (N'ro', N'employee_exceeded_hours', N'Atenție: acest angajat a depășit limita de ore lunare. Decizia va fi evaluată în faza de aprobare. Continuați oricum?');

-- Inglese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_exceeded_hours' AND LanguageCode = N'en')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue])
    VALUES (N'en', N'employee_exceeded_hours', N'Warning: this employee has exceeded the monthly hours limit. The decision will be evaluated during the approval phase. Proceed anyway?');

-- Tedesco
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_exceeded_hours' AND LanguageCode = N'de')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue])
    VALUES (N'de', N'employee_exceeded_hours', N'Achtung: Dieser Mitarbeiter hat das monatliche Stundenlimit überschritten. Die Entscheidung wird in der Genehmigungsphase bewertet. Trotzdem fortfahren?');

-- Svedese
IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE TranslationKey = N'employee_exceeded_hours' AND LanguageCode = N'sv')
    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue])
    VALUES (N'sv', N'employee_exceeded_hours', N'Varning: denna anställd har överskridit den månatliga timgränsen. Beslutet kommer att utvärderas under godkännandefasen. Fortsätt ändå?');
