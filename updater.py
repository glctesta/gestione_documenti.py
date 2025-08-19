# updater.py
import sys
import os
import shutil
import subprocess
import time
from datetime import datetime



def log(message):
    """Scrive un messaggio in un file di log per il debug."""
    log_file_path = os.path.join(os.path.expanduser("~"), "maintenance_app_updater.log")
    with open(log_file_path, "a") as f:
        f.write(f"{datetime.now()}: {message}\n")


if __name__ == "__main__":
    try:
        # Argomenti passati dal programma principale:
        # sys.argv[1]: Percorso della nuova versione (sorgente)
        # sys.argv[2]: Percorso di installazione attuale (destinazione)
        # sys.argv[3]: Nome dell'eseguibile da riavviare (es. MaintenanceApp.exe)
        source_path = sys.argv[1]
        dest_path = sys.argv[2]
        exe_name = sys.argv[3]

        log(f"Updater avviato. Sorgente: {source_path}, Destinazione: {dest_path}, Eseguibile: {exe_name}")

        # Attende 2 secondi per assicurarsi che il programma principale si sia chiuso
        time.sleep(2)

        # Copia l'intera directory della nuova versione sopra quella vecchia
        # dirs_exist_ok=True permette di sovrascrivere i file esistenti
        log("Inizio copia file...")
        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
        log("Copia completata.")

        # Rilancia il programma aggiornato
        new_exe_path = os.path.join(dest_path, exe_name)
        log(f"Rilancio di {new_exe_path}...")
        subprocess.Popen([new_exe_path])

        log("Updater ha completato il suo lavoro.")

    except Exception as e:
        # In caso di errore, lo scriviamo nel log per poterlo analizzare
        log(f"ERRORE CRITICO nell'updater: {e}")
        # Potresti anche mostrare un popup di errore qui se includessi tkinter
        # ma per un updater è meglio mantenerlo semplice.