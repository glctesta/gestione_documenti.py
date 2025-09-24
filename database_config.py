# config/database_config.py
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import logging
from pathlib import Path

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConfig:
    def __init__(self):
        self.conn_str = None
        self._load_environment()
        self._setup_encryption()
        self._create_connection_string()

    def _load_environment(self):
        """Carica le variabili d'ambiente dal file .env.db"""
        try:
            # Cerca il file .env.db in vari percorsi
            env_path = self._find_env_file()
            if env_path:
                load_dotenv(env_path)
                logger.info(f"File di configurazione caricato: {env_path}")
            else:
                logger.warning("File .env.db non trovato, usando variabili d'ambiente di sistema")

        except Exception as e:
            logger.error(f"Errore nel caricamento della configurazione: {e}")
            raise

    def _find_env_file(self):
        """Cerca il file .env.db nelle directory vicine"""
        possible_paths = [
            '.env.db',
            '../.env.db',
            '../../.env.db',
            os.path.join(os.path.dirname(__file__), '.env.db'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env.db'),
            str(Path.home() / '.db_config' / '.env.db')
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def _setup_encryption(self):
        """Setup per la cifratura (opzionale per password cifrate)"""
        self.encryption_key = os.getenv('ENCRYPTION_KEY')
        if self.encryption_key:
            try:
                self.cipher = Fernet(self.encryption_key.encode())
            except Exception as e:
                logger.warning(f"Errore nella configurazione della cifratura: {e}")
                self.cipher = None
        else:
            self.cipher = None

    def _get_password(self):
        """Restituisce la password in modo sicuro"""
        # Prima cerca una password cifrata
        encrypted_pwd = os.getenv('DB_PWD_ENCRYPTED')
        if encrypted_pwd and self.cipher:
            try:
                return self.cipher.decrypt(encrypted_pwd.encode()).decode()
            except Exception as e:
                logger.error(f"Errore nella decifratura della password: {e}")

        # Fallback alla password in chiaro
        pwd = os.getenv('DB_PWD')
        if not pwd:
            logger.error("Password del database non configurata")
            raise ValueError("Password del database non configurata")
        return pwd

    def _create_connection_string(self):
        """Crea e valida la stringa di connessione"""
        try:
            driver = os.getenv('DB_DRIVER', '{SQL Server Native Client 11.0}')
            server = os.getenv('DB_SERVER')
            database = os.getenv('DB_DATABASE')
            uid = os.getenv('DB_UID')
            pwd = self._get_password()

            # Validazione dei parametri obbligatori
            required_params = {
                'DB_DRIVER': driver,
                'DB_SERVER': server,
                'DB_DATABASE': database,
                'DB_UID': uid,
                'DB_PWD': pwd
            }

            missing_params = []
            for param_name, param_value in required_params.items():
                if not param_value:
                    missing_params.append(param_name)

            if missing_params:
                error_msg = f"Parametri di configurazione mancanti: {', '.join(missing_params)}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            # Parametri opzionali
            trust_cert = os.getenv('DB_TRUST_SERVER_CERTIFICATE', 'yes')
            timeout = os.getenv('DB_TIMEOUT', '30')
            encrypt = os.getenv('DB_ENCRYPT', 'no')

            # Costruzione della connection string
            self.conn_str = (
                f'DRIVER={driver};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={uid};'
                f'PWD={pwd};'
                f'TrustServerCertificate={trust_cert};'
                f'Connection Timeout={timeout};'
                f'Encrypt={encrypt};'
            )

            # Maschera la password per il logging
            safe_conn_str = self.conn_str.replace(pwd, '******')
            logger.info(f"Stringa di connessione generata: {safe_conn_str}")

        except Exception as e:
            logger.error(f"Errore nella creazione della connection string: {e}")
            self.conn_str = None
            raise

    def get_connection_string(self):
        """Restituisce la stringa di connessione validata"""
        if not self.conn_str:
            raise ValueError("Stringa di connessione non inizializzata")
        return self.conn_str

    def get_connection_params(self):
        """Restituisce i parametri di connessione come dizionario"""
        return {
            'driver': os.getenv('DB_DRIVER'),
            'server': os.getenv('DB_SERVER'),
            'database': os.getenv('DB_DATABASE'),
            'uid': os.getenv('DB_UID'),
            'trust_cert': os.getenv('DB_TRUST_SERVER_CERTIFICATE', 'yes'),
            'timeout': int(os.getenv('DB_TIMEOUT', '30')),
            'encrypt': os.getenv('DB_ENCRYPT', 'no')
        }

    def test_connection(self):
        """Testa la connessione al database"""
        try:
            import pyodbc
            conn_str = self.get_connection_string()
            conn = pyodbc.connect(conn_str, timeout=10)
            conn.close()
            logger.info("Test connessione al database: SUCCESSO")
            return True
        except Exception as e:
            logger.error(f"Test connessione al database: FALLITO - {e}")
            return False


# Istanza singleton con validazione immediata
try:
    db_config = DatabaseConfig()
    logger.info("Configurazione database inizializzata con successo")
except Exception as e:
    logger.error(f"Errore nell'inizializzazione della configurazione database: {e}")
    db_config = None