# Suggerimento Automatico ItemID

## Funzionalità Implementata

Quando si crea un **nuovo task** e si seleziona una **categoria**, il sistema propone automaticamente un `ItemID` suggerito basato sui task esistenti nella categoria.

## File Modificato

**`npi/windows/config_window.py`** - Classe `TaskManagementFrame`

## Come Funziona

### 1. Evento Trigger
Quando l'utente seleziona una categoria dal combobox per un nuovo task, si attiva automaticamente il metodo `_on_category_selected()`.

### 2. Logica di Generazione

Il sistema analizza gli `ItemID` esistenti nella categoria e genera un suggerimento seguendo queste regole:

#### Caso 1: Nessun Task nella Categoria
```
Categoria selezionata: "Design"
Task esistenti: Nessuno

Suggerimento: DES-005
```
*(Prime 3 lettere della categoria + "-005")*

#### Caso 2: Task Esistenti con Pattern Riconosciuto
```
Categoria selezionata: "Materials procurement"
Task esistenti:
  - MAT-005
  - MAT-010
  - MAT-015

Ultimo ItemID: MAT-015
Suggerimento: MAT-020
```
*(Incremento di 5 rispetto all'ultimo)*

#### Caso 3: Incremento con Arrotondamento
```
Categoria selezionata: "Testing"
Task esistenti:
  - TEST-007
  - TEST-012

Ultimo ItemID: TEST-012
Calcolo: (12 ÷ 5) + 1 = 3, quindi 3 × 5 = 15
Suggerimento: TEST-015
```
*(Arrotonda al multiplo di 5 superiore)*

#### Caso 4: Pattern Non Riconosciuto
```
Categoria selezionata: "Quality"
Task esistenti:
  - QualityCheck1
  - QualityCheck2

Pattern non riconosciuto (non segue PREFIX-NUMERO)
Suggerimento: QUA-005
```
*(Fallback al default)*

## Algoritmo

```python
def genera_suggerimento(categoria, tasks_esistenti):
    if nessun_task_esistente:
        return f"{categoria[:3].upper()}-005"
    
    # Trova l'ultimo ItemID
    ultimo_id = max(item_ids)
    
    # Estrai PREFIX e NUMERO
    match = regex(r'^([A-Za-z]+)-?(\d+)$', ultimo_id)
    
    if match:
        prefix = match.group(1)
        numero = int(match.group(2))
        
        # Arrotonda al multiplo di 5 superiore
        prossimo_numero = ((numero // 5) + 1) * 5
        
        return f"{prefix}-{prossimo_numero:03d}"
    else:
        # Fallback
        return f"{categoria[:3].upper()}-005"
```

## Esempi Pratici

### Esempio 1: Prima Volta
```
┌─────────────────────────────────────┐
│ Nuovo Task                          │
├─────────────────────────────────────┤
│ ItemID:     [vuoto]                 │
│ Categoria:  [seleziona Design]      │
│             ↓                       │
│ ItemID:     DES-005  ← suggerito!   │
└─────────────────────────────────────┘
```

### Esempio 2: Incremento Normale
```
Task esistenti in "Materials":
  - MAT-005
  - MAT-010
  - MAT-015

Nuovo task:
┌─────────────────────────────────────┐
│ ItemID:     [vuoto]                 │
│ Categoria:  [seleziona Materials]   │
│             ↓                       │
│ ItemID:     MAT-020  ← suggerito!   │
└─────────────────────────────────────┘
```

### Esempio 3: Arrotondamento
```
Task esistenti in "Testing":
  - TEST-003
  - TEST-008

Nuovo task:
┌─────────────────────────────────────┐
│ ItemID:     [vuoto]                 │
│ Categoria:  [seleziona Testing]     │
│             ↓                       │
│ ItemID:     TEST-010  ← suggerito!  │
│             (8 → arrotonda a 10)    │
└─────────────────────────────────────┘
```

## Regole di Attivazione

Il suggerimento viene generato **SOLO** se:

1. ✅ Stai creando un **nuovo task** (non modificando uno esistente)
2. ✅ Il campo `ItemID` è **vuoto**
3. ✅ Hai selezionato una **categoria valida**

### Non si Attiva Se:

- ❌ Stai modificando un task esistente
- ❌ Hai già inserito un ItemID manualmente
- ❌ Non hai selezionato una categoria
- ❌ Hai selezionato "Tutte le categorie"

## Pattern Supportati

Il sistema riconosce questi pattern:

✅ **Supportati**:
```
DES-001, DES-002, DES-003
MAT001, MAT002, MAT003
TEST-5, TEST-10, TEST-15
Design1, Design2, Design3
```

❌ **Non Supportati** (usa fallback):
```
Task_Design_001
1-Design
Design-A-001
```

## Modifica Manuale

Il suggerimento è solo un **aiuto**. L'utente può:

1. ✅ **Accettare** il suggerimento (lasciarlo così com'è)
2. ✅ **Modificare** il suggerimento (cambiare il numero o il prefisso)
3. ✅ **Cancellare** e inserire un codice completamente diverso

## Vantaggi

1. ✅ **Risparmio di tempo**: Non devi ricordare l'ultimo numero usato
2. ✅ **Consistenza**: Mantiene automaticamente il pattern esistente
3. ✅ **Flessibilità**: Puoi sempre modificare il suggerimento
4. ✅ **Intelligente**: Si adatta al pattern che hai già usato
5. ✅ **Sicuro**: Non sovrascrive mai un ItemID già inserito

## Workflow Tipico

```
1. Clicca "Nuovo" per creare un task
   └─ Tutti i campi sono vuoti

2. Seleziona la categoria "Design"
   └─ ItemID viene popolato automaticamente con "DES-005"

3. Opzioni:
   a) Accetta il suggerimento → Continua con gli altri campi
   b) Modifica → Cambia "DES-005" in "DES-010"
   c) Sostituisci → Cancella e scrivi "DESIGN-001"

4. Compila gli altri campi e salva
```

## Note Tecniche

- Il suggerimento usa **zero padding** (es: `005` invece di `5`) per mantenere l'ordine alfabetico corretto
- L'incremento è sempre di **5** (o multiplo di 5)
- Il prefisso viene estratto dall'ultimo ItemID esistente, o dalle prime 3 lettere della categoria
- In caso di errore, il sistema fallisce silenziosamente (l'utente può inserire manualmente)

## Esempi di Fallback

Se il sistema non riesce a generare un suggerimento (es: errore di connessione al database), il campo `ItemID` rimane vuoto e l'utente può inserire il codice manualmente.

```
Errore durante il caricamento dei task
↓
Campo ItemID rimane vuoto
↓
Utente inserisce manualmente "DES-001"
```

## Raccomandazione

Per ottenere i migliori suggerimenti, mantieni una **convenzione consistente**:

✅ **Buona pratica**:
```
Categoria "Design":
  - DES-005
  - DES-010
  - DES-015
  
Nuovo task → Suggerimento: DES-020 ✓
```

⚠️ **Pratica inconsistente**:
```
Categoria "Design":
  - DES-001
  - Design-10
  - DESIGN_100
  
Nuovo task → Suggerimento: DES-005 (fallback)
```
