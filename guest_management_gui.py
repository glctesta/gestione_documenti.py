# -*- coding: utf-8 -*-
"""
Modulo per la gestione ospiti: booking non confermati e dati ospiti.
Apre da menu Ospiti → Settings → Gestione Ospiti.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
import os

logger = logging.getLogger("TraceabilityRS")


class GuestManagementWindow(tk.Toplevel):
    """Finestra per gestire booking non confermati e dati ospiti."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name

        self.title(self.lang.get('guest_management_title', 'Gestione Ospiti'))
        self.geometry('1100x650')
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._load_bookings()
        self._load_companies()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ================================================================
    # UI
    # ================================================================
    def _build_ui(self):
        """Costruisce l'interfaccia con 2 tab."""
        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Tab 1: Booking
        booking_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(booking_frame, text=self.lang.get('tab_bookings', '📋 Booking'))
        self._build_booking_tab(booking_frame)

        # Tab 2: Dati Ospiti
        guests_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(guests_frame, text=self.lang.get('tab_guest_data', '👤 Dati Ospiti'))
        self._build_guests_tab(guests_frame)

        # Pulsante Chiudi
        btn_frame = ttk.Frame(self, padding=5)
        btn_frame.pack(fill='x', padx=10, pady=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_close', 'Chiudi'),
                   command=self._on_close).pack(side='right', padx=5)

    # ================================================================
    # TAB 1 — BOOKING
    # ================================================================
    def _build_booking_tab(self, parent):
        """Tab booking non confermati."""
        # Toolbar
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill='x', pady=(0, 5))

        self.show_all_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(toolbar,
            text=self.lang.get('show_all_bookings', 'Mostra anche confermati'),
            variable=self.show_all_var,
            command=self._load_bookings).pack(side='left', padx=5)

        ttk.Button(toolbar, text=self.lang.get('btn_refresh', '🔄 Aggiorna'),
                   command=self._load_bookings).pack(side='right', padx=5)
        ttk.Button(toolbar, text=self.lang.get('btn_confirm_booking', '✅ Segna Confermato'),
                   command=self._confirm_booking).pack(side='right', padx=5)
        ttk.Button(toolbar, text=self.lang.get('btn_resend_email', '📧 Reinvia Email'),
                   command=self._resend_booking_email).pack(side='right', padx=5)
        ttk.Button(toolbar, text=self.lang.get('btn_generate_booking', '➕ Genera Booking'),
                   command=self._generate_booking).pack(side='right', padx=5)

        # TreeView
        columns = ('id', 'flight', 'arrival_date', 'departure_date', 'service_email',
                   'sent_date', 'confirmed')
        self.booking_tree = ttk.Treeview(parent, columns=columns, show='headings',
                                          selectmode='browse', height=18)

        self.booking_tree.heading('id', text='ID')
        self.booking_tree.heading('flight', text=self.lang.get('col_flight', 'Volo'))
        self.booking_tree.heading('arrival_date', text=self.lang.get('col_arrival_date', 'Data Arrivo'))
        self.booking_tree.heading('departure_date', text=self.lang.get('col_departure_date', 'Data Partenza'))
        self.booking_tree.heading('service_email', text=self.lang.get('col_service_email', 'Email Servizio'))
        self.booking_tree.heading('sent_date', text=self.lang.get('col_sent_date', 'Inviato'))
        self.booking_tree.heading('confirmed', text=self.lang.get('col_confirmed', 'Confermato'))

        self.booking_tree.column('id', width=50, anchor='center')
        self.booking_tree.column('flight', width=120, anchor='center')
        self.booking_tree.column('arrival_date', width=130, anchor='center')
        self.booking_tree.column('departure_date', width=130, anchor='center')
        self.booking_tree.column('service_email', width=250)
        self.booking_tree.column('sent_date', width=140, anchor='center')
        self.booking_tree.column('confirmed', width=80, anchor='center')

        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.booking_tree.yview)
        self.booking_tree.configure(yscrollcommand=scrollbar.set)
        self.booking_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Dati interni: {iid: {booking_id, arrival_detail_id, email, ...}}
        self._booking_data = {}

    def _load_bookings(self):
        """Carica i booking dalla DB."""
        try:
            self.booking_tree.delete(*self.booking_tree.get_children())
            self._booking_data = {}

            show_all = self.show_all_var.get()

            query = """
                SELECT
                    bse.VisitorCBookingServiceEmailId,
                    bse.VisitorArrivalDetailId,
                    bse.EmailRequestBooking,
                    bse.SentOnDate,
                    bse.Confirmed,
                    vad.FlightNumber,
                    vad.DateTimeArrival,
                    vad.DateOut,
                    fc.CompanyName AS AirlineName
                FROM Employee.dbo.VisitorBookingServiceEmails bse
                INNER JOIN Employee.dbo.VisitorArrivalDetails vad
                    ON bse.VisitorArrivalDetailId = vad.VisitorArrivalDetailId
                LEFT JOIN Employee.dbo.FlyghtCompanies fc
                    ON vad.FlightCompanyId = fc.FlightCompanyId
            """
            if not show_all:
                query += " WHERE bse.Confirmed = 0"
            query += " ORDER BY bse.SentOnDate DESC"

            cursor = self.db.conn.cursor()
            cursor.execute(query)

            for row in cursor.fetchall():
                booking_id = row.VisitorCBookingServiceEmailId
                flight_info = row.FlightNumber or ''
                if row.AirlineName:
                    flight_info = f"{row.AirlineName} {flight_info}"

                arr_date = row.DateTimeArrival.strftime('%d/%m/%Y %H:%M') if row.DateTimeArrival else ''
                dep_date = row.DateOut.strftime('%d/%m/%Y') if row.DateOut else ''
                sent_date = row.SentOnDate.strftime('%d/%m/%Y %H:%M') if row.SentOnDate else ''
                confirmed = '✅' if row.Confirmed else '❌'

                iid = self.booking_tree.insert('', 'end', values=(
                    booking_id, flight_info, arr_date, dep_date,
                    row.EmailRequestBooking or '', sent_date, confirmed
                ))

                self._booking_data[iid] = {
                    'booking_id': booking_id,
                    'arrival_detail_id': row.VisitorArrivalDetailId,
                    'email': row.EmailRequestBooking,
                    'confirmed': row.Confirmed,
                    'flight_number': row.FlightNumber,
                    'airline_name': row.AirlineName,
                    'arrival_date': row.DateTimeArrival,
                    'departure_date': row.DateOut,
                }

            cursor.close()
            logger.info(f"Caricati {len(self._booking_data)} booking")
        except Exception as e:
            logger.error(f"Errore caricamento booking: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    def _get_selected_booking(self):
        """Ritorna i dati del booking selezionato o None."""
        sel = self.booking_tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_booking', 'Selezionare un booking dalla lista.'))
            return None
        return self._booking_data.get(sel[0])

    def _confirm_booking(self):
        """Segna un booking come confermato."""
        data = self._get_selected_booking()
        if not data:
            return
        if data['confirmed']:
            messagebox.showinfo(
                self.lang.get('info', 'Informazione'),
                self.lang.get('already_confirmed', 'Questo booking è già confermato.'))
            return

        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                UPDATE Employee.dbo.VisitorBookingServiceEmails
                SET Confirmed = 1
                WHERE VisitorCBookingServiceEmailId = ?
            """, (data['booking_id'],))
            self.db.conn.commit()
            cursor.close()
            logger.info(f"Booking {data['booking_id']} confermato")
            self._load_bookings()
        except Exception as e:
            logger.error(f"Errore conferma booking: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    def _resend_booking_email(self):
        """Reinvia l'email di booking."""
        data = self._get_selected_booking()
        if not data:
            return

        if not data['email']:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('no_email_for_booking', 'Nessuna email associata a questo booking.'))
            return

        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_resend',
                          f"Reinviare l'email di prenotazione a {data['email']}?")):
            return

        try:
            from email_connector import EmailSender

            user_email = self._get_user_email()
            logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')

            # Determina se è shuttle o hotel dal tipo di servizio (email)
            flight_info = ''
            if data['airline_name']:
                flight_info += f"<strong>Compagnia:</strong> {data['airline_name']}<br/>"
            if data['flight_number']:
                flight_info += f"<strong>Volo:</strong> {data['flight_number']}<br/>"

            arr_date = data['arrival_date'].strftime('%d/%m/%Y %H:%M') if data['arrival_date'] else 'N/D'
            dep_date = data['departure_date'].strftime('%d/%m/%Y') if data['departure_date'] else 'N/D'

            body_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; font-size: 12px;">
                <img src="cid:company_logo" alt="Logo" style="width: 150px; margin-bottom: 10px;" /><br/>
                <h3 style="color: #1565C0;">Reiterare cerere rezervare / Booking Request Resend</h3>
                <p>Bună ziua,</p>
                <p>Vă reiterăm cererea de rezervare necunoscută ca confirmată:</p>

                {flight_info}
                <p><strong>Data sosire:</strong> {arr_date}</p>
                <p><strong>Data plecare:</strong> {dep_date}</p>

                <div style="background-color: #FFF3E0; border-left: 4px solid #E65100; padding: 10px; margin: 15px 0;">
                    <p style="color: #B71C1C; font-weight: bold; font-size: 12px;">⚠ IMPORTANT / IMPORTANT:</p>
                    <p style="color: #333; font-size: 11px;">
                        Vă rugăm să confirmați primirea acestei cereri și că serviciul a fost rezervat.<br/>
                        Vă rugăm să trimiteți confirmarea la adresa: <strong>{user_email if user_email else 'expeditorul acestui email'}</strong>
                    </p>
                    <p style="color: #333; font-size: 11px; font-style: italic;">
                        Please confirm receipt of this request and that the service has been booked.<br/>
                        Please send confirmation to: <strong>{user_email if user_email else 'the sender of this email'}</strong>
                    </p>
                </div>

                <hr style="border: 1px solid #ddd;"/>
                <p style="color: #888; font-size: 10px;">
                    Email generată automat de TraceabilityRS — {self.user_name}</p>
            </body>
            </html>
            """

            sender = EmailSender()
            attachments = []
            if os.path.exists(logo_path):
                attachments.append(('inline', logo_path, 'company_logo'))

            cc = user_email if user_email else None

            sender.send_email(
                to_email=data['email'],
                subject=f"Reiterare Rezervare — {arr_date}",
                body=body_html,
                is_html=True,
                attachments=attachments if attachments else None,
                cc_emails=cc
            )

            # Aggiorna SentOnDate
            cursor = self.db.conn.cursor()
            cursor.execute("""
                UPDATE Employee.dbo.VisitorBookingServiceEmails
                SET SentOnDate = GETDATE()
                WHERE VisitorCBookingServiceEmailId = ?
            """, (data['booking_id'],))
            self.db.conn.commit()
            cursor.close()

            logger.info(f"Email reinviata a {data['email']} per booking {data['booking_id']}")
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('email_resent', f"Email reinviata a {data['email']}"))
            self._load_bookings()

        except Exception as e:
            logger.error(f"Errore reinvio email: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")
    def _generate_booking(self):
        """Genera booking per ospiti attivi (correnti/futuri) senza prenotazione."""
        try:
            from datetime import date
            today = date.today()

            # Trova ospiti con visita corrente/futura che NON hanno booking
            query = """
                SELECT
                    v.VisitorId,
                    v.GuestName,
                    v.CompanyName,
                    v.StartVisit,
                    v.EndVisit,
                    v.SponsorGuy,
                    vd.EmailAddress
                FROM Employee.dbo.Visitors v
                LEFT JOIN Employee.dbo.VisitorData vd
                    ON v.VisitorDataId = vd.VisitorDataID
                WHERE v.EndVisit >= ?
                  AND v.VisitorId NOT IN (
                      SELECT DISTINCT v2.VisitorId
                      FROM Employee.dbo.Visitors v2
                      INNER JOIN Employee.dbo.VisitorArrivalDetails vad
                          ON CAST(v2.StartVisit AS DATE) = CAST(vad.DateTimeArrival AS DATE)
                      INNER JOIN Employee.dbo.VisitorBookingServiceEmails bse
                          ON bse.VisitorArrivalDetailId = vad.VisitorArrivalDetailId
                  )
                ORDER BY v.StartVisit, v.GuestName
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (today,))

            visitors = []
            for row in cursor.fetchall():
                visitors.append({
                    'visitor_id': row.VisitorId,
                    'guest_name': row.GuestName or '',
                    'company': row.CompanyName or '',
                    'start_visit': row.StartVisit,
                    'end_visit': row.EndVisit,
                    'sponsor': row.SponsorGuy or '',
                    'email': row.EmailAddress or ''
                })
            cursor.close()

            if not visitors:
                messagebox.showinfo(
                    self.lang.get('info', 'Informazione'),
                    self.lang.get('no_visitors_without_booking',
                                  'Tutti gli ospiti attivi hanno già una prenotazione.'))
                return

            # Raggruppa per data di arrivo
            from collections import defaultdict
            groups = defaultdict(list)
            for v in visitors:
                key = v['start_visit'].strftime('%d/%m/%Y') if v['start_visit'] else '?'
                groups[key].append(v)

            # Mostra dialog di selezione
            sel_win = tk.Toplevel(self)
            sel_win.title(self.lang.get('select_guests_booking', 'Seleziona ospiti per booking'))
            sel_win.geometry('550x400')
            sel_win.transient(self)
            sel_win.grab_set()

            ttk.Label(sel_win,
                text=self.lang.get('guests_without_booking',
                    f'{len(visitors)} ospiti senza prenotazione:'),
                font=('Arial', 10, 'bold')).pack(padx=10, pady=5, anchor='w')

            # Treeview con checkbox via tag
            cols = ('sel', 'guest', 'company', 'arrival', 'departure')
            tree = ttk.Treeview(sel_win, columns=cols, show='headings', height=12)
            tree.heading('sel', text='✓')
            tree.heading('guest', text=self.lang.get('col_guest_name', 'Ospite'))
            tree.heading('company', text=self.lang.get('col_company', 'Società'))
            tree.heading('arrival', text=self.lang.get('col_arrival_date', 'Arrivo'))
            tree.heading('departure', text=self.lang.get('col_departure_date', 'Partenza'))
            tree.column('sel', width=30, anchor='center')
            tree.column('guest', width=180)
            tree.column('company', width=150)
            tree.column('arrival', width=90, anchor='center')
            tree.column('departure', width=90, anchor='center')

            # Inserisci tutti deselezionati di default
            selected_items = set()
            for v in visitors:
                arr = v['start_visit'].strftime('%d/%m/%Y') if v['start_visit'] else ''
                dep = v['end_visit'].strftime('%d/%m/%Y') if v['end_visit'] else ''
                iid = tree.insert('', 'end', values=(
                    '☐', v['guest_name'], v['company'], arr, dep
                ))

            def toggle_selection(event):
                item = tree.identify_row(event.y)
                if item:
                    vals = list(tree.item(item, 'values'))
                    if item in selected_items:
                        selected_items.discard(item)
                        vals[0] = '☐'
                    else:
                        selected_items.add(item)
                        vals[0] = '☑'
                    tree.item(item, values=vals)

            tree.bind('<Button-1>', toggle_selection)
            tree.pack(fill='both', expand=True, padx=10, pady=5)

            def on_generate():
                # Raccogli ospiti selezionati
                chosen = []
                for i, v in enumerate(visitors):
                    iid = tree.get_children()[i]
                    if iid in selected_items:
                        chosen.append(v)

                if not chosen:
                    messagebox.showwarning(
                        self.lang.get('warning', 'Attenzione'),
                        self.lang.get('select_at_least_one', 'Selezionare almeno un ospite.'))
                    return

                sel_win.destroy()

                # Raggruppa per data arrivo e apri booking sequenziale
                grp = defaultdict(list)
                for c in chosen:
                    key = str(c.get('start_visit', ''))
                    grp[key].append(c)

                booking_groups = list(grp.values())
                self._pending_booking_groups = booking_groups
                self._pending_booking_index = 0
                self._open_pending_booking()

            btn_frame = ttk.Frame(sel_win)
            btn_frame.pack(fill='x', padx=10, pady=10)
            ttk.Button(btn_frame,
                text=self.lang.get('btn_generate_booking', '➕ Genera Booking'),
                command=on_generate).pack(side='right', padx=5)
            ttk.Button(btn_frame,
                text=self.lang.get('btn_cancel', 'Annulla'),
                command=sel_win.destroy).pack(side='right', padx=5)

        except Exception as e:
            logger.error(f"Errore genera booking: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    def _open_pending_booking(self):
        """Apre il booking form per il prossimo gruppo."""
        from guest_booking_gui import GuestBookingWindow

        if self._pending_booking_index >= len(self._pending_booking_groups):
            self._load_bookings()
            messagebox.showinfo(
                self.lang.get('info', 'Informazione'),
                self.lang.get('all_bookings_generated', 'Tutti i booking sono stati generati.'))
            return

        group = self._pending_booking_groups[self._pending_booking_index]
        self._pending_booking_index += 1

        GuestBookingWindow(
            self, self.db, self.lang, self.user_name,
            group,
            on_close_callback=self._open_pending_booking
        )

    def _get_user_email(self):
        """Recupera l'email dell'utente loggato."""
        try:
            query = """
                SELECT TOP 1 s.Email
                FROM Traceability_RS.dbo.vw_Soggetti s
                WHERE s.Cognome + ' ' + s.Nome = ?
                   OR s.Nome + ' ' + s.Cognome = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self.user_name, self.user_name))
            row = cursor.fetchone()
            cursor.close()
            return row.Email if row and row.Email else None
        except Exception as e:
            logger.warning(f"Impossibile recuperare email utente: {e}")
            return None

    # ================================================================
    # TAB 2 — DATI OSPITI
    # ================================================================
    def _build_guests_tab(self, parent):
        """Tab per modificare email/telefono degli ospiti."""
        # Toolbar: filtro per compagnia
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill='x', pady=(0, 5))

        ttk.Label(toolbar, text=self.lang.get('filter_company', 'Filtra per società:')).pack(
            side='left', padx=5)
        self.company_filter_var = tk.StringVar()
        self.company_filter_combo = ttk.Combobox(toolbar, textvariable=self.company_filter_var,
                                                   state='readonly', width=30)
        self.company_filter_combo.pack(side='left', padx=5)
        self.company_filter_combo.bind('<<ComboboxSelected>>', lambda e: self._load_guests())

        ttk.Button(toolbar, text=self.lang.get('btn_show_all', 'Mostra Tutti'),
                   command=self._show_all_guests).pack(side='left', padx=5)

        ttk.Button(toolbar, text=self.lang.get('btn_refresh', '🔄 Aggiorna'),
                   command=self._load_guests).pack(side='right', padx=5)

        # TreeView
        columns = ('id', 'guest_name', 'email', 'phone', 'company')
        self.guests_tree = ttk.Treeview(parent, columns=columns, show='headings',
                                         selectmode='browse', height=14)

        self.guests_tree.heading('id', text='ID')
        self.guests_tree.heading('guest_name', text=self.lang.get('col_guest_name', 'Nome Ospite'))
        self.guests_tree.heading('email', text='Email')
        self.guests_tree.heading('phone', text=self.lang.get('col_phone', 'Telefono'))
        self.guests_tree.heading('company', text=self.lang.get('col_company', 'Società'))

        self.guests_tree.column('id', width=50, anchor='center')
        self.guests_tree.column('guest_name', width=200)
        self.guests_tree.column('email', width=250)
        self.guests_tree.column('phone', width=150)
        self.guests_tree.column('company', width=200)

        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.guests_tree.yview)
        self.guests_tree.configure(yscrollcommand=scrollbar.set)
        self.guests_tree.pack(fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.guests_tree.bind('<<TreeviewSelect>>', self._on_guest_selected)

        # Form di modifica
        edit_frame = ttk.LabelFrame(parent, text=self.lang.get('edit_guest', 'Modifica Ospite'),
                                     padding=10)
        edit_frame.pack(fill='x', pady=(10, 0))

        ttk.Label(edit_frame, text=self.lang.get('guest_name', 'Nome:')).grid(
            row=0, column=0, sticky='w', padx=5, pady=3)
        self.edit_name_var = tk.StringVar()
        self.edit_name_entry = ttk.Entry(edit_frame, textvariable=self.edit_name_var,
                                          width=40, state='readonly')
        self.edit_name_entry.grid(row=0, column=1, padx=5, pady=3, sticky='ew')

        ttk.Label(edit_frame, text='Email:').grid(
            row=0, column=2, sticky='w', padx=5, pady=3)
        self.edit_email_var = tk.StringVar()
        ttk.Entry(edit_frame, textvariable=self.edit_email_var, width=35).grid(
            row=0, column=3, padx=5, pady=3, sticky='ew')

        ttk.Label(edit_frame, text=self.lang.get('phone', 'Telefono:')).grid(
            row=1, column=0, sticky='w', padx=5, pady=3)
        self.edit_phone_var = tk.StringVar()
        ttk.Entry(edit_frame, textvariable=self.edit_phone_var, width=25).grid(
            row=1, column=1, padx=5, pady=3, sticky='w')

        ttk.Button(edit_frame, text=self.lang.get('btn_save_guest', '💾 Salva'),
                   command=self._save_guest_data).grid(
            row=1, column=3, padx=5, pady=3, sticky='e')

        edit_frame.columnconfigure(1, weight=1)
        edit_frame.columnconfigure(3, weight=1)

        self._selected_guest_id = None

    def _load_companies(self):
        """Carica le società per il filtro."""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT DISTINCT vpc.VisitorPlanToChargeID, vpc.CompanyName
                FROM Employee.dbo.VisitorPlanToCharges vpc
                WHERE vpc.CompanyName IS NOT NULL
                ORDER BY vpc.CompanyName
            """)
            companies = []
            self._company_ids = {}
            for row in cursor.fetchall():
                companies.append(row.CompanyName)
                self._company_ids[row.CompanyName] = row.VisitorPlanToChargeID
            self.company_filter_combo['values'] = companies
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento società: {e}")

    def _show_all_guests(self):
        """Mostra tutti gli ospiti senza filtro."""
        self.company_filter_var.set('')
        self._load_guests()

    def _load_guests(self):
        """Carica gli ospiti dalla DB, opzionalmente filtrati per società."""
        try:
            self.guests_tree.delete(*self.guests_tree.get_children())
            self._selected_guest_id = None
            self.edit_name_var.set('')
            self.edit_email_var.set('')
            self.edit_phone_var.set('')

            company = self.company_filter_var.get().strip()
            plan_id = self._company_ids.get(company) if company else None

            query = """
                SELECT
                    vd.VisitorDataID, vd.GuestName, vd.EmailAddress,
                    vd.TelephonNumber, vpc.CompanyName
                FROM Employee.dbo.VisitorData vd
                LEFT JOIN Employee.dbo.VisitorPlanToCharges vpc
                    ON vd.VisitorPlanToChargeID = vpc.VisitorPlanToChargeID
                WHERE vd.DateOut IS NULL
            """
            params = []
            if plan_id:
                query += " AND vd.VisitorPlanToChargeID = ?"
                params.append(plan_id)

            query += " ORDER BY vd.GuestName"

            cursor = self.db.conn.cursor()
            cursor.execute(query, params)

            for row in cursor.fetchall():
                self.guests_tree.insert('', 'end', values=(
                    row.VisitorDataID,
                    row.GuestName or '',
                    row.EmailAddress or '',
                    row.TelephonNumber or '',
                    row.CompanyName or ''
                ))

            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento ospiti: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    def _on_guest_selected(self, event=None):
        """Popola i campi di modifica con l'ospite selezionato."""
        sel = self.guests_tree.selection()
        if not sel:
            return
        values = self.guests_tree.item(sel[0], 'values')
        if not values:
            return

        self._selected_guest_id = int(values[0])
        self.edit_name_var.set(values[1])
        self.edit_email_var.set(values[2])
        self.edit_phone_var.set(values[3])

    def _save_guest_data(self):
        """Salva email e telefono dell'ospite selezionato."""
        if not self._selected_guest_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_guest', 'Selezionare un ospite dalla lista.'))
            return

        email = self.edit_email_var.get().strip()
        phone = self.edit_phone_var.get().strip()

        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                UPDATE Employee.dbo.VisitorData
                SET EmailAddress = ?, TelephonNumber = ?
                WHERE VisitorDataID = ?
            """, (email or None, phone or None, self._selected_guest_id))
            self.db.conn.commit()
            cursor.close()

            logger.info(f"Aggiornato ospite {self._selected_guest_id}: email={email}, tel={phone}")
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('guest_data_saved', 'Dati ospite salvati con successo.'))
            self._load_guests()
        except Exception as e:
            logger.error(f"Errore salvataggio dati ospite: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    # ================================================================
    # CLOSE
    # ================================================================
    def _on_close(self):
        """Chiude la finestra."""
        self.destroy()
