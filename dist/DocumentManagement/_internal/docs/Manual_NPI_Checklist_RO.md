# 📋 Manual Utilizare — Fișa NPI Checklist (MD.RAQ.089)

**Versiune document:** 1.0  
**Data:** 24.03.2026  
**Aplicație:** TraceabilityRS — Document Management  

---

## 1. Prezentare Generală

Fișa **NPI Checklist** (MD.RAQ.089) este o digitalizare completă a checklist-ului utilizat în procesul de introducere a produselor noi (New Product Introduction). Aceasta permite:

- **Colectarea datelor** pentru fiecare fază de producție (SMT, PTH, ICT, FCT, Coating etc.)
- **Înregistrarea programelor** utilizate pe fiecare linie/mașină
- **Urmărirea materialelor** și echipamentelor indirecte de producție
- **Colectarea datelor cantitative** de producție (produse, inspectate, passed, failed)
- **Verificarea BOM** și FQC
- **Înregistrarea acțiunilor corective** și a operațiunilor de rework
- **Aprobarea finală** de către proprietarul proiectului NPI
- **Suport multi-sesiune** — datele pot fi completate în mai multe etape

### Arhitectură dinamică

Checklist-ul se adaptează automat la fiecare proiect, generând tab-uri (secțiuni) pornind de la **configurația familiilor NPI** asociate produsului. Astfel, un produs care necesită doar SMT și ICT va afișa doar acele secțiuni, fără PTH sau Coating.

---

## 2. Configurarea Inițială (Administratori)

### 2.1. Execuția scripturilor SQL

Înainte de utilizarea checklist-ului, administratorul bazei de date trebuie să execute două scripturi SQL pe baza de date `Traceability_RS`:

#### Script 1: `npi_checklist_schema.sql`
Creează **8 tabele** necesare stocării datelor:

| Nr | Tabela | Descriere |
|----|--------|-----------|
| 1 | `NpiChecklistSessions` | Sesiunile (header-ul) checklist-ului — date generale, responsabili, aprobare |
| 2 | `NpiChecklistPrograms` | Programele utilizate per fază (Printing, SPI, Pick&Place, AOI etc.) |
| 3 | `NpiChecklistMaterials` | Materiale, attrezzature, tools (Solder paste, Stencil, Glue etc.) |
| 4 | `NpiChecklistProductionData` | Date cantitative producție (produced, inspected, pass, fail) |
| 5 | `NpiChecklistVerifications` | Verificări BOM și FQC (conform/neconform, qty inspectată) |
| 6 | `NpiChecklistPreformingChecks` | Verificări pre-asamblare (preforming fixtures, tools) |
| 7 | `NpiChecklistActions` | Comentarii și acțiuni corective |
| 8 | `NpiChecklistRework` | Log-ul operațiunilor de rework (serial, fail ICT/FCT, diagnoză) |

**Execuție:**
```sql
-- În SQL Server Management Studio, deschide fișierul și execută:
USE Traceability_RS
GO
-- [restul scriptului se execută automat]
```

#### Script 2: `npi_checklist_family_alter.sql`
Adaugă coloane de configurare în tabela existentă `FamilyNpis`:

| Coloană | Tip | Descriere |
|---------|-----|-----------|
| `ChecklistSection` | NVARCHAR(100) | Numele secțiunii checklist (ex: SMT_TOP, PTH, ICT) |
| `CL_HasPrograms` | BIT | Secțiunea conține programe (Da/Nu) |
| `CL_HasMaterials` | BIT | Secțiunea conține materiale/tools (Da/Nu) |
| `CL_HasProductionData` | BIT | Secțiunea conține date cantitative producție (Da/Nu) |
| `CL_HasVerification` | BIT | Secțiunea conține verificări BOM/FQC (Da/Nu) |
| `CL_HasPreformingChecks` | BIT | Secțiunea conține verificări pre-asamblare (Da/Nu) |
| `CL_HasCoating` | BIT | Secțiunea conține date coating/lăcuire (Da/Nu) |
| `CL_SortOrder` | INT | Ordinea de afișare în interfață (0 = primul tab) |

---

### 2.2. Configurarea Familiilor NPI

Configurarea se face din meniul principal al aplicației:

**Meniu → NPI → Configurare NPI**

Se deschide fereastra de configurare cu mai multe tab-uri. Tab-ul **Famiglie** permite:

1. **Selectarea unei familii** din lista din stânga
2. **Vizualizarea task-urilor** deja asociate familiei respective (în panoul din dreapta, secțiunea "Task Collegati")
3. **Filtrarea task-urilor** cu ajutorul câmpului de căutare 🔍

#### Setarea coloanelor Checklist

Pentru ca o familie să apară ca secțiune în checklist, trebuie configurat direct în baza de date:

```sql
-- Exemplu: Configurarea familiei SMT TOP (FamilyNpiID = 1)
UPDATE dbo.FamilyNpis
SET ChecklistSection = 'SMT TOP',
    CL_HasPrograms = 1,        -- Da, avem programe
    CL_HasMaterials = 1,       -- Da, avem materiale (solder paste, stencil)
    CL_HasProductionData = 1,  -- Da, colectăm date cantitative
    CL_HasVerification = 1,    -- Da, avem verificări BOM/FQC
    CL_HasPreformingChecks = 0,-- Nu, nu are pre-assembly
    CL_HasCoating = 0,         -- Nu, nu are coating
    CL_SortOrder = 1           -- Se afișează primul (după header)
WHERE FamilyNpiID = 1;
```

**Exemple tipice de configurare:**

| Familie | ChecklistSection | Programs | Materials | Prod.Data | Verification | Preforming | Coating | Sort |
|---------|-----------------|----------|-----------|-----------|-------------|------------|---------|------|
| SMT TOP | SMT TOP | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | 1 |
| SMT BOTTOM | SMT BOTTOM | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | 2 |
| PTH | PTH | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | 3 |
| ICT/FCT | ICT | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | 4 |
| Coating | COATING | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | 5 |

> **⚠️ Important:** Doar familiile care au `ChecklistSection` completat ȘI sunt asociate la task-uri active ale proiectului vor genera tab-uri în fereastra checklist-ului.

---

### 2.3. Asocierea Task-urilor la Familii

Tab-ul **Legare Familii** din fereastra de configurare NPI permite:

1. Selectați o **familie** din lista de sus
2. Vedeți **task-urile disponibile** (neconectate) în panoul din dreapta
3. Folosiți **filtrul** 🔍 pentru a găsi rapid un task după nume
4. Apăsați **"Collega"** pentru a asocia task-ul selectat la familie
5. Apăsați **"Scollega"** pentru a elimina asocierea

> **Notă:** Task-urile asociate la familii determină ce secțiuni checklist vor fi vizibile pentru un anumit proiect. Un proiect va afișa secțiuni doar pentru familiile care au task-uri active în acel proiect.

---

## 3. Utilizarea Checklist-ului (Operatori / Ingineri)

### 3.1. Deschiderea Checklist-ului

1. Deschideți **Gestione Progetto NPI** (din meniul NPI → selectați proiectul)
2. În fereastra de management al proiectului, apăsați butonul **📋 Checklist**
3. Se deschide fereastra **NPI Checklist** cu tab-urile specifice produsului

### 3.2. Structura Ferestrei

Fereastra checklist-ului conține:

#### ➊ Bara Sesiuni (sus)
- **Sesiune** — combobox pentru selectarea sesiunii de lucru
- **➕ Nuova** — creează o sesiune nouă
- **💾 Salva** — salvează datele curente
- **🗑️ Elimina** — șterge sesiunea selectată
- **✅ Approva** — aprobă definitiv checklist-ul (vizibil doar pentru owner-ul proiectului)

#### ➋ Tab Intestazione (întotdeauna prezent)
Acest tab conține datele generale ale verificării:

| Câmp | Descriere |
|------|-----------|
| **PN** | Codul produsului (preluat automat din proiect) |
| **Nr. KIT (Ordine)** | Selectați din lista de ordini asociate produsului |
| **QTY** | Cantitatea din ordin (se completează automat la selectarea ordinului) |
| **Data** | Data verificării (implicit: data curentă) |
| **Responsabil Calitate Proces** | Numele responsabilului calitate |
| **Responsabil Producție** | Numele responsabilului producție |
| **Responsabil Inginer Process** | Numele inginerului de proces |
| **Faze Proces** | Lista secțiunilor active pentru acest proiect |

#### ➌ Tab-uri Dinamice (generate automat)
Fiecare secțiune configurată (SMT TOP, PTH, ICT etc.) generează un tab separat cu sub-secțiunile specifice:

**Programe** (dacă `CL_HasPrograms = 1`)
- Process Step — etapa procesului (Printing, SPI, Pick&Place, Reflow, AOI)
- Line nr — numărul liniei/mașinii
- Program name — numele programului
- Result — OK / Not OK
- Responsible — cine a verificat
- Date — data verificării
- Note — observații

**Materiale / Fixtures / Tools** (dacă `CL_HasMaterials = 1`)
- Material / Tool — tipul (Solder paste, Glue, Stencil TOP, Stencil BOTTOM, Solder Bar etc.)
- Code / PN — codul materialului
- Note — observații

**Preforming / Pre-assembly** (dacă `CL_HasPreformingChecks = 1`)
- Check Item — elementul verificat
- Result — OK / Not OK
- Note — observații

**Production Data** (dacă `CL_HasProductionData = 1`)
- Process — sub-procesul (ex: SMT_AOI_TOP, XRAY_SMT)
- Date — data producției
- Produced — cantitate produsă
- Inspected — cantitate inspectată
- Pass — cantitate conformă
- Fail — cantitate neconformă
- Note — observații

**Coating** (dacă `CL_HasCoating = 1`)
- Furnizor — furnizorul serviciului de coating
- Date — data aplicării

**Verification** (dacă `CL_HasVerification = 1`)
- Section — secțiunea verificată (BOM_SMT, FQC_PTH etc.)
- Conform / Neconform — status conformitate
- Inspected Qty — cantitate inspectată
- Result — OK / NC
- CQ Responsible — responsabil calitate
- Date — data verificării
- Note — observații

#### ➍ Tab Azioni/Rework (întotdeauna prezent)
Ultimul tab conține două secțiuni fixe:

**Comentarii / Acțiuni:**
- Comentarii — descrierea problemei sau acțiunii
- Responsabil — persoana responsabilă
- Data închidere — termenul limită
- Status — Aperto / Chiuso (deschis / închis)

**REWORK:**
- Serial nr — numărul de serie al plăcii
- FAIL ICT — defectul constatat la ICT
- FAIL FCT — defectul constatat la FCT
- Diagnoză — analiza cauzei
- Referință — referința componentei
- Rework resp — cine a efectuat rework-ul

### 3.3. Adăugarea și Editarea Datelor

#### Adăugarea unui rând nou
1. Apăsați butonul **➕** de sub tabelul dorit
2. Se deschide un dialog cu câmpurile specifice secțiunii
3. Completați câmpurile și apăsați **Salva**
4. Rândul apare în tabel

#### Editarea unui rând existent
1. Selectați rândul din tabel
2. Apăsați butonul **✏️**
3. Se deschide dialogul de editare cu datele curente
4. Modificați și apăsați **Salva**

#### Ștergerea unui rând
1. Selectați rândul din tabel
2. Apăsați butonul **❌**
3. Rândul este eliminat imediat

> **⚠️ Atenție:** Ștergerea unui rând NU necesită confirmare. Dacă ați șters accidental, puteți reîncărca sesiunea (selectați-o din combobox).

---

## 4. Gestionarea Sesiunilor

### 4.1. Crearea unei Sesiuni Noi
- Apăsați **➕ Nuova** în bara de sus
- Se creează o sesiune goală cu data curentă
- Statusul inițial: **"InLavorazione"** (în lucru)

### 4.2. Salvarea
- Apăsați **💾 Salva** pentru a salva toate datele din toate tab-urile
- Se pot face **salvări intermediare** — nu este necesar să completați totul dintr-o dată
- La fiecare salvare se actualizează câmpul `LastModifiedBy` și `LastModifiedDate`

### 4.3. Ștergerea
- Selectați sesiunea din combobox
- Apăsați **🗑️ Elimina**
- Se cere confirmare înainte de ștergere
- Ștergerea este **soft delete** (câmpul `DateOut` este setat)

### 4.4. Aprobarea Finală
- Butonul **✅ Approva** este vizibil **doar pentru owner-ul proiectului NPI**
- După aprobare:
  - Statusul se schimbă în **"Completato"**
  - Se înregistrează `ApprovedBy` și `ApprovedDate`
  - Sesiunea **nu mai poate fi modificată**

---

## 5. Fluxul Complet de Lucru

```
    ┌─────────────────────────────────────────┐
    │   1. Administrator configurează         │
    │      familiile NPI în baza de date       │
    │      (ChecklistSection + flag-uri)       │
    └───────────────┬─────────────────────────┘
                    ▼
    ┌─────────────────────────────────────────┐
    │   2. Administrator asociază task-uri     │
    │      la familii (Configurare NPI →       │
    │      tab "Legare Familii")               │
    └───────────────┬─────────────────────────┘
                    ▼
    ┌─────────────────────────────────────────┐
    │   3. Operator deschide proiectul NPI    │
    │      și apasă butonul "Checklist"       │
    └───────────────┬─────────────────────────┘
                    ▼
    ┌─────────────────────────────────────────┐
    │   4. Sistemul generează tab-urile       │
    │      automat pe baza familiilor          │
    │      active ale proiectului              │
    └───────────────┬─────────────────────────┘
                    ▼
    ┌─────────────────────────────────────────┐
    │   5. Operator creează sesiune nouă      │
    │      și completează datele per fază      │
    │      (salvare intermediară posibilă)     │
    └───────────────┬─────────────────────────┘
                    ▼
    ┌─────────────────────────────────────────┐
    │   6. Owner proiect NPI aprobă           │
    │      checklist-ul → Status: Completat   │
    └─────────────────────────────────────────┘
```

---

## 6. Întrebări frecvente (FAQ)

**Î: De ce nu apare niciun tab în checklist?**  
R: Familiile NPI ale proiectului nu au configurat câmpul `ChecklistSection`. Contactați administratorul pentru a seta coloanele necesare în tabela `FamilyNpis`.

**Î: De ce un anumit produs are mai puține secțiuni decât altul?**  
R: Secțiunile depind de task-urile active ale proiectului. Dacă un produs nu necesită PTH (ex: placă doar SMD), familia PTH nu este asociată, deci secțiunea nu apare.

**Î: Pot reveni la o sesiune mai veche și modifica datele?**  
R: Da, dacă sesiunea nu a fost aprobată. Selectați sesiunea din combobox și modificați datele.

**Î: Cine poate aproba checklist-ul?**  
R: Doar **owner-ul proiectului NPI** (proprietarul desemnat la crearea proiectului) are vizibil butonul de aprobare.

**Î: Ce se întâmplă după aprobare?**  
R: Sesiunea devine doar citire (read-only). Nu mai pot fi adăugate sau modificate date. Se înregistrează automat cine și când a aprobat.

**Î: Cum filtrăm task-urile în configurare?**  
R: În tab-ul "Legare Familii" al configurației NPI, folosiți câmpul de căutare 🔍 deasupra listei de task-uri. Tastați câteva litere din numele task-ului. Apăsați **↺ Reset** pentru a anula filtrul.

---

## 7. Tabele Bază de Date — Referință Tehnică

### Diagrama relațiilor

```
NpiChecklistSessions (1)
    ├── NpiChecklistPrograms (N)
    ├── NpiChecklistMaterials (N)
    ├── NpiChecklistProductionData (N)
    ├── NpiChecklistVerifications (N)
    ├── NpiChecklistPreformingChecks (N)
    ├── NpiChecklistActions (N)
    └── NpiChecklistRework (N)

FamilyNpis (configurare)
    └── ChecklistSection + CL_* flags → definește secțiunile
```

Toate tabelele de date sunt legate de `NpiChecklistSessions` prin cheia externă `SessionId`.

---

*Document generat automat — TraceabilityRS v2.3.8.9*
