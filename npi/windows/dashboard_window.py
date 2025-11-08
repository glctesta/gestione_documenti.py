# File: npi/windows/dashboard_window.py (CODICE CORRETTO)

import tkinter as tk
from tkinter import ttk, messagebox
from .project_window import ProjectWindow
from .gantt_window import NpiGanttWindow


class NpiDashboardWindow(tk.Toplevel):
    def __init__(self, master, npi_manager, lang):
        super().__init__(master)
        self.npi_manager = npi_manager
        self.lang = lang

        self.title(self.lang.get('npi_dashboard_title', "Dashboard Progetti NPI"))
        self.geometry("1000x500")
        self.transient(master)
        self.grab_set()

        self._create_widgets()
        self.load_npi_projects()

        # Bind per doppio click
        self.project_tree.bind('<Double-1>', self._on_double_click)

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('active_npi_projects', "Progetti NPI Attivi"),
                                    padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)

        cols = ('ID', 'Codice Prodotto', 'Nome Prodotto', 'Stato Progetto')
        self.project_tree = ttk.Treeview(list_frame, columns=cols, show='headings', selectmode='browse')

        self.project_tree.heading('ID', text=self.lang.get('col_id', 'ID'))
        self.project_tree.column('ID', width=60, anchor=tk.CENTER)
        self.project_tree.heading('Codice Prodotto', text=self.lang.get('col_product_code', 'Codice Prodotto'))
        self.project_tree.column('Codice Prodotto', width=150)
        self.project_tree.heading('Nome Prodotto', text=self.lang.get('col_product_name', 'Nome Prodotto'))
        self.project_tree.column('Nome Prodotto', width=300)
        self.project_tree.heading('Stato Progetto', text=self.lang.get('col_project_status', 'Stato'))
        self.project_tree.column('Stato Progetto', width=120)

        self.project_tree.pack(fill=tk.BOTH, expand=True)

        self.project_tree.bind("<Button-3>", self._show_project_context_menu)

        button_frame = ttk.Frame(main_frame, padding=(0, 10, 0, 0))
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text=self.lang.get('btn_refresh', 'Aggiorna'), command=self.load_npi_projects).pack(
            side=tk.LEFT)
        ttk.Button(button_frame, text=self.lang.get('btn_close', 'Chiudi'), command=self.destroy).pack(side=tk.RIGHT)

    def _on_double_click(self, event):
        """Gestisce il doppio click su un progetto"""
        self._launch_project_window()

    def load_npi_projects(self):
        for i in self.project_tree.get_children():
            self.project_tree.delete(i)

        try:
            progetti = self.npi_manager.get_progetti_attivi()
            print(f"DEBUG: Numero progetti attivi trovati: {len(progetti)}")

            if not progetti:
                self.project_tree.insert('', tk.END, values=("-", self.lang.get('no_active_projects',
                                                                                "Nessun progetto attivo trovato."), "",
                                                             ""))
                return

            for proj in progetti:
                print(
                    f"DEBUG: Progetto ID={proj.ProgettoID}, Prodotto={proj.prodotto.NomeProdotto if proj.prodotto else 'Nessuno'}")
                if proj.prodotto:
                    self.project_tree.insert(
                        '', tk.END,
                        values=(
                            proj.ProgettoID,
                            proj.prodotto.CodiceProdotto or "",
                            proj.prodotto.NomeProdotto,
                            proj.StatoProgetto
                        )
                    )
        except Exception as e:
            print(f"DEBUG: Errore nel caricamento progetti: {e}")
            self.project_tree.insert('', tk.END, values=("Errore", "Impossibile caricare i dati.", str(e), ""))

    def _show_project_context_menu(self, event):
        iid = self.project_tree.identify_row(event.y)
        if not iid:
            return

        # Controlla se è una riga di errore o vuota
        item_values = self.project_tree.item(iid, 'values')
        if not item_values or item_values[0] in ("-", "Errore"):
            return

        self.project_tree.selection_set(iid)
        context_menu = tk.Menu(self, tearoff=0)

        context_menu.add_command(
            label=self.lang.get('manage_project', "Gestisci Progetto..."),
            command=self._launch_project_window
        )
        context_menu.add_command(
            label=self.lang.get('npi_view_gantt', "Visualizza Gantt..."),
            command=self._launch_gantt_window
        )

        context_menu.post(event.x_root, event.y_root)

    def _launch_project_window(self):
        """Apre la finestra di gestione del progetto selezionato."""
        selection = self.project_tree.selection()
        if not selection:
            messagebox.showwarning("Selezione", "Seleziona un progetto dalla lista.", parent=self)
            return

        item_values = self.project_tree.item(selection[0], 'values')
        print(f"DEBUG: item_values = {item_values}")

        if not item_values or item_values[0] in ("-", "Errore"):
            messagebox.showwarning("Selezione", "Seleziona un progetto valido dalla lista.", parent=self)
            return

        try:
            project_id = int(item_values[0])
            print(f"DEBUG: project_id convertito = {project_id}")

            def open_project_action():
                print(f"DEBUG: Dentro open_project_action, project_id = {project_id}")
                win = ProjectWindow(self, self.npi_manager, self.lang, project_id)
                self.wait_window(win)
                self.load_npi_projects()

            # SOLO UNA CHIAMATA - attraverso l'autorizzazione
            self.master._execute_authorized_action(
                menu_translation_key='project_window',
                action_callback=open_project_action
            )

        except (ValueError, Exception) as e:
            print(f"DEBUG ERROR: {e}")
            messagebox.showerror("Errore", f"Impossibile aprire la finestra di gestione: {e}", parent=self)


    def _launch_gantt_window(self):
        """Apre la finestra Gantt per il progetto selezionato."""
        selection = self.project_tree.selection()
        if not selection:
            messagebox.showwarning("Selezione", "Seleziona un progetto dalla lista.", parent=self)
            return

        item_values = self.project_tree.item(selection[0], 'values')
        if not item_values or item_values[0] in ("-", "Errore"):
            messagebox.showwarning("Selezione", "Seleziona un progetto valido dalla lista.", parent=self)
            return

        try:
            project_id = int(item_values[0])
            print(f"DEBUG: Apertura Gantt per progetto ID: {project_id}")
            NpiGanttWindow(self, self.npi_manager, self.lang, project_id)
        except (ValueError, Exception) as e:
            messagebox.showerror("Errore", f"Impossibile aprire la finestra Gantt: {e}", parent=self)