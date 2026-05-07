# -*- coding: utf-8 -*-
"""
Shipping PDF — Carica Excel spedizioni, genera PDF DDT e invia email.

Flusso:
1. Utente seleziona destinatario (Sites 89/90)
2. Carica file Excel con layout standard spedizioni
3. Gestisce indirizzi email (salvati per destinatario)
4. Genera PDF professionale con lista DDT
5. Invia email con PDF allegato
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import logging
import os
import json

logger = logging.getLogger("TraceabilityRS")

# Percorso file per salvare indirizzi email per destinatario
EMAIL_CACHE_FILE = os.path.join(os.path.dirname(__file__), '.shipping_email_cache.json')

# Color palette (coerente con guest_report_window)
BG_MAIN = "#F0F4F8"
BG_HEADER = "#1F4E79"
BG_CARD = "#FFFFFF"
FG_TITLE = "#FFFFFF"
FG_SUBTITLE = "#B8D4E8"
FG_LABEL = "#2C3E50"
ACCENT = "#2E75B6"
BORDER_COLOR = "#D5DFE9"
BTN_PRIMARY_BG = "#2E75B6"
BTN_PRIMARY_HOVER = "#1A5F9E"
BTN_SUCCESS_BG = "#217346"
BTN_SUCCESS_HOVER = "#1B5E38"
BTN_CLOSE_BG = "#5D6D7E"
BTN_CLOSE_HOVER = "#4A5A6A"


def _load_email_cache() -> dict:
    try:
        if os.path.isfile(EMAIL_CACHE_FILE):
            with open(EMAIL_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_email_cache(cache: dict):
    try:
        with open(EMAIL_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.warning(f"Shipping: errore salvataggio cache email: {e}")


class ShippingPdfWindow(tk.Toplevel):
    """Form per generare PDF spedizioni da file Excel e invio email."""

    def __init__(self, parent, db, lang, logged_user_name: str = ""):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.logged_user = logged_user_name
        self.title(self.lang.get('shipping_pdf_title', 'Shipping PDF — DDT Generator'))
        self.geometry("680x580")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(bg=BG_MAIN)

        self._shipper = {}
        self._recipients_list = []
        self._excel_path = None
        self._excel_data = []
        self._email_cache = _load_email_cache()

        self._load_db_data()
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    # ── DB Data ──
    def _load_db_data(self):
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT SiteName, SiteAddress, SiteVat, SiteCountry
                FROM traceability_rs.dbo.Sites WHERE IDSite = 2
            """)
            r = cur.fetchone()
            if r:
                self._shipper = {
                    'name': r.SiteName or '', 'address': r.SiteAddress or '',
                    'vat': r.SiteVat or '', 'country': r.SiteCountry or ''
                }
            cur.execute("""
                SELECT IDSite, SiteName, SiteAddress, SiteVat, SiteCountry
                FROM traceability_rs.dbo.Sites WHERE IDSite IN (89, 90)
                ORDER BY SiteName
            """)
            for r in cur.fetchall():
                self._recipients_list.append({
                    'id': r.IDSite, 'name': r.SiteName or '',
                    'address': r.SiteAddress or '', 'vat': r.SiteVat or '',
                    'country': r.SiteCountry or ''
                })
            cur.close()
        except Exception as e:
            logger.error(f"Shipping: errore caricamento dati DB: {e}")

    # ── UI ──
    def _make_button(self, parent, text, bg, hover_bg, command, icon=""):
        lbl = f"{icon}  {text}" if icon else text
        btn = tk.Button(parent, text=lbl, font=("Segoe UI Semibold", 10),
                        fg="#FFF", bg=bg, activebackground=hover_bg,
                        activeforeground="#FFF", relief="flat", cursor="hand2",
                        bd=0, padx=14, pady=6, command=command)
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        return btn

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=BG_HEADER, height=64)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text=f"📦  {self.lang.get('shipping_pdf_title', 'Shipping PDF — DDT Generator')}",
                 font=("Segoe UI Semibold", 15), fg=FG_TITLE,
                 bg=BG_HEADER).pack(side="left", padx=20, pady=12)

        # Card
        card = tk.Frame(self, bg=BG_CARD, highlightbackground=BORDER_COLOR,
                        highlightthickness=1, padx=18, pady=14)
        card.pack(fill="both", expand=True, padx=16, pady=(12, 8))

        lbl_kw = dict(font=("Segoe UI", 10), fg=FG_LABEL, bg=BG_CARD)
        row = 0

        # Shipper (read-only)
        tk.Label(card, text=self.lang.get('shipping_shipper', 'SHIPPER'),
                 font=("Segoe UI Semibold", 9),
                 fg=ACCENT, bg=BG_CARD).grid(row=row, column=0, columnspan=3,
                                              sticky="w", pady=(0, 4))
        row += 1
        ship_txt = f"{self._shipper.get('name','')} — {self._shipper.get('address','')} — VAT: {self._shipper.get('vat','')}"
        tk.Label(card, text=ship_txt, font=("Segoe UI", 9, "italic"),
                 fg="#555", bg=BG_CARD, wraplength=600, justify="left"
                 ).grid(row=row, column=0, columnspan=3, sticky="w", pady=(0, 8))
        row += 1

        tk.Frame(card, bg=ACCENT, height=2).grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        row += 1

        # Recipient combo
        tk.Label(card, text=self.lang.get('shipping_recipient', 'Recipient:'),
                 **lbl_kw).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=5)
        self.recipient_var = tk.StringVar()
        self.recipient_combo = ttk.Combobox(
            card, textvariable=self.recipient_var, state="readonly",
            width=50, font=("Segoe UI", 10),
            values=[r['name'] for r in self._recipients_list])
        self.recipient_combo.grid(row=row, column=1, columnspan=2,
                                   sticky="ew", pady=5)
        if self._recipients_list:
            self.recipient_combo.current(0)
        self.recipient_combo.bind("<<ComboboxSelected>>", self._on_recipient_changed)
        row += 1

        # Excel file
        tk.Label(card, text=self.lang.get('shipping_excel_file', 'Excel File:'),
                 **lbl_kw).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=5)
        self.file_var = tk.StringVar(value=self.lang.get('shipping_no_file', 'No file selected'))
        tk.Label(card, textvariable=self.file_var, font=("Segoe UI", 9),
                 fg="#555", bg=BG_CARD, anchor="w", width=45
                 ).grid(row=row, column=1, sticky="w", pady=5)
        self._make_button(card, self.lang.get('shipping_browse', 'Browse...'),
                          ACCENT, BTN_PRIMARY_HOVER,
                          self._browse_file).grid(row=row, column=2,
                                                   padx=(8, 0), pady=5)
        row += 1

        # File info label
        self.file_info_var = tk.StringVar()
        tk.Label(card, textvariable=self.file_info_var, font=("Segoe UI", 9),
                 fg=BTN_SUCCESS_BG, bg=BG_CARD).grid(
            row=row, column=0, columnspan=3, sticky="w", pady=(0, 6))
        row += 1

        # Email addresses
        tk.Label(card, text=self.lang.get('shipping_email_to', 'Email To:'),
                 **lbl_kw).grid(row=row, column=0, sticky="nw", padx=(0, 8), pady=5)
        self.email_text = tk.Text(card, height=3, width=50,
                                   font=("Segoe UI", 10), wrap="word",
                                   bd=1, relief="solid")
        self.email_text.grid(row=row, column=1, columnspan=2,
                              sticky="ew", pady=5)
        row += 1

        tk.Label(card, text=self.lang.get('shipping_email_hint',
                 'One email per line or separated by ;'),
                 font=("Segoe UI", 8), fg="#999", bg=BG_CARD
                 ).grid(row=row, column=1, columnspan=2, sticky="w")
        row += 1

        card.columnconfigure(1, weight=1)

        # Load cached emails for first recipient
        self._on_recipient_changed()

        # Buttons
        btn_bar = tk.Frame(self, bg=BG_MAIN)
        btn_bar.pack(fill="x", padx=16, pady=(0, 12))

        self._make_button(btn_bar,
                          self.lang.get('shipping_btn_generate_send', 'Generate PDF & Send Email'),
                          BTN_SUCCESS_BG, BTN_SUCCESS_HOVER,
                          self._generate_and_send, "📄").pack(
            side="left", padx=(0, 8))
        self._make_button(btn_bar,
                          self.lang.get('shipping_btn_generate_only', 'Generate PDF Only'),
                          BTN_PRIMARY_BG, BTN_PRIMARY_HOVER,
                          self._generate_pdf_only, "📋").pack(
            side="left", padx=(0, 8))
        self._make_button(btn_bar,
                          self.lang.get('shipping_btn_close', 'Close'),
                          BTN_CLOSE_BG, BTN_CLOSE_HOVER,
                          self.destroy).pack(side="right")

    # ── Events ──
    def _on_recipient_changed(self, event=None):
        name = self.recipient_var.get()
        cached = self._email_cache.get(name, '')
        self.email_text.delete("1.0", "end")
        if cached:
            self.email_text.insert("1.0", cached)

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title=self.lang.get('shipping_select_excel', 'Select Shipping Excel'),
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")])
        if not path:
            return
        self._excel_path = path
        self.file_var.set(os.path.basename(path))
        self._parse_excel()

    def _parse_excel(self):
        try:
            import openpyxl
            wb = openpyxl.load_workbook(self._excel_path, read_only=True,
                                         data_only=True)
            ws = wb.active
            self._excel_data = []
            for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
                if not row or not row[0]:
                    continue
                self._excel_data.append({
                    'product': str(row[0] or ''),       # A
                    'date': row[1],                      # B
                    'reference': str(row[4] or ''),      # E (Sales Order)
                    'doc_number': str(row[5] or ''),     # F (Packing Slip)
                    'quantity': abs(float(row[6] or 0)),  # G (abs)
                    'prod_order': str(row[17] or ''),    # R (Batch/Prod Order)
                })
            wb.close()
            total_qty = sum(d['quantity'] for d in self._excel_data)
            self.file_info_var.set(
                f"✅ {len(self._excel_data)} {self.lang.get('shipping_rows_loaded', 'rows loaded')} — "
                f"{self.lang.get('shipping_total_qty', 'Total qty')}: {total_qty:,.0f} pcs")
            logger.info(f"Shipping: Excel parsed, {len(self._excel_data)} rows")
        except Exception as e:
            logger.error(f"Shipping: errore parsing Excel: {e}", exc_info=True)
            messagebox.showerror("Error", f"Error reading Excel:\n{e}")
            self._excel_data = []
            self.file_info_var.set("❌ Error reading file")

    def _get_emails(self) -> list:
        raw = self.email_text.get("1.0", "end").strip()
        emails = []
        for part in raw.replace(';', '\n').split('\n'):
            e = part.strip()
            if e and '@' in e:
                emails.append(e)
        return list(dict.fromkeys(emails))

    def _save_emails_for_recipient(self):
        name = self.recipient_var.get()
        raw = self.email_text.get("1.0", "end").strip()
        self._email_cache[name] = raw
        _save_email_cache(self._email_cache)

    def _get_ship_date_str(self) -> str:
        if self._excel_data and self._excel_data[0].get('date'):
            d = self._excel_data[0]['date']
            if hasattr(d, 'strftime'):
                return d.strftime('%d %B %Y')
            return str(d)
        return datetime.now().strftime('%d %B %Y')

    def _get_recipient_info(self) -> dict:
        name = self.recipient_var.get()
        for r in self._recipients_list:
            if r['name'] == name:
                return r
        return {}

    # ── PDF Generation ──
    def _generate_pdf(self) -> str:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor, white
        from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                         Paragraph, Spacer, Image)
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        font_name, font_bold = "Helvetica", "Helvetica-Bold"
        arial = os.path.join(os.environ.get("WINDIR", r"C:\Windows"),
                             "Fonts", "arial.ttf")
        arialbd = os.path.join(os.environ.get("WINDIR", r"C:\Windows"),
                               "Fonts", "arialbd.ttf")
        if os.path.isfile(arial) and os.path.isfile(arialbd):
            try:
                pdfmetrics.registerFont(TTFont("ArialPDF", arial))
                pdfmetrics.registerFont(TTFont("ArialPDF-Bold", arialbd))
                font_name, font_bold = "ArialPDF", "ArialPDF-Bold"
            except Exception:
                pass

        temp_dir = r"C:\Temp"
        os.makedirs(temp_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = os.path.join(temp_dir, f"Shipping_DDT_{ts}.pdf")

        doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                                leftMargin=1.5*cm, rightMargin=1.5*cm,
                                topMargin=1.5*cm, bottomMargin=1.5*cm)

        DARK_BLUE = HexColor("#1F4E79")
        MED_BLUE = HexColor("#2E75B6")
        ALT_ROW = HexColor("#F2F7FB")

        styles = getSampleStyleSheet()
        title_s = ParagraphStyle("T", parent=styles["Title"],
                                  fontName=font_bold, fontSize=16,
                                  textColor=DARK_BLUE, spaceAfter=4)
        sub_s = ParagraphStyle("S", parent=styles["Normal"],
                                fontName=font_name, fontSize=10,
                                textColor=HexColor("#333"), spaceAfter=8)
        cell_s = ParagraphStyle("C", parent=styles["Normal"],
                                 fontName=font_name, fontSize=9, leading=11)
        cell_b = ParagraphStyle("CB", parent=cell_s, fontName=font_bold)

        elements = []
        logo_path = os.path.join(os.path.dirname(__file__), "Logo.png")
        if os.path.isfile(logo_path):
            try:
                elements.append(Image(logo_path, width=4*cm, height=1.5*cm))
                elements.append(Spacer(1, 6))
            except Exception:
                pass

        ship_date = self._get_ship_date_str()
        total_qty = sum(d['quantity'] for d in self._excel_data)
        n_ddt = len(self._excel_data)
        recip = self._get_recipient_info()

        elements.append(Paragraph(
            f"Shipment List (DDT) — {ship_date}", title_s))
        elements.append(Paragraph(
            f"This list contains <b>{n_ddt}</b> DDTs for a total quantity "
            f"of <b>{total_qty:,.0f}</b> pieces.", sub_s))

        # Shipper / Recipient info
        info_data = [
            [Paragraph("<b>Shipper:</b>", cell_b),
             Paragraph(f"{self._shipper.get('name','')} — "
                       f"{self._shipper.get('address','')} — "
                       f"VAT: {self._shipper.get('vat','')}", cell_s)],
            [Paragraph("<b>Recipient:</b>", cell_b),
             Paragraph(f"{recip.get('name','')} — "
                       f"{recip.get('address','')} — "
                       f"VAT: {recip.get('vat','')}", cell_s)],
        ]
        info_tbl = Table(info_data, colWidths=[2.5*cm, 15*cm])
        info_tbl.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(info_tbl)
        elements.append(Spacer(1, 12))

        # Table
        headers = ["Document No.", "Sales Order", "Production Order",
                    "Product", "Quantity"]
        header_row = [Paragraph(h, cell_b) for h in headers]
        table_data = [header_row]
        for d in self._excel_data:
            table_data.append([
                Paragraph(d['doc_number'], cell_s),
                Paragraph(d['reference'], cell_s),
                Paragraph(d['prod_order'], cell_s),
                Paragraph(d['product'], cell_s),
                Paragraph(f"{d['quantity']:,.0f}", cell_s),
            ])

        col_w = [3.2*cm, 3.2*cm, 3.2*cm, 5.5*cm, 2.5*cm]
        tbl = Table(table_data, colWidths=col_w, repeatRows=1)
        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), MED_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("ALIGN", (4, 0), (4, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#B4C6E7")),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]
        for i in range(1, len(table_data)):
            if i % 2 == 0:
                style_cmds.append(("BACKGROUND", (0, i), (-1, i), ALT_ROW))
        tbl.setStyle(TableStyle(style_cmds))
        elements.append(tbl)

        # Total row
        elements.append(Spacer(1, 8))
        total_s = ParagraphStyle("Tot", parent=styles["Normal"],
                                  fontName=font_bold, fontSize=10,
                                  textColor=DARK_BLUE, alignment=TA_RIGHT)
        elements.append(Paragraph(
            f"Total: {n_ddt} DDTs — {total_qty:,.0f} pcs", total_s))

        # Footer
        footer_s = ParagraphStyle("F", parent=styles["Normal"],
                                   fontName=font_name, fontSize=7,
                                   textColor=HexColor("#888"),
                                   alignment=TA_CENTER, spaceBefore=20)
        try:
            import main
            ver = getattr(main, 'APP_VERSION', '')
        except Exception:
            ver = ''
        elements.append(Paragraph(
            f"Generated by TraceabilityRS — Vandewiele Romania"
            f"{f' — v{ver}' if ver else ''}", footer_s))

        doc.build(elements)
        logger.info(f"Shipping: PDF generato: {pdf_path}")
        return pdf_path

    # ── Email ──
    def _send_email(self, pdf_path: str):
        from email_connector import EmailSender

        emails = self._get_emails()
        if not emails:
            messagebox.showwarning("Warning", "No email addresses specified.")
            return False

        self._save_emails_for_recipient()
        ship_date = self._get_ship_date_str()
        recip = self._get_recipient_info()
        n_ddt = len(self._excel_data)
        total_qty = sum(d['quantity'] for d in self._excel_data)

        logo_path = os.path.join(os.path.dirname(__file__), "Logo.png")

        body = f"""
        <html><body style="font-family: Arial, sans-serif; font-size: 13px; color: #333;">
            <img src="cid:company_logo" alt="Vandewiele"
                 style="width: 150px; margin-bottom: 10px;" /><br/>
            <h2 style="color: #1F4E79;">
                📦 Shipment Notification — {ship_date}</h2>
            <p>Dear colleagues,</p>
            <p>Please find attached the list of <strong>{n_ddt} DDTs</strong>
               shipped on <strong>{ship_date}</strong> to
               <strong>{recip.get('name','')}</strong>,
               for a total of <strong>{total_qty:,.0f} pieces</strong>.</p>
            <div style="background-color: #E8F5E9; border-left: 4px solid #2E7D32;
                        padding: 12px; margin: 15px 0;">
                <p style="font-weight: bold; color: #2E7D32;">
                    📎 Attachment: Shipment List (DDT) — PDF</p>
                <p>The attached PDF contains the complete list of documents
                   with sales orders, production orders, and quantities.</p>
            </div>
            <p>Best regards,<br/><em>TraceabilityRS — Vandewiele Romania</em></p>
            <hr style="border: 1px solid #ddd;"/>
            <p style="color: #888; font-size: 10px;">
                This email was automatically generated by TraceabilityRS.</p>
        </body></html>
        """

        try:
            sender = EmailSender()
            attachments = [pdf_path]
            if os.path.isfile(logo_path):
                attachments.append(('inline', logo_path, 'company_logo'))

            # CC: logged user email
            cc = []
            if self.logged_user:
                try:
                    cur = self.db.conn.cursor()
                    cur.execute("""
                        SELECT TOP 1 a.WorkEmail
                        FROM Employee.dbo.EmployeeAddress a
                        INNER JOIN Employee.dbo.Employees e
                            ON e.EmployeeId = a.EmployeeId
                        WHERE (e.EmployeeSurname + ' ' + e.EmployeeName) = ?
                          AND a.DateOut IS NULL AND a.WorkEmail IS NOT NULL
                    """, (self.logged_user,))
                    r = cur.fetchone()
                    if r and r.WorkEmail:
                        cc.append(r.WorkEmail.strip())
                    cur.close()
                except Exception:
                    pass

            sender.send_email(
                to_email=emails[0],
                subject=f"📦 Shipment List (DDT) — {ship_date} — "
                        f"{recip.get('name','')} — {n_ddt} DDTs",
                body=body, is_html=True,
                attachments=attachments,
                cc_emails=(emails[1:] + cc) if (emails[1:] + cc) else None
            )
            logger.info(f"Shipping: email inviata a {emails}, CC={cc}")
            return True
        except Exception as e:
            logger.error(f"Shipping: errore invio email: {e}", exc_info=True)
            messagebox.showerror("Error", f"Error sending email:\n{e}")
            return False

    # ── Actions ──
    def _validate(self) -> bool:
        if not self._excel_data:
            messagebox.showwarning("Warning",
                self.lang.get('shipping_error_no_file', 'Please load an Excel file first.'))
            return False
        if not self.recipient_var.get():
            messagebox.showwarning("Warning",
                self.lang.get('shipping_error_no_recipient', 'Please select a recipient.'))
            return False
        return True

    def _generate_pdf_only(self):
        if not self._validate():
            return
        try:
            pdf_path = self._generate_pdf()
            os.startfile(pdf_path)
            messagebox.showinfo("Success",
                f"{self.lang.get('shipping_success_pdf', 'PDF generated:')}\n{pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating PDF:\n{e}")

    def _generate_and_send(self):
        if not self._validate():
            return
        emails = self._get_emails()
        if not emails:
            messagebox.showwarning("Warning",
                self.lang.get('shipping_error_no_email', 'Please enter email addresses.'))
            return
        try:
            pdf_path = self._generate_pdf()
            if self._send_email(pdf_path):
                self._save_emails_for_recipient()
                messagebox.showinfo("Success",
                    f"{self.lang.get('shipping_success_send', 'PDF generated and email sent!')}\n{pdf_path}")
                os.startfile(pdf_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error:\n{e}")
