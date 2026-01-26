# Fix: Combo Filtro Steps Vuoto al Caricamento

## Data: 2026-01-14

## Problema Riscontrato

Il combobox "Filtra Step" nel tab Steps non mostrava alcun valore al caricamento iniziale della form.

## Causa

Il metodo `_update_steps_filter_combo()` non veniva chiamato dopo il caricamento iniziale dei template (`_load_steps_templates()`).

### Sequenza Precedente:
```python
# In _create_steps_tab()
self._load_steps_templates()  # ← Caricava template
self._load_steps()             # ← Chiamava _update_steps_filter_combo()
```

**Problema:** Tra questi due metodi, il combo filtro steps rimaneva vuoto momentaneamente e non veniva inizializzato correttamente se l'utente non cambiava template.

## Soluzione

Aggiunta chiamata a `_update_steps_filter_combo()` alla fine di `_load_steps_templates()`:

```python
def _load_steps_templates(self):
    """Carica i template per il combo del tab Steps."""
    try:
        # ... caricamento template ...
        
        self.steps_template_combo['values'] = template_values
        if template_values:
            self.steps_template_var.set(template_values[0])
        
        # ✅ FIX: Aggiorna il combo filtro steps dopo aver caricato i template
        self._update_steps_filter_combo()
        
    except Exception as e:
        logger.error(f"Errore caricamento template per steps: {e}", exc_info=True)
```

## Comportamento Corretto

Ora il combo "Filtra Step" viene correttamente inizializzato in 3 momenti:

1. **All'apertura del tab** → dopo `_load_steps_templates()` 
2. **Al cambio template** → in `_on_steps_template_select()`
3. **Dopo ricarica steps** → in `_load_steps()`

### Valore Iniziale

- Se template selezionato = "Tutti i template" → Combo filtro mostra solo: `["Tutti gli steps"]`
- Se template specifico selezionato → Combo filtro mostra: `["Tutti gli steps", "1 - NomeStep1", "2 - NomeStep2", ...]`

## File Modificato

**`fai_template_manager.py`**
- Metodo `_load_steps_templates()` - Aggiunta chiamata a `_update_steps_filter_combo()`

## Test

✅ Aprire tab Steps → Combo "Filtra Step" mostra "Tutti gli steps"
✅ Selezionare un template → Combo si popola con gli step di quel template
✅ Tornare a "Tutti i template" → Combo torna a mostrare solo "Tutti gli steps"
✅ Premere "Aggiorna" → Combo rimane correttamente popolato
