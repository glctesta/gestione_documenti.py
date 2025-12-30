# Filtro Prodotti per Cliente e Gestione Prodotti nei Complaints

## Modifiche Implementate

### 1. **Filtro Prodotti per Cliente**

I prodotti nel combo sono ora filtrati in base al cliente selezionato, mostrando solo i prodotti associati a quel cliente tramite `IDFinalClient`.

### 2. **Bottone Gestione Prodotti**

Aggiunto bottone per aprire la gestione prodotti direttamente dalla form dei complaints, senza richiedere un login aggiuntivo.

## File Modificato

**`add_complaint.py`** - Classe `AddComplaintWindow`

## Modifiche Dettagliate

### 1. Query Prodotti con IDFinalClient

**Prima**:
```sql
SELECT idproduct, ProductCode, ProductName
FROM products
WHERE CHARINDEX('cipr', ProductCode, 1) = 0
  AND CHARINDEX('RMA', ProductCode, 1) = 0
ORDER BY ProductCode
```

**Dopo**:
```sql
SELECT idproduct, ProductCode, ProductName, IDFinalClient
FROM products
WHERE CHARINDEX('cipr', ProductCode, 1) = 0
  AND CHARINDEX('RMA', ProductCode, 1) = 0
ORDER BY ProductCode
```

### 2. Evento sul Combo Clienti

```python
self.combo_client.bind('<<ComboboxSelected>>', self._on_client_selected)
```

### 3. Metodo `_on_client_selected()`

```python
def _on_client_selected(self, event=None):
    """Filtra i prodotti in base al cliente selezionato."""
    client_text = self.var_client.get()
    client_id = self.combo_data['clients_map'].get(client_text)
    
    # Filtra i prodotti per questo cliente
    all_products = self.combo_data.get('products', [])
    filtered_products = [p for p in all_products if p[3] == client_id]
    
    if not filtered_products:
        # Mostra warning e suggerisci di usare Gestione Prodotti
        messagebox.showwarning(
            'Attenzione',
            "Nessun prodotto associato al cliente selezionato.\n\n"
            "Usa il bottone 'Gestione Prodotti' per associare prodotti al cliente."
        )
        self.combo_product['values'] = []
    else:
        product_values = [f"{p[1]} - {p[2]}" for p in filtered_products]
        self.combo_product['values'] = product_values
```

### 4. Bottone Gestione Prodotti

```python
ttk.Button(
    buttons_frame,
    text=self.lang.get('btn_manage_products', 'Gestione Prodotti'),
    command=self._open_products_management
).pack(side=tk.LEFT, padx=(0, 5))
```

### 5. Metodo `_open_products_management()`

```python
def _open_products_management(self):
    """Apre la gestione prodotti senza login aggiuntivo."""
    # Usa l'utente già autenticato
    if hasattr(self.parent, 'traceability_manager'):
        self.parent.traceability_manager.open_define_products(self.authenticated_user)
```

## Workflow

### Scenario 1: Cliente con Prodotti Associati

```
1. Utente apre form complaints
2. Seleziona cliente "Vandewiele (VDW)"
   ├─ Evento <<ComboboxSelected>> si attiva
   ├─ Sistema filtra prodotti per IDFinalClient = 1
   └─ Combo prodotti mostra solo:
       - VDW-001 - Carpet Loom
       - VDW-002 - Weaving Machine
       - VDW-003 - Control Panel

3. Utente seleziona prodotto dalla lista filtrata
4. Continua con il reclamo
```

### Scenario 2: Cliente senza Prodotti Associati

```
1. Utente apre form complaints
2. Seleziona cliente "Nuovo Cliente (NC)"
   ├─ Evento <<ComboboxSelected>> si attiva
   ├─ Sistema filtra prodotti per IDFinalClient = 99
   └─ Nessun prodotto trovato

3. Sistema mostra warning:
   ┌─────────────────────────────────────────┐
   │ Attenzione                              │
   ├─────────────────────────────────────────┤
   │ Nessun prodotto associato al cliente   │
   │ selezionato.                            │
   │                                         │
   │ Usa il bottone 'Gestione Prodotti' per │
   │ associare prodotti al cliente.          │
   │                                         │
   │              [OK]                       │
   └─────────────────────────────────────────┘

4. Utente clicca "Gestione Prodotti"
5. Si apre la gestione prodotti (senza login)
6. Utente associa prodotti al cliente
7. Torna alla form complaints
8. Ricarica i dati (o riapre la form)
```

### Scenario 3: Apertura Gestione Prodotti

```
1. Utente clicca bottone "Gestione Prodotti"
2. Sistema:
   ├─ Verifica che parent.traceability_manager esista
   ├─ Chiama open_define_products(authenticated_user)
   └─ Passa l'utente già autenticato (nessun login richiesto)

3. Si apre la finestra di gestione prodotti
4. Utente può:
   ├─ Creare nuovi prodotti
   ├─ Modificare prodotti esistenti
   └─ Associare prodotti ai clienti (IDFinalClient)

5. Chiude la gestione prodotti
6. Torna alla form complaints
```

## Struttura Dati

### Tabella `products`

```
┌────────────┬─────────────┬──────────────┬───────────────┐
│ idproduct  │ ProductCode │ ProductName  │ IDFinalClient │
├────────────┼─────────────┼──────────────┼───────────────┤
│ 1          │ VDW-001     │ Carpet Loom  │ 1             │
│ 2          │ VDW-002     │ Weaving Mach │ 1             │
│ 3          │ BSH-001     │ Dishwasher   │ 2             │
│ 4          │ BSH-002     │ Washing Mach │ 2             │
└────────────┴─────────────┴──────────────┴───────────────┘
                                           ↑
                                    Filtro per cliente
```

### Tabella `FinalClients`

```
┌───────────────┬─────────────────┬────────────────┐
│ IDFinalClient │ FinalClientName │ AcronimForCode │
├───────────────┼─────────────────┼────────────────┤
│ 1             │ Vandewiele      │ VDW            │
│ 2             │ Bosch           │ BSH            │
│ 3             │ Siemens         │ SIE            │
└───────────────┴─────────────────┴────────────────┘
```

## UI Layout

### Prima

```
┌─────────────────────────────────────────────────────┐
│ Testata Reclamo                                     │
├─────────────────────────────────────────────────────┤
│ Cliente: [Vandewiele (VDW) ▼]                      │
│ Prodotto: [Tutti i prodotti ▼]  ← Non filtrato     │
│                                                     │
│                    [Salva] [Annulla]                │
└─────────────────────────────────────────────────────┘
```

### Dopo

```
┌─────────────────────────────────────────────────────┐
│ Testata Reclamo                                     │
├─────────────────────────────────────────────────────┤
│ Cliente: [Vandewiele (VDW) ▼]                      │
│ Prodotto: [VDW-001 - Carpet Loom ▼]  ← Filtrato!   │
│                                                     │
│ [Gestione Prodotti]        [Salva] [Annulla]       │
│  ↑ Nuovo bottone                                    │
└─────────────────────────────────────────────────────┘
```

## Vantaggi

1. ✅ **Filtro Automatico**: Solo prodotti del cliente selezionato
2. ✅ **Prevenzione Errori**: Impossibile selezionare prodotti di altri clienti
3. ✅ **Accesso Rapido**: Bottone per gestione prodotti senza login
4. ✅ **User Friendly**: Warning chiaro se nessun prodotto associato
5. ✅ **Workflow Integrato**: Gestione prodotti accessibile dalla form

## Note Tecniche

- Il filtro si basa sul campo `IDFinalClient` nella tabella `products`
- Se `IDFinalClient` è NULL, il prodotto non apparirà per nessun cliente
- L'utente autenticato viene passato direttamente alla gestione prodotti
- Il filtro si aggiorna automaticamente quando si cambia cliente

## Test

### Test 1: Filtro Funzionante
1. Apri form complaints
2. Seleziona cliente "Vandewiele"
3. ✅ Verifica che combo prodotti mostri solo prodotti VDW

### Test 2: Nessun Prodotto
1. Apri form complaints
2. Seleziona cliente senza prodotti
3. ✅ Verifica warning
4. ✅ Verifica combo prodotti vuoto

### Test 3: Gestione Prodotti
1. Apri form complaints
2. Clicca "Gestione Prodotti"
3. ✅ Verifica apertura senza login
4. ✅ Verifica utente corretto

### Test 4: Cambio Cliente
1. Seleziona cliente A
2. Verifica prodotti filtrati
3. Seleziona cliente B
4. ✅ Verifica che prodotti cambino

---

**Data**: 22 Dicembre 2024  
**Versione**: 1.0  
**Stato**: ✅ Completato
