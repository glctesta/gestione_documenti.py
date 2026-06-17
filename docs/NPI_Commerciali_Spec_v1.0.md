# NPI — Gestione Commerciali e associazione ai progetti
## v1.0 (BOZZA — in attesa di conferma). Nessuna modifica al codice/DB effettuata.

> Attendo conferma e le risposte ai *Punti aperti* (§5) prima di migrare lo schema e scrivere codice.

---

## 1. Obiettivo
- Nuovo TAB **"Commerciale"** (dopo "Progetti") nella form `_configura_catalogo_task_npi`
  (`NpiConfigWindow`), per gestire i commerciali a cui fanno capo i progetti NPI:
  **nome, email, telefono, società di appartenenza**.
- Possibilità di **associare i commerciali ai progetti** — scelta confermata: **per cliente**
  (tutti i progetti di un cliente ereditano il commerciale).

## 2. Decisioni confermate
- I commerciali sono righe di **`dbo.Soggetti`** con `IsCommercial = 1`.
- Colonne da aggiungere a `Soggetti`:
  - `Telefono NVARCHAR(30) NULL`
  - `IsCommercial BIT NOT NULL DEFAULT 0`
  - `IdSite SMALLINT NULL` → **società di appartenenza**, FK a `dbo.Sites.IDSite`
    (scelta tra i siti con `IsSupplier IS NULL`: oggi AROS / EUTRON / ROJ).
- Associazione commerciale↔progetti = **per cliente** (non per singolo progetto).

## 3. Schema dati (proposto)
```sql
ALTER TABLE dbo.Soggetti ADD Telefono NVARCHAR(30) NULL;
ALTER TABLE dbo.Soggetti ADD IsCommercial BIT NOT NULL CONSTRAINT DF_Soggetti_IsCommercial DEFAULT 0;
ALTER TABLE dbo.Soggetti ADD IdSite SMALLINT NULL;   -- FK -> Sites.IDSite (società del commerciale)
-- (FK opzionale)
-- ALTER TABLE dbo.Soggetti ADD CONSTRAINT FK_Soggetti_Sites FOREIGN KEY (IdSite) REFERENCES dbo.Sites(IDSite);
```
**Associazione per cliente** — proposta tabella di legame:
```sql
CREATE TABLE dbo.CommercialeCliente (
    IDSiteCliente SMALLINT  NOT NULL,   -- cliente = Sites.IDSite con IsSupplier = 1
    SoggettoID    INT        NOT NULL,   -- commerciale = Soggetti.SoggettoID (IsCommercial=1)
    DateOut       DATETIME   NULL,
    CONSTRAINT PK_CommercialeCliente PRIMARY KEY (IDSiteCliente, SoggettoID)
);
```

## 4. UI
### 4.1 TAB "Commerciale" (nuovo, dopo "Progetti")
Modellato su `SubjectManagementFrame` (CRUD su `Soggetti`). Campi:
| Campo UI | Colonna Soggetti |
|---|---|
| Nome | NomeSoggetto |
| Email | Email |
| Telefono | Telefono |
| Società (combo) | IdSite (da `Sites` WHERE `IsSupplier IS NULL`) |
| (fisso) | IsCommercial = 1 |
Lista + form Aggiungi/Modifica/Elimina. Mostra solo i soggetti con `IsCommercial = 1`.

### 4.2 Associazione per cliente
Nel TAB Progetti (o nel TAB Commerciale) una sezione: scegli un **cliente** (Site IsSupplier=1)
e assegna uno o più **commerciali** → righe in `CommercialeCliente`.

## 5. Punti aperti (da confermare)
- **P1 — Cos'è il "cliente" per l'associazione?** `Sites` con `IsSupplier = 1` (come il
  "cliente finale" NPI di `get_suppliers()`)? *(assunto sì)*
- **P2 — Come risale un progetto al cliente-Site?** `Prodotti.Cliente` è una **stringa libera**
  (es. 'Electrolux'), non una FK a `Sites`. Per mostrare "il commerciale di questo progetto" serve
  una corrispondenza prodotto→cliente-Site. Opzioni:
  - (a) abbinare per nome (`Prodotti.Cliente` = `Sites.SiteName`) — fragile;
  - (b) associare i commerciali direttamente alla **stringa `Prodotti.Cliente`** (tabella
    `CommercialeCliente(ClienteNome NVARCHAR, SoggettoID)`) invece che al Site;
  - (c) aggiungere un `IDSiteCliente` ai Prodotti e mapparlo (più invasivo).
  → **Quale preferisci?** (propongo (b): associare alla stringa Cliente, coerente con come i
  progetti già identificano il cliente, zero mapping fragile).
- **P3 — Un cliente può avere più commerciali** o uno solo? *(propongo: più, con tabella di legame)*
- **P4 — Dove metto la UI di associazione**: nel TAB Progetti o nel TAB Commerciale?

## 6. File da toccare (previsti)
- `setup_*` / script SQL: ALTER `Soggetti` (+3 col) e CREATE tabella legame.
- `npi/npi_manager.py`: metodi `get_commerciali`, `create/update/delete_commerciale`,
  `get_sites_commerciali` (IsSupplier NULL), `get_clienti` (IsSupplier=1),
  `get/set_commerciali_per_cliente`.
- `npi/windows/config_window.py`: nuovo `CommercialeManagementFrame` + tab; UI associazione.
- `main.py`: eventuale combo nella selezione/gestione progetti.
- Traduzioni (5 lingue) per le nuove etichette.

---
*In attesa di conferma e risposte a §5 (in particolare P2) prima di procedere.*
