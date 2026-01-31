"""
Printer Configuration Manager
Gestisce il salvataggio e caricamento delle configurazioni stampante da file JSON.
"""

import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger("TraceabilityRS")

# Path del file di configurazione (nella directory dell'applicazione)
CONFIG_FILE = "printer_config.json"


class PrinterConfigManager:
    """Gestisce le configurazioni stampante salvate in JSON"""
    
    def __init__(self, config_file: str = CONFIG_FILE):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carica la configurazione dal file JSON"""
        if not os.path.exists(self.config_file):
            logger.info(f"File configurazione {self.config_file} non trovato, creazione default")
            return self._get_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"Configurazione caricata da {self.config_file}")
            return config
        except Exception as e:
            logger.error(f"Errore caricamento configurazione: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Restituisce la configurazione di default"""
        return {
            "connection_type": "DEFAULT",
            "ip": "",
            "port": 9100,
            "usb_printer_name": "",
            "printer_model": "ZEBRA",
            "last_updated": ""
        }
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Salva la configurazione nel file JSON"""
        try:
            from datetime import datetime
            config['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            self.config = config
            logger.info(f"Configurazione salvata in {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Errore salvataggio configurazione: {e}")
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """Restituisce la configurazione corrente"""
        return self.config.copy()
    
    def get_connection_type(self) -> str:
        """Restituisce il tipo di connessione configurato"""
        return self.config.get('connection_type', 'DEFAULT')
    
    def update_connection_type(self, connection_type: str) -> bool:
        """Aggiorna il tipo di connessione"""
        if connection_type not in ['DEFAULT', 'USB', 'IP']:
            logger.error(f"Tipo di connessione non valido: {connection_type}")
            return False
        
        self.config['connection_type'] = connection_type
        return self.save_config(self.config)
    
    def update_ip_config(self, ip: str, port: int) -> bool:
        """Aggiorna la configurazione IP"""
        self.config['connection_type'] = 'IP'
        self.config['ip'] = ip
        self.config['port'] = port
        return self.save_config(self.config)
    
    def update_usb_config(self, printer_name: str, printer_model: str = 'ZEBRA') -> bool:
        """Aggiorna la configurazione USB"""
        self.config['connection_type'] = 'USB'
        self.config['usb_printer_name'] = printer_name
        self.config['printer_model'] = printer_model
        return self.save_config(self.config)
    
    def update_default_config(self) -> bool:
        """Imposta la stampante di default di Windows"""
        self.config['connection_type'] = 'DEFAULT'
        return self.save_config(self.config)
    
    def get_config_summary(self) -> str:
        """Restituisce un riepilogo della configurazione corrente"""
        conn_type = self.config.get('connection_type', 'DEFAULT')
        
        if conn_type == 'DEFAULT':
            return "Stampante di default di Windows"
        elif conn_type == 'USB':
            printer_name = self.config.get('usb_printer_name', 'Non configurata')
            model = self.config.get('printer_model', 'ZEBRA')
            return f"USB: {printer_name} ({model})"
        elif conn_type == 'IP':
            ip = self.config.get('ip', 'Non configurato')
            port = self.config.get('port', 9100)
            return f"IP: {ip}:{port}"
        else:
            return "Non configurata"
