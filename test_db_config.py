# test_db_config.py
"""
Script di test per verificare che le credenziali criptate funzionino correttamente
"""
from config_manager import ConfigManager
import pyodbc


def test_db_config():
    """Testa il caricamento delle credenziali e la connessione al database"""
    print("=" * 60)
    print("TEST CONFIGURAZIONE DATABASE CRIPTATA")
    print("=" * 60)
    print()
    
    try:
        # Carica le credenziali
        print("1. Caricamento credenziali da db_config.enc...")
        config_mgr = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
        db_credentials = config_mgr.load_config()
        
        print("   ✅ Credenziali caricate con successo")
        print(f"      Driver:   {db_credentials['driver']}")
        print(f"      Server:   {db_credentials['server']}")
        print(f"      Database: {db_credentials['database']}")
        print(f"      Username: {db_credentials['username']}")
        print(f"      Password: {'*' * len(db_credentials['password'])}")
        print()
        
        # Costruisci la connection string
        print("2. Costruzione connection string...")
        DB_DRIVER = db_credentials['driver']
        DB_SERVER = db_credentials['server']
        DB_DATABASE = db_credentials['database']
        DB_UID = db_credentials['username']
        DB_PWD = db_credentials['password']
        DB_CONN_STR = (f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};'
                       f'UID={DB_UID};PWD={DB_PWD};MARS_Connection=Yes;TrustServerCertificate=Yes')
        
        print("   ✅ Connection string creata")
        print()
        
        # Test connessione
        print("3. Test connessione al database...")
        conn = pyodbc.connect(DB_CONN_STR, timeout=10)
        cursor = conn.cursor()
        
        # Esegui una query di test
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        
        print("   ✅ Connessione riuscita!")
        print(f"      SQL Server Version: {version[:80]}...")
        print()
        
        cursor.close()
        conn.close()
        
        print("=" * 60)
        print("✅ TUTTI I TEST SUPERATI!")
        print("=" * 60)
        print()
        print("Il sistema di credenziali criptate funziona correttamente.")
        print("Ora puoi avviare main.py in sicurezza.")
        
        return True
        
    except FileNotFoundError as e:
        print(f"   ❌ File non trovato: {e}")
        print()
        print("Esegui prima setup_db_credentials.py")
        return False
        
    except pyodbc.Error as e:
        print(f"   ❌ Errore di connessione al database:")
        print(f"      {e}")
        print()
        print("Verifica che le credenziali siano corrette.")
        return False
        
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_db_config()
