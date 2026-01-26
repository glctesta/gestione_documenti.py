"""
Viewer per visualizzare e aprire i report FAI salvati nel database
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import tempfile
import os
import subprocess
import logging

logger = logging.getLogger(__name__)


class FaiReportsViewerWindow(tk.Toplevel):
    """Finestra per visualizzare e aprire report FAI salvati"""
    
    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        
        self.db = db
        self.lang = lang
        self.user_name = user_name
        
        self.title(lang.get('storico_validazioni_fai', "Storico Validazioni FAI"))
        self.geometry("1200x700")
        
        # Centra finestra
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"1200x700+{x}+{y}")
        
        self._build_ui()
        self._load_data()
    
    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Frame filtri
        filters_frame = ttk.LabelFrame(self, text=self.lang.get('fai_filters_search', "Filtri Ricerca"), padding="10")
        filters_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Prima riga filtri
        row1 = ttk.Frame(filters_frame)
        row1.pack(fill=tk.X, pady=5)
        
        # Data Da
        ttk.Label(row1, text=self.lang.get('fai_date_from', "Data Da:")).pack(side=tk.LEFT, padx=5)
        self.date_from_var = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        self.date_from_entry = ttk.Entry(row1, textvariable=self.date_from_var, width=12)
        self.date_from_entry.pack(side=tk.LEFT, padx=5)
        
        # Data A
        ttk.Label(row1, text=self.lang.get('fai_date_to', "Data A:")).pack(side=tk.LEFT, padx=5)
        self.date_to_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_to_entry = ttk.Entry(row1, textvariable=self.date_to_var, width=12)
        self.date_to_entry.pack(side=tk.LEFT, padx=5)
        
        # Codice Prodotto
        ttk.Label(row1, text=self.lang.get('fai_product_code', "Codice Prodotto:")).pack(side=tk.LEFT, padx=5)
        self.product_var = tk.StringVar()
        self.product_entry = ttk.Entry(row1, textvariable=self.product_var, width=25)
        self.product_entry.pack(side=tk.LEFT, padx=5)
        
        # Operatore
        ttk.Label(row1, text=self.lang.get('fai_operator', "Operatore:")).pack(side=tk.LEFT, padx=5)
        self.operator_var = tk.StringVar()
        self.operator_entry = ttk.Entry(row1, textvariable=self.operator_var, width=20)
        self.operator_entry.pack(side=tk.LEFT, padx=5)
        
        # Pulsante Cerca
        ttk.Button(row1, text="🔍 " + self.lang.get('search', "Cerca"), command=self._load_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(row1, text="🔄 " + self.lang.get('reset', "Reset"), command=self._reset_filters).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        columns = ('FaiLogId', 'Data', 'Ordine', 'Prodotto', 'Operatore', 'Risultato', 'HasPDF')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                 yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Configura colonne
        self.tree.heading('FaiLogId', text='ID')
        self.tree.heading('Data', text='Data/Ora')
        self.tree.heading('Ordine', text='N. Ordine')
        self.tree.heading('Prodotto', text='Codice Prodotto')
        self.tree.heading('Operatore', text='Operatore')
        self.tree.heading('Risultato', text='Risultato')
        self.tree.heading('HasPDF', text='PDF')
        
        self.tree.column('FaiLogId', width=60, anchor='center')
        self.tree.column('Data', width=150, anchor='center')
        self.tree.column('Ordine', width=120, anchor='center')
        self.tree.column('Prodotto', width=300)
        self.tree.column('Operatore', width=150)
        self.tree.column('Risultato', width=100, anchor='center')
        self.tree.column('HasPDF', width=60, anchor='center')
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Doppio click per aprire
        self.tree.bind('<Double-1>', lambda e: self._open_pdf())
        
        # Pulsanti azioni
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(buttons_frame, text=self.lang.get('fai_open_pdf', "📄 Apri PDF"), 
                  command=self._open_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text=self.lang.get('fai_delete_validation', "🗑️ Elimina Validazione"), 
                  command=self._delete_validation).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="❌ " + self.lang.get('close', "Chiudi"), 
                  command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.status_label = ttk.Label(self, text=self.lang.get('ready', "Pronto"), relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _reset_filters(self):
        """Reset filtri"""
        self.date_from_var.set((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        self.date_to_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.product_var.set('')
        self.operator_var.set('')
        self._load_data()
    
    def _load_data(self):
        """Carica dati validazioni"""
        try:
            # Pulisci treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Query
            query = """
            SELECT DISTINCT
                l.FaiLogId,
                l.DateIn,
                l.OrderId,
                o.ProductCode,
                l.Operator,
                l.IsOk,
                CASE WHEN l.DocVerification IS NOT NULL THEN 1 ELSE 0 END AS HasPDF
            FROM [Traceability_RS].[fai].[FaiLogs] l
            LEFT JOIN [Traceability_RS].[dbo].[orders] o ON l.OrderId = o.IDOrder
            WHERE l.DateIn >= ? AND l.DateIn <= ?
            """
            
            params = [
                self.date_from_var.get() + ' 00:00:00',
                self.date_to_var.get() + ' 23:59:59'
            ]
            
            # Filtro prodotto
            if self.product_var.get().strip():
                query += " AND o.ProductCode LIKE ?"
                params.append(f"%{self.product_var.get().strip()}%")
            
            # Filtro operatore
            if self.operator_var.get().strip():
                query += " AND l.Operator LIKE ?"
                params.append(f"%{self.operator_var.get().strip()}%")
            
            query += " ORDER BY l.DateIn DESC"
            
            rows = self.db.fetch_all(query, tuple(params))
            
            # Popola treeview
            for row in rows:
                fai_log_id = row.FaiLogId
                date_in = row.DateIn.strftime('%d/%m/%Y %H:%M') if row.DateIn else ''
                order_id = row.OrderId or ''
                product_code = row.ProductCode or 'N/A'
                operator = row.Operator or 'N/A'
                result = '✓ OK' if row.IsOk else '✗ NOT OK'
                has_pdf = '✓' if row.HasPDF else '✗'
                
                # Colore in base al risultato
                tag = 'ok' if row.IsOk else 'not_ok'
                
                self.tree.insert('', 'end', values=(
                    fai_log_id, date_in, order_id, product_code, 
                    operator, result, has_pdf
                ), tags=(tag,))
            
            # Tags colori
            self.tree.tag_configure('ok', foreground='green')
            self.tree.tag_configure('not_ok', foreground='red')
            
            self.status_label.config(text=f"Trovate {len(rows)} validazioni")
            
        except Exception as e:
            logger.error(f"Errore caricamento validazioni: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile caricare i dati:\n{e}")
    
    def _open_pdf(self):
        """Apre il PDF della validazione selezionata"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona una validazione")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        fai_log_id = values[0]
        has_pdf = values[6]
        
        if has_pdf != '✓':
            messagebox.showwarning("Attenzione", "Nessun PDF disponibile per questa validazione")
            return
        
        try:
            # Recupera PDF dal database
            query = """
            SELECT DocVerification 
            FROM [Traceability_RS].[fai].[FaiLogs]
            WHERE FaiLogId = ?
            """
            
            row = self.db.fetch_one(query, (fai_log_id,))
            
            if not row or not row.DocVerification:
                messagebox.showerror("Errore", "PDF non trovato nel database")
                return
            
            # Salva PDF in temp
            pdf_path = os.path.join(tempfile.gettempdir(), f"FAI_Report_{fai_log_id}.pdf")
            with open(pdf_path, 'wb') as f:
                f.write(row.DocVerification)
            
            # Apri PDF
            os.startfile(pdf_path)
            logger.info(f"PDF aperto: {pdf_path}")
            self.status_label.config(text=f"PDF aperto: FAI Report {fai_log_id}")
            
        except Exception as e:
            logger.error(f"Errore apertura PDF: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile aprire il PDF:\n{e}")
    
    def _delete_validation(self):
        """Elimina validazione selezionata"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona una validazione")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        fai_log_id = values[0]
        
        response = messagebox.askyesno(
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare la validazione FAI ID {fai_log_id}?\n\n"
            "Questa azione è irreversibile!",
            icon='warning'
        )
        
        if not response:
            return
        
        try:
            # Elimina header se esiste
            delete_header = """
            DELETE FROM [Traceability_RS].[fai].[FaiLogHeathers]
            WHERE FaiLogId = ?
            """
            self.db.execute_query(delete_header, (fai_log_id,))
            
            # Elimina tutti i log con questo FaiLogId
            delete_logs = """
            DELETE FROM [Traceability_RS].[fai].[FaiLogs]
            WHERE FaiLogId = ?
            """
            self.db.execute_query(delete_logs, (fai_log_id,))
            
            messagebox.showinfo("Successo", "Validazione eliminata con successo")
            self._load_data()
            
        except Exception as e:
            logger.error(f"Errore eliminazione validazione: {e}", exc_info=True)
            messagebox.showerror("Errore", f"Impossibile eliminare la validazione:\n{e}")
