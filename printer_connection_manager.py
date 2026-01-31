"""
Printer Connection Manager
Gestisce le connessioni alle stampanti per la stampa etichette.
Supporta:
- Stampanti USB (Zebra, Brother)
- Stampante di default di Windows
- Stampanti IP/Network
"""

import logging
import socket
import win32print
import win32api
from typing import Optional, Dict, Any, List

logger = logging.getLogger("TraceabilityRS")


class PrinterConnectionError(Exception):
    """Eccezione per errori di connessione stampante"""
    pass


class PrinterConnection:
    """Classe base per connessioni stampante"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection_type = config.get('connection_type', 'DEFAULT')
    
    def connect(self) -> bool:
        """Stabilisce la connessione alla stampante"""
        raise NotImplementedError
    
    def disconnect(self):
        """Chiude la connessione"""
        raise NotImplementedError
    
    def test_connection(self) -> bool:
        """Testa la connessione alla stampante"""
        raise NotImplementedError
    
    def print_label(self, label_data: str) -> bool:
        """Stampa un'etichetta"""
        raise NotImplementedError
    
    def get_status(self) -> str:
        """Ottiene lo stato della stampante"""
        raise NotImplementedError


class DefaultWindowsPrinterConnection(PrinterConnection):
    """Connessione alla stampante di default di Windows"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.printer_name = None
    
    def connect(self) -> bool:
        """Ottiene la stampante di default"""
        try:
            self.printer_name = win32print.GetDefaultPrinter()
            logger.info(f"Stampante di default: {self.printer_name}")
            return True
        except Exception as e:
            logger.error(f"Errore ottenimento stampante di default: {e}")
            raise PrinterConnectionError(f"Impossibile ottenere la stampante di default: {e}")
    
    def disconnect(self):
        """Non necessario per stampante Windows"""
        pass
    
    def test_connection(self) -> bool:
        """Verifica che la stampante di default sia disponibile"""
        try:
            if not self.printer_name:
                self.connect()
            
            # Verifica che la stampante esista
            printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
            
            if self.printer_name in printers:
                logger.info(f"Test connessione stampante '{self.printer_name}': OK")
                return True
            else:
                logger.warning(f"Stampante '{self.printer_name}' non trovata")
                return False
        except Exception as e:
            logger.error(f"Errore test connessione: {e}")
            return False
    
    def print_label(self, label_data: str) -> bool:
        """Stampa un'etichetta usando la stampante di default"""
        try:
            if not self.printer_name:
                self.connect()
            
            # Apre la stampante
            hPrinter = win32print.OpenPrinter(self.printer_name)
            
            try:
                # Inizia un documento di stampa
                hJob = win32print.StartDocPrinter(hPrinter, 1, ("Label", None, "RAW"))
                
                try:
                    win32print.StartPagePrinter(hPrinter)
                    
                    # Invia i dati alla stampante
                    win32print.WritePrinter(hPrinter, label_data.encode('utf-8'))
                    
                    win32print.EndPagePrinter(hPrinter)
                finally:
                    win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)
            
            logger.info(f"Etichetta stampata su '{self.printer_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Errore stampa etichetta: {e}")
            raise PrinterConnectionError(f"Errore durante la stampa: {e}")
    
    def get_status(self) -> str:
        """Ottiene lo stato della stampante"""
        try:
            if not self.printer_name:
                self.connect()
            return f"Stampante di default: {self.printer_name}"
        except:
            return "Stampante di default non disponibile"


class USBPrinterConnection(PrinterConnection):
    """Connessione diretta a stampante USB (Zebra, Brother)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.printer_name = config.get('usb_printer_name')
        self.printer_model = config.get('printer_model', 'ZEBRA')  # ZEBRA o BROTHER
    
    def connect(self) -> bool:
        """Verifica che la stampante USB sia disponibile"""
        try:
            if not self.printer_name:
                raise PrinterConnectionError("Nome stampante USB non specificato")
            
            # Verifica che la stampante esista
            printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
            
            if self.printer_name in printers:
                logger.info(f"Stampante USB '{self.printer_name}' trovata")
                return True
            else:
                raise PrinterConnectionError(f"Stampante USB '{self.printer_name}' non trovata")
        except Exception as e:
            logger.error(f"Errore connessione stampante USB: {e}")
            raise
    
    def disconnect(self):
        """Non necessario per stampante USB"""
        pass
    
    def test_connection(self) -> bool:
        """Testa la connessione alla stampante USB"""
        try:
            return self.connect()
        except:
            return False
    
    def print_label(self, label_data: str) -> bool:
        """Stampa un'etichetta sulla stampante USB"""
        try:
            # Apre la stampante
            hPrinter = win32print.OpenPrinter(self.printer_name)
            
            try:
                # Inizia un documento di stampa
                hJob = win32print.StartDocPrinter(hPrinter, 1, ("Label", None, "RAW"))
                
                try:
                    win32print.StartPagePrinter(hPrinter)
                    
                    # Invia i dati ZPL/ESC-POS alla stampante
                    win32print.WritePrinter(hPrinter, label_data.encode('utf-8'))
                    
                    win32print.EndPagePrinter(hPrinter)
                finally:
                    win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)
            
            logger.info(f"Etichetta stampata su '{self.printer_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Errore stampa etichetta USB: {e}")
            raise PrinterConnectionError(f"Errore durante la stampa USB: {e}")
    
    def get_status(self) -> str:
        """Ottiene lo stato della stampante"""
        try:
            if self.connect():
                return f"Stampante USB: {self.printer_name} ({self.printer_model})"
        except:
            pass
        return f"Stampante USB '{self.printer_name}' non disponibile"


class IPPrinterConnection(PrinterConnection):
    """Connessione a stampante di rete via IP"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.ip = config.get('ip')
        self.port = config.get('port', 9100)
        self.socket = None
    
    def connect(self) -> bool:
        """Stabilisce connessione socket alla stampante IP"""
        try:
            if not self.ip:
                raise PrinterConnectionError("Indirizzo IP non specificato")
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.ip, self.port))
            logger.info(f"Connesso a stampante IP {self.ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Errore connessione stampante IP: {e}")
            raise PrinterConnectionError(f"Impossibile connettersi a {self.ip}:{self.port}: {e}")
    
    def disconnect(self):
        """Chiude la connessione socket"""
        if self.socket:
            try:
                self.socket.close()
                logger.info("Connessione stampante IP chiusa")
            except:
                pass
            self.socket = None
    
    def test_connection(self) -> bool:
        """Testa la connessione alla stampante IP"""
        try:
            self.connect()
            self.disconnect()
            return True
        except:
            return False
    
    def print_label(self, label_data: str) -> bool:
        """Stampa un'etichetta sulla stampante IP"""
        try:
            if not self.socket:
                self.connect()
            
            self.socket.sendall(label_data.encode('utf-8'))
            logger.info(f"Etichetta inviata a {self.ip}:{self.port}")
            return True
            
        except Exception as e:
            logger.error(f"Errore stampa etichetta IP: {e}")
            raise PrinterConnectionError(f"Errore durante la stampa IP: {e}")
    
    def get_status(self) -> str:
        """Ottiene lo stato della stampante"""
        return f"Stampante IP: {self.ip}:{self.port}"


def get_printer_connection(config: Dict[str, Any]) -> PrinterConnection:
    """Factory per creare la connessione appropriata in base alla configurazione"""
    connection_type = config.get('connection_type', 'DEFAULT').upper()
    
    if connection_type == 'DEFAULT':
        return DefaultWindowsPrinterConnection(config)
    elif connection_type == 'USB':
        return USBPrinterConnection(config)
    elif connection_type == 'IP':
        return IPPrinterConnection(config)
    else:
        raise ValueError(f"Tipo di connessione non supportato: {connection_type}")


def get_available_printers() -> List[str]:
    """Ottiene la lista delle stampanti disponibili sul sistema"""
    try:
        printers = [printer[2] for printer in win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )]
        return printers
    except Exception as e:
        logger.error(f"Errore ottenimento lista stampanti: {e}")
        return []


def get_default_printer() -> Optional[str]:
    """Ottiene il nome della stampante di default"""
    try:
        return win32print.GetDefaultPrinter()
    except Exception as e:
        logger.error(f"Errore ottenimento stampante di default: {e}")
        return None
