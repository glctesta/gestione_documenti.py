# -*- coding: utf-8 -*-
"""
scrap_returns_gui.py
Form "Gestione scorie / rientri materiali".

Registra in dbo.ReturnMaterials i kg di materiale scartato/rientrato. Si possono
dichiarare solo i materiali-scoria (MustCode) collegati a un materiale richiesto
tramite dbo.MaterialRules (regole attive, DateOut IS NULL).

Spec: docs/GestioneScorie_ReturnMaterials_Spec_v1.0.md
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import date

logger = logging.getLogger(__name__)


def open_scrap_returns(master, db, lang, user_name="Unknown", preselect_must_code_id=None):
    return ScrapReturnsWindow(master, db, lang, user_name, preselect_must_code_id)


class ScrapReturnsWindow(tk.Toplevel):
    def __init__(self, master, db, lang, user_name="Unknown", preselect_must_code_id=None):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name or "Unknown"
        self._preselect = preselect_must_code_id

        self.title(lang.get('scrap_title', 'Gestione Scorie / Rientri Materiali'))
        self.geometry("720x620")
        self.resizable(True, True)
        self.transient(master)
        self.grab_set()

        self._materials = []   # [{must_code_id, codice, descrizione, for_text}]
        self._build_ui()
        self._load_materials()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    # ------------------------------------------------------------------ #
    def _build_ui(self):
        main = ttk.Frame(self, padding=12)
        main.pack(expand=True, fill="both")

        ttk.Label(main, text=self.lang.get('scrap_header', 'Dichiarazione scorie / rientri'),
                  font=("Segoe UI", 13, "bold")).pack(fill="x", pady=(0, 10))

        form = ttk.LabelFrame(main, text=self.lang.get('scrap_new', 'Nuova registrazione'), padding=10)
        form.pack(fill="x")

        # Materiale (scoria / MustCode)
        ttk.Label(form, text=self.lang.get('scrap_material', 'Materiale (scoria):')).grid(
            row=0, column=0, sticky="w", padx=4, pady=4)
        self.material_var = tk.StringVar()
        self.material_combo = ttk.Combobox(form, textvariable=self.material_var,
                                           state="readonly", width=46)
        self.material_combo.grid(row=0, column=1, columnspan=3, sticky="w", padx=4, pady=4)
        self.material_combo.bind('<<ComboboxSelected>>', self._on_material_change)

        # Per quale materiale richiesto
        self.for_var = tk.StringVar(value="")
        ttk.Label(form, textvariable=self.for_var, foreground="#555",
                  font=("Segoe UI", 9, "italic")).grid(row=1, column=0, columnspan=4, sticky="w", padx=4)

        # Data (default oggi)
        ttk.Label(form, text=self.lang.get('scrap_date', 'Data:')).grid(
            row=2, column=0, sticky="w", padx=4, pady=4)
        self.date_widget = self._make_date_entry(form)
        self.date_widget.grid(row=2, column=1, sticky="w", padx=4, pady=4)

        # Peso (kg, 1 decimale)
        ttk.Label(form, text=self.lang.get('scrap_weight', 'Peso (kg):')).grid(
            row=2, column=2, sticky="w", padx=4, pady=4)
        self.weight_var = tk.StringVar(value="")
        ttk.Entry(form, textvariable=self.weight_var, width=12).grid(
            row=2, column=3, sticky="w", padx=4, pady=4)

        ttk.Button(form, text=self.lang.get('scrap_btn_save', '💾 Registra'),
                   command=self._save).grid(row=3, column=0, columnspan=4, pady=(10, 0))

        # Storico registrazioni del materiale selezionato
        hist = ttk.LabelFrame(main, text=self.lang.get('scrap_history', 'Registrazioni'), padding=8)
        hist.pack(fill="both", expand=True, pady=(12, 0))
        cols = ('rmid', 'data', 'peso', 'utente', 'stato', 'confermato')
        self.tree = ttk.Treeview(hist, columns=cols, show='headings', height=8)
        self.tree.heading('rmid', text='')
        self.tree.heading('data', text=self.lang.get('scrap_col_date', 'Data'))
        self.tree.heading('peso', text=self.lang.get('scrap_col_weight', 'Peso dich. (kg)'))
        self.tree.heading('utente', text=self.lang.get('scrap_col_user', 'Utente'))
        self.tree.heading('stato', text=self.lang.get('scrap_col_status', 'Stato'))
        self.tree.heading('confermato', text=self.lang.get('scrap_col_confirmed', 'Convalida'))
        self.tree.column('rmid', width=0, stretch=False)
        self.tree.column('data', width=95)
        self.tree.column('peso', width=95, anchor="e")
        self.tree.column('utente', width=130)
        self.tree.column('stato', width=120, anchor="center")
        self.tree.column('confermato', width=150, anchor="center")
        sb = ttk.Scrollbar(hist, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Pannello convalida (controllore): pesa reale + conferma
        valid = ttk.LabelFrame(main, text=self.lang.get('scrap_validate_panel',
                                                        'Convalida quantità dichiarata (controllo)'),
                               padding=8)
        valid.pack(fill="x", pady=(8, 0))
        ttk.Label(valid, text=self.lang.get('scrap_confirmed_weight', 'Peso rilevato (kg):')).pack(
            side="left", padx=(0, 6))
        self.confirm_weight_var = tk.StringVar(value="")
        ttk.Entry(valid, textvariable=self.confirm_weight_var, width=12).pack(side="left", padx=(0, 12))
        ttk.Button(valid, text=self.lang.get('scrap_btn_validate', '✔ Convalida selezionata'),
                   command=self._validate_selected).pack(side="left")
        ttk.Button(valid, text=self.lang.get('scrap_btn_override', '⚠ Forza conforme'),
                   command=self._force_conform).pack(side="left", padx=(12, 0))
        self.tree.bind('<<TreeviewSelect>>', self._on_history_select)

    def _make_date_entry(self, parent):
        try:
            from tkcalendar import DateEntry
            de = DateEntry(parent, width=12, date_pattern='dd/MM/yyyy')
            de.set_date(date.today())
            return de
        except Exception:
            # fallback: entry testuale preimpostata a oggi (dd/MM/yyyy)
            self._date_fallback = tk.StringVar(value=date.today().strftime('%d/%m/%Y'))
            return ttk.Entry(parent, textvariable=self._date_fallback, width=14)

    def _get_selected_date(self):
        if hasattr(self.date_widget, 'get_date'):
            return self.date_widget.get_date()
        from datetime import datetime
        return datetime.strptime(self._date_fallback.get().strip(), '%d/%m/%Y').date()

    # ------------------------------------------------------------------ #
    def _fetch(self, query, params=None):
        if hasattr(self.db, 'fetch_all'):
            return self.db.fetch_all(query, params) if params else self.db.fetch_all(query)
        self.db._ensure_connection()
        with self.db._lock:
            self.db.cursor.execute(query, params) if params else self.db.cursor.execute(query)
            return self.db.cursor.fetchall()

    def _load_materials(self):
        """Materiali-scoria selezionabili (MustCode) dalle regole attive."""
        query = """
            SELECT m1.MaterialeId, m1.CodiceMateriale, m1.DescrizioneMateriale,
                   m.CodiceMateriale AS IndirectMaterial, m.DescrizioneMateriale AS IndirectDescription
            FROM ind.Materiali m
              INNER JOIN dbo.MaterialRules mr ON m.MaterialeId = mr.MaterialeId AND mr.DateOut IS NULL
              INNER JOIN ind.Materiali m1 ON m1.MaterialeId = mr.MustCodeId
            ORDER BY m1.CodiceMateriale
        """
        rows = self._fetch(query) or []
        by_id = {}
        for r in rows:
            mid = r[0]
            entry = by_id.get(mid)
            for_label = f"{r[3]} - {r[4]}"
            if entry is None:
                by_id[mid] = {
                    'must_code_id': mid,
                    'codice': r[1] or '',
                    'descrizione': r[2] or '',
                    'for_list': [for_label],
                }
            else:
                entry['for_list'].append(for_label)

        self._materials = list(by_id.values())
        display = [f"{m['codice']} - {m['descrizione']}" for m in self._materials]
        self.material_combo['values'] = display

        # preselezione (apertura dalla form richieste)
        if self._preselect is not None:
            for i, m in enumerate(self._materials):
                if m['must_code_id'] == self._preselect:
                    self.material_combo.current(i)
                    self._on_material_change()
                    break

    def _current_material(self):
        idx = self.material_combo.current()
        if 0 <= idx < len(self._materials):
            return self._materials[idx]
        return None

    def _on_material_change(self, event=None):
        m = self._current_material()
        if m:
            self.for_var.set(self.lang.get('scrap_for', 'Per il materiale richiesto:') +
                             " " + "; ".join(m['for_list']))
            self._load_history(m['must_code_id'])

    def _load_history(self, must_code_id):
        self.tree.delete(*self.tree.get_children())
        rows = self._fetch(
            "SELECT ReturnMaterialId, DateReturn, ReturWeight, UserRetur, RichiestaId, "
            "       ComfirmedBY, ConfirmedWeight, IsOk, OverrideBy, OverrideReason "
            "FROM dbo.ReturnMaterials WHERE MateriaId = ? AND DateOut IS NULL "
            "ORDER BY DateReturn DESC, ReturnMaterialId DESC",
            (must_code_id,)
        ) or []
        consumed = self.lang.get('scrap_status_consumed', 'Consumata (rich. {0})')
        available = self.lang.get('scrap_status_available', 'Disponibile')
        to_confirm = self.lang.get('scrap_to_confirm', 'Da confermare')
        ok_txt = self.lang.get('scrap_confirmed_ok', '✔ OK ({0} kg)')
        ko_txt = self.lang.get('scrap_confirmed_ko', 'X NON conforme ({0} kg)')
        override_txt = self.lang.get('scrap_confirmed_override', '✔ Forzato ({0} kg)')
        for r in rows:
            rmid = r[0]
            d = r[1].strftime('%d/%m/%Y') if r[1] else ''
            stato = consumed.format(r[4]) if r[4] is not None else available
            confirmed_by = r[5]
            confirmed_w = r[6]
            is_ok = r[7]
            override_by = r[8]
            if confirmed_by is None and is_ok is None and override_by is None:
                conferma = to_confirm
            else:
                cw = f"{float(confirmed_w or 0):.1f}"
                if is_ok and override_by:
                    conferma = override_txt.format(cw)
                elif is_ok:
                    conferma = ok_txt.format(cw)
                else:
                    conferma = ko_txt.format(cw)
            self.tree.insert('', 'end', values=(
                rmid, d, f"{float(r[2] or 0):.1f}", r[3] or '', stato, conferma))

    def _on_history_select(self, event=None):
        """Pre-compila il peso rilevato con il peso dichiarato della riga selezionata."""
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], 'values')
        # vals: (rmid, data, peso_dich, utente, stato, conferma)
        if not self.confirm_weight_var.get().strip():
            self.confirm_weight_var.set(str(vals[2]))

    def _validate_selected(self):
        """Convalida la riga selezionata: registra peso rilevato, ComfirmedBY e IsOk."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('scrap_select_row', 'Seleziona una registrazione da convalidare.'),
                                   parent=self)
            return
        vals = self.tree.item(sel[0], 'values')
        rmid = vals[0]
        try:
            declared = round(float(str(vals[2]).replace(',', '.')), 1)
        except ValueError:
            declared = None
        try:
            confirmed = round(float(self.confirm_weight_var.get().replace(',', '.')), 1)
        except ValueError:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 self.lang.get('scrap_invalid_weight', 'Peso non valido.'), parent=self)
            return
        if confirmed < 0:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 self.lang.get('scrap_weight_positive', 'Il peso deve essere maggiore di 0.'),
                                 parent=self)
            return

        is_ok = 1 if (declared is not None and abs(confirmed - declared) < 0.05) else 0
        if not is_ok:
            if not messagebox.askyesno(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('scrap_mismatch_confirm',
                              'Il peso rilevato ({0} kg) NON corrisponde al dichiarato ({1} kg).\n'
                              'Registrare comunque come NON conforme?').format(
                              f"{confirmed:.1f}", f"{declared:.1f}" if declared is not None else "?"),
                parent=self):
                return

        try:
            self.db._ensure_connection()
            with self.db._lock:
                self.db.cursor.execute(
                    "UPDATE dbo.ReturnMaterials "
                    "SET ConfirmedWeight = ?, ComfirmedBY = ?, IsOk = ? "
                    "WHERE ReturnMaterialId = ?",
                    (confirmed, self.user_name, is_ok, rmid)
                )
                self.db.conn.commit()
            logger.info("Scoria convalidata: ReturnMaterialId=%s peso_rilevato=%.1f IsOk=%s da %s",
                        rmid, confirmed, is_ok, self.user_name)
            messagebox.showinfo(self.lang.get('info', 'Info'),
                                self.lang.get('scrap_validated_ok', 'Convalida registrata.'), parent=self)
            self.confirm_weight_var.set("")
            m = self._current_material()
            if m:
                self._load_history(m['must_code_id'])
        except Exception as e:
            try:
                self.db.conn.rollback()
            except Exception:
                pass
            logger.error("Errore convalida scoria: %s", e, exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 f"{self.lang.get('scrap_save_error', 'Errore salvataggio')}:\n{e}",
                                 parent=self)

    def _force_conform(self):
        """Sblocca una riga NON conforme forzando IsOk=1 con motivazione obbligatoria.
        Richiede autorizzazione supervisore (chiave 'override_convalida_scorie') e
        traccia chi/perche'/quando in OverrideBy/OverrideReason/OverrideDate. Non
        sovrascrive ComfirmedBY/ConfirmedWeight (resta la prova del mismatch rilevato)."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('scrap_select_row', 'Seleziona una registrazione da convalidare.'),
                                   parent=self)
            return
        rmid = self.tree.item(sel[0], 'values')[0]
        # Stato reale dal DB: l'override si applica SOLO alle righe NON conformi (IsOk=0).
        row = self._fetch("SELECT IsOk FROM dbo.ReturnMaterials WHERE ReturnMaterialId = ?", (rmid,))
        is_ok = row[0][0] if row else None
        if is_ok == 1:
            messagebox.showinfo(self.lang.get('info', 'Info'),
                                self.lang.get('scrap_override_already_ok', 'La riga è già conforme.'),
                                parent=self)
            return
        if is_ok is None:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('scrap_override_only_ko',
                                                 "L'override si applica solo alle righe NON conformi.\n"
                                                 "Convalida prima la riga con il peso rilevato."),
                                   parent=self)
            return
        # Motivazione obbligatoria
        from tkinter import simpledialog
        reason = simpledialog.askstring(
            self.lang.get('scrap_override_title', 'Forza conforme'),
            self.lang.get('scrap_override_reason', 'Motivazione (obbligatoria):'),
            parent=self)
        if reason is None:
            return
        reason = reason.strip()
        if not reason:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('scrap_override_reason_required', 'La motivazione è obbligatoria.'),
                                   parent=self)
            return
        if not messagebox.askyesno(
                self.lang.get('scrap_override_title', 'Forza conforme'),
                self.lang.get('scrap_override_confirm',
                              'Forzare la riga come CONFORME? La richiesta collegata potrà essere rilasciata.'),
                parent=self):
            return

        def do_override():
            supervisor = getattr(self.master, 'last_authenticated_user_name', None) or self.user_name
            try:
                self.db._ensure_connection()
                with self.db._lock:
                    self.db.cursor.execute(
                        "UPDATE dbo.ReturnMaterials "
                        "SET IsOk = 1, OverrideBy = ?, OverrideReason = ?, OverrideDate = GETDATE() "
                        "WHERE ReturnMaterialId = ?",
                        (supervisor, reason, rmid)
                    )
                    self.db.conn.commit()
                logger.info("Scoria FORZATA conforme: ReturnMaterialId=%s da %s motivo=%r",
                            rmid, supervisor, reason)
                messagebox.showinfo(self.lang.get('info', 'Info'),
                                    self.lang.get('scrap_override_done',
                                                  'Override registrato. La riga è ora conforme.'),
                                    parent=self)
                m = self._current_material()
                if m:
                    self._load_history(m['must_code_id'])
            except Exception as e:
                try:
                    self.db.conn.rollback()
                except Exception:
                    pass
                logger.error("Errore override scoria: %s", e, exc_info=True)
                messagebox.showerror(self.lang.get('error', 'Errore'),
                                     f"{self.lang.get('scrap_save_error', 'Errore salvataggio')}:\n{e}",
                                     parent=self)

        # Autorizzazione supervisore tramite il flusso standard dell'app.
        # Rilascio temporaneamente il grab della form per non bloccare la LoginWindow.
        master = self.master
        if not hasattr(master, '_execute_authorized_action'):
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 self.lang.get('scrap_override_no_auth',
                                               'Funzione di autorizzazione non disponibile.'),
                                 parent=self)
            return
        try:
            self.grab_release()
        except Exception:
            pass
        try:
            master._execute_authorized_action('override_convalida_scorie', do_override)
        finally:
            try:
                self.grab_set()
            except Exception:
                pass

    # ------------------------------------------------------------------ #
    def _save(self):
        m = self._current_material()
        if not m:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('scrap_select_material', 'Seleziona un materiale.'),
                                   parent=self)
            return
        # peso: kg, 1 decimale, > 0
        try:
            weight = round(float(self.weight_var.get().replace(',', '.')), 1)
        except ValueError:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 self.lang.get('scrap_invalid_weight', 'Peso non valido.'), parent=self)
            return
        if weight <= 0:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 self.lang.get('scrap_weight_positive', 'Il peso deve essere maggiore di 0.'),
                                 parent=self)
            return
        try:
            d = self._get_selected_date()
        except Exception:
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 self.lang.get('scrap_invalid_date', 'Data non valida.'), parent=self)
            return

        # warning duplicato: stessa MateriaId + stessa data + stesso peso (1 decimale)
        dup = self._fetch(
            "SELECT COUNT(*) FROM dbo.ReturnMaterials "
            "WHERE MateriaId = ? AND DateReturn = ? AND ROUND(ReturWeight,1) = ? AND DateOut IS NULL",
            (m['must_code_id'], d, weight)
        )
        if dup and dup[0][0] > 0:
            if not messagebox.askyesno(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('scrap_dup_warning',
                              'La stessa quantità ({0} kg) è già registrata per questo giorno. '
                              'Confermi comunque?').format(f"{weight:.1f}"),
                parent=self):
                return

        try:
            self.db._ensure_connection()
            with self.db._lock:
                self.db.cursor.execute(
                    "INSERT INTO dbo.ReturnMaterials "
                    "(MateriaId, ReturWeight, DateReturn, UserRetur, RichiestaId) "
                    "VALUES (?, ?, ?, ?, NULL)",
                    (m['must_code_id'], weight, d, self.user_name)
                )
                self.db.conn.commit()
            logger.info("Scoria registrata: MustCode=%s kg=%.1f data=%s da %s",
                        m['must_code_id'], weight, d, self.user_name)
            messagebox.showinfo(self.lang.get('info', 'Info'),
                                self.lang.get('scrap_saved_ok', 'Registrazione salvata.'), parent=self)
            self.weight_var.set("")
            self._load_history(m['must_code_id'])
        except Exception as e:
            try:
                self.db.conn.rollback()
            except Exception:
                pass
            logger.error("Errore salvataggio scoria: %s", e, exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 f"{self.lang.get('scrap_save_error', 'Errore salvataggio')}:\n{e}",
                                 parent=self)
