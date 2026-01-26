from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .data_models import Base

# ========================================
# 12. NpiTaskNotification
# ========================================
class NpiTaskNotification(Base):
    __tablename__ = 'NpiTaskNotifications'
    __table_args__ = {'schema': 'dbo'}
    
    NotificationID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Riferimenti
    TaskProdottoID = Column(Integer, ForeignKey('dbo.TaskProdotto.TaskProdottoID'), nullable=False)
    ProgettoID = Column(Integer, ForeignKey('dbo.ProgettiNPI.ProgettoID'), nullable=False)
    RecipientSoggettoID = Column(Integer, nullable=False)
    
    # Tipo notifica
    NotificationType = Column(String(50), nullable=False)  # 'TaskDueTomorrow', 'TaskOverdue'
    NotificationDate = Column(Date, nullable=False)
    
    # Dettagli invio
    SentDateTime = Column(DateTime, default=datetime.utcnow, nullable=False)
    RecipientEmail = Column(String(255), nullable=False)
    RecipientName = Column(String(255))
    RecipientType = Column(String(50))  # 'TaskOwner', 'ProjectOwner'
    
    # Status
    DeliveryStatus = Column(String(50), nullable=False)  # 'Sent', 'Failed', 'Skipped'
    ErrorMessage = Column(Text)
    
    # Metadata
    CreatedBy = Column(String(100), default='AutoNotificationService')
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    task_prodotto = relationship("TaskProdotto")
    progetto = relationship("ProgettoNPI")
    
    def __repr__(self):
        return f"<NpiTaskNotification(ID={self.NotificationID}, Task={self.TaskProdottoID}, Type={self.NotificationType})>"
