# Aggiunta Owner e Descrizione Progetto NPI

## ✅ Implementazione Completata

Ho aggiunto i campi **Owner** e **Descrizione** nel tab "Prodotti" della configurazione NPI, permettendo di impostarli al momento della creazione del progetto.

## 📍 Dove Sono i Campi

### UI: Tab "Prodotti" → Sezione "Gestione Progetto NPI"

```
┌─────────────────────────────────────────────────────┐
│ Gestione Progetto NPI                               │
├─────────────────────────────────────────────────────┤
│ Versione: [____________]                            │
│                                                     │
│ Owner Progetto: [Seleziona Owner ▼]                │
│                                                     │
│ Descrizione Progetto:                               │
│ ┌─────────────────────────────────────────────────┐ │
│ │                                                 │ │
│ │  [Area di testo multilinea]                    │ │
│ │                                                 │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│          [Crea Progetto NPI]                        │
└─────────────────────────────────────────────────────┘
```

## 🗄️ Modifiche Database

### Script SQL

File: `.artifacts/sql_add_owner_description_to_progetti.sql`

```sql
ALTER TABLE dbo.ProgettiNPI
ADD Descrizione NVARCHAR(MAX) NULL,
    OwnerID INT NULL;
```

### Campi Aggiunti

| Campo | Tipo | Nullable | Descrizione |
|-------|------|----------|-------------|
| `OwnerID` | INT | YES | ID del responsabile del progetto (FK a vw_Soggetti) |
| `Descrizione` | NVARCHAR(MAX) | YES | Descrizione dettagliata del progetto |

## 🔧 Modifiche Codice

### 1. Model `ProgettoNPI` (`data_models.py`)

```python
class ProgettoNPI(Base):
    # ... campi esistenti ...
    OwnerID = Column(Integer, ForeignKey('dbo.vw_Soggetti.SoggettoId'), nullable=True)
    Descrizione = Column(Text, nullable=True)
    
    # Nuova relazione
    owner = relationship(
        "Soggetto",
        primaryjoin="foreign(ProgettoNPI.OwnerID) == Soggetto.SoggettoId",
        viewonly=True,
        uselist=False
    )
```

### 2. UI `ProductManagementFrame` (`config_window.py`)

**Campi aggiunti**:
- `self.project_owner_combo`: Combobox per selezionare l'owner
- `self.project_description_text`: Text widget per la descrizione

**Popolamento combobox**:
```python
def _load_products(self):
    # ... codice esistente ...
    
    # Carica i soggetti per il combobox owner
    soggetti = self.npi_manager.get_soggetti()
    self.soggetti_map = {s.Nome: s.SoggettoId for s in soggetti}
    self.project_owner_combo['values'] = [''] + list(self.soggetti_map.keys())
```

### 3. Creazione Progetto (`config_window.py`)

```python
def _create_npi_project(self):
    # Ottieni i dati dal form
    version = self.version_entry.get().strip() or None
    owner_name = self.project_owner_combo.get().strip()
    owner_id = self.soggetti_map.get(owner_name) if owner_name else None
    descrizione = self.project_description_text.get('1.0', tk.END).strip() or None
    
    # Crea il progetto con i nuovi parametri
    progetto = self.npi_manager.create_progetto_npi_for_prodotto(
        self.selected_product_id, 
        version,
        owner_id=owner_id,
        descrizione=descrizione
    )
```

### 4. Manager (`npi_manager.py`)

```python
def create_progetto_npi_for_prodotto(self, prodotto_id, version=None, owner_id=None, descrizione=None):
    nuovo_progetto = ProgettoNPI(
        ProdottoID=prodotto_id,
        StatoProgetto='Attivo',
        DataInizio=datetime.now(),
        Version=version,
        OwnerID=owner_id,
        Descrizione=descrizione
    )
```

## 📝 Workflow Utente

### Creazione Nuovo Progetto NPI

```
1. Apri "Configurazione NPI" → Tab "Prodotti"
   ↓
2. Seleziona un prodotto dalla lista
   ↓
3. Compila i campi:
   - Versione (opzionale)
   - Owner Progetto (opzionale) ← NUOVO
   - Descrizione (opzionale) ← NUOVO
   ↓
4. Click "Crea Progetto NPI"
   ↓
5. Progetto creato con Owner e Descrizione ✅
```

### Esempio Pratico

```
Prodotto: "Carpet Loom XYZ"
Versione: "1.0"
Owner: "Mario Rossi"
Descrizione: "Progetto per sviluppo nuovo telaio per tappeti
             con sistema di controllo automatico della tensione.
             Target market: Europa e Nord America.
             Budget: €500k"
```

## 🎯 Utilizzo Futuro

Questi campi saranno utilizzati per:

1. **Email Notifiche**: 
   - Email inviate "in behalf" dell'owner
   - Descrizione progetto inclusa nell'email

2. **Report**:
   - Owner visibile nei report Excel/PDF
   - Descrizione nei documenti di progetto

3. **Dashboard**:
   - Filtro per owner
   - Vista descrizione nei dettagli progetto

## ✅ Checklist Implementazione

### Database
- [ ] Eseguire script SQL `.artifacts/sql_add_owner_description_to_progetti.sql`
- [ ] Verificare campi aggiunti con query di verifica

### Codice
- [x] Model `ProgettoNPI` aggiornato
- [x] UI campi aggiunti in `ProductManagementFrame`
- [x] Combobox owner popolato
- [x] Metodo `create_progetto_npi_for_prodotto` aggiornato

### Test
- [ ] Test creazione progetto con owner e descrizione
- [ ] Test creazione progetto senza owner (NULL)
- [ ] Test creazione progetto senza descrizione (NULL)
- [ ] Verifica dati salvati correttamente nel database

## 📋 Chiavi di Traduzione

Le chiavi usate:
- `project_owner` → "Owner Progetto:"
- `project_description` → "Descrizione Progetto:"

Già esistenti nel sistema di traduzione.

---

**Data**: 23 Dicembre 2024  
**Versione**: 2.2.8.1  
**Stato**: ✅ Implementato - Richiede Esecuzione Script SQL
