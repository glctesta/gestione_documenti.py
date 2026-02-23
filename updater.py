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

    # ------------------------------------------------------------------ #
    #  Ticket automatico su eccezioni non gestite                          #
    # ------------------------------------------------------------------ #
    import traceback as _tb
    import json as _json
    import threading as _threading
    import datetime as _dt

    _TICKET_DIR = os.path.join(os.getenv("LOCALAPPDATA", "."), "TraceabilityRS", "tickets")
    _LOG_FILE = os.path.join(os.path.expanduser("~"), "Downloads", "maintenance_app_updater.log")

    def _get_log_tail(n=50):
        try:
            if not os.path.exists(_LOG_FILE):
                return "(log non trovato)"
            with open(_LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
                return "".join(f.readlines()[-n:])
        except Exception:
            return "(errore lettura log)"

    def _save_fallback_json(error_info):
        """Salva ticket su file JSON locale se l'email non e' disponibile."""
        try:
            os.makedirs(_TICKET_DIR, exist_ok=True)
            ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(_TICKET_DIR, f"updater_ticket_{ts}.json")
            with open(path, "w", encoding="utf-8") as f:
                _json.dump(error_info, f, ensure_ascii=False, indent=2)
            log(f"[TICKET] Ticket salvato localmente: {path}")
        except Exception as e:
            log(f"[TICKET] Impossibile salvare ticket JSON: {e}")

    def _send_email_alert(error_info):
        """Invia email di notifica ticket updater in background."""
        def _run():
            try:
                # email_connector e' nella stessa cartella dell'exe/script
                _script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
                sys.path.insert(0, _script_dir)
                from email_connector import EmailSender

                # Leggi destinatario (file credenziali locale)
                import pyodbc as _pyodbc  # noqa – solo per tentare lettura DB
                try:
                    # Prova a leggere l'email destinataria dal DB (best-effort)
                    from config_manager import ConfigManager
                    _cfg = ConfigManager()
                    _conn_str = _cfg.get_connection_string()
                    _conn = _pyodbc.connect(_conn_str, timeout=5)
                    _cur = _conn.cursor()
                    _cur.execute(
                        "SELECT [value] FROM traceability_rs.dbo.settingrs "
                        "WHERE Atribute = 'SysEmail_service_tickets'"
                    )
                    _row = _cur.fetchone()
                    recipient = str(_row[0]).strip() if _row and _row[0] else ""
                    _conn.close()
                except Exception:
                    recipient = ""

                if not recipient:
                    log("[TICKET] Nessuna email destinataria trovata per updater ticket.")
                    return

                sender = EmailSender()
                subject = f"[Ticket Updater] {error_info['type']}: {error_info['message'][:80]}"
                body = f"""<html><body style="font-family:Arial,sans-serif;font-size:13px;">
<h2 style="color:#B71C1C;">&#9888; Errore Updater – Ticket automatico</h2>
<table cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%;max-width:700px;">
  <tr><td style="font-weight:bold;width:120px;">Tipo errore</td><td style="color:#C62828;font-weight:bold;">{error_info['type']}</td></tr>
  <tr style="background:#F5F5F5;"><td style="font-weight:bold;">Messaggio</td><td>{error_info['message']}</td></tr>
  <tr><td style="font-weight:bold;">Data/Ora</td><td>{error_info['created_at']}</td></tr>
  <tr style="background:#F5F5F5;"><td style="font-weight:bold;">Sorgente</td><td>{error_info.get('source','N/A')}</td></tr>
  <tr><td style="font-weight:bold;">Destinazione</td><td>{error_info.get('dest','N/A')}</td></tr>
</table>
<h3 style="color:#C62828;">Stacktrace</h3>
<pre style="background:#FFF3E0;padding:10px;border-left:4px solid #C62828;font-size:11px;">{error_info['traceback']}</pre>
<h3 style="color:#2E7D32;">Log recente</h3>
<pre style="background:#E8F5E9;padding:10px;border-left:4px solid #2E7D32;font-size:10px;">{error_info['log_snippet']}</pre>
</body></html>"""

                sender.send_email(
                    to_email=recipient,
                    subject=subject,
                    body=body,
                    is_html=True
                )
                log(f"[TICKET] Email updater inviata a {recipient}")

            except Exception as e:
                log(f"[TICKET] Errore invio email updater: {e}")

        _threading.Thread(target=_run, daemon=True).start()

    def _on_updater_exception(exc_type, exc_value, exc_tb):
        """Intercetta eccezioni non gestite nell'updater e crea un ticket."""
        error_info = {
            'type':       exc_type.__name__,
            'message':    str(exc_value),
            'traceback':  ''.join(_tb.format_tb(exc_tb)),
            'log_snippet': _get_log_tail(50),
            'created_at': _dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'source':     source,
            'dest':       dest,
            'exe':        exe
        }
        log(f"[TICKET] Eccezione non gestita: {exc_value}")
        # 1. Salva localmente (sempre, anche senza rete)
        _save_fallback_json(error_info)
        # 2. Tenta invio email in background
        _send_email_alert(error_info)
        # 3. Mostra dialog all'utente e aspetta l'email
        try:
            messagebox.showerror(
                "Errore Updater",
                f"Si è verificato un errore imprevisto:\n\n"
                f"{exc_type.__name__}: {exc_value}\n\n"
                "Il ticket è stato registrato automaticamente.\n"
                "Il team tecnico riceverà una notifica via email."
            )
        except Exception:
            pass

    sys.excepthook = _on_updater_exception
    # ------------------------------------------------------------------ #

    app = UpdateProgressWindow(source, dest, exe)
    app.mainloop()
