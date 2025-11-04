import sys
import os
import shutil
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def log(message):
    log_file_path = os.path.join(os.path.expanduser("~"), "Downloads", "maintenance_app_updater.log")
    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}: {message}\n")
    except Exception as e:
        print(f"Failed to write to log: {e}")


class UpdateProgressWindow(tk.Tk):
    """Finestra grafica per mostrare il progresso dell'aggiornamento."""

    def __init__(self, source_path, dest_path, exe_name):
        super().__init__()

        self.source_path = source_path
        self.dest_path = dest_path
        self.exe_name = exe_name

        self.title("Aggiornamento Applicazione")
        self.geometry("450x150")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')

        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Label del progresso
        self.progress_label = ttk.Label(
            main_frame,
            text="Aggiornamento in corso, attendere...",
            font=("Helvetica", 10)
        )
        self.progress_label.pack(pady=(5, 10))

        # Barra di progresso
        self.progress_bar = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress_bar.pack(pady=5)

        # Frame per il nome del file (con altezza fissa)
        file_frame = ttk.Frame(main_frame, height=20)
        file_frame.pack(fill='x', pady=5)
        file_frame.pack_propagate(False)  # Mantiene l'altezza fissa

        # Label per il nome del file
        self.file_label = ttk.Label(
            file_frame,
            text="",
            font=("Helvetica", 8),
            foreground="grey",
            anchor="w",  # Questo anchor è per l'allineamento del testo DENTRO la label
            width=80
        )
        self.file_label.pack(fill='x')  # ✅ CORRETTO - riempie tutta la larghezza disponibile

        self.after(500, self.start_update)

    def update_file_label(self, text):
        """Aggiorna il testo della label del file senza artefatti grafici."""
        try:
            width = int(self.file_label.cget('width')) or 0
        except Exception:
            width = 0
        if width > 0:
            self.file_label.configure(text=" " * width)
            self.file_label.update_idletasks()

        # Imposta il nuovo testo
        self.file_label.configure(text=text or "")
        self.file_label.update_idletasks()

    def copy_files_safely(self, file_list):
        """Copia i file con gestione degli errori."""
        for i, (root, name) in enumerate(file_list):
            # Aggiorna il nome del file corrente
            self.update_file_label(f"Copia di: {name}")
            self.update_idletasks()

            if name.lower() == 'updater.exe':
                self.progress_bar["value"] = i + 1
                continue

            try:
                source_file = os.path.join(root, name)
                relative_path = os.path.relpath(root, self.source_path)
                dest_dir = os.path.join(self.dest_path, relative_path)

                # Crea directory se non esiste
                os.makedirs(dest_dir, exist_ok=True)

                # File di destinazione
                dest_file = os.path.join(dest_dir, name)

                # Tentativo di copia con ritry
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        shutil.copy2(source_file, dest_file)
                        break
                    except PermissionError:
                        if attempt < max_retries - 1:
                            time.sleep(1)  # Aspetta 1 secondo prima di ritentare
                            continue
                        else:
                            raise

                # Aggiorna la barra di progresso
                self.progress_bar["value"] = i + 1
                self.update_idletasks()

            except Exception as e:
                log(f"Errore nella copia di {name}: {e}")
                # Continua con il prossimo file invece di fermarsi completamente

    def start_update(self):
        try:
            # Attesa iniziale per permettere all'app principale di chiudersi
            self.after(2000, self._perform_update)

        except Exception as e:
            log(f"ERRORE CRITICO nell'updater: {e}")
            messagebox.showerror("Errore di Aggiornamento", f"Si è verificato un errore:\n{e}")
            self.destroy()

    def _perform_update(self):
        """Esegue l'aggiornamento vero e proprio."""
        try:
            # Verifica che le directory esistano
            if not os.path.exists(self.source_path):
                raise FileNotFoundError(f"Directory sorgente non trovata: {self.source_path}")

            if not os.path.exists(self.dest_path):
                os.makedirs(self.dest_path, exist_ok=True)

            # Crea la lista dei file da copiare
            file_list = []
            for root, _, files in os.walk(self.source_path):
                for name in files:
                    file_list.append((root, name))

            if not file_list:
                raise Exception("Nessun file trovato nella directory sorgente")

            self.progress_bar["maximum"] = len(file_list)
            self.progress_bar["value"] = 0

            # Copia i file
            self.copy_files_safely(file_list)

            # Aggiornamento completato
            self.progress_label.config(text="Aggiornamento completato con successo!")
            self.update_file_label("")

            # Chiedi all'utente se vuole riavviare l'applicazione
            if messagebox.askyesno("Riavvio", "Aggiornamento completato. Vuoi riavviare l'applicazione ora?"):
                new_exe_path = os.path.join(self.dest_path, self.exe_name)

                # Verifica che l'exe esista
                if not os.path.exists(new_exe_path):
                    raise FileNotFoundError(f"File eseguibile non trovato: {new_exe_path}")

                # Avvia il nuovo processo gestendo correttamente i percorsi con spazi
                if os.name == 'nt':  # Windows
                    subprocess.Popen(f'"{new_exe_path}"')
                else:  # Linux/Mac
                    subprocess.Popen([new_exe_path])

            self.destroy()

        except Exception as e:
            log(f"ERRORE CRITICO nell'updater: {e}")
            messagebox.showerror("Errore di Aggiornamento", f"Si è verificato un errore:\n{e}")
            self.destroy()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        log(f"Numero insufficiente di argomenti: {len(sys.argv)}")
        sys.exit(1)

    source = sys.argv[1]
    dest = sys.argv[2]
    exe = sys.argv[3]

    log(f"Avvio updater: source={source}, dest={dest}, exe={exe}")

    app = UpdateProgressWindow(source, dest, exe)
    app.mainloop()