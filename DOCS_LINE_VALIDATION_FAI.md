# Documentazione - Modulo Validazione Linea FAI

## Panoramica
Il modulo di validazione linea (FAI - First Article Inspection) permette di gestire le ispezioni della prima produzione per verificare che tutti i processi siano conformi agli standard definiti.

## Funzionalità Principali

### 1. Selezione Ordine e Prodotto
- Selezione dell'ordine di produzione dalla lista degli ordini recenti (dal 01/08/2025)
- Visualizzazione automatica del codice prodotto associato
- Campi per Cliente e Quantità

### 2. Tipo di Validazione
Il sistema supporta 5 tipi di validazione (checkbox):
- **NPI (PRESERIE)** - Validazione per nuovi prodotti in preserie
- **TEST** - Validazione per test
- **PRODUZIONE** - Validazione per produzione standard
- **VARIAȚIA STANDARD A PROCESULUI** - Variazione standard del processo
- **Others** - Altri tipi di validazione

### 3. Checklist Step FAI
Ogni validazione include una checklist dinamica con gli step definiti nel template FAI:
- **Step**: Nome dello step e numero documento di riferimento
- **Descrizione**: Descrizione dettagliata dello step
- **Equipment**: Equipaggiamento utilizzato (se applicabile)
- **OK / Not OK**: Checkbox mutuamente esclusivi per indicare l'esito
- **Note**: Campo testo per annotazioni

### 4. Salvataggio Dati
Il sistema salva:
- **Header** della validazione con tipo e timestamp in `FaiLogHeathers`
- **Dettagli** per ogni step verificato in `FaiLogs`

## Struttura Database

### Tabella: fai.FaiLogHeathers
Contiene le intestazioni delle validazioni:
```sql
- FaiLogId (PK, IDENTITY)
- NPI (bit) - Flag NPI
- Test (bit) - Flag Test
- PRODUCTION (bit) - Flag Produzione
- StandardProcessDeviation (bit) - Flag Deviazione Standard
- Others (bit) - Flag Altri
- DateIn, UserIn - Timestamp e utente creazione
- DateOut, UserOut - Timestamp e utente chiusura (soft delete)
```

### Tabella: fai.FaiLogs
Contiene i dettagli di ogni step validato:
```sql
- FaiLogDetailId (PK, IDENTITY)
- FaiLogId (FK) - Riferimento all'header
- FaiStepDetailId (FK) - Riferimento allo step del template
- isOK (bit) - True se OK, False se Not OK
- Notes (nvarchar) - Note dello step
- DateIn, UserIn - Timestamp e utente creazione
- DateOut, UserOut - Timestamp e utente chiusura (soft delete)
```

## Query Principali

### Carica Step FAI
```sql
SELECT 
    d.[FaiStepDetailId],
    s.StepName + ' -> ' + t.NrDocument as Step,
    d.[StepDetail],
    ISNULL(e.[Description], '') + ' ' + ISNULL(e.SerialNumber, '') as Equipment,
    s.OrderinList
FROM [Traceability_RS].[fai].[FaiStepDetails] d
INNER JOIN [Traceability_RS].[fai].FaiSteps s ON d.FatStepId = s.FatStepId AND s.DateOut IS NULL
LEFT JOIN [Traceability_RS].[fai].FaiEquipments e ON d.FaiEquipmentId = e.FaiEquipmentid
INNER JOIN [Traceability_RS].[fai].FaiTemplates t ON t.FaiTemplateId = s.FaiTemplateId
WHERE d.DateOut IS NULL
ORDER BY s.OrderinList
```

### Carica Ordini Disponibili
```sql
SELECT o.IDOrder, o.OrderNumber, p.ProductCode, p.ProductName
FROM Traceability_RS.dbo.Orders o  
INNER JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
WHERE o.OrderDate >= '2025-08-01'
ORDER BY o.OrderNumber
```

## Utilizzo

### 1. Apertura Modulo
Dal menu principale: **Produzione → Dichiarazioni → Validazione linea → Validazioni**

### 2. Compilazione Form
1. Selezionare l'ordine dal dropdown
2. Inserire Cliente e Quantità
3. Selezionare il tipo di validazione (almeno uno)
4. Scorrere la checklist e marcare ogni step come OK o Not OK
5. Aggiungere note dove necessario

### 3. Salvataggio
Cliccare su "Salva Validazione" per registrare i dati nel database.

### 4. Stato
La barra di stato in basso mostra:
- Messaggi di errore/successo
- ID della validazione salvata

## Permessi
L'accesso al modulo richiede l'autorizzazione `validazione_line` nella tabella permissions.

## File Coinvolti

- **line_validation_gui.py** - Interfaccia grafica principale
- **SQL_SETUP_FAI_VALIDATIONS.sql** - Script setup database
- **main.py** - Integrazione nel menu (metodi `open_line_validations_with_login` e `_open_line_validations`)

## Note Implementative

### Checkbox Mutuamente Esclusivi
OK e Not OK sono gestiti in modo esclusivo:
- Selezionando OK, Not OK viene deselezionato automaticamente
- Selezionando Not OK, OK viene deselezionato automaticamente

### Scroll Dinamico
La lista degli step supporta lo scroll con la rotella del mouse per form con molti step.

### Layout Adattivo
Il form rispetta il layout del documento cartaceo FAI originale per facilitare la transizione digitale.

## Sviluppi Futuri

1. **Stampa PDF** - Generazione PDF del form compilato
2. **Storico Validazioni** - Vista delle validazioni precedenti per lo stesso prodotto
3. **Filtri** - Ricerca e filtro delle validazioni per data, prodotto, tipo
4. **Dashboard** - Statistiche sulle validazioni (% OK/Not OK per step)
5. **Export Excel** - Esportazione dati per analisi
6. **Firma Digitale** - Integrazione firma digitale operatore e supervisore
