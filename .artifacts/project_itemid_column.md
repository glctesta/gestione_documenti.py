# Visualizzazione ItemID nella Gestione Progetto NPI

## Modifica Implementata

Aggiunta la colonna **ItemID** (Codice) nella lista dei task del progetto NPI, per mostrare il codice identificativo del task accanto alla categoria.

## File Modificato

**`npi/windows/project_window.py`** - Classe `ProjectWindow`

## Modifiche

### 1. Aggiunta Colonna alla Treeview

**Prima**:
```python
columns = ('Category', 'Name', 'Owner', 'Status', 'DueDate')
```

**Dopo**:
```python
columns = ('Category', 'ItemID', 'Name', 'Owner', 'Status', 'DueDate')
```

### 2. Configurazione Colonna

```python
self.tree.heading('ItemID', text=self.lang.get('col_item_id', 'Codice'))
self.tree.column('ItemID', width=80)
```

### 3. Popolamento Dati

```python
item_id = task.task_catalogo.ItemID if task.task_catalogo else ""
self.tree.insert('', tk.END, text=task.TaskProdottoID, 
                 values=(cat, item_id, name, owner, status, due_date),
                 tags=tuple(tags))
```

## Visualizzazione

### Prima
```
┌──────────────┬─────────────────────┬────────────┬─────────┬───────────┐
│ Categoria    │ Task                │ Assegnato  │ Stato   │ Scadenza  │
├──────────────┼─────────────────────┼────────────┼─────────┼───────────┤
│ Design       │ Initial sketches    │ Mario R.   │ Attivo  │ 15/01/25  │
│ Design       │ 3D modeling         │            │ Pending │           │
│ Materials    │ Source materials    │ Luca B.    │ Attivo  │ 20/01/25  │
└──────────────┴─────────────────────┴────────────┴─────────┴───────────┘
```

### Dopo
```
┌──────────────┬─────────┬─────────────────────┬────────────┬─────────┬───────────┐
│ Categoria    │ Codice  │ Task                │ Assegnato  │ Stato   │ Scadenza  │
├──────────────┼─────────┼─────────────────────┼────────────┼─────────┼───────────┤
│ Design       │ DES-005 │ Initial sketches    │ Mario R.   │ Attivo  │ 15/01/25  │
│ Design       │ DES-010 │ 3D modeling         │            │ Pending │           │
│ Materials    │ MAT-005 │ Source materials    │ Luca B.    │ Attivo  │ 20/01/25  │
└──────────────┴─────────┴─────────────────────┴────────────┴─────────┴───────────┘
              ↑
         Nuova colonna!
```

## Vantaggi

1. ✅ **Identificazione Rapida**: Vedi subito il codice del task
2. ✅ **Riferimento Univoco**: Puoi usare il codice per comunicare (es: "Completa DES-005")
3. ✅ **Coerenza**: Stesso codice usato nel catalogo task
4. ✅ **Ordinamento**: I task sono già ordinati per ItemID

## Ordine Colonne

```
1. Categoria     (120px) - Categoria del task
2. Codice        (80px)  - ItemID (es: DES-005) ← NUOVO!
3. Task          (200px) - Nome del task
4. Assegnato a   (100px) - Owner
5. Stato         (100px) - Stato attuale
6. Scadenza      (80px)  - Data scadenza
```

## Note

- La colonna mostra l'`ItemID` dal catalogo task
- Se il task non ha un catalogo associato, la colonna è vuota
- La larghezza di 80px è sufficiente per codici tipo "DES-005", "MAT-010", etc.
- L'ordinamento rimane basato su ItemID (già implementato)

## Integrazione con Altre Funzionalità

### Filtro Categoria
- ✅ Funziona correttamente con il nuovo layout
- ✅ Mostra solo i task della categoria selezionata

### Filtro "Mostra Assegnati"
- ✅ Funziona correttamente con il nuovo layout
- ✅ Filtra in base all'Owner

### Task Speciali (Post-Final Milestone)
- ✅ Evidenziati in rosso e grassetto
- ✅ Visibili anche con la nuova colonna

## Esempio Completo

```
Progetto: "Nuovo Prodotto XYZ"
Wave: 1.0

┌──────────────┬─────────┬──────────────────────┬────────────┬─────────┬───────────┐
│ Categoria    │ Codice  │ Task                 │ Assegnato  │ Stato   │ Scadenza  │
├──────────────┼─────────┼──────────────────────┼────────────┼─────────┼───────────┤
│ Design       │ DES-005 │ Initial sketches     │ Mario R.   │ Attivo  │ 15/01/25  │
│ Design       │ DES-010 │ 3D modeling          │ Luca B.    │ Attivo  │ 20/01/25  │
│ Design       │ DES-015 │ Technical drawings   │            │ Pending │           │
│ Materials    │ MAT-005 │ Source raw materials │ Anna M.    │ Attivo  │ 18/01/25  │
│ Materials    │ MAT-010 │ Supplier qual.       │            │ Pending │           │
│ Testing      │ TEST-005│ Functional testing   │            │ Pending │           │
│ Testing      │ TEST-010│ Stress testing       │            │ Pending │           │
└──────────────┴─────────┴──────────────────────┴────────────┴─────────┴───────────┘
```

## Traduzione

Assicurati di avere la traduzione per `col_item_id` nelle lingue supportate:

```sql
-- IT
INSERT INTO Translations (TranslationKey, IT) VALUES ('col_item_id', 'Codice');

-- EN
INSERT INTO Translations (TranslationKey, EN) VALUES ('col_item_id', 'Code');

-- RO
INSERT INTO Translations (TranslationKey, RO) VALUES ('col_item_id', 'Cod');

-- DE
INSERT INTO Translations (TranslationKey, DE) VALUES ('col_item_id', 'Code');

-- SV
INSERT INTO Translations (TranslationKey, SV) VALUES ('col_item_id', 'Kod');
```

## Test

1. Apri un progetto NPI esistente
2. ✅ Verifica che la colonna "Codice" sia visibile
3. ✅ Verifica che mostri l'ItemID corretto per ogni task
4. ✅ Verifica che i filtri funzionino correttamente
5. ✅ Verifica che l'ordinamento sia per ItemID

---

**Data**: 22 Dicembre 2024  
**Versione**: 1.0  
**Stato**: ✅ Completato
