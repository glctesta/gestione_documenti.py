"""
NPI Overdue Tasks Window — Visualizza tutti i task NPI scaduti con filtri,
ordinamento, invio solleciti e generazione Excel.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from collections import defaultdict
import logging
import os

logger = logging.getLogger(__name__)


class NpiOverdueTasksWindow(tk.Toplevel):
    """Finestra per la visualizzazione e gestione dei task NPI scaduti."""

    COLUMNS = (
        'project_name', 'customer', 'product_code', 'category',
        'task_name', 'owner_name', 'due_date', 'days_late', 'status'
    )
    HEADER_KEYS = {
        'project_name': ('npi_overdue_col_project', 'NPI Project'),
        'customer': ('npi_overdue_col_customer', 'Customer'),
        'product_code': ('npi_overdue_col_product', 'Product'),
        'category': ('npi_overdue_col_family', 'Family'),
        'task_name': ('npi_overdue_col_task', 'Task'),
        'owner_name': ('npi_overdue_col_owner', 'Owner'),
        'due_date': ('npi_overdue_col_due_date', 'Due Date'),
        'days_late': ('npi_overdue_col_days_late', 'Days Late'),
        'status': ('npi_overdue_col_status', 'Status')
    }
    COL_WIDTHS = {
        'project_name': 180, 'customer': 130, 'product_code': 110,
        'category': 100, 'task_name': 200, 'owner_name': 130,
        'due_date': 90, 'days_late': 70, 'status': 80
    }

    def __init__(self, master, npi_manager, lang):
        super().__init__(master)
        self.npi_manager = npi_manager
        self.lang = lang

        # Resolve translated headers
        self.HEADERS = {
            col: self.lang.get(key, default)
            for col, (key, default) in self.HEADER_KEYS.items()
        }

        self.title(self.lang.get('npi_overdue_title', 'NPI — Task Scaduti'))
        self.geometry('1350x680')
        self.transient(master)
        self.grab_set()

        self._all_data = []          # dati grezzi
        self._filtered_data = []     # dati filtrati
        self._sort_col = 'days_late'
        self._sort_reverse = True

        # Testo "Tutti" per i filtri (tradotto)
        self._all_label = self.lang.get('npi_overdue_filter_all', 'Tutti')

        self._build_ui()
        self._load_data()

    # ────────────────────────── UI ──────────────────────────
    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        # ── Filtri ──
        filter_frame = ttk.LabelFrame(
            main,
            text=self.lang.get('npi_overdue_filters', 'Filtri'),
            padding=6
        )
        filter_frame.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(filter_frame,
                  text=self.lang.get('npi_overdue_filter_customer', 'Cliente:')
                  ).grid(row=0, column=0, padx=4, sticky='w')
        self.filter_customer_var = tk.StringVar(value=self._all_label)
        self.filter_customer = ttk.Combobox(filter_frame, textvariable=self.filter_customer_var,
                                             state='readonly', width=20)
        self.filter_customer.grid(row=0, column=1, padx=4)
        self.filter_customer.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())

        ttk.Label(filter_frame,
                  text=self.lang.get('npi_overdue_filter_owner', 'Responsabile:')
                  ).grid(row=0, column=2, padx=4, sticky='w')
        self.filter_owner_var = tk.StringVar(value=self._all_label)
        self.filter_owner = ttk.Combobox(filter_frame, textvariable=self.filter_owner_var,
                                          state='readonly', width=20)
        self.filter_owner.grid(row=0, column=3, padx=4)
        self.filter_owner.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())

        ttk.Label(filter_frame,
                  text=self.lang.get('npi_overdue_filter_product', 'Prodotto:')
                  ).grid(row=0, column=4, padx=4, sticky='w')
        self.filter_product_var = tk.StringVar(value=self._all_label)
        self.filter_product = ttk.Combobox(filter_frame, textvariable=self.filter_product_var,
                                            state='readonly', width=18)
        self.filter_product.grid(row=0, column=5, padx=4)
        self.filter_product.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())

        ttk.Label(filter_frame,
                  text=self.lang.get('npi_overdue_filter_task', 'Task:')
                  ).grid(row=0, column=6, padx=4, sticky='w')
        self.filter_task_var = tk.StringVar(value=self._all_label)
        self.filter_task = ttk.Combobox(filter_frame, textvariable=self.filter_task_var,
                                         state='readonly', width=20)
        self.filter_task.grid(row=0, column=7, padx=4)
        self.filter_task.bind('<<ComboboxSelected>>', lambda e: self._apply_filters())

        ttk.Button(filter_frame,
                   text=self.lang.get('npi_overdue_btn_reset', 'Reset'),
                   command=self._reset_filters
                   ).grid(row=0, column=8, padx=(10, 4))

        # ── Treeview ──
        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            tree_frame, columns=self.COLUMNS, show='headings',
            selectmode='extended', height=22
        )
        for col in self.COLUMNS:
            self.tree.heading(col, text=self.HEADERS[col],
                              command=lambda c=col: self._on_sort(c))
            anchor = tk.CENTER if col in ('days_late', 'due_date', 'status') else tk.W
            self.tree.column(col, width=self.COL_WIDTHS.get(col, 100), anchor=anchor)

        # Tags
        self.tree.tag_configure('critical', foreground='#C0392B', font=('Segoe UI', 9, 'bold'))
        self.tree.tag_configure('warning', foreground='#E67E22')
        self.tree.tag_configure('normal', foreground='#2C3E50')

        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # ── Bottoni ──
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=(8, 0))

        ttk.Button(btn_frame,
                   text=self.lang.get('npi_overdue_btn_remind_all', '📧 Sollecita tutti'),
                   command=self._send_reminders_all).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame,
                   text=self.lang.get('npi_overdue_btn_remind_selected', '📧 Sollecita selezionati'),
                   command=self._send_reminders_selected).pack(side=tk.LEFT, padx=4)
        ttk.Separator(btn_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6)
        ttk.Button(btn_frame,
                   text=self.lang.get('npi_overdue_btn_export', '📊 Esporta Excel'),
                   command=self._export_excel).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame,
                   text=self.lang.get('btn_refresh', '🔄 Aggiorna'),
                   command=self._load_data).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame,
                   text=self.lang.get('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side=tk.RIGHT, padx=4)

        # ── Status bar ──
        self.status_var = tk.StringVar(value='')
        ttk.Label(main, textvariable=self.status_var, relief='sunken',
                  anchor='w').pack(fill=tk.X, pady=(6, 0))

    # ────────────────────────── Dati ──────────────────────────
    def _load_data(self):
        """Carica tutti i task scaduti dal manager."""
        self.config(cursor='watch')
        self.update_idletasks()
        try:
            self._all_data = self.npi_manager.get_all_overdue_tasks()
            self._populate_filter_combos()
            self._apply_filters()
        except Exception as e:
            logger.error(f"Errore caricamento task scaduti: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('npi_overdue_load_error', 'Impossibile caricare i task')}:\n{e}",
                parent=self
            )
        finally:
            self.config(cursor='')

    def _populate_filter_combos(self):
        """Popola i combo filtro con i valori distinti."""
        customers = sorted(set(d['customer'] for d in self._all_data if d['customer']))
        owners = sorted(set(d['owner_name'] for d in self._all_data if d['owner_name']))
        products = sorted(set(d['product_code'] for d in self._all_data if d['product_code']))
        tasks = sorted(set(d['task_name'] for d in self._all_data if d['task_name']))

        self.filter_customer['values'] = [self._all_label] + customers
        self.filter_owner['values'] = [self._all_label] + owners
        self.filter_product['values'] = [self._all_label] + products
        self.filter_task['values'] = [self._all_label] + tasks

    def _apply_filters(self):
        """Filtra e visualizza."""
        cust = self.filter_customer_var.get()
        own = self.filter_owner_var.get()
        prod = self.filter_product_var.get()
        task = self.filter_task_var.get()

        data = self._all_data
        if cust != self._all_label:
            data = [d for d in data if d['customer'] == cust]
        if own != self._all_label:
            data = [d for d in data if d['owner_name'] == own]
        if prod != self._all_label:
            data = [d for d in data if d['product_code'] == prod]
        if task != self._all_label:
            data = [d for d in data if d['task_name'] == task]

        self._filtered_data = data
        self._sort_data()
        self._refresh_tree()

    def _reset_filters(self):
        self.filter_customer_var.set(self._all_label)
        self.filter_owner_var.set(self._all_label)
        self.filter_product_var.set(self._all_label)
        self.filter_task_var.set(self._all_label)
        self._apply_filters()

    # ────────────────────────── Ordinamento ──────────────────────────
    def _on_sort(self, col):
        if self._sort_col == col:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_col = col
            self._sort_reverse = False
        self._sort_data()
        self._refresh_tree()

    def _sort_data(self):
        col = self._sort_col

        def sort_key(item):
            val = item.get(col, '')
            if col == 'days_late':
                return val if isinstance(val, int) else 0
            if col == 'due_date':
                return val or datetime.min
            return str(val).lower()

        self._filtered_data.sort(key=sort_key, reverse=self._sort_reverse)

    # ────────────────────────── Render ──────────────────────────
    def _refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for d in self._filtered_data:
            due_str = d['due_date'].strftime('%Y-%m-%d') if d['due_date'] else ''
            tag = 'critical' if d['days_late'] > 14 else ('warning' if d['days_late'] > 7 else 'normal')
            self.tree.insert('', tk.END, values=(
                d['project_name'], d['customer'], d['product_code'],
                d['category'], d['task_name'], d['owner_name'],
                due_str, d['days_late'], d['status']
            ), tags=(tag,))

        # Aggiorna sort indicator
        for col in self.COLUMNS:
            arrow = ''
            if col == self._sort_col:
                arrow = ' ▼' if self._sort_reverse else ' ▲'
            self.tree.heading(col, text=self.HEADERS[col] + arrow)

        # Contatori unici
        unique_owners = set(d['owner_name'] for d in self._filtered_data if d['owner_name'])
        overdue_label = self.lang.get('npi_overdue_status_overdue', 'task scaduti')
        owners_label = self.lang.get('npi_overdue_status_owners', 'responsabili')
        total_label = self.lang.get('npi_overdue_status_total', 'Totale')
        self.status_var.set(
            f"{len(self._filtered_data)} {overdue_label}  |  "
            f"{len(unique_owners)} {owners_label}  |  "
            f"{total_label}: {len(self._all_data)}"
        )

    # ────────────────────────── Email ──────────────────────────
    def _send_reminders_all(self):
        """Invia sollecito a tutti i responsabili nella lista filtrata."""
        if not self._filtered_data:
            messagebox.showinfo('Info',
                                self.lang.get('npi_overdue_no_tasks', 'Nessun task in lista.'),
                                parent=self)
            return
        self._send_reminders(self._filtered_data)

    def _send_reminders_selected(self):
        """Invia sollecito solo ai responsabili dei task selezionati."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('npi_overdue_select_task', 'Selezionare almeno un task.'),
                parent=self
            )
            return

        # Recupera i dati corrispondenti alle righe selezionate
        selected_data = []
        for iid in selection:
            idx = self.tree.index(iid)
            if idx < len(self._filtered_data):
                selected_data.append(self._filtered_data[idx])
        self._send_reminders(selected_data)

    def _send_reminders(self, tasks_data):
        """Raggruppa per owner e invia email di sollecito."""
        # Raggruppa per owner
        by_owner = defaultdict(list)
        for t in tasks_data:
            if t['owner_email']:
                by_owner[(t['owner_name'], t['owner_email'])].append(t)

        if not by_owner:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('npi_overdue_no_email', 'Nessun responsabile con indirizzo email trovato.'),
                parent=self
            )
            return

        owner_list = '\n'.join(f"  • {name} ({email}) — {len(tasks)} task"
                               for (name, email), tasks in by_owner.items())

        if not messagebox.askyesno(
            self.lang.get('npi_overdue_confirm_title', 'Conferma invio'),
            f"{self.lang.get('npi_overdue_confirm_msg', 'Inviare email di sollecito a')} "
            f"{len(by_owner)} {self.lang.get('npi_overdue_status_owners', 'responsabili')}?\n\n"
            f"{owner_list}\n\n"
            f"Totale task: {len(tasks_data)}",
            parent=self
        ):
            return

        self.config(cursor='watch')
        self.update_idletasks()

        sent = 0
        failed = 0
        try:
            from email_connector import EmailSender
            email_sender = EmailSender()

            for (owner_name, owner_email), tasks in by_owner.items():
                try:
                    # Costruisci corpo email
                    tasks_html = ''.join(
                        f"<tr>"
                        f"<td style='padding:6px;border:1px solid #ddd'>{t['project_name']}</td>"
                        f"<td style='padding:6px;border:1px solid #ddd'>{t['product_code']}</td>"
                        f"<td style='padding:6px;border:1px solid #ddd'>{t['task_name']}</td>"
                        f"<td style='padding:6px;border:1px solid #ddd;text-align:center'>"
                        f"{t['due_date'].strftime('%Y-%m-%d') if t['due_date'] else 'N/A'}</td>"
                        f"<td style='padding:6px;border:1px solid #ddd;text-align:center;color:#C0392B'>"
                        f"{t['days_late']}d</td>"
                        f"</tr>"
                        for t in tasks
                    )

                    body = f"""
                    <html><body style="font-family:Arial,sans-serif">
                    <h2 style="color:#C0392B">NPI — Overdue Task Reminder</h2>
                    <p>Dear {owner_name},</p>
                    <p>The following <strong>{len(tasks)}</strong> NPI tasks assigned to you are 
                    <strong>overdue</strong>. Please update their status as soon as possible.</p>
                    <table style="border-collapse:collapse;width:100%">
                    <thead><tr style="background:#C0392B;color:#fff">
                        <th style="padding:8px;border:1px solid #ddd">Project</th>
                        <th style="padding:8px;border:1px solid #ddd">Product</th>
                        <th style="padding:8px;border:1px solid #ddd">Task</th>
                        <th style="padding:8px;border:1px solid #ddd">Due Date</th>
                        <th style="padding:8px;border:1px solid #ddd">Days Late</th>
                    </tr></thead>
                    <tbody>{tasks_html}</tbody>
                    </table>
                    <br><p>Thank you,<br><strong>NPI Management System</strong></p>
                    </body></html>
                    """

                    email_sender.send_email(
                        to_email=owner_email,
                        subject="NPI — Overdue Task Reminder",
                        body=body,
                        is_html=True
                    )
                    sent += 1
                    logger.info(f"Sollecito NPI inviato a {owner_email} ({len(tasks)} task)")
                except Exception as e:
                    failed += 1
                    logger.error(f"Errore invio sollecito a {owner_email}: {e}")

        except Exception as e:
            logger.error(f"Errore inizializzazione EmailSender: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('npi_overdue_email_error', 'Errore email')}:\n{e}",
                parent=self
            )
            return
        finally:
            self.config(cursor='')

        msg = f"{self.lang.get('npi_overdue_email_sent', 'Email inviate')}: {sent}"
        if failed:
            msg += f"\n{self.lang.get('npi_overdue_email_failed', 'Fallite')}: {failed}"
        messagebox.showinfo(self.lang.get('npi_overdue_result', 'Risultato'), msg, parent=self)

    # ────────────────────────── Excel ──────────────────────────
    def _export_excel(self):
        """Genera Excel con i task filtrati correnti."""
        if not self._filtered_data:
            messagebox.showinfo('Info',
                                self.lang.get('npi_overdue_no_export', 'Nessun task da esportare.'),
                                parent=self)
            return

        self.config(cursor='watch')
        self.update_idletasks()
        try:
            file_path = self.npi_manager.export_overdue_tasks_to_excel(self._filtered_data)
            if messagebox.askyesno(
                self.lang.get('success', 'Successo'),
                f"{self.lang.get('npi_overdue_excel_saved', 'Excel salvato in')}:\n{file_path}\n\n"
                f"{self.lang.get('npi_overdue_open_now', 'Aprirlo ora?')}",
                parent=self
            ):
                os.startfile(file_path)
        except Exception as e:
            logger.error(f"Errore export Excel task scaduti: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('npi_overdue_export_error', 'Impossibile generare Excel')}:\n{e}",
                parent=self
            )
        finally:
            self.config(cursor='')
