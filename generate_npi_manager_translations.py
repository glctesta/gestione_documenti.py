#!/usr/bin/env python3
# Script per generare le traduzioni SQL per npi_manager.py

from pathlib import Path

# Dizionario delle traduzioni per npi_manager.py
translations = {
    # Validazioni
    'validation_error_end_before_start': {
        'it': 'La data di fine non può essere precedente alla data di inizio',
        'ro': 'Data de sfârșit nu poate fi înainte de data de început',
        'en': 'End date cannot be before start date',
        'de': 'Enddatum kann nicht vor dem Startdatum liegen',
        'sv': 'Slutdatum kan inte vara före startdatum'
    },
    'validation_error_start_date_required': {
        'it': 'La data di inizio è obbligatoria quando è specificata la data di fine',
        'ro': 'Data de început este obligatorie când este specificată data de sfârșit',
        'en': 'Start date is required when end date is specified',
        'de': 'Startdatum ist erforderlich, wenn Enddatum angegeben ist',
        'sv': 'Startdatum krävs när slutdatum anges'
    },
    
    # Info
    'info_project_due_date_aligned': {
        'it': 'La scadenza del progetto è stata allineata all\'ultimo task',
        'ro': 'Termenul limită al proiectului a fost aliniat la ultima sarcină',
        'en': 'Project due date has been aligned to the last task',
        'de': 'Projektfälligkeitsdatum wurde an die letzte Aufgabe angepasst',
        'sv': 'Projektets förfallodatum har anpassats till den sista uppgiften'
    },
    
    # Errori dipendenze
    'error_dependency_not_satisfied': {
        'it': 'Dipendenza non soddisfatta: il task "{predecessor}" deve essere completato prima',
        'ro': 'Dependență nesatisfăcută: sarcina "{predecessor}" trebuie finalizată mai întâi',
        'en': 'Dependency not satisfied: task "{predecessor}" must be completed first',
        'de': 'Abhängigkeit nicht erfüllt: Aufgabe "{predecessor}" muss zuerst abgeschlossen werden',
        'sv': 'Beroende ej uppfyllt: uppgift "{predecessor}" måste slutföras först'
    },
}

# Genera lo script SQL
output_file = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\NPI_MANAGER_TRANSLATIONS.sql")

with output_file.open('w', encoding='utf-8') as f:
    f.write("-- Script di traduzione per NPI Manager\n")
    f.write("-- Generato automaticamente\n")
    f.write("-- Tabella: [Traceability_RS].[dbo].[AppTranslations]\n\n")
    
    for key in sorted(translations.keys()):
        trans = translations[key]
        
        # IT
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        f.write(f"    VALUES ('it', '{key}', '{trans['it']}');\n\n")
        
        # RO (con N davanti)
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        f.write(f"    VALUES ('ro', '{key}', N'{trans['ro']}');\n\n")
        
        # EN
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        f.write(f"    VALUES ('en', '{key}', '{trans['en']}');\n\n")
        
        # DE
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        f.write(f"    VALUES ('de', '{key}', '{trans['de']}');\n\n")
        
        # SV
        f.write(f"IF NOT EXISTS (SELECT 1 FROM [Traceability_RS].[dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = '{key}')\n")
        f.write(f"    INSERT INTO [Traceability_RS].[dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])\n")
        f.write(f"    VALUES ('sv', '{key}', '{trans['sv']}');\n\n")

print(f"\n✅ Script SQL generato: {output_file}")
print(f"✅ Totale chiavi tradotte: {len(translations)}")
print(f"✅ Totale INSERT statements: {len(translations) * 5}")
