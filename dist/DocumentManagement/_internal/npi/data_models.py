# File: npi/data_models.py (VERSIONE CORRETTA)
from sqlalchemy import LargeBinary
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, NVARCHAR, Date, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

Base = declarative_base()


# ========================================
# 1. Soggetto (VIEW cross-database)
# Nota: La mappatura a una VIEW è considerata read-only da SQLAlchemy
# ========================================
class Soggetto(Base):
    __tablename__ = 'vw_Soggetti'
    __table_args__ = {'schema': 'dbo'}  # Schema specificato qui

    # Colonna primaria per la mappatura ORM
    SoggettoId = Column('SoggettoId', Integer, primary_key=True)
    Nome = Column('NomeSoggetto', String)
    Email = Column('Email', String)
    Tipo = Column('Tipo', String)
    TeamsAddress = Column('MSTeamsUserID', String)
    # Nota: External è scritto via raw SQL su dbo.Soggetti (non esposto da vw_Soggetti)

    def EmployeeId(self):
        return self.SoggettoId
    def MSTeamsUserID(self):
        return self.TeamsAddress

    def __repr__(self):
        return f"<Soggetto(SoggettoId={self.SoggettoId}, Nome='{self.Nome}')>"



# ========================================
# 2. Categories (Categorie Task)
# ========================================
class Categoria(Base):
    __tablename__ = 'Categories'
    __table_args__ = {'schema': 'dbo'}

    CategoryId = Column(Integer, primary_key=True, autoincrement=True)
    Category = Column(String(255))
    NrOrdin = Column(Integer)
    DefaultCategory = Column(Boolean, default=False)

    # Relazione ai task del catalogo
    tasks_catalogo = relationship("TaskCatalogo", back_populates="categoria")


# ========================================
# 3. Prodotti
# ========================================
class Prodotto(Base):
    __tablename__ = 'Prodotti'
    __table_args__ = {'schema': 'dbo'}

    ProdottoID = Column(Integer, primary_key=True, autoincrement=True)
    NomeProdotto = Column(String(255), nullable=False)
    CodiceProdotto = Column(String(100))
    Cliente = Column(String(255))
    DataScadenzaProgetto = Column(DateTime)
    SimilarAsProductId = Column(Integer, nullable=True)
    IDFinalClient = Column(Integer, nullable=True)
    DateOut = Column(DateTime, nullable=True)   # soft-delete: valorizzato = prodotto eliminato

    # La relazione punta al NOME DELLA CLASSE, non alla tabella del DB
    progetti_npi = relationship("ProgettoNPI", back_populates="prodotto")

    # La relazione a TaskProdotto è mantenuta per coerenza
    task_prodotto = relationship("TaskProdotto", back_populates="prodotto")


# ========================================
# 4. ProgettiNPI
# ========================================
class ProgettoNPI(Base):
    __tablename__ = 'ProgettiNPI'
    __table_args__ = {'schema': 'dbo'}

    ProgettoId = Column('ProgettoID', Integer, primary_key=True, autoincrement=True)
    ProdottoID = Column(Integer, ForeignKey('dbo.Prodotti.ProdottoID'))
    StatoProgetto = Column(String(50))
    DataInizio = Column(DateTime)
    NomeProgetto = Column(String(255))
    ScadenzaProgetto = Column(DateTime, nullable=True)
    Version = Column(String(50), nullable=True)  # Campo versione prodotto
    OwnerID = Column(Integer, ForeignKey('dbo.vw_Soggetti.SoggettoId'), nullable=True)  # Owner del progetto
    Descrizione = Column(Text, nullable=True)  # Descrizione del progetto
    DateOut = Column(DateTime, nullable=True)  # 🆕 Soft-delete: valorizzato = progetto cancellato
    OnHold = Column(Boolean, default=False, nullable=True)  # Progetto sospeso: escluso dalle email di warning
    
    # 🆕 CAMPI PER GERARCHIA PROGETTI (Parent-Child)
    ParentProjectID = Column('ParentProjectID', Integer, ForeignKey('dbo.ProgettiNPI.ProgettoID'), nullable=True)
    HierarchyLevel = Column(Integer, default=0, nullable=True)
    ProjectType = Column(String(50), default='Standard', nullable=True)  # 'Standard', 'Parent', 'Child'

    # Relationships esistenti
    prodotto = relationship("Prodotto", back_populates="progetti_npi")
    waves = relationship("WaveNPI", back_populates="progetto", cascade="all, delete-orphan")
    budgets = relationship("NpiBudget", back_populates="progetto", cascade="all, delete-orphan")
    documenti = relationship("ProgettoDocumento", back_populates="progetto", cascade="all, delete-orphan")
    owner = relationship(
        "Soggetto",
        primaryjoin="foreign(ProgettoNPI.OwnerID) == Soggetto.SoggettoId",
        viewonly=True,
        uselist=False
    )
    
    # 🆕 RELAZIONI PER GERARCHIA PROGETTI
    # Relazione verso il progetto padre (un solo padre)
    parent_project = relationship(
        "ProgettoNPI",
        remote_side=[ProgettoId],  # Indica che la FK è sul lato "child"
        backref="child_projects",   # Crea automaticamente la lista dei figli sul padre
        foreign_keys=[ParentProjectID],
        post_update=True  # Evita problemi con cicli di dipendenze
    )

    def __repr__(self):
        return f"<ProgettoNPI(ProgettoID={self.ProgettoId}, NomeProgetto='{self.NomeProgetto}')>"


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
    
    def __repr__(self):
        return f"<ProgettoDocumento(DocumentoID={self.DocumentoID}, NomeFile='{self.NomeFile}')>"



# ========================================
# 5. WaveNPI
# ========================================
class WaveNPI(Base):
    __tablename__ = 'WaveNPI'
    __table_args__ = {'schema': 'dbo'}

    WaveID = Column(Integer, primary_key=True, autoincrement=True)
    ProgettoID = Column(Integer, ForeignKey('dbo.ProgettiNPI.ProgettoID'), nullable=False)
    WaveIdentifier = Column(Float, nullable=False)

    # Relationships
    progetto = relationship("ProgettoNPI", back_populates="waves")
    tasks = relationship("TaskProdotto", back_populates="wave")

    def __repr__(self):
        return f"<WaveNPI(WaveID={self.WaveID}, ProgettoID={self.ProgettoID})>"


# ========================================
# 6. TaskCatalogo
# ========================================
class TaskCatalogo(Base):
    __tablename__ = 'TaskCatalogo'
    __table_args__ = {'schema': 'dbo'}

    TaskID = Column('TaskID', Integer, primary_key=True, autoincrement=True)
    ItemID = Column(String(50))  # Cambiato a String per coerenza con vecchie versioni
    NomeTask = Column(String(255), nullable=False)
    Descrizione = Column(Text)
    CategoryId = Column(Integer, ForeignKey('dbo.Categories.CategoryId'))
    NrOrdin = Column('NrOrdin', Integer)  # Corretto nome in minuscolo
    IsTitle = Column(Boolean, default=False)
    DefaultTask = Column(Boolean, default=False)
    # IsFinalMilestone removed as requested

    # Relationship
    # Anche qui, si usa il nome della classe
    categoria = relationship("Categoria", back_populates="tasks_catalogo")
# ========================================
# 7. TaskProdotto
# ========================================
class TaskProdotto(Base):
    __tablename__ = 'TaskProdotto'
    __table_args__ = {'schema': 'dbo'}

    TaskProdottoID = Column(Integer, primary_key=True, autoincrement=True)
    WaveID = Column(Integer, ForeignKey('dbo.WaveNPI.WaveID'))
    TaskID = Column(Integer, ForeignKey('dbo.TaskCatalogo.TaskID'))
    ProdottoId = Column(Integer, ForeignKey('dbo.Prodotti.ProdottoID'))
    OwnerID = Column(Integer)  # ForeignKey non è usata per la VIEW cross-database
    Stato = Column(String(50))
    DataInizio = Column(DateTime)
    DataScadenza = Column(DateTime)
    DataCompletamento = Column(DateTime)
    Costo = Column(Float)
    Note = Column(Text)  # Cambiato a Text per uniformità
    PercentualeCompletamento = Column(Integer, default=0)
    IsPostFinalMilestone = Column(Boolean, default=False)


    # Relationships ai modelli dello stesso DB
    wave = relationship("WaveNPI", back_populates="tasks")
    task_catalogo = relationship("TaskCatalogo")
    prodotto = relationship("Prodotto", back_populates="task_prodotto")
    notification_logs = relationship("NotificationLog", back_populates="task_prodotto")
    documents = relationship("NpiDocument", back_populates="task_prodotto", cascade="all, delete-orphan")
    dependencies = relationship("TaskDependency", foreign_keys="TaskDependency.TaskProdottoID", back_populates="task", cascade="all, delete-orphan")
    
    # Relationships per predecessori e successori
    predecessors = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.TaskProdottoID",
        back_populates="task",
        overlaps="dependencies"
    )
    successors = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.DependsOnTaskProdottoID",
        overlaps="depends_on_task"
    )

    # Relationship con Soggetto (VIEW)
    owner = relationship(
        "Soggetto",
        primaryjoin="foreign(TaskProdotto.OwnerID) == Soggetto.SoggettoId",
        viewonly=True,
        uselist=False
    )


# ========================================
# 8. NotificationLog
# ========================================
class NotificationLog(Base):
    __tablename__ = 'NotificationLog'
    __table_args__ = {'schema': 'dbo'}

    NotificationLogId = Column(Integer, primary_key=True, autoincrement=True)
    TaskProdottoId = Column(Integer, ForeignKey('dbo.TaskProdotto.TaskProdottoID'))
    EmployeeHireHistoryId = Column(Integer)
    NotificationType = Column(String(50))
    NotificationReason = Column(String(255))
    RecipientEmail = Column(String(255))
    RecipientName = Column(String(255))
    RecipientTeamsId = Column(String(255))
    Subject = Column(String(500))
    MessageBody = Column(Text)
    SentDate = Column(DateTime)
    DeliveryStatus = Column(String(50))
    ErrorMessage = Column(Text)
    RetryCount = Column(Integer, default=0)
    LastRetryDate = Column(DateTime)
    CreatedBy = Column(String(255))
    CreatedDate = Column(DateTime, default=datetime.utcnow)

    # Relationships
    task_prodotto = relationship("TaskProdotto", back_populates="notification_logs")

    def __repr__(self):
        return f"<NotificationLog(Id={self.NotificationLogId}, TaskId={self.TaskProdottoId})>"


# ========================================
# 9. NpiDocumentType
# ========================================
class NpiDocumentType(Base):
    __tablename__ = 'NpiDocumentTypes'
    __table_args__ = {'schema': 'dbo'}

    NpiDocumentTypeId = Column(Integer, primary_key=True, autoincrement=True)
    NpiDocumentDescription = Column(String(255), nullable=False)
    HasValue = Column(Boolean, default=False)
    CheckDate = Column(Boolean, default=False)
    documents = relationship("NpiDocument", back_populates="document_type")



# ========================================
# 10. NpiDocument
# ========================================
class NpiDocument(Base):
    __tablename__ = 'NpiDocuments'
    __table_args__ = {'schema': 'dbo'}

    NpiDocumentId = Column(Integer, primary_key=True, autoincrement=True)
    TaskProdottoId = Column(Integer, ForeignKey('dbo.TaskProdotto.TaskProdottoID'))
    NpiDocumentTypeId = Column(Integer, ForeignKey('dbo.NpiDocumentTypes.NpiDocumentTypeId'))
    DocumentTitle = Column(String(255), nullable=False)
    DocumentBody = Column(LargeBinary)  # Per VARBINARY(MAX)
    DateIn = Column(DateTime, default=datetime.utcnow)
    User = Column(String(255))
    NewVersionOf = Column(Integer, nullable=True)
    ValueInEur = Column(Float, nullable=True)
    DateOut = Column(DateTime, nullable=True)
    VersionNumber = Column(Integer, default=0)
    Note = Column(Text, nullable=True)
    AutorizedBy = Column(String(255), nullable=True)
    AuthorizedOn = Column(DateTime, nullable=True)
    IDSite = Column('IDSite',Integer, nullable=True)
    BudgetItemId = Column(Integer, ForeignKey('dbo.NpiBudgetItems.BudgetItemId'), nullable=True)

    # Relazioni
    task_prodotto = relationship("TaskProdotto", back_populates="documents")
    document_type = relationship("NpiDocumentType", back_populates="documents")
    budget_item = relationship("NpiBudgetItem", back_populates="documents")


# ========================================
# 11. TaskDependency
# ========================================
class TaskDependency(Base):
    __tablename__ = 'TaskDependencies'
    __table_args__ = {'schema': 'dbo'}
    
    DependencyID = Column(Integer, primary_key=True, autoincrement=True)
    TaskProdottoID = Column(Integer, ForeignKey('dbo.TaskProdotto.TaskProdottoID'), nullable=False)
    DependsOnTaskProdottoID = Column(Integer, ForeignKey('dbo.TaskProdotto.TaskProdottoID'), nullable=False)
    DependencyType = Column(String(20), default='FinishToStart')
    LagDays = Column(Integer, default=0)
    
    # Relationships
    task = relationship("TaskProdotto", foreign_keys=[TaskProdottoID], back_populates="dependencies")
    depends_on_task = relationship("TaskProdotto", foreign_keys=[DependsOnTaskProdottoID])
    
    def __repr__(self):
        return f"<TaskDependency(ID={self.DependencyID}, Task={self.TaskProdottoID} depends on {self.DependsOnTaskProdottoID})>"



# ========================================
# 12. FamilyNpi
# ========================================
class FamilyNpi(Base):
    __tablename__ = 'FamilyNpis'
    __table_args__ = {'schema': 'dbo'}
    
    FamilyNpiID = Column(Integer, primary_key=True, autoincrement=True)
    NpiFamily = Column(String(255), nullable=False)
    DateEnd = Column(DateTime, nullable=True)
    # Checklist configuration
    ChecklistSection = Column(String(100), nullable=True)
    CL_HasPrograms = Column(Boolean, nullable=False, default=False)
    CL_HasMaterials = Column(Boolean, nullable=False, default=False)
    CL_HasProductionData = Column(Boolean, nullable=False, default=False)
    CL_HasVerification = Column(Boolean, nullable=False, default=False)
    CL_HasPreformingChecks = Column(Boolean, nullable=False, default=False)
    CL_HasCoating = Column(Boolean, nullable=False, default=False)
    CL_SortOrder = Column(Integer, nullable=False, default=0)
    
    # Relationship to logs (family-task links)
    logs = relationship("FamilyNpiLog", back_populates="family", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<FamilyNpi(FamilyNpiID={self.FamilyNpiID}, NpiFamily='{self.NpiFamily}')>"


# ========================================
# 13. FamilyNpiLog (serves as both link table and audit log)
# ========================================
class FamilyNpiLog(Base):
    __tablename__ = 'FamilyNpiLogs'
    __table_args__ = {'schema': 'dbo'}
    
    FamilyNpiLogID = Column(Integer, primary_key=True, autoincrement=True)
    FamilyNpiID = Column(Integer, ForeignKey('dbo.FamilyNpis.FamilyNpiID'), nullable=False)
    TaskID = Column(Integer, ForeignKey('dbo.TaskCatalogo.TaskID'), nullable=False)
    DateEnd = Column(DateTime, nullable=True)
    
    # Relationships
    family = relationship("FamilyNpi", back_populates="logs")
    task = relationship("TaskCatalogo")
    
    def __repr__(self):
        return f"<FamilyNpiLog(FamilyNpiLogID={self.FamilyNpiLogID}, FamilyNpiID={self.FamilyNpiID}, TaskID={self.TaskID})>"


# ========================================
# 14. NpiBudgetCategory (Categorie budget configurabili)
# ========================================
class NpiBudgetCategory(Base):
    __tablename__ = 'NpiBudgetCategories'
    __table_args__ = {'schema': 'dbo'}

    CategoryId = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(255), nullable=False)
    DateOut = Column(DateTime, nullable=True)

    items = relationship("NpiBudgetItem", back_populates="category")

    def __repr__(self):
        return f"<NpiBudgetCategory(CategoryId={self.CategoryId}, CategoryName='{self.CategoryName}')>"


# ========================================
# 15. NpiBudget (Budget per progetto NPI)
# ========================================
class NpiBudget(Base):
    __tablename__ = 'NpiBudgets'
    __table_args__ = {'schema': 'dbo'}

    BudgetId = Column(Integer, primary_key=True, autoincrement=True)
    ProgettoID = Column(Integer, ForeignKey('dbo.ProgettiNPI.ProgettoID'), nullable=False)
    BudgetName = Column(String(255), nullable=False)
    BudgetStatus = Column(String(50), nullable=False, default='Bozza')
    ApprovalStatus = Column(String(50), nullable=False, default='DaApprovare')
    IsActive = Column(Boolean, default=False)
    CreatedBy = Column(String(255))
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    ApprovedBy = Column(String(255), nullable=True)
    ApprovedDate = Column(DateTime, nullable=True)
    RejectionNote = Column(Text, nullable=True)
    DateOut = Column(DateTime, nullable=True)

    # Relationships
    progetto = relationship("ProgettoNPI", back_populates="budgets")
    items = relationship("NpiBudgetItem", back_populates="budget", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<NpiBudget(BudgetId={self.BudgetId}, BudgetName='{self.BudgetName}')>"


# ========================================
# 16. NpiBudgetItem (Righe budget)
# ========================================
class NpiBudgetItem(Base):
    __tablename__ = 'NpiBudgetItems'
    __table_args__ = {'schema': 'dbo'}

    BudgetItemId = Column(Integer, primary_key=True, autoincrement=True)
    BudgetId = Column(Integer, ForeignKey('dbo.NpiBudgets.BudgetId'), nullable=False)
    ItemDescription = Column(String(500), nullable=False)
    CategoryId = Column(Integer, ForeignKey('dbo.NpiBudgetCategories.CategoryId'), nullable=True)
    Quantity = Column(DECIMAL(18, 2), nullable=False, default=1)
    UnitPrice = Column(DECIMAL(18, 2), nullable=False, default=0)
    # TotalPrice is a computed column in SQL (Quantity * UnitPrice)
    ItemStatus = Column(String(50), nullable=False, default='InLavorazione')
    ItemApproval = Column(String(50), nullable=False, default='DaApprovare')
    ApprovedBy = Column(String(255), nullable=True)
    ApprovedDate = Column(DateTime, nullable=True)
    RejectionNote = Column(Text, nullable=True)
    Note = Column(Text, nullable=True)
    DateOut = Column(DateTime, nullable=True)

    # Relationships
    budget = relationship("NpiBudget", back_populates="items")
    category = relationship("NpiBudgetCategory", back_populates="items")
    documents = relationship("NpiDocument", back_populates="budget_item")

    @property
    def TotalPrice(self):
        """Computed property for total price (mirrors SQL computed column)."""
        return float(self.Quantity or 0) * float(self.UnitPrice or 0)

    def __repr__(self):
        return f"<NpiBudgetItem(BudgetItemId={self.BudgetItemId}, Desc='{self.ItemDescription}')>"


# ========================================
# 17. NpiChecklistSession
# ========================================
class NpiChecklistSession(Base):
    __tablename__ = 'NpiChecklistSessions'
    __table_args__ = {'schema': 'dbo'}

    SessionId = Column(Integer, primary_key=True, autoincrement=True)
    ProgettoID = Column(Integer, nullable=False)
    OrderId = Column(Integer, nullable=True)
    ProductCode = Column(String(100), nullable=True)
    OrderQuantity = Column(Integer, nullable=True)
    CheckDate = Column(DateTime, nullable=True)
    Status = Column(String(50), nullable=False, default='InLavorazione')
    HasSMT_TOP = Column(Boolean, nullable=False, default=True)
    HasSMT_BOTTOM = Column(Boolean, nullable=False, default=False)
    HasPTH = Column(Boolean, nullable=False, default=True)
    HasICT = Column(Boolean, nullable=False, default=True)
    HasFCT = Column(Boolean, nullable=False, default=True)
    HasCoating = Column(Boolean, nullable=False, default=False)
    FinalApproval = Column(Boolean, nullable=True)
    ResponsabileQualita = Column(String(255), nullable=True)
    ResponsabileProduzione = Column(String(255), nullable=True)
    ResponsabileIngegneria = Column(String(255), nullable=True)
    ApprovedBy = Column(String(255), nullable=True)
    ApprovedDate = Column(DateTime, nullable=True)
    CreatedBy = Column(String(255), nullable=True)
    CreatedDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    LastModifiedBy = Column(String(255), nullable=True)
    LastModifiedDate = Column(DateTime, nullable=True)
    DateOut = Column(DateTime, nullable=True)

    # Relationships
    programs = relationship("NpiChecklistProgram", back_populates="session", cascade="all, delete-orphan")
    materials = relationship("NpiChecklistMaterial", back_populates="session", cascade="all, delete-orphan")
    production_data = relationship("NpiChecklistProductionData", back_populates="session", cascade="all, delete-orphan")
    verifications = relationship("NpiChecklistVerification", back_populates="session", cascade="all, delete-orphan")
    preforming_checks = relationship("NpiChecklistPreformingCheck", back_populates="session", cascade="all, delete-orphan")
    actions = relationship("NpiChecklistAction", back_populates="session", cascade="all, delete-orphan")
    rework_items = relationship("NpiChecklistRework", back_populates="session", cascade="all, delete-orphan")


# ========================================
# 18. NpiChecklistProgram
# ========================================
class NpiChecklistProgram(Base):
    __tablename__ = 'NpiChecklistPrograms'
    __table_args__ = {'schema': 'dbo'}

    ProgramId = Column(Integer, primary_key=True, autoincrement=True)
    SessionId = Column(Integer, ForeignKey('dbo.NpiChecklistSessions.SessionId'), nullable=False)
    ProcessSection = Column(String(50), nullable=False)
    ProcessStep = Column(String(50), nullable=False)
    LineNr = Column(String(50), nullable=True)
    ProgramName = Column(String(255), nullable=True)
    Result = Column(String(20), nullable=True)
    ResponsabileName = Column(String(255), nullable=True)
    ProcessDate = Column(DateTime, nullable=True)
    Note = Column(Text, nullable=True)
    ProgramFile = Column(LargeBinary, nullable=True)
    ProgramFileName = Column(String(255), nullable=True)

    session = relationship("NpiChecklistSession", back_populates="programs")


# ========================================
# 19. NpiChecklistMaterial
# ========================================
class NpiChecklistMaterial(Base):
    __tablename__ = 'NpiChecklistMaterials'
    __table_args__ = {'schema': 'dbo'}

    MaterialId = Column(Integer, primary_key=True, autoincrement=True)
    SessionId = Column(Integer, ForeignKey('dbo.NpiChecklistSessions.SessionId'), nullable=False)
    ProcessSection = Column(String(50), nullable=False)
    MaterialType = Column(String(100), nullable=False)
    CodePN = Column(String(255), nullable=True)
    Note = Column(Text, nullable=True)

    session = relationship("NpiChecklistSession", back_populates="materials")


# ========================================
# 20. NpiChecklistProductionData
# ========================================
class NpiChecklistProductionData(Base):
    __tablename__ = 'NpiChecklistProductionData'
    __table_args__ = {'schema': 'dbo'}

    ProductionDataId = Column(Integer, primary_key=True, autoincrement=True)
    SessionId = Column(Integer, ForeignKey('dbo.NpiChecklistSessions.SessionId'), nullable=False)
    ProcessName = Column(String(100), nullable=False)
    ProcessDate = Column(DateTime, nullable=True)
    ProducedQty = Column(Integer, nullable=True)
    InspectedQty = Column(Integer, nullable=True)
    PassQty = Column(Integer, nullable=True)
    FailQty = Column(Integer, nullable=True)
    Note = Column(Text, nullable=True)
    IsAutoPopulated = Column(Boolean, nullable=False, default=False)

    session = relationship("NpiChecklistSession", back_populates="production_data")


# ========================================
# 21. NpiChecklistVerification
# ========================================
class NpiChecklistVerification(Base):
    __tablename__ = 'NpiChecklistVerifications'
    __table_args__ = {'schema': 'dbo'}

    VerificationId = Column(Integer, primary_key=True, autoincrement=True)
    SessionId = Column(Integer, ForeignKey('dbo.NpiChecklistSessions.SessionId'), nullable=False)
    SectionName = Column(String(100), nullable=False)
    ConformStatus = Column(String(20), nullable=True)
    InspectedQty = Column(Integer, nullable=True)
    InspectionResult = Column(String(20), nullable=True)
    CQResponsible = Column(String(255), nullable=True)
    VerificationDate = Column(DateTime, nullable=True)
    Note = Column(Text, nullable=True)

    session = relationship("NpiChecklistSession", back_populates="verifications")


# ========================================
# 22. NpiChecklistPreformingCheck
# ========================================
class NpiChecklistPreformingCheck(Base):
    __tablename__ = 'NpiChecklistPreformingChecks'
    __table_args__ = {'schema': 'dbo'}

    CheckId = Column(Integer, primary_key=True, autoincrement=True)
    SessionId = Column(Integer, ForeignKey('dbo.NpiChecklistSessions.SessionId'), nullable=False)
    CheckItem = Column(String(255), nullable=False)
    Result = Column(String(20), nullable=True)
    Note = Column(Text, nullable=True)

    session = relationship("NpiChecklistSession", back_populates="preforming_checks")


# ========================================
# 23. NpiChecklistAction
# ========================================
class NpiChecklistAction(Base):
    __tablename__ = 'NpiChecklistActions'
    __table_args__ = {'schema': 'dbo'}

    ActionId = Column(Integer, primary_key=True, autoincrement=True)
    SessionId = Column(Integer, ForeignKey('dbo.NpiChecklistSessions.SessionId'), nullable=False)
    Comment = Column(Text, nullable=True)
    Responsabil = Column(String(255), nullable=True)
    DataChiusura = Column(DateTime, nullable=True)
    Status = Column(String(50), nullable=True)

    session = relationship("NpiChecklistSession", back_populates="actions")


# ========================================
# 24. NpiChecklistRework
# ========================================
class NpiChecklistRework(Base):
    __tablename__ = 'NpiChecklistRework'
    __table_args__ = {'schema': 'dbo'}

    ReworkId = Column(Integer, primary_key=True, autoincrement=True)
    SessionId = Column(Integer, ForeignKey('dbo.NpiChecklistSessions.SessionId'), nullable=False)
    SerialNr = Column(String(100), nullable=True)
    FailICT = Column(Text, nullable=True)
    FailFCT = Column(Text, nullable=True)
    Diagnoza = Column(Text, nullable=True)
    Referinta = Column(String(255), nullable=True)
    ReworkResp = Column(String(255), nullable=True)

    session = relationship("NpiChecklistSession", back_populates="rework_items")

