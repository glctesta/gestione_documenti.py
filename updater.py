import sys
import os
import shutil
import subprocess
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ------------------------------------------------------------------ #
#  Percorso log centralizzato (nella stessa dir del programma padre)  #
# ------------------------------------------------------------------ #
_LOG_DIR = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local")),
    "TraceabilityRS", "logs"
)
os.makedirs(_LOG_DIR, exist_ok=True)
_LOG_FILE = os.path.join(_LOG_DIR, "updater.log")


def log(message):
    try:
        with open(_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}: {message}\n")
            f.flush()
    except Exception as e:
        print(f"Failed to write to log: {e}")


class UpdateProgressWindow(tk.Tk):
    """Finestra grafica per mostrare il progresso dell'aggiornamento."""

    def __init__(self, source_path, dest_path, exe_name):
        super().__init__()

        self.source_path = source_path
        self.dest_path = dest_path
        self.exe_name = exe_name

        # Variabile tkinter per aggiornamenti thread-safe
        self._file_var = tk.StringVar(value="")
        self._cancelled = False

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
        file_frame.pack_propagate(False)

        # Label per il nome del file — usa StringVar per aggiornamenti da altri thread
        self.file_label = ttk.Label(
            file_frame,
            textvariable=self._file_var,
            font=("Helvetica", 8),
            foreground="grey",
            anchor="w",
            width=80
        )
        self.file_label.pack(fill='x')

        # Avvia l'aggiornamento dopo un breve delay
        self.after(500, self.start_update)

        # Impedisce la chiusura manuale durante la copia
        self.protocol("WM_DELETE_WINDOW", self._on_close_requested)

    def _on_close_requested(self):
        """Impedisce la chiusura della finestra durante la copia."""
        if not self._cancelled:
            messagebox.showwarning(
                "Operazione in corso",
                "L'aggiornamento è in corso. Attendere il completamento."
            )

    def _set_progress(self, value, file_text=""):
        """Aggiorna la barra di progresso e il testo del file (thread-safe via after)."""
        self.progress_bar["value"] = value
        self._file_var.set(file_text)

    # File da NON sovrascrivere (configurazioni locali + DLL di runtime bloccate dal processo)
    PRESERVE_FILES = {
        'updater.exe',
        'printer_config.json',
        'user_settings.json',
        'vcruntime140.dll',
        'vcruntime140_1.dll',
    }

    def _copy_worker(self, file_list):
        """
        Worker eseguito in un thread separato.
        NON chiama mai direttamente widget tkinter — usa self.after() come ponte.
        """
        errors = []
        total = len(file_list)
        log(f"_copy_worker: avvio copia di {total} file")

        for i, (root, name) in enumerate(file_list):
            # Aggiorna la GUI tramite after (thread-safe)
            self.after(0, self._set_progress, i + 1, f"Copia di: {name}")

            # Log periodico ogni 50 file
            if (i + 1) % 50 == 0:
                log(f"_copy_worker: progresso {i + 1}/{total}")

            # Salta file di configurazione locale che non devono essere sovrascritti
            if name.lower() in self.PRESERVE_FILES:
                log(f"Preservato file locale: {name}")
                continue

            try:
                source_file = os.path.join(root, name)
                relative_path = os.path.relpath(root, self.source_path)
                dest_dir = os.path.join(self.dest_path, relative_path)

                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, name)

                # Retry in caso di PermissionError (file temporaneamente in uso)
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        shutil.copy2(source_file, dest_file)
                        break
                    except PermissionError:
                        if attempt < max_retries - 1:
                            log(f"PermissionError su {name}, tentativo {attempt + 1}/{max_retries}")
                            time.sleep(1)
                        else:
                            raise

            except Exception as e:
                msg = f"Errore nella copia di {name}: {e}"
                log(msg)
                errors.append(msg)

        log(f"_copy_worker: copia completata. {total - len(errors)} OK, {len(errors)} errori")
        # Al termine notifica il thread principale
        self.after(0, self._on_copy_done, errors)

    def _on_copy_done(self, errors):
        """Chiamata dal thread principale al termine della copia."""
        self._cancelled = True  # Permette ora la chiusura della finestra

        if errors:
            error_summary = "\n".join(errors[:10])
            if len(errors) > 10:
                error_summary += f"\n... e altri {len(errors) - 10} errori (vedi log)"
            log(f"Aggiornamento completato con {len(errors)} errori.")
            messagebox.showwarning(
                "Aggiornamento con errori",
                f"Aggiornamento completato con {len(errors)} file non copiati:\n\n{error_summary}\n\nControlla il log per i dettagli."
            )
        else:
            log("Aggiornamento completato con successo.")

        self.progress_label.config(text="Aggiornamento completato con successo!")
        self._file_var.set("")

        if messagebox.askyesno("Riavvio", "Aggiornamento completato. Vuoi riavviare l'applicazione ora?"):
            new_exe_path = os.path.join(self.dest_path, self.exe_name)

            if not os.path.exists(new_exe_path):
                messagebox.showerror(
                    "File non trovato",
                    f"Impossibile avviare l'applicazione:\n{new_exe_path}"
                )
                log(f"EXE non trovato dopo l'aggiornamento: {new_exe_path}")
            else:
                log(f"Avvio dell'applicazione: {new_exe_path}")
                # Usa lista invece di stringa per gestire correttamente i path con spazi
                subprocess.Popen([new_exe_path], shell=False)

        self.destroy()

    def start_update(self):
        """Attende la chiusura dell'app principale poi avvia il thread di copia."""
        log("start_update: attesa 2 secondi per chiusura app principale...")
        self.after(2000, self._perform_update)

    def _perform_update(self):
        """Verifica le directory e lancia il worker in un thread separato."""
        try:
            log(f"_perform_update: verifica source_path='{self.source_path}'")

            if not os.path.exists(self.source_path):
                raise FileNotFoundError(f"Directory sorgente non trovata: {self.source_path}")

            log(f"_perform_update: source_path esiste. Verifica dest_path='{self.dest_path}'")

            if not os.path.exists(self.dest_path):
                os.makedirs(self.dest_path, exist_ok=True)

            log("_perform_update: inizio scansione file (os.walk)...")

            # Crea la lista dei file da copiare
            file_list = []
            for root, _, files in os.walk(self.source_path):
                for name in files:
                    file_list.append((root, name))

            log(f"_perform_update: scansione completata, trovati {len(file_list)} file")

            if not file_list:
                raise Exception("Nessun file trovato nella directory sorgente")

            log(f"Inizio copia di {len(file_list)} file da '{self.source_path}' a '{self.dest_path}'")

            self.progress_bar["maximum"] = len(file_list)
            self.progress_bar["value"] = 0

            # Avvia la copia in un thread separato per non bloccare la GUI
            t = threading.Thread(target=self._copy_worker, args=(file_list,), daemon=True)
            t.start()
            log("_perform_update: thread di copia avviato")

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
    import datetime as _dt

    _TICKET_DIR = os.path.join(os.getenv("LOCALAPPDATA", "."), "TraceabilityRS", "tickets")

    def _get_log_tail(n=50):
        try:
            if not os.path.exists(_LOG_FILE):
                return "(log non trovato)"
            with open(_LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
                return "".join(f.readlines()[-n:])
        except Exception:
            return "(errore lettura log)"

    def _save_fallback_json(error_info):
        """Salva ticket su file JSON locale se l'email non è disponibile."""
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
                _script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
                sys.path.insert(0, _script_dir)
                from email_connector import EmailSender

                import pyodbc as _pyodbc
                try:
                    from config_manager import ConfigManager
                    _cfg = ConfigManager()
                    _conn_str = _cfg.get_connection_string()
                    _conn = _pyodbc.connect(_conn_str, timeout=5)
                    _cur = _conn.cursor()
                    _cur.execute(
                        "SELECT [value] FROM traceability_rs.dbo.settings "
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

        threading.Thread(target=_run, daemon=True).start()

    def _on_updater_exception(exc_type, exc_value, exc_tb):
        """Intercetta eccezioni non gestite nell'updater e crea un ticket."""
        error_info = {
            'type':        exc_type.__name__,
            'message':     str(exc_value),
            'traceback':   ''.join(_tb.format_tb(exc_tb)),
            'log_snippet': _get_log_tail(50),
            'created_at':  _dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'source':      source,
            'dest':        dest,
            'exe':         exe
        }
        log(f"[TICKET] Eccezione non gestita: {exc_value}")
        _save_fallback_json(error_info)
        _send_email_alert(error_info)
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
