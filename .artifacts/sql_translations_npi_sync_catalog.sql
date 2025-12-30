-- Script SQL per aggiungere le traduzioni per la sincronizzazione catalogo NPI
-- Tabella: apptranslation (languagecode, translationkey, translationvalue)
-- Lingue: it, ro, en, de, sv
-- Nota: Le stringhe rumene (ro) hanno la N davanti per i caratteri speciali

-- ============================================================================
-- BOTTONE SINCRONIZZA CATALOGO
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'btn_sync_catalog')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'btn_sync_catalog', 'Sincronizza Catalogo');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'btn_sync_catalog')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'btn_sync_catalog', 'Sync Catalog');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'btn_sync_catalog')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'btn_sync_catalog', N'Sincronizare Catalog');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'btn_sync_catalog')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'btn_sync_catalog', 'Katalog Synchronisieren');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'btn_sync_catalog')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'btn_sync_catalog', 'Synkronisera Katalog');

-- ============================================================================
-- MESSAGGIO: CONFERMA SINCRONIZZAZIONE
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_sync_catalog')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_sync_catalog', 'Questa operazione aggiungerà al progetto tutti i task del catalogo che non sono ancora presenti.

I task già esistenti non verranno modificati.

Vuoi continuare?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_sync_catalog')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_sync_catalog', 'This operation will add all catalog tasks that are not yet present in the project.

Existing tasks will not be modified.

Do you want to continue?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_sync_catalog')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_sync_catalog', N'Această operațiune va adăuga la proiect toate sarcinile din catalog care nu sunt încă prezente.

Sarcinile existente nu vor fi modificate.

Doriți să continuați?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_sync_catalog')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_sync_catalog', 'Dieser Vorgang fügt dem Projekt alle Katalogaufgaben hinzu, die noch nicht vorhanden sind.

Vorhandene Aufgaben werden nicht geändert.

Möchten Sie fortfahren?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_sync_catalog')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_sync_catalog', 'Denna åtgärd kommer att lägga till alla kataloguppgifter som ännu inte finns i projektet.

Befintliga uppgifter kommer inte att ändras.

Vill du fortsätta?');

-- ============================================================================
-- MESSAGGIO: NESSUN TASK MANCANTE
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_no_missing_tasks')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_no_missing_tasks', 'Tutti i task del catalogo sono già presenti nel progetto.');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_no_missing_tasks')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_no_missing_tasks', 'All catalog tasks are already present in the project.');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_no_missing_tasks')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_no_missing_tasks', N'Toate sarcinile din catalog sunt deja prezente în proiect.');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_no_missing_tasks')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_no_missing_tasks', 'Alle Katalogaufgaben sind bereits im Projekt vorhanden.');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_no_missing_tasks')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_no_missing_tasks', 'Alla kataloguppgifter finns redan i projektet.');

-- ============================================================================
-- MESSAGGIO: TASK SINCRONIZZATI
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_tasks_synced')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_tasks_synced', 'Aggiunti {0} task dal catalogo.');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_tasks_synced')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_tasks_synced', 'Added {0} tasks from catalog.');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_tasks_synced')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_tasks_synced', N'Au fost adăugate {0} sarcini din catalog.');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_tasks_synced')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_tasks_synced', '{0} Aufgaben aus dem Katalog hinzugefügt.');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_tasks_synced')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_tasks_synced', 'Lade till {0} uppgifter från katalogen.');

-- ============================================================================
-- VERIFICA INSERIMENTI
-- ============================================================================

SELECT 
    translationkey,
    COUNT(*) as num_languages,
    STRING_AGG(languagecode, ', ') as languages
FROM apptranslation
WHERE translationkey IN (
    'btn_sync_catalog',
    'msg_sync_catalog',
    'msg_no_missing_tasks',
    'msg_tasks_synced'
)
GROUP BY translationkey
ORDER BY translationkey;
