# config_manager.py
from cryptography.fernet import Fernet
import json
import os
import sys


def get_base_path():
    """
    Restituisce il percorso base dell'applicazione per i file di configurazione.
    
    - In sviluppo: usa la directory corrente dello script
    - Compilato con PyInstaller: usa la directory _internal
    
    Questo permette all'updater di sovrascrivere le credenziali centralizzate.
    """
    if getattr(sys, 'frozen', False):
        # Se l'app è compilata con PyInstaller
        # sys._MEIPASS punta alla directory _internal temporanea
        # ma vogliamo la directory _internal permanente accanto all'exe
        exe_dir = os.path.dirname(sys.executable)
        internal_dir = os.path.join(exe_dir, '_internal')
        
        # Usa _internal se esiste, altrimenti fallback alla directory exe
        if os.path.exists(internal_dir):
            return internal_dir
        else:
            return exe_dir
    else:
        # Se in sviluppo, usa la directory corrente
        return os.path.dirname(os.path.abspath(__file__))


class ConfigManager:
    def __init__(self, key_file='encryption_key.key', config_file='db_config.enc'):
        # Usa il percorso base dell'applicazione
        base_path = get_base_path()
        self.key_file = os.path.join(base_path, key_file)
        self.config_file = os.path.join(base_path, config_file)

    def generate_key(self):
        """Genera una chiave di crittografia e la salva in un file"""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as key_file:
            key_file.write(key)

    def load_key(self):
        """Carica la chiave di crittografia dal file"""
        if not os.path.exists(self.key_file):
            self.generate_key()
        with open(self.key_file, 'rb') as key_file:
            return key_file.read()

    def save_config(self, driver, server, database, username, password):
        """Salva le credenziali del database in modo crittografato"""
        config = {
            'driver': driver,
            'server': server,
            'database': database,
            'username': username,
            'password': password
        }

        key = self.load_key()
        f = Fernet(key)
        encrypted_config = f.encrypt(json.dumps(config).encode())

        with open(self.config_file, 'wb') as config_file:
            config_file.write(encrypted_config)

    def load_config(self):
        """Carica e decritta le credenziali del database"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"File di configurazione non trovato: {self.config_file}")

        key = self.load_key()
        f = Fernet(key)

        with open(self.config_file, 'rb') as config_file:
            encrypted_config = config_file.read()

        decrypted_config = f.decrypt(encrypted_config)
        return json.loads(decrypted_config)
