# Guida ai Campi ID nel Sistema NPI

## Panoramica dei Campi

Nel sistema NPI esistono **tre diversi campi** che identificano i task. Ognuno ha uno scopo specifico:

| Campo | Tipo | Scopo | Esempio | Visibile all'utente |
|-------|------|-------|---------|---------------------|
| **TaskID** | Integer (PK) | Chiave primaria del database | 1, 2, 3, 4... | ❌ No |
| **ItemID** | String(50) | Codice identificativo leggibile | "DES-001", "MAT-010" | ✅ Sì |
| **NrOrdin** | Integer | Numero d'ordine per sorting | 1005, 1010, 2005 | ✅ Sì (solo modifica) |

---

## 1. TaskID (Chiave Primaria)

### Caratteristiche
- **Tipo**: `Integer` (autoincrement)
- **Scopo**: Identificatore univoco nel database
- **Generato**: Automaticamente dal database
- **Modificabile**: ❌ No
- **Visibile**: ❌ No (solo uso interno)

### Utilizzo
```python
# Usato internamente per relazioni database
task = npi_manager.get_catalogo_task_by_id(task_id=5)
```

### Esempio
```
TaskID: 1, 2, 3, 4, 5, 6, 7, 8...
```

---

## 2. ItemID (Codice Identificativo)

### Caratteristiche
- **Tipo**: `String(50)`
- **Scopo**: **Codice leggibile e significativo** per identificare il task
- **Generato**: ✅ **Manualmente dall'utente**
- **Modificabile**: ✅ Sì
- **Visibile**: ✅ Sì (colonna principale nella lista)
- **Univoco**: ✅ Deve essere unico in tutto il catalogo

### Utilizzo
L'`ItemID` è il **codice che l'utente vede e usa** per identificare rapidamente un task. È come un "codice articolo" o "SKU".

### Esempi Pratici

#### Convenzione Suggerita: `[CATEGORIA]-[NUMERO]`
```
Design:
  - DES-001: "Create initial sketches"
  - DES-002: "3D modeling"
  - DES-003: "Technical drawings"

Materials:
  - MAT-001: "Source raw materials"
  - MAT-010: "Supplier qualification"
  - MAT-020: "Material testing"

Testing:
  - TEST-001: "Functional testing"
  - TEST-002: "Stress testing"
  - TEST-003: "Quality inspection"
```

#### Altre Convenzioni Possibili
```
Numerica semplice:
  - 001, 002, 003, 004...

Gerarchica:
  - 1.1, 1.2, 1.3, 2.1, 2.2...

Descrittiva:
  - SKETCH, 3DMODEL, DRAWINGS, SOURCING...
```

### Validazione
- ✅ Deve essere **univoco** in tutto il catalogo
- ⚠️ Il sistema controlla i duplicati e impedisce il salvataggio

### Dove si Vede
```
┌─────────────────────────────────────────────┐
│ Catalogo Task                               │
├──────────┬──────────────────┬───────────────┤
│ ItemID   │ Nome Task        │ Categoria     │
├──────────┼──────────────────┼───────────────┤
│ DES-001  │ Initial sketches │ Design        │
│ DES-002  │ 3D modeling      │ Design        │
│ MAT-001  │ Source materials │ Materials     │
│ TEST-001 │ Functional test  │ Testing       │
└──────────┴──────────────────┴───────────────┘
```

---

## 3. NrOrdin (Numero d'Ordine)

### Caratteristiche
- **Tipo**: `Integer`
- **Scopo**: **Ordinamento automatico** dei task
- **Generato**: 
  - ✅ **Automaticamente** per nuovi task
  - ✅ **Modificabile manualmente** per task esistenti
- **Modificabile**: ✅ Sì (solo per task esistenti)
- **Visibile**: ✅ Sì (solo in modifica)
- **Univoco**: ⚠️ Solo all'interno della stessa categoria

### Utilizzo
Il `NrOrdin` determina l'**ordine di visualizzazione** dei task nelle liste e nei progetti.

### Schema di Numerazione
```
Formula: NrOrdin = (NrOrdin_Categoria × 100) + numero_progressivo

Categoria Design (NrOrdin = 10):
  TaskID  ItemID    NomeTask           NrOrdin
  ------  --------  -----------------  -------
  1       DES-001   Initial sketches   1005
  2       DES-002   3D modeling        1010
  3       DES-003   Drawings           1015

Categoria Materials (NrOrdin = 20):
  TaskID  ItemID    NomeTask           NrOrdin
  ------  --------  -----------------  -------
  4       MAT-001   Source materials   2005
  5       MAT-010   Qualification      2010
  6       MAT-020   Testing            2015
```

### Dove si Vede
```
┌─────────────────────────────────────────────┐
│ Dettagli Task (Modifica)                    │
├─────────────────────────────────────────────┤
│ ItemID:        DES-001                      │
│ Nome Task:     Initial sketches             │
│ Categoria:     Design                       │
│ Nr. Ordine:    1005          ← Modificabile │
│ Descrizione:   ...                          │
└─────────────────────────────────────────────┘
```

---

## Confronto Pratico

### Scenario: Creazione di un Task "3D Modeling" nella categoria Design

```python
# 1. L'utente compila il form:
ItemID = "DES-002"           # ← Inserito manualmente dall'utente
NomeTask = "3D modeling"
CategoryId = 1 (Design)

# 2. Il sistema salva:
TaskID = 2                   # ← Generato automaticamente dal DB
ItemID = "DES-002"           # ← Quello inserito dall'utente
NrOrdin = 1010               # ← Calcolato automaticamente (10×100 + 10)
```

### Visualizzazione nella Lista
```
┌──────────┬──────────────┬───────────┐
│ ItemID   │ Nome Task    │ Categoria │  ← L'utente vede ItemID
├──────────┼──────────────┼───────────┤
│ DES-001  │ Sketches     │ Design    │
│ DES-002  │ 3D modeling  │ Design    │  ← Ordinato per NrOrdin
│ DES-003  │ Drawings     │ Design    │
└──────────┴──────────────┴───────────┘
```

### Ordinamento Interno
```sql
-- Il sistema ordina per NrOrdin
SELECT * FROM TaskCatalogo 
ORDER BY NrOrdin;

-- Risultato:
-- TaskID=1, ItemID=DES-001, NrOrdin=1005
-- TaskID=2, ItemID=DES-002, NrOrdin=1010
-- TaskID=3, ItemID=DES-003, NrOrdin=1015
```

---

## Best Practices

### Per ItemID
1. ✅ **Usa una convenzione consistente** (es: `CATEGORIA-NUMERO`)
2. ✅ **Rendi il codice significativo** (facile da ricordare e cercare)
3. ✅ **Mantieni una lunghezza ragionevole** (max 10-15 caratteri)
4. ❌ **Non usare caratteri speciali** che potrebbero creare problemi

### Esempi di Buone Convenzioni
```
✅ BUONO:
   DES-001, DES-002, DES-003
   MAT-010, MAT-020, MAT-030
   TEST-FUNC, TEST-STRESS, TEST-QC

❌ DA EVITARE:
   task1, task2, task3              (non significativo)
   Design/001, Design/002           (caratteri speciali)
   VERY_LONG_DESCRIPTIVE_CODE_001   (troppo lungo)
```

### Per NrOrdin
1. ✅ **Lascia che il sistema lo calcoli** per nuovi task
2. ✅ **Modifica solo se necessario** riordinare manualmente
3. ✅ **Mantieni incrementi di 5** per coerenza
4. ⚠️ **Attenzione ai duplicati** nella stessa categoria

---

## Riepilogo Visivo

```
┌─────────────────────────────────────────────────────────────┐
│                    TASK NEL DATABASE                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TaskID: 5                    ← Chiave primaria (nascosto) │
│  ItemID: "DES-002"            ← Codice utente (visibile)   │
│  NomeTask: "3D modeling"      ← Nome descrittivo          │
│  NrOrdin: 1010                ← Numero ordinamento         │
│  CategoryId: 1                ← Categoria (Design)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘

         ↓ Visualizzato all'utente come ↓

┌──────────┬──────────────┬───────────┐
│ DES-002  │ 3D modeling  │ Design    │
└──────────┴──────────────┴───────────┘
   ↑
   ItemID (il codice che l'utente vede e usa)
```

---

## Domande Frequenti

### Q: Perché abbiamo bisogno di ItemID se c'è già TaskID?
**A**: Il `TaskID` è un numero sequenziale del database (1, 2, 3...) che non ha significato per l'utente. L'`ItemID` è un codice leggibile e significativo (es: "DES-001") che l'utente può usare per identificare rapidamente il task.

### Q: Posso cambiare l'ItemID dopo aver creato il task?
**A**: Sì, ma assicurati che il nuovo codice sia univoco. Se il task è già usato in progetti, il cambio potrebbe creare confusione.

### Q: Cosa succede se due task hanno lo stesso NrOrdin?
**A**: Il sistema impedisce duplicati **nella stessa categoria**. Puoi avere lo stesso `NrOrdin` in categorie diverse.

### Q: Devo preoccuparmi di NrOrdin quando creo un task?
**A**: No! Il sistema lo calcola automaticamente. Devi solo preoccuparti di scegliere un buon `ItemID`.

---

## Conclusione

- **TaskID**: Uso interno del database (non ti preoccupare)
- **ItemID**: Il "nome in codice" del task (sceglilo con cura!)
- **NrOrdin**: L'ordine di visualizzazione (lascia che il sistema lo gestisca)

**Focus principale**: Concentrati su scegliere buoni **ItemID** significativi e consistenti! 🎯
