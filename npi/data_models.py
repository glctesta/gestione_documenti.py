# File: npi/data_models.py (VERSIONE CORRETTA)
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

    # --- CORREZIONE QUI ---
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

    # Relationships
    prodotto = relationship("Prodotto", back_populates="progetti_npi")
    waves = relationship("WaveNPI", back_populates="progetto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProgettoNPI(ProgettoID={self.ProgettoId}, NomeProgetto='{self.NomeProgetto}')>"


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
    IsFinalMilestone = Column(Boolean, default=False, nullable=False)

    # Relationship
    # --- CORREZIONE QUI ---
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

    # Relationships ai modelli dello stesso DB
    task_catalogo = relationship("TaskCatalogo")
    prodotto = relationship("Prodotto", back_populates="task_prodotto")
    wave = relationship("WaveNPI", back_populates="tasks")
    notification_logs = relationship("NotificationLog", back_populates="task_prodotto", cascade="all, delete-orphan")

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