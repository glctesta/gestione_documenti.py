# Feature Proposal — Gestione integrata Etichette di Produzione

> **⚠️ Documento obsoleto:** questa proposta è stata implementata. Vedere `PrintLabelForProduction_Spec_v2.0.md` per lo stato attuale del modulo Etichette Produzione.

**Programma:** DocumentManagement
**Area:** Materiali indiretti / Preparazione kit / Verifica prelievi
**Stato:** Proposta / Analisi funzionale
**Data:** 12 agosto 2026

---

## 1. Contesto

Il programma DocumentManagement dispone già di una sezione dedicata alla richiesta, gestione e prelievo dei **materiali indiretti**. Tra questi rientrano anche **etichette** e **ribbon** per la loro stampa.

Le funzionalità oggi presenti sono distribuite su tre menu principali:

| Menu / Entry point | Funzione | Stato |
|---|---|---|
| `open_kit_picking_with_login` | Preparazione dei kit e prelievo da parte della produzione | Operativo |
| `_open_production_labels_bom_with_auth` | Gestione BOM etichette e stampa in produzione | **Non ultimato** |
| `_open_request_indirect_materials` | Richieste di materiali indiretti dalla produzione e relativa consegna | Operativo |

È inoltre già disponibile una procedura (interfaccia **browser**, lanciata da DocumentManagement) che gestisce l'associazione:

```
Prodotto  →  Etichetta/e (1..N)  →  Ribbon  →  Stampante
```

---

## 2. Problema

Le **etichette non sono presenti in BOM**. Ne consegue che:

- la loro gestione a livello di materiali è **farraginosa** e non integrata nel flusso di prelievo standard;
- non esiste un controllo di disponibilità sistematico prima dell'ingresso dell'ordine in produzione;
- si verificano **frequenti ritardi di produzione** dovuti alla mancanza di etichette al momento del bisogno;
- il fabbisogno viene calcolato manualmente o rilevato solo quando l'ordine è già in linea.

---

## 3. Obiettivo

Estendere la fase di **verifica materiali** degli ordini in ingresso in produzione affinché includa automaticamente il **fabbisogno etichette**, calcolato a partire dalle associazioni `Prodotto → Etichetta → Ribbon → Stampante`, e ne governi il prelievo, la distribuzione per ordine e la tracciabilità.

**Risultato atteso:** azzeramento dei fermi produzione causati da mancanza etichette, con un flusso allineato a quello già esistente per i materiali PTHM.

---

## 4. Dati già disponibili nel sistema

La proposta non richiede nuove fonti dati: tutte le informazioni necessarie sono già presenti.

1. **Ordini in ingresso in produzione** — ordini che non hanno ancora alcuna quantità dichiarata nella prima fase (**AOI**).
2. **Gli stessi ordini** compaiono nella lista per la **verifica delle quantità**.
3. **Verifica quantità** — eseguita oggi su tutti i materiali **PTHM** presenti in BOM di ciascun prodotto.
4. **Associazioni etichette** — mappatura `Prodotto → Etichetta/e → Ribbon → Stampante` gestita via browser.
5. **Anagrafica etichette** — codice etichetta, tipo, ribbon compatibile, stampante assegnata.

> Incrociando (1)+(3) con (4) si ottiene, per la giornata di prelievo/verifica, l'elenco completo delle etichette necessarie per codice e per ordine.

---

## 5. Logica funzionale proposta

### 5.1 Individuazione degli ordini

Selezione degli ordini che:
- stanno per entrare in produzione;
- **non hanno quantità dichiarate in AOI**;
- sono presenti nella lista di verifica quantità/prelievo **della giornata**.

### 5.2 Determinazione del fabbisogno etichette

Per ciascun ordine selezionato:

```
Per ogni prodotto dell'ordine:
    Recupera le etichette associate (1..N)
    Per ogni etichetta:
        fabbisogno_ordine = qta_ordine × n_etichette_per_pezzo
        scarto            = f(tipo_etichetta)        ← parametrizzabile
        fabbisogno_totale = fabbisogno_ordine + scarto
```

Lo **scarto tecnico** è parametrizzato **per tipo di etichetta** (valore fisso, percentuale, o minimo garantito — vedi §7).

### 5.3 Aggregazione per codice etichetta

Tutte le righe di fabbisogno vengono **raggruppate per codice etichetta**, sommando le quantità di tutti gli ordini della giornata che utilizzano quel codice.

Questo consente **un solo prelievo per codice**, invece di N prelievi frammentati.

### 5.4 Aggancio a un ordine di prelievo

Il totale aggregato per codice viene **aggiunto a un ordine di produzione prescelto** durante la sua fase di verifica, come riga di materiale indiretto.

Nella **nota associata all'ordine prescelto** vengono riportati:

- l'elenco degli **ordini** che concorrono al fabbisogno;
- la **quantità prelevata per ciascun ordine** (netto + scarto tecnico);
- il **codice etichetta** di riferimento;
- ribbon e stampante associati.

### 5.5 Distribuzione per ordine

Una volta effettuata la verifica del codice a cui fanno riferimento tutti gli ordini coinvolti, la quantità totale prelevata viene **redistribuita** — nella quantità corretta e comprensiva di scarto tecnico — su ciascun ordine che necessita di etichette.

---

## 6. Flusso operativo (end-to-end)

```
[1] Ordini prossimi alla produzione (qta AOI = 0)
              │
              ▼
[2] Lista verifica quantità giornaliera  ──► materiali PTHM (da BOM)
              │
              └──► NEW: materiali etichette (da associazioni Prodotto→Etichetta)
                             │
                             ▼
[3] Calcolo fabbisogno per ordine  (+ scarto tecnico per tipo etichetta)
                             │
                             ▼
[4] Aggregazione per CODICE ETICHETTA (tutti gli ordini del giorno)
                             │
                             ▼
[5] Riga di prelievo su ordine prescelto + NOTA con dettaglio ordini/quantità
                             │
                             ▼
[6] Prelievo fisico da magazzino (flusso materiali indiretti esistente)
                             │
                             ▼
[7] Verifica codice etichetta prelevato
                             │
                             ▼
[8] Distribuzione quantità per singolo ordine (netto + scarto)
                             │
                             ▼
[9] Consegna in produzione + stampa (ribbon/stampante associati)
```

---

## 7. Parametri da introdurre

| Parametro | Livello | Descrizione | Esempio |
|---|---|---|---|
| `scarto_tecnico_tipo` | Tipo etichetta | Quantità o % di scarto da aggiungere al fabbisogno netto | 3% oppure 20 pz |
| `scarto_minimo` | Tipo etichetta | Quantità minima di scarto indipendentemente dal volume | 10 pz |
| `arrotondamento` | Tipo etichetta | Arrotondamento a multiplo di rotolo/confezione | multipli di 500 |
| `etichette_per_pezzo` | Prodotto → Etichetta | Numero di etichette per unità di prodotto | 1, 2, … |
| `soglia_riordino_ribbon` | Ribbon | Alert su consumo ribbon associato | — |

---

## 8. Impatti sui moduli esistenti

### 8.1 `open_kit_picking_with_login` — Preparazione kit e prelievo
- Aggiunta della **sezione etichette** al kit, alimentata dal calcolo aggregato di §5.3.
- Le righe etichetta vanno evidenziate come **materiale indiretto non-BOM**, per distinguerle dai PTHM.
- Il kit deve poter essere confermato solo se le righe etichetta risultano prelevate o esplicitamente derogate.

> ⚠️ **Punto aperto:** la specifica di dettaglio sui moduli di preparazione kit è rimasta incompleta nella descrizione iniziale. Da definire: se le etichette costituiscono un kit separato o righe aggiuntive del kit esistente, e chi (magazzino o produzione) esegue materialmente il prelievo.

### 8.2 `_open_production_labels_bom_with_auth` — BOM etichette e stampa
- Modulo da **completare**: diventa il punto centrale di consultazione BOM-etichette.
- Deve esporre le associazioni `Prodotto → Etichetta → Ribbon → Stampante` in sola lettura per la produzione e in modifica per gli utenti autorizzati.
- Da qui parte la **stampa** in produzione, con instradamento automatico sulla stampante associata.

### 8.3 `_open_request_indirect_materials` — Richieste materiali indiretti
- Riuso del flusso di richiesta/consegna esistente per il prelievo aggregato delle etichette.
- Le richieste generate automaticamente dal calcolo fabbisogno devono essere distinguibili da quelle manuali (flag origine: `AUTO` / `MANUALE`).

### 8.4 Interfaccia browser associazioni
- Aggiunta dei campi di parametrizzazione scarto tecnico per tipo etichetta.
- Validazione: nessun prodotto in produzione deve restare privo di associazione etichetta (report di copertura).

---

## 9. Casi da gestire

- **Prodotto senza associazione etichetta** → segnalazione bloccante o warning in fase di verifica.
- **Etichette multiple per prodotto** → tutte le righe devono confluire nell'aggregazione.
- **Stesso codice etichetta su più prodotti/ordini** → aggregazione corretta e distribuzione proporzionale.
- **Ordine aggiunto/rimosso dopo il prelievo aggregato** → ricalcolo o gestione della differenza.
- **Giacenza insufficiente** → alert anticipato prima dell'ingresso in produzione (obiettivo primario del progetto).
- **Ribbon mancante o incompatibile** → blocco della stampa con notifica.
- **Deroga/prelievo parziale** → tracciamento del residuo per ordine.

---

## 10. Benefici attesi

- Fabbisogno etichette **calcolato automaticamente**, senza intervento manuale.
- **Un solo prelievo per codice** al giorno invece di prelievi frammentati.
- **Anticipo** della verifica disponibilità rispetto all'ingresso in produzione.
- **Tracciabilità completa**: quale ordine ha consumato quali etichette e in che quantità.
- Riduzione/eliminazione dei **fermi linea per mancanza etichette**.
- Allineamento del flusso etichette a quello già consolidato dei materiali PTHM.

---

## 11. Prossimi passi

1. Completare la specifica del comportamento nei moduli di preparazione kit (§8.1 — punto aperto).
2. Definire la struttura dati per la parametrizzazione dello scarto tecnico per tipo etichetta.
3. Definire la regola di scelta dell'**ordine prescelto** su cui agganciare il prelievo aggregato.
4. Definire il formato standard della **nota** allegata all'ordine (§5.4).
5. Completare il modulo `_open_production_labels_bom_with_auth`.
6. Prototipo sul flusso di una giornata di produzione reale per validazione.
