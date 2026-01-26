# Aggiornamento Automatico OrderInList - FAI Steps

## Data: 2026-01-14

## Descrizione
Implementato suggerimento automatico del prossimo `OrderInList` disponibile quando si crea un nuovo step FAI.

---

## Funzionalità

### 📋 Comportamento Automatico

Quando l'utente **crea un nuovo step** (non in modifica), il campo `OrderInList` viene automaticamente aggiornato con il **prossimo numero disponibile** basandosi sul template selezionato.

### 🔄 Trigger di Aggiornamento

L'`OrderInList` viene aggiornato automaticamente in questi momenti:

1. **Caricamento Iniziale del Dialog**
   - Quando si apre il dialog per creare un nuovo step
   - Viene selezionato il primo template disponibile
   - `OrderInList` viene impostato al prossimo numero libero

2. **Cambio Template**
   - Quando l'utente cambia il template dal combobox
   - `OrderInList` viene ricalcolato per il nuovo template selezionato

3. **Preselezione Template**
   - Quando si crea uno step partendo da un template già filtrato
   - `OrderInList` viene calcolato per quel template specifico

---

## Implementazione Tecnica

### Metodo Principale: `_update_suggested_order()`

```python
def _update_suggested_order(self):
    """Calcola e imposta il prossimo OrderInList disponibile per il template selezionato."""
    template_label = self.template_var.get()
    if not template_label or template_label not in self.templates_data:
        return
    
    try:
        template_id = self.templates_data[template_label]
        
        # Query per trovare il massimo OrderInList per questo template (solo record attivi)
        query = """
        SELECT ISNULL(MAX(OrderInList), 0) as MaxOrder
        FROM [Traceability_RS].[fai].[FaiSteps]
        WHERE FaiTemplateId = ? AND DateOut IS NULL
        """
        
        cursor = self.db.cursor
        cursor.execute(query, (template_id,))
        result = cursor.fetchone()
        
        if result:
            max_order = result.MaxOrder if result.MaxOrder is not None else 0
            # Suggerisci il prossimo numero (max + 1), ma non superare 255
            next_order = min(max_order + 1, 255)
            self.order_var.set(next_order)
```

### Query SQL

```sql
SELECT ISNULL(MAX(OrderInList), 0) as MaxOrder
FROM [Traceability_RS].[fai].[FaiSteps]
WHERE FaiTemplateId = ? AND DateOut IS NULL
```

**Caratteristiche:**
- Considera solo record **attivi** (`DateOut IS NULL`)
- Usa `ISNULL(MAX(...), 0)` per gestire template senza step (ritorna 0)
- Il prossimo numero suggerito è `MAX + 1`

### Binding Eventi

```python
# Nel metodo _create_widgets()
self.template_combo.bind('<<ComboboxSelected>>', self._on_template_change)

# Gestore evento
def _on_template_change(self, event=None):
    """Gestisce il cambio di template e aggiorna OrderInList suggerito."""
    if not self.step_id:  # Solo per nuovi step, non in modifica
        self._update_suggested_order()
```

---

## Esempi di Utilizzo

### Scenario 1: Template Vuoto
- Template A **non ha step attivi**
- Query ritorna: `MaxOrder = 0`
- **Suggerimento:** `OrderInList = 1`

### Scenario 2: Template con Steps
- Template B ha step con `OrderInList`: 1, 2, 3, 5, 8
- Query ritorna: `MaxOrder = 8`
- **Suggerimento:** `OrderInList = 9`

### Scenario 3: Template con Steps Cancellati
- Template C ha:
  - Step attivi: `OrderInList` 1, 2, 3
  - Step cancellati (DateOut NOT NULL): `OrderInList` 10, 15
- Query ritorna: `MaxOrder = 3` (ignora i cancellati)
- **Suggerimento:** `OrderInList = 4`

### Scenario 4: Limite Massimo
- Template D ha step fino a `OrderInList = 255`
- Query ritorna: `MaxOrder = 255`
- **Suggerimento:** `OrderInList = 255` (limite massimo, tinyint)

### Scenario 5: Cambio Template
1. Utente seleziona Template A (suggerito: 5)
2. Utente cambia a Template B
3. Sistema ricalcola automaticamente (nuovo suggerimento: 3)

---

## Vantaggi UX

✅ **Nessun Conflitto:** L'utente non deve indovinare quale numero usare

✅ **Velocità:** Inserimento rapido senza dover controllare gli step esistenti

✅ **Flessibilità:** L'utente può comunque modificare manualmente il valore se necessario

✅ **Dinamico:** Si aggiorna automaticamente al cambio template

✅ **Intelligente:** Considera solo step attivi, ignorando quelli cancellati

---

## Protezione da Errori

### Gestione Errori Database
Se la query fallisce, il sistema:
- Logga l'errore
- Mantiene il valore predefinito (1)
- Non blocca l'utente

### Validazione Sempre Attiva
Anche con il suggerimento automatico, la **validazione anti-duplicati** rimane attiva:
- Se l'utente modifica manualmente il numero
- Se c'è un conflitto race condition (altro utente inserisce nello stesso momento)
- Il sistema impedisce comunque il salvataggio di duplicati

---

## Limitazioni e Note

⚠️ **Solo per Nuovi Step:**
- L'aggiornamento automatico funziona solo quando si crea un nuovo step
- In modalità **modifica**, l'`OrderInList` mantiene il valore esistente

⚠️ **Limite Tinyint:**
- Valore massimo: 255
- Se raggiunto, rimane a 255 (l'utente dovrà gestirlo manualmente)

ℹ️ **Suggerimento, Non Imposizione:**
- Il valore è un suggerimento intelligente
- L'utente può sempre modificarlo manualmente usando lo Spinbox

---

## File Modificato

**`fai_template_manager.py`** - Classe `StepEditorDialog`

**Metodi aggiunti/modificati:**
- `_on_template_change()` - Gestore evento cambio template
- `_update_suggested_order()` - Calcolo prossimo OrderInList
- `_load_templates()` - Aggiornamento iniziale
- `_preselect_template()` - Aggiornamento con preselezione
- `_create_widgets()` - Binding evento combobox

---

## Conclusione

L'aggiornamento automatico dell'`OrderInList` migliora significativamente l'esperienza utente, rendendo più veloce e sicuro l'inserimento di nuovi step FAI. Il sistema bilancia automazione e flessibilità, fornendo suggerimenti intelligenti mantenendo sempre il controllo manuale disponibile.
