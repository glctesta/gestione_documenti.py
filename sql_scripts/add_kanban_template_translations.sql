-- Kanban template translations (extended with instructions sheet)

DECLARE @Keys TABLE (TranslationKey NVARCHAR(200), IT NVARCHAR(800), RO NVARCHAR(800), EN NVARCHAR(800), DE NVARCHAR(800), SV NVARCHAR(800));
INSERT INTO @Keys (TranslationKey, IT, RO, EN, DE, SV) VALUES
('button_export_template', 'Crea template Excel', 'Creeaza sablon Excel', 'Create Excel template', 'Excel-Vorlage erstellen', 'Skapa Excel-mall'),
('template_save_as', 'Salva template', 'Salveaza sablon', 'Save template', 'Vorlage speichern', 'Spara mall'),
('template_saved', 'Template salvato.', 'Sablon salvat.', 'Template saved.', 'Vorlage gespeichert.', 'Mall sparad.'),
('template_save_error', 'Errore salvataggio template: {err}', 'Eroare salvare sablon: {err}', 'Template save error: {err}', 'Fehler beim Speichern der Vorlage: {err}', 'Fel vid sparning av mall: {err}'),
('template_instructions_title', 'Istruzioni', 'Instructiuni', 'Instructions', 'Anleitung', 'Instruktioner'),
('template_instructions_body',
 'Compila le colonne:\n- ComponentCode: codice componente\n- LocationCode: locazione (gia precompilata)\n- Quantity: quantita (positiva=carico, negativa=prelievo)\nSalva e importa il file dalla maschera Kanban.',
 'Completeaza coloanele:\n- ComponentCode: cod componenta\n- LocationCode: locatie (precompletata)\n- Quantity: cantitate (pozitiva=incarcare, negativa=descarcare)\nSalveaza si importa fisierul din fereastra Kanban.',
 'Fill in the columns:\n- ComponentCode: component code\n- LocationCode: location (pre-filled)\n- Quantity: quantity (positive=load, negative=withdraw)\nSave and import the file from the Kanban form.',
 'Spalten ausfuellen:\n- ComponentCode: Bauteilcode\n- LocationCode: Lagerort (vorbefuellt)\n- Quantity: Menge (positiv=Einlagerung, negativ=Entnahme)\nSpeichern und die Datei im Kanban-Formular importieren.',
 'Fyll i kolumnerna:\n- ComponentCode: komponentkod\n- LocationCode: plats (forifylld)\n- Quantity: kvantitet (positiv=inlagring, negativ=uttag)\nSpara och importera filen i Kanban-formularet.'
);

-- Insert if missing
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue)
SELECT L.LanguageCode, K.TranslationKey,
       CASE L.LanguageCode
            WHEN 'it' THEN K.IT
            WHEN 'ro' THEN K.RO
            WHEN 'en' THEN K.EN
            WHEN 'de' THEN K.DE
            WHEN 'sv' THEN K.SV
       END AS TranslationValue
FROM @Keys K
CROSS JOIN (VALUES ('it'), ('ro'), ('en'), ('de'), ('sv')) AS L(LanguageCode)
WHERE NOT EXISTS (
    SELECT 1 FROM dbo.AppTranslations T
    WHERE T.LanguageCode = L.LanguageCode AND T.TranslationKey = K.TranslationKey
);

-- Verify
SELECT TranslationKey, LanguageCode, TranslationValue
FROM dbo.AppTranslations
WHERE TranslationKey IN (
    'button_export_template',
    'template_save_as',
    'template_saved',
    'template_save_error',
    'template_instructions_title',
    'template_instructions_body'
)
ORDER BY TranslationKey, LanguageCode;
