-- Script SQL per aggiungere le traduzioni per la gestione prodotti nei complaints
-- Tabella: apptranslation (languagecode, translationkey, translationvalue)
-- Lingue: it, ro, en, de, sv
-- Nota: Le stringhe rumene (ro) hanno la N davanti per i caratteri speciali
-- Usa IF NOT EXISTS per evitare duplicati

-- ============================================================================
-- BOTTONE REFRESH PRODOTTI
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'btn_refresh_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'btn_refresh_products', '🔄 Refresh Prodotti');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'btn_refresh_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'btn_refresh_products', '🔄 Refresh Products');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'btn_refresh_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'btn_refresh_products', N'🔄 Reîmprospătare Produse');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'btn_refresh_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'btn_refresh_products', '🔄 Produkte Aktualisieren');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'btn_refresh_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'btn_refresh_products', '🔄 Uppdatera Produkter');

-- ============================================================================
-- MESSAGGIO: VUOI RICARICARE I DATI?
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_reload_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_reload_products', 'Vuoi ricaricare i dati dei prodotti per vedere le eventuali modifiche?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_reload_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_reload_products', 'Do you want to reload product data to see any changes?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_reload_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_reload_products', N'Doriți să reîncărcați datele produselor pentru a vedea eventualele modificări?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_reload_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_reload_products', 'Möchten Sie die Produktdaten neu laden, um Änderungen zu sehen?');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_reload_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_reload_products', 'Vill du ladda om produktdata för att se eventuella ändringar?');

-- ============================================================================
-- MESSAGGIO: DATI PRODOTTI AGGIORNATI
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'msg_products_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'msg_products_updated', 'Dati prodotti aggiornati!');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'msg_products_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'msg_products_updated', 'Product data updated!');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'msg_products_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'msg_products_updated', N'Date produse actualizate!');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'msg_products_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'msg_products_updated', 'Produktdaten aktualisiert!');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'msg_products_updated')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'msg_products_updated', 'Produktdata uppdaterad!');

-- ============================================================================
-- ERRORE: IMPOSSIBILE APRIRE GESTIONE PRODOTTI
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'err_cannot_open_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'err_cannot_open_products', 'Impossibile aprire la gestione prodotti');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'err_cannot_open_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'err_cannot_open_products', 'Cannot open product management');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'err_cannot_open_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'err_cannot_open_products', N'Nu se poate deschide gestionarea produselor');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'err_cannot_open_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'err_cannot_open_products', 'Produktverwaltung kann nicht geöffnet werden');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'err_cannot_open_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'err_cannot_open_products', 'Kan inte öppna produkthantering');

-- ============================================================================
-- ERRORE: ERRORE NELL'APERTURA GESTIONE PRODOTTI
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'err_opening_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'err_opening_products', 'Errore nell''apertura della gestione prodotti');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'err_opening_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'err_opening_products', 'Error opening product management');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'err_opening_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'err_opening_products', N'Eroare la deschiderea gestionării produselor');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'err_opening_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'err_opening_products', 'Fehler beim Öffnen der Produktverwaltung');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'err_opening_products')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'err_opening_products', 'Fel vid öppning av produkthantering');

-- ============================================================================
-- ERRORE: ERRORE DURANTE IL REFRESH
-- ============================================================================

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'err_refresh_failed')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'err_refresh_failed', 'Errore durante il refresh');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'en' AND translationkey = 'err_refresh_failed')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('en', 'err_refresh_failed', 'Error during refresh');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'ro' AND translationkey = 'err_refresh_failed')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('ro', 'err_refresh_failed', N'Eroare în timpul reîmprospătării');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'de' AND translationkey = 'err_refresh_failed')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('de', 'err_refresh_failed', 'Fehler beim Aktualisieren');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'sv' AND translationkey = 'err_refresh_failed')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('sv', 'err_refresh_failed', 'Fel vid uppdatering');

-- ============================================================================
-- VERIFICA INSERIMENTI
-- ============================================================================

-- Query per verificare che tutte le traduzioni siano state inserite
SELECT 
    translationkey,
    COUNT(*) as num_languages,
    STRING_AGG(languagecode, ', ') as languages
FROM apptranslation
WHERE translationkey IN (
    'btn_refresh_products',
    'msg_reload_products',
    'msg_products_updated',
    'err_cannot_open_products',
    'err_opening_products',
    'err_refresh_failed'
)
GROUP BY translationkey
ORDER BY translationkey;

-- Dovrebbe mostrare 5 lingue per ogni chiave (it, ro, en, de, sv)

-- ============================================================================
-- QUERY DI ROLLBACK (se necessario)
-- ============================================================================

/*
-- Esegui questo solo se devi rimuovere le traduzioni
DELETE FROM apptranslation
WHERE translationkey IN (
    'btn_refresh_products',
    'msg_reload_products',
    'msg_products_updated',
    'err_cannot_open_products',
    'err_opening_products',
    'err_refresh_failed'
);
*/
