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

        # Stato ordinamento: {tree_widget: (colonna, reverse)}
        self._sort_state = {}

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
        columns = ('id', 'service', 'guest_name', 'flight', 'arrival_date', 'departure_date', 'service_email',
                   'sent_date', 'confirmed')
        self.booking_tree = ttk.Treeview(parent, columns=columns, show='headings',
                                          selectmode='browse', height=18)

        # Etichette originali per le colonne (usate per reset frecce)
        self._booking_col_labels = {
            'id': 'ID',
            'service': self.lang.get('col_service', 'Servizio'),
            'guest_name': self.lang.get('col_guest_name', 'Ospite'),
            'flight': self.lang.get('col_flight', 'Volo'),
            'arrival_date': self.lang.get('col_arrival_date', 'Data Arrivo'),
            'departure_date': self.lang.get('col_departure_date', 'Data Partenza'),
            'service_email': self.lang.get('col_service_email', 'Email Servizio'),
            'sent_date': self.lang.get('col_sent_date', 'Inviato'),
            'confirmed': self.lang.get('col_confirmed', 'Confermato'),
        }
        for col, label in self._booking_col_labels.items():
            self.booking_tree.heading(
                col, text=label,
                command=lambda c=col: self._sort_treeview(self.booking_tree, c, self._booking_col_labels)
            )

        self.booking_tree.column('id', width=40, anchor='center')
        self.booking_tree.column('service', width=80, anchor='center')
        self.booking_tree.column('guest_name', width=160)
        self.booking_tree.column('flight', width=120, anchor='center')
        self.booking_tree.column('arrival_date', width=120, anchor='center')
        self.booking_tree.column('departure_date', width=100, anchor='center')
        self.booking_tree.column('service_email', width=200)
        self.booking_tree.column('sent_date', width=120, anchor='center')
        self.booking_tree.column('confirmed', width=70, anchor='center')

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
                    vad.VisitorId,
                    fc.CompanyName AS AirlineName,
                    CASE 
                        WHEN EXISTS (
                            SELECT 1 FROM Employee.dbo.VisitorSupportersData vs2 
                            WHERE vs2.ReservationEmail = bse.EmailRequestBooking 
                              AND vs2.SupporterTypeID = 2 AND vs2.DateOut IS NULL
                        ) THEN 'Shuttle'
                        WHEN EXISTS (
                            SELECT 1 FROM Employee.dbo.VisitorSupportersData vs2 
                            WHERE vs2.ReservationEmail = bse.EmailRequestBooking 
                              AND vs2.SupporterTypeID = 1 AND vs2.DateOut IS NULL
                        ) THEN 'Hotel'
                        ELSE 'Guest'
                    END AS ServiceType,
                    -- JOIN diretto su VisitorId; fallback date-match per record legacy
                    CASE
                        WHEN vad.VisitorId IS NOT NULL THEN v.GuestName
                        ELSE STUFF(
                            (SELECT DISTINCT ', ' + v2.GuestName
                             FROM Employee.dbo.Visitors v2
                             WHERE CAST(v2.StartVisit AS DATE) = CAST(vad.DateTimeArrival AS DATE)
                               AND v2.EndVisit >= vad.DateOut
                             FOR XML PATH(''), TYPE
                            ).value('.', 'NVARCHAR(MAX)')
                        , 1, 2, '')
                    END AS GuestNames
                FROM Employee.dbo.VisitorBookingServiceEmails bse
                INNER JOIN Employee.dbo.VisitorArrivalDetails vad
                    ON bse.VisitorArrivalDetailId = vad.VisitorArrivalDetailId
                LEFT JOIN Employee.dbo.Visitors v
                    ON vad.VisitorId = v.VisitorId
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

                service_type = row.ServiceType if row.ServiceType else 'Ospite'
                arr_date = row.DateTimeArrival.strftime('%d/%m/%Y %H:%M') if row.DateTimeArrival else ''
                dep_date = row.DateOut.strftime('%d/%m/%Y') if row.DateOut else ''
                sent_date = row.SentOnDate.strftime('%d/%m/%Y %H:%M') if row.SentOnDate else ''
                confirmed = '✅' if row.Confirmed else '❌'
                guest_names = row.GuestNames or ''

                # Icona servizio
                service_icon = {'Hotel': '🏨 Hotel', 'Shuttle': '🚐 Shuttle'}.get(service_type, '👤 Guest')

                iid = self.booking_tree.insert('', 'end', values=(
                    booking_id, service_icon, guest_names, flight_info, arr_date, dep_date,
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
                    'service_type': service_type,
                    'guest_names': guest_names,
                }

            cursor.close()
            logger.info(f"Caricati {len(self._booking_data)} booking")

            # Applica ordinamento default: Data Arrivo DESC
            self._sort_state[id(self.booking_tree)] = ('arrival_date', False)  # pre-set per toggle a DESC
            self._sort_treeview(self.booking_tree, 'arrival_date', self._booking_col_labels)
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
        """Reinvia l'email di booking differenziando Hotel/Shuttle con dettagli specifici."""
        data = self._get_selected_booking()
        if not data:
            return

        if not data['email']:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('no_email_for_booking', 'Nessuna email associata a questo booking.'))
            return

        service_type = data.get('service_type', 'Guest')
        service_label = '🚐 Shuttle' if service_type == 'Shuttle' else '🏨 Hotel' if service_type == 'Hotel' else service_type

        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            f"Reinviare l'email di prenotazione {service_label} a {data['email']}?"):
            return

        try:
            from email_connector import EmailSender

            user_email = self._get_user_email()
            logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')

            # Recupera nome fornitore servizio dal DB
            provider_name = self._get_provider_name(data['email'])

            # Dati volo
            flight_info = ''
            if data['airline_name']:
                flight_info += f"<strong>Compagnia aerea:</strong> {data['airline_name']}<br/>"
            if data['flight_number']:
                flight_info += f"<strong>Numero volo:</strong> {data['flight_number']}<br/>"

            arr_date = data['arrival_date'].strftime('%d/%m/%Y %H:%M') if data['arrival_date'] else 'N/D'
            arr_date_short = data['arrival_date'].strftime('%d/%m/%Y') if data['arrival_date'] else 'N/D'
            dep_date = data['departure_date'].strftime('%d/%m/%Y') if data['departure_date'] else 'N/D'

            # Lista ospiti
            guest_names = data.get('guest_names', '')
            guests_html = ''
            if guest_names:
                names = [n.strip() for n in guest_names.split(',') if n.strip()]
                guests_html = '<h4>Oaspeți ({} persoane):</h4><ul>{}</ul>'.format(
                    len(names),
                    ''.join([f'<li><strong>{n}</strong></li>' for n in names])
                )

            # --- Contenuto specifico per tipo di servizio ---
            if service_type == 'Shuttle':
                title_html = '<h3 style="color: #1565C0;">🚐 Reiterare cerere transport / Transport Request Resend</h3>'
                service_details = f"""
                    {guests_html}
                    {flight_info}
                    <p><strong>Data sosire:</strong> {arr_date}</p>
                    <p><strong>Data plecare:</strong> {dep_date}</p>
                """
                if provider_name:
                    service_details = f'<p><strong>Serviciu transport:</strong> {provider_name}</p>' + service_details
                confirm_text_ro = "Vă rugăm să confirmați primirea acestei cereri de transport și că serviciul a fost rezervat."
                confirm_text_en = "Please confirm receipt of this transport request and that the service has been booked."
                subject_line = f"Reiterare Transport — {arr_date_short}"
                accent_color = '#1565C0'
                bg_color = '#FFF3E0'
                border_color = '#E65100'

            elif service_type == 'Hotel':
                # Calcola notti se possibile
                nights_html = ''
                if data['arrival_date'] and data['departure_date']:
                    num_nights = (data['departure_date'] - data['arrival_date'].date() 
                                  if hasattr(data['arrival_date'], 'date') 
                                  else data['departure_date'] - data['arrival_date']).days
                    if num_nights > 0:
                        nights_html = f'<p><strong>Număr nopți:</strong> {num_nights}</p>'

                # Numero camere = numero ospiti
                num_guests = len([n for n in guest_names.split(',') if n.strip()]) if guest_names else 1

                # Dati aziendali per fatturazione
                company_html = self._get_company_billing_html()

                title_html = '<h3 style="color: #2E7D32;">🏨 Reiterare cerere rezervare hotel / Hotel Reservation Resend</h3>'
                service_details = f"""
                    {f'<p><strong>Hotel:</strong> {provider_name}</p>' if provider_name else ''}
                    {guests_html}
                    <p><strong>Check-in:</strong> {arr_date_short}</p>
                    <p><strong>Check-out:</strong> {dep_date}</p>
                    {nights_html}
                    <p><strong>Număr camere:</strong> {num_guests}</p>
                    {company_html}
                """
                confirm_text_ro = "Vă rugăm să confirmați primirea acestei cereri de rezervare și că camerele au fost rezervate."
                confirm_text_en = "Please confirm receipt of this reservation request and that the rooms have been booked."
                subject_line = f"Reiterare Rezervare Hotel — {arr_date_short} - {dep_date}"
                accent_color = '#2E7D32'
                bg_color = '#E8F5E9'
                border_color = '#2E7D32'
            else:
                # Fallback generico
                title_html = '<h3 style="color: #1565C0;">Reiterare cerere rezervare / Booking Request Resend</h3>'
                service_details = f"""
                    {guests_html}
                    {flight_info}
                    <p><strong>Data sosire:</strong> {arr_date}</p>
                    <p><strong>Data plecare:</strong> {dep_date}</p>
                """
                confirm_text_ro = "Vă rugăm să confirmați primirea acestei cereri și că serviciul a fost rezervat."
                confirm_text_en = "Please confirm receipt of this request and that the service has been booked."
                subject_line = f"Reiterare Rezervare — {arr_date_short}"
                accent_color = '#1565C0'
                bg_color = '#FFF3E0'
                border_color = '#E65100'

            body_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; font-size: 12px;">
                <img src="cid:company_logo" alt="Logo" style="width: 150px; margin-bottom: 10px;" /><br/>
                {title_html}
                <p>Bună ziua,</p>
                <p>Vă reiterăm cererea de rezervare necunoscută ca confirmată:</p>

                {service_details}

                <div style="background-color: {bg_color}; border-left: 4px solid {border_color}; padding: 10px; margin: 15px 0;">
                    <p style="color: #B71C1C; font-weight: bold; font-size: 12px;">⚠ IMPORTANT / IMPORTANT:</p>
                    <p style="color: #333; font-size: 11px;">
                        {confirm_text_ro}<br/>
                        Vă rugăm să trimiteți confirmarea la adresa: <strong>{user_email if user_email else 'expeditorul acestui email'}</strong>
                    </p>
                    <p style="color: #333; font-size: 11px; font-style: italic;">
                        {confirm_text_en}<br/>
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

            # Aggiungi ConfirmationEmails da VisitorPlanToCharges
            confirmation_emails = self._get_confirmation_emails_by_detail(
                data.get('arrival_detail_id'))

            # Supporta email multiple separate da ';'
            email_addresses = [e.strip() for e in data['email'].split(';') if e.strip()]
            to_addr = email_addresses[0]
            extra_cc = email_addresses[1:]
            all_cc = extra_cc + ([cc] if cc else []) + confirmation_emails

            logger.info(f"Resend {service_type} email TO: {to_addr}, CC: {all_cc}")
            sender.send_email(
                to_email=to_addr,
                subject=subject_line,
                body=body_html,
                is_html=True,
                attachments=attachments if attachments else None,
                cc_emails=all_cc if all_cc else None
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
                      -- FK diretta: ospiti con VisitorArrivalDetails collegato
                      SELECT vad.VisitorId
                      FROM Employee.dbo.VisitorArrivalDetails vad
                      INNER JOIN Employee.dbo.VisitorBookingServiceEmails bse
                          ON bse.VisitorArrivalDetailId = vad.VisitorArrivalDetailId
                      WHERE vad.VisitorId IS NOT NULL
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
                WHERE s.NomeSoggetto = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self.user_name,))
            row = cursor.fetchone()
            cursor.close()
            return row.Email if row and row.Email else None
        except Exception as e:
            logger.warning(f"Impossibile recuperare email utente: {e}")
            return None

    def _get_confirmation_emails_by_detail(self, arrival_detail_id):
        """Recupera ConfirmationEmails da VisitorPlanToCharges partendo da un ArrivalDetailId.
        
        Catena: VisitorArrivalDetails.VisitorId → Visitors.VisitorDataId
        → VisitorData.VisitorPlanToChargeID → VisitorPlanToCharges.ConfirmationEmails
        
        Returns:
            Lista di indirizzi email unici, oppure lista vuota.
        """
        if not arrival_detail_id:
            return []
        emails = set()
        try:
            query = """
                SELECT DISTINCT vpc.ConfirmationEmails
                FROM Employee.dbo.VisitorArrivalDetails vad
                INNER JOIN Employee.dbo.Visitors v
                    ON vad.VisitorId = v.VisitorId
                INNER JOIN Employee.dbo.VisitorData vd
                    ON v.VisitorDataId = vd.VisitorDataID
                INNER JOIN Employee.dbo.VisitorPlanToCharges vpc
                    ON vd.VisitorPlanToChargeID = vpc.VisitorPlanToChargeID
                WHERE vad.VisitorArrivalDetailId = ?
                    AND vpc.ConfirmationEmails IS NOT NULL
                    AND vpc.ConfirmationEmails != ''
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (arrival_detail_id,))
            for row in cursor.fetchall():
                if row.ConfirmationEmails:
                    for email in row.ConfirmationEmails.replace(',', ';').split(';'):
                        email = email.strip()
                        if email and '@' in email:
                            emails.add(email)
            cursor.close()
            if emails:
                logger.info(f"ConfirmationEmails per ArrivalDetail {arrival_detail_id}: {emails}")
        except Exception as e:
            logger.warning(f"Errore recupero ConfirmationEmails: {e}")
        return list(emails)

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

        self._guests_col_labels = {
            'id': 'ID',
            'guest_name': self.lang.get('col_guest_name', 'Nome Ospite'),
            'email': 'Email',
            'phone': self.lang.get('col_phone', 'Telefono'),
            'company': self.lang.get('col_company', 'Società'),
        }
        for col, label in self._guests_col_labels.items():
            self.guests_tree.heading(
                col, text=label,
                command=lambda c=col: self._sort_treeview(self.guests_tree, c, self._guests_col_labels)
            )

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

        ttk.Label(edit_frame, text=self.lang.get('badge_number', 'Badge:')).grid(
            row=1, column=2, sticky='w', padx=5, pady=3)
        self.edit_badge_var = tk.StringVar()
        self.edit_badge_combo = ttk.Combobox(
            edit_frame,
            textvariable=self.edit_badge_var,
            width=33,
            state='readonly'
        )
        self.edit_badge_combo.grid(row=1, column=3, padx=5, pady=3, sticky='ew')

        self.badge_info_var = tk.StringVar(value='')
        ttk.Label(edit_frame, textvariable=self.badge_info_var, foreground='gray').grid(
            row=2, column=0, columnspan=2, sticky='w', padx=5, pady=(2, 0)
        )

        self.edit_worker_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            edit_frame,
            text=self.lang.get('guest_worker_flag', 'Worker'),
            variable=self.edit_worker_var,
        ).grid(row=2, column=2, sticky='w', padx=5, pady=(2, 0))

        ttk.Button(edit_frame, text=self.lang.get('btn_save_guest', '💾 Salva'),
                   command=self._save_guest_data).grid(
            row=2, column=3, padx=5, pady=3, sticky='e')

        edit_frame.columnconfigure(1, weight=1)
        edit_frame.columnconfigure(3, weight=1)

        self._selected_guest_id = None
        self._badge_values = {}

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
            self.edit_badge_var.set('')
            self.edit_badge_combo['values'] = []
            self.badge_info_var.set('')
            self.edit_worker_var.set(False)

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

            # Applica ordinamento default: Nome Ospite ASC
            self._sort_state.pop(id(self.guests_tree), None)  # reset per forzare ASC
            self._sort_treeview(self.guests_tree, 'guest_name', self._guests_col_labels)
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
        self._load_badge_combo_for_guest(self._selected_guest_id)
        self.edit_worker_var.set(self._is_worker_enabled_for_guest(self._selected_guest_id))

    def _get_guest_active_visit(self, visitor_data_id):
        """Ritorna la visita attiva/futura del visitatore per badge assignment."""
        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            SELECT TOP 1 VisitorId, CompanyName, GuestName, StartVisit, EndVisit
            FROM Employee.dbo.Visitors
            WHERE VisitorDataId = ?
              AND CAST(EndVisit AS DATE) >= CAST(GETDATE() AS DATE)
            ORDER BY EndVisit DESC, StartVisit DESC
            """,
            (visitor_data_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        return row

    def _is_worker_enabled_for_guest(self, visitor_data_id):
        """Verifica se l'ospite risulta attivo come worker in Timeclocking."""
        try:
            visit = self._get_guest_active_visit(visitor_data_id)
            if not visit:
                return False

            cursor = self.db.conn.cursor()
            cursor.execute(
                """
                SELECT TOP 1 IDEmployee
                FROM Timeclocking.dbo.Employee
                WHERE CompanyID = ?
                  AND DataStop IS NULL
                ORDER BY IDEmployee DESC
                """,
                (visit.VisitorId,),
            )
            row = cursor.fetchone()
            cursor.close()
            return bool(row)
        except Exception as e:
            logger.warning(f"Impossibile verificare stato worker per VisitorDataID={visitor_data_id}: {e}")
            return False

    def _split_guest_name(self, full_name):
        """Split nome/cognome da GuestName: prima parola nome, resto cognome.

        Se non esiste cognome, usa lo stesso valore del nome (non NULL).
        """
        text = (full_name or '').strip()
        if not text:
            return 'UNKNOWN', 'UNKNOWN'

        parts = text.split()
        name = parts[0]
        surname = ' '.join(parts[1:]).strip() if len(parts) > 1 else name
        return name, (surname or name)

    def _generate_next_fk_company_cui(self):
        """Genera CompanyCUI progressivo con prefisso FK + 8 cifre."""
        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            SELECT MAX(TRY_CONVERT(BIGINT, SUBSTRING(CompanyCUI, 3, 32))) AS MaxNum
            FROM Timeclocking.dbo.Company
            WHERE CompanyCUI LIKE 'FK%'
            """
        )
        row = cursor.fetchone()
        cursor.close()
        next_num = (int(row.MaxNum) if row and row.MaxNum is not None else 0) + 1
        return f"FK{next_num:08d}"

    def _generate_next_fk_unique_id(self):
        """Genera UniqueID progressivo con prefisso FK + 12 cifre."""
        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            SELECT MAX(TRY_CONVERT(BIGINT, SUBSTRING(UniqueID, 3, 32))) AS MaxNum
            FROM Timeclocking.dbo.Employee
            WHERE UniqueID LIKE 'FK%'
            """
        )
        row = cursor.fetchone()
        cursor.close()
        next_num = (int(row.MaxNum) if row and row.MaxNum is not None else 0) + 1
        return f"FK{next_num:012d}"

    def _get_or_create_timeclocking_company_id(self, company_name):
        """Recupera o crea la Company in Timeclocking e ritorna IDCompany."""
        if not company_name or not str(company_name).strip():
            raise ValueError(self.lang.get('worker_company_required', 'CompanyName mancante per sync Worker.'))

        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            SELECT TOP 1 IDCompany
            FROM Timeclocking.dbo.Company
            WHERE CompanyName = ?
            ORDER BY IDCompany DESC
            """,
            (company_name,),
        )
        row = cursor.fetchone()
        if row and row.IDCompany is not None:
            cursor.close()
            return int(row.IDCompany)

        company_cui = self._generate_next_fk_company_cui()
        cursor.execute(
            """
            INSERT INTO Timeclocking.dbo.Company
                (CompanyName, CompanyCUI, CompanyAddress, CompanyLogo, CompanyDestMail, IsPrimary, IsActive)
            OUTPUT INSERTED.IDCompany
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (company_name, company_cui, '', None, None, 0, 1),
        )
        created = cursor.fetchone()
        cursor.close()

        if not created or created[0] is None:
            raise ValueError(self.lang.get('worker_company_create_failed', 'Creazione Company Timeclocking fallita.'))

        return int(created[0])

    def _get_assigned_badge_code(self, visitor_data_id, reference_date):
        """Ritorna NoBadge attivo per il visitatore alla data di riferimento."""
        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            SELECT TOP 1 b.NoBadge
            FROM Employee.dbo.VisitorBadgeLogs vb
            INNER JOIN Employee.dbo.Badges b ON b.BadgeId = vb.BadgeId
            WHERE vb.VisitorDataID = ?
              AND CAST(vb.DateOut AS DATE) >= CAST(? AS DATE)
            ORDER BY vb.DateOut DESC, vb.DateIn DESC
            """,
            (visitor_data_id, reference_date),
        )
        row = cursor.fetchone()
        cursor.close()
        return (str(row.NoBadge).strip() if row and row.NoBadge is not None else None)

    def _sync_guest_worker_to_timeclocking(self, visitor_data_id):
        """Crea/riattiva il worker in Timeclocking a partire dal visitatore selezionato."""
        visit = self._get_guest_active_visit(visitor_data_id)
        if not visit:
            raise ValueError(
                self.lang.get('worker_no_active_visit', 'Nessuna visita attiva o futura per questo ospite (Worker).')
            )

        employee_name, employee_surname = self._split_guest_name(visit.GuestName)
        company_name = (visit.CompanyName or '').strip()
        company_id_tc = self._get_or_create_timeclocking_company_id(company_name)

        badge_code = self._get_assigned_badge_code(visitor_data_id, visit.StartVisit)
        if not badge_code:
            raise ValueError(
                self.lang.get('worker_badge_required', 'Per Worker=1 è obbligatorio assegnare un badge al visitatore.')
            )

        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            SELECT TOP 1 IDEmployee, UniqueID, DataStop
            FROM Timeclocking.dbo.Employee
            WHERE CompanyID = ?
            ORDER BY IDEmployee DESC
            """,
            (visit.VisitorId,),
        )
        existing = cursor.fetchone()

        unique_id = None
        if existing:
            unique_id = (existing.UniqueID or '').strip() if existing.UniqueID else ''
            if not unique_id:
                unique_id = self._generate_next_fk_unique_id()

            if existing.DataStop is not None:
                cursor.execute(
                    """
                    UPDATE Timeclocking.dbo.Employee
                    SET DataStop = NULL
                    WHERE IDEmployee = ?
                    """,
                    (existing.IDEmployee,),
                )

            cursor.execute(
                """
                UPDATE Timeclocking.dbo.Employee
                SET EmployeeName = ?,
                    EmployeeSurname = ?,
                    UniqueID = ?,
                    Department = 'Production',
                    Profession = 'TRAINER',
                    DataStart = ?,
                    CodeBadge = ?,
                    IDCompany = ?,
                    IDTeam = 135,
                    IDProfession = 2,
                    IDRuleCalculationMode = NULL,
                    IsDirect = 0
                WHERE IDEmployee = ?
                """,
                (
                    employee_name,
                    employee_surname,
                    unique_id,
                    visit.StartVisit,
                    badge_code,
                    company_id_tc,
                    existing.IDEmployee,
                ),
            )
        else:
            unique_id = self._generate_next_fk_unique_id()
            cursor.execute(
                """
                INSERT INTO Timeclocking.dbo.Employee
                    (EmployeeName, EmployeeSurname, UniqueID, CompanyID, Department,
                     Profession, DataStart, DataStop, CodeBadge, DataLastImport,
                     EmployeeSalary, IDCompany, IDTeam, IDProfession,
                     IDRuleCalculationMode, IsDirect)
                VALUES
                    (?, ?, ?, ?, 'Production',
                     'TRAINER', ?, NULL, ?, NULL,
                     NULL, ?, 135, 2,
                     NULL, 0)
                """,
                (
                    employee_name,
                    employee_surname,
                    unique_id,
                    visit.VisitorId,
                    visit.StartVisit,
                    badge_code,
                    company_id_tc,
                ),
            )

        cursor.close()

    def _get_current_badge_assignment(self, visitor_data_id, reference_date):
        """Ritorna badge attivo per questo visitatore alla data di riferimento."""
        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            SELECT TOP 1 vb.BadgeId, b.NoBadge, vb.DateOut
            FROM Employee.dbo.VisitorBadgeLogs vb
            INNER JOIN Employee.dbo.Badges b ON b.BadgeId = vb.BadgeId
            WHERE vb.VisitorDataID = ?
              AND CAST(vb.DateOut AS DATE) >= CAST(? AS DATE)
            ORDER BY vb.DateOut DESC, vb.DateIn DESC
            """,
            (visitor_data_id, reference_date),
        )
        row = cursor.fetchone()
        cursor.close()
        return row

    def _load_badge_combo_for_guest(self, visitor_data_id):
        """Carica badge disponibili + eventuale badge già assegnato al visitatore."""
        self._badge_values = {}
        self.edit_badge_var.set('')
        self.edit_badge_combo['values'] = []
        self.badge_info_var.set('')

        try:
            visit = self._get_guest_active_visit(visitor_data_id)
            if not visit:
                self.badge_info_var.set(
                    self.lang.get('guest_badge_no_active_visit', 'Nessuna visita attiva o futura per questo ospite.')
                )
                return

            reference_date = visit.StartVisit
            current_assignment = self._get_current_badge_assignment(visitor_data_id, reference_date)

            query = """
                SELECT DISTINCT TOP (1000)
                    b.BadgeId,
                    b.NoBadge
                FROM Employee.dbo.Badges b
                LEFT JOIN Employee.dbo.EmployeeBadgeHistory bh
                    ON b.BadgeId = bh.BadgeID
                WHERE ISNULL(b.ForGuest, 0) = 1
                  AND ISNULL(b.EmployeerId, 2) = 2
                  AND (
                        bh.BadgeID IS NULL
                     OR bh.DateOut IS NULL
                     OR CAST(bh.DateOut AS DATE) < CAST(? AS DATE)
                  )
                ORDER BY b.NoBadge
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (reference_date,))
            rows = cursor.fetchall()
            if not rows:
                # Fallback: se lo storico badge e' incoerente/non presente,
                # mostra comunque i badge visitatori disponibili per anagrafica.
                cursor.execute(
                    """
                    SELECT TOP (1000) b.BadgeId, b.NoBadge
                    FROM Employee.dbo.Badges b
                                        WHERE ISNULL(b.ForGuest, 0) = 1
                      AND ISNULL(b.EmployeerId, 2) = 2
                    ORDER BY b.NoBadge
                    """
                )
                rows = cursor.fetchall()
            cursor.close()

            values = ['']
            for row in rows:
                label = str(row.NoBadge)
                self._badge_values[label] = row.BadgeId
                values.append(label)

            if current_assignment and current_assignment.NoBadge:
                current_label = str(current_assignment.NoBadge)
                if current_label not in self._badge_values:
                    self._badge_values[current_label] = current_assignment.BadgeId
                    values.append(current_label)
                self.edit_badge_var.set(current_label)
                valid_to = current_assignment.DateOut.strftime('%d/%m/%Y') if current_assignment.DateOut else ''
                self.badge_info_var.set(
                    self.lang.get(
                        'guest_badge_current_assignment',
                        'Badge attuale: {0} - valido fino al {1}'
                    ).format(current_label, valid_to)
                )
            else:
                self.badge_info_var.set(
                    self.lang.get('guest_badge_available_hint', 'Seleziona un badge disponibile per il visitatore.')
                )

            self.edit_badge_combo['values'] = values
        except Exception as e:
            logger.error(f"Errore caricamento combo badge ospite: {e}", exc_info=True)
            self.badge_info_var.set(str(e))

    def _save_guest_badge_assignment(self, visitor_data_id):
        """Salva/aggiorna l'assegnazione badge visitatore."""
        selected_label = self.edit_badge_var.get().strip()
        if not selected_label:
            return

        selected_badge_id = self._badge_values.get(selected_label)
        if not selected_badge_id:
            raise ValueError(self.lang.get('select_valid_badge', 'Selezionare un badge valido.'))

        visit = self._get_guest_active_visit(visitor_data_id)
        if not visit:
            raise ValueError(
                self.lang.get('guest_badge_no_active_visit', 'Nessuna visita attiva o futura per questo ospite.')
            )

        reference_date = visit.StartVisit
        valid_up_to = visit.EndVisit
        current_assignment = self._get_current_badge_assignment(visitor_data_id, reference_date)

        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            SELECT TOP 1 VisitorDataID
            FROM Employee.dbo.VisitorBadgeLogs
            WHERE BadgeId = ?
              AND CAST(DateOut AS DATE) >= CAST(? AS DATE)
              AND VisitorDataID <> ?
            """,
            (selected_badge_id, reference_date, visitor_data_id),
        )
        busy_row = cursor.fetchone()
        if busy_row:
            cursor.close()
            raise ValueError(
                self.lang.get('badge_already_assigned', 'Il badge selezionato è già assegnato a un altro visitatore.')
            )

        if current_assignment and current_assignment.BadgeId == selected_badge_id:
            cursor.execute(
                """
                UPDATE Employee.dbo.VisitorBadgeLogs
                SET DateOut = ?
                WHERE VisitorDataID = ?
                  AND BadgeId = ?
                  AND CAST(DateOut AS DATE) >= CAST(? AS DATE)
                """,
                (valid_up_to, visitor_data_id, selected_badge_id, reference_date),
            )
            cursor.close()
            return

        if current_assignment:
            cursor.execute(
                """
                UPDATE Employee.dbo.VisitorBadgeLogs
                SET DateOut = GETDATE()
                WHERE VisitorDataID = ?
                  AND BadgeId = ?
                  AND CAST(DateOut AS DATE) >= CAST(? AS DATE)
                """,
                (visitor_data_id, current_assignment.BadgeId, reference_date),
            )

        cursor.execute(
            """
            INSERT INTO Employee.dbo.VisitorBadgeLogs (BadgeId, VisitorDataID, DateIn, DateOut)
            VALUES (?, ?, GETDATE(), ?)
            """,
            (selected_badge_id, visitor_data_id, valid_up_to),
        )
        cursor.close()

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
            cursor.close()

            self._save_guest_badge_assignment(self._selected_guest_id)

            if self.edit_worker_var.get():
                confirm_worker = messagebox.askyesno(
                    self.lang.get('confirm', 'Conferma'),
                    self.lang.get(
                        'confirm_worker_enable',
                        "Confermi che l'ospite deve avere accesso al sistema di tracciabilità come Worker?"
                    ),
                    parent=self,
                )
                if confirm_worker:
                    self._sync_guest_worker_to_timeclocking(self._selected_guest_id)
                else:
                    self.edit_worker_var.set(False)

            self.db.conn.commit()

            logger.info(f"Aggiornato ospite {self._selected_guest_id}: email={email}, tel={phone}")
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('guest_data_saved', 'Dati ospite salvati con successo.'))
            self._load_guests()
        except Exception as e:
            logger.error(f"Errore salvataggio dati ospite: {e}")
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    # ================================================================
    # HELPER METHODS
    # ================================================================
    def _get_provider_name(self, email):
        """Recupera il nome del fornitore (Hotel/Shuttle) dall'email di prenotazione."""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT vsd.Name, t.TownName
                FROM Employee.dbo.VisitorSupportersData vsd
                INNER JOIN Employee.Geo.Towns t ON vsd.CityId = t.TownId
                WHERE vsd.ReservationEmail LIKE ? AND vsd.DateOut IS NULL
            """, (f'%{email}%',))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return f"{row.Name} — {row.TownName}" if row.TownName else row.Name
        except Exception as e:
            logger.warning(f"Errore recupero nome fornitore per email {email}: {e}")
        return None

    def _get_company_billing_html(self):
        """Recupera i dati aziendali Vandewiele per la fatturazione hotel."""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT EmployeerName, [Address], t.TownName, c.CountyName,
                       EmployeerFiscalCode, ChamberOfCommercNo
                FROM Employee.dbo.Employeers e
                INNER JOIN Employee.Geo.Towns t ON e.TownId = t.TownId
                INNER JOIN Employee.Geo.Counties c ON t.CountyId = c.CountyId
                WHERE EmployeerId = 2
            """)
            row = cursor.fetchone()
            cursor.close()
            if row:
                return f"""
                <h4>Date companie gazdă:</h4>
                <table style="border-collapse: collapse;">
                    <tr><td style="padding: 3px 10px; font-weight: bold;">Companie:</td>
                        <td>{row.EmployeerName}</td></tr>
                    <tr><td style="padding: 3px 10px; font-weight: bold;">Adresă:</td>
                        <td>{row.Address}, {row.TownName}, {row.CountyName}</td></tr>
                    <tr><td style="padding: 3px 10px; font-weight: bold;">CUI:</td>
                        <td>{row.EmployeerFiscalCode}</td></tr>
                    <tr><td style="padding: 3px 10px; font-weight: bold;">Nr. Reg. Comerț:</td>
                        <td>{row.ChamberOfCommercNo}</td></tr>
                </table>
                """
        except Exception as e:
            logger.warning(f"Errore recupero dati aziendali: {e}")
        return ''

    # ================================================================
    # SORTING
    # ================================================================
    def _sort_treeview(self, tree, col, col_labels):
        """Ordina un Treeview cliccando sull'intestazione della colonna."""
        # Determina direzione: toggle se stessa colonna, altrimenti ASC
        current = self._sort_state.get(id(tree))
        if current and current[0] == col:
            reverse = not current[1]
        else:
            reverse = False

        self._sort_state[id(tree)] = (col, reverse)

        # Leggi tutti gli item
        items = [(tree.set(iid, col), iid) for iid in tree.get_children('')]

        # Ordina: prova numerico, altrimenti stringa case-insensitive
        def sort_key(item):
            val = item[0]
            try:
                return (0, float(val))
            except (ValueError, TypeError):
                return (1, val.lower() if val else '')

        items.sort(key=sort_key, reverse=reverse)

        # Riposiziona gli item
        for index, (_, iid) in enumerate(items):
            tree.move(iid, '', index)

        # Aggiorna intestazioni: reset tutte, poi freccia sulla colonna attiva
        arrow = ' ▼' if reverse else ' ▲'
        for c, label in col_labels.items():
            if c == col:
                tree.heading(c, text=label + arrow)
            else:
                tree.heading(c, text=label)

    # ================================================================
    # CLOSE
    # ================================================================
    def _on_close(self):
        """Chiude la finestra."""
        self.destroy()
