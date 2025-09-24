import sys
import os
import shutil
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def log(message):
    # ... (funzione di log invariata)
    pass


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
            foreground="grey"
        )
        self.file_label.pack(anchor='center')

        self.after(200, self.start_update)

    def update_file_label(self, text):
        """Aggiorna il testo della label del file in modo pulito"""
        self.file_label.configure(text=text)
        self.update_idletasks()

    def start_update(self):
        try:
            time.sleep(2)

            # Crea la lista dei file da copiare
            file_list = []
            for root, _, files in os.walk(self.source_path):
                for name in files:
                    file_list.append((root, name))

            self.progress_bar["maximum"] = len(file_list)

            for i, (root, name) in enumerate(file_list):
                # Aggiorna il nome del file corrente
                self.update_file_label(f"Copia di: {name}")

                if name.lower() == 'updater.exe':
                    self.progress_bar["value"] = i + 1
                    continue

                # Copia il file
                source_file = os.path.join(root, name)
                relative_path = os.path.relpath(root, self.source_path)
                dest_dir = os.path.join(self.dest_path, relative_path)

                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy2(source_file, dest_dir)

                # Aggiorna la barra di progresso
                self.progress_bar["value"] = i + 1

            # Aggiornamento completato
            self.progress_label.config(text="Aggiornamento completato con successo!")
            self.update_file_label("")  # Pulisce la label del file

            # Chiedi all'utente se vuole riavviare l'applicazione
            if messagebox.askyesno("Riavvio", "Aggiornamento completato. Vuoi riavviare l'applicazione ora?"):
                new_exe_path = os.path.join(self.dest_path, self.exe_name)
                subprocess.Popen([new_exe_path])

            self.destroy()

        except Exception as e:
            log(f"ERRORE CRITICO nell'updater: {e}")
            messagebox.showerror("Errore di Aggiornamento", f"Si è verificato un errore:\n{e}")
            self.destroy()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(1)

    source = sys.argv[1]
    dest = sys.argv[2]
    exe = sys.argv[3]

    app = UpdateProgressWindow(source, dest, exe)
    app.mainloop()
