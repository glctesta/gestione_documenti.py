# Ordinamento dei Task per ItemID

## Modifica Implementata

I task nella lista del tab "Catalogo Task" sono ora ordinati per **ItemID** (codice identificativo) invece che per **NrOrdin** (numero d'ordine interno).

## File Modificato

**`npi/windows/config_window.py`** - Metodo `_load_tasks()`

## Comportamento

### Prima (ordinamento per NrOrdin)
```
Lista Task:
├─ DES-003  | Technical drawings    | Design     (NrOrdin: 1005)
├─ DES-001  | Initial sketches      | Design     (NrOrdin: 1010)
├─ DES-002  | 3D modeling           | Design     (NrOrdin: 1015)
├─ MAT-020  | Material testing      | Materials  (NrOrdin: 2005)
└─ MAT-010  | Supplier qualification| Materials  (NrOrdin: 2010)
```
*(Ordine basato su NrOrdin, che è un numero interno)*

### Dopo (ordinamento per ItemID)
```
Lista Task:
├─ DES-001  | Initial sketches      | Design
├─ DES-002  | 3D modeling           | Design
├─ DES-003  | Technical drawings    | Design
├─ MAT-010  | Supplier qualification| Materials
└─ MAT-020  | Material testing      | Materials
```
*(Ordine alfabetico basato su ItemID)*

## Implementazione

```python
# Ordina i task per ItemID prima di visualizzarli
if tasks:
    tasks = sorted(tasks, key=lambda t: t.ItemID or "")
    
    for t in tasks:
        # Inserisci nella treeview...
```

## Vantaggi

1. ✅ **Più intuitivo**: L'utente vede i task ordinati per il codice che ha assegnato
2. ✅ **Prevedibile**: Se usi una convenzione come `DES-001`, `DES-002`, l'ordine è naturale
3. ✅ **Flessibile**: Puoi usare qualsiasi schema di codifica (numerico, alfanumerico, gerarchico)
4. ✅ **Indipendente**: Non dipende dal NrOrdin interno del sistema

## Differenza tra NrOrdin e ItemID

### NrOrdin (Numero d'Ordine)
- **Scopo**: Ordinamento interno e calcolo automatico
- **Generato**: Automaticamente dal sistema (es: 1005, 1010, 2005)
- **Visibile**: Solo in modifica task
- **Uso**: Ordinamento nei progetti e workflow interni

### ItemID (Codice Identificativo)
- **Scopo**: Identificazione leggibile del task
- **Generato**: Manualmente dall'utente (es: DES-001, MAT-010)
- **Visibile**: Sempre (colonna principale)
- **Uso**: Comunicazione, ricerca, riferimenti

## Esempio Pratico

Se hai questa convenzione di codifica:
```
DES-001: Initial sketches
DES-002: 3D modeling
DES-003: Technical drawings
MAT-010: Source materials
MAT-020: Supplier qualification
TEST-001: Functional testing
```

La lista mostrerà i task in questo ordine alfabetico, indipendentemente dal loro NrOrdin interno:
```
DES-001
DES-002
DES-003
MAT-010
MAT-020
TEST-001
```

## Note

- L'ordinamento è **case-sensitive** (maiuscole prima delle minuscole)
- Se ItemID è NULL o vuoto, il task apparirà all'inizio della lista
- L'ordinamento si applica sia quando visualizzi tutti i task che quando filtri per categoria
- Il NrOrdin continua ad essere usato internamente per l'ordinamento nei progetti

## Raccomandazione

Per ottenere il miglior risultato visivo, usa una **convenzione consistente** per ItemID:

✅ **Buone convenzioni**:
```
DES-001, DES-002, DES-003, ...
MAT-010, MAT-020, MAT-030, ...
1.1, 1.2, 1.3, 2.1, 2.2, ...
```

❌ **Da evitare** (ordine non intuitivo):
```
DES-1, DES-2, DES-10, DES-20  → ordine: DES-1, DES-10, DES-2, DES-20
Task1, Task2, Task10          → ordine: Task1, Task10, Task2
```

**Suggerimento**: Usa sempre lo **zero padding** nei numeri (es: `001` invece di `1`) per mantenere l'ordine corretto.
