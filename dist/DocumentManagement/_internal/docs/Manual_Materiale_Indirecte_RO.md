# MANUAL DE UTILIZARE — Materiale Indirecte (Materiale de Consum)

**Aplicație:** TraceabilityRS — DocumentManagement  
**Versiune document:** 1.1  
**Data:** 22/04/2026  

---

## Cuprins

1. [Prezentare generală](#1-prezentare-generală)
2. [Structura meniului](#2-structura-meniului)
3. [Solicitare Materiale Indirecte](#3-solicitare-materiale-indirecte)
4. [Confirmare Materiale (Istoric Cereri)](#4-confirmare-materiale-istoric-cereri)
5. [Import Coduri Materiale (Aliniere Coduri)](#5-import-coduri-materiale-aliniere-coduri)
6. [Configurare Coduri Materiale](#6-configurare-coduri-materiale)
7. [Tipuri Materiale](#7-tipuri-materiale)
8. [Confirmare WH WorkStation](#8-confirmare-wh-workstation)
9. [Monitorizare Automată (WH Monitor & Requester Monitor)](#9-monitorizare-automată)
10. [Generare PDF — Cerere de Material de Consum](#10-generare-pdf)
11. [Schema Bazei de Date](#11-schema-bazei-de-date)
12. [Fluxul Complet de Lucru](#12-fluxul-complet-de-lucru)

---

## 1. Prezentare Generală

Modulul **Materiale Indirecte** permite gestionarea completă a materialelor de consum (consumabile de producție) prin intermediul aplicației TraceabilityRS. Funcționalitățile acoperite sunt:

- **Importul** codurilor de materiale din fișiere Excel exportate din Dynamics
- **Configurarea** regulilor de fracționare și cantitate standard per cod material
- **Solicitarea** materialelor de către operatori/departamente
- **Notificarea automată** a depozitului (WH) prin popup-uri cu semnale sonore
- **Confirmarea** și **pregătirea** cererilor de către personalul de depozit
- **Notificarea automată** a solicitantului când materialul este pregătit
- **Generarea** PDF-ului oficial „Cerere de Material de Consum" cu posibilitate de tipărire

---

## 2. Structura Meniului

Meniu principal: **Materiale** → **Materiale Indirecte**

```
📂 Materiale
├── ...
├── ─────────────────────
├── 📂 Materiale Indirecte
│   ├── 📋 Solicitare Materiale        ← Cerere nouă (necesită autorizare)
│   └── 📋 Confirmare Materiale        ← Istoric cereri + ristampare PDF
│
├── 📂 Configurații
│   ├── 🖨️ Stampante
│   ├── 🏷️ Etichetă
│   ├── ─────────────────
│   ├── 🖥️ Confirmare WH WorkStation   ← Activare/dezactivare stație WH
│   ├── 📥 Aliniere Coduri             ← Import coduri din Excel (necesită autorizare)
│   ├── ⚙️ Configurare Coduri          ← Reguli per-cod (necesită autorizare)
│   └── 📦 Tipuri Materiale            ← CRUD tipuri materiale
```

> **Notă:** Funcțiile marcate cu „necesită autorizare" solicită autentificarea cu credențiale autorizate înainte de deschiderea ferestrei.

---

## 3. Solicitare Materiale Indirecte

**Acces meniu:** Materiale → Materiale Indirecte → **Solicitare Materiale**  
**Protecție:** Necesita autorizare (login cu rol autorizat)

### 3.1 Descriere

Aceasta fereastra permite operatorilor sa solicite **mai multe materiale de consum** intr-o singura sesiune. Materialele selectate sunt adaugate intr-o **lista de cereri** (zona inferioara a ferestrei), iar operatorul le poate revizui, elimina sau corecta inainte de a le trimite pe toate simultan.

### 3.2 Structura ferestrei

Fereastra este organizata in **4 zone**:

| Zona | Locatie | Functie |
|------|---------|---------|
| **Filtre** | Sus | Filtrare materiale pe cod si descriere |
| **Tabel materiale** | Centru-sus | Lista completa a materialelor cu stoc disponibil |
| **Selectie si cantitate** | Centru | Selectare material, introducere cantitate, buton Adauga in lista |
| **Lista cereri** (Cos) | Jos | Materialele adaugate, gata de trimis |

### 3.3 Pasi de utilizare

1. **Deschideti** fereastra din meniu - se solicita autentificarea
2. **Filtrati** materialele folosind campurile:
   - **Cod** - filtrare partiala pe codul materialului
   - **Descriere** - filtrare partiala pe descrierea materialului
   - Butonul **Curata** reseteaza filtrele
3. **Selectati** materialul dorit din tabelul cu coloanele:
   | Coloana | Descriere |
   |---------|-----------|
   | Cod | Codul materialului din Dynamics |
   | Descriere | Descrierea materialului |
   | Tip | Categoria materialului (ex: Generico, Abrazivi, etc.) |
   | Stoc | Cantitatea disponibila in depozit |
   | Ambalaj | Cantitatea standard per ambalaj |
   | Fractionabil | Da/Nu - daca materialul poate fi solicitat in cantitati partiale |
4. **Introduceti cantitatea** in campul Cantitate:
   - **Material fractionabil:** cantitate libera, maxim = stocul disponibil
   - **Material non-fractionabil:** cantitate obligatoriu multiplu al ambalajului standard
5. **Adaugati in lista** cu butonul **Adauga in lista**
   - Materialul apare in **Lista Cereri de Trimis** (zona inferioara)
   - Puteti repeta pasii 3-5 pentru a adauga mai multe materiale
6. **Revizuiti lista** - verificati materialele adaugate in cos:
   | Coloana cos | Descriere |
   |-------------|-----------|
   | Cod | Codul materialului |
   | Descriere | Descrierea materialului |
   | Cantitate | Cantitatea solicitata |
   | Tip | Tipul materialului |
7. **Gestionati lista** cu butoanele disponibile:
   - **Elimina selectate** - elimina din lista elementele selectate (selectie multipla posibila)
   - **Goleste lista** - elimina toate elementele din lista (cu confirmare)
8. **Trimiteti toate cererile** cu butonul **Trimite toate cererile**
   - Apare un dialog de confirmare cu rezumatul complet al tuturor materialelor
   - La confirmare, toate cererile sunt trimise **simultan** intr-o singura tranzactie atomica

### 3.4 Reguli de Validare

| Regula | Descriere |
|--------|-----------|
| Stoc insuficient | Cantitatea solicitata nu poate depasi stocul disponibil (inclusiv cantitatile deja adaugate in lista pentru acelasi material) |
| Non-fractionabil | Cantitatea trebuie sa fie multiplu exact al cantitatii standard (ambalaj) |
| Cantitate pozitiva | Cantitatea trebuie sa fie mai mare decat 0 |
| Verificare cumulativa | La adaugarea unui material deja prezent in lista, stocul disponibil tine cont de cantitatile deja adaugate |

### 3.5 Ce se intampla la trimitere

- Se creeaza **cate o inregistrare** in tabela `ind.MaterialiRichieste` pentru fiecare material din lista, toate cu starea `RICHIESTA`
- Toate inserarile sunt efectuate intr-o **tranzactie atomica** (tot sau nimic):
  - Daca toate inserarile reusesc - COMMIT - lista se goleste - stocurile se reincaraca
  - Daca apare o eroare la oricare inserare - ROLLBACK - nicio cerere nu este salvata
- Se inregistreaza: MaterialeId, cantitatea solicitata, stocul la momentul cererii, numele solicitantului, hostname-ul computerului
- **Monitorul WH** detecteaza automat cererile si afiseaza popup-uri pe statia de depozit

### 3.6 Istoric Cereri

Din fereastra de solicitare, butonul **Istoric Cereri** deschide fereastra cu toate cererile anterioare.

---

## 4. Confirmare Materiale (Istoric Cereri)

**Acces meniu:** Materiale → Materiale Indirecte → **Confirmare Materiale**  
**Protecție:** Fără autorizare — acces liber

### 4.1 Descriere

Afișează tabelul complet al tuturor cererilor de materiale indirecte, cu posibilitatea de ristampare PDF.

### 4.2 Coloane afișate

| Coloană | Descriere |
|---------|-----------|
| ID | Numărul unic al cererii |
| Data | Data și ora cererii (dd/mm/yyyy HH:MM) |
| Cod | Codul materialului solicitat |
| Descriere | Descrierea materialului |
| Cantitate | Cantitatea solicitată |
| Stare | RICHIESTA / PRONTA / PRELEVATA |
| Solicitant | Numele persoanei care a trimis cererea |
| Pregătitor | Numele personalului WH care a pregătit materialul |

### 4.3 Ristampare PDF

1. Selectați o cerere din tabel
2. Apăsați butonul **Ristampare PDF**
3. Se generează PDF-ul „CERERE DE MATERIAL DE CONSUM" și se trimite la imprimanta implicită

---

## 5. Import Coduri Materiale (Aliniere Coduri)

**Acces meniu:** Materiale → Configurații → **Aliniere Coduri**  
**Protecție:** Necesită autorizare (login cu rol autorizat)

### 5.1 Descriere

Această funcție importă codurile materialelor indirecte dintr-un fișier Excel exportat din Microsoft Dynamics. Importul actualizează anagrafica materialelor și înlocuiește stocurile existente cu valorile din fișier.

### 5.2 Format Excel așteptat

Fișierul Excel trebuie să respecte formatul export Dynamics cu coloanele fixe:

| Coloană Excel | Poziție | Conținut |
|---------------|---------|----------|
| A | Coloana 1 | **Cod Material** |
| B | Coloana 2 | **Descriere** |
| H | Coloana 8 | **Cantitate Stoc** |
| Q | Coloana 17 | **Tip Material** |

> **Notă:** Prima linie (antet) este ignorată automat. Liniile fără cod material sunt omise.

### 5.3 Pași de utilizare

1. **Deschideți** fereastra din meniu → se solicită autentificarea
2. Apăsați **Selectează Excel** și alegeți fișierul `.xlsx`
3. Datele sunt afișate în tabelul de previzualizare cu coloanele: Cod, Descriere, Cantitate Stoc, Tip
   - Tipurile sunt verificate automat contra tabelei `ind.TipoMateriali`
   - Dacă un tip nu este găsit în DB, se afișează „NomeTip (→Generico)" indicând că va fi asociat la tipul Generico
4. Verificați datele, apoi apăsați butonul **Importă**
5. Confirmați dialogul: „Importare N coduri materiale?"
6. Se execută importul cu bara de progres

### 5.4 Logica de Import (Tranzacție Atomică)

Întregul proces de import este executat într-o **singură tranzacție** de bază de date. Dacă apare o eroare la orice pas, toate modificările sunt anulate (ROLLBACK).

#### Faza 0 — Tip Generico (default)
- Caută tipul „Generico" în `ind.TipoMateriali`
- Dacă nu există, îl creează automat

#### Faza 1 — Upsert Anagrafica (`ind.Materiali`)
Pentru fiecare linie din Excel:
- **Dacă codul există** → actualizează descrierea, tipul și setează `IsActive = 1`
- **Dacă codul nu există** → inserează un nou material

#### Faza 2 — Închidere stocuri active (Soft-Close)
- Se actualizează `DateOut = GETDATE()` **doar** pe înregistrările `ind.MaterialiStock` ale materialelor importate
- Stocurile materialelor **neimportate** nu sunt afectate

#### Faza 3 — Inserare stocuri noi
- Se creează o nouă înregistrare în `ind.MaterialiStock` pentru fiecare material importat
- `DateOut = NULL` → reprezintă stocul activ curent
- Se înregistrează `CaricatoDa` (utilizatorul care a efectuat importul)

#### COMMIT / ROLLBACK
- **Succes** → `COMMIT` unic la finalul tuturor celor 3 faze
- **Eroare** → `ROLLBACK` complet, baza de date rămâne neschimbată

### 5.5 Rezultat

La finalul importului se afișează un rezumat:
```
🆕 Coduri noi: X
🔄 Coduri actualizate: Y
📦 Stocuri încărcate: Z
❌ Erori: N
```

---

## 6. Configurare Coduri Materiale

**Acces meniu:** Materiale → Configurații → **Configurare Coduri**  
**Protecție:** Necesită autorizare (login cu rol autorizat)

### 6.1 Descriere

Permite configurarea regulilor specifice per cod material: dacă materialul este fracționabil și care este cantitatea standard (dimensiunea ambalajului). Aceste configurări suprascriu regulile implicite ale tipului de material.

### 6.2 Ierarhia Regulilor

```
MaterialConfigurations (per-cod)  →  prioritate MAXIMĂ
         ↓ dacă nu există
TipoMateriali (per-tip)           →  valori implicite
```

### 6.3 Interfața

- **Filtru Cod / Descriere** — filtrare rapidă
- **Solo configurate** — checkbox care afișează doar materialele cu configurare activă
- **Tabel** cu: ID, Cod, Descriere, Fracționabil, Cantitate Standard, Stare

Rândurile cu configurare activă sunt evidențiate cu fundal verde.

### 6.4 Operațiuni

| Acțiune | Descriere |
|---------|-----------|
| **💾 Salvează** | Creează sau actualizează configurația per-cod |
| **🗑️ Dezactivează** | Soft-delete (setează DateOut = GETDATE()) |
| **♻️ Reactivează** | Restaurează o configurare dezactivată (DateOut = NULL) |

### 6.5 Câmpuri

| Câmp | Descriere |
|------|-----------|
| **Fracționabil** | ☐ Da/Nu — dacă materialul poate fi solicitat în cantități parțiale |
| **Cantitate Standard** | Cantitatea standard per ambalaj (ex: 100 buc, 1 cutie, etc.) |

> **Exemplu:** Un material „Mânuși" configurat cu Fracționabil=Nu, Cantitate Standard=50 va putea fi solicitat doar în multipli de 50 (50, 100, 150...).

---

## 7. Tipuri Materiale

**Acces meniu:** Materiale → Configurații → **Tipuri Materiale**  
**Protecție:** Fără autorizare

### 7.1 Descriere

Gestionarea categoriilor (tipurilor) de materiale indirecte. Fiecare tip definește regulile implicite de fracționare și dimensiunea ambalajului pentru toate materialele asociate.

### 7.2 Tabel afișat

| Coloană | Descriere |
|---------|-----------|
| ID | Identificator unic |
| Tip | Numele categoriei (ex: Abrazivi, Lubrifianți, Generico) |
| Fracționabil | Da/Nu |
| Ambalaj | Cantitatea standard implicită |

### 7.3 Operațiuni

| Buton | Acțiune |
|-------|---------|
| **➕ Adaugă** | Creează un tip nou |
| **💾 Salvează** | Actualizează tipul selectat |
| **🗑️ Elimină** | Șterge tipul (doar dacă nu are materiale asociate) |
| **🔄 Actualizează** | Reîncarcă lista din baza de date |

> **Atenție:** Un tip nu poate fi eliminat dacă are materiale asociate. Sistemul afișează: „Tip folosit de N materiale. Nu poate fi eliminat."

---

## 8. Confirmare WH WorkStation

**Acces meniu:** Materiale → Configurații → **Confirmare WH WorkStation**  
**Protecție:** Fără autorizare

### 8.1 Descriere

Această funcție identifică computerul curent ca **stație de depozit (Warehouse)**. Când este activată, pe acest computer vor apărea automat popup-urile de notificare pentru cererile de materiale noi.

### 8.2 Cum funcționează

- **Activare** → se creează fișierul `wh_host.json` în directorul `%LOCALAPPDATA%` cu informațiile:
  - Hostname al computerului
  - Utilizatorul care a activat stația
  - Data și ora activării
- **Dezactivare** → se șterge fișierul `wh_host.json`

### 8.3 Starea afișată

| Stare | Descriere |
|-------|-----------|
| ✅ WH WorkStation ACTIVĂ | Computerul primește notificări |
| ❌ WH WorkStation NEACTIVĂ | Computerul nu primește notificări |

### 8.4 Operațiuni

| Buton | Acțiune |
|-------|---------|
| **Activează WH WorkStation** | Creează configurarea (dezactivat dacă deja activă) |
| **Dezactivează WH WorkStation** | Șterge configurarea (necesită confirmare) |

---

## 9. Monitorizare Automată

### 9.1 WH Monitor (Depozit)

**Activ pe:** Computere cu WH WorkStation activată (fișier `wh_host.json` prezent)  
**Polling:** La fiecare 10 secunde

#### Funcționare:
1. Verifică în baza de date cereri cu starea `RICHIESTA` care nu au fost notificate sau au fost notificate cu mai mult de 5 minute în urmă
2. Actualizează câmpul `DataUltimaNotificaWH` cu data/ora curentă
3. Afișează un **popup roșu** cu semnale sonore (3 beep-uri) conținând:
   - Cod material
   - Descriere
   - Cantitate solicitată
   - Solicitant
   - Data cererii
   - Computer solicitant

#### Butoane popup:

| Buton | Acțiune |
|-------|---------|
| **✅ Pregătește și Confirmă** | Setează starea la `PRONTA`, înregistrează pregătitorul, generează și tipărește PDF |
| **🖨️ Tipărește** | Generează și tipărește PDF-ul fără a schimba starea |
| **Închide** | Închide popup-ul (se va renotifica după 5 minute) |

### 9.2 Requester Monitor (Solicitant)

**Activ pe:** Toate computerele  
**Polling:** La fiecare 10 secunde

#### Funcționare:
1. Verifică cereri cu starea `PRONTA` al căror `ComputerRichiedente` corespunde hostname-ului curent
2. Dacă cererea nu a fost notificată sau au trecut 5 minute de la ultima notificare:
3. Afișează un **popup verde** cu semnale sonore conținând:
   - Cod material
   - Descriere
   - Cantitate
   - Pregătit de (numele angajatului WH)
   - Ora pregătirii

#### Butoane popup:

| Buton | Acțiune |
|-------|---------|
| **✅ Ridicat** | Setează starea la `PRELEVATA`, înregistrează data ridicării |
| **⏳ Mai târziu** | Închide popup-ul (se va renotifica după 5 minute) |

---

## 10. Generare PDF

### 10.1 Format Document

Documentul generat se intitulează **„CERERE DE MATERIAL DE CONSUM"** și conține:

- **Logo** Vandewiele (din fișierul Logo.png)
- **Număr cerere** (Nr. ID)
- **Data și ora cererii**
- **Tabel material:**

| Cod Material | Descriere | Cantitate solicitată | Stoc la momentul cererii |
|-------------|-----------|---------------------|------------------------|
| ABC-123 | Mânuși protecție | 100.00 | 500.00 |

- **Solicitant:** Numele persoanei
- **Pregătit de:** Numele personalului WH (sau linie de semnătură)
- **Note** (dacă sunt prezente)
- **Semnături:**
  - Semnătura solicitant: ___________________
  - Semnătura predare: ___________________
- **Footer:** „Generat automat — dd/mm/yyyy HH:MM:SS"

### 10.2 Tipărire

PDF-ul este generat în directorul temporar al sistemului (`%TEMP%\ind_materials\`) și poate fi:
- **Tipărit automat** pe imprimanta implicită Windows
- **Deschis** în vizualizatorul PDF implicit dacă tipărirea directă eșuează

---

## 11. Schema Bazei de Date

### 11.1 Tabele Principale

```
┌─────────────────────────┐     ┌──────────────────────────┐
│   ind.TipoMateriali     │     │    ind.Materiali          │
├─────────────────────────┤     ├──────────────────────────┤
│ TipoMaterialeId (PK)   │◄────┤ TipoMaterialeId (FK)     │
│ Tipo                    │     │ MaterialeId (PK)         │
│ IsFrazionabile          │     │ CodiceMateriale          │
│ QtaConfezione           │     │ DescrizioneMateriale     │
└─────────────────────────┘     │ IsActive                 │
                                └──────────┬───────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
┌──────────────────────────┐  ┌───────────────────────┐  ┌───────────────────────────┐
│   ind.MaterialiStock     │  │ ind.MaterialiRichieste│  │ dbo.MaterialConfigurations │
├──────────────────────────┤  ├───────────────────────┤  ├───────────────────────────┤
│ MaterialeId (FK)         │  │ RichiestaId (PK)      │  │ MaterialConfigurationId   │
│ Qty                      │  │ MaterialeId (FK)      │  │ MaterialId (FK)           │
│ DateIn                   │  │ QtaRichiesta          │  │ IsFractionabil            │
│ DateOut (NULL=activ)     │  │ QtaStockAlMomento     │  │ QuantityStandard          │
│ CaricatoDa               │  │ Stato                 │  │ DateOut (NULL=activ)       │
└──────────────────────────┘  │ DataRichiesta         │  └───────────────────────────┘
                              │ RichiestoDa           │
                              │ ComputerRichiedente   │
                              │ DataUltimaNotificaWH  │
                              │ PreparatoDa           │
                              │ ComputerPreparatore   │
                              │ DataPreparazione      │
                              │ DataUltimaNotificaRich│
                              │ DataPrelievo          │
                              │ Note                  │
                              └───────────────────────┘
```

### 11.2 Dettagli Campi Critici

#### `ind.MaterialiStock`
- `DateOut = NULL` → stocul este **activ** (reprezintă cantitatea curentă)
- `DateOut ≠ NULL` → stocul este **storicizat** (înlocuit de un import mai recent)

#### `ind.MaterialiRichieste.Stato`
| Valoare | Semnificație |
|---------|-------------|
| `RICHIESTA` | Cerere trimisă, în așteptare la depozit |
| `PRONTA` | Material pregătit de depozit, în așteptare ridicare |
| `PRELEVATA` | Material ridicat de solicitant |

#### `dbo.MaterialConfigurations`
- `DateOut = NULL` → configurare **activă** (suprascrie valorile din TipoMateriali)
- `DateOut ≠ NULL` → configurare **dezactivată** (se folosesc valorile implicite din TipoMateriali)

---

## 12. Fluxul Complet de Lucru

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONFIGURARE (O SINGURĂ DATĂ)                │
│                                                                 │
│  1. Configurare WH WorkStation → Activare pe PC-ul depozitului │
│  2. Import Coduri (Aliniere) → Import Excel din Dynamics        │
│  3. Tipuri Materiale → Definire categorii + reguli implicite    │
│  4. Configurare Coduri → Override per-cod (opțional)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FLUX OPERAȚIONAL ZILNIC                     │
│                                                                 │
│  ┌──────────┐    auto     ┌──────────┐    auto     ┌──────────┐│
│  │SOLICITANT│───────────► │  DEPOZIT │───────────► │SOLICITANT││
│  │          │  10s poll   │   (WH)   │  10s poll   │          ││
│  │Trimite   │             │Popup roșu│             │Popup verde│
│  │cerere    │             │🔊 3 beeps│             │🔊 3 beeps│
│  │          │             │Pregătește│             │Confirmă  ││
│  │          │             │+ Stampă  │             │ridicare  ││
│  └──────────┘             └──────────┘             └──────────┘│
│                                                                 │
│  Stare:  RICHIESTA ──────► PRONTA ──────► PRELEVATA            │
└─────────────────────────────────────────────────────────────────┘
```

### Pasul 1 — Solicitantul
- Deschide **Solicitare Materiale** → selectează materialul → introduce cantitatea → trimite cererea
- Starea cererii: `RICHIESTA`

### Pasul 2 — Depozitul (automat)
- Pe PC-ul WH apare automat popup-ul roșu cu sunet de alarmă
- Personalul WH pregătește materialul fizic
- Apasă **✅ Pregătește și Confirmă** → se tipărește PDF-ul → starea devine `PRONTA`

### Pasul 3 — Solicitantul (automat)
- Pe PC-ul solicitantului apare automat popup-ul verde cu sunet
- Solicitantul ridică materialul
- Apasă **✅ Ridicat** → starea devine `PRELEVATA`

---

> **Document generat pentru uzul intern Vandewiele România.**  
> **Toate drepturile rezervate.**
