-- Script SQL: traduzioni per menu/finestra spedizioni urgenti
-- Tabella: [Traceability_RS].[dbo].[AppTranslations]
-- Data: 2026-05-25

USE [Traceability_RS];
GO

;WITH T AS (
    SELECT * FROM (VALUES
        -- ===== MENU ORDINI / SPEDIZIONI =====
        (N'it', N'submenu_shipments', N'Spedizioni'),
        (N'en', N'submenu_shipments', N'Shipments'),
        (N'de', N'submenu_shipments', N'Lieferungen'),
        (N'ro', N'submenu_shipments', N'Expedieri'),
        (N'sv', N'submenu_shipments', N'Leveranser'),

        (N'it', N'submenu_shipment_ws_config', N'Imposta Computer Spedizioni'),
        (N'en', N'submenu_shipment_ws_config', N'Set Shipment Computer'),
        (N'de', N'submenu_shipment_ws_config', N'Shipping-PC konfigurieren'),
        (N'ro', N'submenu_shipment_ws_config', N'Setează Calculator Expediții'),
        (N'sv', N'submenu_shipment_ws_config', N'Ställ in Leveransdator'),

        (N'it', N'submenu_shipment_confirm', N'Conferma Shipping'),
        (N'en', N'submenu_shipment_confirm', N'Confirm Shipping'),
        (N'de', N'submenu_shipment_confirm', N'Versand bestätigen'),
        (N'ro', N'submenu_shipment_confirm', N'Confirmă Livrarea'),
        (N'sv', N'submenu_shipment_confirm', N'Bekräfta Leverans'),

        -- Chiave usata per autorizzazione menu
        (N'it', N'spedizioni_urgenti', N'Spedizioni Urgenti'),
        (N'en', N'spedizioni_urgenti', N'Urgent Shipments'),
        (N'de', N'spedizioni_urgenti', N'Dringende Lieferungen'),
        (N'ro', N'spedizioni_urgenti', N'Expedieri Urgente'),
        (N'sv', N'spedizioni_urgenti', N'Akuta Leveranser'),

        -- ===== WORKSTATION CONFIG WINDOW =====
        (N'it', N'shipment_ws_title', N'Configurazione Postazione Spedizioni'),
        (N'en', N'shipment_ws_title', N'Shipment Workstation Configuration'),
        (N'de', N'shipment_ws_title', N'Konfiguration Versand-Arbeitsplatz'),
        (N'ro', N'shipment_ws_title', N'Configurare Stație Expedieri'),
        (N'sv', N'shipment_ws_title', N'Konfiguration av Leveransarbetsstation'),

        (N'it', N'shipment_ws_header', N'Configurazione Postazione Spedizioni Urgenti'),
        (N'en', N'shipment_ws_header', N'Urgent Shipment Workstation Configuration'),
        (N'de', N'shipment_ws_header', N'Konfiguration Dringende Versand-Station'),
        (N'ro', N'shipment_ws_header', N'Configurare Stație Expedieri Urgente'),
        (N'sv', N'shipment_ws_header', N'Konfiguration för Akut Leveransstation'),

        (N'it', N'shipment_ws_desc', N'Attivando questa funzione, il computer riceverà i popup di notifica per le spedizioni urgenti inserite nel sistema.'),
        (N'en', N'shipment_ws_desc', N'By enabling this function, the computer will receive notification popups for urgent shipments entered in the system.'),
        (N'de', N'shipment_ws_desc', N'Durch Aktivierung dieser Funktion empfängt der Computer Benachrichtigungs-Popups für dringende Sendungen im System.'),
        (N'ro', N'shipment_ws_desc', N'Prin activarea acestei funcții, calculatorul va primi popup-uri de notificare pentru expedierile urgente introduse în sistem.'),
        (N'sv', N'shipment_ws_desc', N'När funktionen aktiveras får datorn popup-notiser för akuta leveranser som registrerats i systemet.'),

        (N'it', N'shipment_ws_activate', N'Attiva Postazione'),
        (N'en', N'shipment_ws_activate', N'Activate Workstation'),
        (N'de', N'shipment_ws_activate', N'Arbeitsplatz aktivieren'),
        (N'ro', N'shipment_ws_activate', N'Activează Stația'),
        (N'sv', N'shipment_ws_activate', N'Aktivera Station'),

        (N'it', N'shipment_ws_deactivate', N'Disattiva Postazione'),
        (N'en', N'shipment_ws_deactivate', N'Deactivate Workstation'),
        (N'de', N'shipment_ws_deactivate', N'Arbeitsplatz deaktivieren'),
        (N'ro', N'shipment_ws_deactivate', N'Dezactivează Stația'),
        (N'sv', N'shipment_ws_deactivate', N'Inaktivera Station'),

        (N'it', N'shipment_ws_active', N'Postazione ATTIVA\nHost: {0}\nAttivata da: {1} - {2}'),
        (N'en', N'shipment_ws_active', N'Workstation ACTIVE\nHost: {0}\nActivated by: {1} - {2}'),
        (N'de', N'shipment_ws_active', N'Arbeitsplatz AKTIV\nHost: {0}\nAktiviert von: {1} - {2}'),
        (N'ro', N'shipment_ws_active', N'Stație ACTIVĂ\nHost: {0}\nActivată de: {1} - {2}'),
        (N'sv', N'shipment_ws_active', N'Station AKTIV\nVärd: {0}\nAktiverad av: {1} - {2}'),

        (N'it', N'shipment_ws_file_error', N'File presente ma non leggibile'),
        (N'en', N'shipment_ws_file_error', N'File exists but cannot be read'),
        (N'de', N'shipment_ws_file_error', N'Datei vorhanden, aber nicht lesbar'),
        (N'ro', N'shipment_ws_file_error', N'Fișier prezent dar ilizibil'),
        (N'sv', N'shipment_ws_file_error', N'Filen finns men kan inte läsas'),

        (N'it', N'shipment_ws_inactive', N'Postazione NON attiva'),
        (N'en', N'shipment_ws_inactive', N'Workstation NOT active'),
        (N'de', N'shipment_ws_inactive', N'Arbeitsplatz NICHT aktiv'),
        (N'ro', N'shipment_ws_inactive', N'Stație NEactivă'),
        (N'sv', N'shipment_ws_inactive', N'Station EJ aktiv'),

        (N'it', N'shipment_ws_activated', N'Postazione spedizioni attivata.'),
        (N'en', N'shipment_ws_activated', N'Shipment workstation activated.'),
        (N'de', N'shipment_ws_activated', N'Versand-Arbeitsplatz aktiviert.'),
        (N'ro', N'shipment_ws_activated', N'Stația de expediții a fost activată.'),
        (N'sv', N'shipment_ws_activated', N'Leveransstation aktiverad.'),

        (N'it', N'shipment_ws_perm_error', N'Permessi insufficienti. Eseguire come Amministratore.'),
        (N'en', N'shipment_ws_perm_error', N'Insufficient permissions. Run as Administrator.'),
        (N'de', N'shipment_ws_perm_error', N'Unzureichende Berechtigungen. Als Administrator ausführen.'),
        (N'ro', N'shipment_ws_perm_error', N'Permisiuni insuficiente. Rulați ca Administrator.'),
        (N'sv', N'shipment_ws_perm_error', N'Otillräckliga behörigheter. Kör som administratör.'),

        (N'it', N'shipment_ws_confirm_deactivate', N'Disattivare questa postazione spedizioni?'),
        (N'en', N'shipment_ws_confirm_deactivate', N'Deactivate this shipment workstation?'),
        (N'de', N'shipment_ws_confirm_deactivate', N'Diesen Versand-Arbeitsplatz deaktivieren?'),
        (N'ro', N'shipment_ws_confirm_deactivate', N'Dezactivați această stație de expediții?'),
        (N'sv', N'shipment_ws_confirm_deactivate', N'Inaktivera denna leveransstation?'),

        (N'it', N'shipment_ws_deactivated', N'Postazione spedizioni disattivata.'),
        (N'en', N'shipment_ws_deactivated', N'Shipment workstation deactivated.'),
        (N'de', N'shipment_ws_deactivated', N'Versand-Arbeitsplatz deaktiviert.'),
        (N'ro', N'shipment_ws_deactivated', N'Stația de expediții a fost dezactivată.'),
        (N'sv', N'shipment_ws_deactivated', N'Leveransstation inaktiverad.'),

        -- ===== CONFERMA SHIPPING WINDOW =====
        (N'it', N'shipment_confirm_title', N'Conferma Spedizioni Urgenti'),
        (N'en', N'shipment_confirm_title', N'Confirm Urgent Shipments'),
        (N'de', N'shipment_confirm_title', N'Dringende Lieferungen bestätigen'),
        (N'ro', N'shipment_confirm_title', N'Confirmare Expedieri Urgente'),
        (N'sv', N'shipment_confirm_title', N'Bekräfta Akuta Leveranser'),

        (N'it', N'shipment_confirm_header', N'Spedizioni Urgenti - Conferma Ricezione'),
        (N'en', N'shipment_confirm_header', N'Urgent Shipments - Receipt Confirmation'),
        (N'de', N'shipment_confirm_header', N'Dringende Lieferungen - Empfangsbestätigung'),
        (N'ro', N'shipment_confirm_header', N'Expedieri Urgente - Confirmare Primire'),
        (N'sv', N'shipment_confirm_header', N'Akuta Leveranser - Mottagningsbekräftelse'),

        (N'it', N'shipment_confirm_panel', N'Conferma Spedizione Selezionata'),
        (N'en', N'shipment_confirm_panel', N'Confirm Selected Shipment'),
        (N'de', N'shipment_confirm_panel', N'Ausgewählte Lieferung bestätigen'),
        (N'ro', N'shipment_confirm_panel', N'Confirmă Expedierea Selectată'),
        (N'sv', N'shipment_confirm_panel', N'Bekräfta vald leverans'),

        (N'it', N'shipment_confirm_qty_label', N'Quantità confermata:'),
        (N'en', N'shipment_confirm_qty_label', N'Confirmed quantity:'),
        (N'de', N'shipment_confirm_qty_label', N'Bestätigte Menge:'),
        (N'ro', N'shipment_confirm_qty_label', N'Cantitate confirmată:'),
        (N'sv', N'shipment_confirm_qty_label', N'Bekräftad kvantitet:'),

        (N'it', N'btn_confirm_shipping', N'Conferma Spedizione'),
        (N'en', N'btn_confirm_shipping', N'Confirm Shipping'),
        (N'de', N'btn_confirm_shipping', N'Versand bestätigen'),
        (N'ro', N'btn_confirm_shipping', N'Confirmă Livrarea'),
        (N'sv', N'btn_confirm_shipping', N'Bekräfta Leverans'),

        (N'it', N'select_row_first', N'Seleziona una riga per confermare'),
        (N'en', N'select_row_first', N'Select a row to confirm'),
        (N'de', N'select_row_first', N'Wählen Sie eine Zeile zur Bestätigung'),
        (N'ro', N'select_row_first', N'Selectați un rând pentru confirmare'),
        (N'sv', N'select_row_first', N'Välj en rad att bekräfta'),

        (N'it', N'shipment_pending_count', N'{0} spedizione/i urgente/i in attesa di conferma'),
        (N'en', N'shipment_pending_count', N'{0} urgent shipment(s) pending confirmation'),
        (N'de', N'shipment_pending_count', N'{0} dringende Lieferung(en) warten auf Bestätigung'),
        (N'ro', N'shipment_pending_count', N'{0} expediere(i) urgentă(e) în așteptarea confirmării'),
        (N'sv', N'shipment_pending_count', N'{0} akut(a) leverans(er) väntar på bekräftelse'),

        (N'it', N'shipment_qty_discrepancy', N'Attenzione: la quantità confermata ({0}) differisce dalla quantità richiesta ({1}) - differenza: {2}. Continuare con la conferma?'),
        (N'en', N'shipment_qty_discrepancy', N'Warning: confirmed quantity ({0}) differs from requested quantity ({1}) - difference: {2}. Continue?'),
        (N'de', N'shipment_qty_discrepancy', N'Achtung: Die bestätigte Menge ({0}) unterscheidet sich von der angeforderten Menge ({1}) - Differenz: {2}. Fortfahren?'),
        (N'ro', N'shipment_qty_discrepancy', N'Atenție: cantitatea confirmată ({0}) diferă de cantitatea solicitată ({1}) - diferență: {2}. Continuați?'),
        (N'sv', N'shipment_qty_discrepancy', N'Varning: bekräftad kvantitet ({0}) skiljer sig från begärd kvantitet ({1}) - skillnad: {2}. Fortsätt?'),

        (N'it', N'shipment_confirmed_ok', N'Spedizione confermata con successo.'),
        (N'en', N'shipment_confirmed_ok', N'Shipment confirmed successfully.'),
        (N'de', N'shipment_confirmed_ok', N'Lieferung erfolgreich bestätigt.'),
        (N'ro', N'shipment_confirmed_ok', N'Expedierea a fost confirmată cu succes.'),
        (N'sv', N'shipment_confirmed_ok', N'Leveransen har bekräftats.'),

        -- Colonne dinamiche TreeView (col_{col.lower()})
        (N'it', N'col_productionorder', N'Ordine Prod.'),
        (N'en', N'col_productionorder', N'Production Order'),
        (N'de', N'col_productionorder', N'Produktionsauftrag'),
        (N'ro', N'col_productionorder', N'Comandă Producție'),
        (N'sv', N'col_productionorder', N'Produktionsorder'),

        (N'it', N'col_sonumber', N'Ord. Vendita'),
        (N'en', N'col_sonumber', N'Sales Order'),
        (N'de', N'col_sonumber', N'Verkaufsauftrag'),
        (N'ro', N'col_sonumber', N'Comandă Vânzare'),
        (N'sv', N'col_sonumber', N'Försäljningsorder'),

        (N'it', N'col_itemcode', N'Codice'),
        (N'en', N'col_itemcode', N'Item Code'),
        (N'de', N'col_itemcode', N'Artikelcode'),
        (N'ro', N'col_itemcode', N'Cod Articol'),
        (N'sv', N'col_itemcode', N'Artikelkod'),

        (N'it', N'col_itemname', N'Prodotto'),
        (N'en', N'col_itemname', N'Product'),
        (N'de', N'col_itemname', N'Produkt'),
        (N'ro', N'col_itemname', N'Produs'),
        (N'sv', N'col_itemname', N'Produkt'),

        (N'it', N'col_datetoship', N'Data Spedizione'),
        (N'en', N'col_datetoship', N'Ship Date'),
        (N'de', N'col_datetoship', N'Versanddatum'),
        (N'ro', N'col_datetoship', N'Data Expedierii'),
        (N'sv', N'col_datetoship', N'Leveransdatum'),

        (N'it', N'col_qtyrequested', N'Qtà Rich.'),
        (N'en', N'col_qtyrequested', N'Requested Qty'),
        (N'de', N'col_qtyrequested', N'Angeforderte Menge'),
        (N'ro', N'col_qtyrequested', N'Cant. Solicitată'),
        (N'sv', N'col_qtyrequested', N'Efterfrågad kvantitet'),

        (N'it', N'col_producedqty', N'Qtà Prodotta'),
        (N'en', N'col_producedqty', N'Produced Qty'),
        (N'de', N'col_producedqty', N'Produzierte Menge'),
        (N'ro', N'col_producedqty', N'Cant. Produsă'),
        (N'sv', N'col_producedqty', N'Producerad kvantitet'),

        (N'it', N'col_remainoverpo', N'Rimanenti PO'),
        (N'en', N'col_remainoverpo', N'Remaining on PO'),
        (N'de', N'col_remainoverpo', N'Rest auf Produktionsauftrag'),
        (N'ro', N'col_remainoverpo', N'Rămas pe Comanda de Producție'),
        (N'sv', N'col_remainoverpo', N'Återstående på PO'),

        (N'it', N'col_shipto', N'Destinazione'),
        (N'en', N'col_shipto', N'Destination'),
        (N'de', N'col_shipto', N'Zielort'),
        (N'ro', N'col_shipto', N'Destinație'),
        (N'sv', N'col_shipto', N'Destination'),

        (N'it', N'col_addedby', N'Inserito Da'),
        (N'en', N'col_addedby', N'Added By'),
        (N'de', N'col_addedby', N'Eingefügt von'),
        (N'ro', N'col_addedby', N'Adăugat de'),
        (N'sv', N'col_addedby', N'Tillagt av'),

        -- ===== MONITOR POPUP =====
        (N'it', N'shipment_popup_title', N'SPEDIZIONI URGENTI - in attesa di conferma'),
        (N'en', N'shipment_popup_title', N'URGENT SHIPMENTS - pending confirmation'),
        (N'de', N'shipment_popup_title', N'DRINGENDE LIEFERUNGEN - Bestätigung ausstehend'),
        (N'ro', N'shipment_popup_title', N'EXPEDIERI URGENTE - în așteptare confirmare'),
        (N'sv', N'shipment_popup_title', N'AKUTA LEVERANSER - väntar på bekräftelse'),

        (N'it', N'shipment_popup_header', N'SPEDIZIONI URGENTI NON CONFERMATE'),
        (N'en', N'shipment_popup_header', N'URGENT SHIPMENTS NOT CONFIRMED'),
        (N'de', N'shipment_popup_header', N'DRINGENDE LIEFERUNGEN NICHT BESTÄTIGT'),
        (N'ro', N'shipment_popup_header', N'EXPEDIERI URGENTE NECONFIRMATE'),
        (N'sv', N'shipment_popup_header', N'AKUTA LEVERANSER EJ BEKRÄFTADE'),

        (N'it', N'shipment_popup_subheader', N'Aprire la finestra Conferma Shipping per registrare la conferma.'),
        (N'en', N'shipment_popup_subheader', N'Open the Confirm Shipping window to register confirmation.'),
        (N'de', N'shipment_popup_subheader', N'Öffnen Sie das Fenster Versand bestätigen, um die Bestätigung zu erfassen.'),
        (N'ro', N'shipment_popup_subheader', N'Deschideți fereastra Confirmă Livrarea pentru a înregistra confirmarea.'),
        (N'sv', N'shipment_popup_subheader', N'Öppna fönstret Bekräfta Leverans för att registrera bekräftelsen.'),

        (N'it', N'shipment_popup_btn_open', N'Apri Conferma Shipping'),
        (N'en', N'shipment_popup_btn_open', N'Open Confirm Shipping'),
        (N'de', N'shipment_popup_btn_open', N'Versand bestätigen öffnen'),
        (N'ro', N'shipment_popup_btn_open', N'Deschide Confirmă Livrarea'),
        (N'sv', N'shipment_popup_btn_open', N'Öppna Bekräfta Leverans')
    ) AS X([LanguageCode], [TranslationKey], [TranslationValue])
)
INSERT INTO [dbo].[AppTranslations] ([LanguageCode], [TranslationKey], [TranslationValue])
SELECT T.[LanguageCode], T.[TranslationKey], T.[TranslationValue]
FROM T
WHERE NOT EXISTS (
    SELECT 1
    FROM [dbo].[AppTranslations] A
    WHERE A.[LanguageCode] = T.[LanguageCode]
      AND A.[TranslationKey] = T.[TranslationKey]
);
GO
