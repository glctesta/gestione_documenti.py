# -*- coding: utf-8 -*-
"""
Modulo per la gestione delle autorizzazioni assenze.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import logging
import os
from email_connector import EmailSender

logger = logging.getLogger("TraceabilityRS")


class AbsenceAuthorizationWindow(tk.Toplevel):
    """
    Finestra per l'autorizzazione delle richieste di assenza.
    L'utente può approvare, modificare il periodo o rifiutare le richieste.
    """
    
    def __init__(self, parent, db_handler, lang_manager, authorized_user_id, authorized_user_name=None):
        super().__init__(parent)
        self.parent = parent
        self.db = db_handler
        self.lang = lang_manager
        self.authorized_user_id = authorized_user_id  # EmployeeHireHistoryId dell'utente autorizzato
        self.authorized_user_name = authorized_user_name  # Nome per visualizzazione
        
        logger.info(f"=== Inizializzazione AbsenceAuthorizationWindow ===")
        logger.info(f"Utente autorizzato ID: {self.authorized_user_id}, Nome: {self.authorized_user_name}")
        
        self.title(self.lang.get('absence_authorization_title', 'Autorizzazione Assenze'))
        self.geometry("1200x700")
        self.transient(parent)
        self.grab_set()
        
        # Variabili per la richiesta selezionata
        self.selected_request = None
        self.pending_requests = []
        
        self._create_widgets()
        self._load_pending_requests()
        
    def _create_widgets(self):
        """Crea i widget della finestra"""
        # Frame principale
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titolo
        title_label = ttk.Label(
            main_frame,
            text=self.lang.get('absence_authorization_header', 'Richieste di Assenza da Autorizzare'),
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Frame per la lista
        list_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('pending_requests', 'Richieste Pendenti'),
            padding="10"
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview per mostrare le richieste
        columns = ('ID', 'Tipo', 'Dipendente', 'Data Registrazione', 'Data Inizio', 'Data Fine', 'Giorni', 'Ore')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        
        # Definizione intestazioni
        self.tree.heading('ID', text='ID')
        self.tree.heading('Tipo', text='Tipo Richiesta')
        self.tree.heading('Dipendente', text='Dipendente')
        self.tree.heading('Data Registrazione', text='Registrata il')
        self.tree.heading('Data Inizio', text='Data Inizio')
        self.tree.heading('Data Fine', text='Data Fine')
        self.tree.heading('Giorni', text='Giorni')
        self.tree.heading('Ore', text='Ore')
        
        # Dimensioni colonne
        self.tree.column('ID', width=50)
        self.tree.column('Tipo', width=150)
        self.tree.column('Dipendente', width=200)
        self.tree.column('Data Registrazione', width=120)
        self.tree.column('Data Inizio', width=100)
        self.tree.column('Data Fine', width=100)
        self.tree.column('Giorni', width=60)
        self.tree.column('Ore', width=60)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selezione
        self.tree.bind('<<TreeviewSelect>>', self._on_request_select)
        
        # Frame per i dettagli e azioni
        details_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('request_details', 'Dettagli Richiesta'),
            padding="10"
        )
        details_frame.pack(fill=tk.BOTH, pady=(0, 10))
        
        # Area informazioni
        info_frame = ttk.Frame(details_frame)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Usare tk.Label invece di ttk.Label per supportare il cambio di colore
        self.info_label = tk.Label(
            info_frame,
            text=self.lang.get('select_request_prompt', 'Selezionare una richiesta dalla lista'),
            justify=tk.LEFT,
            font=("Helvetica", 10),
            bg='SystemButtonFace'  # Colore di sfondo di default per Windows
        )
        self.info_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)
        
        # Frame pulsanti azioni
        actions_frame = ttk.Frame(main_frame)
        actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.approve_btn = ttk.Button(
            actions_frame,
            text=self.lang.get('approve_request', 'Approva'),
            command=self._approve_request,
            state=tk.DISABLED
        )
        self.approve_btn.pack(side=tk.LEFT, padx=5)
        
        self.modify_btn = ttk.Button(
            actions_frame,
            text=self.lang.get('modify_period', 'Modifica Periodo'),
            command=self._modify_period,
            state=tk.DISABLED
        )
        self.modify_btn.pack(side=tk.LEFT, padx=5)
        
        self.reject_btn = ttk.Button(
            actions_frame,
            text=self.lang.get('reject_request', 'Rifiuta'),
            command=self._reject_request,
            state=tk.DISABLED
        )
        self.reject_btn.pack(side=tk.LEFT, padx=5)
        
        # Bottone chiudi
        close_btn = ttk.Button(
            actions_frame,
            text=self.lang.get('close', 'Chiudi'),
            command=self.destroy
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
        
    def _load_pending_requests(self):
        """Carica le richieste di assenza pendenti autorizzabili dal capo loggato."""
        try:
            logger.info(f"Caricamento richieste per ID login: {self.authorized_user_id}")

            # STEP 1: risolve EmployeeHireHistoryId del capo loggato.
            employee_hire_history_id = None
            direct_id_query = """
                SELECT TOP 1 EmployeeHireHistoryId
                FROM Employee.dbo.EmployeeHireHistory
                WHERE EmployeeHireHistoryId = ?
            """
            conversion_query = """
                SELECT EmployeeHireHistoryId
                FROM traceability_rs.dbo.AutorizedUsers
                WHERE AuthorizedUsedId = ?
            """

            with self.db._lock:
                self.db.cursor.execute(direct_id_query, self.authorized_user_id)
                direct_match = self.db.cursor.fetchone()
                if direct_match and direct_match.EmployeeHireHistoryId:
                    employee_hire_history_id = direct_match.EmployeeHireHistoryId
                else:
                    self.db.cursor.execute(conversion_query, self.authorized_user_id)
                    conversion_result = self.db.cursor.fetchone()
                    if conversion_result and conversion_result.EmployeeHireHistoryId:
                        employee_hire_history_id = conversion_result.EmployeeHireHistoryId

            if not employee_hire_history_id:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    (
                        f"Impossibile determinare EmployeeHireHistoryId per l'utente loggato "
                        f"(ID: {self.authorized_user_id})"
                    ),
                    parent=self
                )
                self.pending_requests = []
                self._populate_tree([])
                return

            # STEP 2: determina se admin (FunctionCode massimo) o responsabile normale
            admin_check_query = """
                SELECT TOP 1
                    CASE WHEN f.FunctionCode = (SELECT MAX(FunctionCode) FROM Employee.dbo.Functions)
                         THEN 1 ELSE 0 END AS IsAdmin
                FROM Employee.dbo.EmployeeCdcStories cs
                INNER JOIN Employee.dbo.Functions f ON cs.FunctionId = f.FunctionId
                WHERE cs.EmployeeHireHistoryId = ?
                  AND cs.DateOut IS NULL
            """
            with self.db._lock:
                self.db.cursor.execute(admin_check_query, employee_hire_history_id)
                admin_row = self.db.cursor.fetchone()
            is_admin = bool(admin_row and admin_row[0] == 1)
            logger.info(f"EmployeeHireHistoryId={employee_hire_history_id}, IsAdmin={is_admin}")

            # STEP 3: costruisce filtro gerarchia
            subordinate_filter = ""
            subordinate_ids = []

            if not is_admin:
                # Recupera subalterni con CTE gerarchica (stesso CDC)
                subordinate_query = """
                WITH Manager (SubCdcId, FunctionCode, MainCdcId) AS
                (
                    SELECT cs.SubCdcId, f.FunctionCode, c.CdcId
                    FROM employee.dbo.EmployeeCdcStories cs
                    INNER JOIN employee.dbo.CdcSub c
                        ON c.SubCdcId = cs.SubCdcId AND cs.DateOut IS NULL
                    INNER JOIN Employee.dbo.Functions F ON cs.FunctionId = F.FunctionId
                    WHERE cs.EmployeeHireHistoryId = ?
                      AND cs.DateOut IS NULL
                )
                SELECT h.EmployeeHireHistoryId
                FROM employee.dbo.EmployeeHireHistory h
                INNER JOIN employee.dbo.EmployeeCdcStories css
                    ON h.EmployeeHireHistoryId = css.EmployeeHireHistoryId
                    AND css.DateOut IS NULL
                    AND h.EndWorkDate IS NULL
                    AND h.employeerid = 2
                INNER JOIN employee.dbo.Employees e ON h.EmployeeId = e.EmployeeId
                INNER JOIN employee.dbo.CdcSub s ON s.SubCdcId = css.SubCdcId
                INNER JOIN employee.dbo.Functions f ON f.FunctionId = css.FunctionId
                INNER JOIN employee.dbo.CostCenters c ON c.CdcId = s.CdcId
                INNER JOIN Manager m ON m.MainCdcId = s.CdcId AND m.FunctionCode > f.FunctionCode
                WHERE f.FunctionCode < m.FunctionCode
                """
                with self.db._lock:
                    self.db.cursor.execute(subordinate_query, employee_hire_history_id)
                    sub_rows = self.db.cursor.fetchall()

                subordinate_ids = [row[0] for row in sub_rows if row and row[0] is not None]

                # FALLBACK: verifica anche tramite SP GetManagerForSingleEmployee
                # per dipendenti con richieste pendenti che non appaiono nella CTE subordinati
                try:
                    pending_emp_query = """
                        SELECT DISTINCT AR.EmployrrHireHistoryId
                        FROM [Employee].[dbo].[AbsenceRequestes] AR
                        WHERE AR.Approved = '1900-01-01 00:00:00.000'
                          AND AR.EmployrrHireHistoryId NOT IN ({})
                    """.format(', '.join(['?'] * len(subordinate_ids)) if subordinate_ids else '-1')
                    
                    with self.db._lock:
                        self.db.cursor.execute(pending_emp_query, subordinate_ids if subordinate_ids else [])
                        pending_rows = self.db.cursor.fetchall()

                    for prow in pending_rows:
                        emp_id = prow[0]
                        try:
                            with self.db._lock:
                                self.db.cursor.execute(
                                    "EXEC Employee.dbo.GetManagerForSingleEmployee @EmployeeHireHistoryId = ?",
                                    emp_id
                                )
                                mgr_rows = self.db.cursor.fetchall()
                            
                            # Se il manager trovato dalla SP corrisponde al loggato, aggiungi
                            for mr in mgr_rows:
                                if mr[0] == employee_hire_history_id and emp_id not in subordinate_ids:
                                    subordinate_ids.append(emp_id)
                                    logger.info(f"Fallback SP: aggiunto subordinato {emp_id} via GetManagerForSingleEmployee")
                        except Exception as sp_err:
                            logger.debug(f"SP GetManagerForSingleEmployee non disponibile per {emp_id}: {sp_err}")
                except Exception as fb_err:
                    logger.warning(f"Fallback ricerca subordinati: {fb_err}")

                logger.info(f"Subalterni trovati per {employee_hire_history_id}: {subordinate_ids}")

                if not subordinate_ids:
                    logger.info("Nessun subalterno trovato, lista richieste vuota")
                    self.pending_requests = []
                    self._populate_tree([])
                    return

                placeholders = ", ".join(["?"] * len(subordinate_ids))
                subordinate_filter = f"AND H.EmployeeHireHistoryId IN ({placeholders})"

            # STEP 4: Query principale con filtro gerarchia
            query = f"""
                SELECT
                    AR.[AbsenceRequestId],
                    R.RequestName + ' [' + R.Abbreviation + ']' AS RequestType,
                    E.EmployeeSurname + ' ' + E.EmployeeName AS Employee,
                    AR.Datesys AS RecordedOnDate,
                    AR.[DateStart],
                    AR.[DateEnd],
                    DATEDIFF(DAY, AR.[DateStart], AR.[DateEnd]) + 1 AS NrDays,
                    CASE
                        WHEN R.IsConsideredEntireDay = 0
                             AND AR.FromTime IS NOT NULL AND AR.ToTime IS NOT NULL
                        THEN DATEDIFF(MINUTE, AR.FromTime, AR.ToTime) / 60.0
                        ELSE NULL
                    END AS NrHours,
                    AR.FromTime,
                    AR.ToTime,
                    H.EmployeeHireHistoryId,
                    R.IDRequestType,
                    R.IsConsideredEntireDay
                FROM
                    [Employee].[dbo].[AbsenceRequestes] AR
                INNER JOIN
                    Employee.dbo.EmployeeHireHistory H ON H.EmployeeHireHistoryId = AR.EmployrrHireHistoryId
                INNER JOIN
                    Employee.dbo.Employees E ON E.EmployeeId = H.EmployeeId
                INNER JOIN
                    Timeclocking.dbo.RequestType R ON R.IDRequestType = AR.IDRequestType
                INNER JOIN
                    Employee.dbo.Registry RE ON RE.RegistroId = AR.RegistroId
                WHERE
                    AR.Approved = '1900-01-01 00:00:00.000'
                    {subordinate_filter}
                ORDER BY
                    AR.[DateStart],
                    E.EmployeeSurname + ' ' + E.EmployeeName
            """

            with self.db._lock:
                self.db.cursor.execute(query, subordinate_ids)
                all_requests = self.db.cursor.fetchall()

            logger.info(f"Trovate {len(all_requests) if all_requests else 0} richieste pendenti per EmployeeHireHistoryId={employee_hire_history_id}")

            self.pending_requests = all_requests
            self._populate_tree(all_requests)

        except Exception as e:
            logger.error(f"Errore nel caricamento richieste assenza: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Impossibile caricare le richieste: {str(e)}",
                parent=self
            )


    def _populate_tree(self, requests):
        """Popola il Treeview con le richieste"""
        # Pulisce il tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Aggiunge le richieste
        for req in requests:
            is_hourly = hasattr(req, 'IsConsideredEntireDay') and req.IsConsideredEntireDay == 0
            if is_hourly:
                # Assenza oraria: mostra ore, niente giorni
                hours_display = ''
                if req.NrHours is not None:
                    h = float(req.NrHours)
                    hours_display = f"{h:.1f}" if h != int(h) else str(int(h))
                values = (
                    req.AbsenceRequestId,
                    req.RequestType,
                    req.Employee,
                    req.RecordedOnDate.strftime('%d/%m/%Y') if req.RecordedOnDate else '',
                    req.DateStart.strftime('%d/%m/%Y') if req.DateStart else '',
                    req.DateEnd.strftime('%d/%m/%Y') if req.DateEnd else '',
                    '',   # Giorni vuoto per assenze orarie
                    hours_display
                )
            else:
                # Assenza giornaliera: mostra giorni, niente ore
                values = (
                    req.AbsenceRequestId,
                    req.RequestType,
                    req.Employee,
                    req.RecordedOnDate.strftime('%d/%m/%Y') if req.RecordedOnDate else '',
                    req.DateStart.strftime('%d/%m/%Y') if req.DateStart else '',
                    req.DateEnd.strftime('%d/%m/%Y') if req.DateEnd else '',
                    req.NrDays if req.NrDays else '',
                    ''    # Ore vuoto per assenze giornaliere
                )
            self.tree.insert('', tk.END, values=values)
            
    def _on_request_select(self, event):
        """Gestisce la selezione di una richiesta"""
        selection = self.tree.selection()
        if not selection:
            self.selected_request = None
            self.approve_btn.config(state=tk.DISABLED)
            self.modify_btn.config(state=tk.DISABLED)
            self.reject_btn.config(state=tk.DISABLED)
            self.info_label.config(
                text=self.lang.get('select_request_prompt', 'Selezionare una richiesta dalla lista'),
                foreground='black'  # Ripristina il colore nero
            )
            return
            
        # Ottiene i dati della riga selezionata
        item = self.tree.item(selection[0])
        request_id = item['values'][0]
        
        # Trova la richiesta completa
        self.selected_request = None
        for req in self.pending_requests:
            if req.AbsenceRequestId == request_id:
                self.selected_request = req
                break
                
        if self.selected_request:
            # Abilita i pulsanti
            self.approve_btn.config(state=tk.NORMAL)
            # self.modify_btn.config(state=tk.NORMAL)  # Disabilitato temporaneamente
            self.reject_btn.config(state=tk.NORMAL)
            
            # Mostra le informazioni — distingue assenza giornaliera/oraria
            is_hourly = (hasattr(self.selected_request, 'IsConsideredEntireDay')
                         and self.selected_request.IsConsideredEntireDay == 0)

            if is_hourly:
                # Formatta FromTime / ToTime
                from_time_str = ''
                to_time_str = ''
                if self.selected_request.FromTime is not None:
                    ft = self.selected_request.FromTime
                    if hasattr(ft, 'strftime'):
                        from_time_str = ft.strftime('%H:%M')
                    else:
                        from_time_str = str(ft)[:5]
                if self.selected_request.ToTime is not None:
                    tt = self.selected_request.ToTime
                    if hasattr(tt, 'strftime'):
                        to_time_str = tt.strftime('%H:%M')
                    else:
                        to_time_str = str(tt)[:5]

                hours_display = 'N/A'
                if self.selected_request.NrHours is not None:
                    h = float(self.selected_request.NrHours)
                    hours_display = f"{h:.1f}" if h != int(h) else str(int(h))

                info_text = f"""
            Dipendente: {self.selected_request.Employee}
            Tipo Richiesta: {self.selected_request.RequestType}
            Data: {self.selected_request.DateStart.strftime('%d/%m/%Y')}
            Interval orar: {from_time_str} - {to_time_str}
            ore: {hours_display}
            """
            else:
                info_text = f"""
            Dipendente: {self.selected_request.Employee}
            Tipo Richiesta: {self.selected_request.RequestType}
            Data Inizio: {self.selected_request.DateStart.strftime('%d/%m/%Y')}
            Data Fine: {self.selected_request.DateEnd.strftime('%d/%m/%Y')}
giorni: {self.selected_request.NrDays if self.selected_request.NrDays else 'N/A'}
            """
            self.info_label.config(text=info_text, foreground='black')  # Ripristina colore nero
            
            # Se è una richiesta di ferie, verifica la disponibilità
            if self.selected_request.IDRequestType == 1:  # 1 = Ferie
                self._check_vacation_availability()
                
    def _check_vacation_availability(self):
        """Verifica se il dipendente ha giorni di ferie disponibili"""
        logger.info("=== INIZIO _check_vacation_availability ===")
        
        if not self.selected_request:
            logger.warning("Nessuna richiesta selezionata")
            return
        
        logger.info(f"Richiesta selezionata ID: {self.selected_request.AbsenceRequestId}")
        logger.info(f"Tipo richiesta ID: {self.selected_request.IDRequestType}")
        logger.info(f"EmployeeHireHistoryId: {self.selected_request.EmployeeHireHistoryId}")
            
        try:
            # Prima ottiene il badge number
            badge_query = """
                SELECT serialbadge 
                FROM employee.dbo.EmployeeBadgeHistory BS 
                INNER JOIN Employee.dbo.Badges B ON B.BadgeId = BS.BadgeID
                WHERE BS.DateOut IS NULL AND BS.EmployeeHireHistoryId = ?
            """
            
            logger.info(f"Esecuzione query badge per EmployeeHireHistoryId: {self.selected_request.EmployeeHireHistoryId}")
            
            with self.db._lock:
                self.db.cursor.execute(badge_query, self.selected_request.EmployeeHireHistoryId)
                badge_result = self.db.cursor.fetchone()
                
            if not badge_result:
                logger.warning(f"❌ Badge non trovato per EmployeeHireHistoryId: {self.selected_request.EmployeeHireHistoryId}")
                return
                
            badge_number = badge_result.serialbadge
            current_year = datetime.now().year
            
            logger.info(f"✓ Badge trovato: {badge_number}, Anno corrente: {current_year}")
            
            # Esegue la query complessa per il calcolo ferie
            availability_query = """
                DECLARE @NoBadge VARCHAR(50) = ?
                DECLARE @Anno INT = ?
                DECLARE @DataRiferimento DATE = GETDATE()
                DECLARE @InizioAnno DATE = DATEFROMPARTS(@Anno, 1, 1)
                DECLARE @FineAnno DATE = DATEFROMPARTS(@Anno, 12, 31)

                ;WITH 
                Numbers AS (
                    SELECT a.n + b.n + c.n AS n 
                    FROM (
                        SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 
                        UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
                    ) a
                    CROSS JOIN (
                        SELECT 0 AS n UNION ALL SELECT 10 UNION ALL SELECT 20 UNION ALL SELECT 30 UNION ALL SELECT 40 
                        UNION ALL SELECT 50 UNION ALL SELECT 60 UNION ALL SELECT 70 UNION ALL SELECT 80 UNION ALL SELECT 90
                    ) b
                    CROSS JOIN (
                        SELECT 0 AS n UNION ALL SELECT 100 UNION ALL SELECT 200 UNION ALL SELECT 300
                    ) c
                    WHERE a.n + b.n + c.n <= 365
                ),
                BonusAnzianitaCTE AS (
                    SELECT 
                        noYears,
                        FixValueOnBrutSalary AS GiorniBonus
                    FROM 
                        [Employee].[dbo].[BonusTypeSeniotiry]
                    WHERE 
                        BonusTypeValueId = 4 
                        AND dateout IS NULL
                ),
                FestiviCTE AS (
                    SELECT DISTINCT
                        DATEFROMPARTS(YearPublicHoliday, MonthPublicHoliday, DayPublicHoliday) AS DataFestivo
                    FROM 
                        [Timeclocking].[dbo].[PublicHoliday]
                    WHERE 
                        YearPublicHoliday BETWEEN @Anno - 50 AND @Anno + 1
                ),
                CalcoloAnzianitaCTE AS (
                    SELECT 
                        te.IDEmployee,
                        h.EmployeeHireHistoryId,
                        e.EmployeeName,
                        e.EmployeeSurname,
                        b.NoBadge,
                        h.HireDate,
                        h.HolidayPerYear,
                        CASE 
                            WHEN h.HireDate <= @DataRiferimento THEN
                                CASE 
                                    WHEN MONTH(@DataRiferimento) > MONTH(h.HireDate) 
                                        OR (MONTH(@DataRiferimento) = MONTH(h.HireDate) AND DAY(@DataRiferimento) >= DAY(h.HireDate))
                                    THEN DATEDIFF(YEAR, h.HireDate, @DataRiferimento)
                                    ELSE DATEDIFF(YEAR, h.HireDate, @DataRiferimento) - 1
                                END
                            ELSE 0
                        END AS Anni
                    FROM 
                        employee.dbo.employees E
                        INNER JOIN employee.dbo.EmployeeHireHistory H 
                            ON e.EmployeeId = h.EmployeeId 
                            AND h.EmployeerId = 2 
                            AND h.EndWorkDate IS NULL
                        INNER JOIN [Timeclocking].[dbo].[Employee] TE 
                            ON e.EmployeeNID COLLATE Latin1_General_CI_AI = te.UniqueID COLLATE Latin1_General_CI_AI
                            AND te.DataStop IS NULL
                        INNER JOIN employee.dbo.EmployeeBadgeHistory BH 
                            ON h.EmployeeHireHistoryId = bh.EmployeeHireHistoryId 
                            AND bh.DateOut IS NULL
                        INNER JOIN employee.dbo.Badges B 
                            ON bh.BadgeID = b.BadgeId
                    WHERE 
                        b.NoBadge COLLATE Latin1_General_CI_AI = @NoBadge COLLATE Latin1_General_CI_AI
                ),
                FerieSpettantiCTE AS (
                    SELECT 
                        C.*,
                        ISNULL((
                            SELECT TOP 1 GiorniBonus 
                            FROM BonusAnzianitaCTE 
                            WHERE noYears <= C.Anni
                            ORDER BY noYears DESC
                        ), 0) AS GiorniBonusAnzianita,
                        CASE 
                            WHEN YEAR(C.HireDate) = @Anno THEN 
                                CEILING(CAST(C.HolidayPerYear AS FLOAT) * 
                                       (DATEDIFF(DAY, C.HireDate, @DataRiferimento) + 1) / 
                                       (CASE WHEN (@Anno % 4 = 0 AND @Anno % 100 != 0) OR (@Anno % 400 = 0) 
                                             THEN 366 ELSE 365 END))
                            WHEN YEAR(C.HireDate) < @Anno THEN 
                                C.HolidayPerYear
                            ELSE 
                                0
                        END AS FerieAnnoCorrente
                    FROM CalcoloAnzianitaCTE C
                ),
                FerieSpettantiPerAnnoCTE AS (
                    SELECT 
                        F.IDEmployee,
                        YEAR(F.HireDate) + (N.n / 10) AS Anno,
                        CASE 
                            WHEN YEAR(F.HireDate) = YEAR(F.HireDate) + (N.n / 10) THEN 
                                CEILING(CAST(F.HolidayPerYear AS FLOAT) * 
                                       (DATEDIFF(DAY, F.HireDate, DATEFROMPARTS(YEAR(F.HireDate) + (N.n / 10), 12, 31)) + 1) / 
                                       (CASE WHEN ((YEAR(F.HireDate) + (N.n / 10)) % 4 = 0 AND (YEAR(F.HireDate) + (N.n / 10)) % 100 != 0) 
                                          OR ((YEAR(F.HireDate) + (N.n / 10)) % 400 = 0) 
                                             THEN 366 ELSE 365 END))
                            WHEN YEAR(F.HireDate) < YEAR(F.HireDate) + (N.n / 10) THEN 
                                F.HolidayPerYear
                            ELSE 
                                0
                        END AS FerieSpettanti
                    FROM 
                        FerieSpettantiCTE F
                        CROSS JOIN Numbers N
                    WHERE 
                        N.n % 10 = 0
                        AND (N.n / 10) <= 30
                        AND YEAR(F.HireDate) + (N.n / 10) < @Anno
                ),
                FerieSpettantiAnniPrecedentiCTE AS (
                    SELECT 
                        IDEmployee,
                        SUM(FerieSpettanti) AS TotaleFerieSpettantiAnniPrecedenti
                    FROM 
                        FerieSpettantiPerAnnoCTE
                    GROUP BY 
                        IDEmployee
                ),
                GiorniAssenzeEspansi AS (
                    SELECT 
                        D.IDEmployee,
                        D.IDRequestType,
                        DATEADD(DAY, N.n, D.DateFrom) AS DataCorrente,
                        CASE 
                            WHEN DATEADD(DAY, N.n, D.DateFrom) < @InizioAnno THEN 1
                            ELSE 0
                        END AS IsAnniPrecedenti,
                        CASE 
                            WHEN DATEADD(DAY, N.n, D.DateFrom) >= @InizioAnno 
                                AND DATEADD(DAY, N.n, D.DateFrom) <= @FineAnno THEN 1
                            ELSE 0
                        END AS IsAnnoCorrente,
                        CASE 
                            WHEN DATEPART(WEEKDAY, DATEADD(DAY, N.n, D.DateFrom)) IN (1, 7) THEN 0
                            WHEN EXISTS (
                                SELECT 1 
                                FROM FestiviCTE F 
                                WHERE F.DataFestivo = DATEADD(DAY, N.n, D.DateFrom)
                            ) THEN 0
                            ELSE 1
                        END AS IsGiornoLavorativo
                    FROM 
                        [Timeclocking].[dbo].[EmployeeRequestEntireDay] D
                        CROSS JOIN Numbers N
                    WHERE 
                        DATEADD(DAY, N.n, D.DateFrom) <= D.DateTo
                        AND D.DateFrom <= DATEADD(YEAR, 1, @FineAnno)
                ),
                FerieUsateAnniPrecedentiCTE AS (
                    SELECT 
                        IDEmployee,
                        SUM(IsGiornoLavorativo) AS FerieUsateAnniPrecedenti
                    FROM 
                        GiorniAssenzeEspansi
                    WHERE 
                        IDRequestType = 1
                        AND IsAnniPrecedenti = 1
                    GROUP BY 
                        IDEmployee
                ),
                FerieUsateAnnoCorrenteCTE AS (
                    SELECT 
                        IDEmployee,
                        SUM(IsGiornoLavorativo) AS FerieUsateAnnoCorrente
                    FROM 
                        GiorniAssenzeEspansi
                    WHERE 
                        IDRequestType = 1
                        AND IsAnnoCorrente = 1
                    GROUP BY 
                        IDEmployee
                )
                SELECT 
                    F.IDEmployee,
                    F.EmployeeHireHistoryId,
                    F.EmployeeName,
                    F.EmployeeSurname,
                    F.NoBadge,
                    F.FerieAnnoCorrente + F.GiorniBonusAnzianita + 
                    (ISNULL(FSAP.TotaleFerieSpettantiAnniPrecedenti, 0) - ISNULL(FUAP.FerieUsateAnniPrecedenti, 0)) - 
                    ISNULL(FUAC.FerieUsateAnnoCorrente, 0) AS GiorniDisponibili
                FROM 
                    FerieSpettantiCTE F
                    LEFT JOIN FerieSpettantiAnniPrecedentiCTE FSAP ON F.IDEmployee = FSAP.IDEmployee
                    LEFT JOIN FerieUsateAnniPrecedentiCTE FUAP ON F.IDEmployee = FUAP.IDEmployee
                    LEFT JOIN FerieUsateAnnoCorrenteCTE FUAC ON F.IDEmployee = FUAC.IDEmployee
            """
            
            logger.info("Esecuzione query CTE per calcolo ferie...")
            
            with self.db._lock:
                self.db.cursor.execute(availability_query, badge_number, current_year)
                availability_result = self.db.cursor.fetchone()
            
            logger.info(f"Risultato query CTE: {availability_result}")
                
            if availability_result:
                available_days = availability_result.GiorniDisponibili
                requested_days = self.selected_request.NrDays
                
                logger.info(f"Giorni disponibili: {available_days}")
                logger.info(f"Giorni richiesti: {requested_days}")
                
                # Aggiorna l'info label con la disponibilità
                current_info = self.info_label.cget('text')
                availability_info = f"\n\nGiorni disponibili: {available_days}"
                
                if requested_days > available_days:
                    availability_info += f"\n⚠️ ATTENZIONE: giorni richiesti ({requested_days}) superano la disponibilità!"
                    logger.info("🔴 Impostazione colore ROSSO")
                    self.info_label.config(foreground='red')
                else:
                    availability_info += f"\n✓ Richiesta compatibile con disponibilità"
                    logger.info("🟢 Impostazione colore VERDE")
                    self.info_label.config(foreground='darkgreen')
                    
                self.info_label.config(text=current_info + availability_info)
                logger.info(f"Testo aggiornato: {current_info + availability_info}")
            else:
                logger.warning("❌ Query CTE non ha restituito risultati")
                
        except Exception as e:
            logger.error(f"❌ Errore nella verifica disponibilità ferie: {e}", exc_info=True)
        
        logger.info("=== FINE _check_vacation_availability ===")
            
    def _approve_request(self):
        """Approva la richiesta selezionata"""
        if not self.selected_request:
            return
            
        response = messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_approve', 'Confermare l\'approvazione della richiesta?'),
            parent=self
        )
        
        if not response:
            return
        
        try:
            logger.info(f"=== INIZIO APPROVAZIONE RICHIESTA {self.selected_request.AbsenceRequestId} ===")
            
            date_start = self.selected_request.DateStart
            date_end = self.selected_request.DateEnd
            request_type_id = self.selected_request.IDRequestType
            
            logger.info(f"Data inizio: {date_start}, Data fine: {date_end}, Tipo: {request_type_id}")
            
            # STEP 1: Verifica esistenza mesi in DailyState
            self._ensure_months_exist_in_daily_state(date_start, date_end)
            
            # STEP 2: Recupera IDEmployee da Timeclocking tramite badge
            id_employee_timeclocking = self._get_timeclocking_employee_id(self.selected_request.EmployeeHireHistoryId)
            
            if not id_employee_timeclocking:
                raise Exception("Impossibile trovare IDEmployee in Timeclocking per questo dipendente")
            
            logger.info(f"IDEmployee Timeclocking: {id_employee_timeclocking}")
            
            # STEP 3: Inserimento basato sul tipo di richiesta
            if request_type_id not in [2, 3]:  # Ferie, malattia, ecc. (giornata intera)
                self._approve_entire_day_request(id_employee_timeclocking, date_start, date_end)
            else:  # Permessi (tipo 2 = pagato, tipo 3 = non pagato)
                self._approve_fractional_request(id_employee_timeclocking, date_start, request_type_id)
            
            # STEP 4: Aggiorna la richiesta come approvata
            self._mark_request_as_approved(self.selected_request.AbsenceRequestId)
            
            logger.info(f"✅ Richiesta {self.selected_request.AbsenceRequestId} approvata con successo")
            
            # STEP 5: Invia notifica email al richiedente
            try:
                self._send_absence_decision_email(approved=True)
            except Exception as email_err:
                logger.warning(f"Notifica email non inviata: {email_err}")
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('request_approved_success', 'Richiesta approvata con successo'),
                parent=self
            )
            
            # Ricarica la lista
            self._load_pending_requests()
            
        except Exception as e:
            logger.error(f"❌ Errore durante l'approvazione: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante l'approvazione della richiesta: {str(e)}",
                parent=self
            )
    
    def _ensure_months_exist_in_daily_state(self, date_start, date_end):
        """Verifica e crea i mesi necessari in DailyState"""
        logger.info("Verifica esistenza mesi in DailyState...")
        
        months_to_check = []
        months_to_check.append((date_start.year, date_start.month))
        
        # Se la data fine è in un mese diverso, aggiungila
        if date_end.year != date_start.year or date_end.month != date_start.month:
            months_to_check.append((date_end.year, date_end.month))
        
        for year, month in months_to_check:
            # Verifica se esiste
            check_query = """
                SELECT DISTINCT year(DailyStateDate) AS [Year], month(DailyStateDate) AS [Month] 
                FROM TimeClocking.dbo.DailyState 
                WHERE year(DailyStateDate) = ? AND month(DailyStateDate) = ?
            """
            
            with self.db._lock:
                self.db.cursor.execute(check_query, year, month)
                result = self.db.cursor.fetchone()
            
            if not result:
                # Il mese non esiste, crealo
                logger.info(f"Mese {year}-{month:02d} non trovato in DailyState, creazione in corso...")
                first_day = datetime(year, month, 1)
                
                create_month_sp = f"EXECUTE TimeClocking.dbo.DailyStateDateMonth @date = N'{first_day.strftime('%Y-%m-%d')}'"
                
                with self.db._lock:
                    self.db.cursor.execute(create_month_sp)
                
                logger.info(f"✓ Mese {year}-{month:02d} creato in DailyState")
            else:
                logger.info(f"✓ Mese {year}-{month:02d} già esistente in DailyState")
    
    def _get_timeclocking_employee_id(self, employee_hire_history_id):
        """Recupera IDEmployee da Timeclocking tramite badge"""
        logger.info(f"Recupero IDEmployee Timeclocking per EmployeeHireHistoryId {employee_hire_history_id}")
        
        # Prima recupera il badge
        badge_query = """
            SELECT B.NoBadge
            FROM employee.dbo.EmployeeBadgeHistory bh
            INNER JOIN Employee.dbo.Badges B ON B.BadgeId = bh.BadgeId
            WHERE bh.EmployeeHireHistoryId = ? AND bh.DateOut IS NULL
        """
        
        with self.db._lock:
            self.db.cursor.execute(badge_query, employee_hire_history_id)
            badge_result = self.db.cursor.fetchone()
        
        if not badge_result:
            raise Exception(f"Badge non trovato per EmployeeHireHistoryId {employee_hire_history_id}")
        
        badge_number = badge_result.NoBadge
        logger.info(f"Badge trovato: {badge_number}")
        
        # Poi recupera IDEmployee da Timeclocking
        id_employee_query = """
            SELECT [IDEmployee], UniqueID  
            FROM [Timeclocking].[dbo].[Employee] 
            WHERE UniqueID COLLATE database_default = (
                SELECT EmployeeNID 
                FROM Employee.dbo.Employees e 
                INNER JOIN employee.dbo.employeehirehistory h ON e.employeeid = h.employeeid AND h.employeerid = 2 
                INNER JOIN employee.dbo.EmployeeBadgeHistory bh ON h.employeehirehistoryid = bh.EmployeeHireHistoryId AND bh.DateOut IS NULL 
                INNER JOIN Employee.dbo.badges B ON B.BadgeId = bh.badgeid
                WHERE B.NoBadge = ?
            )
            AND [Timeclocking].[dbo].[Employee].DataStop IS NULL
        """
        
        with self.db._lock:
            self.db.cursor.execute(id_employee_query, badge_number)
            result = self.db.cursor.fetchone()
        
        if not result:
            raise Exception(f"IDEmployee non trovato in Timeclocking per badge {badge_number}")
        
        return result.IDEmployee
    
    def _approve_entire_day_request(self, id_employee, date_start, date_end):
        """Approva una richiesta di assenza a giornata intera (ferie, malattia, ecc.)"""
        logger.info("Approvazione richiesta giornata intera...")
        
        # STEP 1: INSERT in EmployeeRequestEntireDay
        insert_query = """
            INSERT INTO [Timeclocking].[dbo].[EmployeeRequestEntireDay] 
            (IDEmployee, IDRequestType, Number, RequestDate, DateFrom, DateTo)
            VALUES (?, ?, ?, GETDATE(), ?, ?)
        """
        
        with self.db._lock:
            self.db.cursor.execute(
                insert_query,
                id_employee,
                self.selected_request.IDRequestType,
                self.selected_request.AbsenceRequestId,  # Number = AbsenceRequestId
                date_start,
                date_end
            )
        
        # STEP 2: Recupera l'ID appena inserito
        with self.db._lock:
            self.db.cursor.execute(
                "SELECT TOP 1 IDEmployeeRequestEntireDay FROM TimeClocking.dbo.EmployeeRequestEntireDay ORDER BY IDEmployeeRequestEntireDay DESC"
            )
            result = self.db.cursor.fetchone()
            id_request = result.IDEmployeeRequestEntireDay
        
        logger.info(f"IDEmployeeRequestEntireDay creato: {id_request}")
        
        # STEP 3: UPDATE DailyState per ogni giorno (esclusi sabato, domenica e festivi)
        current_date = date_start
        days_updated = 0
        
        while current_date <= date_end:
            # Controlla se è sabato (5) o domenica (6) - SQL Server DATEPART(WEEKDAY) con DATEFIRST 1
            weekday = current_date.weekday()  # Python: 0=Mon, 6=Sun
            
            # Controlla se è festivo
            is_holiday = self._is_public_holiday(current_date)
            
            if weekday < 5 and not is_holiday:  # Lun-Ven e non festivo
                update_query = """
                    UPDATE TimeClocking.dbo.DailyState 
                    SET IDEmployeeRequestEntireDay = ?,
                        PlanningWorkMin = 0,
                        IsPresenceProblem = 0,
                        WorkedMin = 0
                    WHERE IDEmployee = ? 
                    AND DailyStateDate = ?
                """
                
                with self.db._lock:
                    self.db.cursor.execute(update_query, id_request, id_employee, current_date)
                
                days_updated += 1
                logger.debug(f"  Aggiornato DailyState per {current_date.strftime('%Y-%m-%d')}")
            else:
                logger.debug(f"  Saltato {current_date.strftime('%Y-%m-%d')} (weekend o festivo)")
            
            current_date += timedelta(days=1)
        logger.info(f"✓ Aggiornati {days_updated} giorni in DailyState")
    
    def _is_public_holiday(self, date):
        """Verifica se una data è un giorno festivo"""
        check_query = """
            SELECT 1 
            FROM Timeclocking.dbo.PublicHoliday 
            WHERE YearPublicHoliday = ? 
            AND MonthPublicHoliday = ? 
            AND DayPublicHoliday = ?
        """
        
        with self.db._lock:
            self.db.cursor.execute(check_query, date.year, date.month, date.day)
            result = self.db.cursor.fetchone()
        
        return result is not None
    
    def _approve_fractional_request(self, id_employee, date_start, request_type_id):
        """Approva una richiesta di permesso frazionato (ore)"""
        logger.info("Approvazione richiesta permesso frazionato...")
        
        # Calcola i minuti (dalle ore della richiesta)
        # Nota: questa parte richiede che tu abbia anche l'orario di inizio/fine nella richiesta
        # Per ora uso NrHours dalla richiesta
        no_minuti = self.selected_request.NrHours * 60 if self.selected_request.NrHours else 0
        
        # Recupera IDDailyState
        get_daily_state_query = """
            SELECT IDDailyState 
            FROM [Timeclocking].[dbo].[DailyState] 
            WHERE IDEmployee = ? 
            AND CAST(DailyStateDate AS date) = ?
        """
        
        with self.db._lock:
            self.db.cursor.execute(get_daily_state_query, id_employee, date_start.date())
            result = self.db.cursor.fetchone()
        
        if not result:
            raise Exception(f"DailyState non trovato per la data {date_start.date()}. Generare prima il mese.")
        
        id_daily_state = result.IDDailyState
        
        # Mappa tipo richiesta: 2 = permesso pagato (10), 3 = non pagato (12)
        timeclocking_request_type = 10 if request_type_id == 2 else 12
        
        # Elimina eventuali permessi esistenti dello stesso tipo
        delete_query = """
            DELETE FROM [Timeclocking].[dbo].[EmployeeRequestFractionalDay] 
            WHERE IDDailyState = ? AND IDRequestType = ?
        """
        
        with self.db._lock:
            self.db.cursor.execute(delete_query, id_daily_state, timeclocking_request_type)
        
        # Inserisce il nuovo permesso
        insert_query = """
            INSERT INTO [Timeclocking].[dbo].[EmployeeRequestFractionalDay] 
            (IDEmployee, IDRequestType, IDDailyState, NoMin)
            VALUES (?, ?, ?, ?)
        """
        
        with self.db._lock:
            self.db.cursor.execute(insert_query, id_employee, timeclocking_request_type, id_daily_state, no_minuti)
        
        logger.info(f"✓ Permesso frazionato inserito: {no_minuti} minuti")
    
    def _mark_request_as_approved(self, absence_request_id):
        """Marca la richiesta come approvata nel database Employee"""
        logger.info(f"Aggiornamento stato richiesta {absence_request_id} come approvata...")
        
        update_query = """
            UPDATE [Employee].[dbo].[AbsenceRequestes]
            SET Approved = GETDATE(),
                ApprovedBy = ?,
                Rejected = 0
            WHERE AbsenceRequestId = ?
        """
        
        logger.info(f"Esecuzione UPDATE per AbsenceRequestId={absence_request_id}")
        logger.info(f"  ApprovedBy='{self.authorized_user_name}'")
        
        with self.db._lock:
            self.db.cursor.execute(
                update_query,
                self.authorized_user_name,  # Nome del manager che approva
                absence_request_id
            )
            rows_affected = self.db.cursor.rowcount
            logger.info(f"  Righe aggiornate: {rows_affected}")
            
            # Commit esplicito
            try:
                self.db.cursor.connection.commit()
                logger.info("  Commit eseguito con successo")
            except Exception as commit_error:
                logger.warning(f"  Commit non riuscito (probabilmente autocommit è attivo): {commit_error}")
        
        if rows_affected == 0:
            logger.error(f"❌ ATTENZIONE: UPDATE non ha modificato nessuna riga!")
            raise Exception(f"UPDATE non ha modificato nessuna riga per AbsenceRequestId={absence_request_id}")
        
        logger.info(f"✓ Richiesta {absence_request_id} marcata come approvata da {self.authorized_user_name}")
            
    def _modify_period(self):
        """Permette di modificare il periodo della richiesta"""
        if not self.selected_request:
            return
            
        # TODO: Aprire una finestra per modificare le date
        messagebox.showinfo(
            self.lang.get('info', 'Informazione'),
            'Funzione di modifica periodo in fase di sviluppo.',
            parent=self
        )
        
    def _reject_request(self):
        """Rifiuta la richiesta con motivazione"""
        if not self.selected_request:
            return
            
        # Finestra per inserire la motivazione del rifiuto
        RejectReasonDialog(self, self.lang, self._process_rejection)
        
    def _process_rejection(self, reason):
        """Processa il rifiuto con la motivazione fornita"""
        if not reason or not reason.strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('rejection_reason_required', 'La motivazione del rifiuto è obbligatoria'),
                parent=self
            )
            return
        
        try:
            logger.info(f"=== INIZIO RIFIUTO RICHIESTA {self.selected_request.AbsenceRequestId} ===")
            logger.info(f"Motivo rifiuto: {reason}")
            logger.info(f"Manager: {self.authorized_user_name}")
            
            # UPDATE della tabella AbsenceRequestes
            update_query = """
                UPDATE [Employee].[dbo].[AbsenceRequestes]
                SET ApprovedBy = ?,
                    Approved = GETDATE(),
                    Rejected = 1,
                    RefuseMotive = ?
                WHERE AbsenceRequestId = ?
            """
            
            logger.info(f"Esecuzione UPDATE per AbsenceRequestId={self.selected_request.AbsenceRequestId}")
            logger.info(f"  ApprovedBy='{self.authorized_user_name}'")
            logger.info(f"  RefuseMotive='{reason}'")
            
            with self.db._lock:
                self.db.cursor.execute(
                    update_query,
                    self.authorized_user_name,  # Nome del manager
                    reason,  # Motivo del rifiuto
                    self.selected_request.AbsenceRequestId
                )
                rows_affected = self.db.cursor.rowcount
                logger.info(f"  Righe aggiornate: {rows_affected}")
                
                # Commit esplicito
                try:
                    self.db.cursor.connection.commit()
                    logger.info("  Commit eseguito con successo")
                except Exception as commit_error:
                    logger.warning(f"  Commit non riuscito (probabilmente autocommit è attivo): {commit_error}")
            
            if rows_affected == 0:
                logger.error(f"❌ ATTENZIONE: UPDATE non ha modificato nessuna riga!")
                raise Exception(f"UPDATE non ha modificato nessuna riga per AbsenceRequestId={self.selected_request.AbsenceRequestId}")
            
            logger.info(f"✅ Richiesta {self.selected_request.AbsenceRequestId} rifiutata con successo")
            logger.info(f"   ApprovedBy: {self.authorized_user_name}")
            logger.info(f"   Approved: GETDATE()")
            logger.info(f"   Rejected: 1")
            
            # Invia notifica email al richiedente
            try:
                self._send_absence_decision_email(approved=False, reason=reason)
            except Exception as email_err:
                logger.warning(f"Notifica email rifiuto non inviata: {email_err}")
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('request_rejected_success', f'Richiesta rifiutata con successo.\n\nMotivo: {reason}'),
                parent=self
            )
            
            # Ricarica la lista
            self._load_pending_requests()
            
        except Exception as e:
            logger.error(f"❌ Errore durante il rifiuto: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante il rifiuto della richiesta: {str(e)}",
                parent=self
            )

    # ──────────────────────────────────────────────────────────────────────────
    # Email notification helpers
    # ──────────────────────────────────────────────────────────────────────────

    def _get_employee_email(self, employee_hire_history_id):
        """Restituisce (full_name, work_email) per l'EmployeeHireHistoryId dato."""
        query = """
            SELECT DISTINCT
                e.EmployeeName + ' ' + e.EmployeeSurname AS Employee,
                ea.WorkEmail AS Email
            FROM  Employee.dbo.EmployeeHireHistory h
            LEFT JOIN Employee.dbo.Employees e
                ON e.EmployeeId = h.EmployeeId AND h.employeerid = 2 AND h.EndWorkDate IS NULL
            LEFT JOIN Employee.dbo.EmployeeAddress ea
                ON ea.EmployeeId = e.EmployeeId AND ea.DateOut IS NULL
            INNER JOIN resetservices.dbo.tbuserkey k
                ON e.employeeid = k.IdAnga
            WHERE h.EmployeeHireHistoryId = ?
        """
        with self.db._lock:
            self.db.cursor.execute(query, employee_hire_history_id)
            row = self.db.cursor.fetchone()
        if row and row.Email:
            return row.Employee, row.Email
        return None, None

    def _get_cc_recipients(self, employee_hire_history_id):
        """Raccoglie tutti gli indirizzi email in CC:
           1. Valore settings 'Sys_email_absence_decision'
           2. Email dei manager diretti del dipendente richiedente
        """
        cc = []

        # 1. Indirizzi fissi da settings
        try:
            with self.db._lock:
                self.db.cursor.execute(
                    "SELECT [value] FROM traceability_rs.dbo.settings WHERE atribute = 'Sys_email_absence_decision'"
                )
                row = self.db.cursor.fetchone()
            if row and row.value:
                for addr in row.value.replace(';', ',').split(','):
                    addr = addr.strip()
                    if addr:
                        cc.append(addr)
        except Exception as e:
            logger.warning(f"Impossibile leggere Sys_email_absence_decision dalle settings: {e}")

        # 2. Email dei manager del dipendente richiedente
        try:
            with self.db._lock:
                self.db.cursor.execute(
                    "EXEC Employee.dbo.GetManagerForSingleEmployee @EmployeeHireHistoryId = ?",
                    employee_hire_history_id
                )
                manager_rows = self.db.cursor.fetchall()

            manager_ids = [row[0] for row in manager_rows if row and row[0] is not None]

            for mgr_id in manager_ids:
                _, mgr_email = self._get_employee_email(mgr_id)
                if mgr_email and mgr_email not in cc:
                    cc.append(mgr_email)
        except Exception as e:
            logger.warning(f"Impossibile recuperare email manager: {e}")

        return cc

    def _get_vacation_balance(self, employee_hire_history_id):
        """Restituisce il saldo giorni ferie anno corrente per il dipendente.
        Usa EmployeeHireHistoryId come parametro diretto.
        Restituisce None in caso di errore o dati non disponibili."""
        try:
            current_year = datetime.now().year

            query = """
                DECLARE @Anno INT = ?
                DECLARE @DataRiferimento DATE = GETDATE()
                DECLARE @InizioAnno DATE = DATEFROMPARTS(@Anno, 1, 1)
                DECLARE @FineAnno DATE = DATEFROMPARTS(@Anno, 12, 31)

                ;WITH 
                Numbers AS (
                    SELECT a.n + b.n + c.n AS n 
                    FROM (
                        SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 
                        UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
                    ) a
                    CROSS JOIN (
                        SELECT 0 AS n UNION ALL SELECT 10 UNION ALL SELECT 20 UNION ALL SELECT 30 UNION ALL SELECT 40 
                        UNION ALL SELECT 50 UNION ALL SELECT 60 UNION ALL SELECT 70 UNION ALL SELECT 80 UNION ALL SELECT 90
                    ) b
                    CROSS JOIN (
                        SELECT 0 AS n UNION ALL SELECT 100 UNION ALL SELECT 200 UNION ALL SELECT 300
                    ) c
                    WHERE a.n + b.n + c.n <= 365
                ),
                BonusAnzianitaCTE AS (
                    SELECT 
                        noYears,
                        FixValueOnBrutSalary AS GiorniBonus
                    FROM 
                        [Employee].[dbo].[BonusTypeSeniotiry]
                    WHERE 
                        BonusTypeValueId = 4 
                        AND dateout IS NULL
                ),
                FestiviCTE AS (
                    SELECT DISTINCT
                        DATEFROMPARTS(YearPublicHoliday, MonthPublicHoliday, DayPublicHoliday) AS DataFestivo
                    FROM 
                        [Timeclocking].[dbo].[PublicHoliday]
                    WHERE 
                        YearPublicHoliday BETWEEN @Anno - 50 AND @Anno + 1
                ),
                CalcoloAnzianitaCTE AS (
                    SELECT 
                        te.IDEmployee,
                        h.EmployeeHireHistoryId,
                        e.EmployeeName,
                        e.EmployeeSurname,
                        b.NoBadge,
                        h.HireDate,
                        h.HolidayPerYear,
                        CASE 
                            WHEN h.HireDate <= @DataRiferimento THEN
                                CASE 
                                    WHEN MONTH(@DataRiferimento) > MONTH(h.HireDate) 
                                        OR (MONTH(@DataRiferimento) = MONTH(h.HireDate) AND DAY(@DataRiferimento) >= DAY(h.HireDate))
                                    THEN DATEDIFF(YEAR, h.HireDate, @DataRiferimento)
                                    ELSE DATEDIFF(YEAR, h.HireDate, @DataRiferimento) - 1
                                END
                            ELSE 0
                        END AS Anni
                    FROM 
                        employee.dbo.employees E
                        INNER JOIN employee.dbo.EmployeeHireHistory H 
                            ON e.EmployeeId = h.EmployeeId 
                            AND h.EmployeerId = 2 
                            AND h.EndWorkDate IS NULL
                        INNER JOIN [Timeclocking].[dbo].[Employee] TE 
                            ON e.EmployeeNID COLLATE Latin1_General_CI_AI = te.UniqueID COLLATE Latin1_General_CI_AI
                            AND te.DataStop IS NULL
                        INNER JOIN employee.dbo.EmployeeBadgeHistory BH 
                            ON h.EmployeeHireHistoryId = bh.EmployeeHireHistoryId 
                            AND bh.DateOut IS NULL
                        INNER JOIN employee.dbo.Badges B 
                            ON bh.BadgeID = b.BadgeId
                    WHERE 
                        h.EmployeeHireHistoryId = ?
                ),
                FerieSpettantiCTE AS (
                    SELECT 
                        C.*,
                        ISNULL((
                            SELECT TOP 1 GiorniBonus 
                            FROM BonusAnzianitaCTE 
                            WHERE noYears <= C.Anni
                            ORDER BY noYears DESC
                        ), 0) AS GiorniBonusAnzianita,
                        CASE 
                            WHEN YEAR(C.HireDate) = @Anno THEN 
                                CEILING(CAST(C.HolidayPerYear AS FLOAT) * 
                                       (DATEDIFF(DAY, C.HireDate, @DataRiferimento) + 1) / 
                                       (CASE WHEN (@Anno % 4 = 0 AND @Anno % 100 != 0) OR (@Anno % 400 = 0) 
                                             THEN 366 ELSE 365 END))
                            WHEN YEAR(C.HireDate) < @Anno THEN 
                                C.HolidayPerYear
                            ELSE 
                                0
                        END AS FerieAnnoCorrente
                    FROM CalcoloAnzianitaCTE C
                ),
                FerieSpettantiPerAnnoCTE AS (
                    SELECT 
                        F.IDEmployee,
                        YEAR(F.HireDate) + (N.n / 10) AS Anno,
                        CASE 
                            WHEN YEAR(F.HireDate) = YEAR(F.HireDate) + (N.n / 10) THEN 
                                CEILING(CAST(F.HolidayPerYear AS FLOAT) * 
                                       (DATEDIFF(DAY, F.HireDate, DATEFROMPARTS(YEAR(F.HireDate) + (N.n / 10), 12, 31)) + 1) / 
                                       (CASE WHEN ((YEAR(F.HireDate) + (N.n / 10)) % 4 = 0 AND (YEAR(F.HireDate) + (N.n / 10)) % 100 != 0) 
                                          OR ((YEAR(F.HireDate) + (N.n / 10)) % 400 = 0) 
                                             THEN 366 ELSE 365 END))
                            WHEN YEAR(F.HireDate) < YEAR(F.HireDate) + (N.n / 10) THEN 
                                F.HolidayPerYear
                            ELSE 
                                0
                        END AS FerieSpettanti
                    FROM 
                        FerieSpettantiCTE F
                        CROSS JOIN Numbers N
                    WHERE 
                        N.n % 10 = 0
                        AND (N.n / 10) <= 30
                        AND YEAR(F.HireDate) + (N.n / 10) < @Anno
                ),
                FerieSpettantiAnniPrecedentiCTE AS (
                    SELECT 
                        IDEmployee,
                        SUM(FerieSpettanti) AS TotaleFerieSpettantiAnniPrecedenti
                    FROM 
                        FerieSpettantiPerAnnoCTE
                    GROUP BY 
                        IDEmployee
                ),
                GiorniAssenzeEspansi AS (
                    SELECT 
                        D.IDEmployee,
                        D.IDRequestType,
                        DATEADD(DAY, N.n, D.DateFrom) AS DataCorrente,
                        CASE 
                            WHEN DATEADD(DAY, N.n, D.DateFrom) < @InizioAnno THEN 1
                            ELSE 0
                        END AS IsAnniPrecedenti,
                        CASE 
                            WHEN DATEADD(DAY, N.n, D.DateFrom) >= @InizioAnno 
                                AND DATEADD(DAY, N.n, D.DateFrom) <= @FineAnno THEN 1
                            ELSE 0
                        END AS IsAnnoCorrente,
                        CASE 
                            WHEN DATEPART(WEEKDAY, DATEADD(DAY, N.n, D.DateFrom)) IN (1, 7) THEN 0
                            WHEN EXISTS (
                                SELECT 1 
                                FROM FestiviCTE F 
                                WHERE F.DataFestivo = DATEADD(DAY, N.n, D.DateFrom)
                            ) THEN 0
                            ELSE 1
                        END AS IsGiornoLavorativo
                    FROM 
                        [Timeclocking].[dbo].[EmployeeRequestEntireDay] D
                        CROSS JOIN Numbers N
                    WHERE 
                        DATEADD(DAY, N.n, D.DateFrom) <= D.DateTo
                        AND D.DateFrom <= DATEADD(YEAR, 1, @FineAnno)
                ),
                FerieUsateAnniPrecedentiCTE AS (
                    SELECT 
                        IDEmployee,
                        SUM(IsGiornoLavorativo) AS FerieUsateAnniPrecedenti
                    FROM 
                        GiorniAssenzeEspansi
                    WHERE 
                        IDRequestType = 1
                        AND IsAnniPrecedenti = 1
                    GROUP BY 
                        IDEmployee
                ),
                FerieUsateAnnoCorrenteCTE AS (
                    SELECT 
                        IDEmployee,
                        SUM(IsGiornoLavorativo) AS FerieUsateAnnoCorrente
                    FROM 
                        GiorniAssenzeEspansi
                    WHERE 
                        IDRequestType = 1
                        AND IsAnnoCorrente = 1
                    GROUP BY 
                        IDEmployee
                )
                SELECT 
                    F.FerieAnnoCorrente + F.GiorniBonusAnzianita + 
                    (ISNULL(FSAP.TotaleFerieSpettantiAnniPrecedenti, 0) - ISNULL(FUAP.FerieUsateAnniPrecedenti, 0)) - 
                    ISNULL(FUAC.FerieUsateAnnoCorrente, 0) AS GiorniDisponibili
                FROM 
                    FerieSpettantiCTE F
                    LEFT JOIN FerieSpettantiAnniPrecedentiCTE FSAP ON F.IDEmployee = FSAP.IDEmployee
                    LEFT JOIN FerieUsateAnniPrecedentiCTE FUAP ON F.IDEmployee = FUAP.IDEmployee
                    LEFT JOIN FerieUsateAnnoCorrenteCTE FUAC ON F.IDEmployee = FUAC.IDEmployee
            """
            with self.db._lock:
                self.db.cursor.execute(query, current_year, employee_hire_history_id)
                result = self.db.cursor.fetchone()
            if result:
                return result.GiorniDisponibili
            return None
        except Exception as e:
            logger.warning(f"Impossibile calcolare saldo ferie: {e}")
            return None

    def _send_absence_decision_email(self, approved: bool, reason: str = None):
        """Invia email di notifica in rumeno al richiedente (TO) e ai manager/HR (CC)."""
        req = self.selected_request
        employee_hire_history_id = req.EmployeeHireHistoryId

        # Recupera email dipendente
        employee_name, to_email = self._get_employee_email(employee_hire_history_id)
        if not to_email:
            logger.warning(
                f"Email dipendente non trovata per EmployeeHireHistoryId={employee_hire_history_id}. "
                "Notifica non inviata."
            )
            return

        # Recupera CC e deduplica (rimuovi duplicati e l'indirizzo TO se presente)
        cc_emails = self._get_cc_recipients(employee_hire_history_id)
        seen = {to_email.lower()}
        cc_emails_unique = []
        for addr in cc_emails:
            if addr.lower() not in seen:
                seen.add(addr.lower())
                cc_emails_unique.append(addr)
        cc_emails = cc_emails_unique

        current_year = datetime.now().year

        # Dettagli richiesta
        request_type = req.RequestType if hasattr(req, 'RequestType') else ""
        date_start = req.DateStart.strftime('%d.%m.%Y') if req.DateStart else ""
        date_end = req.DateEnd.strftime('%d.%m.%Y') if req.DateEnd else ""
        manager_name = self.authorized_user_name or ""

        # Determina se è assenza oraria
        is_hourly = (hasattr(req, 'IsConsideredEntireDay')
                     and req.IsConsideredEntireDay == 0)

        # Testo esito in rumeno
        if approved:
            subject = f"Cererea dvs. de absență a fost APROBATĂ"
            status_color = "#28a745"
            status_text = "APROBATĂ"
            status_icon = "✔"
            decision_block = ""
        else:
            subject = f"Cererea dvs. de absență a fost RESPINSĂ"
            status_color = "#dc3545"
            status_text = "RESPINSĂ"
            status_icon = "✘"
            rejection_html = (
                f'<tr><td style="padding:6px 12px;color:#555;">Motiv refuz:</td>'
                f'<td style="padding:6px 12px;"><strong>{reason or ""}</strong></td></tr>'
            )
            decision_block = rejection_html

        # Saldo ferie: solo per richieste di congedo giornaliero (IDRequestType == 1)
        balance_block = ""
        if getattr(req, 'IDRequestType', None) == 1:
            vacation_balance = self._get_vacation_balance(employee_hire_history_id)
            if vacation_balance is not None:
                balance_block = (
                    f'<tr><td style="padding:6px 12px;color:#555;">Sold concediu disponibil ({current_year}):</td>'
                    f'<td style="padding:6px 12px;"><strong>{vacation_balance} zile</strong></td></tr>'
                )

        # Blocco date/ore: diverso per assenza oraria vs giornaliera
        if is_hourly:
            from_time_str = ''
            to_time_str = ''
            if req.FromTime is not None:
                ft = req.FromTime
                from_time_str = ft.strftime('%H:%M') if hasattr(ft, 'strftime') else str(ft)[:5]
            if req.ToTime is not None:
                tt = req.ToTime
                to_time_str = tt.strftime('%H:%M') if hasattr(tt, 'strftime') else str(tt)[:5]

            hours_display = ''
            if req.NrHours is not None:
                h = float(req.NrHours)
                hours_display = f"{h:.1f}" if h != int(h) else str(int(h))

            date_rows_html = f"""
              <tr>
                <td style="padding:6px 12px;color:#555;">Data:</td>
                <td style="padding:6px 12px;"><strong>{date_start}</strong></td>
              </tr>
              <tr style="background:#f8f9fa;">
                <td style="padding:6px 12px;color:#555;">Interval orar:</td>
                <td style="padding:6px 12px;"><strong>{from_time_str} - {to_time_str}</strong></td>
              </tr>
              <tr>
                <td style="padding:6px 12px;color:#555;">Ore:</td>
                <td style="padding:6px 12px;"><strong>{hours_display}</strong></td>
              </tr>"""
        else:
            date_rows_html = f"""
              <tr>
                <td style="padding:6px 12px;color:#555;">Data început:</td>
                <td style="padding:6px 12px;"><strong>{date_start}</strong></td>
              </tr>
              <tr style="background:#f8f9fa;">
                <td style="padding:6px 12px;color:#555;">Data sfârșit:</td>
                <td style="padding:6px 12px;"><strong>{date_end}</strong></td>
              </tr>"""

        # Path logo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir, "Logo.png")

        # Corpo HTML
        html_body = f"""
<!DOCTYPE html>
<html lang="ro">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width"></head>
<body style="margin:0;padding:0;background:#f4f6f8;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f8;padding:30px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0"
             style="background:#ffffff;border-radius:8px;overflow:hidden;
                    box-shadow:0 2px 8px rgba(0,0,0,0.08);">

        <!-- Header con logo -->
        <tr>
          <td style="background:#003366;padding:24px 32px;text-align:center;">
            <img src="cid:company_logo" alt="Company Logo"
                 style="max-height:60px;max-width:200px;" />
          </td>
        </tr>

        <!-- Banner esito -->
        <tr>
          <td style="background:{status_color};padding:16px 32px;text-align:center;">
            <span style="font-size:22px;font-weight:bold;color:#ffffff;letter-spacing:1px;">
              {status_icon}&nbsp;&nbsp;Cerere de absență {status_text}
            </span>
          </td>
        </tr>

        <!-- Salut -->
        <tr>
          <td style="padding:28px 32px 8px 32px;">
            <p style="margin:0;font-size:15px;color:#222;">Stimate/Stimată <strong>{employee_name}</strong>,</p>
            <p style="margin:12px 0 0 0;font-size:14px;color:#444;line-height:1.6;">
              Vă informăm că cererea dvs. de absență a fost
              <strong style="color:{status_color};">{status_text.lower()}</strong>
              de către <strong>{manager_name}</strong>.
            </p>
          </td>
        </tr>

        <!-- Detalii cerere -->
        <tr>
          <td style="padding:16px 32px;">
            <p style="margin:0 0 10px 0;font-size:14px;font-weight:bold;color:#003366;">Detalii cerere:</p>
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="border:1px solid #e0e0e0;border-radius:6px;font-size:14px;color:#333;">
              <tr style="background:#f8f9fa;">
                <td style="padding:6px 12px;color:#555;">Tip absență:</td>
                <td style="padding:6px 12px;"><strong>{request_type}</strong></td>
              </tr>
              {date_rows_html}
              {decision_block}
              {balance_block}
            </table>
          </td>
        </tr>

        <!-- Nota -->
        <tr>
          <td style="padding:8px 32px 28px 32px;">
            <p style="margin:0;font-size:13px;color:#888;line-height:1.5;">
              Această notificare a fost generată automat de sistemul TraceabilityRS.
              Vă rugăm să nu răspundeți la acest mesaj.
            </p>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#f0f0f0;padding:14px 32px;text-align:center;">
            <span style="font-size:12px;color:#999;">
              &copy; {current_year} Vandewiele &mdash; TraceabilityRS System
            </span>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""

        # Allegato logo inline
        attachments = []
        if os.path.exists(logo_path):
            attachments.append(('inline', logo_path, 'company_logo'))
        else:
            logger.warning(f"Logo non trovato in {logo_path}, email inviata senza logo")

        # Invia
        sender = EmailSender()
        sender.send_email(
            to_email=to_email,
            subject=subject,
            body=html_body,
            is_html=True,
            attachments=attachments if attachments else None,
            cc_emails=cc_emails if cc_emails else None
        )
        logger.info(
            f"Email notifica {'approvazione' if approved else 'rifiuto'} inviata a {to_email}"
            + (f" CC: {', '.join(cc_emails)}" if cc_emails else "")
        )


class RejectReasonDialog(tk.Toplevel):
    """Dialog per inserire la motivazione del rifiuto"""
    
    def __init__(self, parent, lang_manager, callback):
        super().__init__(parent)
        self.lang = lang_manager
        self.callback = callback
        
        self.title(self.lang.get('rejection_reason_title', 'Motivazione Rifiuto'))
        self.geometry("400x200")
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crea i widget del dialog"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        label = ttk.Label(
            main_frame,
            text=self.lang.get('enter_rejection_reason', 'Inserire la motivazione del rifiuto:'),
            font=("Helvetica", 10)
        )
        label.pack(pady=(0, 10))
        
        # Text widget per la motivazione
        self.reason_text = tk.Text(main_frame, height=5, wrap=tk.WORD)
        self.reason_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.reason_text.focus_set()
        
        # Bottoni
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ok_btn = ttk.Button(
            btn_frame,
            text=self.lang.get('ok', 'OK'),
            command=self._on_ok
        )
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(
            btn_frame,
            text=self.lang.get('cancel', 'Annulla'),
            command=self.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
    def _on_ok(self):
        """Gestisce il click su OK"""
        reason = self.reason_text.get("1.0", tk.END).strip()
        self.destroy()
        if self.callback:
            self.callback(reason)
