# -*- coding: utf-8 -*-
"""
Modulo per la gestione delle note disciplinari (Referat).
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import logging
import os

logger = logging.getLogger("TraceabilityRS")


class DisciplinaryClaimWindow(tk.Toplevel):
    """Finestra per emissione note disciplinari (Referat)."""

    def __init__(self, parent, db_handler, lang_manager, author_name, author_user_id=None):
        super().__init__(parent)
        self.parent = parent
        self.db = db_handler
        self.lang = lang_manager
        self.author_name = author_name or "Unknown"
        self.author_user_id = author_user_id

        # Dati correnti
        self.selected_employee_id = None
        self.selected_employee_name = None
        self.selected_employee_sex = None
        self.selected_employee_cdc = None
        self.selected_cause_id = None
        self.selected_cause_text = None
        self.selected_cause_article = None
        self.referat_id = None
        self.doc_name = None

        self.title("Emitere notă disciplinară")
        self.geometry("900x650")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._load_author_info()
        self._create_widgets()
        self._load_employees()
        self._load_disciplinary_causes()

    def _load_author_info(self):
        """Carica informazioni sull'autore (cost center, department)."""
        self.author_department = ""
        self.author_cost_center_id = None
        self.author_email = None
        self.author_is_global = False
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.EmployeeHireHistoryId, e.EmployeeName, e.EmployeeSurname,
                       cc.CostCenterDesc, h.CostCenterId, e.WorkEmail
                FROM Employee.dbo.EmployeeHireHistory h
                INNER JOIN Employee.dbo.Employees e ON e.EmployeeId = h.EmployeeId
                LEFT JOIN Employee.dbo.CostCenters cc ON cc.CostCenterId = h.CostCenterId
                WHERE h.DateEnd IS NULL
                  AND (e.EmployeeName + ' ' + e.EmployeeSurname = ?
                       OR e.EmployeeSurname + ' ' + e.EmployeeName = ?)
            """, (self.author_name, self.author_name))
            row = cursor.fetchone()
            if row:
                self.author_department = row.CostCenterDesc or ""
                self.author_cost_center_id = row.CostCenterId
                self.author_email = row.WorkEmail
            cursor.close()
        except Exception as e:
            logger.warning(f"Errore caricamento info autore: {e}")

    def _create_widgets(self):
        """Crea i widget della finestra."""
        # === HEADER ===
        header_frame = tk.Frame(self, bg="white", pady=8)
        header_frame.pack(fill=tk.X)

        # Logo
        logo_path = "Logo.png"
        if os.path.exists(logo_path):
            try:
                self._logo_image = tk.PhotoImage(file=logo_path)
                # Ridimensiona se necessario
                w, h = self._logo_image.width(), self._logo_image.height()
                if w > 120:
                    factor = max(1, w // 120)
                    self._logo_image = self._logo_image.subsample(factor, factor)
                logo_label = tk.Label(header_frame, image=self._logo_image, bg="white")
                logo_label.pack(side=tk.LEFT, padx=10)
            except Exception:
                pass

        title_label = tk.Label(
            header_frame, text="Emitere notă disciplinară",
            font=("Arial", 16, "bold"), fg="#B22222", bg="white"
        )
        title_label.pack(side=tk.TOP, pady=(5, 0))

        author_text = f"Departament: {self.author_department}, procedura pornită de către {self.author_name}"
        self.author_label = tk.Label(
            header_frame, text=author_text,
            font=("Arial", 9), bg="white"
        )
        self.author_label.pack(side=tk.TOP)

        ttk.Separator(self, orient="horizontal").pack(fill=tk.X)

        # === FORM BODY ===
        form_frame = tk.Frame(self, padx=15, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)

        row = 0
        # Data Referat
        tk.Label(form_frame, text="Data Referat:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="w", pady=5)
        self.date_referat_var = tk.StringVar(value=date.today().strftime('%d-%m-%Y'))
        self.date_referat_entry = tk.Entry(
            form_frame, textvariable=self.date_referat_var, width=15,
            font=("Arial", 10))
        self.date_referat_entry.grid(row=row, column=1, sticky="w", padx=5, pady=5)

        # Employee dropdown
        tk.Label(form_frame, text="Angajatul:", font=("Arial", 10)).grid(
            row=row, column=2, sticky="w", pady=5, padx=(20, 5))
        self.employee_combo = ttk.Combobox(
            form_frame, width=40, state="readonly", font=("Arial", 10))
        self.employee_combo.grid(row=row, column=3, sticky="w", padx=5, pady=5)
        self.employee_combo.bind("<<ComboboxSelected>>", self._on_employee_selected)

        # History button
        self.history_btn = tk.Button(
            form_frame, text="📋", font=("Arial", 12),
            command=self._show_history, state="disabled",
            relief="flat", cursor="hand2"
        )
        self.history_btn.grid(row=row, column=4, padx=5, pady=5)

        row += 1
        # Disciplinary causes
        tk.Label(form_frame, text="Cazuri de abatere disciplinară:", font=("Arial", 10)).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=5)
        self.cause_combo = ttk.Combobox(
            form_frame, width=80, state="readonly", font=("Arial", 9))
        self.cause_combo.grid(row=row, column=2, columnspan=3, sticky="we", padx=5, pady=5)
        self.cause_combo.bind("<<ComboboxSelected>>", self._on_cause_selected)

        row += 1
        # Data eveniment + Ora eveniment
        tk.Label(form_frame, text="Data eveniment:", font=("Arial", 10)).grid(
            row=row, column=0, sticky="w", pady=5)
        self.date_event_var = tk.StringVar()
        self.date_event_entry = tk.Entry(
            form_frame, textvariable=self.date_event_var, width=15,
            font=("Arial", 10))
        self.date_event_entry.grid(row=row, column=1, sticky="w", padx=5, pady=5)

        tk.Label(form_frame, text="Ora eveniment:", font=("Arial", 10)).grid(
            row=row, column=2, sticky="w", pady=5, padx=(20, 5))
        self.time_event_var = tk.StringVar()
        self.time_event_entry = tk.Entry(
            form_frame, textvariable=self.time_event_var, width=8,
            font=("Arial", 10))
        self.time_event_entry.grid(row=row, column=3, sticky="w", padx=5, pady=5)

        row += 1
        # Motivul referatului
        tk.Label(
            form_frame, text="Motivul referatului:",
            font=("Arial", 10, "italic"), fg="#B22222"
        ).grid(row=row, column=0, columnspan=5, sticky="w", pady=(10, 2))

        row += 1
        self.reason_text = tk.Text(
            form_frame, height=8, font=("Arial", 10),
            wrap=tk.WORD, bg="#F5F5F5", relief="solid", bd=1
        )
        self.reason_text.grid(
            row=row, column=0, columnspan=5, sticky="nsew", pady=5)
        form_frame.grid_rowconfigure(row, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)

        # === BUTTONS ===
        btn_frame = tk.Frame(self, pady=10, padx=15)
        btn_frame.pack(fill=tk.X)

        self.delete_btn = tk.Button(
            btn_frame, text="🗑️ Șterge", font=("Arial", 10),
            command=self._delete_claim, state="disabled",
            bg="#DC3545", fg="white", padx=15, pady=5
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(
            btn_frame, text="❌ Anulare", font=("Arial", 10),
            command=self.destroy,
            bg="#6C757D", fg="white", padx=15, pady=5
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)

        self.save_btn = tk.Button(
            btn_frame, text="✅ Salvare", font=("Arial", 10),
            command=self._save_claim,
            bg="#28A745", fg="white", padx=15, pady=5
        )
        self.save_btn.pack(side=tk.RIGHT, padx=5)

    def _load_employees(self):
        """Carica i dipendenti nel combo (filtro per cost center o tutti)."""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = """
                SELECT h.EmployeeHireHistoryId,
                       e.EmployeeSurname, e.EmployeeName,
                       cc.CostCenterDesc,
                       CASE WHEN e.Sex = 'F' THEN 'Doamna' ELSE 'Domnul' END AS Sex_,
                       e.WorkEmail
                FROM Employee.dbo.EmployeeHireHistory h
                INNER JOIN Employee.dbo.Employees e ON e.EmployeeId = h.EmployeeId
                LEFT JOIN Employee.dbo.CostCenters cc ON cc.CostCenterId = h.CostCenterId
                WHERE h.DateEnd IS NULL
                ORDER BY e.EmployeeSurname
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            self._employees_data = []
            display_list = []
            for row in rows:
                self._employees_data.append({
                    'id': row.EmployeeHireHistoryId,
                    'surname': row.EmployeeSurname,
                    'name': row.EmployeeName,
                    'cdc': row.CostCenterDesc or '',
                    'sex': row.Sex_,
                    'email': row.WorkEmail
                })
                display_list.append(
                    f"{row.EmployeeSurname} {row.EmployeeName} - {row.CostCenterDesc or ''}"
                )
            self.employee_combo['values'] = display_list
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento dipendenti: {e}", exc_info=True)
            messagebox.showerror("Eroare", f"Nu s-au putut încărca angajații:\n{e}", parent=self)

    def _load_disciplinary_causes(self):
        """Carica le cause disciplinari dal DB."""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT L.[ArticoloLegaleId], [DescriptionTxt], [Articolo],
                       [Paragrafo], [Lettera], ld.ExplicationTxt
                FROM [Employee].[dbo].[LawArticles] L
                LEFT JOIN Employee.dbo.LawArticleDescriptions ld
                    ON L.ArticoloLegaleId = ld.ArticoloLegaleId
                WHERE [LegalType] = 'DISCIPLINA'
                ORDER BY DescriptionTxt
            """)
            rows = cursor.fetchall()

            self._causes_data = []
            display_list = []
            for row in rows:
                self._causes_data.append({
                    'id': row.ArticoloLegaleId,
                    'description': row.DescriptionTxt or '',
                    'article': row.Articolo or '',
                    'paragraph': row.Paragrafo or '',
                    'letter': row.Lettera or '',
                    'explication': row.ExplicationTxt or ''
                })
                display_list.append(row.DescriptionTxt or '')
            self.cause_combo['values'] = display_list
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento cause disciplinari: {e}", exc_info=True)
            messagebox.showerror("Eroare", f"Nu s-au putut încărca cauzele:\n{e}", parent=self)

    def _on_employee_selected(self, event=None):
        """Gestisce la selezione del dipendente."""
        idx = self.employee_combo.current()
        if idx < 0:
            return
        emp = self._employees_data[idx]
        self.selected_employee_id = emp['id']
        self.selected_employee_name = f"{emp['sex']} {emp['surname']} {emp['name']}"
        self.selected_employee_sex = emp['sex']
        self.selected_employee_cdc = emp['cdc']

        # Aggiorna testo area con preambolo
        current_text = self.reason_text.get("1.0", tk.END).strip()
        preambolo = (
            f"{emp['sex']} {emp['surname']} {emp['name']}, "
            f"aparținând la centrul de cost {emp['cdc']} "
            f"i se întocmește un referat pentru următoarele motive:"
        )
        if not current_text:
            self.reason_text.insert("1.0", preambolo + "\n\n")

        # Verifica storico
        count = self._count_prior_claims(emp['id'])
        if count > 0:
            self.history_btn.config(state="normal")
        else:
            self.history_btn.config(state="disabled")

    def _on_cause_selected(self, event=None):
        """Gestisce la selezione della causa disciplinare."""
        idx = self.cause_combo.current()
        if idx < 0:
            return
        cause = self._causes_data[idx]
        self.selected_cause_id = cause['id']
        self.selected_cause_text = cause['description']
        self.selected_cause_article = (
            f"Art. {cause['article']}  Alineat: {cause['paragraph']} - "
            f"{cause['description']} {cause['explication']}"
        )

        # Aggiungi causa al testo se non già presente
        current_text = self.reason_text.get("1.0", tk.END)
        if cause['description'] not in current_text:
            self.reason_text.insert(tk.END, f"\n{cause['description']}")

    def _validate_fields(self):
        """Valida i campi obbligatori."""
        errors = []

        # Data referat
        try:
            date_ref = datetime.strptime(self.date_referat_var.get(), '%d-%m-%Y').date()
            if date_ref > date.today():
                errors.append("Data referat nu poate fi în viitor!")
            elif (date.today() - date_ref).days > 2:
                errors.append("Nu se pot înregistra evenimente mai vechi de 3 zile!")
        except ValueError:
            errors.append("Data referat invalidă! Folosiți formatul DD-MM-YYYY.")

        # Employee
        if not self.selected_employee_id:
            errors.append("Selectați angajatul!")

        # Cause
        if not self.selected_cause_id:
            errors.append("Selectați cauza de abatere disciplinară!")

        # Date event
        date_event_str = self.date_event_var.get().strip()
        if not date_event_str:
            errors.append("Introduceți data evenimentului!")
        else:
            try:
                date_ev = datetime.strptime(date_event_str, '%d-%m-%Y').date()
                if date_ev > date.today():
                    errors.append("Data evenimentului nu poate fi în viitor!")
                elif (date.today() - date_ev).days > 2:
                    errors.append("Nu se pot înregistra evenimente mai vechi de 3 zile!")
            except ValueError:
                errors.append("Data evenimentului invalidă! Folosiți formatul DD-MM-YYYY.")

        # Reason
        reason = self.reason_text.get("1.0", tk.END).strip()
        if not reason or len(reason) < 10:
            errors.append("Descrieți motivul referatului (minim 10 caractere)!")

        if errors:
            messagebox.showwarning(
                "Validare", "\n".join(errors), parent=self)
            return False
        return True

    def _save_claim(self):
        """Salva la nota disciplinare nel DB."""
        if not self._validate_fields():
            return

        if not messagebox.askyesno(
                "Confirmare", "Doriți să salvați această notă disciplinară?",
                parent=self):
            return

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            date_ref = datetime.strptime(self.date_referat_var.get(), '%d-%m-%Y')
            date_event = datetime.strptime(self.date_event_var.get(), '%d-%m-%Y')
            time_event = self.time_event_var.get().strip() or '--'
            reason_text = self.reason_text.get("1.0", tk.END).strip()
            reason_text = reason_text.replace("'", "''")

            # 1. Chiama SP Employee.dbo.Registro per generare documento
            registry_type_id = 60  # Referat
            cursor.execute("""
                EXEC Employee.dbo.Registro
                    @RegistryTypeId = ?,
                    @anno = ?,
                    @DataDocumento = ?,
                    @iussedBy = ?,
                    @EmployeerId = ?,
                    @Accessid = NULL,
                    @DocumentTypeId = NULL
            """, (
                registry_type_id,
                date_ref.year,
                date_ref.strftime('%Y-%m-%d'),
                self.author_name,
                self.selected_employee_id
            ))

            # 2. Recupera RegistroId e DocName
            cursor.execute("""
                SELECT TOP 1 RegistroId, DocName
                FROM Employee.dbo.Registry
                WHERE RegistryTypeId = ?
                ORDER BY RegistroId DESC
            """, (registry_type_id,))
            reg_row = cursor.fetchone()
            if not reg_row:
                raise Exception("Impossibil de generat numărul documentului!")

            self.referat_id = reg_row.RegistroId
            self.doc_name = reg_row.DocName

            # 3. Insert into EmployeeDisciplinaryHistory
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT [RegistroId] FROM Employee.[dbo].[EmployeeDisciplinaryHistory]
                    WHERE [RegistroId] = ?
                )
                INSERT INTO Employee.[dbo].[EmployeeDisciplinaryHistory]
                    ([EmployeeHireHistoryId], [RegistroId], [DocSavedOn],
                     [ExplicationNote], [ArticoloLegaleId], [SefID],
                     [DataAvvenimento], [OraAvvenimento])
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.referat_id,
                self.selected_employee_id,
                self.referat_id,
                date_ref.strftime('%Y-%m-%d'),
                reason_text,
                self.selected_cause_id,
                getattr(self, 'last_authorized_user_id', None) or self.author_user_id,
                date_event.strftime('%Y-%m-%d'),
                time_event
            ))

            conn.commit()
            cursor.close()

            logger.info(
                f"Nota disciplinară salvată: RegistroId={self.referat_id}, "
                f"DocName={self.doc_name}, Employee={self.selected_employee_id}")

            # 4. Genera PDF
            pdf_path = self._generate_pdf(date_ref, date_event, time_event, reason_text)

            # 5. Invia email
            if pdf_path:
                self._send_notification_email(pdf_path)

            self.save_btn.config(state="disabled")
            self.delete_btn.config(state="normal")

            messagebox.showinfo(
                "Succes",
                f"Referatul a fost înregistrat cu succes.\n"
                f"Număr document: {self.doc_name}\n"
                f"Biroul Resurse Umane va completa procedura disciplinară.",
                parent=self
            )

        except Exception as e:
            logger.error(f"Errore salvataggio nota disciplinare: {e}", exc_info=True)
            messagebox.showerror(
                "Eroare", f"Eroare la salvarea referatului:\n{e}", parent=self)

    def _generate_pdf(self, date_ref, date_event, time_event, reason_text):
        """Genera il PDF del referat usando reportlab con font Arial per rumeno."""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.lib.styles import ParagraphStyle
            from reportlab.platypus import Paragraph, Frame

            # Registra font Arial per caratteri rumeni
            font_dir = r'C:\Windows\Fonts'
            if 'Arial' not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont('Arial', os.path.join(font_dir, 'arial.ttf')))
                pdfmetrics.registerFont(TTFont('Arial-Bold', os.path.join(font_dir, 'arialbd.ttf')))
                pdfmetrics.registerFont(TTFont('Arial-Italic', os.path.join(font_dir, 'ariali.ttf')))

            output_dir = r"C:\Temp"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            safe_doc_name = (self.doc_name or "referat").replace("/", "-").replace("\\", "-")
            filename = f"Referat_{safe_doc_name}.pdf"
            file_path = os.path.join(output_dir, filename)

            # Se bloccato, aggiungi timestamp
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'ab') as _t:
                        pass
                except PermissionError:
                    ts = datetime.now().strftime('%H%M%S')
                    filename = f"Referat_{safe_doc_name}_{ts}.pdf"
                    file_path = os.path.join(output_dir, filename)

            page_w, page_h = A4
            c = canvas.Canvas(file_path, pagesize=A4)

            # Logo
            logo_path = "Logo.png"
            if os.path.exists(logo_path):
                try:
                    c.drawImage(logo_path, 2 * cm, page_h - 3 * cm,
                                width=3 * cm, height=1.5 * cm,
                                preserveAspectRatio=True, mask='auto')
                except Exception:
                    pass

            # Titolo
            y = page_h - 4 * cm
            c.setFont("Arial-Bold", 18)
            c.drawCentredString(page_w / 2, y, "REFERAT")

            # Numero documento
            y -= 1 * cm
            c.setFont("Arial", 11)
            c.drawString(2 * cm, y,
                         f"Nr. {self.doc_name} / {date_ref.strftime('%d-%m-%Y')}")

            # Destinatario
            y -= 1.5 * cm
            c.setFont("Arial", 11)
            c.drawString(2 * cm, y,
                         f"În atenția Domnului ADMINISTRATOR Gianluca Testa,")

            # Corpo principale - usa Paragraph per word wrap
            y -= 1.5 * cm
            body_style = ParagraphStyle(
                'Body', fontName='Arial', fontSize=11,
                leading=16, firstLineIndent=1 * cm
            )

            emp_data = self._employees_data[self.employee_combo.current()]
            body_text = (
                f"Subsemnatul {self.author_name} la centrul de cost "
                f"{self.author_department}, în virtutea atribuțiunilor stabilite "
                f"prin fișa postului, doresc vă aduc la cunoștință următoarele:"
            )

            # Draw wrapped body text
            body_para = Paragraph(body_text, body_style)
            w_avail = page_w - 4 * cm
            bw, bh = body_para.wrap(w_avail, 900)
            body_para.drawOn(c, 2 * cm, y - bh)
            y -= bh + 0.5 * cm

            # Event description
            event_text = (
                f"În data de {date_event.strftime('%d-%m-%Y')}, "
                f"la orele {time_event} am constatat faptul că salariatul "
                f"{emp_data['surname']} {emp_data['name']} "
                f"a săvârșit următoarele abateri disciplinare constând în:"
            )
            event_para = Paragraph(event_text, body_style)
            ew, eh = event_para.wrap(w_avail, 900)
            event_para.drawOn(c, 2 * cm, y - eh)
            y -= eh + 0.5 * cm

            # Reason text (word wrapped)
            # Pulisci il testo dalle citazioni automatiche
            clean_reason = reason_text.replace("''", "'")
            reason_style = ParagraphStyle(
                'Reason', fontName='Arial', fontSize=11,
                leading=15
            )
            reason_para = Paragraph(clean_reason.replace('\n', '<br/>'), reason_style)
            rw, rh = reason_para.wrap(w_avail, 400)

            # Se supera la pagina, abbrevia
            if y - rh < 5 * cm:
                rh = y - 5 * cm
            reason_para.drawOn(c, 2 * cm, y - rh)
            y -= rh + 1.5 * cm

            # Articolo legale
            if self.selected_cause_article:
                cause_para = Paragraph(
                    f"<i>{self.selected_cause_article}</i>", reason_style)
                cw, ch = cause_para.wrap(w_avail, 200)
                cause_para.drawOn(c, 2 * cm, y - ch)
                y -= ch + 1.5 * cm

            # Footer: data e firma
            y = max(y, 4 * cm)
            c.setFont("Arial", 11)
            c.drawString(2 * cm, y,
                         f"Data GHIRODA, {date_ref.strftime('%d-%m-%Y')}")

            y -= 1 * cm
            c.drawString(2 * cm, y, "Semnătura,")

            y -= 0.8 * cm
            c.setFont("Arial-Bold", 11)
            c.drawString(2 * cm, y, self.author_name.upper())

            y -= 0.8 * cm
            c.setFont("Arial", 11)
            c.drawString(2 * cm, y, "______________________")

            c.save()
            logger.info(f"PDF Referat generat: {file_path}")

            # Apri il PDF
            try:
                os.startfile(file_path)
            except Exception:
                pass

            return file_path

        except Exception as e:
            logger.error(f"Errore generazione PDF referat: {e}", exc_info=True)
            messagebox.showwarning(
                "Atenție",
                f"Referatul a fost salvat, dar PDF-ul nu a putut fi generat:\n{e}",
                parent=self
            )
            return None

    def _send_notification_email(self, pdf_path):
        """Invia email di notifica con il PDF allegato."""
        try:
            from email_connector import EmailSender

            # Destinatari
            to_emails = []

            # 1. Email autore
            if self.author_email:
                to_emails.append(self.author_email)

            # 2. Email dipendente (se ha email)
            if self.selected_employee_id and self.employee_combo.current() >= 0:
                emp = self._employees_data[self.employee_combo.current()]
                if emp.get('email') and emp['email'].strip():
                    to_emails.append(emp['email'].strip())

            if not to_emails:
                logger.warning("Nessun destinatario email trovato per il referat")
                return

            # CC da settings
            cc_emails = []
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT ValueItem FROM Traceability_RS.dbo.Settings
                    WHERE Atribute = 'Sys_email_referat' AND DateOut IS NULL
                """)
                row = cursor.fetchone()
                if row and row.ValueItem:
                    cc_emails = [e.strip() for e in row.ValueItem.split(';')
                                 if e.strip()]
                cursor.close()
            except Exception as e:
                logger.warning(f"Errore lettura CC email referat: {e}")

            # Corpo email HTML in rumeno con logo
            subject = f"Referat disciplinar - {self.doc_name}"
            emp_data = self._employees_data[self.employee_combo.current()]

            body_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; font-size: 12px;">
                <img src="cid:company_logo" alt="Logo" style="width: 150px; margin-bottom: 10px;" /><br/>
                <h3 style="color: #B22222;">Notă disciplinară emisă</h3>
                <p>Bună ziua,</p>
                <p>Un nou referat disciplinar a fost emis:</p>
                <table style="border-collapse: collapse; margin: 10px 0;">
                    <tr><td style="padding: 5px; font-weight: bold;">Număr document:</td>
                        <td style="padding: 5px;">{self.doc_name}</td></tr>
                    <tr><td style="padding: 5px; font-weight: bold;">Angajat:</td>
                        <td style="padding: 5px;">{emp_data['surname']} {emp_data['name']}</td></tr>
                    <tr><td style="padding: 5px; font-weight: bold;">Emis de:</td>
                        <td style="padding: 5px;">{self.author_name}</td></tr>
                    <tr><td style="padding: 5px; font-weight: bold;">Data:</td>
                        <td style="padding: 5px;">{self.date_referat_var.get()}</td></tr>
                </table>
                <p>Vă rugăm să deschideți fișierul atașat pentru detalii.</p>
                <p style="color: #888; font-size: 10px;">
                    Document generat automat de sistemul TraceabilityRS.</p>
            </body>
            </html>
            """

            sender = EmailSender()
            # Invio a tutti i destinatari (primo come TO, gli altri in CC)
            primary_to = to_emails[0]
            all_cc = cc_emails + to_emails[1:]

            attachments = [pdf_path]

            # Logo inline
            logo_path = "Logo.png"
            if os.path.exists(logo_path):
                attachments.append(('inline', logo_path, 'company_logo'))

            sender.send_email(
                to_email=primary_to,
                subject=subject,
                body=body_html,
                is_html=True,
                attachments=attachments,
                cc_emails=all_cc if all_cc else None
            )

            logger.info(f"Email referat inviata a {primary_to}, CC: {all_cc}")

        except Exception as e:
            logger.error(f"Errore invio email referat: {e}", exc_info=True)
            messagebox.showwarning(
                "Atenție",
                f"Referatul a fost salvat, dar email-ul nu a putut fi trimis:\n{e}",
                parent=self
            )

    def _delete_claim(self):
        """Cancella (soft-delete) la nota disciplinare."""
        if not self.referat_id:
            return

        if not messagebox.askyesno(
                "Confirmare",
                "Doriți să ștergeți această notă disciplinară?",
                parent=self):
            return

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Employee.dbo.Registry SET IsDeleted = 1 WHERE RegistroId = ?",
                (self.referat_id,))
            conn.commit()
            cursor.close()

            messagebox.showinfo(
                "Succes", "Nota disciplinară a fost ștearsă.", parent=self)
            self.save_btn.config(state="normal")
            self.delete_btn.config(state="disabled")
            self.referat_id = None
            self.doc_name = None

        except Exception as e:
            logger.error(f"Errore cancellazione referat: {e}", exc_info=True)
            messagebox.showerror(
                "Eroare", f"Eroare la ștergerea referatului:\n{e}", parent=self)

    def _count_prior_claims(self, employee_hire_history_id):
        """Conta le precedenti note disciplinari per un dipendente."""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(DISTINCT d.RegistroId)
                FROM Employee.[dbo].[EmployeeDisciplinaryHistory] d
                INNER JOIN Employee.dbo.Registry r ON r.RegistroId = d.RegistroId
                WHERE d.EmployeeHireHistoryId = ?
                  AND ISNULL(r.IsDeleted, 0) = 0
            """, (employee_hire_history_id,))
            row = cursor.fetchone()
            cursor.close()
            return row[0] if row else 0
        except Exception as e:
            logger.warning(f"Errore conteggio referati: {e}")
            return 0

    def _show_history(self):
        """Mostra lo storico delle note disciplinari per il dipendente selezionato."""
        if not self.selected_employee_id:
            return

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT
                    r.DocName,
                    d.DataAvvenimento,
                    d.ExplicationNote,
                    r.RegistroId
                FROM Employee.[dbo].[EmployeeDisciplinaryHistory] d
                INNER JOIN Employee.dbo.Registry r ON r.RegistroId = d.RegistroId
                WHERE d.EmployeeHireHistoryId = ?
                  AND ISNULL(r.IsDeleted, 0) = 0
                ORDER BY d.DataAvvenimento DESC
            """, (self.selected_employee_id,))
            rows = cursor.fetchall()
            cursor.close()

            if not rows:
                messagebox.showinfo(
                    "Istoric", "Nu există referate anterioare.", parent=self)
                return

            # Costruisci il messaggio
            emp_data = self._employees_data[self.employee_combo.current()]
            msg = f"{emp_data['surname']} {emp_data['name']} are {len(rows)} referat(e):\n\n"
            for i, row in enumerate(rows, 1):
                dt = row.DataAvvenimento
                date_str = dt.strftime('%d-%m-%Y') if dt else 'N/A'
                note = (row.ExplicationNote or '')[:80]
                msg += f"{i}) {row.DocName} - {date_str}\n   {note}\n\n"

            messagebox.showinfo("Istoric referate", msg, parent=self)

        except Exception as e:
            logger.error(f"Errore visualizzazione storico: {e}", exc_info=True)
            messagebox.showerror(
                "Eroare", f"Eroare la încărcarea istoricului:\n{e}", parent=self)


def open_disciplinary_window(parent, db_handler, lang_manager, author_name, author_user_id=None):
    """Entry point per aprire la finestra note disciplinari."""
    DisciplinaryClaimWindow(parent, db_handler, lang_manager, author_name, author_user_id)
