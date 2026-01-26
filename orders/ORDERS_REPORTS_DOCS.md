# Modulo Rapporti Ordini - Documentazione

## Panoramica
Sistema completo di reporting per gli ordini dinamici con 4 tipologie di rapporti, visualizzazione KPI, e export Excel professionale.

## File Creati/Modificati

### 1. **orders_reports_window.py** (NUOVO)
Finestra con notebook a 4 tab per diversi tipi di rapporti.

---

## Tab 1: Riepilogo Generale

### Funzionalità
- **Filtri temporali:** Data Da / Data A
- **5 KPI Cards colorati:**
  - 🔵 Ordini Totali
  - 🟢 Ordini Aperti
  - 🟢 Ordini Completati
  - 🔴 Ordini in Ritardo
  - 🟣 Valore Totale (€)

### Treeview Dettagli
**Colonne:**
- N. Ordine
- Cliente
- Prodotto
- Data Spedizione
- Qtà Ordine
- Qtà Assegnata
- Qtà Rimanente
- **Stato** (Completato / In Corso / In Ritardo)
- Valore (€)

**Colorazione righe:**
- 🟢 Verde: Ordini completati (qty_remaining <= 0)
- 🟡 Giallo: Ordini in corso
- 🔴 Rosso: Ordini in ritardo (ship_date < oggi)

### Logica Calcoli
```python
# Stato ordine
if qty_remaining <= 0:
   stato = "Completato"
elif ship_date < oggi:
    stato = "In Ritardo"
else:
    stato = "In Corso"

# Valore ordine
valore = qty_order * unit_price
```

---

## Tab 2: Report per Cliente

### Funzionalità
- **Combo Clienti:** Lista clienti univoci da DB
- **Statistiche Cliente:**
  - Ordini Totali
  - Ordini Completati (con %)
  - Valore Totale

### Treeview Ordini Cliente
**Colonne:**
- N. Ordine
- Prodotto
- Data Spedizione
- Qtà
- Assegnata
- Stato
- Valore (€)

**Stesso schema colorazione del Tab 1**

### Query SQL
```sql
SELECT DISTINCT CustomerName
FROM [Traceability_RS].[dyn].[DynamicSaleOrders]
WHERE CustomerName IS NOT NULL
ORDER BY CustomerName
```

---

## Tab 3: Associazioni Produzione

### Funzionalità
- **Filtro per N. Ordine:** Filtro parziale LIKE
- **Vista completa associazioni**

### Treeview Associazioni
**Colonne:**
- Ordine Vendita
- Cliente
- Prodotto Vendita
- Ordine Produzione
- Prodotto Produzione
- Quantità
- Data Inserimento

### Query SQL
```sql
SELECT 
    dso.SONumber,
    dso.CustomerName,
    dso.ItemCode + ' [' + dso.ItemName + ']' AS SaleProduct,
    o.OrderNumber AS ProductionOrder,
    p.ProductCode + ' [' + p.ProductName + ']' AS ProductionProduct,
    dpo.Qty,
    dpo.DateIn
FROM [Traceability_RS].[dyn].[DynamicProductionOrders] dpo
INNER JOIN [Traceability_RS].[dyn].[DynamicSaleOrders] dso
    ON dpo.DynamicSaleOrderId = dso.DynamicSaleOrderId
LEFT JOIN [Traceability_RS].dbo.orders o
    ON o.IdOrder = dpo.IdOrder
LEFT JOIN [Traceability_RS].dbo.Products p
    ON p.IDProduct = o.IDProduct
WHERE 1=1
ORDER BY dso.SONumber, dpo.DateIn DESC
```

---

## Tab 4: Carichi di Lavoro

### Funzionalità
- **Aggregazione per prodotto**
- **Vista carico di lavoro complessivo**

### Treeview Carichi
**Colonne:**
- Prodotto
- Qtà Totale Ordinata
- Qtà Totale Assegnata
- Qtà Rimanente
- N. Ordini
- Valore Medio

**Ordinamento:** Per Qtà Rimanente DESC (priorità produzione)

### Query SQL
```sql
SELECT 
    dso.ItemCode + ' [' + dso.ItemName + ']' AS Product,
    SUM(dso.QtyOrder) AS TotalOrdered,
    ISNULL(SUM(dpo.Qty), 0) AS TotalAssigned,
    SUM(dso.QtyOrder) - ISNULL(SUM(dpo.Qty), 0) AS TotalRemaining,
    COUNT(DISTINCT dso.DynamicSaleOrderId) AS OrdersCount,
    AVG(dso.UnitPrice * dso.QtyOrder) AS AvgValue
FROM [Traceability_RS].[dyn].[DynamicSaleOrders] dso
LEFT JOIN [Traceability_RS].[dyn].[DynamicProductionOrders] dpo
    ON dso.DynamicSaleOrderId = dpo.DynamicSaleOrderId
GROUP BY dso.ItemCode, dso.ItemName
ORDER BY TotalRemaining DESC
```

---

## Funzionalità Export Excel

### Caratteristiche
- **Formato professionale** con stili
- **Header colorato** (blu scuro) con testo bianco in grassetto
- **Bordi** su tutte le celle
- **Auto-dimensionamento colonne** (max 50 caratteri)
- **Allineamento** header centrato, dati a sinistra

### Codice Stili Excel
```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
```

### Salvataggio
- Dialog nativo Windows per selezione percorso
- Default extension: `.xlsx`
- Messaggio conferma con percorso file

---

## Metodi OrdersManager Aggiunti

### 1. `get_customers_list()` → List[str]
Recupera lista clienti univoci ordinata alfabeticamente.

### 2. `get_all_associations(so_number_filter=None)` → List[Dict]
Recupera tutte le associazioni con opzionale filtro per numero ordine.

**Parametri:**
- `so_number_filter`: Stringa opzionale per filtro LIKE

**Returns:**
```python
{
    'SONumber': str,
    'CustomerName': str,
    'SaleProduct': str,
    'ProductionOrder': str,
    'ProductionProduct': str,
    'Qty': float,
    'DateIn': datetime
}
```

### 3. `get_workload_by_product()` → List[Dict]
Calcola carichi di lavoro aggregati per prodotto.

**Returns:**
```python
{
    'Product': str,
    'TotalOrdered': float,
    'TotalAssigned': float,
    'TotalRemaining': float,
    'OrdersCount': int,
    'AvgValue': float
}
```

---

## Utilizzo della Funzionalità

### Apertura Finestra
```python
from orders.orders_reports_window import open_orders_reports_window

open_orders_reports_window(master, db, lang, user_name)
```

### Workflow Utente

#### 1. Riepilogo Generale
1. Seleziona range date
2. Clicca "Genera Rapporto"
3. Visualizza KPI e dettagli
4. (Opzionale) Clicca "Esporta Excel"

#### 2. Report per Cliente
1. Clicca "Carica Clienti"
2. Seleziona cliente dal combo
3. Clicca "Genera Rapporto"
4. Visualizza statistiche e ordini
5. (Opzionale) Esporta Excel

#### 3. Associazioni Produzione
1. (Opzionale) Inserisci filtro ordine
2. Clicca "Genera Rapporto"
3. Visualizza tutte le associazioni
4. (Opzionale) Esporta Excel

#### 4. Carichi di Lavoro
1. Clicca "Genera Rapporto"
2. Visualizza carichi per prodotto
3. Priorità produzione = Qtà Rimanente più alta
4. (Opzionale) Esporta Excel

---

## Traduzioni Necessarie

Eseguire lo script: **`INSERT_TRANSLATIONS_REPORTS.sql`**

Include 35+ chiavi tradotte in 5 lingue (IT, EN, RO, DE, SV).

---

## Performance

### Ottimizzazioni
- **Query parametrizzate** (SQL injection safe)
- **GROUP BY ottimizzato** con indici su chiavi
- **LEFT JOIN** per evitare perdita dati
- **Caching locale** per lista clienti
- **Lazy loading** tab (carica solo quando selezionato)

### Tempi Stimati
- Riepilogo Generale: < 1s (fino a 1000 ordini)
- Report Cliente: < 500ms
- Associazioni: < 800ms
- Carichi Lavoro: < 1s (aggregazione complessa)

---

## Dipendenze

### Python
- `tkinter` + `ttk`
- `tkcalendar`
- `openpyxl`
- `SQLAlchemy`

### Database
- Tabelle: `DynamicSaleOrders`, `DynamicProductionOrders`
- Join con: `orders`, `Products`

---

## Gestione Errori

### Errori Database
- Logging dettagliato con `exc_info=True`
- Rollback automatico transazioni
- Messaggio utente user-friendly

### Errori Export
- Verifica permessi scrittura file
- Gestione cancellazione dialog
- Conferma salvataggio

### Validazione Input
- Verifica selezione cliente prima generazione
- Controllo validità date
- Gestione combo vuoto

---

## Testing Checklist

### Funzionale
- [ ] Apertura finestra
- [ ] Switch tra tab
- [ ] Filtri date funzionanti
- [ ] Calcolo KPI corretto
- [ ] Colorazione righe (verde/giallo/rosso)
- [ ] Caricamento lista clienti
- [ ] Filtro numero ordine associazioni
- [ ] Ordinamento carichi per rimanente
- [ ] Export Excel tutti i tab
- [ ] Formato Excel corretto
- [ ] Auto-dimensionamento colonne

### Performance
- [ ] Caricamento riepilogo < 2s
- [ ] Switch tab istantaneo
- [ ] Export Excel < 3s
- [ ] Nessun freeze UI

### UI/UX
- [ ] Layout responsive
- [ ] Scrollbar funzionanti
- [ ] DateEntry localizzato
- [ ] Messaggi errore chiari
- [ ] Conferme salvataggio

---

## Esempi Output Excel

### Struttura File
```
| N. Ordine | Cliente | Prodotto | Data Spedizione | ... |
|-----------|---------|----------|-----------------|-----|
| SO12345   | ACME    | P001 [...| 15/02/2026      | ... |
| SO12346   | XYZ     | P002 [...| 20/02/2026      | ... |
```

**Formattazione:**
- Header: Blu scuro, testo bianco, grassetto
- Dati: Testo nero, bordi sottili
- Allineamento: Numeri a destra, testo a sinistra

---

## Prossimi Sviluppi Possibili

1. **Grafici integrati** (matplotlib/plotly)
   - Torta per distribuzione clienti
   - Barre per carichi lavoro
   - Timeline ordini

2. **Export PDF** con logo aziendale

3. **Schedulazione rapporti** automatici via email

4. **Dashboard interattiva** con drill-down

5. **Confronto periodi** (mese corrente vs precedente)

6. **Alert automatici** per ordini in ritardo

7. **Stampa diretta** rapporti

8. **Template rapporti** personalizzabili

---

## Note Implementative

### Thread Safety
- Session SQLAlchemy per operazione (no condivisione)
- Chiusura automatica connessioni (try/finally)

### Memoria
- Nessun caching massivo dati
- Garbage collection automatico oggetti treeview

### Logging
- Livello INFO per operazioni normali
- Livello ERROR per eccezioni
- exc_info=True per stack trace completo

---

## Integrazione con Main.py

### Sostituire placeholder:
```python
def _orders_reports_placeholder(self):
    """Apre la finestra rapporti ordini"""
    from orders.orders_reports_window import open_orders_reports_window
    open_orders_reports_window(self, self.db, self.lang, self.user_name)
```

### Menu entry:
```python
reports_menu = tk.Menu(orders_menu, tearoff=0)
orders_menu.add_cascade(label=self.lang.get('menu_reports', 'Rapporti'), menu=reports_menu)
reports_menu.add_command(
    label=self.lang.get('menu_orders_reports', 'Rapporti Ordini'),
    command=lambda: self._execute_authorized_action(
        self._orders_reports_placeholder,
        'Rapporti_Ordini'
    )
)
```

---

## Conclusione

Sistema di reporting completo e professionale per la gestione ordini dinamici. Fornisce visibilità completa su:
- Stato avanzamento ordini
- Performance per cliente
- Allocazione risorse produttive
- Carichi di lavoro pianificati

Con export Excel integrato per condivisione rapporti con stakeholders.
