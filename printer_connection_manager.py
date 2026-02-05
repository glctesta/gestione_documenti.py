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
            logger.info("🖨️ PRINT_LABEL: Inizio processo di stampa (Default Windows Printer)")
            
            if not self.printer_name:
                logger.info("🖨️ PRINT_LABEL: Connessione alla stampante di default...")
                self.connect()
            
            logger.info(f"🖨️ PRINT_LABEL: Stampante selezionata: '{self.printer_name}'")
            logger.info(f"🖨️ PRINT_LABEL: Dimensione dati da stampare: {len(label_data)} bytes")
            
            # Apre la stampante
            logger.info("🖨️ PRINT_LABEL: Apertura handle stampante...")
            hPrinter = win32print.OpenPrinter(self.printer_name)
            logger.info(f"🖨️ PRINT_LABEL: ✓ Handle stampante aperto: {hPrinter}")
            
            try:
                # Inizia un documento di stampa
                logger.info("🖨️ PRINT_LABEL: Avvio documento di stampa...")
                hJob = win32print.StartDocPrinter(hPrinter, 1, ("Label", None, "RAW"))
                logger.info(f"🖨️ PRINT_LABEL: ✓ Documento avviato, Job ID: {hJob}")
                
                try:
                    logger.info("🖨️ PRINT_LABEL: Avvio pagina...")
                    win32print.StartPagePrinter(hPrinter)
                    logger.info("🖨️ PRINT_LABEL: ✓ Pagina avviata")
                    
                    # Invia i dati alla stampante
                    logger.info("🖨️ PRINT_LABEL: Invio dati alla stampante...")
                    bytes_written = win32print.WritePrinter(hPrinter, label_data.encode('utf-8'))
                    logger.info(f"🖨️ PRINT_LABEL: ✓ Dati inviati: {bytes_written} bytes scritti")
                    
                    logger.info("🖨️ PRINT_LABEL: Chiusura pagina...")
                    win32print.EndPagePrinter(hPrinter)
                    logger.info("🖨️ PRINT_LABEL: ✓ Pagina chiusa")
                finally:
                    logger.info("🖨️ PRINT_LABEL: Chiusura documento...")
                    win32print.EndDocPrinter(hPrinter)
                    logger.info("🖨️ PRINT_LABEL: ✓ Documento chiuso")
            finally:
                logger.info("🖨️ PRINT_LABEL: Chiusura handle stampante...")
                win32print.ClosePrinter(hPrinter)
                logger.info("🖨️ PRINT_LABEL: ✓ Handle stampante chiuso")
            
            # Verifica stato stampante dopo la stampa
            logger.info("🖨️ PRINT_LABEL: Verifica stato stampante dopo la stampa...")
            try:
                hPrinter = win32print.OpenPrinter(self.printer_name)
                printer_info = win32print.GetPrinter(hPrinter, 2)
                win32print.ClosePrinter(hPrinter)
                
                status = printer_info.get('Status', 0)
                status_msg = self._get_printer_status_message(status)
                logger.info(f"🖨️ PRINT_LABEL: Status stampante post-stampa: {status} - {status_msg}")
                
                # Verifica job nella coda
                hPrinter = win32print.OpenPrinter(self.printer_name)
                jobs = win32print.EnumJobs(hPrinter, 0, -1, 1)
                win32print.ClosePrinter(hPrinter)
                logger.info(f"🖨️ PRINT_LABEL: Job in coda: {len(jobs)}")
                
                if len(jobs) > 0:
                    for job in jobs:
                        logger.info(f"🖨️ PRINT_LABEL: Job ID {job['JobId']}: Status={job.get('Status', 'N/A')}, Pages={job.get('TotalPages', 0)}")
                else:
                    logger.info("🖨️ PRINT_LABEL: ✓ Nessun job in coda (stampa completata o in corso)")
                
            except Exception as e:
                logger.warning(f"🖨️ PRINT_LABEL: Impossibile verificare status post-stampa: {e}")
            
            logger.info(f"🖨️ PRINT_LABEL: ✅ STAMPA COMPLETATA CON SUCCESSO su '{self.printer_name}'")
            return True
            
        except Exception as e:
            logger.error(f"🖨️ PRINT_LABEL: ❌ ERRORE DURANTE LA STAMPA: {e}", exc_info=True)
            raise PrinterConnectionError(f"Errore durante la stampa: {e}")
    
    def _get_printer_status_message(self, status: int) -> str:
        """Converte il codice di status in messaggio leggibile"""
        status_messages = {
            0: "READY (Pronta)",
            0x00000001: "PAUSED (In pausa)",
            0x00000002: "ERROR (Errore)",
            0x00000004: "PENDING_DELETION (In eliminazione)",
            0x00000008: "PAPER_JAM (Carta inceppata)",
            0x00000010: "PAPER_OUT (Carta esaurita)",
            0x00000020: "MANUAL_FEED (Alimentazione manuale)",
            0x00000040: "PAPER_PROBLEM (Problema carta)",
            0x00000080: "OFFLINE (Offline)",
            0x00000100: "IO_ACTIVE (I/O attivo)",
            0x00000200: "BUSY (Occupata)",
            0x00000400: "PRINTING (In stampa)",
            0x00000800: "OUTPUT_BIN_FULL (Vassoio pieno)",
            0x00001000: "NOT_AVAILABLE (Non disponibile)",
            0x00002000: "WAITING (In attesa)",
            0x00004000: "PROCESSING (In elaborazione)",
            0x00008000: "INITIALIZING (Inizializzazione)",
            0x00010000: "WARMING_UP (Riscaldamento)",
            0x00020000: "TONER_LOW (Toner basso)",
            0x00040000: "NO_TONER (Toner esaurito)",
            0x00080000: "PAGE_PUNT (Pagina espulsa)",
            0x00100000: "USER_INTERVENTION (Intervento utente)",
            0x00200000: "OUT_OF_MEMORY (Memoria esaurita)",
            0x00400000: "DOOR_OPEN (Sportello aperto)",
        }
        return status_messages.get(status, f"UNKNOWN ({hex(status)})")
    
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
            logger.info(f"🖨️ PRINT_LABEL: Inizio processo di stampa USB (Modello: {self.printer_model})")
            logger.info(f"🖨️ PRINT_LABEL: Stampante USB: '{self.printer_name}'")
            logger.info(f"🖨️ PRINT_LABEL: Dimensione dati da stampare: {len(label_data)} bytes")
            
            # Apre la stampante
            logger.info("🖨️ PRINT_LABEL: Apertura handle stampante USB...")
            hPrinter = win32print.OpenPrinter(self.printer_name)
            logger.info(f"🖨️ PRINT_LABEL: ✓ Handle stampante USB aperto: {hPrinter}")
            
            try:
                # Inizia un documento di stampa
                logger.info("🖨️ PRINT_LABEL: Avvio documento di stampa USB...")
                hJob = win32print.StartDocPrinter(hPrinter, 1, ("Label", None, "RAW"))
                logger.info(f"🖨️ PRINT_LABEL: ✓ Documento USB avviato, Job ID: {hJob}")
                
                try:
                    logger.info("🖨️ PRINT_LABEL: Avvio pagina USB...")
                    win32print.StartPagePrinter(hPrinter)
                    logger.info("🖨️ PRINT_LABEL: ✓ Pagina USB avviata")
                    
                    # Invia i dati ZPL/ESC-POS alla stampante
                    logger.info(f"🖨️ PRINT_LABEL: Invio dati {self.printer_model} alla stampante USB...")
                    bytes_written = win32print.WritePrinter(hPrinter, label_data.encode('utf-8'))
                    logger.info(f"🖨️ PRINT_LABEL: ✓ Dati USB inviati: {bytes_written} bytes scritti")
                    
                    logger.info("🖨️ PRINT_LABEL: Chiusura pagina USB...")
                    win32print.EndPagePrinter(hPrinter)
                    logger.info("🖨️ PRINT_LABEL: ✓ Pagina USB chiusa")
                finally:
                    logger.info("🖨️ PRINT_LABEL: Chiusura documento USB...")
                    win32print.EndDocPrinter(hPrinter)
                    logger.info("🖨️ PRINT_LABEL: ✓ Documento USB chiuso")
            finally:
                logger.info("🖨️ PRINT_LABEL: Chiusura handle stampante USB...")
                win32print.ClosePrinter(hPrinter)
                logger.info("🖨️ PRINT_LABEL: ✓ Handle stampante USB chiuso")
            
            # Verifica stato stampante dopo la stampa
            logger.info("🖨️ PRINT_LABEL: Verifica stato stampante USB dopo la stampa...")
            try:
                hPrinter = win32print.OpenPrinter(self.printer_name)
                printer_info = win32print.GetPrinter(hPrinter, 2)
                win32print.ClosePrinter(hPrinter)
                
                status = printer_info.get('Status', 0)
                logger.info(f"🖨️ PRINT_LABEL: Status stampante USB post-stampa: {status}")
                
                # Verifica job nella coda
                hPrinter = win32print.OpenPrinter(self.printer_name)
                jobs = win32print.EnumJobs(hPrinter, 0, -1, 1)
                win32print.ClosePrinter(hPrinter)
                logger.info(f"🖨️ PRINT_LABEL: Job USB in coda: {len(jobs)}")
                
                if len(jobs) > 0:
                    for job in jobs:
                        job_status = job.get('Status', 0)
                        job_status_msg = self._decode_job_status(job_status)
                        logger.info(f"🖨️ PRINT_LABEL: USB Job ID {job['JobId']}: Status={job_status} ({job_status_msg})")
                        
                        # Avviso se il job ha problemi
                        if job_status != 0 and job_status != 16:  # 0=printing, 16=spooling
                            logger.warning(f"⚠️ PRINT_LABEL: ATTENZIONE - Job in coda con status problematico: {job_status_msg}")
                            logger.warning(f"⚠️ PRINT_LABEL: La stampante potrebbe avere problemi hardware (carta, coperchio, ecc.)")
                else:
                    logger.info("🖨️ PRINT_LABEL: ✓ Nessun job USB in coda (stampa completata o in corso)")
                
            except Exception as e:
                logger.warning(f"🖨️ PRINT_LABEL: Impossibile verificare status USB post-stampa: {e}")
            
            logger.info(f"🖨️ PRINT_LABEL: ✅ STAMPA USB COMPLETATA CON SUCCESSO su '{self.printer_name}'")
            return True
            
        except Exception as e:
            logger.error(f"🖨️ PRINT_LABEL: ❌ ERRORE DURANTE LA STAMPA USB: {e}", exc_info=True)
            raise PrinterConnectionError(f"Errore durante la stampa USB: {e}")
    
    def _decode_job_status(self, status: int) -> str:
        """Decodifica lo status code del job di stampa"""
        # Status codes comuni per i job di stampa Windows
        status_flags = []
        
        if status == 0:
            return "PRINTING (In stampa)"
        
        if status & 0x0001:
            status_flags.append("PAUSED")
        if status & 0x0002:
            status_flags.append("ERROR")
        if status & 0x0004:
            status_flags.append("DELETING")
        if status & 0x0010:
            status_flags.append("SPOOLING")
        if status & 0x0020:
            status_flags.append("PRINTING")
        if status & 0x0040:
            status_flags.append("OFFLINE")
        if status & 0x0080:
            status_flags.append("PAPEROUT")
        if status & 0x0100:
            status_flags.append("PRINTED")
        if status & 0x0200:
            status_flags.append("DELETED")
        if status & 0x2000:
            status_flags.append("RETAINED")
        if status & 0x8000:
            status_flags.append("RESTART")
        
        if status_flags:
            return " | ".join(status_flags)
        else:
            return f"UNKNOWN (0x{status:04X})"
    
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
            logger.info(f"🖨️ PRINT_LABEL: Inizio processo di stampa IP")
            logger.info(f"🖨️ PRINT_LABEL: Stampante IP: {self.ip}:{self.port}")
            logger.info(f"🖨️ PRINT_LABEL: Dimensione dati da stampare: {len(label_data)} bytes")
            
            if not self.socket:
                logger.info("🖨️ PRINT_LABEL: Connessione socket alla stampante IP...")
                self.connect()
                logger.info("🖨️ PRINT_LABEL: ✓ Socket connesso")
            
            logger.info("🖨️ PRINT_LABEL: Invio dati alla stampante IP...")
            self.socket.sendall(label_data.encode('utf-8'))
            logger.info(f"🖨️ PRINT_LABEL: ✓ Dati inviati a {self.ip}:{self.port}")
            
            # Attendi un breve momento per la risposta della stampante (se disponibile)
            logger.info("🖨️ PRINT_LABEL: Attesa risposta stampante IP (timeout 2s)...")
            try:
                self.socket.settimeout(2.0)
                response = self.socket.recv(1024)
                if response:
                    logger.info(f"🖨️ PRINT_LABEL: ✓ Risposta ricevuta dalla stampante IP: {response[:100]}")
                else:
                    logger.info("🖨️ PRINT_LABEL: Nessuna risposta dalla stampante IP (normale per alcune stampanti)")
            except socket.timeout:
                logger.info("🖨️ PRINT_LABEL: Timeout risposta stampante IP (normale, stampa probabilmente in corso)")
            except Exception as e:
                logger.info(f"🖨️ PRINT_LABEL: Nessuna risposta dalla stampante IP: {e}")
            finally:
                # Ripristina timeout originale
                self.socket.settimeout(5.0)
            
            logger.info(f"🖨️ PRINT_LABEL: ✅ STAMPA IP COMPLETATA CON SUCCESSO a {self.ip}:{self.port}")
            return True
            
        except Exception as e:
            logger.error(f"🖨️ PRINT_LABEL: ❌ ERRORE DURANTE LA STAMPA IP: {e}", exc_info=True)
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
