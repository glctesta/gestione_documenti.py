# -*- coding: utf-8 -*-
"""
Modulo per la gestione booking ospiti (voli, shuttle, hotel).
Si apre automaticamente alla chiusura di GuestRegistrationWindow
quando ci sono ospiti registrati nella sessione.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger("TraceabilityRS")


class GuestBookingWindow(tk.Toplevel):
    """Finestra per gestire booking: volo, shuttle, hotel per gli ospiti registrati."""

    def __init__(self, parent, db, lang, user_name, guests_data, on_close_callback=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.guests_data = guests_data  # Lista dizionari ospiti dalla sessione
        self.on_close_callback = on_close_callback
        # Titolo con nomi ospiti e data arrivo per chiarezza
        guest_names = ', '.join([g.get('guest_name', '?') for g in guests_data[:3]])
        if len(guests_data) > 3:
            guest_names += f' +{len(guests_data) - 3}'
        arrival_info = ''
        if guests_data:
            sv = guests_data[0].get('start_visit', '')
            if sv:
                try:
                    from datetime import datetime as _dt
                    if isinstance(sv, str):
                        arrival_info = f" — Arrivo: {_dt.strptime(sv, '%Y-%m-%d').strftime('%d/%m/%Y')}"
                    else:
                        arrival_info = f" — Arrivo: {sv.strftime('%d/%m/%Y')}"
                except:
                    arrival_info = f" — {sv}"
        self.title(f"{self.lang.get('guest_booking_title', 'Booking Ospiti')}: {guest_names}{arrival_info}")
        self.geometry('900x750')
        self.transient(parent)
        self.grab_set()

        # Dati compagnie aeree
        self._airline_ids = {}  # {CompanyName: (FlightCompanyId, FlightIdentifyCode)}
        # Dati supporters
        self._shuttle_data = {}  # {Name: (SupporterDataId, ReservationEmail, TownName)}
        self._hotel_data = {}    # {Name: (SupporterDataId, ReservationEmail, TownName)}
        # Dati aziendali
        self._company_info = None

        self._build_ui()
        self._load_airlines()
        self._load_supporters()
        self._load_company_info()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ================================================================
    # UI
    # ================================================================
    def _build_ui(self):
        """Costruisce l'interfaccia con 3 sezioni: Volo, Shuttle, Hotel."""
        # Header con lista ospiti
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        guests_names = ', '.join([g['guest_name'] for g in self.guests_data])
        ttk.Label(header, text=f"  |  {self.lang.get('guests', 'Ospiti')}: {guests_names}",
                  font=('Arial', 9)).pack(side='left', padx=10)

        # Notebook per le sezioni
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # --- Tab 1: Volo ---
        flight_frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(flight_frame, text=self.lang.get('flight_tab', '✈ Volo'))
        self._build_flight_section(flight_frame)

        # --- Tab 2: Shuttle ---
        shuttle_frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(shuttle_frame, text=self.lang.get('shuttle_tab', '🚐 Shuttle'))
        self._build_shuttle_section(shuttle_frame)

        # --- Tab 3: Hotel ---
        hotel_frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(hotel_frame, text=self.lang.get('hotel_tab', '🏨 Hotel'))
        self._build_hotel_section(hotel_frame)

        # Pulsanti in basso
        btn_frame = ttk.Frame(self, padding=10)
        btn_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(btn_frame, text=self.lang.get('btn_send_bookings', '📧 Invia Prenotazioni'),
                   command=self._send_all_bookings).pack(side='right', padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_skip_booking', 'Salta Booking'),
                   command=self._on_close).pack(side='right', padx=5)

    def _build_flight_section(self, parent):
        """Sezione informazioni volo."""
        row = 0

        # Compagnia aerea
        ttk.Label(parent, text=self.lang.get('airline', 'Compagnia Aerea')).grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.airline_var = tk.StringVar()
        self.airline_combo = ttk.Combobox(parent, textvariable=self.airline_var, width=40)
        self.airline_combo.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        self._all_airlines = []
        self.airline_var.trace('w', self._filter_airlines)
        row += 1

        # Numero volo
        ttk.Label(parent, text=self.lang.get('flight_number', 'Numero Volo')).grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.flight_number_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.flight_number_var, width=20).grid(
            row=row, column=1, padx=5, pady=5, sticky='w')
        ttk.Button(parent, text=self.lang.get('btn_search_flight', '🔍 Cerca Orario'),
                   command=self._search_flight_time).grid(row=row, column=2, padx=5, pady=5)
        row += 1

        # Data arrivo (default = start_visit del primo ospite)
        default_date = self.guests_data[0]['start_visit'] if self.guests_data else datetime.now().date()
        ttk.Label(parent, text=self.lang.get('arrival_date', 'Data Arrivo')).grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.arrival_date = DateEntry(parent, width=20, background='darkblue',
                                      foreground='white', borderwidth=2,
                                      date_pattern='yyyy-mm-dd')
        self.arrival_date.set_date(default_date)
        self.arrival_date.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        self.arrival_date.bind('<<DateEntrySelected>>', self._validate_arrival_date)
        row += 1

        # Ora arrivo
        ttk.Label(parent, text=self.lang.get('arrival_time', 'Ora Arrivo (HH:MM)')).grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.arrival_time_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.arrival_time_var, width=10).grid(
            row=row, column=1, padx=5, pady=5, sticky='w')
        row += 1

        # Data partenza (default = end_visit del primo ospite)
        default_end = self.guests_data[0]['end_visit'] if self.guests_data else datetime.now().date()
        ttk.Label(parent, text=self.lang.get('departure_date', 'Data Partenza')).grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.departure_date = DateEntry(parent, width=20, background='darkblue',
                                         foreground='white', borderwidth=2,
                                         date_pattern='yyyy-mm-dd')
        self.departure_date.set_date(default_end)
        self.departure_date.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        self.departure_date.bind('<<DateEntrySelected>>', self._validate_departure_date)
        row += 1

        # Ora partenza
        ttk.Label(parent, text=self.lang.get('departure_time', 'Ora Partenza (HH:MM)')).grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.departure_time_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.departure_time_var, width=10).grid(
            row=row, column=1, padx=5, pady=5, sticky='w')

        parent.columnconfigure(1, weight=1)

    def _validate_arrival_date(self, event=None):
        """Valida la data di arrivo: non può essere nel passato."""
        today = datetime.now().date()
        arrival = self.arrival_date.get_date()
        if arrival < today:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('arrival_not_past', 'La data di arrivo non può essere nel passato.')
            )
            self.arrival_date.set_date(today)
        # Aggiorna anche partenza se necessario
        departure = self.departure_date.get_date()
        if departure < self.arrival_date.get_date():
            self.departure_date.set_date(self.arrival_date.get_date())

    def _validate_departure_date(self, event=None):
        """Valida la data di partenza: non può essere anteriore alla data di arrivo."""
        arrival = self.arrival_date.get_date()
        departure = self.departure_date.get_date()
        if departure < arrival:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('departure_before_arrival',
                              'La data di partenza non può essere anteriore alla data di arrivo.')
            )
            self.departure_date.set_date(arrival)

    def _build_shuttle_section(self, parent):
        """Sezione prenotazione shuttle."""
        row = 0

        # Checkbox per skippare il servizio shuttle
        self.skip_shuttle_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(parent,
            text=self.lang.get('skip_shuttle', 'Non richiedere servizio shuttle'),
            variable=self.skip_shuttle_var).grid(
            row=row, column=0, columnspan=2, sticky='w', padx=5, pady=(5, 10))
        row += 1

        ttk.Label(parent, text=self.lang.get('select_shuttle', 'Servizio Shuttle')).grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.shuttle_var = tk.StringVar()
        self.shuttle_combo = ttk.Combobox(parent, textvariable=self.shuttle_var,
                                           state='readonly', width=40)
        self.shuttle_combo.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        row += 1

        ttk.Label(parent, text=self.lang.get('shuttle_notes', 'Note Shuttle')).grid(
            row=row, column=0, sticky='nw', padx=5, pady=5)
        self.shuttle_notes = tk.Text(parent, height=4, width=40)
        self.shuttle_notes.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        row += 1

        # Info box
        info_label = ttk.Label(parent,
            text=self.lang.get('shuttle_info',
                '⚠ Se l\'arrivo è dopo le 16:00 la destinazione sarà l\'Hotel.\n'
                'Altrimenti la destinazione sarà la fabbrica.'),
            foreground='#B22222', font=('Arial', 9, 'italic'))
        info_label.grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=10)

        parent.columnconfigure(1, weight=1)

    def _build_hotel_section(self, parent):
        """Sezione prenotazione hotel."""
        row = 0

        # Checkbox per skippare il servizio hotel
        self.skip_hotel_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(parent,
            text=self.lang.get('skip_hotel', 'Non richiedere servizio hotel'),
            variable=self.skip_hotel_var).grid(
            row=row, column=0, columnspan=2, sticky='w', padx=5, pady=(5, 10))
        row += 1

        ttk.Label(parent, text=self.lang.get('select_hotel', 'Hotel')).grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.hotel_var = tk.StringVar()
        self.hotel_combo = ttk.Combobox(parent, textvariable=self.hotel_var,
                                         state='readonly', width=40)
        self.hotel_combo.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        row += 1

        # Date check-in / check-out
        default_start = self.guests_data[0]['start_visit'] if self.guests_data else datetime.now().date()
        default_end = self.guests_data[0]['end_visit'] if self.guests_data else datetime.now().date()

        ttk.Label(parent, text='Check-in').grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.checkin_date = DateEntry(parent, width=20, background='darkblue',
                                      foreground='white', borderwidth=2,
                                      date_pattern='yyyy-mm-dd')
        self.checkin_date.set_date(default_start)
        self.checkin_date.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        row += 1

        ttk.Label(parent, text='Check-out').grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.checkout_date = DateEntry(parent, width=20, background='darkblue',
                                       foreground='white', borderwidth=2,
                                       date_pattern='yyyy-mm-dd')
        self.checkout_date.set_date(default_end)
        self.checkout_date.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        row += 1

        ttk.Label(parent, text=self.lang.get('hotel_notes', 'Note Hotel')).grid(
            row=row, column=0, sticky='nw', padx=5, pady=5)
        self.hotel_notes = tk.Text(parent, height=4, width=40)
        self.hotel_notes.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

        parent.columnconfigure(1, weight=1)

    # ================================================================
    # DATA LOADING
    # ================================================================
    def _load_airlines(self):
        """Carica le compagnie aeree da FlyghtCompanies."""
        try:
            query = """
                SELECT FlightCompanyId, CompanyName, FlightIdentifyCode
                FROM Employee.dbo.FlyghtCompanies
                ORDER BY CompanyName
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            self._airline_ids = {}
            airlines = []
            for row in cursor.fetchall():
                name = row.CompanyName or ''
                self._airline_ids[name] = (row.FlightCompanyId, row.FlightIdentifyCode)
                airlines.append(name)
            self._all_airlines = airlines
            self.airline_combo['values'] = airlines
            cursor.close()
            logger.info(f"Caricate {len(airlines)} compagnie aeree")
        except Exception as e:
            logger.error(f"Errore caricamento compagnie aeree: {e}")

    def _filter_airlines(self, *args):
        """Filtra le compagnie aeree durante la digitazione."""
        typed = self.airline_var.get().lower()
        if not typed:
            self.airline_combo['values'] = self._all_airlines
        else:
            filtered = [a for a in self._all_airlines if typed in a.lower()]
            self.airline_combo['values'] = filtered

    def _create_new_airline(self, airline_name):
        """Crea una nuova compagnia aerea in FlyghtCompanies."""
        try:
            code = airline_name[:2].upper() if len(airline_name) >= 2 else airline_name.upper()
            query = """
                INSERT INTO Employee.dbo.FlyghtCompanies (CompanyName, FlightIdentifyCode)
                OUTPUT INSERTED.FlightCompanyId
                VALUES (?, ?)
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (airline_name, code))
            row = cursor.fetchone()
            self.db.conn.commit()
            cursor.close()
            new_id = row[0] if row else None
            if new_id:
                logger.info(f"Nuova compagnia aerea creata: '{airline_name}' Code={code} ID={new_id}")
                self._airline_ids[airline_name] = (new_id, code)
                self._load_airlines()
                self.airline_var.set(airline_name)
            return new_id
        except Exception as e:
            logger.error(f"Errore creazione compagnia aerea: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")
            return None

    def _load_supporters(self):
        """Carica shuttle e hotel da VisitorSupportersData."""
        try:
            query = """
                SELECT
                    vsd.SupporterDataId, vsd.SupporterTypeID,
                    vsd.Name, vsd.ReservationEmail,
                    t.TownName, c.CountyName, n.NationName
                FROM Employee.dbo.VisitorSupportersData vsd
                INNER JOIN Employee.dbo.SupporterTypes st
                    ON vsd.SupporterTypeID = st.SupporterTypeID
                INNER JOIN Employee.Geo.Towns t ON vsd.CityId = t.TownId
                INNER JOIN Employee.Geo.Counties c ON t.CountyId = c.CountyId
                INNER JOIN Employee.Geo.Nations n ON c.NationId = n.NationId
                WHERE vsd.DateOut IS NULL
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)

            self._shuttle_data = {}
            self._hotel_data = {}
            shuttles = []
            hotels = []

            for row in cursor.fetchall():
                name = row.Name or ''
                display = f"{name} — {row.TownName}"
                entry = (row.SupporterDataId, row.ReservationEmail, row.TownName)

                if row.SupporterTypeID == 1:  # Hotel
                    self._hotel_data[display] = entry
                    hotels.append(display)
                elif row.SupporterTypeID == 2:  # Shuttle
                    self._shuttle_data[display] = entry
                    shuttles.append(display)

            self.shuttle_combo['values'] = shuttles
            self.hotel_combo['values'] = hotels
            cursor.close()
            logger.info(f"Caricati {len(shuttles)} shuttle, {len(hotels)} hotel")
        except Exception as e:
            logger.error(f"Errore caricamento supporters: {e}")

    def _load_company_info(self):
        """Carica i dati della società ospitante (Vandewiele Romania)."""
        try:
            query = """
                SELECT EmployeerName, [Address], t.TownName, c.CountyName,
                       EmployeerFiscalCode, ChamberOfCommercNo
                FROM Employee.dbo.Employeers e
                INNER JOIN Employee.Geo.Towns t ON e.TownId = t.TownId
                INNER JOIN Employee.Geo.Counties c ON t.CountyId = c.CountyId
                WHERE EmployeerId = 2
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            if row:
                self._company_info = {
                    'name': row.EmployeerName,
                    'address': row.Address,
                    'town': row.TownName,
                    'county': row.CountyName,
                    'fiscal_code': row.EmployeerFiscalCode,
                    'chamber': row.ChamberOfCommercNo
                }
                logger.info(f"Dati aziendali caricati: {self._company_info['name']}")
        except Exception as e:
            logger.error(f"Errore caricamento dati aziendali: {e}")

    def _search_flight_time(self):
        """Cerca l'orario del volo online tramite AviationStack API.
        
        Cerca per:
        1. Numero volo specifico (se inserito)
        2. Compagnia aerea + data arrivo (anche senza numero volo)
        Se più risultati → mostra lista selezione.
        """
        import threading

        airline_name = self.airline_var.get().strip()
        flight_no = self.flight_number_var.get().strip()
        arrival_date = self.arrival_date.get_date()

        if not airline_name and not flight_no:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_airline_or_flight',
                              'Inserire la compagnia aerea o il numero del volo.')
            )
            return

        # Recupera IATA code dalla compagnia selezionata
        iata_code = ''
        if airline_name and airline_name in self._airline_ids:
            _, iata_code = self._airline_ids[airline_name]
            iata_code = iata_code or ''

        logger.info(f"Ricerca volo: airline={airline_name} IATA={iata_code} "
                     f"flight={flight_no} date={arrival_date}")

        # Esegui ricerca in un thread separato per non bloccare la UI
        self._set_search_status(True)
        thread = threading.Thread(
            target=self._do_flight_search,
            args=(flight_no, iata_code, arrival_date, airline_name),
            daemon=True
        )
        thread.start()

    def _set_search_status(self, searching):
        """Abilita/disabilita UI durante la ricerca."""
        # Placeholder — potrebbe mostrare un indicatore di caricamento
        pass

    def _do_flight_search(self, flight_no, iata_code, arrival_date, airline_name):
        """Esegue la ricerca del volo in background.
        
        Prova FlightLabs (date future), poi AviationStack come fallback.
        Se iata_code contiene più codici separati da ';' (es. 'LH;VL'),
        filtra i risultati per ciascun codice in sequenza.
        """
        import urllib.request
        import urllib.parse
        import json

        try:
            all_flights = []

            # --- Tentativo 1: FlightLabs ---
            flightlabs_key = self._get_setting('FlightLabs_API_Key')
            if flightlabs_key:
                # Prova prima /advanced-future-flights, poi /flights
                endpoints = [
                    {
                        'url': 'https://www.goflightlabs.com/advanced-flights-schedules',
                        'params': {
                            'access_key': flightlabs_key,
                            'iataCode': 'TSR',
                            'type': 'arrival',
                            'date': arrival_date.strftime('%Y-%m-%d')
                        },
                        'name': 'future-flights',
                        'parser': 'realtime'
                    },
                    {
                        'url': 'https://www.goflightlabs.com/flights',
                        'params': {
                            'access_key': flightlabs_key,
                            'arr_iata': 'TSR',
                            'flight_date': arrival_date.strftime('%Y-%m-%d')
                        },
                        'name': '/flights',
                        'parser': 'realtime'
                    }
                ]

                for ep in endpoints:
                    if all_flights:
                        break
                    try:
                        url = f"{ep['url']}?{urllib.parse.urlencode(ep['params'])}"
                        logger.info(f"FlightLabs {ep['name']}: {url[:80]}...")
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=20) as response:
                            raw = response.read().decode('utf-8')
                        logger.info(f"FlightLabs {ep['name']} response: {len(raw)} chars, {raw[:200]}")

                        if not raw or len(raw) < 10:
                            continue
                        data = json.loads(raw)
                        items = data.get('data', [])
                        if not items:
                            continue

                        date_str = arrival_date.strftime('%Y-%m-%d')
                        skip_date_filter = 'date' in ep['params']

                        for item in items:
                            arr_time_full = item.get('arr_time', '') or ''
                            if not skip_date_filter and date_str and not arr_time_full.startswith(date_str):
                                continue
                            arr_time = arr_time_full[11:16] if len(arr_time_full) >= 16 else ''
                            dep_time_full = item.get('dep_time', '') or ''
                            dep_time = dep_time_full[11:16] if len(dep_time_full) >= 16 else ''
                            all_flights.append({
                                'flight_iata': item.get('flight_iata', ''),
                                'flight_number': item.get('flight_number', ''),
                                'airline_code': item.get('airline_iata', ''),
                                'airline_name': item.get('airline_iata', ''),
                                'arrival_time': arr_time,
                                'departure_time': dep_time,
                                'arrival_airport': 'Timisoara (TSR)',
                                'departure_airport': item.get('dep_iata', ''),
                                'status': item.get('status', 'scheduled')
                            })

                        logger.info(f"FlightLabs {ep['name']}: {len(all_flights)} voli trovati")
                        # Log codici compagnie per diagnostica
                        codes_found = set(f['airline_code'] for f in all_flights)
                        logger.info(f"Codici compagnia trovati: {codes_found}")
                    except Exception as e:
                        logger.warning(f"FlightLabs {ep['name']} errore: {e}")

            # --- Tentativo 2: AviationStack ---
            if not all_flights:
                avstack_key = self._get_setting('AviationStack_API_Key')
                if avstack_key:
                    try:
                        base_url = 'http://api.aviationstack.com/v1/flights'
                        params = {
                            'access_key': avstack_key,
                            'arr_iata': 'TSR',
                            'flight_date': arrival_date.strftime('%Y-%m-%d'),
                            'limit': 100
                        }
                        url = f"{base_url}?{urllib.parse.urlencode(params)}"
                        logger.info(f"AviationStack API call: TSR arrivals {arrival_date}")
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=15) as response:
                            data = json.loads(response.read().decode('utf-8'))
                        for item in data.get('data', []):
                            arr = item.get('arrival', {})
                            dep = item.get('departure', {})
                            flight = item.get('flight', {})
                            airline_d = item.get('airline', {})
                            arr_time = arr.get('estimated') or arr.get('scheduled') or ''
                            if arr_time and 'T' in arr_time:
                                arr_time = arr_time.split('T')[1][:5]
                            all_flights.append({
                                'flight_iata': flight.get('iata', ''),
                                'flight_number': flight.get('number', ''),
                                'airline_code': flight.get('iata', '')[:2] if flight.get('iata') else '',
                                'airline_name': airline_d.get('name', ''),
                                'arrival_time': arr_time,
                                'departure_time': '',
                                'arrival_airport': arr.get('airport', ''),
                                'departure_airport': dep.get('airport', ''),
                                'status': item.get('flight_status', '')
                            })
                        logger.info(f"AviationStack: {len(all_flights)} voli trovati")
                    except Exception as e:
                        logger.warning(f"AviationStack non disponibile: {e}")

            if not all_flights:
                logger.warning("Nessuna API disponibile o nessun volo trovato")

            # --- Filtra risultati ---
            flights = []
            if flight_no:
                flight_no_upper = flight_no.upper().replace(' ', '')
                flights = [f for f in all_flights
                           if f['flight_iata'].upper() == flight_no_upper]
                logger.info(f"Filtro flight_no={flight_no_upper}: {len(flights)} trovati")
            elif iata_code:
                codes = [c.strip().upper() for c in iata_code.split(';') if c.strip()]
                for code in codes:
                    flights = [f for f in all_flights
                               if f['airline_code'].upper() == code]
                    logger.info(f"Filtro airline_code={code}: {len(flights)} voli")
                    if flights:
                        break
                # Se nessun codice corrisponde, mostra tutti i voli disponibili
                if not flights and all_flights:
                    logger.info(f"Nessun volo per {codes}, mostro tutti i {len(all_flights)} voli TSR")
                    flights = all_flights
            else:
                flights = all_flights

            self.after(0, self._handle_flight_results, flights, airline_name, flight_no)

        except Exception as e:
            logger.error(f"Errore ricerca volo: {e}")
            self.after(0, self._handle_flight_search_error, str(e))

    def _get_setting(self, attribute):
        """Recupera un valore dalla tabella settings."""
        try:
            query = """
                SELECT [value]
                FROM Traceability_RS.dbo.Settings
                WHERE atribute = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (attribute,))
            row = cursor.fetchone()
            cursor.close()
            return row[0] if row else None
        except Exception as e:
            logger.warning(f"Errore lettura setting '{attribute}': {e}")
            return None

    def _handle_flight_search_error(self, error_msg):
        """Gestisce errore ricerca volo — propone inserimento manuale."""
        self._set_search_status(False)
        messagebox.showinfo(
            self.lang.get('info', 'Informazione'),
            self.lang.get('flight_search_manual',
                          f'Ricerca automatica non disponibile.\n'
                          f'Errore: {error_msg}\n'
                          'Inserire data e ora di arrivo manualmente.')
        )

    def _handle_flight_results(self, flights, airline_name, flight_no):
        """Gestisce i risultati della ricerca volo."""
        self._set_search_status(False)

        if not flights:
            # Nessun risultato — inserimento manuale
            messagebox.showinfo(
                self.lang.get('info', 'Informazione'),
                self.lang.get('no_flights_found',
                              'Nessun volo trovato per i criteri specificati.\n'
                              'Inserire data e ora manualmente.')
            )
            return

        if len(flights) == 1:
            # Un solo risultato → chiedi conferma
            f = flights[0]
            display = (f"{f['flight_iata']} — {f['airline_name']}\n"
                       f"Da: {f['departure_airport']}\n"
                       f"Arrivo: {f['arrival_time']}\n"
                       f"Stato: {f['status']}")

            if messagebox.askyesno(
                self.lang.get('confirm_flight', 'Conferma Volo'),
                f"{self.lang.get('confirm_flight_details', 'Confermi questo volo?')}\n\n{display}"
            ):
                self._apply_flight_data(f)
        else:
            # Più risultati → mostra lista selezione
            self._show_flight_selection_dialog(flights)

    def _show_flight_selection_dialog(self, flights):
        """Mostra un dialog per selezionare tra più voli trovati."""
        dialog = tk.Toplevel(self)
        dialog.title(self.lang.get('select_flight', 'Seleziona Volo'))
        dialog.geometry('650x400')
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text=self.lang.get('multiple_flights_found',
                  'Trovati più voli. Selezionarne uno:'),
                  font=('Arial', 10, 'bold')).pack(padx=10, pady=10)

        # Treeview con i voli
        columns = ('flight', 'airline', 'from', 'arrival', 'status')
        tree = ttk.Treeview(dialog, columns=columns, show='headings', height=12)
        tree.heading('flight', text='Volo')
        tree.heading('airline', text='Compagnia')
        tree.heading('from', text='Da')
        tree.heading('arrival', text='Arrivo')
        tree.heading('status', text='Stato')

        tree.column('flight', width=80)
        tree.column('airline', width=150)
        tree.column('from', width=180)
        tree.column('arrival', width=80)
        tree.column('status', width=80)

        for f in flights:
            tree.insert('', 'end', values=(
                f['flight_iata'],
                f['airline_name'],
                f['departure_airport'],
                f['arrival_time'],
                f['status']
            ))

        tree.pack(fill='both', expand=True, padx=10, pady=5)

        def on_select():
            selection = tree.selection()
            if not selection:
                return
            idx = tree.index(selection[0])
            self._apply_flight_data(flights[idx])
            dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill='x', padx=10, pady=10)
        ttk.Button(btn_frame, text=self.lang.get('confirm', 'Conferma'),
                   command=on_select).pack(side='right', padx=5)
        ttk.Button(btn_frame, text=self.lang.get('cancel', 'Annulla'),
                   command=dialog.destroy).pack(side='right', padx=5)

    def _apply_flight_data(self, flight_data):
        """Applica i dati del volo selezionato ai campi della form."""
        if flight_data.get('flight_iata'):
            self.flight_number_var.set(flight_data['flight_iata'])
        if flight_data.get('arrival_time'):
            self.arrival_time_var.set(flight_data['arrival_time'])
        logger.info(f"Volo selezionato: {flight_data['flight_iata']} "
                     f"arrivo {flight_data['arrival_time']}")

    # ================================================================
    # EMAIL SENDING
    # ================================================================
    def _get_user_email(self):
        """Recupera l'email dell'utente loggato."""
        try:
            query = """
                SELECT ea.WorkEmail
                FROM Employee.dbo.Employees e
                INNER JOIN Employee.dbo.EmployeeAddress ea ON ea.EmployeeId = e.EmployeeId
                    AND ea.DateOut IS NULL
                WHERE UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self.user_name.upper(),))
            row = cursor.fetchone()
            cursor.close()
            return row.WorkEmail if row and row.WorkEmail else None
        except Exception as e:
            logger.error(f"Errore recupero email utente: {e}")
            return None

    def _send_all_bookings(self):
        """Invia tutte le prenotazioni (shuttle + hotel).
        
        Se mancano dati obbligatori, naviga alla tab incompleta.
        I servizi con flag 'skip' attivo vengono saltati.
        """
        skip_shuttle = self.skip_shuttle_var.get()
        skip_hotel = self.skip_hotel_var.get()

        # Se entrambi sono skippati, chiedi conferma e chiudi
        if skip_shuttle and skip_hotel:
            if messagebox.askyesno(
                self.lang.get('confirm', 'Conferma'),
                self.lang.get('skip_all_bookings',
                              'Entrambi i servizi sono disattivati. Chiudere senza prenotazioni?')):
                self._on_close()
            return

        # --- Validazione dati volo (Tab 0) ---
        arrival = self.arrival_date.get_date()
        departure = self.departure_date.get_date()

        if departure < arrival:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('invalid_date_range',
                              'La data di partenza non può essere anteriore alla data di arrivo.'))
            self.notebook.select(0)
            return

        # --- Validazione shuttle (Tab 1) ---
        if not skip_shuttle:
            shuttle = self.shuttle_var.get().strip()
            if not shuttle or shuttle not in self._shuttle_data:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('shuttle_required',
                                  'Selezionare un servizio shuttle oppure disattivare il servizio.'))
                self.notebook.select(1)
                return

        # --- Validazione hotel (Tab 2) ---
        if not skip_hotel:
            hotel = self.hotel_var.get().strip()
            checkin = self.checkin_date.get_date()
            checkout = self.checkout_date.get_date()

            if not hotel or hotel not in self._hotel_data:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('hotel_required',
                                  'Selezionare un hotel oppure disattivare il servizio.'))
                self.notebook.select(2)
                return

            if checkout < checkin:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('invalid_checkout_date',
                                  'La data di check-out non può essere anteriore alla data di check-in.'))
                self.notebook.select(2)
                return

        # Validazione: compagnia aerea
        airline_name = self.airline_var.get().strip()

        # Auto-create compagnia aerea se nuova
        if airline_name and airline_name not in self._airline_ids:
            if messagebox.askyesno(
                self.lang.get('confirm', 'Conferma'),
                self.lang.get('confirm_new_airline',
                              f'La compagnia "{airline_name}" non esiste. Crearla?')
            ):
                if not self._create_new_airline(airline_name):
                    return
            else:
                return

        # --- Verifica email ospiti: avvisa se mancano ---
        guests_no_email = [g['guest_name'] for g in self.guests_data
                           if not g.get('email', '').strip()]
        if guests_no_email:
            names_list = '\n'.join([f"  • {n}" for n in guests_no_email])
            proceed = messagebox.askyesno(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('guests_no_email_warning',
                    f"I seguenti ospiti non hanno un indirizzo email registrato e "
                    f"NON riceveranno la conferma di prenotazione:\n\n"
                    f"{names_list}\n\n"
                    f"Vuoi procedere comunque con l'invio?"))
            if not proceed:
                return

        logger.info(f"=== BOOKING START === skip_shuttle={skip_shuttle}, skip_hotel={skip_hotel}")
        logger.info(f"Guests data: {[g.get('guest_name','?') for g in self.guests_data]}")
        errors = []
        successes = []

        # Crea record VisitorArrivalDetails (dati volo/arrivo)
        arrival_detail_id = None
        try:
            arrival_date = self.arrival_date.get_date()
            departure_date = self.departure_date.get_date()
            arrival_time = self.arrival_time_var.get().strip()
            flight_no = self.flight_number_var.get().strip()

            # FlightCompanyId dalla compagnia selezionata
            flight_company_id = None
            airline_name = self.airline_var.get().strip()
            if airline_name and airline_name in self._airline_ids:
                flight_company_id = self._airline_ids[airline_name][0]

            # HotelId dal hotel selezionato (SupporterDataId)
            hotel_id = None
            if not skip_hotel:
                hotel = self.hotel_var.get().strip()
                if hotel and hotel in self._hotel_data:
                    hotel_id = self._hotel_data[hotel][0]

            # Recupera AirportCityId (= TownId da Geo.Towns) per Timisoara
            airport_city_id = None
            try:
                ac_cursor = self.db.conn.cursor()
                ac_cursor.execute("""
                    SELECT TOP 1 TownId 
                    FROM Employee.Geo.Towns 
                    WHERE TownName LIKE '%Timisoara%' OR TownName LIKE '%Timi%oara%'
                """)
                ac_row = ac_cursor.fetchone()
                if ac_row:
                    airport_city_id = ac_row[0]
                    logger.info(f"AirportCityId (TownId) per Timisoara: {airport_city_id}")
                else:
                    # Fallback: prendi il primo TownId disponibile
                    ac_cursor.execute("SELECT TOP 1 TownId FROM Employee.Geo.Towns")
                    ac_row = ac_cursor.fetchone()
                    if ac_row:
                        airport_city_id = ac_row[0]
                        logger.warning(f"Timisoara non trovata in Geo.Towns, uso TownId fallback: {airport_city_id}")
                ac_cursor.close()
            except Exception as ac_err:
                logger.warning(f"Cannot lookup TownId for Timisoara: {ac_err}")

            if airport_city_id is None:
                logger.error("AirportCityId (TownId) non trovato! INSERT potrebbe fallire.")
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    "Città aeroporto (Timisoara) non trovata nel database. Contattare l'amministratore.")
                return

            # DateTimeArrival = data + ora arrivo
            dt_arrival = None
            if arrival_time:
                try:
                    dt_arrival = datetime.combine(arrival_date, 
                                                   datetime.strptime(arrival_time, '%H:%M').time())
                except ValueError:
                    dt_arrival = datetime.combine(arrival_date, datetime.min.time())
            else:
                dt_arrival = datetime.combine(arrival_date, datetime.min.time())

            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO Employee.dbo.VisitorArrivalDetails
                    (AirportCityId, HotelId, FlightNumber, FlightCompanyId, DateTimeArrival, DateSys, DateOut)
                OUTPUT INSERTED.VisitorArrivalDetailId
                VALUES (?, ?, ?, ?, ?, GETDATE(), ?)
            """, (airport_city_id, hotel_id, flight_no or None, flight_company_id, dt_arrival,
                  datetime.combine(departure_date, datetime.min.time())))
            row = cursor.fetchone()
            arrival_detail_id = row[0] if row else None
            self.db.conn.commit()
            cursor.close()
            logger.info(f"Creato VisitorArrivalDetails ID={arrival_detail_id}")
        except Exception as e:
            logger.error(f"Errore creazione VisitorArrivalDetails: {e}")

        # Invia email shuttle
        if not skip_shuttle:
            shuttle = self.shuttle_var.get().strip()
            logger.info(f"Shuttle selezionato: '{shuttle}', presente in _shuttle_data: {shuttle in self._shuttle_data}")
            if shuttle and shuttle in self._shuttle_data:
                shuttle_info = self._shuttle_data[shuttle]
                logger.info(f"Shuttle data: ID={shuttle_info[0]}, email='{shuttle_info[1]}', town='{shuttle_info[2]}'")
                try:
                    self._send_shuttle_email(shuttle)
                    successes.append('Shuttle')
                    if arrival_detail_id:
                        self._save_booking_record(arrival_detail_id, self._shuttle_data[shuttle][1])
                    # Invio conferma email agli ospiti
                    self._send_guest_confirmation_email('Shuttle / Transport', shuttle, arrival_detail_id)
                except Exception as e:
                    logger.error(f"Errore invio email shuttle: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    errors.append(f"Shuttle: {e}")

        # Invia email hotel
        if not skip_hotel:
            hotel = self.hotel_var.get().strip()
            logger.info(f"Hotel selezionato: '{hotel}', presente in _hotel_data: {hotel in self._hotel_data}")
            if hotel and hotel in self._hotel_data:
                hotel_info = self._hotel_data[hotel]
                logger.info(f"Hotel data: ID={hotel_info[0]}, email='{hotel_info[1]}', town='{hotel_info[2]}'")
                try:
                    self._send_hotel_email(hotel)
                    successes.append('Hotel')
                    if arrival_detail_id:
                        self._save_booking_record(arrival_detail_id, self._hotel_data[hotel][1])
                    # Invio conferma email agli ospiti
                    self._send_guest_confirmation_email('Hotel', hotel, arrival_detail_id)
                except Exception as e:
                    logger.error(f"Errore invio email hotel: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    errors.append(f"Hotel: {e}")

        # Report
        if successes:
            msg = f"Prenotazioni inviate: {', '.join(successes)}"
            if errors:
                msg += f"\n\nErrori: {', '.join(errors)}"
            messagebox.showinfo(self.lang.get('success', 'Successo'), msg)
        elif errors:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 f"Errori: {', '.join(errors)}")

        self._on_close_after_send()

    def _send_shuttle_email(self, shuttle_key):
        """Invia email al servizio shuttle."""
        from email_connector import EmailSender

        supporter_id, reservation_email, town = self._shuttle_data[shuttle_key]
        if not reservation_email:
            raise ValueError("Nessuna email di prenotazione per lo shuttle selezionato")

        user_email = self._get_user_email()
        airline_name = self.airline_var.get().strip()
        flight_no = self.flight_number_var.get().strip()
        arrival_time = self.arrival_time_var.get().strip()
        arrival_date = self.arrival_date.get_date()
        departure_date = self.departure_date.get_date()
        departure_time = self.departure_time_var.get().strip()

        # Determina destinazione: dopo le 16:00 → Hotel, altrimenti → Fabbrica
        destination = 'Hotel'
        try:
            if arrival_time:
                hour = int(arrival_time.split(':')[0])
                if hour < 16:
                    destination = self._company_info['name'] if self._company_info else 'Fabbrica'
        except (ValueError, IndexError):
            pass

        guests_list = '\n'.join([f"  • {g['guest_name']} ({g['company']})" for g in self.guests_data])
        guests_html = ''.join([
            f"<li><strong>{g['guest_name']}</strong> — {g['company']}</li>"
            for g in self.guests_data
        ])

        flight_info = ''
        if airline_name:
            flight_info = f"<strong>Compagnia aerea:</strong> {airline_name}<br/>"
        if flight_no:
            flight_info += f"<strong>Numero volo:</strong> {flight_no}<br/>"

        # Logo path
        logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')

        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 12px;">
            <img src="cid:company_logo" alt="Logo" style="width: 150px; margin-bottom: 10px;" /><br/>
            <h3 style="color: #1565C0;">Cerere transport / Transport Request</h3>
            <p>Bună ziua,</p>
            <p>Vă rugăm să asigurați transportul pentru următorii oaspeți:</p>

            <h4>Oaspeți ({len(self.guests_data)} persoane):</h4>
            <ul>{guests_html}</ul>

            {flight_info}
            <p><strong>Data sosire:</strong> {arrival_date.strftime('%d/%m/%Y')}</p>
            <p><strong>Ora sosire:</strong> {arrival_time if arrival_time else 'De confirmat'}</p>
            <p><strong>Destinația:</strong> <span style="color: #B22222; font-weight: bold;">{destination}</span></p>

            <p><strong>Data plecare:</strong> {departure_date.strftime('%d/%m/%Y')}</p>
            <p><strong>Ora plecare:</strong> {departure_time if departure_time else 'De confirmat'}</p>

            <div style="background-color: #FFF3E0; border-left: 4px solid #E65100; padding: 10px; margin: 15px 0;">
                <p style="color: #B71C1C; font-weight: bold; font-size: 12px;">⚠ IMPORTANT / IMPORTANT:</p>
                <p style="color: #333; font-size: 11px;">
                    Vă rugăm să confirmați primirea acestei cereri de transport și că serviciul a fost rezervat.<br/>
                    Vă rugăm să trimiteți confirmarea la adresa: <strong>{user_email if user_email else 'expeditorul acestui email'}</strong>
                </p>
                <p style="color: #333; font-size: 11px; font-style: italic;">
                    Please confirm receipt of this transport request and that the service has been booked.<br/>
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

        # Supporta email multiple separate da ';'
        email_addresses = [e.strip() for e in reservation_email.split(';') if e.strip()]
        for addr in email_addresses:
            sender.send_email(
                to_email=addr,
                subject=f"Transport Request — {len(self.guests_data)} oaspeți — {arrival_date.strftime('%d/%m/%Y')}",
                body=body_html,
                is_html=True,
                attachments=attachments if attachments else None,
                cc_emails=cc
            )
            logger.info(f"Email shuttle inviata a {addr}")

    def _send_hotel_email(self, hotel_key):
        """Invia email all'hotel."""
        from email_connector import EmailSender

        supporter_id, reservation_email, town = self._hotel_data[hotel_key]
        if not reservation_email:
            raise ValueError("Nessuna email di prenotazione per l'hotel selezionato")

        user_email = self._get_user_email()
        checkin = self.checkin_date.get_date()
        checkout = self.checkout_date.get_date()
        hotel_notes_text = self.hotel_notes.get('1.0', 'end-1c').strip()

        guests_html = ''.join([
            f"<li><strong>{g['guest_name']}</strong> — {g['company']}</li>"
            for g in self.guests_data
        ])

        # Dati aziendali
        company_html = ''
        if self._company_info:
            ci = self._company_info
            company_html = f"""
            <h4>Date companie gazdă:</h4>
            <table style="border-collapse: collapse;">
                <tr><td style="padding: 3px 10px; font-weight: bold;">Companie:</td>
                    <td>{ci['name']}</td></tr>
                <tr><td style="padding: 3px 10px; font-weight: bold;">Adresă:</td>
                    <td>{ci['address']}, {ci['town']}, {ci['county']}</td></tr>
                <tr><td style="padding: 3px 10px; font-weight: bold;">CUI:</td>
                    <td>{ci['fiscal_code']}</td></tr>
                <tr><td style="padding: 3px 10px; font-weight: bold;">Nr. Reg. Comerț:</td>
                    <td>{ci['chamber']}</td></tr>
            </table>
            """

        notes_html = f"<p><strong>Note:</strong> {hotel_notes_text}</p>" if hotel_notes_text else ""

        logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')

        num_nights = (checkout - checkin).days
        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 12px;">
            <img src="cid:company_logo" alt="Logo" style="width: 150px; margin-bottom: 10px;" /><br/>
            <h3 style="color: #2E7D32;">Cerere rezervare hotel / Hotel Reservation Request</h3>
            <p>Bună ziua,</p>
            <p>Vă rugăm să faceți o rezervare pentru următorii oaspeți:</p>

            <h4>Oaspeți ({len(self.guests_data)} persoane):</h4>
            <ul>{guests_html}</ul>

            <p><strong>Check-in:</strong> {checkin.strftime('%d/%m/%Y')}</p>
            <p><strong>Check-out:</strong> {checkout.strftime('%d/%m/%Y')}</p>
            <p><strong>Număr nopți:</strong> {num_nights}</p>
            <p><strong>Număr camere:</strong> {len(self.guests_data)}</p>

            {notes_html}

            {company_html}

            <div style="background-color: #E8F5E9; border-left: 4px solid #2E7D32; padding: 10px; margin: 15px 0;">
                <p style="color: #B71C1C; font-weight: bold; font-size: 12px;">⚠ IMPORTANT / IMPORTANT:</p>
                <p style="color: #333; font-size: 11px;">
                    Vă rugăm să confirmați primirea acestei cereri de rezervare și că serviciul a fost rezervat.<br/>
                    Vă rugăm să trimiteți confirmarea la adresa: <strong>{user_email if user_email else 'expeditorul acestui email'}</strong>
                </p>
                <p style="color: #333; font-size: 11px; font-style: italic;">
                    Please confirm receipt of this reservation request and that the rooms have been booked.<br/>
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

        # Supporta email multiple separate da ';'
        email_addresses = [e.strip() for e in reservation_email.split(';') if e.strip()]
        for addr in email_addresses:
            sender.send_email(
                to_email=addr,
                subject=f"Rezervare Hotel — {len(self.guests_data)} oaspeți — {checkin.strftime('%d/%m/%Y')} - {checkout.strftime('%d/%m/%Y')}",
                body=body_html,
                is_html=True,
                attachments=attachments if attachments else None,
                cc_emails=cc
            )
            logger.info(f"Email hotel inviata a {addr}")

    # ================================================================
    # GUEST CONFIRMATION EMAIL
    # ================================================================
    def _send_guest_confirmation_email(self, service_type, service_key, arrival_detail_id):
        """Invia email di conferma in inglese a ogni ospite che ha un indirizzo email."""
        from email_connector import EmailSender

        user_email = self._get_user_email()
        logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')

        # Dati volo
        airline_name = self.airline_var.get().strip()
        flight_no = self.flight_number_var.get().strip()
        arrival_date = self.arrival_date.get_date().strftime('%d/%m/%Y')
        departure_date = self.departure_date.get_date().strftime('%d/%m/%Y')
        arrival_time = self.arrival_time_var.get().strip()

        for guest in self.guests_data:
            guest_email = guest.get('email', '').strip()
            guest_name = guest.get('guest_name', '')

            if not guest_email:
                logger.info(f"Ospite {guest_name}: nessuna email, skip conferma {service_type}")
                continue

            try:
                flight_info = ''
                if airline_name:
                    flight_info += f"<strong>Airline:</strong> {airline_name}<br/>"
                if flight_no:
                    flight_info += f"<strong>Flight:</strong> {flight_no}<br/>"
                if arrival_time:
                    flight_info += f"<strong>Arrival Time:</strong> {arrival_time}<br/>"

                body_html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; font-size: 13px; color: #333;">
                    <img src="cid:company_logo" alt="Vandewiele" style="width: 160px; margin-bottom: 15px;" /><br/>

                    <h2 style="color: #1565C0;">{service_type} Booking Confirmation</h2>

                    <p>Dear <strong>{guest_name}</strong>,</p>

                    <p>We are pleased to inform you that a <strong>{service_type}</strong> booking 
                    has been requested on your behalf for your upcoming visit:</p>

                    <table style="border-collapse: collapse; margin: 15px 0; font-size: 13px;">
                        <tr style="background-color: #E3F2FD;">
                            <td style="padding: 8px 15px; font-weight: bold;">Service</td>
                            <td style="padding: 8px 15px;">{service_type}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 15px; font-weight: bold;">Arrival Date</td>
                            <td style="padding: 8px 15px;">{arrival_date}</td>
                        </tr>
                        <tr style="background-color: #E3F2FD;">
                            <td style="padding: 8px 15px; font-weight: bold;">Departure Date</td>
                            <td style="padding: 8px 15px;">{departure_date}</td>
                        </tr>
                    </table>

                    {f'<p>{flight_info}</p>' if flight_info else ''}

                    <p>If you have any questions or need to make changes, please contact 
                    <strong>{user_email if user_email else 'your host'}</strong>.</p>

                    <p>We look forward to welcoming you!</p>

                    <p style="margin-top: 20px;">Kind regards,<br/>
                    <em>Vandewiele Romania — Guest Services</em></p>

                    <hr style="border: 1px solid #ddd; margin-top: 20px;"/>
                    <p style="color: #999; font-size: 10px;">
                        This is an automated message from TraceabilityRS — {self.user_name}</p>
                </body>
                </html>
                """

                sender = EmailSender()
                attachments = []
                if os.path.exists(logo_path):
                    attachments.append(('inline', logo_path, 'company_logo'))

                cc = user_email if user_email else None

                sender.send_email(
                    to_email=guest_email,
                    subject=f"{service_type} Booking Confirmation — {arrival_date}",
                    body=body_html,
                    is_html=True,
                    attachments=attachments if attachments else None,
                    cc_emails=cc
                )
                logger.info(f"Conferma {service_type} inviata a {guest_name} ({guest_email})")

                # Salva record email ospite in VisitorBookingServiceEmails
                if arrival_detail_id:
                    self._save_booking_record(arrival_detail_id, guest_email)

            except Exception as e:
                logger.error(f"Errore invio conferma {service_type} a {guest_name}: {e}")

    # ================================================================
    # SAVE BOOKING RECORD
    # ================================================================
    def _save_booking_record(self, arrival_detail_id, reservation_email):
        """Salva il record di booking in VisitorBookingServiceEmails."""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO Employee.dbo.VisitorBookingServiceEmails
                    (VisitorArrivalDetailId, EmailRequestBooking, SentOnDate, Confirmed)
                VALUES (?, ?, GETDATE(), 0)
            """, (arrival_detail_id, reservation_email))
            self.db.conn.commit()
            cursor.close()
            logger.info(f"Salvato record booking: ArrivalDetailId={arrival_detail_id}, email={reservation_email}")
        except Exception as e:
            logger.error(f"Errore salvataggio record booking: {e}")

    # ================================================================
    # CLOSE
    # ================================================================
    def _on_close(self):
        """Chiude la finestra senza inviare booking (chiusura manuale)."""
        if messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('close_without_booking',
                          'Chiudere senza inviare le prenotazioni?')):
            self.destroy()
            # NON chiamare callback: l'utente ha annullato

    def _on_close_after_send(self):
        """Chiude dopo invio riuscito e chiama il callback per il prossimo gruppo."""
        self.destroy()
        if self.on_close_callback:
            try:
                self.on_close_callback()
            except Exception as e:
                logger.error(f"Errore nel callback post-booking: {e}")
