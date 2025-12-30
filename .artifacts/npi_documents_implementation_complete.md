# Gestione Documenti Progetto NPI - Implementazione Completata

## ✅ Implementazione Completata

Ho aggiunto la **gestione documenti** direttamente nel **tab "Prodotti"** della Configurazione NPI, esattamente dove hai richiesto!

## 📍 Dove Sono i Campi

### UI: Configurazione NPI → Tab "Prodotti" → Sezione "Gestione Progetto NPI"

```
┌─────────────────────────────────────────────────────┐
│ Gestione Progetto NPI                               │
├─────────────────────────────────────────────────────┤
│ Versione: [____]                                    │
│ Owner Progetto: [Seleziona ▼]                       │
│ Descrizione Progetto:                               │
│ ┌─────────────────────────────────────────────────┐ │
│ │ [Area di testo]                                 │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ Documenti Progetto:                                 │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Nome File          │ Dimensione                 │ │
│ │ image.png          │ 125.3 KB                   │ │
│ │ spec.pdf           │ 450.1 KB                   │ │
│ └─────────────────────────────────────────────────┘ │
│ [Aggiungi] [Elimina]                                │
│                                                     │
│          [Crea Progetto NPI]                        │
└─────────────────────────────────────────────────────┘
```

## 🔧 Funzionalità Implementate

### 1. Aggiungere Documenti
- Click su "Aggiungi"
- Seleziona file (immagini, PDF, Word, Excel, qualsiasi file)
- Il file viene caricato in memoria temporaneamente
- Appare nella lista con nome e dimensione

### 2. Rimuovere Documenti
- Seleziona documento dalla lista
- Click su "Elimina"
- Il documento viene rimosso dalla lista temporanea

### 3. Creazione Progetto con Documenti
- Quando clicki "Crea Progetto NPI":
  1. Crea il progetto con versione, owner e descrizione
  2. Salva automaticamente tutti i documenti allegati nel database
  3. Pulisce la lista documenti
  4. Pronto per un nuovo progetto

## 🗄️ Struttura Database

### Tabella `ProgettoDocumenti`

```sql
CREATE TABLE dbo.ProgettoDocumenti (
    DocumentoID INT PRIMARY KEY IDENTITY(1,1),
    ProgettoID INT NOT NULL,  -- FK a ProgettiNPI
    NomeFile NVARCHAR(255) NOT NULL,
    TipoFile NVARCHAR(50) NULL,  -- MIME type
    Dimensione INT NULL,  -- bytes
    Contenuto VARBINARY(MAX) NOT NULL,  -- File binario
    Descrizione NVARCHAR(500) NULL,
    CaricatoDa NVARCHAR(255) NULL,
    DataCaricamento DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT FK_ProgettoDocumenti_Progetto 
        FOREIGN KEY (ProgettoID) REFERENCES dbo.ProgettiNPI(ProgettoID)
        ON DELETE CASCADE
);
```

## 📝 Modifiche Codice

### 1. `config_window.py` - ProductManagementFrame

**Aggiunte UI**:
```python
# Lista documenti con Treeview
self.docs_tree = ttk.Treeview(...)

# Bottoni
ttk.Button(..., command=self._add_project_document)
ttk.Button(..., command=self._remove_project_document)

# Lista temporanea
self.project_documents = []
```

**Metodi Aggiunti**:
- `_add_project_document()`: Apre file dialog e aggiunge file alla lista
- `_remove_project_document()`: Rimuove file selezionato dalla lista
- `_clear_project_documents()`: Pulisce la lista dopo creazione progetto
- `_get_mime_type()`: Determina il tipo MIME del file

**Salvataggio Documenti**:
```python
def _create_npi_project(self):
    # ... crea progetto ...
    
    # Salva documenti
    if self.project_documents:
        for doc_data in self.project_documents:
            self.npi_manager.add_progetto_documento(
                progetto_id=progetto.ProgettoId,
                nome_file=doc_data['nome'],
                tipo_file=doc_data['tipo'],
                dimensione=doc_data['dimensione'],
                contenuto=doc_data['contenuto'],
                descrizione=None,
                caricato_da=None
            )
```

### 2. `data_models.py` - Model ProgettoDocumento

```python
class ProgettoDocumento(Base):
    __tablename__ = 'ProgettoDocumenti'
    __table_args__ = {'schema': 'dbo'}
    
    DocumentoID = Column(Integer, primary_key=True, autoincrement=True)
    ProgettoID = Column(Integer, ForeignKey('dbo.ProgettiNPI.ProgettoID'), nullable=False)
    NomeFile = Column(String(255), nullable=False)
    TipoFile = Column(String(50), nullable=True)
    Dimensione = Column(Integer, nullable=True)
    Contenuto = Column(LargeBinary, nullable=False)
    Descrizione = Column(String(500), nullable=True)
    CaricatoDa = Column(String(255), nullable=True)
    DataCaricamento = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    progetto = relationship("ProgettoNPI", back_populates="documenti")
```

**Aggiornato ProgettoNPI**:
```python
class ProgettoNPI(Base):
    # ... campi esistenti ...
    
    # Nuova relationship
    documenti = relationship("ProgettoDocumento", back_populates="progetto", cascade="all, delete-orphan")
```

### 3. `npi_manager.py` - Metodi Gestione Documenti

```python
def add_progetto_documento(self, progetto_id, nome_file, tipo_file, dimensione, 
                           contenuto, descrizione=None, caricato_da=None):
    """Aggiunge un documento al progetto."""
    # Crea ProgettoDocumento e salva nel database

def get_progetto_documenti(self, progetto_id):
    """Recupera tutti i documenti di un progetto."""
    # Ritorna lista documenti

def get_progetto_documento(self, documento_id):
    """Recupera un singolo documento."""
    # Ritorna documento specifico

def delete_progetto_documento(self, documento_id):
    """Elimina un documento."""
    # Elimina documento dal database
```

## 🎯 Workflow Utente

### Creazione Progetto con Documenti

```
1. Apri Configurazione NPI → Tab "Prodotti"
   ↓
2. Seleziona un prodotto dalla lista
   ↓
3. Compila:
   - Versione: "1.0"
   - Owner: "Mario Rossi"
   - Descrizione: "Progetto per nuovo telaio..."
   ↓
4. Aggiungi documenti:
   - Click "Aggiungi"
   - Seleziona "design_sketch.png" → Aggiunto
   - Click "Aggiungi"
   - Seleziona "specifications.pdf" → Aggiunto
   - Click "Aggiungi"
   - Seleziona "budget.xlsx" → Aggiunto
   ↓
5. Click "Crea Progetto NPI"
   ↓
6. Sistema:
   - Crea progetto NPI
   - Salva 3 documenti nel database
   - Pulisce form
   ↓
7. Progetto creato con documenti! ✅
```

## 📄 File Creati

1. **`.artifacts/sql_create_progetto_documenti.sql`**
   - Script per creare tabella `ProgettoDocumenti`

2. **`.artifacts/sql_translations_project_documents.sql`**
   - Traduzioni complete (IT, EN, RO, DE, SV)

3. **`.artifacts/npi_project_documents_spec.md`**
   - Specifica completa originale

4. **Questo documento**
   - Riepilogo implementazione

## ✅ Checklist

### Database
- [ ] Eseguire `sql_create_progetto_documenti.sql`
- [ ] Eseguire `sql_translations_project_documents.sql`
- [ ] Eseguire `sql_add_owner_description_to_progetti.sql` (se non già fatto)

### Test
- [ ] Test aggiunta documento
- [ ] Test rimozione documento
- [ ] Test creazione progetto con documenti
- [ ] Test creazione progetto senza documenti
- [ ] Verifica documenti salvati nel database

## 🔑 Tipi File Supportati

Il sistema riconosce automaticamente:
- **Immagini**: PNG, JPG, JPEG, GIF, BMP
- **PDF**: Documenti PDF
- **Word**: DOC, DOCX
- **Excel**: XLS, XLSX
- **Qualsiasi altro file**: Salvato come `application/octet-stream`

## 💾 Storage

- **Dove**: Database SQL Server, tabella `ProgettoDocumenti`
- **Come**: VARBINARY(MAX) - file binario completo
- **Dimensione**: Nessun limite teorico (dipende da SQL Server)
- **Eliminazione**: Automatica quando si elimina il progetto (CASCADE)

---

**Data**: 23 Dicembre 2024  
**Versione**: 2.2.8.1  
**Stato**: ✅ Implementato - Richiede Esecuzione Script SQL
