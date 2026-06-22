# -*- coding: utf-8 -*-
"""
insert_shipment_confirmation_translations.py
Inserisce le chiavi di traduzione della form "Conferma Spedizioni" (v2,
orders/shipment_confirmation_window.py) in Traceability_rs.dbo.AppTranslations
in 5 lingue: it, en, ro, de, sv. Idempotente (salta le chiavi gia' presenti).

Run:  python insert_shipment_confirmation_translations.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from database_config import DatabaseConfig

# (key, it, en, ro, de, sv)
TRANSLATIONS = [
    ('shipment_confirm_title',
     'Conferma Spedizioni Urgenti', 'Confirm Urgent Shipments',
     'Confirmare Expedieri Urgente', 'Dringende Sendungen bestätigen',
     'Bekräfta brådskande leveranser'),
    ('shipment_confirm_header',
     'Spedizioni Urgenti - Conferma su Pallet', 'Urgent Shipments - Pallet Confirmation',
     'Expedieri Urgente - Confirmare pe Palet', 'Dringende Sendungen - Palettenbestätigung',
     'Brådskande leveranser - Pallbekräftelse'),
    ('btn_refresh', 'Aggiorna', 'Refresh', 'Reîmprospătare', 'Aktualisieren', 'Uppdatera'),
    ('btn_recover_shipment',
     'Recupera spedizione...', 'Retrieve shipment...', 'Recuperare expediere...',
     'Sendung abrufen...', 'Hämta leverans...'),
    ('shipment_date_label', 'Data spedizione:', 'Shipment date:', 'Data expedierii:',
     'Versanddatum:', 'Leveransdatum:'),
    ('mode_correction', "MODALITA' CORREZIONE", 'CORRECTION MODE', 'MOD CORECTIE',
     'KORREKTURMODUS', 'KORRIGERINGSLÄGE'),
    ('shipment_n', 'Spedizione N. {0}  [{1}]', 'Shipment No. {0}  [{1}]',
     'Expediere Nr. {0}  [{1}]', 'Sendung Nr. {0}  [{1}]', 'Leverans nr {0}  [{1}]'),
    ('filters', 'Filtri', 'Filters', 'Filtre', 'Filter', 'Filter'),
    ('filter_order', 'Ordine:', 'Order:', 'Comandă:', 'Auftrag:', 'Order:'),
    ('filter_product', 'Prodotto:', 'Product:', 'Produs:', 'Produkt:', 'Produkt:'),
    ('btn_filter', 'Filtra', 'Filter', 'Filtrează', 'Filtern', 'Filtrera'),
    ('btn_clear', 'Pulisci', 'Clear', 'Șterge', 'Löschen', 'Rensa'),
    ('orders_to_ship', 'Ordini da spedire', 'Orders to ship', 'Comenzi de expediat',
     'Zu versendende Aufträge', 'Order att skicka'),

    # colonne griglia ordini
    ('ocol_productionorder', 'Ordine Prod.', 'Prod. Order', 'Comandă Prod.',
     'Prod.-Auftrag', 'Prod.order'),
    ('ocol_customer', 'Cliente', 'Customer', 'Client', 'Kunde', 'Kund'),
    ('ocol_sonumber', 'Ord. Vendita', 'Sales Order', 'Comandă Vânzare',
     'Verkaufsauftrag', 'Försäljningsorder'),
    ('ocol_itemcode', 'Codice', 'Code', 'Cod', 'Code', 'Kod'),
    ('ocol_itemname', 'Prodotto', 'Product', 'Produs', 'Produkt', 'Produkt'),
    ('ocol_datetoship', 'Data Sped.', 'Ship Date', 'Data Exp.', 'Versanddatum', 'Lev.datum'),
    ('ocol_qtytoship', 'Qta da Sped.', 'Qty to Ship', 'Cant. de Exp.',
     'Zu versenden', 'Ant. att skicka'),
    ('ocol_confirmed', 'Confermato', 'Confirmed', 'Confirmat', 'Bestätigt', 'Bekräftad'),
    ('ocol_residual', 'Residuo', 'Remaining', 'Rămas', 'Restmenge', 'Återstående'),

    ('add_pallet', 'Aggiungi pallet alla spedizione', 'Add pallet to shipment',
     'Adaugă palet la expediere', 'Palette zur Sendung hinzufügen', 'Lägg till pall i leverans'),
    ('pallet_code', 'Codice Pallet:', 'Pallet Code:', 'Cod Palet:', 'Palettencode:', 'Pallkod:'),
    ('shipped_qty', 'Qta spedita:', 'Shipped qty:', 'Cant. expediată:',
     'Versandte Menge:', 'Skickad antal:'),
    ('btn_add_to_shipment', 'Aggiungi a spedizione', 'Add to shipment', 'Adaugă la expediere',
     'Zur Sendung hinzufügen', 'Lägg till i leverans'),
    ('shipment_pallets', 'Pallet della spedizione', 'Shipment pallets', 'Paleți expediere',
     'Sendungspaletten', 'Leveranspallar'),

    # colonne griglia pallet
    ('pcol_palletcode', 'Pallet', 'Pallet', 'Palet', 'Palette', 'Pall'),
    ('pcol_productionorder', 'Ordine Prod.', 'Prod. Order', 'Comandă Prod.',
     'Prod.-Auftrag', 'Prod.order'),
    ('pcol_itemcode', 'Codice', 'Code', 'Cod', 'Code', 'Kod'),
    ('pcol_itemname', 'Prodotto', 'Product', 'Produs', 'Produkt', 'Produkt'),
    ('pcol_qty', 'Qta', 'Qty', 'Cant.', 'Menge', 'Antal'),

    ('btn_edit_pallet', 'Modifica qta', 'Edit qty', 'Modifică cant.',
     'Menge bearbeiten', 'Redigera antal'),
    ('btn_delete_pallet', 'Elimina', 'Delete', 'Șterge', 'Löschen', 'Ta bort'),
    ('btn_finalize', 'Finalizza spedizione', 'Finalize shipment', 'Finalizează expedierea',
     'Sendung abschließen', 'Slutför leverans'),
    ('btn_save_corrections', 'Salva correzioni e ristampa', 'Save corrections and reprint',
     'Salvează corecțiile și reimprimă', 'Korrekturen speichern und neu drucken',
     'Spara korrigeringar och skriv ut igen'),

    ('orders_count', '{0} ordini da spedire', '{0} orders to ship', '{0} comenzi de expediat',
     '{0} zu versendende Aufträge', '{0} order att skicka'),
    ('order_hint',
     'da spedire: {0} | confermato: {1} | residuo: {2}',
     'to ship: {0} | confirmed: {1} | remaining: {2}',
     'de expediat: {0} | confirmat: {1} | rămas: {2}',
     'zu versenden: {0} | bestätigt: {1} | Rest: {2}',
     'att skicka: {0} | bekräftat: {1} | kvar: {2}'),

    ('warning', 'Attenzione', 'Warning', 'Atenție', 'Achtung', 'Varning'),
    ('pallet_required', 'Inserire il codice pallet.', 'Enter the pallet code.',
     'Introduceți codul paletului.', 'Geben Sie den Palettencode ein.', 'Ange pallkoden.'),
    ('qty_invalid', 'Quantita non valida.', 'Invalid quantity.', 'Cantitate invalidă.',
     'Ungültige Menge.', 'Ogiltig kvantitet.'),
    ('qty_positive', 'La quantita deve essere maggiore di zero.',
     'Quantity must be greater than zero.', 'Cantitatea trebuie să fie mai mare ca zero.',
     'Die Menge muss größer als null sein.', 'Kvantiteten måste vara större än noll.'),
    ('confirm', 'Conferma', 'Confirm', 'Confirmare', 'Bestätigen', 'Bekräfta'),
    ('shipment_excess_warn',
     'Attenzione: con questa quantita il confermato ({0}) supera la quantita da spedire ({1}) di {2} pezzi.\n\nContinuare comunque?',
     'Warning: with this quantity the confirmed amount ({0}) exceeds the quantity to ship ({1}) by {2} pieces.\n\nContinue anyway?',
     'Atenție: cu această cantitate confirmatul ({0}) depășește cantitatea de expediat ({1}) cu {2} bucăți.\n\nContinuați oricum?',
     'Achtung: Mit dieser Menge übersteigt die bestätigte Menge ({0}) die zu versendende Menge ({1}) um {2} Stück.\n\nTrotzdem fortfahren?',
     'Varning: med denna kvantitet överstiger det bekräftade ({0}) kvantiteten att skicka ({1}) med {2} stycken.\n\nFortsätta ändå?'),
    ('info', 'Info', 'Info', 'Info', 'Info', 'Info'),
    ('select_pallet', 'Seleziona un pallet nella lista.', 'Select a pallet from the list.',
     'Selectați un palet din listă.', 'Wählen Sie eine Palette aus der Liste.',
     'Välj en pall i listan.'),
    ('error', 'Errore', 'Error', 'Eroare', 'Fehler', 'Fel'),
    ('new_qty', 'Nuova quantita:', 'New quantity:', 'Cantitate nouă:', 'Neue Menge:',
     'Ny kvantitet:'),
    ('ok', 'OK', 'OK', 'OK', 'OK', 'OK'),
    ('cancel', 'Annulla', 'Cancel', 'Anulare', 'Abbrechen', 'Avbryt'),
    ('delete_pallet_q', 'Eliminare questa riga pallet?', 'Delete this pallet row?',
     'Ștergeți acest rând de palet?', 'Diese Palettenzeile löschen?',
     'Ta bort denna pallrad?'),
    ('edit_qty_title', 'Modifica quantita', 'Edit quantity', 'Modifică cantitatea',
     'Menge bearbeiten', 'Redigera kvantitet'),
    ('no_pallets', 'Nessun pallet inserito nella spedizione.', 'No pallet added to the shipment.',
     'Niciun palet adăugat la expediere.', 'Keine Palette zur Sendung hinzugefügt.',
     'Ingen pall tillagd i leveransen.'),
    ('finalize_q',
     'Finalizzare la spedizione N. {0}?\nVerranno generati i documenti e inviata l\'email.',
     'Finalize shipment No. {0}?\nDocuments will be generated and the email sent.',
     'Finalizați expedierea Nr. {0}?\nVor fi generate documentele și trimis e-mailul.',
     'Sendung Nr. {0} abschließen?\nDokumente werden erstellt und die E-Mail gesendet.',
     'Slutför leverans nr {0}?\nDokument genereras och e-post skickas.'),
    ('success', 'Successo', 'Success', 'Succes', 'Erfolg', 'Lyckades'),
    ('shipment_finalized',
     'Spedizione finalizzata. Documenti generati ed email in invio.',
     'Shipment finalized. Documents generated and email being sent.',
     'Expediere finalizată. Documente generate și e-mail în curs de trimitere.',
     'Sendung abgeschlossen. Dokumente erstellt und E-Mail wird gesendet.',
     'Leverans slutförd. Dokument genererade och e-post skickas.'),
    ('corr_empty_q',
     'La spedizione non ha pallet. Salvare comunque la correzione?',
     'The shipment has no pallets. Save the correction anyway?',
     'Expedierea nu are paleți. Salvați corecția oricum?',
     'Die Sendung hat keine Paletten. Korrektur trotzdem speichern?',
     'Leveransen har inga pallar. Spara korrigeringen ändå?'),
    ('corr_saved',
     'Correzione salvata. Documenti rigenerati ed email di correzione in invio.',
     'Correction saved. Documents regenerated and correction email being sent.',
     'Corecție salvată. Documente regenerate și e-mail de corecție în curs de trimitere.',
     'Korrektur gespeichert. Dokumente neu erstellt und Korrektur-E-Mail wird gesendet.',
     'Korrigering sparad. Dokument återskapade och korrigerings-e-post skickas.'),
    ('pdf_error', 'Errore nella generazione dei documenti:\n{0}',
     'Error generating documents:\n{0}', 'Eroare la generarea documentelor:\n{0}',
     'Fehler beim Erstellen der Dokumente:\n{0}', 'Fel vid generering av dokument:\n{0}'),
    ('recover_title', 'Recupera spedizione', 'Retrieve shipment', 'Recuperare expediere',
     'Sendung abrufen', 'Hämta leverans'),
    ('date_from', 'Dal:', 'From:', 'De la:', 'Von:', 'Från:'),
    ('date_to', 'Al:', 'To:', 'Până la:', 'Bis:', 'Till:'),
    ('btn_search', 'Cerca', 'Search', 'Caută', 'Suchen', 'Sök'),
    ('btn_load', 'Carica per correzione', 'Load for correction', 'Încarcă pentru corecție',
     'Zur Korrektur laden', 'Ladda för korrigering'),
    ('loaded_shipment', 'Caricata spedizione N. {0} per correzione',
     'Shipment No. {0} loaded for correction', 'Expediere Nr. {0} încărcată pentru corecție',
     'Sendung Nr. {0} zur Korrektur geladen', 'Leverans nr {0} laddad för korrigering'),

    # colonne dialog recupero
    ('rcol_id', 'N.', 'No.', 'Nr.', 'Nr.', 'Nr'),
    ('rcol_date', 'Data', 'Date', 'Data', 'Datum', 'Datum'),
    ('rcol_status', 'Stato', 'Status', 'Stare', 'Status', 'Status'),
    ('rcol_pallets', 'Pallet', 'Pallets', 'Paleți', 'Paletten', 'Pallar'),
    ('rcol_qty', 'Pezzi', 'Pieces', 'Bucăți', 'Stück', 'Stycken'),
    ('rcol_closedby', 'Chiusa da', 'Closed by', 'Închisă de', 'Geschlossen von', 'Stängd av'),

    # select riga (riuso pattern altrove ma garantiamo presenza)
    ('select_row_first', 'Seleziona una riga per confermare', 'Select a row to confirm',
     'Selectați un rând pentru confirmare', 'Wählen Sie eine Zeile zum Bestätigen',
     'Välj en rad att bekräfta'),
]

LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    inserted = skipped = 0
    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            val = row[i + 1]
            cur.execute(
                "SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                "WHERE LanguageCode = ? AND TranslationKey = ?",
                (lang, key),
            )
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "INSERT INTO Traceability_rs.dbo.AppTranslations "
                    "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                    (lang, key, val),
                )
                inserted += 1
            else:
                skipped += 1
    conn.commit()
    conn.close()
    print(f"[OK] Shipment confirmation translations - Inserite: {inserted}, "
          f"Saltate (gia' presenti): {skipped}")


if __name__ == '__main__':
    main()
