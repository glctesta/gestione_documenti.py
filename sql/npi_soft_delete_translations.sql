-- ============================================================
-- NPI Soft-Delete: Aggiunta Traduzioni Nuove Labels
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Lingue: it, en, ro, de, sv
-- ============================================================

USE [Traceability_RS];
GO

-- -------------------------------------------------------
-- show_deleted_products  (Checkbox "Mostra eliminati")
-- -------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'show_deleted_products')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'show_deleted_products', N'Mostra eliminati');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'show_deleted_products')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'show_deleted_products', N'Show deleted');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'show_deleted_products')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'show_deleted_products', N'Afișează șterse');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'show_deleted_products')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'show_deleted_products', N'Gelöschte anzeigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'show_deleted_products')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'show_deleted_products', N'Visa borttagna');

-- -------------------------------------------------------
-- col_status  (Colonna "Stato" nel treeview prodotti)
-- -------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'col_status', N'Stato');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'col_status', N'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'col_status', N'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'col_status', N'Status');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'col_status')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'col_status', N'Status');

-- -------------------------------------------------------
-- status_active  (Valore cella: prodotto attivo)
-- -------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'status_active')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'status_active', N'Attivo');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'status_active')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'status_active', N'Active');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'status_active')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'status_active', N'Activ');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'status_active')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'status_active', N'Aktiv');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'status_active')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'status_active', N'Aktiv');

-- -------------------------------------------------------
-- status_deleted  (Valore cella: prodotto eliminato)
-- -------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'status_deleted')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'status_deleted', N'🗑 Eliminato');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'status_deleted')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'status_deleted', N'🗑 Deleted');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'status_deleted')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'status_deleted', N'🗑 Șters');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'status_deleted')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'status_deleted', N'🗑 Gelöscht');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'status_deleted')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'status_deleted', N'🗑 Raderad');

-- -------------------------------------------------------
-- btn_restore  (Pulsante "Ripristina")
-- -------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'btn_restore')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'btn_restore', N'↩ Ripristina');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'btn_restore')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'btn_restore', N'↩ Restore');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'btn_restore')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'btn_restore', N'↩ Restaurare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'btn_restore')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'btn_restore', N'↩ Wiederherstellen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'btn_restore')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'btn_restore', N'↩ Återställ');

-- -------------------------------------------------------
-- confirm_restore_title  (Titolo finestra conferma ripristino)
-- -------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'confirm_restore_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'confirm_restore_title', N'Conferma Ripristino');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'confirm_restore_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'confirm_restore_title', N'Confirm Restore');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'confirm_restore_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'confirm_restore_title', N'Confirmare Restaurare');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'confirm_restore_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'confirm_restore_title', N'Wiederherstellung bestätigen');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'confirm_restore_title')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'confirm_restore_title', N'Bekräfta återställning');

-- -------------------------------------------------------
-- confirm_restore_product_text  (Testo conferma ripristino)
-- -------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'confirm_restore_product_text')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'confirm_restore_product_text', N'Vuoi ripristinare questo prodotto? Tornerà visibile nelle liste attive.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'confirm_restore_product_text')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'confirm_restore_product_text', N'Do you want to restore this product? It will become visible in active lists again.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'confirm_restore_product_text')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'confirm_restore_product_text', N'Doriți să restaurați acest produs? Va fi din nou vizibil în listele active.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'confirm_restore_product_text')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'confirm_restore_product_text', N'Möchten Sie dieses Produkt wiederherstellen? Es wird wieder in den aktiven Listen sichtbar.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'confirm_restore_product_text')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'confirm_restore_product_text', N'Vill du återställa den här produkten? Den blir synlig i aktiva listor igen.');

-- -------------------------------------------------------
-- success_product_restored  (Messaggio successo ripristino)
-- -------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'success_product_restored')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'success_product_restored', N'Prodotto ripristinato con successo.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'success_product_restored')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'success_product_restored', N'Product restored successfully.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'success_product_restored')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'success_product_restored', N'Produs restaurat cu succes.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'success_product_restored')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'success_product_restored', N'Produkt erfolgreich wiederhergestellt.');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'success_product_restored')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'success_product_restored', N'Produkten återställdes.');

-- -------------------------------------------------------
-- db_error_restore_product  (Errore ripristino prodotto)
-- -------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'it' AND [TranslationKey] = 'db_error_restore_product')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'it', N'db_error_restore_product', N'Errore nel ripristino del prodotto: {error}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'en' AND [TranslationKey] = 'db_error_restore_product')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'en', N'db_error_restore_product', N'Error restoring product: {error}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'ro' AND [TranslationKey] = 'db_error_restore_product')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'ro', N'db_error_restore_product', N'Eroare la restaurarea produsului: {error}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'de' AND [TranslationKey] = 'db_error_restore_product')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'de', N'db_error_restore_product', N'Fehler beim Wiederherstellen des Produkts: {error}');
IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] WHERE [LanguageCode] = 'sv' AND [TranslationKey] = 'db_error_restore_product')
    INSERT INTO [dbo].[AppTranslations] ([LanguageCode],[TranslationKey],[TranslationValue]) VALUES (N'sv', N'db_error_restore_product', N'Fel vid återställning av produkt: {error}');

GO
PRINT 'NPI Soft-Delete translations inserted successfully.';
