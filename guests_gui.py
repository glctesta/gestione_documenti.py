"""
Modulo per la gestione degli ospiti/visitatori in azienda.
Gestisce:
- Registrazione visitatori con società e nome ospite
- Gestione date visita e messaggi di benvenuto
- Report ospiti
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import logging

logger = logging.getLogger("TraceabilityRS")


class GuestRegistrationWindow(tk.Toplevel):
    """Finestra per la registrazione degli ospiti/visitatori"""

    def __init__(self, parent, db_handler, lang_manager, user_name):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_name = user_name

        self.title(self.lang.get('guest_registration_title', 'Registrazione Ospiti'))
        self.geometry('800x700')
        self.transient(parent)

        self._current_visitor_id = None
        self._build_ui()
        self._load_companies()
        self._load_sponsors()
        
        # Intercetta la chiusura della finestra (X button)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

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

        # Form
        form_frame = ttk.LabelFrame(main_frame, text=self.lang.get('guest_form', 'Dati Visitatore'))
        form_frame.pack(fill='both', expand=True, pady=(0, 10))

        row = 0

        # Company Name (Combobox editabile con filtro)
        ttk.Label(form_frame, text=self.lang.get('company_name', 'Nome Società') + ' *').grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.company_var = tk.StringVar()
        self.company_combo = ttk.Combobox(form_frame, textvariable=self.company_var, width=37)
        self.company_combo.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        self.company_var.trace('w', self._filter_companies)
        self.company_combo.bind('<<ComboboxSelected>>', self._on_company_selected)
        self.company_combo.bind('<FocusOut>', lambda e: self._open_dropdown_if_filtered(self.company_combo))
        self.company_combo.bind('<Return>', lambda e: self._open_dropdown_if_filtered(self.company_combo))
        self._all_companies = []  # Lista completa delle società
        row += 1

        # Guest Name (Combobox editabile con filtro)
        ttk.Label(form_frame, text=self.lang.get('guest_name', 'Nome Ospite') + ' *').grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.guest_var = tk.StringVar()
        self.guest_combo = ttk.Combobox(form_frame, textvariable=self.guest_var, width=37)
        self.guest_var.trace('w', self._filter_guests)
        self.guest_combo.bind('<FocusOut>', lambda e: self._open_dropdown_if_filtered(self.guest_combo))
        self.guest_combo.bind('<Return>', lambda e: self._open_dropdown_if_filtered(self.guest_combo))
        self._all_guests = []  # Lista completa degli ospiti per la società selezionata
        self.guest_combo.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        row += 1

        # Start Visit Date
        ttk.Label(form_frame, text=self.lang.get('start_visit', 'Data Inizio Visita') + ' *').grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.start_date = DateEntry(form_frame, width=35, background='darkblue',
                                     foreground='white', borderwidth=2,
                                     date_pattern='yyyy-mm-dd')
        self.start_date.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        row += 1

        # End Visit Date
        ttk.Label(form_frame, text=self.lang.get('end_visit', 'Data Fine Visita') + ' *').grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.end_date = DateEntry(form_frame, width=35, background='darkblue',
                                   foreground='white', borderwidth=2,
                                   date_pattern='yyyy-mm-dd')
        self.end_date.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        row += 1

        # Purpose
        ttk.Label(form_frame, text=self.lang.get('purpose', 'Motivo della Visita') + ' *').grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.purpose_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.purpose_var, width=40).grid(
            row=row, column=1, padx=5, pady=5, sticky='ew')
        row += 1

        # Welcome Message
        ttk.Label(form_frame, text=self.lang.get('welcome_message', 'Messaggio di Benvenuto')).grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.welcome_var = tk.StringVar(value='Welcome in our factory')
        ttk.Entry(form_frame, textvariable=self.welcome_var, width=40).grid(
            row=row, column=1, padx=5, pady=5, sticky='ew')
        row += 1

        # Sponsor Guy (Combobox editabile con filtro, ma validato)
        ttk.Label(form_frame, text=self.lang.get('sponsor_guy', 'Persona di Riferimento') + ' *').grid(
            row=row, column=0, sticky='w', padx=5, pady=5)
        self.sponsor_var = tk.StringVar()
        self.sponsor_combo = ttk.Combobox(form_frame, textvariable=self.sponsor_var, width=37)
        self.sponsor_combo.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        self.sponsor_var.trace('w', self._filter_sponsors)
        self.sponsor_combo.bind('<FocusOut>', lambda e: self._open_dropdown_if_filtered(self.sponsor_combo))
        self.sponsor_combo.bind('<Return>', lambda e: self._open_dropdown_if_filtered(self.sponsor_combo))
        self._all_sponsors = []  # Lista completa degli sponsor
        row += 1

        # Pulsanti
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'),
                   command=self._on_new).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                   command=self._on_save).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_edit', 'Modifica'),
                   command=self._on_edit).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'),
                   command=self._on_delete).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_close', 'Chiudi'),
                   command=self._on_close).pack(side='left', padx=2)

        form_frame.columnconfigure(1, weight=1)

        # Lista visitatori recenti con filtro data
        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('recent_visitors', 'Visitatori Recenti'))
        list_frame.pack(fill='both', expand=True)

        # Frame filtro data
        filter_frame = ttk.Frame(list_frame)
        filter_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(filter_frame, text=self.lang.get('filter_date', 'Filtra per Data')).pack(side='left', padx=5)
        self.filter_date = DateEntry(filter_frame, width=15, background='darkblue',
                                      foreground='white', borderwidth=2,
                                      date_pattern='yyyy-mm-dd')
        self.filter_date.set_date(datetime.now())
        self.filter_date.pack(side='left', padx=5)
        
        ttk.Button(filter_frame, text=self.lang.get('btn_filter', 'Filtra'),
                   command=self._load_recent_visitors).pack(side='left', padx=5)
        ttk.Button(filter_frame, text=self.lang.get('btn_show_all', 'Mostra Tutti'),
                   command=self._load_all_visitors).pack(side='left', padx=5)
        ttk.Button(filter_frame, text=self.lang.get('btn_print_list', 'Stampa Lista'),
                   command=self._print_filtered_report).pack(side='left', padx=5)

        # TreeView
        columns = ('id', 'company', 'guest', 'start', 'end', 'sponsor')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        self.tree.heading('id', text='ID')
        self.tree.heading('company', text=self.lang.get('company', 'Società'))
        self.tree.heading('guest', text=self.lang.get('guest', 'Ospite'))
        self.tree.heading('start', text=self.lang.get('start', 'Inizio'))
        self.tree.heading('end', text=self.lang.get('end', 'Fine'))
        self.tree.heading('sponsor', text=self.lang.get('sponsor', 'Sponsor'))

        self.tree.column('id', width=40)
        self.tree.column('company', width=150)
        self.tree.column('guest', width=150)
        self.tree.column('start', width=100)
        self.tree.column('end', width=100)
        self.tree.column('sponsor', width=150)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Carica visitatori recenti
        self._load_recent_visitors()

    def _filter_companies(self, *args):
        """Filtra le società durante la digitazione"""
        typed = self.company_var.get().lower()
        if typed == '':
            self.company_combo['values'] = self._all_companies
        else:
            filtered = [c for c in self._all_companies if typed in c.lower()]
            self.company_combo['values'] = filtered

    def _filter_guests(self, *args):
        """Filtra gli ospiti durante la digitazione"""
        typed = self.guest_var.get().lower()
        if typed == '':
            self.guest_combo['values'] = self._all_guests
        else:
            filtered = [g for g in self._all_guests if typed in g.lower()]
            self.guest_combo['values'] = filtered

    def _filter_sponsors(self, *args):
        """Filtra gli sponsor durante la digitazione"""
        typed = self.sponsor_var.get().lower()
        if typed == '':
            self.sponsor_combo['values'] = self._all_sponsors
        else:
            filtered = [s for s in self._all_sponsors if typed in s.lower()]
            self.sponsor_combo['values'] = filtered

    def _open_dropdown_if_filtered(self, combo):
        """Apre il dropdown se ci sono risultati filtrati"""
        try:
            # Apri il dropdown solo se ci sono valori
            if combo['values']:
                combo.event_generate('<Down>')
        except:
            pass

    def _load_companies(self):
        """Carica le società distinte dal database"""
        try:
            query = """
                SELECT DISTINCT CompanyName 
                FROM Employee.dbo.Visitors 
                WHERE CompanyName IS NOT NULL 
                ORDER BY CompanyName
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            companies = [row.CompanyName for row in cursor.fetchall()]
            self._all_companies = companies
            self.company_combo['values'] = companies
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento società: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento società: {str(e)}"
            )

    def _load_guests_by_company(self, company_name):
        """Carica gli ospiti filtrati per società"""
        try:
            query = """
                SELECT DISTINCT GuestName 
                FROM Employee.dbo.Visitors 
                WHERE CompanyName = ? AND GuestName IS NOT NULL
                ORDER BY GuestName
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (company_name,))
            guests = [row.GuestName for row in cursor.fetchall()]
            self._all_guests = guests
            self.guest_combo['values'] = guests
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento ospiti: {e}")

    def _load_sponsors(self):
        """Carica i dipendenti attivi come sponsor"""
        try:
            query = """
                SELECT UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) AS Sponsor
                FROM Employee.dbo.Employees e 
                INNER JOIN Employee.dbo.EmployeeAddress a 
                    ON a.EmployeeId = e.EmployeeId 
                    AND a.DateOut IS NULL 
                INNER JOIN Employee.dbo.EmployeeHireHistory h 
                    ON e.EmployeeId = h.EmployeeId 
                    AND h.EndWorkDate IS NULL 
                    AND h.EmployeeRId = 2
                ORDER BY e.EmployeeName + ' ' + e.EmployeeSurname
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            sponsors = [row.Sponsor for row in cursor.fetchall()]
            self._all_sponsors = sponsors
            self.sponsor_combo['values'] = sponsors
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento sponsor: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento sponsor: {str(e)}"
            )

    def _load_recent_visitors(self):
        """Carica i visitatori filtrati per data"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            filter_date = self.filter_date.get_date()

            query = """
                SELECT 
                    VisitorId, CompanyName, GuestName, 
                    StartVisit, EndVisit, SponsorGuy
                FROM Employee.dbo.Visitors
                WHERE  ? between CAST(StartVisit AS DATE)  and cast(EndVisit as date)
                ORDER BY VisitorId DESC
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (filter_date,))
            
            for row in cursor.fetchall():
                start_str = row.StartVisit.strftime('%Y-%m-%d') if row.StartVisit else ''
                end_str = row.EndVisit.strftime('%Y-%m-%d') if row.EndVisit else ''
                self.tree.insert('', 'end', values=(
                    row.VisitorId,
                    row.CompanyName or '',
                    row.GuestName or '',
                    start_str,
                    end_str,
                    row.SponsorGuy or ''
                ))
            
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento visitatori filtrati: {e}")

    def _load_all_visitors(self):
        """Carica tutti i visitatori recenti (ultimi 30 giorni)"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            query = """
                SELECT TOP 50 
                    VisitorId, CompanyName, GuestName, 
                    StartVisit, EndVisit, SponsorGuy
                FROM Employee.dbo.Visitors
                WHERE StartVisit >= DATEADD(day, -30, GETDATE())
                ORDER BY VisitorId DESC
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            
            for row in cursor.fetchall():
                start_str = row.StartVisit.strftime('%Y-%m-%d') if row.StartVisit else ''
                end_str = row.EndVisit.strftime('%Y-%m-%d') if row.EndVisit else ''
                self.tree.insert('', 'end', values=(
                    row.VisitorId,
                    row.CompanyName or '',
                    row.GuestName or '',
                    start_str,
                    end_str,
                    row.SponsorGuy or ''
                ))
            
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento tutti i visitatori: {e}")

    def _on_company_selected(self, event):
        """Gestisce la selezione della società"""
        company = self.company_var.get()
        if company:
            self._load_guests_by_company(company)

    def _on_select(self, event):
        """Gestisce la selezione di un visitatore dalla lista"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self._current_visitor_id = values[0]
        self.company_var.set(values[1])
        self.guest_var.set(values[2])
        
        # Carica gli ospiti per la società selezionata
        if values[1]:
            self._load_guests_by_company(values[1])

        # Parse dates
        if values[3]:
            try:
                start_dt = datetime.strptime(values[3], '%Y-%m-%d')
                self.start_date.set_date(start_dt)
            except:
                pass

        if values[4]:
            try:
                end_dt = datetime.strptime(values[4], '%Y-%m-%d')
                self.end_date.set_date(end_dt)
            except:
                pass

        self.sponsor_var.set(values[5])

    def _on_new(self):
        """Pulisce il form per un nuovo inserimento"""
        self._current_visitor_id = None
        self.company_var.set('')
        self.guest_var.set('')
        self.start_date.set_date(datetime.now())
        self.end_date.set_date(datetime.now())
        self.purpose_var.set('')
        self.welcome_var.set('Welcome in our factory')
        self.sponsor_var.set('')
        self.guest_combo['values'] = []

    def _on_close(self):
        """Gestisce la chiusura della finestra con prompt per prenotazione sala riunioni"""
        # Chiedi se l'utente vuole prenotare una meeting room
        response = messagebox.askyesno(
            self.lang.get('book_meeting_room', 'Prenotazione Sala'),
            self.lang.get('book_meeting_room_question', 'Vuoi prenotare una sala riunioni?')
        )
        
        if response:
            # Apri la finestra di prenotazione sale con dati preimpostati
            self._open_room_booking()
        else:
            # Chiudi la finestra
            self.destroy()
    
    def _open_room_booking(self):
        """Apre la finestra di prenotazione sale con dati preimpostati"""
        try:
            # Importa la classe BookingManagerWindow
            from room_booking_gui import BookingManagerWindow
            
            # Recupera le date e ore dal form ospiti
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()
            
            logger.info(f"Apertura finestra prenotazione sale - Date: {start_date} - {end_date}")
            
            # Crea la finestra di prenotazione usando self.master come parent
            # (non self, altrimenti si chiude quando chiudiamo questa finestra)
            booking_window = BookingManagerWindow(self.master, self.db, self.lang, self.user_name)
            
            # Preimposta i campi con i dati degli ospiti
            booking_window.start_date_var.set(start_date.strftime('%Y-%m-%d'))
            booking_window.end_date_var.set(end_date.strftime('%Y-%m-%d'))
            
            # Imposta ore di default per la riunione (es. 09:00 - 17:00)
            booking_window.start_time_var.set('09:00')
            booking_window.end_time_var.set('17:00')
            
            logger.info("Finestra prenotazione sale aperta con successo")
            
            # Chiudi la finestra ospiti DOPO un breve delay per permettere alla finestra booking di aprirsi
            self.after(100, self.destroy)
            
        except Exception as e:
            logger.error(f"Errore apertura finestra prenotazione sale: {e}")
            import traceback
            logger.error(traceback.format_exc())
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante l'apertura della prenotazione sale: {str(e)}"
            )
            # In caso di errore, chiudi comunque la finestra
            self.destroy()


    def _on_closing(self):
        """Gestisce la chiusura della finestra stampando la lista giornaliera"""
        try:
            self._print_daily_report()
        except Exception as e:
            logger.error(f"Errore stampa lista giornaliera: {e}")
        finally:
            self.destroy()

    def _print_daily_report(self):
        """Stampa la lista giornaliera dei visitatori in formato professionale rumeno"""
        try:
            from datetime import datetime
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import ImageReader
            import os
            import tempfile
            import subprocess
            
            # Query per ottenere i visitatori del giorno
            today = datetime.now().date()
            query = """
                SELECT 
                    GuestName,
                    CompanyName,
                    StartVisit,
                    EndVisit
                FROM [Employee].[dbo].[Visitors]
                WHERE CAST(StartVisit AS DATE) = ?
                ORDER BY GuestName
            """
            
            cursor = self.db.conn.cursor()
            cursor.execute(query, (today,))
            visitors = cursor.fetchall()
            cursor.close()
            
            if not visitors:
                logger.info("Nessun visitatore per oggi, stampa annullata")
                return
            
            # Crea PDF temporaneo
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            pdf_path = temp_pdf.name
            temp_pdf.close()
            
            # Crea PDF
            c = canvas.Canvas(pdf_path, pagesize=A4)
            width, height = A4
            
            # Logo
            logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
            if os.path.exists(logo_path):
                img = ImageReader(logo_path)
                c.drawImage(img, 2*cm, height - 4*cm, width=4*cm, height=2*cm, preserveAspectRatio=True)
            
            # Titolo
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(width/2, height - 5*cm, "LISTĂ VIZITATORI PREZENȚI")
            
            # Data
            c.setFont("Helvetica", 12)
            data_ro = today.strftime("%d.%m.%Y")
            c.drawCentredString(width/2, height - 6*cm, f"Data: {data_ro}")
            
            # Tabella visitatori
            y = height - 8*cm
            c.setFont("Helvetica-Bold", 10)
            c.drawString(2*cm, y, "Nume Vizitator")
            c.drawString(8*cm, y, "Companie")
            c.drawString(13*cm, y, "Ora Sosire")
            c.drawString(16*cm, y, "Ora Plecare")
            
            # Linea separatrice
            y -= 0.3*cm
            c.line(2*cm, y, width - 2*cm, y)
            y -= 0.5*cm
            
            # Dati visitatori
            c.setFont("Helvetica", 9)
            for visitor in visitors:
                if y < 4*cm:  # Nuova pagina se necessario
                    c.showPage()
                    y = height - 3*cm
                    c.setFont("Helvetica", 9)
                
                guest_name = visitor.GuestName or ''
                company = visitor.CompanyName or ''
                start_time = visitor.StartVisit.strftime("%H:%M") if visitor.StartVisit else ''
                end_time = visitor.EndVisit.strftime("%H:%M") if visitor.EndVisit else 'În curs'
                
                c.drawString(2*cm, y, guest_name[:35])  # Limita lunghezza
                c.drawString(8*cm, y, company[:25])
                c.drawString(13*cm, y, start_time)
                c.drawString(16*cm, y, end_time)
                
                y -= 0.6*cm
            
            # Nota legale in rumeno (ben formattata)
            y -= 1*cm
            if y < 6*cm:
                c.showPage()
                y = height - 3*cm
            
            c.setFont("Helvetica-Bold", 10)
            c.drawString(2*cm, y, f"Listă persoane prezente în Vandewiele Romania pentru ziua {data_ro}")
            y -= 0.8*cm
            
            c.setFont("Helvetica", 9)
            text_lines = [
                "Prezenta listă trebuie păstrată de departamentul de personal și predată",
                "responsabililor în caz de evenimente catastrofale (cum ar fi incendii,",
                "cutremure sau alte tipuri de calamități)."
            ]
            
            for line in text_lines:
                c.drawString(2*cm, y, line)
                y -= 0.5*cm
            
            # Footer
            c.setFont("Helvetica-Oblique", 8)
            c.drawCentredString(width/2, 1.5*cm, "Document generat automat - Vandewiele Romania")
            
            c.save()
            
            # Stampa su stampante di default
            if os.name == 'nt':  # Windows
                os.startfile(pdf_path, "print")
            else:  # Linux/Mac
                subprocess.run(['lpr', pdf_path])
            
            logger.info(f"Lista giornaliera stampata: {len(visitors)} visitatori")
            
        except ImportError:
            logger.error("Libreria reportlab non installata. Eseguire: pip install reportlab")
        except Exception as e:
            logger.error(f"Errore stampa lista giornaliera: {e}")
            import traceback
            traceback.print_exc()

    def _print_filtered_report(self):
        """Stampa la lista dei visitatori per la data filtrata dall'utente"""
        try:
            from datetime import datetime
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import ImageReader
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os
            import tempfile
            
            # Registra font Unicode per supportare caratteri rumeni
            try:
                pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
                pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
                font_name = 'DejaVuSans'
                font_name_bold = 'DejaVuSans-Bold'
            except:
                try:
                    pdfmetrics.registerFont(TTFont('ArialUnicode', 'ARIALUNI.TTF'))
                    font_name = 'ArialUnicode'
                    font_name_bold = 'ArialUnicode'
                except:
                    font_name = 'Helvetica'
                    font_name_bold = 'Helvetica-Bold'
            
            # Usa la data del filtro
            filter_date = self.filter_date.get_date()
            
            # Query per ottenere i visitatori della data filtrata
            query = """
                SELECT 
                    GuestName,
                    CompanyName,
                    StartVisit,
                    EndVisit
                FROM [Employee].[dbo].[Visitors]
                WHERE CAST(StartVisit AS DATE) = ?
                ORDER BY GuestName
            """
            
            cursor = self.db.conn.cursor()
            cursor.execute(query, (filter_date,))
            visitors = cursor.fetchall()
            cursor.close()
            
            if not visitors:
                messagebox.showinfo(
                    self.lang.get('info', 'Informazione'),
                    self.lang.get('no_visitors_for_date', f'Nessun visitatore per la data {filter_date.strftime("%d/%m/%Y")}')
                )
                return
            
            # Crea PDF temporaneo
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            pdf_path = temp_pdf.name
            temp_pdf.close()
            
            # Crea PDF
            c = canvas.Canvas(pdf_path, pagesize=A4)
            width, height = A4
            
            # Logo
            logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
            if os.path.exists(logo_path):
                img = ImageReader(logo_path)
                c.drawImage(img, 2*cm, height - 4*cm, width=4*cm, height=2*cm, preserveAspectRatio=True)
            
            # Titolo
            c.setFont(font_name_bold, 16)
            c.drawCentredString(width/2, height - 5*cm, "LISTĂ VIZITATORI PREZENȚI")
            
            # Data
            c.setFont(font_name, 12)
            data_ro = filter_date.strftime("%d.%m.%Y")
            c.drawCentredString(width/2, height - 6*cm, f"Data: {data_ro}")
            
            # Tabella visitatori
            y = height - 8*cm
            c.setFont(font_name_bold, 10)
            c.drawString(2*cm, y, "Nume Vizitator")
            c.drawString(8*cm, y, "Companie")
            c.drawString(13*cm, y, "Ora Sosire")
            c.drawString(16*cm, y, "Ora Plecare")
            
            # Linea separatrice
            y -= 0.3*cm
            c.line(2*cm, y, width - 2*cm, y)
            y -= 0.5*cm
            
            # Dati visitatori
            c.setFont(font_name, 9)
            for visitor in visitors:
                if y < 4*cm:  # Nuova pagina se necessario
                    c.showPage()
                    y = height - 3*cm
                    c.setFont(font_name, 9)
                
                guest_name = visitor.GuestName or ''
                company = visitor.CompanyName or ''
                start_time = visitor.StartVisit.strftime("%H:%M") if visitor.StartVisit else ''
                end_time = visitor.EndVisit.strftime("%H:%M") if visitor.EndVisit else 'În curs'
                
                c.drawString(2*cm, y, guest_name[:35])
                c.drawString(8*cm, y, company[:25])
                c.drawString(13*cm, y, start_time)
                c.drawString(16*cm, y, end_time)
                
                y -= 0.6*cm
            
            # Nota legale in rumeno
            y -= 1*cm
            if y < 6*cm:
                c.showPage()
                y = height - 3*cm
            
            c.setFont(font_name_bold, 10)
            c.drawString(2*cm, y, f"Listă persoane prezente în Vandewiele Romania pentru ziua {data_ro}")
            y -= 0.8*cm
            
            c.setFont(font_name, 9)
            text_lines = [
                "Prezenta listă trebuie păstrată de departamentul de personal și predată",
                "responsabililor în caz de evenimente catastrofale (cum ar fi incendii,",
                "cutremure sau alte tipuri de calamități)."
            ]
            
            for line in text_lines:
                c.drawString(2*cm, y, line)
                y -= 0.5*cm
            
            # Footer
            c.setFont(font_name, 8)
            c.drawCentredString(width/2, 1.5*cm, "Document generat automat - Vandewiele Romania")
            
            c.save()
            
            # Stampa su stampante di default
            if os.name == 'nt':  # Windows
                os.startfile(pdf_path, "print")
            else:  # Linux/Mac
                import subprocess
                subprocess.run(['lpr', pdf_path])
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('list_printed', f'Lista stampata: {len(visitors)} visitatori')
            )
            
            logger.info(f"Lista stampata per {data_ro}: {len(visitors)} visitatori")
            
        except ImportError:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('missing_reportlab', 'Libreria reportlab non installata.\nEseguire: pip install reportlab')
            )
        except Exception as e:
            logger.error(f"Errore stampa lista filtrata: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante la stampa: {str(e)}"
            )

    def _on_save(self):
        """Salva il visitatore"""
        # Validazione
        if not self.company_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_company', 'Inserire il nome della società')
            )
            return

        if not self.guest_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_guest', 'Inserire il nome dell\'ospite')
            )
            return

        if not self.purpose_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_purpose', 'Inserire il motivo della visita')
            )
            return

        if not self.sponsor_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_sponsor', 'Inserire la persona di riferimento')
            )
            return

        # Validazione sponsor: deve essere nella lista
        sponsor = self.sponsor_var.get().strip()
        if sponsor not in self._all_sponsors:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('invalid_sponsor', 'Lo sponsor selezionato non è valido. Selezionare dalla lista.')
            )
            return

        try:
            # Recupera i dati
            company = self.company_var.get().strip()
            guest = self.guest_var.get().strip().upper()  # Salva in maiuscolo
            start_visit = self.start_date.get_date()
            end_visit = self.end_date.get_date()
            pourpose = self.purpose_var.get().strip()
            welcome = self.welcome_var.get().strip()
            sponsor = self.sponsor_var.get().strip()

            # Validazione date
            if end_visit < start_visit:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('invalid_date_range', 'La data di fine deve essere successiva alla data di inizio')
                )
                return

            # Calcola ShowFrom e ShowUntil
            show_from = datetime.combine(start_visit, datetime.strptime('08:30', '%H:%M').time())
            show_until = datetime.combine(end_visit, datetime.strptime('17:00', '%H:%M').time())

            # Recupera RegistryId dall'utente loggato
            registry_id = self._get_registry_id(self.user_name)

            if self._current_visitor_id:
                # Update
                query = """
                    UPDATE Employee.dbo.Visitors
                    SET CompanyName = ?,
                        GuestName = ?,
                        StartVisit = ?,
                        EndVisit = ?,
                        Pourpose = ?,
                        WelcomeMessage = ?,
                        SponsorGuy = ?,
                        ShowFrom = ?,
                        ShowUntil = ?
                    WHERE VisitorId = ?
                """
                cursor = self.db.conn.cursor()
                cursor.execute(query, (
                    company, guest, start_visit, end_visit,
                    pourpose, welcome, sponsor, show_from, show_until,
                    self._current_visitor_id
                ))
                self.db.conn.commit()
                cursor.close()
                message = self.lang.get('visitor_updated', 'Visitatore aggiornato con successo')
            else:
                # Insert
                query = """
                    INSERT INTO Employee.dbo.Visitors (
                        RegistryId, CompanyName, GuestName, StartVisit, EndVisit,
                        Pourpose, WelcomeMessage, ShowFrom, ShowUntil, 
                        IsActive, CreatedAt, SponsorGuy
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, GETDATE(), ?)
                """
                cursor = self.db.conn.cursor()
                cursor.execute(query, (
                    registry_id, company, guest, start_visit, end_visit,
                    pourpose, welcome, show_from, show_until, sponsor
                ))
                self.db.conn.commit()
                cursor.close()
                message = self.lang.get('visitor_saved', 'Visitatore registrato con successo')

            messagebox.showinfo(self.lang.get('success', 'Successo'), message)
            
            # Ricarica le liste
            self._load_companies()
            self._load_recent_visitors()
            self._on_new()

        except Exception as e:
            logger.error(f"Errore salvataggio visitatore: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante il salvataggio: {str(e)}"
            )

    def _get_registry_id(self, user_name):
        """Recupera il RegistryId chiamando la stored procedure Employee.dbo.registro"""
        try:
            from datetime import datetime
            
            # Parametri per la stored procedure
            registry_type_id = 930
            anno = datetime.now().year
            data_documento = datetime.now().date()
            issued_by = user_name
            employeer_id = 2
            
            # Chiama la stored procedure
            query = """
                EXEC Employee.dbo.registro 
                    @RegistryTypeId = ?, 
                    @anno = ?, 
                    @DataDocumento = ?, 
                    @IussedBy = ?, 
                    @EmployeerId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (registry_type_id, anno, data_documento, issued_by, employeer_id))
            
            # La stored procedure dovrebbe restituire il RegistryId
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                # Assumendo che la stored procedure restituisca il RegistryId come primo campo
                registry_id = row[0]
                logger.info(f"RegistryId generato: {registry_id} per utente: {user_name}")
                return registry_id
            else:
                logger.warning(f"Stored procedure non ha restituito RegistryId per utente: {user_name}")
                return None
                
        except Exception as e:
            logger.error(f"Errore chiamata stored procedure registro: {e}")
            return None

    def _on_edit(self):
        """Carica i dati del visitatore selezionato per la modifica"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_visitor_to_edit', 'Selezionare un visitatore da modificare')
            )
            return
        
        # Carica i dati nel form dalla TreeView
        item = self.tree.item(selection[0])
        values = item['values']
        
        self._current_visitor_id = values[0]
        self.company_var.set(values[1])
        self.guest_var.set(values[2])
        
        # Parse dates
        if values[3]:
            try:
                start_dt = datetime.strptime(values[3], '%Y-%m-%d')
                self.start_date.set_date(start_dt)
            except:
                pass
        
        if values[4]:
            try:
                end_dt = datetime.strptime(values[4], '%Y-%m-%d')
                self.end_date.set_date(end_dt)
            except:
                pass
        
        self.sponsor_var.set(values[5])
        
        # Carica anche Purpose e Welcome dal database
        try:
            query = """
                SELECT Pourpose, WelcomeMessage
                FROM [Employee].[dbo].[Visitors]
                WHERE VisitorId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self._current_visitor_id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                self.purpose_var.set(row.Pourpose or '')
                self.welcome_var.set(row.WelcomeMessage or 'Welcome in our factory')
        except Exception as e:
            logger.error(f"Errore caricamento dati visitatore: {e}")

    def _on_delete(self):
        """Elimina il visitatore selezionato (solo per il giorno corrente)"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_visitor_to_edit', 'Selezionare un visitatore da eliminare')
            )
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        visitor_id = values[0]
        
        try:
            # Verifica che sia del giorno corrente
            query = """
                SELECT CAST(StartVisit AS DATE) as VisitDate
                FROM [Employee].[dbo].[Visitors]
                WHERE VisitorId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (visitor_id,))
            row = cursor.fetchone()
            cursor.close()
            
            if not row:
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    self.lang.get('visitor_not_found', 'Visitatore non trovato')
                )
                return
            
            visit_date = row.VisitDate
            today = datetime.now().date()
            
            if visit_date != today:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('cannot_delete_old_visitor', 'È possibile eliminare solo i visitatori del giorno corrente')
                )
                return
            
            # Conferma eliminazione
            if not messagebox.askyesno(
                self.lang.get('confirm', 'Conferma'),
                self.lang.get('confirm_delete_visitor', 'Eliminare il visitatore selezionato?')
            ):
                return
            
            # Elimina
            delete_query = """
                DELETE FROM [Employee].[dbo].[Visitors]
                WHERE VisitorId = ?
            """
            cursor = self.db.conn.cursor()
            cursor.execute(delete_query, (visitor_id,))
            self.db.conn.commit()
            cursor.close()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('visitor_deleted', 'Visitatore eliminato con successo')
            )
            
            self._on_new()
            self._load_recent_visitors()
            
        except Exception as e:
            logger.error(f"Errore eliminazione visitatore: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante l'eliminazione: {str(e)}"
            )


class GuestReportWindow(tk.Toplevel):
    """Finestra per visualizzare il report degli ospiti"""

    def __init__(self, parent, db_handler, lang_manager):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager

        self.title(self.lang.get('guest_report_title', 'Report Ospiti'))
        self.geometry('1200x600')
        self.transient(parent)

        self._build_ui()
        self._load_visitors()

    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Frame filtri
        filter_frame = ttk.LabelFrame(self, text=self.lang.get('filters', 'Filtri'))
        filter_frame.pack(fill='x', padx=10, pady=5)

        # Data inizio
        ttk.Label(filter_frame, text=self.lang.get('from_date', 'Da Data')).grid(
            row=0, column=0, padx=5, pady=5, sticky='w')
        self.from_date = DateEntry(filter_frame, width=15, background='darkblue',
                                    foreground='white', borderwidth=2,
                                    date_pattern='yyyy-mm-dd')
        self.from_date.set_date(datetime.now() - timedelta(days=30))
        self.from_date.grid(row=0, column=1, padx=5, pady=5)

        # Data fine
        ttk.Label(filter_frame, text=self.lang.get('to_date', 'A Data')).grid(
            row=0, column=2, padx=5, pady=5, sticky='w')
        self.to_date = DateEntry(filter_frame, width=15, background='darkblue',
                                  foreground='white', borderwidth=2,
                                  date_pattern='yyyy-mm-dd')
        self.to_date.set_date(datetime.now() + timedelta(days=30))
        self.to_date.grid(row=0, column=3, padx=5, pady=5)

        # Pulsante ricerca
        ttk.Button(filter_frame, text=self.lang.get('search', 'Cerca'),
                   command=self._load_visitors).grid(row=0, column=4, padx=5, pady=5)
        
        # Pulsante genera report PDF
        ttk.Button(filter_frame, text=self.lang.get('generate_pdf_report', 'Genera Report PDF'),
                   command=self._generate_pdf_report).grid(row=0, column=5, padx=5, pady=5)

        # TreeView
        list_frame = ttk.Frame(self)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)

        columns = ('id', 'company', 'guest', 'start', 'end', 'purpose', 'sponsor', 'welcome')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('company', text=self.lang.get('company', 'Società'))
        self.tree.heading('guest', text=self.lang.get('guest', 'Ospite'))
        self.tree.heading('start', text=self.lang.get('start', 'Inizio'))
        self.tree.heading('end', text=self.lang.get('end', 'Fine'))
        self.tree.heading('purpose', text=self.lang.get('purpose', 'Motivo'))
        self.tree.heading('sponsor', text=self.lang.get('sponsor', 'Sponsor'))
        self.tree.heading('welcome', text=self.lang.get('welcome', 'Messaggio'))

        self.tree.column('id', width=40)
        self.tree.column('company', width=150)
        self.tree.column('guest', width=150)
        self.tree.column('start', width=100)
        self.tree.column('end', width=100)
        self.tree.column('purpose', width=150)
        self.tree.column('sponsor', width=150)
        self.tree.column('welcome', width=200)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def _load_visitors(self):
        """Carica i visitatori nel periodo selezionato"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            from_date = self.from_date.get_date()
            to_date = self.to_date.get_date()

            query = """
                SELECT 
                    VisitorId, CompanyName, GuestName, 
                    StartVisit, EndVisit, Pourpose, SponsorGuy, WelcomeMessage
                FROM Employee.dbo.Visitors
                WHERE StartVisit >= ? AND StartVisit <= ?
                ORDER BY StartVisit DESC
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query, (from_date, to_date))
            
            for row in cursor.fetchall():
                start_str = row.StartVisit.strftime('%Y-%m-%d') if row.StartVisit else ''
                end_str = row.EndVisit.strftime('%Y-%m-%d') if row.EndVisit else ''
                self.tree.insert('', 'end', values=(
                    row.VisitorId,
                    row.CompanyName or '',
                    row.GuestName or '',
                    start_str,
                    end_str,
                    row.Pourpose or '',
                    row.SponsorGuy or '',
                    row.WelcomeMessage or ''
                ))
            
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento visitatori: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante il caricamento: {str(e)}"
            )

    def _generate_pdf_report(self):
        """Genera un report PDF dei visitatori presenti in fabbrica e aggiorna PrintedOn"""
        try:
            from datetime import datetime
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import ImageReader
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os
            
            # Registra font Unicode per supportare caratteri rumeni
            try:
                pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
                pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
                font_name = 'DejaVuSans'
                font_name_bold = 'DejaVuSans-Bold'
            except:
                try:
                    pdfmetrics.registerFont(TTFont('ArialUnicode', 'ARIALUNI.TTF'))
                    font_name = 'ArialUnicode'
                    font_name_bold = 'ArialUnicode'
                except:
                    font_name = 'Helvetica'
                    font_name_bold = 'Helvetica-Bold'
            
            # Ottieni la data corrente
            today = datetime.now().date()
            
            # Query per ottenere i visitatori presenti oggi
            query = """
                SELECT 
                    VisitorId,
                    GuestName,
                    CompanyName,
                    StartVisit,
                    EndVisit,
                    SponsorGuy
                FROM [Employee].[dbo].[Visitors]
                WHERE CAST(StartVisit AS DATE) <= ?
                  AND CAST(EndVisit AS DATE) >= ?
                  AND (PrintedOn IS NULL OR CAST(PrintedOn AS DATE) < ?)
                ORDER BY GuestName
            """
            
            cursor = self.db.conn.cursor()
            cursor.execute(query, (today, today, today))
            visitors = cursor.fetchall()
            cursor.close()
            
            if not visitors:
                messagebox.showinfo(
                    self.lang.get('info', 'Informazione'),
                    self.lang.get('no_visitors_today', 'Nessun visitatore presente oggi da stampare')
                )
                return
            
            # Crea directory C:\Temp se non esiste
            temp_dir = r'C:\Temp'
            os.makedirs(temp_dir, exist_ok=True)
            
            # Crea nome file con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_filename = f'Visitors_Report_{timestamp}.pdf'
            pdf_path = os.path.join(temp_dir, pdf_filename)
            
            # Crea PDF
            c = canvas.Canvas(pdf_path, pagesize=A4)
            width, height = A4
            
            # Logo
            logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
            if os.path.exists(logo_path):
                img = ImageReader(logo_path)
                c.drawImage(img, 2*cm, height - 4*cm, width=4*cm, height=2*cm, preserveAspectRatio=True)
            
            # Titolo
            c.setFont(font_name_bold, 16)
            c.drawCentredString(width/2, height - 5*cm, "LISTĂ VIZITATORI PREZENȚI")
            
            # Data
            c.setFont(font_name, 12)
            data_ro = today.strftime("%d.%m.%Y")
            c.drawCentredString(width/2, height - 6*cm, f"Data: {data_ro}")
            
            # Tabella visitatori
            y = height - 8*cm
            c.setFont(font_name_bold, 10)
            c.drawString(2*cm, y, "Nume Vizitator")
            c.drawString(8*cm, y, "Companie")
            c.drawString(13*cm, y, "Ora Sosire")
            c.drawString(16*cm, y, "Ora Plecare")
            
            # Linea separatrice
            y -= 0.3*cm
            c.line(2*cm, y, width - 2*cm, y)
            y -= 0.5*cm
            
            # Dati visitatori
            c.setFont(font_name, 9)
            visitor_ids = []  # Lista per tracciare gli ID dei visitatori stampati
            
            for visitor in visitors:
                if y < 4*cm:  # Nuova pagina se necessario
                    c.showPage()
                    y = height - 3*cm
                    c.setFont(font_name, 9)
                
                visitor_ids.append(visitor.VisitorId)
                guest_name = visitor.GuestName or ''
                company = visitor.CompanyName or ''
                start_time = visitor.StartVisit.strftime("%H:%M") if visitor.StartVisit else ''
                end_time = visitor.EndVisit.strftime("%H:%M") if visitor.EndVisit else 'În curs'
                
                c.drawString(2*cm, y, guest_name[:35])
                c.drawString(8*cm, y, company[:25])
                c.drawString(13*cm, y, start_time)
                c.drawString(16*cm, y, end_time)
                
                y -= 0.6*cm
            
            # Nota legale in rumeno
            y -= 1*cm
            if y < 6*cm:
                c.showPage()
                y = height - 3*cm
            
            c.setFont(font_name_bold, 10)
            c.drawString(2*cm, y, f"Listă persoane prezente în Vandewiele Romania pentru ziua {data_ro}")
            y -= 0.8*cm
            
            c.setFont(font_name, 9)
            text_lines = [
                "Prezenta listă trebuie păstrată de departamentul de personal și predată",
                "responsabililor în caz de evenimente catastrofale (cum ar fi incendii,",
                "cutremure sau alte tipuri de calamități)."
            ]
            
            for line in text_lines:
                c.drawString(2*cm, y, line)
                y -= 0.5*cm
            
            # Footer
            c.setFont(font_name, 8)
            c.drawCentredString(width/2, 1.5*cm, "Document generat automat - Vandewiele Romania")
            
            c.save()
            
            # Aggiorna PrintedOn per tutti i visitatori stampati
            if visitor_ids:
                try:
                    placeholders = ','.join(['?' for _ in visitor_ids])
                    update_query = f"""
                        UPDATE [Employee].[dbo].[Visitors]
                        SET PrintedOn = GETDATE()
                        WHERE VisitorId IN ({placeholders})
                    """
                    cursor = self.db.conn.cursor()
                    cursor.execute(update_query, visitor_ids)
                    self.db.conn.commit()
                    cursor.close()
                    logger.info(f"PrintedOn aggiornato per {len(visitor_ids)} visitatori")
                except Exception as e:
                    logger.error(f"Errore aggiornamento PrintedOn: {e}")
            
            # Apri il PDF
            if os.name == 'nt':  # Windows
                os.startfile(pdf_path)
            else:  # Linux/Mac
                import subprocess
                subprocess.run(['xdg-open', pdf_path])
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                f"Report PDF generato con successo:\n{pdf_path}\n\nVisitatori: {len(visitors)}"
            )
            
            logger.info(f"Report PDF generato: {pdf_path} ({len(visitors)} visitatori)")
            
        except ImportError:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('missing_reportlab', 'Libreria reportlab non installata.\nEseguire: pip install reportlab')
            )
        except Exception as e:
            logger.error(f"Errore generazione report PDF: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante la generazione del report: {str(e)}"
            )

