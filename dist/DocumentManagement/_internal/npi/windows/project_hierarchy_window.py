# File: npi/windows/project_hierarchy_window.py
"""
Finestra dedicata alla gestione della gerarchia progetti NPI (Parent-Child).
Il progetto aperto è sempre il PADRE, e questa finestra permette di:
- Visualizzare i figli già assegnati
- Aggiungere nuovi figli (progetti dello stesso cliente)
- Rimuovere figli esistenti
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)


class ProjectHierarchyWindow(tk.Toplevel):
    """Finestra per gestire la gerarchia progetti (assegnazione figli al progetto padre)."""
    
    def __init__(self, parent, npi_manager, lang, parent_project_id, parent_project_name, parent_client):
        """
        Args:
            parent: Finestra padre
            npi_manager: Gestore NPI
            lang: Gestore traduzioni
            parent_project_id: ID del progetto PADRE (fisso)
            parent_project_name: Nome del progetto padre
            parent_client: Cliente del progetto padre
        """
        super().__init__(parent)
        self.npi_manager = npi_manager
        self.lang = lang
        self.parent_project_id = parent_project_id
        self.parent_project_name = parent_project_name
        self.parent_client = parent_client
        
        self.title(f"Gerarchia Progetto: {parent_project_name}")
        self.geometry("900x800")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._load_data()
    
    def _create_widgets(self):
        """Crea l'interfaccia utente."""
        # Header
        header_frame = ttk.Frame(self, padding=10)
        header_frame.pack(fill=tk.X)
        
        ttk.Label(
            header_frame,
            text=f"🔗 Gestione Gerarchia Progetto",
            font=('Helvetica', 14, 'bold')
        ).pack()
        
        ttk.Label(
            header_frame,
            text=f"Progetto Padre: {self.parent_project_name}",
            font=('Helvetica', 11, 'bold'),
            foreground="blue"
        ).pack(pady=5)
        
        ttk.Label(
            header_frame,
            text=f"Cliente: {self.parent_client} | ID Progetto: {self.parent_project_id}",
            font=('Helvetica', 9),
            foreground="gray"
        ).pack()
        
        # Separator
        ttk.Separator(self, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Main content
        content_frame = ttk.Frame(self, padding=10)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # === SEZIONE FIGLI ASSEGNATI ===
        assigned_frame = ttk.LabelFrame(
            content_frame,
            text="✅ Progetti Figli Assegnati",
            padding=10
        )
        assigned_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview figli assegnati
        tree_frame = ttk.Frame(assigned_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'nome', 'stato', 'data_inizio', 'scadenza')
        self.assigned_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.assigned_tree.heading('id', text='ID')
        self.assigned_tree.heading('nome', text='Nome Progetto')
        self.assigned_tree.heading('stato', text='Stato')
        self.assigned_tree.heading('data_inizio', text='Data Inizio')
        self.assigned_tree.heading('scadenza', text='Scadenza')
        
        self.assigned_tree.column('id', width=50)
        self.assigned_tree.column('nome', width=300)
        self.assigned_tree.column('stato', width=120)
        self.assigned_tree.column('data_inizio', width=100)
        self.assigned_tree.column('scadenza', width=100)
        
        scrollbar_assigned = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.assigned_tree.yview)
        self.assigned_tree.configure(yscrollcommand=scrollbar_assigned.set)
        
        self.assigned_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_assigned.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottoni per figli assegnati
        btn_frame_assigned = ttk.Frame(assigned_frame)
        btn_frame_assigned.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            btn_frame_assigned,
            text="❌ Rimuovi Figlio",
            command=self._remove_child
        ).pack(side=tk.LEFT, padx=5)
        
        self.assigned_count_label = ttk.Label(
            btn_frame_assigned,
            text="Figli assegnati: 0",
            foreground="green"
        )
        self.assigned_count_label.pack(side=tk.RIGHT, padx=5)
        
        # === SEZIONE PROGETTI DISPONIBILI ===
        available_frame = ttk.LabelFrame(
            content_frame,
            text="📋 Progetti Disponibili (stesso cliente, non già padri)",
            padding=10
        )
        available_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview progetti disponibili
        tree_frame_avail = ttk.Frame(available_frame)
        tree_frame_avail.pack(fill=tk.BOTH, expand=True)
        
        self.available_tree = ttk.Treeview(tree_frame_avail, columns=columns, show='headings', selectmode='browse')
        
        self.available_tree.heading('id', text='ID')
        self.available_tree.heading('nome', text='Nome Progetto')
        self.available_tree.heading('stato', text='Stato')
        self.available_tree.heading('data_inizio', text='Data Inizio')
        self.available_tree.heading('scadenza', text='Scadenza')
        
        self.available_tree.column('id', width=50)
        self.available_tree.column('nome', width=300)
        self.available_tree.column('stato', width=120)
        self.available_tree.column('data_inizio', width=100)
        self.available_tree.column('scadenza', width=100)
        
        scrollbar_avail = ttk.Scrollbar(tree_frame_avail, orient=tk.VERTICAL, command=self.available_tree.yview)
        self.available_tree.configure(yscrollcommand=scrollbar_avail.set)
        
        self.available_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_avail.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottoni per progetti disponibili
        btn_frame_avail = ttk.Frame(available_frame)
        btn_frame_avail.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            btn_frame_avail,
            text="➕ Aggiungi come Figlio",
            command=self._add_child
        ).pack(side=tk.LEFT, padx=5)
        
        self.available_count_label = ttk.Label(
            btn_frame_avail,
            text="Disponibili: 0",
            foreground="blue"
        )
        self.available_count_label.pack(side=tk.RIGHT, padx=5)
        
        # === BOTTONI FINALI ===
        bottom_frame = ttk.Frame(self, padding=10)
        bottom_frame.pack(fill=tk.X)
        
        ttk.Button(
            bottom_frame,
            text="🔄 Aggiorna",
            command=self._load_data
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            bottom_frame,
            text="Chiudi",
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _load_data(self):
        """Carica i dati: figli assegnati e progetti disponibili."""
        self._load_assigned_children()
        self._load_available_projects()
    
    def _load_assigned_children(self):
        """Carica i progetti figli già assegnati a questo padre."""
        try:
            # Pulisci treeview
            for item in self.assigned_tree.get_children():
                self.assigned_tree.delete(item)
            
            # Recupera figli
            children = self.npi_manager.get_child_projects(self.parent_project_id)
            
            
            for child in children:
                # 🔄 Fallback per nome progetto
                if child.NomeProgetto:
                    nome_display = child.NomeProgetto
                elif hasattr(child, 'prodotto') and child.prodotto:
                    # Usa nome prodotto o codice prodotto come fallback
                    if child.prodotto.NomeProdotto:
                        nome_display = f"{child.prodotto.NomeProdotto} (Prog.{child.ProgettoId})"
                    elif child.prodotto.CodiceProdotto:
                        nome_display = f"{child.prodotto.CodiceProdotto} (Prog.{child.ProgettoId})"
                    else:
                        nome_display = f"Progetto ID {child.ProgettoId}"
                else:
                    nome_display = f"Progetto ID {child.ProgettoId}"
                
                data_inizio = child.DataInizio.strftime('%d/%m/%Y') if child.DataInizio else ''
                scadenza = child.ScadenzaProgetto.strftime('%d/%m/%Y') if child.ScadenzaProgetto else ''
                
                self.assigned_tree.insert('', tk.END, values=(
                    child.ProgettoId,
                    nome_display,
                    child.StatoProgetto or '',
                    data_inizio,
                    scadenza
                ))
            
            # Aggiorna contatore
            self.assigned_count_label.config(text=f"Figli assegnati: {len(children)}")
            
        except Exception as e:
            logger.error(f"Errore caricamento figli assegnati: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile caricare i figli assegnati:\n{e}", parent=self)
    
    def _load_available_projects(self):
        """Carica i progetti che possono diventare figli di questo padre."""
        try:
            # Pulisci treeview
            for item in self.available_tree.get_children():
                self.available_tree.delete(item)
            
            # Recupera progetti disponibili
            available = self.npi_manager.get_available_child_projects(
                self.parent_project_id,
                self.parent_client
            )
            
            
            for proj in available:
                # 🔄 Fallback per nome progetto
                if proj.NomeProgetto:
                    nome_display = proj.NomeProgetto
                elif hasattr(proj, 'prodotto') and proj.prodotto:
                    # Usa nome prodotto o codice prodotto come fallback
                    if proj.prodotto.NomeProdotto:
                        nome_display = f"{proj.prodotto.NomeProdotto} (Prog.{proj.ProgettoId})"
                    elif proj.prodotto.CodiceProdotto:
                        nome_display = f"{proj.prodotto.CodiceProdotto} (Prog.{proj.ProgettoId})"
                    else:
                        nome_display = f"Progetto ID {proj.ProgettoId}"
                else:
                    nome_display = f"Progetto ID {proj.ProgettoId}"
                
                data_inizio = proj.DataInizio.strftime('%d/%m/%Y') if proj.DataInizio else ''
                scadenza = proj.ScadenzaProgetto.strftime('%d/%m/%Y') if proj.ScadenzaProgetto else ''
                
                self.available_tree.insert('', tk.END, values=(
                    proj.ProgettoId,
                    nome_display,
                    proj.StatoProgetto or '',
                    data_inizio,
                    scadenza
                ))
            
            # Aggiorna contatore
            self.available_count_label.config(text=f"Disponibili: {len(available)}")
            
        except Exception as e:
            logger.error(f"Errore caricamento progetti disponibili: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile caricare i progetti disponibili:\n{e}", parent=self)
    
    def _add_child(self):
        """Aggiunge il progetto selezionato come figlio del padre."""
        selection = self.available_tree.selection()
        if not selection:
            messagebox.showwarning(
                "Attenzione",
                "Seleziona un progetto da aggiungere come figlio.",
                parent=self
            )
            return
        
        # Ottieni ID progetto selezionato
        item = self.available_tree.item(selection[0])
        child_id = item['values'][0]
        child_name = item['values'][1]
        
        # Conferma
        if not messagebox.askyesno(
            "Conferma",
            f"Vuoi aggiungere '{child_name}' come figlio di '{self.parent_project_name}'?",
            parent=self
        ):
            return
        
        try:
            # Assegna figlio
            self.npi_manager.assign_child_project(self.parent_project_id, child_id)
            
            messagebox.showinfo(
                "Successo",
                f"Progetto '{child_name}' aggiunto come figlio!",
                parent=self
            )
            
            # Ricarica dati
            self._load_data()
            
        except Exception as e:
            logger.error(f"Errore assegnazione figlio: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile assegnare il figlio:\n{e}", parent=self)
    
    def _remove_child(self):
        """Rimuove il figlio selezionato (setta ParentProjectID = NULL)."""
        selection = self.assigned_tree.selection()
        if not selection:
            messagebox.showwarning(
                "Attenzione",
                "Seleziona un progetto figlio da rimuovere.",
                parent=self
            )
            return
        
        # Ottieni ID progetto selezionato
        item = self.assigned_tree.item(selection[0])
        child_id = item['values'][0]
        child_name = item['values'][1]
        
        # Conferma
        if not messagebox.askyesno(
            "Conferma",
            f"Vuoi rimuovere '{child_name}' dai figli di '{self.parent_project_name}'?",
            parent=self
        ):
            return
        
        try:
            # Rimuovi figlio
            self.npi_manager.remove_child_project(child_id)
            
            messagebox.showinfo(
                "Successo",
                f"Progetto '{child_name}' rimosso dai figli!",
                parent=self
            )
            
            # Ricarica dati
            self._load_data()
            
        except Exception as e:
            logger.error(f"Errore rimozione figlio: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile rimuovere il figlio:\n{e}", parent=self)
