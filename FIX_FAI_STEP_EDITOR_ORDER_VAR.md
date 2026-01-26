# Fix: AttributeError in StepEditorDialog

## Problema
```
AttributeError: 'StepEditorDialog' object has no attribute 'order_var'
```

**Traceback**: Errore alla linea 1706 in `_update_suggested_order()` quando tenta di chiamare `self.order_var.set(next_order)`.

## Causa
Ordine di inizializzazione errato nel metodo `_create_widgets()`:

1. Alla linea 1607 viene chiamato `_load_templates()`
2. `_load_templates()` chiama `_update_suggested_order()` alla linea 1662
3. `_update_suggested_order()` tenta di accedere a `self.order_var` alla linea 1706
4. **MA** `self.order_var` viene definito solo alla linea 1618, DOPO la chiamata a `_load_templates()`

## Soluzione
Spostata l'inizializzazione di `self.order_var` PRIMA della chiamata a `_load_templates()`:

```python
# PRIMA (errato):
# Template
self.template_var = tk.StringVar()
self.template_combo = ttk.Combobox(...)
self._load_templates()  # <-- Chiama _update_suggested_order() che usa order_var
row += 1

# Nome Step
...
row += 1

# Ordine
self.order_var = tk.IntVar(value=1)  # <-- Definito DOPO!
```

```python
# DOPO (corretto):
# Inizializza order_var PRIMA
self.order_var = tk.IntVar(value=1)  # <-- Definito PRIMA!

# Template
self.template_var = tk.StringVar()
self.template_combo = ttk.Combobox(...)
self._load_templates()  # <-- Ora può usare order_var
```

## File Modificato
- [`fai_template_manager.py`](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/fai_template_manager.py#L1594-L1620) - Metodo `StepEditorDialog._create_widgets()`

## Test
Riavviare l'applicazione e verificare che:
1. L'apertura del dialog "Nuovo Step" non generi più l'errore
2. Il campo "Ordine" venga popolato automaticamente con il valore suggerito
3. La modifica di uno step esistente funzioni correttamente
