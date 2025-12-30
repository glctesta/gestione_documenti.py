# Gestione Documenti e Modifica Intestazione Progetti NPI

## 📋 Requisiti

### 1. Modifica Dati Intestazione
- **Chi**: Solo l'owner del progetto può modificare i dati di intestazione
- **Cosa**: Versione, Owner, Descrizione, Date progetto
- **Dove**: Nella finestra di gestione progetto (`project_window.py`)

### 2. Gestione Documenti Progetto
- **Cosa**: Allegare immagini e documenti al progetto
- **Dove**: Nella configurazione progetto (sia creazione che modifica)
- **Storage**: File salvati come BLOB nel database

### 3. Nuova Tabella Database
- **Nome**: `ProgettoDocumenti`
- **Scopo**: Mantenere documenti allegati al progetto

---

## 🗄️ Struttura Database

### Tabella `ProgettoDocumenti`

```sql
CREATE TABLE dbo.ProgettoDocumenti (
    DocumentoID INT PRIMARY KEY IDENTITY(1,1),
    ProgettoID INT NOT NULL,
    NomeFile NVARCHAR(255) NOT NULL,
    TipoFile NVARCHAR(50) NULL,  -- es: 'image/png', 'application/pdf'
    Dimensione INT NULL,  -- in bytes
    Contenuto VARBINARY(MAX) NOT NULL,  -- File binario
    Descrizione NVARCHAR(500) NULL,
    CaricatoDa NVARCHAR(255) NULL,  -- Nome utente che ha caricato
    DataCaricamento DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT FK_ProgettoDocumenti_Progetto 
        FOREIGN KEY (ProgettoID) REFERENCES dbo.ProgettiNPI(ProgettoID)
        ON DELETE CASCADE
);

-- Indice per performance
CREATE INDEX IX_ProgettoDocumenti_ProgettoID 
    ON dbo.ProgettoDocumenti(ProgettoID);
```

### Campi Spiegati

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `DocumentoID` | INT | Chiave primaria auto-incrementale |
| `ProgettoID` | INT | FK al progetto NPI |
| `NomeFile` | NVARCHAR(255) | Nome originale del file |
| `TipoFile` | NVARCHAR(50) | MIME type (image/png, application/pdf, etc.) |
| `Dimensione` | INT | Dimensione file in bytes |
| `Contenuto` | VARBINARY(MAX) | Contenuto binario del file |
| `Descrizione` | NVARCHAR(500) | Descrizione opzionale del documento |
| `CaricatoDa` | NVARCHAR(255) | Utente che ha caricato il file |
| `DataCaricamento` | DATETIME | Timestamp caricamento |

---

## 🔧 Implementazione Codice

### 1. Model SQLAlchemy (`data_models.py`)

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
    
    # Relationship
    progetto = relationship("ProgettoNPI", back_populates="documenti")

# Aggiornare ProgettoNPI
class ProgettoNPI(Base):
    # ... campi esistenti ...
    
    # Nuova relationship
    documenti = relationship(
        "ProgettoDocumento", 
        back_populates="progetto",
        cascade="all, delete-orphan"
    )
```

### 2. UI - Sezione Documenti in `project_window.py`

```python
# Nuovo frame per documenti progetto
docs_frame = ttk.LabelFrame(main_frame, text=self.lang.get('project_documents', 'Documenti Progetto'))
docs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Lista documenti
docs_list_frame = ttk.Frame(docs_frame)
docs_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

cols = ('Nome File', 'Tipo', 'Dimensione', 'Caricato Da', 'Data')
self.docs_tree = ttk.Treeview(docs_list_frame, columns=cols, show='headings', height=5)
for col in cols:
    self.docs_tree.heading(col, text=col)
self.docs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(docs_list_frame, orient=tk.VERTICAL, command=self.docs_tree.yview)
self.docs_tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Bottoni gestione documenti
docs_buttons = ttk.Frame(docs_frame)
docs_buttons.pack(fill=tk.X, padx=5, pady=5)

ttk.Button(docs_buttons, text='Aggiungi Documento', command=self._add_document).pack(side=tk.LEFT, padx=5)
ttk.Button(docs_buttons, text='Visualizza', command=self._view_document).pack(side=tk.LEFT, padx=5)
ttk.Button(docs_buttons, text='Scarica', command=self._download_document).pack(side=tk.LEFT, padx=5)
ttk.Button(docs_buttons, text='Elimina', command=self._delete_document).pack(side=tk.LEFT, padx=5)
```

### 3. Metodi Gestione Documenti

```python
def _add_document(self):
    """Aggiunge un documento al progetto."""
    if not self.progetto:
        return
    
    # Seleziona file
    file_path = filedialog.askopenfilename(
        title=self.lang.get('select_document', 'Seleziona Documento'),
        filetypes=[
            ('Tutti i file', '*.*'),
            ('Immagini', '*.png;*.jpg;*.jpeg;*.gif;*.bmp'),
            ('PDF', '*.pdf'),
            ('Word', '*.doc;*.docx'),
            ('Excel', '*.xls;*.xlsx')
        ]
    )
    
    if not file_path:
        return
    
    # Chiedi descrizione
    desc_window = tk.Toplevel(self)
    desc_window.title(self.lang.get('document_description', 'Descrizione Documento'))
    desc_window.geometry('400x150')
    desc_window.transient(self)
    desc_window.grab_set()
    
    ttk.Label(desc_window, text='Descrizione (opzionale):').pack(pady=10)
    desc_entry = ttk.Entry(desc_window, width=50)
    desc_entry.pack(pady=5)
    
    def save_doc():
        descrizione = desc_entry.get().strip() or None
        try:
            # Leggi file
            with open(file_path, 'rb') as f:
                contenuto = f.read()
            
            nome_file = os.path.basename(file_path)
            tipo_file = self._get_mime_type(nome_file)
            dimensione = len(contenuto)
            
            # Salva nel database
            self.npi_manager.add_progetto_documento(
                progetto_id=self.progetto.ProgettoId,
                nome_file=nome_file,
                tipo_file=tipo_file,
                dimensione=dimensione,
                contenuto=contenuto,
                descrizione=descrizione,
                caricato_da=self.logged_in_user
            )
            
            messagebox.showinfo('Successo', 'Documento aggiunto con successo')
            self._load_project_documents()
            desc_window.destroy()
            
        except Exception as e:
            logger.error(f"Errore aggiunta documento: {e}")
            messagebox.showerror('Errore', f'Impossibile aggiungere il documento:\n{e}')
    
    ttk.Button(desc_window, text='Salva', command=save_doc).pack(pady=10)

def _view_document(self):
    """Visualizza il documento selezionato."""
    selection = self.docs_tree.selection()
    if not selection:
        messagebox.showwarning('Attenzione', 'Seleziona un documento')
        return
    
    doc_id = int(self.docs_tree.item(selection[0], 'text'))
    
    try:
        documento = self.npi_manager.get_progetto_documento(doc_id)
        
        # Salva temporaneamente e apri
        temp_path = os.path.join(tempfile.gettempdir(), documento.NomeFile)
        with open(temp_path, 'wb') as f:
            f.write(documento.Contenuto)
        
        os.startfile(temp_path)
        
    except Exception as e:
        logger.error(f"Errore visualizzazione documento: {e}")
        messagebox.showerror('Errore', f'Impossibile visualizzare il documento:\n{e}')

def _download_document(self):
    """Scarica il documento selezionato."""
    selection = self.docs_tree.selection()
    if not selection:
        messagebox.showwarning('Attenzione', 'Seleziona un documento')
        return
    
    doc_id = int(self.docs_tree.item(selection[0], 'text'))
    
    try:
        documento = self.npi_manager.get_progetto_documento(doc_id)
        
        # Chiedi dove salvare
        save_path = filedialog.asksaveasfilename(
            defaultextension=os.path.splitext(documento.NomeFile)[1],
            initialfile=documento.NomeFile,
            filetypes=[('Tutti i file', '*.*')]
        )
        
        if save_path:
            with open(save_path, 'wb') as f:
                f.write(documento.Contenuto)
            
            messagebox.showinfo('Successo', 'Documento salvato con successo')
            
    except Exception as e:
        logger.error(f"Errore download documento: {e}")
        messagebox.showerror('Errore', f'Impossibile scaricare il documento:\n{e}')

def _delete_document(self):
    """Elimina il documento selezionato."""
    selection = self.docs_tree.selection()
    if not selection:
        messagebox.showwarning('Attenzione', 'Seleziona un documento')
        return
    
    if not messagebox.askyesno('Conferma', 'Sei sicuro di voler eliminare questo documento?'):
        return
    
    doc_id = int(self.docs_tree.item(selection[0], 'text'))
    
    try:
        self.npi_manager.delete_progetto_documento(doc_id)
        messagebox.showinfo('Successo', 'Documento eliminato con successo')
        self._load_project_documents()
        
    except Exception as e:
        logger.error(f"Errore eliminazione documento: {e}")
        messagebox.showerror('Errore', f'Impossibile eliminare il documento:\n{e}')

def _load_project_documents(self):
    """Carica la lista dei documenti del progetto."""
    for item in self.docs_tree.get_children():
        self.docs_tree.delete(item)
    
    if not self.progetto:
        return
    
    try:
        documenti = self.npi_manager.get_progetto_documenti(self.progetto.ProgettoId)
        
        for doc in documenti:
            size_kb = doc.Dimensione / 1024 if doc.Dimensione else 0
            size_str = f"{size_kb:.1f} KB"
            data_str = doc.DataCaricamento.strftime('%d/%m/%Y %H:%M') if doc.DataCaricamento else ""
            
            self.docs_tree.insert('', tk.END, text=doc.DocumentoID,
                                 values=(doc.NomeFile, doc.TipoFile or 'N/A', 
                                        size_str, doc.CaricatoDa or 'N/A', data_str))
    except Exception as e:
        logger.error(f"Errore caricamento documenti: {e}")

def _get_mime_type(self, filename):
    """Determina il MIME type dal nome file."""
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    return mime_types.get(ext, 'application/octet-stream')
```

### 4. Metodi Manager (`npi_manager.py`)

```python
def add_progetto_documento(self, progetto_id, nome_file, tipo_file, dimensione, 
                           contenuto, descrizione=None, caricato_da=None):
    """Aggiunge un documento al progetto."""
    session = self._get_session()
    try:
        documento = ProgettoDocumento(
            ProgettoID=progetto_id,
            NomeFile=nome_file,
            TipoFile=tipo_file,
            Dimensione=dimensione,
            Contenuto=contenuto,
            Descrizione=descrizione,
            CaricatoDa=caricato_da,
            DataCaricamento=datetime.utcnow()
        )
        session.add(documento)
        session.commit()
        logger.info(f"Documento {nome_file} aggiunto al progetto {progetto_id}")
        return True
    except Exception as e:
        logger.error(f"Errore aggiunta documento: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def get_progetto_documenti(self, progetto_id):
    """Recupera tutti i documenti di un progetto."""
    session = self._get_session()
    try:
        documenti = session.scalars(
            select(ProgettoDocumento)
            .where(ProgettoDocumento.ProgettoID == progetto_id)
            .order_by(ProgettoDocumento.DataCaricamento.desc())
        ).all()
        return [self._detach_object(session, d) for d in documenti]
    finally:
        session.close()

def get_progetto_documento(self, documento_id):
    """Recupera un singolo documento."""
    session = self._get_session()
    try:
        documento = session.get(ProgettoDocumento, documento_id)
        return self._detach_object(session, documento) if documento else None
    finally:
        session.close()

def delete_progetto_documento(self, documento_id):
    """Elimina un documento."""
    session = self._get_session()
    try:
        documento = session.get(ProgettoDocumento, documento_id)
        if documento:
            session.delete(documento)
            session.commit()
            logger.info(f"Documento {documento_id} eliminato")
            return True
        return False
    except Exception as e:
        logger.error(f"Errore eliminazione documento: {e}")
        session.rollback()
        raise
    finally:
        session.close()
```

### 5. Controllo Permessi Owner

```python
def _check_owner_permission(self):
    """Verifica se l'utente corrente è l'owner del progetto."""
    if not self.progetto or not self.progetto.owner:
        return False
    
    # Confronta l'utente loggato con l'owner del progetto
    return self.logged_in_user == self.progetto.owner.Nome

def _enable_header_editing(self):
    """Abilita la modifica dei dati di intestazione solo per l'owner."""
    is_owner = self._check_owner_permission()
    
    # Abilita/disabilita campi
    state = tk.NORMAL if is_owner else tk.DISABLED
    
    self.project_start_date_entry.config(state=state)
    self.project_due_date_entry.config(state=state)
    self.project_version_entry.config(state=state)
    self.project_owner_combo.config(state='readonly' if is_owner else tk.DISABLED)
    self.project_description_text.config(state=state)
    
    # Mostra/nascondi bottone salva
    if is_owner:
        self.save_header_button.pack(side=tk.LEFT, padx=5)
    else:
        self.save_header_button.pack_forget()
```

---

## 📝 Workflow

### Creazione Progetto con Documenti

```
1. Configurazione NPI → Tab Prodotti
   ↓
2. Seleziona prodotto
   ↓
3. Compila: Versione, Owner, Descrizione
   ↓
4. Click "Crea Progetto NPI"
   ↓
5. Progetto creato
   ↓
6. Apri progetto → Sezione "Documenti Progetto"
   ↓
7. Click "Aggiungi Documento"
   ↓
8. Seleziona file (immagine/PDF/etc)
   ↓
9. Inserisci descrizione (opzionale)
   ↓
10. Documento salvato nel database ✅
```

### Modifica Intestazione (Solo Owner)

```
1. Apri progetto NPI
   ↓
2. Sistema verifica: Utente = Owner?
   ├─ [Sì] → Campi editabili + Bottone "Salva"
   └─ [No] → Campi read-only
   ↓
3. Owner modifica: Date, Versione, Descrizione
   ↓
4. Click "Salva Date Progetto"
   ↓
5. Modifiche salvate ✅
```

---

## ✅ Checklist Implementazione

### Database
- [ ] Creare tabella `ProgettoDocumenti`
- [ ] Verificare FK e indici

### Codice
- [ ] Aggiungere model `ProgettoDocumento`
- [ ] Aggiornare relationship in `ProgettoNPI`
- [ ] Implementare UI sezione documenti
- [ ] Implementare metodi manager
- [ ] Implementare controllo permessi owner

### Test
- [ ] Test caricamento documento
- [ ] Test visualizzazione documento
- [ ] Test download documento
- [ ] Test eliminazione documento
- [ ] Test permessi owner vs non-owner

---

**Data**: 23 Dicembre 2024  
**Versione**: 2.2.8.1  
**Stato**: 📋 Specifica Completa - Pronto per Implementazione
