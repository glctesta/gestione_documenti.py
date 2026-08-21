# MANUAL DE UTILIZARE — Materiale Indirecte (Materiale de Consum)

**Aplicație:** TraceabilityRS — DocumentManagement  
**Versiune document:** 2.0  
**Data:** 14/08/2026  
**Stare:** Actualizat după ultimele modificări (popup achiziții, conferma ordini, serviciu background, scorie/rientri, rapoarte).

---

## Cuprins

1. [Prezentare generală](#1-prezentare-generală)
2. [Structura meniului](#2-structura-meniului)
3. [Configurare inițială](#3-configurare-inițială)
   - 3.1 Configurare WorkStation (WH / Achiziții)
   - 3.2 Serviciu de notificări în background
4. [Solicitare Materiale Indirecte](#4-solicitare-materiale-indirecte)
5. [Confirmare Materiale (Istoric Cereri)](#5-confirmare-materiale-istoric-cereri)
6. [Conferma ordini (achiziții)](#6-conferma-ordini-achiziții)
7. [Gestione Scorie / Rientri](#7-gestione-scorie-rientri)
8. [Verificare Giacenze și Configurare Scorte Minime](#8-verificare-giacenze-și-configurare-scorte-minime)
9. [Rapoarte, Statistici și Analize](#9-rapoarte-statistici-și-analize)
10. [Notificări și popup](#10-notificări-și-popup)
11. [Generare PDF — Cerere de Material de Consum](#11-generare-pdf--cerere-de-material-de-consum)
12. [Schema Bazei de Date](#12-schema-bazei-de-date)
13. [Fluxul Complet de Lucru](#13-fluxul-complet-de-lucru)
14. [Fișiere implicate](#14-fișiere-implicate)
15. [Note și probleme cunoscute](#15-note-și-probleme-cunoscute)

---

## 1. Prezentare Generală

Modulul **Materiale Indirecte** gestionează complet materialele de consum (consumabile de producție) prin intermediul aplicației TraceabilityRS. Funcționalitățile acoperite sunt:

- **Importul** codurilor de materiale din fișiere Excel exportate din Dynamics.
- **Configurarea** regulilor de fracționare și a cantității standard per cod material.
- **Solicitarea** materialelor de către operatori/departamente.
- **Notificarea automată** a depozitului (WH) prin popup-uri cu semnale sonore.
- **Confirmarea** și **pregătirea** cererilor de către personalul de depozit.
- **Notificarea automată** a solicitantului când materialul este pregătit.
- **Generarea** PDF-ului oficial „Cerere de Material de Consum" cu posibilitate de tipărire.
- **Gestionarea scoriilor/rientrurilor** necesare pentru anumite materiale.
- **Monitorizarea scurtelor** și **generarea automată de email-uri de reaprovizionare** către achiziții.
- **Confirmarea ordinelor de achiziție** (cantitate comandată, număr PO, data estimată de livrare).
- **Serviciul de notificări în background** care permite primirea de popup-uri chiar și când aplicația principală este închisă.
- **Rapoarte, statistici și analize de consum**.

---

## 2. Structura Meniului

Meniu principal: **Materiale** → **Materiale Indirecte**

```
📂 Materiale
├── ...
├── ─────────────────────
├── 📂 Materiale Indirecte
│   ├── 📋 Solicitare Materiale        ← autorizare: richiesta_materiali_indiretti
│   ├── 📋 Confirmare Materiale        ← autorizare: rilascia_materiali
│   ├── 📋 Conferma ordini             ← autorizare: acquisto_materiali_indiretti_conferma
│   ├── 📋 Gestione Scorie / Rientri   ← autorizare: dichiara_scarti-rientri
│   ├── 📋 Convalida Quantități Dichiarate  ← autorizare: dichiara_scarti-rientri
│   ├── 📋 Verificare Giacenze         ← acces liber
│   ├── 📋 Configurare Scorte Minime   ← autorizare: Stock_minimo_met_indiretti
│   ├── 📋 Raport Mensil Materiale     ← acces liber
│   ├── 📋 Statistici & Anomalii       ← acces liber
│   └── 📋 Analiză Consumuri & Budget  ← acces liber
│
├── 📂 Configurații
│   ├── 🖨️ Stampante
│   ├── 🏷️ Etichetă
│   ├── ─────────────────
│   ├── 🖥️ Configurare WorkStation      ← login simplu
│   ├── 📦 Instalare serviciu notificări background  ← UAC (runas)
│   ├── 📦 Dezinstalare serviciu notificări background  ← UAC (runas)
│   ├── 📥 Aliniere Coduri             ← import Excel
│   ├── ⚙️ Configurare Coduri          ← acces liber
│   └── 📦 Tipuri Materiale            ← acces liber
```

Funcțiile marcate cu **autorizare** solicită autentificare cu un utilizator căruia i-a fost acordată permisiunea respectivă în `dbo.AutorizedUsers`.

---

## 3. Configurare Inițială

### 3.1 Configurare WorkStation (WH / Achiziții)

**Acces meniu:** Materiale → Configurații → **Configurare WorkStation**
**Protecție:** Login simplu (fără permisiune specială).

Această funcție identifică computerul curent ca:
- **Stație de depozit (WH)** — primește popup-uri pentru cererile noi de materiale.
- **Stație de achiziții materiale indirecte** — primește popup zilnic cu solicițările de reaprovizionare neconfirmate.

#### Funcționare

- **Activare** → creează fișierul corespunzător în `%LOCALAPPDATA%`:
  - `wh_host.json` pentru WH
  - `purchasing_host.json` pentru achiziții
  
  Format fișier:
  ```json
  {
      "workstation_type": "WH",
      "hostname": "PC-WH01",
      "activated_by": "user.name",
      "activated_at": "2026-08-14 11:34:10"
  }
  ```

- **Dezactivare** → șterge fișierul corespunzător.

#### Starea afișată

| Stare | Descriere |
|-------|-----------|
| ✅ WorkStation ACTIVĂ | Computerul primește notificări |
| ❌ WorkStation NEACTIVĂ | Computerul nu primește notificări |

#### Butoane

| Buton | Acțiune |
|-------|---------|
| **Activează WorkStation** | Creează configurarea (dezactivat dacă deja activă) |
| **Dezactivează WorkStation** | Șterge configurarea (necesită confirmare) |

### 3.2 Serviciu de notificări în background

**Acces meniu:** Materiale → Configurații → **Instalare serviciu notificări background** / **Dezinstalare serviciu notificări background**
**Protecție:** Necesită drepturi de administrator (UAC / `runas`).

Acest serviciu permite primirea de popup-uri (cereri WH, cereri pregătite, solicițări achiziții, etc.) **chiar și atunci când aplicația principală `main.py` este închisă**.

#### Funcționare

- Se creează un task în **Task Scheduler Windows** cu numele `TraceabilityRS Background Notifications`.
- Trigger: **la logarea utilizatorului** (`ONLOGON`).
- Task-ul execută `services/run_background_service.bat`, care la rândul său lansează `background_notification_service.py` cu `pythonw.exe` (fără fereastră de consolă).
- Serviciul verifică la fiecare **30 de secunde** prezența fișierelor marker JSON din `%LOCALAPPDATA%` și pornește doar monitorii corespunzători:
  - `wh_host.json` → popup-uri WH pentru cereri noi.
  - `purchasing_host.json` → popup zilnic pentru achiziții.
  - și alte markere pentru SCT, touch-up, kit, etc. (vedeți fișierul `background_notification_service.py`).
- Dacă un marker este șters, monitorul respectiv se oprește automat.
- Log-uri: `%LOCALAPPDATA%\TraceabilityRS\logs\background_notifications.log`.

#### Fișiere BAT

| Fișier | Rol |
|--------|-----|
| `services/install_background_service.bat` | Creează task-ul în Task Scheduler |
| `services/run_background_service.bat` | Pornește serviciul cu `pythonw.exe` |
| `services/uninstall_background_service.bat` | Șterge task-ul din Task Scheduler |

> **Notă:** Butonul „Apri" din popup-ul serviciului poate lansa automat executabilul principal `TraceabilityRS.exe` (sau `main.py`) dacă programul este oprit.

---

## 4. Solicitare Materiale Indirecte

**Acces meniu:** Materiale → Materiale Indirecte → **Solicitare Materiale**
**Protecție:** Autorizare (`richiesta_materiali_indiretti`).

### 4.1 Descriere

Fereastra permite operatorilor să solicite **mai multe materiale de consum** într-o singură sesiune. Materialele selectate sunt adăugate într-o **listă de cereri** (zona inferioară), iar operatorul le poate revizui, elimina sau corecta înainte de a le trimite pe toate simultan.

### 4.2 Structura ferestrei

| Zona | Locație | Funcție |
|------|---------|---------|
| **Filtre** | Sus | Filtrare materiale pe cod și descriere |
| **Tabel materiale** | Centru-sus | Lista completă a materialelor cu stoc disponibil |
| **Selectie și cantitate** | Centru | Selectare material, introducere cantitate, buton Adaugă în listă |
| **Lista cereri** (Coș) | Jos | Materialele adăugate, gata de trimis |

### 4.3 Pași de utilizare

1. Deschideți fereastra din meniu — se solicită autentificarea.
2. Filtrați materialele folosind câmpurile:
   - **Cod** — filtrare parțială pe codul materialului.
   - **Descriere** — filtrare parțială pe descrierea materialului.
   - Butonul **Curăță** resetează filtrele.
3. Selectați materialul dorit din tabelul cu coloanele:
   | Coloană | Descriere |
   |---------|-----------|
   | Cod | Codul materialului din Dynamics |
   | Descriere | Descrierea materialului |
   | Tip | Categoria materialului (ex: Generico, Abrazivi, etc.) |
   | Stoc | Cantitatea disponibilă în depozit |
   | Ambalaj | Cantitatea standard per ambalaj |
   | Fracționabil | Da/Nu — dacă materialul poate fi solicitat în cantități parțiale |
4. Introduceți cantitatea în câmpul **Cantitate**:
   - **Material fracționabil:** cantitate liberă, maxim = stocul disponibil.
   - **Material non-fracționabil:** cantitate obligatoriu multiplu al ambalajului standard.
5. Apăsați **Adaugă în listă**.
6. Revizuiți lista în zona inferioară.
7. Apăsați **Trimite toate cererile** pentru a confirma și salva.

### 4.4 Reguli de Validare

| Regulă | Descriere |
|--------|-----------|
| Stoc insuficient | Cantitatea solicitată nu poate depăși stocul disponibil (inclusiv cantitățile deja adăugate în listă pentru același material) |
| Non-fracționabil | Cantitatea trebuie să fie multiplu exact al cantității standard (ambalaj) |
| Cantitate pozitivă | Cantitatea trebuie să fie mai mare decât 0 |
| Verificare cumulativă | La adăugarea unui material deja prezent în listă, stocul disponibil ține cont de cantitățile deja adăugate |
| Gating scorie | Dacă materialul are o regulă în `dbo.MaterialRules`, este necesară prezența unei scorii/rientri neconsumate pentru `MustCodeId` (vedeți §7) |

### 4.5 Ce se întâmplă la trimitere

- Se creează câte o înregistrare în tabela `ind.MaterialiRichieste` pentru fiecare material din listă, toate cu starea `RICHIESTA`.
- Toate inserările sunt efectuate într-o **tranzacție atomică** (tot sau nimic).
- Se înregistrează: `MaterialeId`, cantitatea solicitată, stocul la momentul cererii, numele solicitantului, hostname-ul computerului.
- **Monitorul WH** detectează automat cererile și afișează popup pe stația de depozit.
- **La ridicare**, stocul este scăzut printr-un moviment de **SCARICO** în `ind.MaterialiMovimenti`.

---

## 5. Confirmare Materiale (Istoric Cereri)

**Acces meniu:** Materiale → Materiale Indirecte → **Confirmare Materiale**
**Protecție:** Autorizare (`rilascia_materiali`).

### 5.1 Descriere

Afișează tabelul complet al tuturor cererilor de materiale indirecte, cu posibilitatea de a pregăti materialele, de a confirma ridicarea și de a retipări PDF-ul.

### 5.2 Coloane afișate

| Coloană | Descriere |
|---------|-----------|
| ID | Numărul unic al cererii |
| Data | Data și ora cererii (dd/mm/yyyy HH:MM) |
| Cod | Codul materialului solicitat |
| Descriere | Descrierea materialului |
| Cantitate | Cantitatea solicitată |
| Stare | `RICHIESTA` / `PREPARATA` / `PRONTA` / `PRELEVATA` / `ANNULLATA` |
| Solicitant | Numele persoanei care a trimis cererea |
| Pregătitor | Numele personalului WH care a pregătit materialul |

### 5.3 Acțiuni disponibile

- **Pregătește și Confirmă** — setează starea `PRONTA`, înregistrează pregătitorul, generează și tipărește PDF.
- **Tipărește** — generează și tipărește PDF-ul fără a schimba starea.
- **Ridicat** — setează starea `PRELEVATA` și înregistrează data ridicării.
- **Anulează** — setează starea `ANNULLATA`.

---

## 6. Conferma ordini (Achiziții)

**Acces meniu:** Materiale → Materiale Indirecte → **Conferma ordini**
**Protecție:** Autorizare (`acquisto_materiali_indiretti_conferma`).

### 6.1 Descriere

Fereastra permite operatorului de achiziții să înregistreze, pentru fiecare solicițare de reaprovizionare trimisă prin email, cantitatea efectiv comandată, numărul PO și data estimată de livrare.

### 6.2 Date afișate

| Coloană | Descriere |
|---------|-----------|
| Annulla | Checkbox pentru a anula solicițarea |
| Cod | Codul materialului |
| Descriere | Descrierea materialului |
| Qta sugerată | Cantitatea sugerată în email-ul de riordino |
| Giacență | Stocul detectat la momentul solicițării |
| Qta ordonată | Cantitatea comandată efectiv (de completat) |
| Număr PO | Numărul comandă furnizor (de completat) |
| Data livrare | Data estimată de livrare (de completat) |
| Zile | Zile de când solicițarea a fost trimisă |

### 6.3 Comportament

- Rândurile cu **Stato = 'INVIATO'** din `ind.RiordineEmailLog` (ultimele 120 de zile) sunt afișate.
- **Header-ul tabelului rămâne vizibil** în timpul scroll-ului; lista rândurilor se derulează separat sub antet.
- **Fereastra este redimensionabilă cu mouse-ul** (colțul/dreapta-jos); coloanele **Cod Material** și **Descriere** se lărgesc automat când mărești fereastra.
- Câmpul **Data livrare** folosește un **selector de dată (datepicker)**; valoarea implicită este **data de mâine** (ziua următoare datei curente).
- Dacă se bifează **Annulla**, rândul este salvat cu `Stato = 'ANNULLATO'`.
- Dacă se completează **Qta ordonată** / **Număr PO** / **Data livrare**, rândul este salvat cu `Stato = 'CONFERMATO'` și `DataConferma = GETDATE()`.
- Dacă se introduce PO fără cantitate, cantitatea este considerată `0`.
- Butoane: **Salvează conferme**, **Actualizează**, **Închide**.
- Scroll-ul cu rotița mouse-ului funcționează în zona rândurilor.

### 6.4 Reminder automat

- În fiecare zi lucrătoare la ora **07:30**, sistemul verifică stocurile sub pragul minim și trimite un email de riordino către achiziții.
- Dedublarea este gestionată prin tabela `ind.RiordineEmailLog` — un material este solicițat o singură dată până la confirmare/anulare.
- Dacă există solicițări `INVIATO` neconfirmate, în fiecare zi lucrătoare la ora **10:00** apare un **popup** pe stația de achiziții configurată (dacă serviciul background este activ).
- La fiecare **2 zile lucrătoare** de la prima solicițare, dacă există solicițări încă neconfirmate, sistemul trimite un **email de reminder** profesional în engleză cu:
  - lista codurilor de confirmat;
  - cantitățile sugerate;
  - numărul de reiterări;
  - numărul de zile de la prima solicițare.

---

## 7. Gestione Scorie / Rientri

**Acces meniu:** Materiale → Materiale Indirecte → **Gestione Scorie / Rientri**
**Protecție:** Autorizare (`dichiara_scarti-rientri`).

### 7.1 Descriere

Permite declararea cantității de material scăpat/rientrat (în kg) pentru materialele care au o regulă în `dbo.MaterialRules`. Fără o scorie/rientru disponibilă, anumite materiale nu pot fi solicitate.

### 7.2 Câmpuri

| Câmp | Descriere |
|------|-----------|
| Material scorie | `m1` (MustCode) — selectabil din listă |
| Material solicitat | `m` — afișat pentru context |
| Data | Precompletată cu data curentă, modificabilă |
| Peso (kg) | Numeric, 1 zecimal, > 0 |

### 7.3 Comportament

- La salvare se inserează o înregistrare în `dbo.ReturnMaterials` cu `RichiestaId = NULL`.
- Dacă există deja o înregistrare cu același `MateriaId`, `DateReturn` și `ReturWeight` (rotunjit la 1 zecimală), se afișează un **warning** de confirmare.
- Când o cerere de material `m` este trimisă, sistemul consumă scorii disponibile ale `m1` setând `RichiestaId` pe înregistrările din `dbo.ReturnMaterials`.

### 7.4 Convalida Quantități Dichiarate

**Acces meniu:** Materiale → Materiale Indirecte → **Convalida Quantități Dichiarate**
**Protecție:** Autorizare (`dichiara_scarti-rientri`).

Permite verificarea și validarea scoriilor/rientrurilor declarate.

---

## 8. Verificare Giacenze și Configurare Scorte Minime

### 8.1 Verificare Giacenze

**Acces meniu:** Materiale → Materiale Indirecte → **Verificare Giacenze**
**Protecție:** Acces liber.

Afișează stocul curent al materialelor, calculat din vizualizarea `ind.vw_GiacenzaCorrente` (suma movimentelor din `ind.MaterialiMovimenti`).

### 8.2 Configurare Scorte Minime

**Acces meniu:** Materiale → Materiale Indirecte → **Configurare Scorte Minime**
**Protecție:** Autorizare (`Stock_minimo_met_indiretti`).

Permite configurarea pentru fiecare material a:
- **LivelloMinimo** — stoc minim;
- **LottoRiordino** — lotul de reaprovizionare sugerat;
- **LivelloRaccomandato** — stoc recomandat;
- **IsAttivo** — dacă materialul este inclus în verificarea automată de riordino.

Acestor parametri li se bazează email-urile zilnice de reaprovizionare.

---

## 9. Rapoarte, Statistici și Analize

| Voce meniu | Scop | Protecție |
|---|---|---|
| Raport Mensil Materiale | Istoric cereri/consegne și verificare achiziții | liber |
| Statistici & Anomalii | Anomalii în consumuri și cereri | liber |
| Analiză Consumuri & Budget | Analiză consum pe săptămână/lună/an și propunere buget | liber |

---

## 10. Notificări și Popup

### 10.1 WH Monitor (Depozit)

**Activ pe:** Computere cu `wh_host.json` prezent.  
**Polling:** La fiecare 10 secunde în `main.py`; 30 de secunde în serviciul background.

1. Verifică cererile cu starea `RICHIESTA` care nu au fost notificate sau au fost notificate cu mai mult de 5 minute în urmă.
2. Actualizează `DataUltimaNotificaWH`.
3. Afișează un **popup roșu** cu semnale sonore (3 beep-uri) conținând:
   - Cod material
   - Descriere
   - Cantitate solicitată
   - Solicitant
   - Data cererii
   - Computer solicitant

#### Butoane popup WH

| Buton | Acțiune |
|-------|---------|
| **Pregătește și Confirmă** | Setează starea `PRONTA`, înregistrează pregătitorul, generează și tipărește PDF |
| **Tipărește** | Generează și tipărește PDF-ul fără a schimba starea |
| **Închide** | Închide popup-ul (se va renotifica după 5 minute) |

### 10.2 Requester Monitor (Solicitant)

**Activ pe:** Computere cu `wh_host.json` prezent (sau pe baza `ComputerRichiedente` în funcție de implementare).  
**Polling:** La fiecare 10 secunde.

1. Verifică cererile cu starea `PRONTA`.
2. Afișează un **popup verde** cu semnale sonore conținând:
   - Cod material
   - Descriere
   - Cantitate
   - Pregătit de (numele angajatului WH)
   - Ora pregătirii

#### Butoane popup solicitant

| Buton | Acțiune |
|-------|---------|
| **Ridicat** | Setează starea `PRELEVATA`, înregistrează data ridicării |
| **Mai târziu** | Închide popup-ul (se va renotifica după 5 minute) |

### 10.3 Purchasing Monitor (Achiziții)

**Activ pe:** Computere cu `purchasing_host.json` prezent.  
**Polling:** La fiecare 60 de secunde.

- Afișează un popup zilnic (o singură dată pe zi) după ora **10:00** cu solicițările de riordino `INVIATO` neconfirmate.
- Popup conține tabel cu cod, descriere, stoc, minim, cantitate sugerată, data invio, zile.
- Butoane: **Scarică Excel** (deschide fișierul cu lista completă), **Închide**.
- Fișierul Excel este salvat în `%LOCALAPPDATA%` cu numele `purchasing_reorders_YYYYMMDD_HHMMSS.xlsx`.

---

## 11. Generare PDF — Cerere de Material de Consum

Documentul generat se intitulează **„CERERE DE MATERIAL DE CONSUM"** și conține:

- Logo Vandewiele (din fișierul `Logo.png`)
- Număr cerere (Nr. ID)
- Data și ora cererii
- Tabel material:

| Cod Material | Descriere | Cantitate solicitată | Stoc la momentul cererii |
|-------------|-----------|---------------------|------------------------|
| ABC-123 | Mănuși protecție | 100.00 | 500.00 |

- Solicitant: Numele persoanei
- Pregătit de: Numele personalului WH (sau linie de semnătură)
- Note (dacă sunt prezente)
- Semnături:
  - Semnătura solicitant: ___________________
  - Semnătura predare: ___________________
- Footer: „Generat automat — dd/mm/yyyy HH:MM:SS"

PDF-ul este generat în directorul temporar al sistemului (`%TEMP%\ind_materials\`) și poate fi:
- **Tipărit automat** pe imprimanta implicită Windows.
- **Deschis** în vizualizatorul PDF implicit dacă tipărirea directă eșuează.

---

## 12. Schema Bazei de Date

### 12.1 Tabele Principale

```
┌─────────────────────────┐     ┌──────────────────────────┐
│   ind.TipoMateriali     │     │    ind.Materiali          │
├─────────────────────────┤     ├──────────────────────────┤
│ TipoMaterialeId (PK)    │◄────┤ TipoMaterialeId (FK)     │
│ Tipo                    │     │ MaterialeId (PK)          │
│ IsFrazionabile          │     │ CodiceMateriale           │
│ QtaConfezione           │     │ DescrizioneMateriale      │
└─────────────────────────┘     │ IsActive                  │
                                └──────────┬───────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
┌──────────────────────────┐  ┌──────────────────────────┐  ┌───────────────────────────┐
│   ind.MaterialiMovimenti  │  │   ind.MaterialiRichieste  │  │ dbo.MaterialConfigurations │
├──────────────────────────┤  ├──────────────────────────┤  ├───────────────────────────┤
│ MovimentoId (PK)          │  │ RichiestaId (PK)         │  │ MaterialConfigurationId    │
│ MaterialeId (FK)          │  │ MaterialeId (FK)         │  │ MaterialId (FK)            │
│ TipoMovimento             │  │ QtaRichiesta             │  │ IsFractionabil             │
│ Qty                       │  │ QtaStockAlMomento        │  │ QuantityStandard           │
│ [User]                    │  │ Stato                    │  │ DateOut (NULL=activ)       │
│ DataMovimento             │  │ DataRichiesta            │  └───────────────────────────┘
└──────────────────────────┘  │ RichiestoDa              │
                              │ ComputerRichiedente      │
                              │ DataUltimaNotificaWH     │
                              │ PreparatoDa              │
                              │ ComputerPreparatore      │
                              │ DataPreparazione         │
                              │ DataUltimaNotificaRich   │
                              │ DataPrelievo             │
                              │ Note                     │
                              └──────────────────────────┘

┌──────────────────────────┐  ┌──────────────────────────┐  ┌───────────────────────────┐
│   ind.MaterialiRiordino   │  │   ind.RiordineEmailLog    │  │ dbo.ReturnMaterials        │
├──────────────────────────┤  ├──────────────────────────┤  ├───────────────────────────┤
│ MaterialeId (FK)          │  │ RiordineLogId (PK)       │  │ ReturnMaterialId (PK)      │
│ LivelloMinimo             │  │ MaterialeId (FK)         │  │ MateriaId (FK)             │
│ LottoRiordino             │  │ GiacenzaRilevata         │  │ ReturWeight                │
│ LivelloRaccomandato       │  │ LivelloMinimo            │  │ DateReturn                 │
│ IsAttivo                  │  │ QtaSuggerita             │  │ UserRetur                  │
└──────────────────────────┘  │ DataInvio                │  │ RichiestaId (FK)           │
                                │ QtaOrdinata              │  │ IsOk                       │
                                │ NumeroPO                 │  │ DateOut                    │
                                │ DataPrevistaArrivo       │  └───────────────────────────┘
                                │ Stato                    │
                                │ DataConferma             │
                                │ ConfermatoDa             │
                                │ ReminderCount            │
                                │ DataUltimoReminder       │
                                └──────────────────────────┘

        ┌──────────────────────────┐
        │   dbo.MaterialRules       │
        ├──────────────────────────┤
        │ MaterilRuleId (PK)        │
        │ MaterialeId (FK) → m      │
        │ MustCodeId (FK) → m1      │
        │ DateIn / DateOut          │
        └──────────────────────────┘
```

### 12.2 Semnificație Stări

| Stare | Semnificație |
|-------|-------------|
| `RICHIESTA` | Cerere trimisă, în așteptare la depozit |
| `PREPARATA` | Material în pregătire |
| `PRONTA` | Material pregătit de depozit, în așteptare ridicare |
| `PRELEVATA` | Material ridicat de solicitant |
| `ANNULLATA` | Cerere anulată |

### 12.3 Semnificație Stato `ind.RiordineEmailLog`

| Valoare | Semnificație |
|---------|-------------|
| `INVIATO` | Email de riordino trimis, în așteptare confirmare |
| `CONFERMATO` | Comandă confirmată de achiziții |
| `ANNULLATO` | Solicitare anulată |

---

## 13. Fluxul Complet de Lucru

### 13.1 Configurare (o singură dată)

```
1. Configurare WorkStation → Activare pe PC-ul depozitului și/sau achiziții
2. Instalare serviciu notificări background (opțional, pentru popup fără main.py deschis)
3. Import Coduri (Aliniere) → Import Excel din Dynamics
4. Tipuri Materiale → Definire categorii + reguli implicite
5. Configurare Coduri → Override per-cod (opțional)
6. Configurare Scorte Minime → Definire praguri de riordino
7. MaterialRules → Configurare reguli scorie/rientri (opțional, dacă necesar)
```

### 13.2 Flux Operațional Zilnic

```
┌──────────┐    auto     ┌──────────┐    auto     ┌──────────┐
│SOLICITANT│───────────► │  DEPOZIT │───────────► │SOLICITANT│
│          │  10s poll   │   (WH)   │  10s poll   │          │
│Trimite   │             │Popup roșu│             │Popup verde│
│cerere    │             │🔊 3 beeps│             │🔊 3 beeps│
│          │             │Pregătește│             │Confirmă  │
│          │             │+ Stampă  │             │ridicare  │
└──────────┘             └──────────┘             └──────────┘

Stare:  RICHIESTA ──────► PREPARATA/PRONTA ──────► PRELEVATA
```

### 13.3 Flux Achiziții

```
07:30  → sistemul verifică stocurile și trimite email de riordino (dacă sunt sub prag)
10:00  → popup pe workstation achiziții cu lista materialelor de comandat
         ↓
   Operator achiziții completează: Qta ordonată, Număr PO, Data livrare
         ↓
   Salvare în RiordineEmailLog.Stato = 'CONFERMATO'
         ↓
   La fiecare 2 zile lucrătoori: reminder email pentru solicitan neconfirmate
```

---

## 14. Fișiere Implicate

| Fișier | Rol |
|--------|-----|
| `main.py` | Definire meniu, wiring handler, pornire monitori, planificări riordino/reminder |
| `indirect_materials_request.py` | Form solicitare multi-material cu coș |
| `indirect_materials_wh_monitor.py` | Popup WH și popup solicitant |
| `indirect_materials_purchasing_monitor.py` | Popup zilnic achiziții |
| `indirect_materials_order_confirmation.py` | Form confirmare ordini achiziții |
| `indirect_materials_stock_data.py` | Giacenze, movimenti, scarico, riordino, reminder |
| `indirect_materials_stock.py` | GUI Verificare Giacenze și Configurare Scorte Minime |
| `indirect_materials_pdf.py` | Generare PDF cerere |
| `indirect_materials_import.py` | Import Excel materiali |
| `indirect_materials_report.py` | Raport mensual |
| `indirect_materials_stats.py` | Statistici și anomalii |
| `indirect_materials_consumption.py` | Analiză consumuri și buget |
| `indirect_materials_consumption_report.py` | Report consumuri general |
| `indirect_materials_types.py` | CRUD `ind.TipoMateriali` |
| `wh_workstation_config.py` | Configurare WorkStation WH și achiziții |
| `background_notification_service.py` | Serviciu background de notificări |
| `services/install_background_service.bat` | Instalare task Task Scheduler |
| `services/run_background_service.bat` | Pornire serviciu cu pythonw |
| `services/uninstall_background_service.bat` | Dezinstalare task Task Scheduler |
| `material_configurations.py` | Override per cod (`dbo.MaterialConfigurations`) |
| `scrap_returns_gui.py` | Gestione scorie/rientri |

---

## 15. Note și Probleme Cunoscute

1. **Serviciul background** necesită Task Scheduler și pornire la logare; nu este un serviciu de sistem clasic. Se activează doar pe PC-urile cu WorkStation configurată.
2. **Popup-urile** funcționează atât în `main.py` deschis, cât și în serviciul background, folosind aceleași module de monitorizare.
3. **Giacenzele** sunt calculate din vizualizarea `ind.vw_GiacenzaCorrente` (suma movimentelor); stocul istoric din `ind.MaterialiStock` rămâne disponibil doar pentru consultare.
4. **Email-urile de riordino** și **reminder-urile** depind de configurarea destinațiilor de email în aplicație.
5. **Conferma ordini** afișează doar solicițări din ultimele 120 de zile cu `Stato = 'INVIATO'`.
6. **Scorii/rientri** sunt obligatorii doar pentru materialele cu regulă activă în `dbo.MaterialRules`.
7. **Butonul „Apri" din popup** poate lansa automat executabilul principal dacă aplicația este oprită.

---

> **Document generat pentru uzul intern Vandewiele România.**  
> **Toate drepturile rezervate.**
