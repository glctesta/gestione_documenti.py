# -*- coding: utf-8 -*-
"""
insert_warehouse_shipping_translations.py
Traduzioni per la spedizione degli ordini finiti a magazzino
(orders_reports_window.py — righe "da abbinare", dialog abbinamento e correzione).
5 lingue (it, en, ro, de, sv). Idempotente: inserisce solo le chiavi mancanti.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('wh_legend_yellow',
     'Giallo = da abbinare (magazzino, senza ordine di vendita)',
     'Yellow = to match (warehouse, no sales order)',
     'Galben = de asociat (depozit, fără comandă de vânzare)',
     'Gelb = zuzuordnen (Lager, ohne Verkaufsauftrag)',
     'Gul = att matcha (lager, ingen försäljningsorder)'),
    ('wh_legend_red',
     'Rosso = urgente, merce già a magazzino',
     'Red = urgent, goods already in warehouse',
     'Roșu = urgent, marfă deja în depozit',
     'Rot = dringend, Ware bereits im Lager',
     'Röd = brådskande, varan redan i lager'),
    ('wh_hint_dblclick',
     '— Doppio click su una riga gialla per abbinarla a un ordine di vendita e inserire i dati, oppure usa il bottone:',
     '— Double-click a yellow row to match it to a sales order and enter the data, or use the button:',
     '— Dublu clic pe un rând galben pentru a-l asocia unei comenzi de vânzare și a introduce datele, sau folosește butonul:',
     '— Doppelklicken Sie auf eine gelbe Zeile, um sie einem Verkaufsauftrag zuzuordnen und die Daten einzugeben, oder verwenden Sie die Schaltfläche:',
     '— Dubbelklicka på en gul rad för att matcha den mot en försäljningsorder och ange data, eller använd knappen:'),
    ('wh_btn_open_match', '🔗 Abbina / Correggi', '🔗 Match / Correct',
     '🔗 Asociază / Corectează', '🔗 Zuordnen / Korrigieren', '🔗 Matcha / Korrigera'),
    ('wh_to_match_hint',
     'Ordine a magazzino da abbinare — doppio click (o bottone Abbina) per abbinare a un ordine di vendita o correggere il già spedito',
     'Warehouse order to match — double-click (or Match button) to link it to a sales order or correct the already-shipped quantity',
     'Comandă în depozit de asociat — dublu clic (sau butonul Asociază) pentru a o lega de o comandă de vânzare sau a corecta cantitatea deja expediată',
     'Lagerauftrag zuzuordnen — Doppelklick (oder Schaltfläche Zuordnen), um ihn mit einem Verkaufsauftrag zu verknüpfen oder die bereits versandte Menge zu korrigieren',
     'Lagerorder att matcha — dubbelklicka (eller Matcha-knappen) för att koppla den till en försäljningsorder eller korrigera redan skickad kvantitet'),
    ('wh_select_yellow',
     'Selezionare una riga gialla "da abbinare".', 'Select a yellow "to match" row.',
     'Selectați un rând galben „de asociat".', 'Wählen Sie eine gelbe Zeile „zuzuordnen".',
     'Välj en gul rad "att matcha".'),
    ('wh_match_title', 'Abbina ordine a magazzino', 'Match warehouse order',
     'Asociază comanda din depozit', 'Lagerauftrag zuordnen', 'Matcha lagerorder'),
    ('wh_available', 'Disponibile a magazzino', 'Available in warehouse',
     'Disponibil în depozit', 'Im Lager verfügbar', 'Tillgängligt i lager'),
    ('wh_btn_match', '✅ Abbina e crea regola', '✅ Match and create rule',
     '✅ Asociază și creează regula', '✅ Zuordnen und Regel erstellen',
     '✅ Matcha och skapa regel'),
    ('wh_btn_shipped', '📦 Già spedito (correzione)', '📦 Already shipped (correction)',
     '📦 Deja expediat (corecție)', '📦 Bereits versandt (Korrektur)',
     '📦 Redan skickat (korrigering)'),
    ('wh_no_so', 'Nessun ordine di vendita con questo prodotto',
     'No sales order for this product', 'Nicio comandă de vânzare pentru acest produs',
     'Kein Verkaufsauftrag für dieses Produkt', 'Ingen försäljningsorder för denna produkt'),
    ('wh_pick_so', 'Selezionare un ordine di vendita', 'Select a sales order',
     'Selectați o comandă de vânzare', 'Wählen Sie einen Verkaufsauftrag',
     'Välj en försäljningsorder'),
    ('wh_matched', 'Ordine abbinato e regola creata', 'Order matched and rule created',
     'Comandă asociată și regulă creată', 'Auftrag zugeordnet und Regel erstellt',
     'Order matchad och regel skapad'),
    ('wh_adj_missing',
     'Tabella correzioni non presente. Eseguire add_warehouse_shipped_adjustments.sql.',
     'Corrections table missing. Run add_warehouse_shipped_adjustments.sql.',
     'Tabelul de corecții lipsește. Executați add_warehouse_shipped_adjustments.sql.',
     'Korrekturtabelle fehlt. Führen Sie add_warehouse_shipped_adjustments.sql aus.',
     'Korrigeringstabellen saknas. Kör add_warehouse_shipped_adjustments.sql.'),
    ('wh_shipped_title', 'Già spedito — correzione', 'Already shipped — correction',
     'Deja expediat — corecție', 'Bereits versandt — Korrektur', 'Redan skickat — korrigering'),
    ('wh_shipped_qty', 'Quantità già spedita', 'Already-shipped quantity',
     'Cantitate deja expediată', 'Bereits versandte Menge', 'Redan skickad kvantitet'),
    ('wh_adj_saved', 'Correzione registrata', 'Correction saved',
     'Corecție înregistrată', 'Korrektur gespeichert', 'Korrigering sparad'),
    ('note', 'Nota', 'Note', 'Notă', 'Notiz', 'Anteckning'),
    # Etichetta voce di menu Aiuto > Manuali > Operazioni > Ordini
    ('manual_warehouse_shipping', 'Spedizioni da magazzino', 'Warehouse shipping',
     'Expedieri din depozit', 'Lagerversand', 'Lagerfrakt'),
]

LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    ins = skip = 0
    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            cur.execute("SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                        "WHERE LanguageCode = ? AND TranslationKey = ?", (lang, key))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO Traceability_rs.dbo.AppTranslations "
                            "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                            (lang, key, row[i + 1]))
                ins += 1
            else:
                skip += 1
    conn.commit()
    conn.close()
    print(f"[OK] Warehouse shipping translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
