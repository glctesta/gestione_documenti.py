import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)


class ImportTasksWindow(tk.Toplevel):
    def __init__(self, master, npi_manager, lang, target_project_id):
        super().__init__(master)
        self.npi_manager = npi_manager
        self.lang = lang
        self.target_project_id = target_project_id

        self.title(self.lang.get('import_tasks_window_title', 'Importa Assegnamenti Task'))
        self.geometry("700x500")
        self.transient(master)
        self.grab_set()

        self._create_widgets()
        self._load_projects()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame,
                  text=self.lang.get('select_source_project', 'Seleziona un progetto da cui copiare gli assegnamenti:'),
                  wraplength=650).pack(pady=(0, 10))

        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        cols = ('product_code', 'product_name')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', selectmode='browse')
        self.tree.heading('product_code', text=self.lang.get('col_product_code', 'Codice Prodotto'))
        self.tree.heading('product_name', text=self.lang.get('col_product_name', 'Nome Prodotto'))
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(button_frame, text=self.lang.get('btn_confirm_import', 'Conferma e Copia'),
                   command=self._confirm_selection).pack(side=tk.LEFT)
        ttk.Button(button_frame, text=self.lang.get('btn_cancel', 'Annulla'), command=self.destroy).pack(side=tk.RIGHT)

    def _load_projects(self):
        try:
            progetti = self.npi_manager.get_all_npi_projects()
            for proj in progetti:
                # Escludi il progetto corrente dalla lista
                if proj.ProgettoId == self.target_project_id:
                    continue

                if proj.prodotto:
                    self.tree.insert('', tk.END, text=str(proj.ProgettoId),
                                     values=(proj.prodotto.CodiceProdotto or "", proj.prodotto.NomeProdotto))
        except Exception as e:
            messagebox.showerror(self.lang.get('error_title'), f"Errore nel caricamento progetti: {e}", parent=self)
            self.destroy()

    def _confirm_selection(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(self.lang.get('warning_title'),
                                   self.lang.get('import_no_selection_error', 'Nessun progetto selezionato.'),
                                   parent=self)
            return

        source_project_id = int(self.tree.item(selection[0], 'text'))

        try:
            updated_count = self.npi_manager.copy_tasks_from_project(source_project_id, self.target_project_id)
            messagebox.showinfo(self.lang.get('success_title'), self.lang.get('import_success',
                                                                              f'Operazione completata! Sono stati aggiornati {updated_count} task.'),
                                parent=self)
            self.destroy()
        except Exception as e:
            logger.error(f"Errore durante la conferma dell'import: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error_title'),
                                 self.lang.get('import_failed_error', f'Copia fallita: {e}'), parent=self)