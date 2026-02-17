# test_config_paths.py
"""
Script di test per verificare che config_manager.py cerchi i file
nella directory corretta sia in sviluppo che quando compilato.
"""
import os
import sys
from config_manager import get_base_path, ConfigManager

def test_config_paths():
    """Testa i percorsi di configurazione"""
    print("=" * 60)
    print("TEST PERCORSI CONFIGURAZIONE")
    print("=" * 60)
    
    # Informazioni ambiente
    is_frozen = getattr(sys, 'frozen', False)
    print(f"\nAmbiente: {'COMPILATO (PyInstaller)' if is_frozen else 'SVILUPPO'}")
    
    if is_frozen:
        print(f"Executable: {sys.executable}")
        exe_dir = os.path.dirname(sys.executable)
        print(f"Directory exe: {exe_dir}")
        internal_dir = os.path.join(exe_dir, '_internal')
        print(f"Directory _internal: {internal_dir}")
        print(f"_internal esiste: {os.path.exists(internal_dir)}")
    else:
        print(f"Script: {__file__}")
        print(f"Directory script: {os.path.dirname(os.path.abspath(__file__))}")
    
    # Test get_base_path
    base_path = get_base_path()
    print(f"\n{'='*60}")
    print(f"Base path restituito: {base_path}")
    print(f"Base path esiste: {os.path.exists(base_path)}")
    
    # Test ConfigManager
    print(f"\n{'='*60}")
    print("TEST CONFIG MANAGER")
    print(f"{'='*60}")
    
    cm = ConfigManager()
    print(f"\nKey file: {cm.key_file}")
    print(f"Key file esiste: {os.path.exists(cm.key_file)}")
    
    print(f"\nConfig file: {cm.config_file}")
    print(f"Config file esiste: {os.path.exists(cm.config_file)}")
    
    # Prova a caricare la configurazione
    print(f"\n{'='*60}")
    print("TEST CARICAMENTO CONFIGURAZIONE")
    print(f"{'='*60}")
    
    try:
        config = cm.load_config()
        print("\n✅ Configurazione caricata con successo!")
        print(f"Driver: {config.get('driver', 'N/A')}")
        print(f"Server: {config.get('server', 'N/A')}")
        print(f"Database: {config.get('database', 'N/A')}")
        print(f"Username: {config.get('username', 'N/A')}")
        print(f"Password: {'*' * len(config.get('password', ''))}")
    except FileNotFoundError as e:
        print(f"\n❌ File di configurazione non trovato: {e}")
    except Exception as e:
        print(f"\n❌ Errore caricamento configurazione: {e}")
    
    print(f"\n{'='*60}")
    print("TEST COMPLETATO")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    test_config_paths()
