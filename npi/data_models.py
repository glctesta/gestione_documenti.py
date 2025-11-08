# File: npi/models.py (Versione corretta e allineata)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, NVARCHAR, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Soggetto(Base):
    __tablename__ = 'Soggetti'
    __table_args__ = {'schema': 'dbo'}
    SoggettoID = Column(Integer, primary_key=True, autoincrement=True)
    NomeSoggetto = Column(NVARCHAR(255), nullable=False)
    Tipo = Column(NVARCHAR(50), nullable=False)
    Email = Column(NVARCHAR(255), unique=True, nullable=True)
    MSTeamsUserID = Column(NVARCHAR(255), unique=True, nullable=True)

class Categoria(Base): # NOME CAMBIATO
    __tablename__ = 'Categories'
    __table_args__ = {'schema': 'dbo'}
    CategoryId = Column(Integer, primary_key=True)
    Category = Column(NVARCHAR(100), nullable=False, unique=True)
    tasks_catalogo = relationship("TaskCatalogo", back_populates="category") # NOME RELAZIONE CAMBIATO
    NrOrdin = Column(Integer, unique=True, nullable=False)

class TaskCatalogo(Base):
    __tablename__ = 'TaskCatalogo'
    __table_args__ = {'schema': 'dbo'}
    TaskID = Column(Integer, primary_key=True, autoincrement=True)
    ItemID = Column(NVARCHAR(50), nullable=False, unique=True)
    NomeTask = Column(NVARCHAR(255))
    Descrizione = Column(NVARCHAR)
    CategoryId = Column(Integer, ForeignKey('dbo.Categories.CategoryId'))
    category = relationship("Categoria", back_populates="tasks_catalogo") # NOME RELAZIONE CAMBIATO
    NrOrdin = Column(Integer, unique=True)
    IsTitle = Column(Boolean, default=False, nullable=False)

class Prodotto(Base):
    __tablename__ = 'Prodotti'
    __table_args__ = {'schema': 'dbo'}
    ProdottoID = Column(Integer, primary_key=True, autoincrement=True)
    NomeProdotto = Column(NVARCHAR(255), nullable=False, unique=True)
    CodiceProdotto = Column(NVARCHAR(100))
    Cliente = Column(NVARCHAR(255))
    progetti = relationship("ProgettoNPI", back_populates="prodotto", cascade="all, delete, delete-orphan")

class ProgettoNPI(Base):
    __tablename__ = 'ProgettiNPI'
    __table_args__ = {'schema': 'dbo'}
    ProgettoID = Column(Integer, primary_key=True, autoincrement=True)
    ProdottoID = Column(Integer, ForeignKey('dbo.Prodotti.ProdottoID'))
    DataInizio = Column(DateTime)
    StatoProgetto = Column(NVARCHAR(50), default='Attivo')
    prodotto = relationship("Prodotto", back_populates="progetti")
    waves = relationship("WaveNPI", back_populates="progetto", cascade="all, delete, delete-orphan")

class WaveNPI(Base):
    __tablename__ = 'WaveNPI'
    __table_args__ = {'schema': 'dbo'}
    WaveID = Column(Integer, primary_key=True, autoincrement=True)
    ProgettoID = Column(Integer, ForeignKey('dbo.ProgettiNPI.ProgettoID'))
    WaveIdentifier = Column(DECIMAL(5, 2), nullable=False)
    progetto = relationship("ProgettoNPI", back_populates="waves")
    tasks = relationship("TaskProdotto", back_populates="wave", cascade="all, delete, delete-orphan")

class TaskProdotto(Base): # QUESTA E' LA CLASSE CORRETTA
    __tablename__ = 'TaskProdotto'
    __table_args__ = {'schema': 'dbo'}
    TaskProdottoID = Column(Integer, primary_key=True, autoincrement=True)
    WaveID = Column(Integer, ForeignKey('dbo.WaveNPI.WaveID'))
    TaskID = Column(Integer, ForeignKey('dbo.TaskCatalogo.TaskID')) # Linka al template nel catalogo
    OwnerID = Column(Integer, ForeignKey('dbo.Soggetti.SoggettoID'), nullable=True) # Reso nullable
    Stato = Column(NVARCHAR(50), default='Da Fare') # Default cambiato
    DataInizio = Column(Date, nullable=True) # Tipo cambiato in Date
    DataScadenza = Column(Date, nullable=True) # Tipo cambiato in Date
    DataCompletamento = Column(Date, nullable=True) # Tipo cambiato in Date e reso nullable
    Costo = Column(DECIMAL(10, 2), nullable=True)
    Note = Column(Text, nullable=True) # Tipo cambiato in Text per note più lunghe
    wave = relationship("WaveNPI", back_populates="tasks")
    task_template = relationship("TaskCatalogo") # questa è la relazione al modello del catalogo
    owner = relationship("Soggetto")

# Aggiungi questa classe dopo le classi esistenti in data_models.py

class NotificationLog(Base):
    __tablename__ = 'NotificationLog'
    __table_args__ = {'schema': 'dbo'}
    LogID = Column(Integer, primary_key=True, autoincrement=True)
    ProgettoID = Column(Integer, ForeignKey('dbo.ProgettiNPI.ProgettoID'), nullable=False)
    TaskProdottoID = Column(Integer, ForeignKey('dbo.TaskProdotto.TaskProdottoID'), nullable=False)
    SoggettoID = Column(Integer, ForeignKey('dbo.Soggetti.SoggettoID'), nullable=False)
    CanaleInvio = Column(NVARCHAR(20), nullable=False)
    DataInvio = Column(DateTime, nullable=False, default=datetime.now)
    StatoInvio = Column(NVARCHAR(50), nullable=False)
    MessaggioErrore = Column(Text, nullable=True)