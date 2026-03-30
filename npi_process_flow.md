# Flusso Logico del Processo NPI (New Product Introduction)

Diagramma completo del ciclo di vita di un progetto NPI nel sistema TraceabilityRS.

---

## Diagramma di Flusso Generale

```mermaid
flowchart TD
    START(["🚀 START: Nuova Richiesta NPI"]) --> SETUP

    subgraph SETUP["1️⃣ SETUP & CONFIGURAZIONE"]
        direction TB
        S1["Creazione/Selezione Prodotto\n(Cliente, Codice, Nome, Versione)"]
        S2["Creazione Progetto NPI\n(ProgettiNPI → WaveNPI)"]
        S3{"Aggiungere\nTask di Default?"}
        S4["Recruitment automatico\nCategorie + Task dal Catalogo"]
        S5["Configurazione manuale\ntask e categorie"]
        S1 --> S2 --> S3
        S3 -->|Sì| S4
        S3 -->|No| S5
    end

    SETUP --> PLAN

    subgraph PLAN["2️⃣ PIANIFICAZIONE"]
        direction TB
        P1["Assegnazione Owner (Responsabile)\nper ogni Task"]
        P2["Definizione Date\n(DataInizio / DataScadenza)"]
        P3["Creazione Dipendenze\n(Predecessore → Successore)"]
        P4["Impostazione Target NPI\n(Milestone Finale)"]
        P5["Upload Documenti\n(Disegni, BOM, Certificati)"]
        P1 --> P2 --> P3 --> P4 --> P5
    end

    PLAN --> NOTIFY_ASSIGN
    NOTIFY_ASSIGN["📧 Email di Assegnazione Task\n(Notifica automatica all'Owner)"]

    NOTIFY_ASSIGN --> EXEC

    subgraph EXEC["3️⃣ ESECUZIONE & MONITORAGGIO"]
        direction TB
        E1["Task in lavorazione\n(Stato: Da Fare → In Lavorazione)"]
        E2["Aggiornamento Progresso\n(%, Note, Documenti)"]
        E3{"Task\ncompletato\nin tempo?"}
        E4["✅ Completato OK\n(DataCompletamento ≤ DataScadenza)"]
        E5["⏰ Completato in Ritardo\n(DataCompletamento > DataScadenza)"]
        E6["⚠️ Task Scaduto\n(non completato, DataScadenza < Oggi)"]
        E1 --> E2 --> E3
        E3 -->|Sì| E4
        E3 -->|No, ma completato| E5
        E3 -->|Non completato| E6
    end

    EXEC --> MONITOR

    subgraph MONITOR["4️⃣ SISTEMA DI NOTIFICHE AUTOMATICHE"]
        direction TB
        M1["⏰ Controllo Giornaliero\n(08:00 / 09:00 / 14:00)"]
        M2{"Tipo di\nalert?"}
        M3["📧 Task Due Tomorrow\n(Scadenza = Domani)"]
        M4["🚨 Task Overdue\n(Scaduto e non completato)"]
        M5["📊 Risk Assessment Progetto\n(Analisi percorso critico)"]
        M6{"Livello\ndi rischio?"}
        M7["🟡 LOW: Buffer ampio"]
        M8["🟠 MEDIUM: >15% ritardo\no 1+ task critico"]
        M9["🔴 HIGH: >30% ritardo\no 3+ task critici"]
        M10["⛔ CRITICAL: Task critico\n+ deadline ≤ 7gg"]

        M1 --> M2
        M2 -->|Scadenza vicina| M3
        M2 -->|Scaduto| M4
        M2 -->|Analisi progetto| M5
        M5 --> M6
        M6 --> M7
        M6 --> M8
        M6 --> M9
        M6 --> M10
    end

    E4 & E5 --> MILESTONE_CHECK

    subgraph MILESTONE_CHECK["5️⃣ VALIDAZIONE MILESTONE FINALE"]
        direction TB
        V1{"Il task completato\nè il Target NPI?"}
        V2["Prosegui con\ni task rimanenti"]
        V3{"Tutti i task\nprecedenti sono\ncompletati?"}
        V4["❌ Blocco: mostra elenco\ntask non completati"]
        V5["✅ Validazione superata"]
        V1 -->|No| V2
        V1 -->|Sì| V3
        V3 -->|No| V4
        V3 -->|Sì| V5
    end

    V4 -->|"Correzione"| EXEC
    V2 -->|"Prossimo task"| EXEC

    V5 --> CLOSE

    subgraph CLOSE["6️⃣ CHIUSURA PROGETTO"]
        direction TB
        C1["Progetto marcato come Chiuso\n(StatoProgetto = Chiuso)"]
        C2["📧 Email di Completamento\n(Broadcast a tutti i partecipanti)"]
        C3["📊 KPI Summary:\n• On-Time Rate %\n• Late Rate %\n• Costi Totali €"]
        C1 --> C2 --> C3
    end

    CLOSE --> END_STATE(["✅ FINE: Progetto NPI Completato"])

    E6 --> MONITOR
```

---

## Flusso Dipendenze e Validazione Date

```mermaid
flowchart LR
    subgraph RULES["Regole di Validazione"]
        R1["DataInizio ≤ DataScadenza"]
        R2["Task.DataInizio ≥ Predecessore.DataScadenza"]
        R3["Task.DataScadenza ≤ ScadenzaProgetto"]
        R4["ScadenzaProgetto ≥ max DataScadenza di tutti i task"]
    end
```

---

## Flusso Gerarchia Progetti (Parent/Child)

```mermaid
flowchart TD
    PARENT["📦 Progetto PADRE"] --> CHILD1["📄 Figlio 1\n(stesso Cliente)"]
    PARENT --> CHILD2["📄 Figlio 2\n(stesso Cliente)"]
    PARENT --> CHILD3["📄 Figlio N\n(stesso Cliente)"]

    PARENT -.->|"Non può chiudersi\nfinché i figli\nnon sono completati"| GUARD["🛡️ Completion Guard"]

    CHILD1 -.->|"Non può essere\npadre a sua volta"| DEPTH["Max profondità = 1 livello"]
```

---

## Riepilogo Fasi del Processo

| # | Fase | Attori | Output |
|:--|:-----|:-------|:-------|
| 1 | **Setup** | Project Owner | Progetto NPI + Wave + Task da catalogo |
| 2 | **Pianificazione** | Project Owner | Date, dipendenze, milestone, documenti |
| 3 | **Esecuzione** | Task Owners | Avanzamento task, upload documenti |
| 4 | **Monitoraggio** | Sistema automatico | Email alert (scadenze, ritardi, rischi) |
| 5 | **Validazione** | Sistema | Controllo sequenziale milestone |
| 6 | **Chiusura** | Sistema + Project Owner | KPI report, email broadcast, archiviazione |

---

## Attori e Ruoli

| Ruolo | Responsabilità |
|:------|:---------------|
| **Project Owner** | Crea progetto, assegna task, gestisce gerarchia, chiude progetto |
| **Task Owner** | Esegue task assegnati, aggiorna stato e documenti |
| **Sistema (Background)** | Notifiche automatiche, risk assessment, validazione milestone |
| **Admin** | Configurazione catalogo, categorie di default, gestione soggetti |

---

## Componenti Software Coinvolti

| Componente | File | Ruolo |
|:-----------|:-----|:------|
| Dashboard | `dashboard_window.py` | Vista globale progetti + KPI |
| Gestione Progetto | `project_window.py` | Task, documenti, metadata |
| Gantt | `gantt_window.py` | Visualizzazione timeline |
| Backend NPI | [npi_manager.py](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/npi/npi_manager.py) | Logica business, validazione, sorting |
| Notifiche Auto | [npi_auto_notifications.py](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/npi/npi_auto_notifications.py) | Risk assessment, email giornaliere |
| Notifiche Task | [notification_manager.py](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/npi/notification_manager.py) | Alert scadenze singoli task |
| Configurazione | `config_window.py` | Catalogo, categorie, default |
