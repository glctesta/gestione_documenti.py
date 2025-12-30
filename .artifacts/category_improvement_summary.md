# Riepilogo Modifiche: Miglioramento Tab Categorie NPI

## Modifiche Implementate

### 1. npi_manager.py ✅
Aggiunti due nuovi metodi alla classe `GestoreNPI`:

- **`get_tasks_by_category(category_id)`**: Recupera tutti i task del catalogo per una specifica categoria, ordinati per `Nrordin`
- **`is_category_used_in_projects(category_id)`**: Verifica se una categoria è stata utilizzata in almeno un progetto (controlla se esistono `TaskProdotto` con task di quella categoria)

### 2. config_window.py - CategoryManagementFrame ✅

#### Modifiche al `__init__`:
- Aggiunta una **Listbox** con scrollbar per visualizzare i task della categoria selezionata
- La listbox è posizionata sotto i campi del form in un `LabelFrame` dedicato
- Configurato il form per espandersi verticalmente

#### Modifiche a `_load_categories`:
- Aggiunto controllo per verificare se la categoria è usata in progetti
- Aggiunto indicatore **`***`** alla fine del nome delle categorie già utilizzate

#### Modifiche a `_on_category_select`:
- Aggiunta chiamata a `_load_category_tasks()` per popolare la listbox quando si seleziona una categoria

#### Nuovo metodo `_load_category_tasks`:
- Carica i task della categoria selezionata nella listbox
- Mostra il formato: `ItemID - NomeTask`
- Aggiunge prefisso `[TITOLO]` per i task con `IsTitle=True`
- Gestisce il caso di categoria senza task

#### Modifiche a `_clear_form`:
- Aggiunta pulizia della listbox dei task quando si pulisce il form

### 3. Traduzioni ✅
Creato script SQL `CATEGORY_IMPROVEMENT_TRANSLATIONS.sql` con le seguenti chiavi:
- `category_tasks_label`: "Task in questa categoria:"
- `no_tasks_in_category`: "Nessun task in questa categoria"
- `label_category_name`: "Nome Categoria:"
- `label_order_number`: "Numero Ordine:"

Tutte le traduzioni sono disponibili in 5 lingue: IT, RO, EN, DE, SV

## Come Testare

1. **Eseguire lo script SQL**:
   ```sql
   -- In SQL Server Management Studio
   -- Eseguire: CATEGORY_IMPROVEMENT_TRANSLATIONS.sql
   ```

2. **Riavviare l'applicazione**

3. **Aprire la finestra di configurazione NPI**:
   - Menu → Operazioni → NPI → Configurazione

4. **Andare al tab "Categorie"**

5. **Verificare**:
   - ✅ Le categorie già utilizzate in progetti mostrano `***` alla fine del nome
   - ✅ Quando si seleziona una categoria, appare la lista dei suoi task
   - ✅ I task sono mostrati nel formato `ItemID - NomeTask`
   - ✅ I task con `IsTitle=True` hanno il prefisso `[TITOLO]`
   - ✅ Se una categoria non ha task, appare il messaggio "Nessun task in questa categoria"

## Struttura Dati

### Tabelle coinvolte:
- `[Traceability_RS].[dbo].[Categories]` - Categorie
- `[Traceability_RS].[dbo].[TaskCatalogo]` - Task del catalogo
- `[Traceability_RS].[dbo].[TaskProdotto]` - Task assegnati ai progetti

### Logica indicatore `***`:
Una categoria viene marcata con `***` se esiste almeno un record in `TaskProdotto` che referenzia un task (`TaskCatalogo`) appartenente a quella categoria.

## Screenshot Atteso

```
┌─────────────────────────────────────────────────────────────┐
│ Categorie                                                   │
├───────────────────┬─────────────────────────────────────────┤
│ ID │ Categoria    │ Dettagli Categoria                      │
├────┼──────────────┤                                         │
│ 1  │ Material *** │ Nome Categoria: Material                │
│ 2  │ Production   │ Numero Ordine: 20                       │
│ 3  │ Prototypes   │                                         │
└────┴──────────────┤ Task in questa categoria:               │
                    │ ┌─────────────────────────────────────┐ │
                    │ │ M01 - Material definition           │ │
                    │ │ M02 - Supplier selection            │ │
                    │ │ M03 - Cost analysis                 │ │
                    │ │ ...                                 │ │
                    │ └─────────────────────────────────────┘ │
                    │                                         │
                    │ [Nuovo] [Salva] [Elimina]              │
                    └─────────────────────────────────────────┘
```

## Note Tecniche

- La query per verificare l'utilizzo della categoria usa un `JOIN` tra `TaskProdotto` e `TaskCatalogo`
- La listbox supporta lo scrolling verticale per categorie con molti task
- Il metodo `_load_category_tasks` gestisce gli errori mostrando un messaggio nella listbox stessa
- Le modifiche sono retrocompatibili: se la listbox non esiste (per qualche motivo), il codice non genera errori

## File Modificati

1. `npi/npi_manager.py` - Aggiunti 2 metodi
2. `npi/windows/config_window.py` - Modificata classe `CategoryManagementFrame`
3. `CATEGORY_IMPROVEMENT_TRANSLATIONS.sql` - Nuovo file con traduzioni

## Prossimi Passi Suggeriti

1. ✅ Testare la funzionalità
2. ⏭️ Considerare l'aggiunta di un doppio click sulla listbox per aprire il task nel tab "Catalogo Task"
3. ⏭️ Aggiungere un contatore del numero di task nella label del LabelFrame
4. ⏭️ Aggiungere un filtro per mostrare solo i task utilizzati/non utilizzati
