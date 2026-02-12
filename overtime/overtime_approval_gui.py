"""
Overtime Approval GUI
Form per l'autorizzazione delle richieste di straordinario
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def open_overtime_approval_window(parent, db_handler, lang_manager, user_name, user_id=0):
    """
    Apre la finestra per autorizzare richieste di straordinario.
    
    Args:
        parent: Finestra parent
        db_handler: DatabaseHandler instance
        lang_manager: LanguageManager instance
        user_name: Nome utente loggato
        user_id: ID utente (idanga da tbuserkey)
    """
    OvertimeApprovalWindow(parent, db_handler, lang_manager, user_name, user_id)


class OvertimeApprovalWindow(tk.Toplevel):
    """
    Finestra per autorizzare/rifiutare richieste di straordinario.
    """
    
    def __init__(self, parent, db_handler, lang_manager, user_name, user_id=0):
        super().__init__(parent)
        
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name
        self.user_id = user_id  # ID utente (idanga)
        
        # Setup finestra
        self.title(self.lang.get('overtime_approval_title', 'Autorizzazione Straordinari'))
        self.geometry("1400x700")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._load_pending_requests()
    
    def _create_widgets(self):
        """Crea i widget dell'interfaccia."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === FILTRI ===
        filter_frame = ttk.LabelFrame(main_frame, text=self.lang.get('filters', 'Filtri'), padding="10")
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text=self.lang.get('status', 'Stato:')).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.status_var = tk.StringVar(value='Pending')
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=['All', 'Pending', 'Approved', 'Rejected'],
            state='readonly',
            width=15
        )
        status_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        status_combo.bind('<<ComboboxSelected>>', lambda e: self._load_pending_requests())
        
        ttk.Button(
            filter_frame,
            text=self.lang.get('refresh', 'Aggiorna'),
            command=self._load_pending_requests
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # === LISTA RICHIESTE ===
        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('requests_list', 'Richieste'), padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        columns = ('id', 'number', 'date', 'supervisor', 'employees', 'total_hours', 'status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('id', text='ID')
        self.tree.heading('number', text=self.lang.get('request_number', 'Numero'))
        self.tree.heading('date', text=self.lang.get('date', 'Data'))
        self.tree.heading('supervisor', text=self.lang.get('supervisor', 'Supervisore'))
        self.tree.heading('employees', text=self.lang.get('employees_count', 'N. Dipendenti'))
        self.tree.heading('total_hours', text=self.lang.get('total_hours', 'Ore Totali'))
        self.tree.heading('status', text=self.lang.get('status', 'Stato'))
        
        self.tree.column('id', width=50)
        self.tree.column('number', width=120)
        self.tree.column('date', width=150)
        self.tree.column('supervisor', width=200)
        self.tree.column('employees', width=100)
        self.tree.column('total_hours', width=100)
        self.tree.column('status', width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Double-1>', self._show_request_details)
        
        # === PULSANTI AZIONE ===
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            action_frame,
            text=self.lang.get('view_details', 'Visualizza Dettagli'),
            command=self._show_request_details
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text=self.lang.get('approve', 'Approva'),
            command=lambda: self._approve_or_reject(True)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text=self.lang.get('reject', 'Rifiuta'),
            command=lambda: self._approve_or_reject(False)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text=self.lang.get('close', 'Chiudi'),
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _load_pending_requests(self):
        """Carica le richieste in attesa di approvazione."""
        # Pulisci treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        status_filter = self.status_var.get()
        
        # Query per recuperare richieste
        query = """
        WITH StoryAggregated AS (
    SELECT 
        ExtraHourApprovalId,
        COUNT(DISTINCT IdEmployee) AS EmployeeCount,
        SUM(DATEDIFF(HOUR, DateStart, DateEnd)) AS TotalHours,
        CASE 
            WHEN MAX(ApprovedId) IS NULL THEN 'Pending'
            WHEN MAX(CAST(Approved AS INT)) = 1 THEN 'Approved'
            ELSE 'Rejected'
        END AS Status, 
        ApprovelDate,
        MAX(ApprovedId) AS ApprovedId,
        MAX(CAST(Approved AS INT)) AS Approved
    FROM ResetServices.dbo.ExtraTimeApprovalStory
    WHERE Datesys >'2026-02-01'
    GROUP BY ExtraHourApprovalId, ApprovelDate
)
SELECT 
    a.ExtraHourApprovalId,
    CAST(a.IdRegistro AS VARCHAR) AS RequestNumber,
    a.DateSys,
    ISNULL(u.NomeUser, 'N/A') AS Supervisor,
    ISNULL(s.EmployeeCount, 0) AS EmployeeCount,
    ISNULL(s.TotalHours, 0) AS TotalHours,
    ISNULL(s.Status, 'Pending') AS Status
FROM ResetServices.dbo.ExtraTimeApproval a
LEFT JOIN StoryAggregated s 
    ON a.ExtraHourApprovalId = s.ExtraHourApprovalId
LEFT JOIN resetservices.dbo.tbuserkey u 
    ON a.IdChief = u.idanga
WHERE s.ApprovelDate IS NULL
  AND a.DateSys > '2026-02-01'
        """
        
        if status_filter == 'Pending':
            query += " AND s.ApprovedId IS NULL"
        elif status_filter == 'Approved':
            query += " AND s.Approved = 1"
        elif status_filter == 'Rejected':
            query += " AND s.Approved = 0 AND s.ApprovedId IS NOT NULL"
        
        query += """
        ORDER BY a.DateSys DESC
        """
        
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            for row in results:
                date_str = row[2].strftime('%d/%m/%Y %H:%M') if row[2] else 'N/D'
                self.tree.insert('', tk.END, values=(
                    row[0],  # ID
                    row[1],  # Number
                    date_str,  # Date
                    row[3],  # Supervisor
                    row[4],  # Employee count
                    row[5] if row[5] else 0,  # Total hours
                    row[6]  # Status
                ))
        except Exception as e:
            logger.error(f"Errore caricamento richieste: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento richieste:\n{str(e)}",
                parent=self
            )
    
    def _show_request_details(self, event=None):
        """Mostra i dettagli della richiesta selezionata."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_request', 'Selezionare una richiesta'),
                parent=self
            )
            return
        
        request_id = self.tree.item(selected[0])['values'][0]
        
        # Apri finestra dettagli
        RequestDetailsWindow(self, self.db, self.lang, request_id)
    
    def _approve_or_reject(self, approve):
        """Approva o rifiuta la richiesta selezionata."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_request', 'Selezionare una richiesta'),
                parent=self
            )
            return
        
        request_id = self.tree.item(selected[0])['values'][0]
        request_number = self.tree.item(selected[0])['values'][1]
        action = 'approvare' if approve else 'rifiutare'
        
        # Conferma
        confirm = messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_action', f'Confermare {action} la richiesta?'),
            parent=self
        )
        
        if not confirm:
            return
        
        # Aggiorna database
        try:
            # Recupera IdChief per inviare email
            chief_query = """
            SELECT IdChief 
            FROM ResetServices.dbo.ExtraTimeApproval 
            WHERE ExtraHourApprovalId = ?
            """
            chief_result = self.db.fetch_one(chief_query, (request_id,))
            requester_id = chief_result[0] if chief_result else None
            
            cursor = self.db.conn.cursor()
            
            # Se approvato, chiama SP Registro per ottenere ID approvazione
            approval_id = None
            if approve:
                from datetime import datetime
                registro_query = """
                EXEC ResetServices.dbo.Registro 
                    @tipo=192, 
                    @anno=?, 
                    @data=?, 
                    @operatore=?, 
                    @obj=?, 
                    @chichiama=0
                """
                
                cursor.execute(
                    registro_query,
                    (datetime.now().year, datetime.now().strftime('%Y-%m-%d'), self.user_id, request_id)
                )
                
                # Recupera il risultato della SP
                result = cursor.fetchone()
                if result:
                    approval_id = result[0]
                    logger.info(f"Registro SP returned approval_id: {approval_id}")
                else:
                    logger.warning("Registro SP did not return a value")
                    approval_id = self.user_id  # Fallback
            
            # Aggiorna stato approvazione
            update_query = """
            UPDATE ResetServices.dbo.ExtraTimeApprovalStory
            SET ApprovedId = ?,
                Approved = ?,
                ApprovelDate = GETDATE()
            WHERE ExtraHourApprovalId = ?
            """
            
            cursor.execute(update_query, (approval_id if approve else self.user_id, 1 if approve else 0, request_id))
            self.db.conn.commit()
            cursor.close()
            
            # Invia email di notifica al richiedente
            if requester_id:
                from .overtime_manager import OvertimeManager
                manager = OvertimeManager(self.db)
                manager.send_approval_notification(
                    request_id=request_id,
                    request_number=request_number,
                    requester_id=requester_id,
                    approved=approve,
                    approver_name=self.user_name
                )
                
                # Genera PDF di conferma approvazione (solo se approvato)
                if approve:
                    approval_pdf = manager.generate_approval_confirmation_pdf(
                        request_id=request_id,
                        approver_name=self.user_name
                    )
                    if approval_pdf:
                        logger.info(f"Approval confirmation PDF generated: {approval_pdf}")
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('request_updated', 'Richiesta aggiornata con successo'),
                parent=self
            )
            
            # Ricarica lista
            self._load_pending_requests()
            
        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore aggiornamento richiesta: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore aggiornamento richiesta:\n{str(e)}",
                parent=self
            )


class RequestDetailsWindow(tk.Toplevel):
    """Finestra dettagli richiesta."""
    
    def __init__(self, parent, db_handler, lang_manager, request_id):
        super().__init__(parent)
        
        self.db = db_handler
        self.lang = lang_manager
        self.request_id = request_id
        
        self.title(self.lang.get('request_details', 'Dettagli Richiesta'))
        self.geometry("900x600")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._load_details()
    
    def _create_widgets(self):
        """Crea i widget."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info richiesta
        info_frame = ttk.LabelFrame(main_frame, text=self.lang.get('request_info', 'Informazioni Richiesta'), padding="10")
        info_frame.pack(fill=tk.X, pady=5)
        
        self.info_labels = {}
        for i, key in enumerate(['number', 'date', 'supervisor', 'status']):
            ttk.Label(info_frame, text=f"{self.lang.get(key, key)}:", font=('', 9, 'bold')).grid(
                row=i, column=0, sticky=tk.W, padx=5, pady=2
            )
            self.info_labels[key] = ttk.Label(info_frame, text='')
            self.info_labels[key].grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Dipendenti
        emp_frame = ttk.LabelFrame(main_frame, text=self.lang.get('employees', 'Dipendenti'), padding="10")
        emp_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        columns = ('employee', 'reason', 'start', 'end', 'hours', 'justify')
        self.tree = ttk.Treeview(emp_frame, columns=columns, show='headings')
        
        self.tree.heading('employee', text=self.lang.get('employee', 'Dipendente'))
        self.tree.heading('reason', text=self.lang.get('reason', 'Motivo'))
        self.tree.heading('start', text=self.lang.get('start', 'Inizio'))
        self.tree.heading('end', text=self.lang.get('end', 'Fine'))
        self.tree.heading('hours', text=self.lang.get('hours', 'Ore'))
        self.tree.heading('justify', text=self.lang.get('justify', 'Giustificazione'))
        
        scrollbar = ttk.Scrollbar(emp_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Pulsante chiudi
        ttk.Button(main_frame, text=self.lang.get('close', 'Chiudi'), command=self.destroy).pack(pady=10)
    
    def _load_details(self):
        """Carica i dettagli della richiesta."""
        # Query info richiesta
        info_query = """
        SELECT CAST(a.IdRegistro AS VARCHAR), a.DateSys, ISNULL(u.NomeUser, 'N/A')
        FROM ResetServices.dbo.ExtraTimeApproval a
        LEFT JOIN resetservices.dbo.tbuserkey u ON a.IdChief = u.idanga
        WHERE a.ExtraHourApprovalId = ?
        """
        
        # Query dipendenti
        emp_query = """
        SELECT 
            e.EmployeeSurname + ' ' + e.EmployeeName AS EmployeeName,
            s.Descriptionreasons,
            s.DateStart,
            s.DateEnd,
            DATEDIFF(HOUR, s.DateStart, s.DateEnd) AS Hours,
            s.Justify
        FROM ResetServices.dbo.ExtraTimeApprovalStory s
        INNER JOIN Employee.dbo.EmployeeHireHistory h ON s.IdEmployee = h.EmployeeHireHistoryId
        INNER JOIN Employee.dbo.Employees e ON h.EmployeeId = e.EmployeeId
        WHERE s.ExtraHourApprovalId = ?
        """
        
        try:
            # Carica info
            info_result = self.db.fetch_one(info_query, (self.request_id,))
            if info_result:
                self.info_labels['number'].config(text=info_result[0])
                self.info_labels['date'].config(text=info_result[1].strftime('%d/%m/%Y %H:%M') if info_result[1] else 'N/D')
                self.info_labels['supervisor'].config(text=info_result[2] or 'N/D')
                self.info_labels['status'].config(text='Pending')  # TODO: Calcolare stato reale
            
            # Carica dipendenti
            cursor = self.db.conn.cursor()
            cursor.execute(emp_query, (self.request_id,))
            employees = cursor.fetchall()
            cursor.close()
            
            for emp in employees:
                self.tree.insert('', tk.END, values=(
                    emp[0],  # Name
                    emp[1],  # Reason
                    emp[2].strftime('%d/%m/%Y %H:%M') if emp[2] else 'N/D',  # Start
                    emp[3].strftime('%d/%m/%Y %H:%M') if emp[3] else 'N/D',  # End
                    emp[4] if emp[4] else 0,  # Hours
                    emp[5] or 'N/A'  # Justify
                ))
                
        except Exception as e:
            logger.error(f"Errore caricamento dettagli: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento dettagli:\n{str(e)}",
                parent=self
            )
