"""
Modulo per la gestione delle prenotazioni sale riunioni.
Gestisce:
- Gestione sale riunioni (CRUD)
- Gestione prenotazioni (creazione, modifica, cancellazione)
- Verifica disponibilità
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("TraceabilityRS")


class RoomManagerWindow(tk.Toplevel):
    """Finestra per la gestione delle sale riunioni"""

    def __init__(self, parent, db_handler, lang_manager):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager

        self.title(self.lang.get('room_manager_title', 'Gestione Sale Riunioni'))
        self.geometry('700x500')
        self.transient(parent)

        self._current_room_id = None
        self._build_ui()
        self._load_rooms()

    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Form
        form_frame = ttk.LabelFrame(main_frame, text=self.lang.get('room_form', 'Dati Sala'))
        form_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(form_frame, text=self.lang.get('room_name', 'Nome Sala') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.room_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.room_name_var, width=40).grid(
            row=0, column=1, padx=5, pady=5, sticky='ew')

        # Pulsanti
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'),
                  command=self._on_new).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                  command=self._on_save).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'),
                  command=self._on_delete).pack(side='left', padx=2)

        form_frame.columnconfigure(1, weight=1)

        # Lista sale
        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('rooms_list', 'Sale Riunioni'))
        list_frame.pack(fill='both', expand=True)

        # TreeView
        columns = ('id', 'name')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text=self.lang.get('room_name', 'Nome Sala'))

        self.tree.column('id', width=50)
        self.tree.column('name', width=400)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

    def _load_rooms(self):
        """Carica le sale"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        rooms = self.db.fetch_meeting_rooms()
        for room in rooms:
            self.tree.insert('', 'end', values=(room.MeetingRoomId, room.MeetingRoomName))

    def _on_select(self, event):
        """Gestisce la selezione"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self._current_room_id = values[0]
        self.room_name_var.set(values[1])

    def _on_new(self):
        """Pulisce il form"""
        self._current_room_id = None
        self.room_name_var.set('')

    def _on_save(self):
        """Salva o aggiorna"""
        if not self.room_name_var.get().strip():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('enter_room_name', 'Inserire il nome della sala'))
            return

        name = self.room_name_var.get().strip()

        if self._current_room_id:
            # Update
            success = self.db.update_meeting_room(self._current_room_id, name)
        else:
            # Insert
            success = self.db.add_meeting_room(name)

        if success:
            messagebox.showinfo(self.lang.get('success', 'Successo'),
                              self.lang.get('room_saved', 'Sala salvata con successo'))
            self._load_rooms()
            self._on_new()
        else:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                               self.lang.get('save_error', 'Errore durante il salvataggio'))

    def _on_delete(self):
        """Elimina"""
        if not self._current_room_id:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('select_room', 'Selezionare una sala da eliminare'))
            return

        if messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                              self.lang.get('confirm_delete_room', 'Eliminare la sala selezionata?')):
            success = self.db.delete_meeting_room(self._current_room_id)
            if success:
                messagebox.showinfo(self.lang.get('success', 'Successo'),
                                  self.lang.get('room_deleted', 'Sala eliminata con successo'))
                self._load_rooms()
                self._on_new()
            else:
                messagebox.showerror(self.lang.get('error', 'Errore'),
                                   self.lang.get('delete_error', 'Errore durante l\'eliminazione'))


class BookingManagerWindow(tk.Toplevel):
    """Finestra per la gestione delle prenotazioni"""

    def __init__(self, parent, db_handler, lang_manager, user_name):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name

        self.title(self.lang.get('booking_manager_title', 'Gestione Prenotazioni Sale'))
        self.geometry('1000x600')
        self.transient(parent)

        self._current_booking_id = None
        self._build_ui()
        self._load_rooms_combo()
        self._load_bookings()

    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_name}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Colonna sinistra: Form
        left_frame = ttk.LabelFrame(main_frame, text=self.lang.get('booking_form', 'Dati Prenotazione'))
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Sala
        ttk.Label(left_frame, text=self.lang.get('room', 'Sala') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.room_var = tk.StringVar()
        self.room_combo = ttk.Combobox(left_frame, textvariable=self.room_var,
                                       state='readonly', width=37)
        self.room_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Titolo riunione
        ttk.Label(left_frame, text=self.lang.get('meeting_title', 'Titolo Riunione') + ' *').grid(
            row=1, column=0, sticky='w', padx=5, pady=5)
        self.title_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.title_var, width=40).grid(
            row=1, column=1, padx=5, pady=5, sticky='ew')

        # Organizzatore
        ttk.Label(left_frame, text=self.lang.get('organizer', 'Organizzatore') + ' *').grid(
            row=2, column=0, sticky='w', padx=5, pady=5)
        self.organizer_var = tk.StringVar(value=self.user_name)
        ttk.Entry(left_frame, textvariable=self.organizer_var, width=40).grid(
            row=2, column=1, padx=5, pady=5, sticky='ew')

        # Data
        ttk.Label(left_frame, text=self.lang.get('date', 'Data') + ' *').grid(
            row=3, column=0, sticky='w', padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttk.Entry(left_frame, textvariable=self.date_var, width=40).grid(
            row=3, column=1, padx=5, pady=5, sticky='ew')

        # Ora inizio
        ttk.Label(left_frame, text=self.lang.get('start_time', 'Ora Inizio') + ' *').grid(
            row=4, column=0, sticky='w', padx=5, pady=5)
        self.start_time_var = tk.StringVar(value='09:00')
        ttk.Entry(left_frame, textvariable=self.start_time_var, width=40).grid(
            row=4, column=1, padx=5, pady=5, sticky='ew')

        # Ora fine
        ttk.Label(left_frame, text=self.lang.get('end_time', 'Ora Fine') + ' *').grid(
            row=5, column=0, sticky='w', padx=5, pady=5)
        self.end_time_var = tk.StringVar(value='10:00')
        ttk.Entry(left_frame, textvariable=self.end_time_var, width=40).grid(
            row=5, column=1, padx=5, pady=5, sticky='ew')

        # Pulsanti
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'),
                  command=self._on_new).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                  command=self._on_save).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_cancel_booking', 'Cancella'),
                  command=self._on_cancel).pack(side='left', padx=2)

        left_frame.columnconfigure(1, weight=1)

        # Colonna destra: Lista prenotazioni
        right_frame = ttk.LabelFrame(main_frame, text=self.lang.get('bookings_list', 'Prenotazioni'))
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # TreeView
        columns = ('id', 'room', 'title', 'organizer', 'start', 'end', 'status')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=18)
        self.tree.heading('id', text='ID')
        self.tree.heading('room', text=self.lang.get('room', 'Sala'))
        self.tree.heading('title', text=self.lang.get('title', 'Titolo'))
        self.tree.heading('organizer', text=self.lang.get('organizer', 'Organizzatore'))
        self.tree.heading('start', text=self.lang.get('start', 'Inizio'))
        self.tree.heading('end', text=self.lang.get('end', 'Fine'))
        self.tree.heading('status', text=self.lang.get('status', 'Stato'))

        self.tree.column('id', width=40)
        self.tree.column('room', width=100)
        self.tree.column('title', width=150)
        self.tree.column('organizer', width=100)
        self.tree.column('start', width=120)
        self.tree.column('end', width=120)
        self.tree.column('status', width=80)

        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

    def _load_rooms_combo(self):
        """Carica le sale nel combo"""
        rooms = self.db.fetch_meeting_rooms()
        self.rooms_dict = {r.MeetingRoomName: r.MeetingRoomId for r in rooms}
        self.room_combo['values'] = list(self.rooms_dict.keys())

    def _load_bookings(self):
        """Carica le prenotazioni"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Carica prenotazioni degli ultimi 7 giorni e prossimi 30
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now() + timedelta(days=30)

        bookings = self.db.fetch_room_bookings(start_date, end_date)
        for booking in bookings:
            start_str = booking.StartTime.strftime('%Y-%m-%d %H:%M') if booking.StartTime else ''
            end_str = booking.EndTime.strftime('%Y-%m-%d %H:%M') if booking.EndTime else ''
            self.tree.insert('', 'end', values=(
                booking.BookingID,
                booking.RoomName,
                booking.MeetingTitle,
                booking.Organizer,
                start_str,
                end_str,
                booking.BookingStatus
            ))

    def _on_select(self, event):
        """Gestisce la selezione"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self._current_booking_id = values[0]
        self.room_var.set(values[1])
        self.title_var.set(values[2])
        self.organizer_var.set(values[3])

        # Parse start/end times
        if values[4]:
            start_dt = datetime.strptime(values[4], '%Y-%m-%d %H:%M')
            self.date_var.set(start_dt.strftime('%Y-%m-%d'))
            self.start_time_var.set(start_dt.strftime('%H:%M'))

        if values[5]:
            end_dt = datetime.strptime(values[5], '%Y-%m-%d %H:%M')
            self.end_time_var.set(end_dt.strftime('%H:%M'))

    def _on_new(self):
        """Pulisce il form"""
        self._current_booking_id = None
        self.room_var.set('')
        self.title_var.set('')
        self.organizer_var.set(self.user_name)
        self.date_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.start_time_var.set('09:00')
        self.end_time_var.set('10:00')

    def _on_save(self):
        """Salva o aggiorna"""
        # Validazione
        if not self.room_var.get():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('select_room', 'Selezionare una sala'))
            return

        if not self.title_var.get().strip():
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('enter_title', 'Inserire il titolo della riunione'))
            return

        try:
            date_str = self.date_var.get()
            start_time_str = self.start_time_var.get()
            end_time_str = self.end_time_var.get()

            start_dt = datetime.strptime(f"{date_str} {start_time_str}", '%Y-%m-%d %H:%M')
            end_dt = datetime.strptime(f"{date_str} {end_time_str}", '%Y-%m-%d %H:%M')

            if end_dt <= start_dt:
                messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                     self.lang.get('invalid_time_range', 'L\'ora di fine deve essere successiva all\'ora di inizio'))
                return

        except ValueError:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('invalid_datetime', 'Formato data/ora non valido'))
            return

        room_name = self.room_var.get()
        title = self.title_var.get().strip()
        organizer = self.organizer_var.get().strip()

        if self._current_booking_id:
            # Update
            success, message = self.db.update_room_booking(
                self._current_booking_id, room_name, title, start_dt, end_dt)
        else:
            # Insert
            success, message = self.db.add_room_booking(
                room_name, title, organizer, start_dt, end_dt)

        if success:
            messagebox.showinfo(self.lang.get('success', 'Successo'), message)
            self._load_bookings()
            self._on_new()
        else:
            messagebox.showerror(self.lang.get('error', 'Errore'), message)

    def _on_cancel(self):
        """Cancella prenotazione"""
        if not self._current_booking_id:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                 self.lang.get('select_booking', 'Selezionare una prenotazione da cancellare'))
            return

        if messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                              self.lang.get('confirm_cancel_booking', 'Cancellare la prenotazione selezionata?')):
            success = self.db.cancel_room_booking(self._current_booking_id)
            if success:
                messagebox.showinfo(self.lang.get('success', 'Successo'),
                                  self.lang.get('booking_cancelled', 'Prenotazione cancellata'))
                self._load_bookings()
                self._on_new()
            else:
                messagebox.showerror(self.lang.get('error', 'Errore'),
                                   self.lang.get('cancel_error', 'Errore durante la cancellazione'))
