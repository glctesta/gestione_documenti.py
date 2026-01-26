# Validazione OrderInList Unico - FAI Steps

## Data: 2026-01-14

## Descrizione
Implementata validazione per garantire che il campo `OrderInList` sia unico per ogni `FaiTemplateId` nella tabella `FaiSteps`, escludendo i record con `DateOut NOT NULL` (cancellati logicamente).

## Motivazione
Evitare che due step attivi dello stesso template abbiano lo stesso numero di ordine, il che potrebbe causare confusione nella visualizzazione e nell'ordinamento degli step.

---

## Modifiche Implementate

### 1. Validazione Lato Applicazione

#### File: `fai_template_manager.py`
**Metodo modificato:** `StepEditorDialog._save()`

**Implementazione:**
- Prima di salvare uno step (INSERT o UPDATE), viene eseguita una query di controllo
- La query verifica se esiste già uno step con lo stesso `OrderInList` per lo stesso `FaiTemplateId`
- La verifica esclude:
  - Il record corrente (se in modifica)
  - I record con `DateOut NOT NULL` (cancellati logicamente)

**Query di validazione:**
```sql
SELECT COUNT(*) as Count
FROM [Traceability_RS].[fai].[FaiSteps]
WHERE FaiTemplateId = ? 
AND OrderInList = ? 
AND DateOut IS NULL
AND FatStepId != ?
```

**Comportamento:**
- Se trovato un duplicato → Mostra messaggio di errore e impedisce il salvataggio
- Se non trovato → Procede con il salvataggio normalmente

---

### 2. Constraint a Livello Database

#### File: `sql_scripts/ADD_UNIQUE_INDEX_FAI_STEPS_ORDER.sql`

**Implementazione:**
Creato un **UNIQUE FILTERED INDEX** sulla tabella `FaiSteps`:

```sql
CREATE UNIQUE NONCLUSTERED INDEX [UX_FaiSteps_Template_Order_Active]
ON [fai].[FaiSteps] ([FaiTemplateId], [OrderInList])
WHERE [DateOut] IS NULL;
```

**Caratteristiche:**
- **Tipo:** Unique Nonclustered Index
- **Colonne:** `FaiTemplateId`, `OrderInList`
- **Filtro:** `WHERE [DateOut] IS NULL`
- **Vantaggio:** Il filtro permette che record cancellati (con DateOut NOT NULL) possano avere OrderInList duplicati

**Protezione:**
- Impedisce a livello database l'inserimento di duplicati
- Fornisce un ulteriore livello di sicurezza oltre alla validazione applicativa

**Verifica Duplicati:**
Lo script include anche una query per verificare eventuali duplicati esistenti:

```sql
SELECT 
    FaiTemplateId,
    OrderInList,
    COUNT(*) as NumDuplicati
FROM [fai].[FaiSteps]
WHERE DateOut IS NULL
GROUP BY FaiTemplateId, OrderInList
HAVING COUNT(*) > 1;
```

---

### 3. Traduzioni

#### Nuovo messaggio: `order_already_exists`

**Tabelle aggiornate:**
- `[dbo].[Translations]` → IT, EN, RO
- `[dbo].[AppTranslations]` → IT, RO, EN, DE, SV

**Traduzioni:**

| Lingua | Traduzione |
|--------|------------|
| **IT** | Esiste già uno step attivo con questo numero di ordine per il template selezionato. Scegli un numero diverso. |
| **EN** | An active step with this order number already exists for the selected template. Choose a different number. |
| **RO** | Există deja un pas activ cu acest număr de ordine pentru șablonul selectat. Alegeți un număr diferit. |
| **DE** | Es existiert bereits ein aktiver Schritt mit dieser Ordnungszahl für die ausgewählte Vorlage. Wählen Sie eine andere Nummer. |
| **SV** | Det finns redan ett aktivt steg med detta ordningsnummer för den valda mallen. Välj ett annat nummer. |

**File modificati:**
- `sql_scripts/ADD_TRANSLATIONS_FAI_STEPS.sql`
- `sql_scripts/ADD_APPTRANSLATIONS_FAI_STEPS.sql`

---

## Script SQL da Eseguire

### Ordine di Esecuzione:

1. **`ADD_ORDERINLIST_FAI_STEPS.sql`**
   - Aggiunge il campo `OrderInList` se non esiste
   - Inizializza i valori per i record esistenti

2. **`ADD_TRANSLATIONS_FAI_STEPS.sql`**
   - Aggiunge traduzioni alla tabella `Translations`

3. **`ADD_APPTRANSLATIONS_FAI_STEPS.sql`**
   - Aggiunge traduzioni alla tabella `AppTranslations`

4. **`ADD_UNIQUE_INDEX_FAI_STEPS_ORDER.sql`**
   - ⚠️ **IMPORTANTE:** Eseguire DOPO aver verificato/risolto eventuali duplicati
   - Crea l'indice unico filtrato

---

## Test Consigliati

### Test Case 1: Inserimento Duplicato (Stesso Template)
1. Creare uno step con Template A, OrderInList = 1
2. Tentare di creare un altro step con Template A, OrderInList = 1
3. **Risultato Atteso:** Errore di validazione, salvataggio impedito

### Test Case 2: Inserimento Valido (Template Diverso)
1. Creare uno step con Template A, OrderInList = 1
2. Creare uno step con Template B, OrderInList = 1
3. **Risultato Atteso:** Entrambi salvati con successo

### Test Case 3: Modifica con Duplicato
1. Avere uno step esistente con Template A, OrderInList = 2
2. Modificare un altro step dello stesso template cambiando OrderInList da 3 a 2
3. **Risultato Atteso:** Errore di validazione, modifica impedita

### Test Case 4: Record Cancellati (DateOut NOT NULL)
1. Avere uno step cancellato (DateOut NOT NULL) con Template A, OrderInList = 1
2. Creare un nuovo step con Template A, OrderInList = 1
3. **Risultato Atteso:** Salvataggio permesso (il cancellato non conta)

---

## Vantaggi della Soluzione

✅ **Doppia Protezione:**
- Validazione applicativa (user-friendly, messaggio chiaro)
- Constraint database (protezione a livello dati)

✅ **Soft Delete Compatibile:**
- Il filtro `WHERE DateOut IS NULL` permette riutilizzo degli OrderInList dopo cancellazione

✅ **Multilingua:**
- Messaggi di errore in 5 lingue

✅ **Performance:**
- Indice filtrato è più efficiente di un indice completo
- Riduce lo spazio utilizzato dall'indice

---

## Note Tecniche

### Perché un Indice Filtrato?
Un **UNIQUE INDEX** normale impedirebbe di avere lo stesso `OrderInList` anche per record cancellati (con `DateOut NOT NULL`). L'indice filtrato risolve questo problema applicando il vincolo solo ai record attivi.

### Gestione Errori Database
Se l'indice unico viene violato (es. in caso di operazioni dirette sul database), SQL Server genererà un errore che verrà catturato dall'applicazione e mostrato all'utente.

### Best Practice
È consigliabile eseguire prima la validazione applicativa (più veloce e user-friendly) e avere l'indice database come rete di sicurezza.

---

## Conclusione

La validazione è completa e protegge l'integrità dei dati sia lato applicazione che lato database. Gli utenti riceveranno messaggi chiari in caso di tentativi di inserimento duplicati, e il sistema è resiliente contro operazioni dirette sul database.
