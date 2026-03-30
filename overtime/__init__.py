"""
Overtime Management Module
Gestione Straordinari per TraceabilityRS

Questo modulo gestisce:
- Richieste di straordinario
- Autorizzazione richieste
- Rapporti e statistiche
- Analisi presenza vs approvazione
- Monitoraggio 48h/4 mesi
- Generazione PDF e notifiche email
"""

__version__ = "1.1.0"
__author__ = "TraceabilityRS Development Team"

# Esporta le funzioni principali per facilitare l'import
from .overtime_manager import OvertimeManager
from .overtime_requests_gui import open_overtime_request_window
from .overtime_approval_gui import open_overtime_approval_window
from .overtime_reports_gui import open_overtime_reports_window
from .overtime_analysis_gui import open_overtime_analysis_window
from .overtime_qa_gui import open_overtime_qa_window
from .overtime_monitoring_gui import open_overtime_monitoring_window

__all__ = [
    'OvertimeManager',
    'open_overtime_request_window',
    'open_overtime_approval_window',
    'open_overtime_reports_window',
    'open_overtime_analysis_window',
    'open_overtime_qa_window',
    'open_overtime_monitoring_window',
]

