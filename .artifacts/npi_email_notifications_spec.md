# Sistema di Notifiche Email Professionali per Assegnazione Task NPI

## 📋 Analisi del Problema

### Situazione Attuale
- ❌ Il sistema dice "notifica inviata" ma non invia realmente l'email
- ❌ Manca descrizione del progetto
- ❌ Manca owner del progetto
- ❌ Email non professionale/strutturata

### Soluzione Proposta
1. ✅ Aggiungere campi `Descrizione` e `OwnerID` alla tabella `ProgettiNPI`
2. ✅ Implementare invio email reale tramite sistema esistente
3. ✅ Email professionale in behalf del project owner
4. ✅ Include dettagli progetto, task assegnati, scadenze e dipendenze

---

## 🗄️ Modifiche Database

### Tabella: `ProgettiNPI`

**Campi da Aggiungere**:

```sql
-- Script per aggiungere i nuovi campi alla tabella ProgettiNPI

-- 1. Descrizione del progetto
ALTER TABLE dbo.ProgettiNPI
ADD Descrizione NVARCHAR(MAX) NULL;

-- 2. Owner del progetto (FK a Soggetto)
ALTER TABLE dbo.ProgettiNPI
ADD OwnerID INT NULL;

-- 3. Foreign Key constraint (opzionale ma consigliato)
ALTER TABLE dbo.ProgettiNPI
ADD CONSTRAINT FK_ProgettiNPI_Owner 
FOREIGN KEY (OwnerID) REFERENCES dbo.vw_Soggetti(SoggettoId);

-- Commenti descrittivi
EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Descrizione dettagliata del progetto NPI', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettiNPI',
    @level2type = N'COLUMN', @level2name = 'Descrizione';

EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'ID del responsabile/owner del progetto (FK a vw_Soggetti)', 
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'ProgettiNPI',
    @level2type = N'COLUMN', @level2name = 'OwnerID';
```

### Perché `ProgettiNPI`?

✅ **Vantaggi**:
- Ogni progetto ha UN solo owner e UNA sola descrizione
- Dati centralizzati e facili da gestire
- Non serve tabella aggiuntiva
- Relazione diretta con `Soggetto` (owner)

❌ **Alternative Scartate**:
- Tabella separata `ProgettoDetails`: Overhead inutile
- Nella tabella `WaveNPI`: Ogni wave avrebbe owner diverso (confusione)
- Nella tabella `Prodotti`: Un prodotto può avere più progetti NPI

---

## 📧 Template Email Professionale

### Struttura Email

```
From: [Owner Name] <owner@company.com>
To: [Assignee Email]
Subject: [Project Name] - Task Assignment Notification

Dear [Assignee Name],

You have been assigned to the following task(s) for the NPI project:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project Name:    [Product Name]
Project Code:    [Product Code]
Project Owner:   [Owner Name]
Start Date:      [Project Start Date]
Target Date:     [Project Due Date]
Version:         [Project Version]

Description:
[Project Description - multiline]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR ASSIGNED TASKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task 1: [ItemID] - [Task Name]
Category:     [Category Name]
Description:  [Task Description]
Due Date:     [Task Due Date]
Status:       [Task Status]

Dependencies:
  ⚠ This task depends on:
    • [Predecessor Task 1] - Assigned to [Owner] - Due: [Date]
    • [Predecessor Task 2] - Assigned to [Owner] - Due: [Date]
  
  ℹ Other tasks depend on this:
    • [Successor Task 1] - Assigned to [Owner] - Due: [Date]

---

Task 2: [ItemID] - [Task Name]
[... same structure ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANT NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Please review the task dependencies carefully
• Coordinate with team members for dependent tasks
• Update task status regularly in the system
• Contact the project owner for any questions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Best regards,
[Owner Name]
[Owner Title/Role]

---
This is an automated notification from the NPI Management System.
Please do not reply to this email.
```

---

## 🔧 Implementazione Codice

### 1. Aggiornare Model `ProgettoNPI`

```python
# File: npi/data_models.py

class ProgettoNPI(Base):
    __tablename__ = 'ProgettiNPI'
    __table_args__ = {'schema': 'dbo'}
    
    ProgettoId = Column('ProgettoID', Integer, primary_key=True, autoincrement=True)
    ProdottoID = Column(Integer, ForeignKey('dbo.Prodotti.ProdottoID'))
    DataInizioProgetto = Column(DateTime)
    DataScadenzaProgetto = Column(DateTime)
    Version = Column(String(50), nullable=True)
    
    # ✅ NUOVI CAMPI
    Descrizione = Column(Text, nullable=True)
    OwnerID = Column(Integer, ForeignKey('dbo.vw_Soggetti.SoggettoId'), nullable=True)
    
    # Relationships
    prodotto = relationship("Prodotto", back_populates="progetti_npi")
    waves = relationship("WaveNPI", back_populates="progetto", cascade="all, delete-orphan")
    
    # ✅ NUOVA RELATIONSHIP per Owner
    owner = relationship(
        "Soggetto",
        primaryjoin="foreign(ProgettoNPI.OwnerID) == Soggetto.SoggettoId",
        viewonly=True,
        uselist=False
    )
```

### 2. Aggiungere Campi nella UI

```python
# File: npi/windows/project_window.py

# Nella sezione header, aggiungere:

# Owner del progetto
ttk.Label(dates_frame, text=self.lang.get('project_owner', 'Owner:')).pack(side=tk.LEFT, padx=5)
self.project_owner_combo = ttk.Combobox(dates_frame, state='readonly', width=20)
self.project_owner_combo.pack(side=tk.LEFT, padx=5)

# Descrizione del progetto (in un frame separato sotto l'header)
desc_frame = ttk.LabelFrame(main_frame, text=self.lang.get('project_description', 'Descrizione Progetto'))
desc_frame.pack(fill=tk.X, pady=(0, 10))

self.project_description_text = tk.Text(desc_frame, height=4, wrap=tk.WORD)
self.project_description_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Aggiornare il bottone salva per includere questi campi
```

### 3. Metodo per Inviare Email

```python
# File: npi/npi_manager.py

def send_task_assignment_notification(self, task_prodotto_id, assignee_id):
    """
    Invia email professionale di notifica assegnazione task.
    
    Args:
        task_prodotto_id: ID del task assegnato
        assignee_id: ID del soggetto assegnato
    """
    session = self._get_session()
    try:
        # Carica task con tutte le relazioni
        task = session.scalars(
            select(TaskProdotto)
            .options(
                joinedload(TaskProdotto.task_catalogo).joinedload(TaskCatalogo.categoria),
                joinedload(TaskProdotto.wave).joinedload(WaveNPI.progetto).joinedload(ProgettoNPI.prodotto),
                joinedload(TaskProdotto.wave).joinedload(WaveNPI.progetto).joinedload(ProgettoNPI.owner),
                joinedload(TaskProdotto.owner),
                joinedload(TaskProdotto.predecessors),
                joinedload(TaskProdotto.successors)
            )
            .where(TaskProdotto.TaskProdottoID == task_prodotto_id)
        ).first()
        
        if not task or not task.owner:
            logger.warning(f"Task {task_prodotto_id} o assignee non trovato")
            return False
        
        # Ottieni project owner
        project = task.wave.progetto
        project_owner = project.owner if project.owner else None
        
        # Prepara dati per email
        email_data = {
            'assignee_name': task.owner.Nome,
            'assignee_email': task.owner.Email,
            'project_name': project.prodotto.NomeProdotto if project.prodotto else "N/A",
            'project_code': project.prodotto.CodiceProdotto if project.prodotto else "N/A",
            'project_owner_name': project_owner.Nome if project_owner else "N/A",
            'project_owner_email': project_owner.Email if project_owner else None,
            'project_description': project.Descrizione or "No description provided",
            'project_start': project.DataInizioProgetto.strftime('%d/%m/%Y') if project.DataInizioProgetto else "N/A",
            'project_due': project.DataScadenzaProgetto.strftime('%d/%m/%Y') if project.DataScadenzaProgetto else "N/A",
            'project_version': project.Version or "N/A",
            'task_item_id': task.task_catalogo.ItemID if task.task_catalogo else "N/A",
            'task_name': task.task_catalogo.NomeTask if task.task_catalogo else "N/A",
            'task_category': task.task_catalogo.categoria.Category if task.task_catalogo and task.task_catalogo.categoria else "N/A",
            'task_description': task.task_catalogo.Descrizione if task.task_catalogo else "N/A",
            'task_due_date': task.DataScadenza.strftime('%d/%m/%Y') if task.DataScadenza else "N/A",
            'task_status': task.Stato or "Not Started",
            'predecessors': self._format_dependencies(task.predecessors, session),
            'successors': self._format_dependencies(task.successors, session)
        }
        
        # Genera HTML email
        email_html = self._generate_task_assignment_email_html(email_data)
        
        # Invia email
        from email_connector import EmailSender
        email_sender = EmailSender()
        
        # Se c'è un project owner, invia in behalf
        from_email = project_owner.Email if project_owner and project_owner.Email else "noreply@company.com"
        from_name = project_owner.Nome if project_owner else "NPI System"
        
        success = email_sender.send_email(
            to_addresses=[task.owner.Email],
            subject=f"{email_data['project_name']} - Task Assignment Notification",
            body_html=email_html,
            from_address=from_email,
            from_name=from_name
        )
        
        # Log notifica
        notification = NotificationLog(
            TaskProdottoID=task_prodotto_id,
            RecipientEmail=task.owner.Email,
            RecipientName=task.owner.Nome,
            NotificationType='TaskAssignment',
            Status='Sent' if success else 'Failed',
            SentDate=datetime.utcnow() if success else None,
            ErrorMessage=None if success else "Email sending failed",
            CreatedBy='System',
            CreatedDate=datetime.utcnow()
        )
        session.add(notification)
        session.commit()
        
        return success
        
    except Exception as e:
        logger.error(f"Errore invio notifica task {task_prodotto_id}: {e}", exc_info=True)
        session.rollback()
        return False
    finally:
        session.close()

def _format_dependencies(self, dependencies, session):
    """Formatta le dipendenze per l'email."""
    if not dependencies:
        return []
    
    formatted = []
    for dep in dependencies:
        dep_task = session.get(TaskProdotto, dep.PredecessorTaskID or dep.SuccessorTaskID)
        if dep_task:
            formatted.append({
                'name': dep_task.task_catalogo.NomeTask if dep_task.task_catalogo else "N/A",
                'item_id': dep_task.task_catalogo.ItemID if dep_task.task_catalogo else "N/A",
                'owner': dep_task.owner.Nome if dep_task.owner else "Unassigned",
                'due_date': dep_task.DataScadenza.strftime('%d/%m/%Y') if dep_task.DataScadenza else "N/A"
            })
    return formatted

def _generate_task_assignment_email_html(self, data):
    """Genera HTML professionale per email assegnazione task."""
    
    # Formatta predecessori
    predecessors_html = ""
    if data['predecessors']:
        predecessors_html = "<h4>⚠ This task depends on:</h4><ul>"
        for pred in data['predecessors']:
            predecessors_html += f"<li><strong>{pred['item_id']}</strong> - {pred['name']} - Assigned to: {pred['owner']} - Due: {pred['due_date']}</li>"
        predecessors_html += "</ul>"
    
    # Formatta successori
    successors_html = ""
    if data['successors']:
        successors_html = "<h4>ℹ Other tasks depend on this:</h4><ul>"
        for succ in data['successors']:
            successors_html += f"<li><strong>{succ['item_id']}</strong> - {succ['name']} - Assigned to: {succ['owner']} - Due: {succ['due_date']}</li>"
        successors_html += "</ul>"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #0078d4; color: white; padding: 20px; border-radius: 5px 5px 0 0; }}
            .section {{ background: #f5f5f5; padding: 15px; margin: 15px 0; border-left: 4px solid #0078d4; }}
            .task-box {{ background: white; padding: 15px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }}
            .label {{ font-weight: bold; color: #0078d4; }}
            .footer {{ background: #f5f5f5; padding: 15px; margin-top: 20px; border-top: 2px solid #0078d4; font-size: 0.9em; color: #666; }}
            h2 {{ color: #0078d4; border-bottom: 2px solid #0078d4; padding-bottom: 10px; }}
            ul {{ margin: 10px 0; padding-left: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Task Assignment Notification</h1>
                <p>NPI Project Management System</p>
            </div>
            
            <p>Dear <strong>{data['assignee_name']}</strong>,</p>
            
            <p>You have been assigned to the following task for the NPI project:</p>
            
            <div class="section">
                <h2>📋 PROJECT DETAILS</h2>
                <p><span class="label">Project Name:</span> {data['project_name']}</p>
                <p><span class="label">Project Code:</span> {data['project_code']}</p>
                <p><span class="label">Project Owner:</span> {data['project_owner_name']}</p>
                <p><span class="label">Start Date:</span> {data['project_start']}</p>
                <p><span class="label">Target Date:</span> {data['project_due']}</p>
                <p><span class="label">Version:</span> {data['project_version']}</p>
                <p><span class="label">Description:</span><br>{data['project_description']}</p>
            </div>
            
            <div class="section">
                <h2>✅ YOUR ASSIGNED TASK</h2>
                <div class="task-box">
                    <h3>{data['task_item_id']} - {data['task_name']}</h3>
                    <p><span class="label">Category:</span> {data['task_category']}</p>
                    <p><span class="label">Description:</span> {data['task_description']}</p>
                    <p><span class="label">Due Date:</span> {data['task_due_date']}</p>
                    <p><span class="label">Status:</span> {data['task_status']}</p>
                    
                    {predecessors_html}
                    {successors_html}
                </div>
            </div>
            
            <div class="section">
                <h2>⚠ IMPORTANT NOTES</h2>
                <ul>
                    <li>Please review the task dependencies carefully</li>
                    <li>Coordinate with team members for dependent tasks</li>
                    <li>Update task status regularly in the system</li>
                    <li>Contact the project owner for any questions</li>
                </ul>
            </div>
            
            <div class="footer">
                <p><strong>Best regards,</strong><br>
                {data['project_owner_name']}<br>
                Project Owner</p>
                <hr>
                <p style="font-size: 0.8em; color: #999;">
                    This is an automated notification from the NPI Management System.<br>
                    Please do not reply to this email.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html
```

---

## 📝 Chiavi di Traduzione

```sql
-- Traduzioni per UI progetto

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'project_owner')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'project_owner', 'Owner:');

IF NOT EXISTS (SELECT 1 FROM apptranslation WHERE languagecode = 'it' AND translationkey = 'project_description')
    INSERT INTO apptranslation (languagecode, translationkey, translationvalue) VALUES
    ('it', 'project_description', 'Descrizione Progetto');

-- Aggiungi per tutte le lingue (en, ro, de, sv)
```

---

## ✅ Checklist Implementazione

### Database
- [ ] Eseguire script ALTER TABLE per aggiungere `Descrizione` e `OwnerID`
- [ ] Verificare FK constraint funzionante
- [ ] Popolare owner per progetti esistenti (se necessario)

### Codice
- [ ] Aggiornare model `ProgettoNPI` in `data_models.py`
- [ ] Aggiungere campi UI in `project_window.py`
- [ ] Implementare metodi email in `npi_manager.py`
- [ ] Testare invio email con dati reali

### Testing
- [ ] Test assegnazione task con email
- [ ] Verifica email ricevuta correttamente
- [ ] Test con/senza dipendenze
- [ ] Test con/senza project owner
- [ ] Verifica log notifiche in database

---

**Data**: 23 Dicembre 2024  
**Versione**: 2.2.8.1  
**Stato**: 📋 Specifica Completa - Pronto per Implementazione
