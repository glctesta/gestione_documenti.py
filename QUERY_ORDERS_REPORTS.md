# Query SQL utilizzate in orders_reports_window.py

## 1. Query Principale: get_sale_orders_for_matching()

**Metodo**: `OrdersManager.get_sale_orders_for_matching(filters)`  
**File**: `orders/orders_manager.py` (linee 281-380)

### Query SQL:
```sql
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
    -- Filtri opzionali:
    -- AND d.SONumber LIKE :so_number
    -- AND d.CustomerName LIKE :customer
    -- AND (d.ItemCode LIKE :product OR d.ItemName LIKE :product)
    -- AND d.ShipDateRequest >= :date_from
    -- AND d.ShipDateRequest <= :date_to
GROUP BY 
    d.[DynamicSaleOrderId],
    d.[SONumber],
    d.[CustomerName],
    d.[ItemCode],
    d.[ItemName],
    d.[ShipDateRequest],
    d.[QtyOrder]
    -- Filtro stato assegnazione (opzionale):
    -- HAVING d.[QtyOrder] = ISNULL(SUM(po.Qty), 0)  -- fully_assigned
    -- HAVING d.[QtyOrder] > ISNULL(SUM(po.Qty), 0)  -- not_fully_assigned
ORDER BY d.SONumber, d.ShipDateRequest
```

### Tabelle utilizzate:
- **[Traceability_RS].[dyn].[DynamicSaleOrders]** - Ordini di vendita
- **[Traceability_RS].[dyn].[DynamicProductionOrders]** - Ordini di produzione associati

### Campi restituiti:
1. `DynamicSaleOrderId` - ID ordine
2. `SONumber` - Numero ordine vendita
3. `CustomerName` - Nome cliente
4. `ItemCode` - Codice prodotto
5. `ItemName` - Nome prodotto
6. `ShipDateRequest` - Data spedizione richiesta
7. `QtyOrder` - Quantità ordinata
8. `QtyAssigned` - Quantità assegnata (somma da ordini produzione)

### Filtri disponibili:
- `so_number` - Filtra per numero ordine (LIKE)
- `customer` - Filtra per cliente (LIKE)
- `product` - Filtra per codice o nome prodotto (LIKE)
- `date_from` - Data spedizione da (>=)
- `date_to` - Data spedizione a (<=)
- `assignment_status`:
  - `'fully_assigned'` - Solo ordini completamente assegnati
  - `'not_fully_assigned'` - Solo ordini non completamente assegnati
  - `None` - Tutti gli ordini

---

## 2. Utilizzo nei Report

### A. Rapporto Riepilogativo (_generate_summary_report)
**Filtri utilizzati**:
```python
filters = {
    'date_from': date_from,  # Da DateEntry
    'date_to': date_to        # Da DateEntry
}
orders = self.orders_manager.get_sale_orders_for_matching(filters)
```

### B. Rapporto Per Cliente (_generate_customer_report)
**Filtri utilizzati**:
```python
filters = {
    'customer': selected_customer  # Da Combobox
}
orders = self.orders_manager.get_sale_orders_for_matching(filters)
```

### C. Rapporto Associazioni (_generate_associations_report)
**Filtri utilizzati**:
```python
filters = {
    'so_number': so_number  # Da Entry (opzionale)
}
orders = self.orders_manager.get_sale_orders_for_matching(filters)
```

### D. Rapporto Carichi di Lavoro (_generate_workload_report)
**Nessun filtro** - Recupera tutti gli ordini e li aggrega per prodotto.

---

## 3. Possibili Cause di "Nessun Dato"

### ✅ Verifiche da fare:

1. **Tabelle vuote**:
   ```sql
   SELECT COUNT(*) FROM [Traceability_RS].[dyn].[DynamicSaleOrders];
   SELECT COUNT(*) FROM [Traceability_RS].[dyn].[DynamicProductionOrders];
   ```

2. **Range date troppo restrittivo**:
   - Verifica che ci siano ordini nel range di date selezionato
   ```sql
   SELECT MIN(ShipDateRequest), MAX(ShipDateRequest) 
   FROM [Traceability_RS].[dyn].[DynamicSaleOrders];
   ```

3. **Filtro cliente non corrispondente**:
   - Verifica i nomi esatti dei clienti
   ```sql
   SELECT DISTINCT CustomerName 
   FROM [Traceability_RS].[dyn].[DynamicSaleOrders]
   ORDER BY CustomerName;
   ```

4. **Errori nella query**:
   - Controlla i log per errori SQL
   - Verifica che le tabelle esistano e abbiano i permessi corretti

---

## 4. Query di Test Diretta

Per testare se ci sono dati disponibili:

```sql
-- Test base: conta ordini totali
SELECT COUNT(*) as TotaleOrdini
FROM [Traceability_RS].[dyn].[DynamicSaleOrders];

-- Test con dettagli: primi 10 ordini
SELECT TOP 10
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
GROUP BY 
    d.[SONumber],
    d.[CustomerName],
    d.[ItemCode],
    d.[ItemName],
    d.[ShipDateRequest],
    d.[QtyOrder]
ORDER BY d.SONumber;
```

---

## 5. Soluzione Rapida

Se le tabelle sono vuote, devi prima caricare gli ordini usando:
- **Menu**: Ordini → Carica Ordini
- **Finestra**: `load_orders_window.py`
- **Funzione**: Importa ordini da Excel nella tabella `DynamicSaleOrders`
