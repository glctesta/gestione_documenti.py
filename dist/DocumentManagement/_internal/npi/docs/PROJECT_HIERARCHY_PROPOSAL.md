# Proposta: Gerarchia Progetti NPI (Parent-Child)

## 📋 Contesto

Attualmente i progetti NPI sono **indipendenti**. Tuttavia, può capitare che vengano lanciati progetti NPI per prodotti che sono **sotto-prodotti** o **componenti** di un progetto NPI principale.

**Esempio pratico:**
- Progetto NPI principale: "Assemblaggio finale prodotto X"
- Progetti NPI figli:
  - "PCB del prodotto X"
  - "Firmware del prodotto X"
  - "Case del prodotto X"

Il progetto padre deve poter dipendere dal completamento dei progetti figli.

---

## 🎯 Obiettivi

1. **Collegamento gerarchico** tra progetti NPI (padre-figlio)
2. **Tracciamento delle dipendenze** tra progetti
3. **Visualizzazione della gerarchia** nell'interfaccia
4. **Validazione del completamento**: il progetto padre può essere completato solo se tutti i figli sono completati

---

## 💡 Soluzione Proposta a Livello Database

### Opzione 1: Self-Referencing (Raccomandato) ⭐

Aggiungi un campo `ParentProjectID` alla tabella `ProgettiNPI` che fa riferimento a se stessa.

#### SQL Script per Modifica

```sql
-- Script: ADD_PROJECT_HIERARCHY.sql
-- Aggiungi colonna ParentProjectID alla tabella ProgettiNPI

USE [Traceability_RS]
GO

-- 1. Aggiungi la colonna ParentProjectID
ALTER TABLE [dbo].[ProgettiNPI]
ADD [ParentProjectID] INT NULL;
GO

-- 2. Aggiungi la Foreign Key che fa riferimento alla stessa tabella
ALTER TABLE [dbo].[ProgettiNPI]
ADD CONSTRAINT FK_ProgettiNPI_ParentProject
    FOREIGN KEY ([ParentProjectID])
    REFERENCES [dbo].[ProgettiNPI]([ProgettoID])
    ON DELETE NO ACTION;  -- Impedisce cancellazione a cascata
GO

-- 3. Aggiungi un indice per migliorare le performance delle query
CREATE NONCLUSTERED INDEX IX_ProgettiNPI_ParentProjectID
ON [dbo].[ProgettiNPI]([ParentProjectID])
INCLUDE ([ProgettoID], [NomeProgetto], [StatoProgetto]);
GO

-- 4. Aggiungi un campo per indicare il livello nella gerarchia (opzionale ma utile)
ALTER TABLE [dbo].[ProgettiNPI]
ADD [HierarchyLevel] INT NULL DEFAULT 0;
GO

-- 5. Aggiungi un campo per il tipo di progetto (opzionale)
ALTER TABLE [dbo].[ProgettiNPI]
ADD [ProjectType] VARCHAR(50) NULL DEFAULT 'Standard';
-- Possibili valori: 'Standard', 'Parent', 'Child'
GO

PRINT '✅ Gerarchia progetti NPI aggiunta con successo!'
GO
```

#### Modifica al Modello SQLAlchemy (`data_models.py`)

```python
class ProgettoNPI(Base):
    __tablename__ = 'ProgettiNPI'
    __table_args__ = {'schema': 'dbo'}

    ProgettoId = Column('ProgettoID', Integer, primary_key=True, autoincrement=True)
    ProdottoID = Column(Integer, ForeignKey('dbo.Prodotti.ProdottoID'))
    StatoProgetto = Column(String(50))
    DataInizio = Column(DateTime)
    NomeProgetto = Column(String(255))
    ScadenzaProgetto = Column(DateTime, nullable=True)
    Version = Column(String(50), nullable=True)
    OwnerID = Column(Integer, ForeignKey('dbo.vw_Soggetti.SoggettoId'), nullable=True)
    Descrizione = Column(Text, nullable=True)
    
    # 🆕 NUOVI CAMPI PER GERARCHIA
    ParentProjectID = Column('ParentProjectID', Integer, ForeignKey('dbo.ProgettiNPI.ProgettoID'), nullable=True)
    HierarchyLevel = Column(Integer, default=0, nullable=True)
    ProjectType = Column(String(50), default='Standard', nullable=True)

    # Relationships esistenti
    prodotto = relationship("Prodotto", back_populates="progetti_npi")
    waves = relationship("WaveNPI", back_populates="progetto", cascade="all, delete-orphan")
    documenti = relationship("ProgettoDocumento", back_populates="progetto", cascade="all, delete-orphan")
    owner = relationship(
        "Soggetto",
        primaryjoin="foreign(ProgettoNPI.OwnerID) == Soggetto.SoggettoId",
        viewonly=True,
        uselist=False
    )
    
    # 🆕 NUOVE RELAZIONI PER GERARCHIA
    # Relazione per il progetto padre
    parent_project = relationship(
        "ProgettoNPI",
        remote_side=[ProgettoId],  # Questo indica che la FK è sul lato "child"
        backref="child_projects",   # Crea automaticamente la lista dei figli
        foreign_keys=[ParentProjectID]
    )
```

---

### Opzione 2: Tabella di Associazione Separata (Alternativa)

Se vuoi maggiore flessibilità (es. progetti che possono avere più padri), puoi creare una tabella di associazione.

#### SQL Script

```sql
-- Crea tabella di associazione ProjectHierarchy
CREATE TABLE [dbo].[ProjectHierarchy] (
    [HierarchyID] INT IDENTITY(1,1) PRIMARY KEY,
    [ParentProjectID] INT NOT NULL,
    [ChildProjectID] INT NOT NULL,
    [RelationType] VARCHAR(50) NULL,  -- 'Component', 'Dependency', etc.
    [CreatedDate] DATETIME DEFAULT GETDATE(),
    [CreatedBy] VARCHAR(255) NULL,
    
    CONSTRAINT FK_ProjectHierarchy_Parent
        FOREIGN KEY ([ParentProjectID])
        REFERENCES [dbo].[ProgettiNPI]([ProgettoID])
        ON DELETE NO ACTION,
    
    CONSTRAINT FK_ProjectHierarchy_Child
        FOREIGN KEY ([ChildProjectID])
        REFERENCES [dbo].[ProgettiNPI]([ProgettoID])
        ON DELETE NO ACTION,
    
    -- Evita duplicati
    CONSTRAINT UQ_ProjectHierarchy
        UNIQUE ([ParentProjectID], [ChildProjectID])
);
GO

-- Evita cicli (un progetto non può essere padre di se stesso)
ALTER TABLE [dbo].[ProjectHierarchy]
ADD CONSTRAINT CK_ProjectHierarchy_NoCycles
    CHECK ([ParentProjectID] <> [ChildProjectID]);
GO
```

---

## 📊 Vantaggi e Svantaggi

### Opzione 1: Self-Referencing ⭐ (Raccomandato)

✅ **Vantaggi:**
- Semplice da implementare
- Performance migliori (no JOIN aggiuntivi)
- Query più semplici
- Struttura ad albero chiara (ogni figlio ha un solo padre)

❌ **Svantaggi:**
- Ogni progetto può avere un solo padre (albero, non grafo)
- Meno flessibile per relazioni complesse

### Opzione 2: Tabella di Associazione

✅ **Vantaggi:**
- Maggiore flessibilità (un progetto può avere più padri)
- Possibilità di aggiungere metadati alla relazione
- Supporta relazioni many-to-many

❌ **Svantaggi:**
- Query più complesse
- Performance leggermente inferiori
- Maggiore complessità di gestione

---

## 🔍 Query di Esempio (Opzione 1)

### Recupera tutti i progetti figli di un progetto

```sql
SELECT 
    p.ProgettoID,
    p.NomeProgetto,
    p.StatoProgetto,
    p.HierarchyLevel
FROM [dbo].[ProgettiNPI] p
WHERE p.ParentProjectID = @ParentProjectID
ORDER BY p.HierarchyLevel, p.NomeProgetto;
```

### Recupera l'intera gerarchia (ricorsiva)

```sql
WITH ProjectTree AS (
    -- Anchor: Progetto principale
    SELECT 
        ProgettoID,
        NomeProgetto,
        ParentProjectID,
        StatoProgetto,
        0 AS Level,
        CAST(NomeProgetto AS VARCHAR(MAX)) AS Path
    FROM [dbo].[ProgettiNPI]
    WHERE ParentProjectID IS NULL
    
    UNION ALL
    
    -- Recursive: Progetti figli
    SELECT 
        p.ProgettoID,
        p.NomeProgetto,
        p.ParentProjectID,
        p.StatoProgetto,
        pt.Level + 1,
        CAST(pt.Path + ' > ' + p.NomeProgetto AS VARCHAR(MAX))
    FROM [dbo].[ProgettiNPI] p
    INNER JOIN ProjectTree pt ON p.ParentProjectID = pt.ProgettoID
)
SELECT * FROM ProjectTree
ORDER BY Path;
```

### Verifica se tutti i figli sono completati

```sql
-- Restituisce TRUE se tutti i progetti figli sono completati
SELECT 
    CASE 
        WHEN COUNT(CASE WHEN StatoProgetto != 'Completato' THEN 1 END) = 0 
        THEN 1 
        ELSE 0 
    END AS AllChildrenCompleted
FROM [dbo].[ProgettiNPI]
WHERE ParentProjectID = @ParentProjectID;
```

---

## 🎨 Visualizzazione UI - Idee

1. **Dashboard Progetti:** Mostra albero di progetti con indent
2. **Badge**: Icona 📦 per progetti padre, 📄 per figli
3. **Colore codificato**: Progetti padre in blu, figli in verde
4. **Filtri**: "Solo progetti padre", "Solo progetti figli", "Mostra gerarchia completa"
5. **Dettaglio progetto**: Sezione "Progetti collegati" con:
   - Link al progetto padre (se esiste)
   - Lista dei progetti figli (se esistono)

---

## ✅ Raccomandazione Finale

**Consiglio l'Opzione 1 (Self-Referencing)** perché:

1. ✅ Copre il 90% dei casi d'uso (un componente appartiene a un solo prodotto finale)
2. ✅ Più semplice da implementare e mantenere
3. ✅ Performance migliori
4. ✅ Query più intuitive
5. ✅ Facile da visualizzare in UI

---

## 📝 Prossimi Passi Implementativi

Dopo l'aggiornamento del database:

1. **Backend (Python):**
   - Aggiornare `data_models.py` con i nuovi campi
   - Creare funzioni in `npi_manager.py`:
     - `get_child_projects(project_id)`
     - `get_parent_project(project_id)`
     - `can_complete_project(project_id)` - verifica se i figli sono completati
     - `get_project_hierarchy(root_project_id)` - albero completo

2. **Frontend (Tkinter):**
   - Dashboard con visualizzazione ad albero
   - Dropdown per selezionare progetto padre quando si crea un progetto
   - Sezione "Progetti collegati" nella form progetto
   - Validazione: impedisci completamento se figli non sono completati

3. **Validazioni:**
   - Impedisci cicli (un progetto non può essere padre di un suo antenato)
   - Aggiorna automaticamente `HierarchyLevel` quando si assegna un padre

---

## 🚀 Pronto per l'implementazione!

Dimmi se sei d'accordo con questa proposta e possiamo procedere con:
1. Creazione dello script SQL
2. Aggiornamento del modello dati
3. Implementazione delle funzioni backend
4. Creazione dell'interfaccia utente
