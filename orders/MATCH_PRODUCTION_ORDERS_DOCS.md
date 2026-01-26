# Accoppiamento Ordini di Vendita e Produzione - Documentazione

## Panoramica
Implementata funzionalità completa per accoppiare gli ordini di vendita (DynamicSaleOrders) con gli ordini di produzione (DynamicProductionOrders).

## File Creati/Modificati

### 1. **match_production_orders_window.py** (NUOVO)
Nuova form con interfaccia divisa in due pannelli:

#### Pannello Sinistro - Ordini di Vendita
- **Filtri disponibili:**
  - Numero Ordine (SO Number)
  - Cliente (CustomerName)
  - Prodotto (ItemCode/ItemName)
  - Range di date (ShipDateRequest)

- **Visualizzazione:**
  - Treeview con colonne: SO Number, Cliente, Prodotto, Data Spedizione, Qtà Ordine, Qtà Assegnata, Qtà Rimanente
  - Ordini completamente assegnati evidenziati in verde
  - Ordinamento per SONumber e ShipDateRequest

#### Pannello Destro - Associazione
- **Info ordine selezionato:** Mostra riepilogo ordine di vendita attivo
- **Combo ordini produzione:** Lista ordini PR* non ancora assegnati
- **Campo quantità:** Auto-popolato con la quantità rimanente
- **Lista associazioni esistenti:** Mostra tutti gli ordini di produzione già associati
- **Elimina associazione:** Possibilità di rimuovere associazioni errate

### 2. **orders_manager.py** (MODIFICATO)
Aggiunti 5 nuovi metodi:

#### `get_sale_orders_for_matching(filters=None)`
```sql
-- Recupera ordini di vendita con calcolo quantità assegnate
SELECT  
    d.[DynamicSaleOrderId],
    d.[SONumber],
    d.[CustomerName],
    d.[ItemCode],
    d.[ItemName],
    d.[ShipDateRequest],
    d.[QtyOrder],
    ISNULL(SUM(po.Qty), 0) as QtyAssigned
FROM [Traceability_RS].[dyn].[DynamicSaleOrders] d
LEFT JOIN [Traceability_RS].[dyn].[DynamicProductionOrders] po
    ON d.DynamicSaleOrderId = po.DynamicSaleOrderId
WHERE 1=1
    [+ filtri dinamici]
GROUP BY ...
ORDER BY d.SONumber, d.ShipDateRequest
```

**Filtri supportati:**
- `so_number`: LIKE %value%
- `customer`: LIKE %value%
- `product`: LIKE su ItemCode O ItemName
- `date_from`: >= data
- `date_to`: <= data

#### `get_available_production_orders()`
```sql
-- Recupera ordini produzione non ancora assegnati
SELECT 
    o.IdOrder, 
    o.OrderNumber, 
    p.ProductCode + ' [' + p.ProductName + ']' AS Product  
FROM [Traceability_RS].dbo.orders o 
LEFT JOIN [Traceability_RS].dbo.Products p 
    ON p.IDProduct = o.IDProduct
WHERE o.IdOrder NOT IN (
    SELECT IdOrder 
    FROM [Traceability_RS].[dyn].[DynamicProductionOrders]
)
AND LEFT(o.OrderNumber, 2) = 'PR'
ORDER BY o.OrderNumber
```

#### `create_production_association(association_data)`
```sql
-- Crea associazione
INSERT INTO [Traceability_RS].[dyn].[DynamicProductionOrders]
(DynamicSaleOrderId, IdOrder, Qty, DateIn)
VALUES
(:dynamic_sale_order_id, :id_order, :qty, GETDATE());
```

**Validazioni:**
- Verifica che la quantità sia > 0
- Verifica che la quantità non superi quella rimanente dell'ordine di vendita

#### `get_production_associations(dynamic_sale_order_id)`
```sql
-- Recupera associazioni esistenti per un ordine di vendita
SELECT 
    po.DynamicProductionOrderID,
    po.IdOrder,
    o.OrderNumber,
    p.ProductCode + ' [' + p.ProductName + ']' AS Product,
    po.Qty,
    po.DateIn
FROM [Traceability_RS].[dyn].[DynamicProductionOrders] po
LEFT JOIN [Traceability_RS].dbo.orders o ON o.IdOrder = po.IdOrder
LEFT JOIN [Traceability_RS].dbo.Products p ON p.IDProduct = o.IDProduct
WHERE po.DynamicSaleOrderId = :dynamic_sale_order_id
ORDER BY po.DateIn DESC
```

#### `delete_production_association(dynamic_production_order_id)`
```sql
-- Elimina associazione
DELETE FROM [Traceability_RS].[dyn].[DynamicProductionOrders]
WHERE DynamicProductionOrderID = :id
```

### 3. **load_orders_window.py** (MODIFICATO)
- Aggiunto bottone "Accoppia Ordini Produzione"
- Aggiunto metodo `_match_production_orders()` che apre la nuova form

## Logica di Business

### Regole di Associazione
1. **Un ordine di vendita può avere più ordini di produzione**
2. **La somma delle quantità assegnate non può superare QtyOrder**
3. **Un ordine di produzione può essere assegnato solo UNA volta**
4. **Solo ordini con OrderNumber che inizia con 'PR' sono disponibili**

### Flusso di Lavoro
1. Utente apre "Carica Ordini"
2. Clicca su "Accoppia Ordini Produzione"
3. Applica filtri per trovare l'ordine di vendita desiderato
4. Seleziona l'ordine di vendita → visualizza info e associazioni esistenti
5. Seleziona ordine di produzione dal combo
6. Inserisce/modifica quantità (default = quantità rimanente)
7. Clicca "Aggiungi Associazione"
8. Sistema verifica validità e inserisce nella tabella DynamicProductionOrders
9. Liste si aggiornano automaticamente

### Gestione Errori
- Messaggi di warning se nessun ordine selezionato
- Validazione quantità (deve essere > 0 e <= rimanente)
- Gestione errori database con log dettagliato
- Transazioni SQL con rollback automatico in caso di errore

## Chiavi di Traduzione Necessarie

Aggiungere alla tabella AppTranslations:

```sql
-- Italiano
INSERT INTO [Traceability_RS].[dbo].[AppTranslations] (KeyName, IT) VALUES
('match_production_orders_title', 'Accoppia Ordini di Produzione'),
('btn_match_production_orders', 'Accoppia Ordini Produzione'),
('sale_orders', 'Ordini di Vendita'),
('filters', 'Filtri'),
('so_number', 'N. Ordine:'),
('customer', 'Cliente:'),
('product', 'Prodotto:'),
('date_from', 'Data Da:'),
('date_to', 'Data A:'),
('btn_apply_filter', 'Applica Filtri'),
('btn_reset_filter', 'Resetta Filtri'),
('col_qty_assigned', 'Qtà Assegnata'),
('col_qty_remaining', 'Qtà Rimanente'),
('association', 'Associazione Ordini'),
('selected_sale_order', 'Ordine di Vendita Selezionato'),
('no_selection', 'Nessun ordine selezionato'),
('add_production_order', 'Aggiungi Ordine di Produzione'),
('production_order', 'Ordine di Produzione:'),
('quantity', 'Quantità:'),
('btn_add_association', 'Aggiungi Associazione'),
('existing_associations', 'Associazioni Esistenti'),
('col_production_order', 'Ordine Produzione'),
('col_date_in', 'Data Ins.'),
('btn_delete_association', 'Elimina Associazione'),
('select_sale_order_first', 'Seleziona prima un ordine di vendita'),
('select_production_order', 'Seleziona un ordine di produzione'),
('invalid_quantity', 'Quantità non valida'),
('qty_exceeds_remaining', 'La quantità eccede quella rimanente'),
('association_created', 'Associazione creata con successo'),
('select_association', 'Seleziona un\'associazione da eliminare'),
('confirm_delete_association', 'Confermare eliminazione associazione?'),
('association_deleted', 'Associazione eliminata');

-- Inglese (EN)
-- Rumeno (RO)
-- Tedesco (DE)
-- Svedese (SV)
```

## Testing Checklist

### Test Funzionali
- [ ] Apertura finestra da "Carica Ordini"
- [ ] Caricamento ordini di vendita
- [ ] Filtro per numero ordine
- [ ] Filtro per cliente
- [ ] Filtro per prodotto
- [ ] Filtro per range date
- [ ] Reset filtri
- [ ] Selezione ordine di vendita
- [ ] Visualizzazione info ordine
- [ ] Caricamento combo ordini produzione
- [ ] Calcolo quantità rimanente
- [ ] Validazione quantità > 0
- [ ] Validazione quantità <= rimanente
- [ ] Creazione associazione
- [ ] Visualizzazione associazioni esistenti
- [ ] Eliminazione associazione
- [ ] Evidenziazione ordini completati (verde)
- [ ] Refresh automatico dopo operazioni

### Test Database
- [ ] INSERT in DynamicProductionOrders
- [ ] SELECT con GROUP BY per quantità assegnate
- [ ] DELETE associazione
- [ ] Transazioni con rollback
- [ ] Handling errori connessione

### Test UI
- [ ] Responsive layout con PanedWindow
- [ ] Scrollbar treeview
- [ ] DateEntry widget funzionante
- [ ] Combo box popolato correttamente
- [ ] Messaggi di errore/successo
- [ ] Traduzioni (se disponibili)

## Note Implementative

### Dipendenze
- `tkcalendar`: Già presente nel progetto
- `SQLAlchemy`: Già configurato
- Tutte le altre dipendenze già disponibili

### Performance
- Le query utilizzano indici su:
  - DynamicSaleOrderId
  - IdOrder
  - SONumber
- GROUP BY ottimizzato per calcolo quantità
- LEFT JOIN per evitare perdita dati

### Sicurezza
- Parametrizzazione query SQL (protezione SQL injection)
- Validazione input lato client
- Gestione sessioni SQLAlchemy con chiusura automatica

## Prossimi Sviluppi Possibili
1. Export Excel delle associazioni
2. Report stampa ordini associati
3. Dashboard riepilogativa carichi di lavoro
4. Notifiche automatiche per ordini non assegnati
5. Gestione priorità ordini
