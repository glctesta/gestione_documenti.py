# MODULO CARICA ORDINI - DOCUMENTAZIONE COMPLETA
## Data: 2026-01-19

## 📋 PANORAMICA

Il modulo **Carica Ordini** permette di importare ordini di vendita dinamici da file Excel nel database, con logica intelligente di INSERT/UPDATE basata sull'esistenza dell'ordine.

---

## 🗂️ STRUTTURA FILE

### File creati:

```
orders/
├── __init__.py                    # Modulo Python
├── orders_manager.py              # Manager database ordini
└── load_orders_window.py          # GUI per caricamento ordini

SQL/
├── SQL_TRADUZIONI_CARICA_ORDINI.sql           # Traduzioni complete
└── SQL_AUTORIZZAZIONI_MENU_ORDINI.sql         # Configurazione permessi
```

---

## 🔐 AUTORIZZAZIONE

**Chiave:** `Aggiungi_Ordini`
- Il menu è protetto da `_execute_authorized_action`
- Richiede login e verifica permessi prima dell'accesso

---

## 📊 DATABASE

### Tabella principale: `[Traceability_RS].[dyn].[DynamicSaleOrders]`

**Query completa per visualizzazione:**
```sql
SELECT  
    d.[DynamicSaleOrderId],
    d.[SONumber],
    d.[CustomerName],
    pr.ProductCode,
    pr.ProductName,
    d.[ShipDateRequest],
    d.[QtyOrder],
    d.[QtyToShip],
    d.[QtyStock],
    d.[Currency],
    d.[UnitPrice]
FROM [Traceability_RS].[dyn].[DynamicSaleOrders] d 
LEFT JOIN [Traceability_RS].[dyn].DynamicProductionOrders p 
    ON d.DynamicSaleOrderId = p.DynamicSaleOrderId
LEFT JOIN [Traceability_RS].dbo.orders o 
    ON o.IDOrder = p.idorder 
LEFT JOIN [Traceability_RS].dbo.products pr 
    ON pr.idproduct = o.IDProduct
```

---

## 📥 IMPORTAZIONE EXCEL

### Struttura file Excel

**Colonne utilizzate** (in base all'immagine fornita):

| Col | Nome Campo          | Usata | Note                          |
|-----|---------------------|-------|-------------------------------|
| A   | SO Number           | ✅    | Numero ordine vendita         |
| B   | -                   | ❌    | **SALTATA**                   |
| C   | Customer Code       | ✅    | Codice cliente                |
| D   | -                   | ❌    | **SALTATA**                   |
| E   | Customer Name       | ✅    | Nome cliente                  |
| F   | Customer Reference  | ✅    | Riferimento cliente           |
| G   | Item Code           | ✅    | Codice articolo               |
| H   | Item Name           | ✅    | Nome articolo                 |
| I   | Ship Date Request   | ✅    | Data spedizione richiesta     |
| J   | Available           | ✅    | Disponibilità                 |
| K   | Order Qty           | ✅    | Quantità ordinata             |
| L   | Remaining Qty       | ✅    | Quantità rimanente (QtyToShip)|
| M   | -                   | ❌    | **SALTATA**                   |
| N   | Stock Qty           | ✅    | Quantità in stock             |
| O   | Currency            | ✅    | Valuta                        |
| P   | Unit Price          | ✅    | Prezzo unitario               |

### Logica di importazione

1. **Verifica esistenza ordine** (basata su `SONumber`)
   
2. **Se l'ordine ESISTE:**
   ```sql
   UPDATE [Traceability_RS].[dyn].[DynamicSaleOrders]
   SET 
       QtyToShip = <valore_da_excel>,
       QtyStock = <valore_da_excel>,
       LastUpdated = GETDATE()
   WHERE SONumber = <so_number>
   ```

3. **Se l'ordine NON ESISTE:**
   ```sql
   INSERT INTO [Traceability_RS].[dyn].[DynamicSaleOrders]
   (SONumber, CustomerName, ShipDateRequest, QtyOrder, QtyToShip, QtyStock, 
    Currency, UnitPrice, CustomerCode, CustomerReference, ItemCode, ItemName)
   VALUES (...)
   ```

### Formati data supportati:
- `dd-mm-yyyy` (es: 20-02-2026)
- `yyyy-mm-dd` (es: 2026-02-20)
- Oggetti `datetime` di Excel

---

## 🖥️ INTERFACCIA UTENTE

### Finestra "Carica Ordini"

**Dimensioni:** 1400x700

**Componenti:**
- **Header:** Titolo "Elenco Ordini Dinamici"
- **Toolbar:**
  - Bottone "Importa da Excel"
  - Bottone "Aggiorna"
- **Treeview:** Visualizzazione ordini con colonne:
  - N. Ordine (100px)
  - Cliente (150px)
  - Cod. Prodotto (100px)
  - Nome Prodotto (200px)
  - Data Spedizione (100px)
  - Qtà Ordinata (80px)
  - Qtà da Spedire (80px)
  - Qtà in Stock (80px)
  - Valuta (60px)
  - Prezzo Unit. (80px)
- **Status Bar:** Mostra conteggio ordini e messaggi di stato

### Flusso utente:

```
1. Utente clicca "Ordini" → "Carica Ordini"
2. Sistema richiede login + verifica permesso "Aggiungi_Ordini"
3. Si apre finestra con elenco ordini esistenti
4. Utente clicca "Importa da Excel"
5. Seleziona file Excel
6. Sistema analizza file e mostra conferma (es: "Importare 10 righe?")
7. Utente conferma
8. Sistema esegue import con logica INSERT/UPDATE
9. Mostra risultati: "Inseriti: 5, Aggiornati: 4, Errori: 1"
10. Ricarica automaticamente la lista ordini
```

---

## 🔧 CODICE INTEGRATO IN MAIN.PY

### Modifica al metodo `_load_orders_placeholder` (riga 14103):

```python
def _load_orders_placeholder(self):
    """Menu Carica Ordini - Protetto da autorizzazione"""
    def authorized_action():
        """Apre la finestra di caricamento ordini"""
        try:
            from orders.load_orders_window import open_load_orders_window
            
            # Recupera il nome dell'utente autenticato
            user_name = self.last_authenticated_user_name if hasattr(self, 'last_authenticated_user_name') else 'Unknown'
            
            open_load_orders_window(self, self.db, self.lang, user_name)
        except Exception as e:
            logger.error(f"Errore apertura finestra caricamento ordini: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('error_opening_window', 'Errore apertura finestra')}:\n{e}",
                parent=self
            )
    
    self._execute_authorized_action(
        menu_translation_key='Aggiungi_Ordini',
        action_callback=authorized_action
    )
```

---

## 🌍 TRADUZIONI

**File SQL:** `SQL_TRADUZIONI_CARICA_ORDINI.sql`

**Lingue supportate:** IT, EN, RO, DE, SV

**Totale chiavi tradotte:** ~40 chiavi x 5 lingue = ~200 traduzioni

**Chiavi principali:**
- `load_orders_title` - Titolo finestra
- `dynamic_orders_list` - Titolo elenco
- `btn_import_excel` - Bottone import
- `btn_refresh` - Bottone aggiorna
- `col_*` - Tutte le colonne del treeview
- `import_completed`, `inserted`, `updated`, `errors` - Messaggi risultato
- Vari messaggi di errore e conferma

**Nota:** Tutte le stringhe rumene hanno il prefisso `N` per Unicode.

---

## 📦 DIPENDENZE

### Python:
- `tkinter` - GUI
- `openpyxl` - Lettura file Excel
- `sqlalchemy` - Database ORM
- `logging` - Log applicazione

### Database:
- SQL Server con schema esistente `[Traceability_RS]`
- Tabella `[dyn].[DynamicSaleOrders]` deve essere presente

---

## 🚀 DEPLOYMENT

### 1. Eseguire script SQL:
```bash
# 1. Traduzioni
Execute: SQL_TRADUZIONI_MENU_ORDINI_FILTRO_PERSONE.sql
Execute: SQL_TRADUZIONI_CARICA_ORDINI.sql

# 2. Configurare permessi
# Seguire istruzioni in: SQL_AUTORIZZAZIONI_MENU_ORDINI.sql
# Aggiungere chiave "Aggiungi_Ordini" alla tabella permessi
# Assegnare permesso agli utenti appropriati
```

### 2. Verificare struttura file:
```
PrductionDocumentation/
├── main.py                        ✅ Modificato
├── orders/                        ✅ Nuova cartella
│   ├── __init__.py
│   ├── orders_manager.py
│   └── load_orders_window.py
└── SQL_*.sql                      ✅ Script SQL
```

### 3. Testare:
1. Riavviare applicazione
2. Navigare a: Operazioni → Ordini → Carica Ordini
3. Effettuare login con utente autorizzato
4. Verificare visualizzazione ordini esistenti
5. Testare import da Excel con file di esempio

---

## ⚠️ NOTE IMPORTANTI

1. **Colonne saltate:** Le colonne B, D e M dell'Excel vengono IGNORATE
2. **Campo chiave:** `SONumber` determina se fare INSERT o UPDATE
3. **Campi aggiornati:** Solo `QtyToShip` e `QtyStock` vengono aggiornati negli UPDATE
4. **Gestione errori:** Gli errori di importazione vengono loggati ma non bloccano le altre righe
5. **Transazioni:** Ogni INSERT/UPDATE è una transazione separata
6. **Date:** Parsing flessibile con multiple formati supportati

---

## 📝 TODO / PROSSIMI PASSI

- [ ] Eseguire script SQL traduzioni
- [ ] Configurare permessi utente per "Aggiungi_Ordini"
- [ ] Testare importazione con file Excel reale
- [ ] Implementare secondo menu "Accoppia Ordini Produzione"
- [ ] Implementare terzo menu "Rapporti"

---

## 🐛 TROUBLESHOOTING

**Problema:** Errore "Tabella non trovata"
**Soluzione:** Verificare che la tabella `[Traceability_RS].[dyn].[DynamicSaleOrders]` esista

**Problema:** Date non vengono importate correttamente
**Soluzione:** Verificare formato date nel file Excel (colonna I)

**Problema:** Permesso negato
**Soluzione:** Verificare che l'utente abbia il permesso "Aggiungi_Ordini" assegnato

**Problema:** Errore import openpyxl
**Soluzione:** Installare: `pip install openpyxl`

---

**Fine documentazione - Versione 1.0**
