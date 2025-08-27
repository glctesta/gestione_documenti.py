# updater.py
import sys
import os
import shutil
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def log(message):
    """Scrive un messaggio in un file di log per il debug."""
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

        self.progress_label = ttk.Label(self, text="Aggiornamento in corso, attendere...", font=("Helvetica", 10))
        self.progress_label.pack(pady=(15, 5))

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=5)

        self.file_label = ttk.Label(self, text="", font=("Helvetica", 8), foreground="grey")
        self.file_label.pack(pady=5)

        self.after(200, self.start_update)

    def start_update(self):
        try:
            log("Updater grafico avviato.")
            time.sleep(2)

            file_list = []
            for root, _, files in os.walk(self.source_path):
                for name in files:
                    file_list.append((root, name))

            self.progress_bar["maximum"] = len(file_list)

            for i, (root, name) in enumerate(file_list):
                # --- CORREZIONE QUI ---
                # Salta la copia del file updater.exe per evitare l'errore di permesso
                if name.lower() == 'updater.exe':
                    self.progress_bar["value"] = i + 1
                    self.update_idletasks()
                    continue  # Salta al prossimo file
                # --- FINE CORREZIONE ---

                self.file_label.config(text=f"Copia di: {name}")

                source_file = os.path.join(root, name)
                relative_path = os.path.relpath(root, self.source_path)
                dest_dir = os.path.join(self.dest_path, relative_path)

                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy2(source_file, dest_dir)

                self.progress_bar["value"] = i + 1
                self.update_idletasks()

            self.progress_label.config(text="Aggiornamento completato con successo!")
            self.file_label.config(text="")
            log("Copia file completata.")

            if messagebox.askyesno("Riavvio", "Aggiornamento completato. Vuoi riavviare l'applicazione ora?"):
                new_exe_path = os.path.join(self.dest_path, self.exe_name)
                log(f"Rilancio di {new_exe_path}...")
                subprocess.Popen([new_exe_path])

            self.destroy()

        except Exception as e:
            log(f"ERRORE CRITICO nell'updater: {e}")
            messagebox.showerror("Errore di Aggiornamento", f"Si è verificato un errore:\n{e}")
            self.destroy()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: updater.exe <percorso_sorgente> <percorso_destinazione> <nome_eseguibile>")
        sys.exit(1)

    source = sys.argv[1]
    dest = sys.argv[2]
    exe = sys.argv[3]

    app = UpdateProgressWindow(source, dest, exe)
    app.mainloop()