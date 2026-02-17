# setup_db_credentials.py
"""
Script per configurare le credenziali del database in modo criptato.
Usa il ConfigManager esistente per salvare le credenziali in db_config.enc
"""
from config_manager import ConfigManager


def setup_database_credentials():
    """Configura le credenziali del database in modo interattivo"""
    print("=" * 60)
    print("CONFIGURAZIONE CREDENZIALI DATABASE CRIPTATE")
    print("=" * 60)
    print()
    
    # Credenziali attuali (da main.py)
    default_driver = '{SQL Server Native Client 11.0}'
    default_server = 'roghipsql01.vandewiele.local\\emsreset'
    default_database = 'Traceability_rs'
    default_username = 'emsreset'
    default_password = 'E6QhqKUxHFXTbkB7eA8c9ya'
    
    print("Inserisci le credenziali del database")
    print("(premi INVIO per usare i valori di default)")
    print()
    
    # Richiedi le credenziali
    driver = input(f"Driver [{default_driver}]: ").strip() or default_driver
    server = input(f"Server [{default_server}]: ").strip() or default_server
    database = input(f"Database [{default_database}]: ").strip() or default_database
    username = input(f"Username [{default_username}]: ").strip() or default_username
    password = input(f"Password [{default_password}]: ").strip() or default_password
    
    print()
    print("-" * 60)
    print("Riepilogo configurazione:")
    print(f"  Driver:   {driver}")
    print(f"  Server:   {server}")
    print(f"  Database: {database}")
    print(f"  Username: {username}")
    print(f"  Password: {'*' * len(password)}")
    print("-" * 60)
    print()
    
    confirm = input("Confermi di voler salvare queste credenziali? (s/n): ").strip().lower()
    
    if confirm != 's':
        print("Operazione annullata.")
        return
    
    try:
        # Usa il ConfigManager esistente
        config_mgr = ConfigManager(
            key_file='encryption_key.key',
            config_file='db_config.enc'
        )
        
        # Salva le credenziali criptate
        config_mgr.save_config(
            driver=driver,
            server=server,
            database=database,
            username=username,
            password=password
        )
        
        print()
        print("✅ Credenziali salvate con successo!")
        print(f"   File creato: db_config.enc")
        print(f"   Chiave usata: encryption_key.key")
        print()
        print("Ora puoi avviare main.py con le credenziali criptate.")
        
    except Exception as e:
        print()
        print(f"❌ Errore durante il salvataggio: {e}")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    setup_database_credentials()
