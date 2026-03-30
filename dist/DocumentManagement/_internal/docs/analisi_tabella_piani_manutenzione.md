# Analisi Tabella: PianiManutenzioneMacchina

## Risultato della Ricerca

**❌ LA TABELLA `[Traceability_RS].[eqp].[PianiManutenzioneMacchina]` NON È UTILIZZATA NEL CODICE**

Ho effettuato una ricerca completa in tutti i file Python del progetto e questa tabella **non compare mai** nel codice sorgente.

---

## Tabelle dello Schema `eqp` Effettivamente Utilizzate

Ecco l'elenco completo delle tabelle dello schema `[eqp]` che **sono effettivamente utilizzate** nel codice delle manutenzioni:

### 1. **`eqp.Equipments`** ⭐ (Tabella Principale)
**Utilizzo**: Gestione completa delle macchine/equipaggiamenti

**Operazioni**:
- ✅ **SELECT**: Lettura dati macchine
- ✅ **INSERT**: Aggiunta nuove macchine
- ✅ **UPDATE**: Modifica dati macchine (non esplicito, ma tramite stored procedures)

**File**: `main.py` (linee 819, 848, 874, 2789, 3262, 5504, 7006, 7053, 7087, 7128, 7233)

**Campi Principali**:
- `EquipmentId`, `InternalName`, `SerialNumber`, `BrandId`, `EquipmentTypeId`, `ParentPhaseId`
- `IsFixture`, `IsStensil`, `MustCalibrated`

---

### 2. **`eqp.CompitiManutenzione`** ⭐ (Task di Manutenzione)
**Utilizzo**: Gestione dei compiti/task di manutenzione associati alle macchine

**Operazioni**:
- ✅ **SELECT**: Lettura task esistenti
- ✅ **INSERT**: Creazione nuovi task ([main.py:6588](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6588))
- ✅ **UPDATE**: Modifica task esistenti
- ✅ **DELETE**: Cancellazione task ([main.py:6545](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6545))

**File**: `main.py` (linee 6505, 6545, 6588, 7584, 7615, 7679)

**Finestra Associata**: `AddMaintenanceTasksWindow` in `maintenance_gui.py`

---

### 3. **`eqp.ProgrammedInterventions`** ⭐ (Cicli/Interventi Programmati)
**Utilizzo**: Definizione dei tipi di intervento di manutenzione (es. "Ogni 100 ore", "Mensile", ecc.)

**Operazioni**:
- ✅ **SELECT**: Lettura interventi programmati ([main.py:6266](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6266))
- ✅ **INSERT**: Creazione nuovi cicli ([main.py:6294](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6294))
- ✅ **UPDATE**: Modifica cicli esistenti (soft delete con `DateOut`)

**File**: `main.py` (linee 6266, 6294)

**Finestra Associata**: `TaskCyclesManagerWindow` in `maintenance_gui.py`

**Campi Principali**:
- `ProgrammedInterventionId`, `TimingDescriprion`, `Value`, `OrdinePrn`
- `IsFixture`, `IsStensil`, `NoCycle`, `DateOut` (soft delete)

---

### 4. **`eqp.LogManutenzioni`** (Log Esecuzioni)
**Utilizzo**: Registro delle manutenzioni effettivamente eseguite

**Operazioni**:
- ✅ **SELECT**: Lettura storico manutenzioni ([main.py:5665](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L5665), 6281, 7580, 7611)
- ✅ **INSERT**: Registrazione nuove esecuzioni (tramite finestra compilazione schede)

**File**: `main.py` (linee 5665, 6281, 7580, 7611)

**Campi Principali**:
- `DataEsecuzione`, `IdManutentore`, `NoteGenerali`, `EquipmentId`

---

### 5. **`eqp.EquipmentBrands`** (Marche Equipaggiamenti)
**Utilizzo**: Gestione delle marche/brand delle macchine

**Operazioni**:
- ✅ **SELECT**: Lettura brand ([main.py:6419](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6419), 7202)
- ✅ **INSERT**: Aggiunta nuovi brand ([main.py:6433](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6433))
- ✅ **DELETE**: Cancellazione brand ([main.py:5280](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L5280))

**File**: `main.py` (linee 5259, 5280, 6419, 6433, 7202)

**Finestra Associata**: `BrandManagerWindow` in `maintenance_gui.py`

---

### 6. **`eqp.EquipmentTypes`** (Tipi Equipaggiamenti)
**Utilizzo**: Definizione dei tipi di macchine (es. "SMT", "ICT", "FCT", ecc.)

**Operazioni**:
- ✅ **SELECT**: Lettura tipi ([main.py:7212](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L7212))
- ✅ **INSERT**: Aggiunta nuovi tipi (tramite `EquipmentTypesManagerWindow`)
- ✅ **UPDATE**: Modifica tipi esistenti (tramite `EquipmentTypesManagerWindow`)
- ✅ **DELETE**: Cancellazione tipi (tramite `EquipmentTypesManagerWindow`)

**File**: `main.py` (linea 7212), `maintenance_gui.py` (nuova finestra appena aggiunta)

**Finestra Associata**: `EquipmentTypesManagerWindow` in `maintenance_gui.py`

---

### 7. **`eqp.EquipmentChanges`** (Log Modifiche Macchine)
**Utilizzo**: Tracciamento delle modifiche apportate alle macchine

**Operazioni**:
- ✅ **SELECT**: Lettura storico modifiche ([main.py:7062](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L7062))
- ✅ **INSERT**: Registrazione modifiche ([main.py:7185](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L7185))

**File**: `main.py` (linee 7062, 7185)

**Campi Principali**:
- `EquipmentId`, `Changed`, `WhoChange`, `DateChange`

---

### 8. **`eqp.EquipmentMantainanceDocs`** (Documenti Manutenzione)
**Utilizzo**: Archiviazione documenti allegati alle macchine

**Operazioni**:
- ✅ **SELECT**: Lettura documenti ([main.py:6884](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6884), 7067)
- ✅ **INSERT**: Caricamento nuovi documenti ([main.py:6968](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6968))

**File**: `main.py` (linee 6884, 6968, 7067)

**Campi Principali**:
- `EquipmentId`, `FileName`, `DocumentSource` (VARBINARY), `UploadedBy`, `DateSys`

---

### 9. **`eqp.Calibrations`** (Calibrazioni)
**Utilizzo**: Gestione delle calibrazioni delle macchine

**Operazioni**:
- ✅ **SELECT**: Lettura dati calibrazioni ([main.py:2792](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L2792), 3290)

**File**: `main.py` (linee 2792, 3290)

---

### 10. **`eqp.CalibrationWarnings`** (Avvisi Calibrazione)
**Utilizzo**: Tracciamento degli avvisi di calibrazione inviati

**Operazioni**:
- ✅ **SELECT**: Verifica avvisi esistenti ([main.py:2801](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L2801), 2838)
- ✅ **INSERT**: Registrazione nuovi avvisi ([main.py:2835](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L2835))

**File**: `main.py` (linee 2801, 2835, 2838)

---

### 11. **`eqp.SparePartMaterials`** (Materiali Ricambi)
**Utilizzo**: Catalogo dei materiali di ricambio

**Operazioni**:
- ✅ **SELECT**: Lettura materiali ([main.py:5859](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L5859), 5870, 5882, 5900, 5998, 6862)
- ✅ **INSERT**: Aggiunta nuovi materiali ([main.py:5911](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L5911), 6697)
- ✅ **DELETE**: Cancellazione materiali ([main.py:5955](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L5955))

**File**: `main.py` (linee 5859, 5870, 5882, 5900, 5911, 5955, 5998, 6697, 6862)

---

### 12. **`eqp.SparePartParents`** (Associazione Ricambi-Macchine)
**Utilizzo**: Collegamento tra materiali di ricambio e macchine

**Operazioni**:
- ✅ **SELECT**: Lettura associazioni ([main.py:5967](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L5967))
- ✅ **INSERT**: Creazione associazioni ([main.py:5981](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L5981))
- ✅ **DELETE**: Rimozione associazioni ([main.py:5978](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L5978))

**File**: `main.py` (linee 5967, 5978, 5981)

---

### 13. **`eqp.RequestSpareParts`** (Richieste Ricambi)
**Utilizzo**: Gestione delle richieste di materiali di ricambio

**Operazioni**:
- ✅ **INSERT**: Creazione nuove richieste ([main.py:6765](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6765))

**File**: `main.py` (linea 6765)

---

## Conclusione

### ❌ Tabella NON Utilizzata
- **`eqp.PianiManutenzioneMacchina`** - Non presente nel codice

### ✅ Tabelle Utilizzate nel Sistema Manutenzioni

**Tabelle Principali** (con operazioni CRUD complete):
1. `eqp.Equipments` - Macchine
2. `eqp.CompitiManutenzione` - Task di manutenzione
3. `eqp.ProgrammedInterventions` - Cicli programmati
4. `eqp.EquipmentBrands` - Marche
5. `eqp.EquipmentTypes` - Tipi equipaggiamenti

**Tabelle di Supporto**:
6. `eqp.LogManutenzioni` - Storico esecuzioni
7. `eqp.EquipmentChanges` - Log modifiche
8. `eqp.EquipmentMantainanceDocs` - Documenti
9. `eqp.Calibrations` - Calibrazioni
10. `eqp.CalibrationWarnings` - Avvisi calibrazione
11. `eqp.SparePartMaterials` - Ricambi
12. `eqp.SparePartParents` - Associazioni ricambi
13. `eqp.RequestSpareParts` - Richieste ricambi

---

## Raccomandazione

Se la tabella `PianiManutenzioneMacchina` esiste nel database ma non è utilizzata nel codice, potrebbe essere:

1. **Tabella obsoleta** - Da rimuovere dal database se non più necessaria
2. **Tabella futura** - Prevista per sviluppi futuri non ancora implementati
3. **Tabella legacy** - Utilizzata da vecchie versioni del software

**Suggerimento**: Verificare con il DBA se questa tabella può essere rimossa o se ci sono piani per utilizzarla in futuro.
