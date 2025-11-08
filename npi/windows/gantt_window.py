# npi/windows/gantt_window.py

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import plotly.express as px
import webbrowser
import os
import logging

logger = logging.getLogger(__name__)


class NpiGanttWindow(tk.Toplevel):
    """
    Finestra che genera e visualizza un diagramma di Gantt per un progetto NPI.
    """

    def __init__(self, master, npi_manager, lang, progetto_id: int, **kwargs):
        super().__init__(master, **kwargs)
        self.npi_manager = npi_manager
        self.lang = lang
        self.progetto_id = progetto_id

        self.progetto_dettagli = self.npi_manager.get_dettagli_progetto(self.progetto_id)
        if not self.progetto_dettagli:
            messagebox.showerror("Errore", f"Progetto con ID {self.progetto_id} non trovato.", parent=self)
            self.destroy()
            return

        titolo = self.lang.get('npi_gantt_title', 'Gantt Progetto NPI')
        self.title(f"{titolo} - {self.progetto_dettagli.prodotto.NomeProdotto}")
        self.geometry("800x200")  # Finestra minima, l'azione principale è aprire il browser

        self.create_widgets()
        self.generate_and_open_gantt()

    def create_widgets(self):
        """Crea i widget di base."""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        label = ttk.Label(main_frame,
                          text=self.lang.get('gantt_opening_message', 'Generazione del diagramma di Gantt in corso...'),
                          font=("Calibri", 12))
        label.pack(pady=10)

        open_button = ttk.Button(main_frame, text=self.lang.get('gantt_reopen', 'Apri di nuovo nel Browser'),
                                 command=self.generate_and_open_gantt)
        open_button.pack(pady=10)

    def generate_and_open_gantt(self):
        """
        Recupera i dati, genera il file HTML con Plotly e lo apre.
        """
        try:
            gantt_data, product_name = self.npi_manager.get_gantt_data(self.progetto_id)
            if not gantt_data:
                messagebox.showinfo(
                    "Info",
                    "Nessun task assegnato con date pianificate da visualizzare per questo progetto.",
                    parent=self
                )
                return

            # Crea esplicitamente il DataFrame con i dati
            df = pd.DataFrame(gantt_data)

            # DEBUG: Stampa le colonne disponibili per verificare
            print(f"DEBUG: Colonne disponibili nel DataFrame: {df.columns.tolist()}")
            print(f"DEBUG: Numero di task nel Gantt: {len(df)}")

            # Verifica che le colonne necessarie esistano
            required_columns = ['Task', 'Start', 'Finish', 'Owner']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Colonne mancanti nel DataFrame: {missing_columns}")

            # Crea il Gantt con i nomi di colonna corretti
            fig = px.timeline(
                df,
                x_start="Start",
                x_end="Finish",
                y="Task",
                color="Owner",
                title=f"Gantt per {product_name} - Task Assegnati",
            )
            fig.update_yaxes(autorange="reversed")

            # Aggiunge informazioni hover
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br>Assegnato a: %{color}<br>Inizio: %{base|%d/%m/%Y}<br>Fine: %{x|%d/%m/%Y}<extra></extra>'
            )

            # Salva in un file HTML temporaneo
            file_path = os.path.join(os.path.expanduser("~"), "temp_npi_gantt.html")
            fig.write_html(file_path)

            # Apre il file nel browser
            webbrowser.open(f'file://{os.path.realpath(file_path)}')
            logger.info(f"Gantt per progetto {self.progetto_id} generato e aperto in {file_path}")

        except Exception as e:
            logger.error(f"Errore nella generazione del Gantt per progetto {self.progetto_id}: {e}", exc_info=True)
            messagebox.showerror("Errore Gantt", f"Impossibile generare il diagramma:\n{e}", parent=self)