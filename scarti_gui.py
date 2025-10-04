# File: scarti_gui.py

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


def open_scrap_declaration_window(parent, db_connection, lang_manager):
    """
    Finestra 'Dichiarazione scarti' con:
    - Inserimento codice scheda (LabelCod) e verifica via DB
    - Campi attivati solo dopo verifica positiva
    - Quantità rimossa (si lavora per scheda singola)
    - 'Area di provenienza' e 'Motivo' caricati da DB
    - Operatore precompilato e non modificabile (ultimo utente autenticato)
    - Salvataggio in dbo.ScarpDeclarations, con immagine opzionale
    """
    win = tk.Toplevel(parent)
    win.title(lang_manager.get('scrap_title', "Dichiarazione scarti"))
    win.geometry("580x520")
    win.transient(parent)
    win.grab_set()

    # Stato
    verified = tk.BooleanVar(value=False)
    id_label_code_var = tk.IntVar(value=0)
    board_info = {"OrderNumber": "", "OrderDate": "", "OrderQuantity": "", "ProductCode": ""}

    # Operatore (non modificabile)
    operator_name = getattr(parent, 'last_authenticated_user_name', '') or ""
    operator_var = tk.StringVar(value=operator_name)

    # Immagine allegata (opzionale)
    picture_path_var = tk.StringVar(value="")
    picture_bytes = None

    # UI
    main = ttk.Frame(win, padding=12)
    main.pack(fill="both", expand=True)

    row = 0

    # Codice scheda
    ttk.Label(main, text=lang_manager.get('scrap_label_code', "Codice scheda")).grid(row=row, column=0, sticky="w", pady=6)
    label_code_var = tk.StringVar()
    label_code_entry = ttk.Entry(main, textvariable=label_code_var, width=28)
    label_code_entry.grid(row=row, column=1, sticky="w", pady=6)
    verify_btn = ttk.Button(main, text=lang_manager.get('scrap_verify_button', "Verifica"))
    verify_btn.grid(row=row, column=2, sticky="w", padx=8)
    row += 1

    # Info ordine/prodotto (read-only)
    ttk.Label(main, text=lang_manager.get('order_number', "Numero ordine")).grid(row=row, column=0, sticky="w", pady=4)
    order_number_var = tk.StringVar()
    order_number_entry = ttk.Entry(main, textvariable=order_number_var, state="readonly", width=28)
    order_number_entry.grid(row=row, column=1, sticky="w", pady=4)
    row += 1

    ttk.Label(main, text=lang_manager.get('order_date', "Data ordine")).grid(row=row, column=0, sticky="w", pady=4)
    order_date_var = tk.StringVar()
    order_date_entry = ttk.Entry(main, textvariable=order_date_var, state="readonly", width=28)
    order_date_entry.grid(row=row, column=1, sticky="w", pady=4)
    row += 1

    ttk.Label(main, text=lang_manager.get('order_qty', "Quantità ordine")).grid(row=row, column=0, sticky="w", pady=4)
    order_qty_var = tk.StringVar()
    order_qty_entry = ttk.Entry(main, textvariable=order_qty_var, state="readonly", width=28)
    order_qty_entry.grid(row=row, column=1, sticky="w", pady=4)
    row += 1

    ttk.Label(main, text=lang_manager.get('scrap_product', "Prodotto")).grid(row=row, column=0, sticky="w", pady=4)
    product_code_var = tk.StringVar()
    product_code_entry = ttk.Entry(main, textvariable=product_code_var, state="readonly", width=28)
    product_code_entry.grid(row=row, column=1, sticky="w", pady=4)
    row += 1

    # Area di provenienza (combo) - disabilitata fino a verifica
    ttk.Label(main, text=lang_manager.get('scrap_origin_area', "Area di provenienza")).grid(row=row, column=0, sticky="w", pady=6)
    origin_area_var = tk.StringVar()
    origin_area_combo = ttk.Combobox(main, textvariable=origin_area_var, state="disabled", width=32)
    origin_area_combo.grid(row=row, column=1, sticky="w", pady=6)
    row += 1

    # Motivo (combo da DB) - disabilitata fino a verifica
    ttk.Label(main, text=lang_manager.get('scrap_reason', "Motivo")).grid(row=row, column=0, sticky="w", pady=6)
    scrap_reason_var = tk.StringVar()
    scrap_reason_combo = ttk.Combobox(main, textvariable=scrap_reason_var, state="disabled", width=32)
    scrap_reason_combo.grid(row=row, column=1, sticky="w", pady=6)
    row += 1

    # Operatore (non modificabile)
    ttk.Label(main, text=lang_manager.get('scrap_operator', "Operatore")).grid(row=row, column=0, sticky="w", pady=6)
    operator_entry = ttk.Entry(main, textvariable=operator_var, state="readonly", width=32)
    operator_entry.grid(row=row, column=1, sticky="w", pady=6)
    row += 1

    # Note
    ttk.Label(main, text=lang_manager.get('scrap_notes', "Note")).grid(row=row, column=0, sticky="nw", pady=6)
    notes_txt = tk.Text(main, width=40, height=5, state="disabled")
    notes_txt.grid(row=row, column=1, sticky="w", pady=6)
    row += 1

    # Immagine (opzionale)
    ttk.Label(main, text=lang_manager.get('scrap_picture', "Immagine")).grid(row=row, column=0, sticky="w", pady=6)
    pic_frame = ttk.Frame(main)
    pic_frame.grid(row=row, column=1, sticky="w", pady=6)
    pic_label = ttk.Label(pic_frame, textvariable=picture_path_var, width=34)
    pic_label.pack(side="left", padx=(0, 6))
    select_pic_btn = ttk.Button(pic_frame, text=lang_manager.get('select_picture', "Seleziona..."), state="disabled")
    select_pic_btn.pack(side="left")
    row += 1

    # Bottoni
    btns = ttk.Frame(main)
    btns.grid(row=row, column=0, columnspan=3, pady=12, sticky="e")
    save_btn = ttk.Button(btns, text=lang_manager.get('save', "Salva"), state="disabled")
    cancel_btn = ttk.Button(btns, text=lang_manager.get('cancel', "Annulla"), command=win.destroy)
    save_btn.pack(side="right", padx=8)
    cancel_btn.pack(side="right")

    # Dizionari per mapping ID/descrizione
    origin_map = {}   # nome -> id
    reason_map = {}   # reason -> id

    def enable_fields():
        origin_area_combo.config(state="readonly")
        scrap_reason_combo.config(state="readonly")
        notes_txt.config(state="normal")
        select_pic_btn.config(state="normal")
        save_btn.config(state="normal")

    def disable_fields():
        origin_area_combo.config(state="disabled", values=[])
        scrap_reason_combo.config(state="disabled", values=[])
        notes_txt.delete("1.0", "end")
        notes_txt.config(state="disabled")
        select_pic_btn.config(state="disabled")
        save_btn.config(state="disabled")
        picture_path_var.set("")
        nonlocal picture_bytes
        picture_bytes = None

    def do_verify():
        disable_fields()

        code = label_code_var.get().strip()
        if not code:
            messagebox.showerror(lang_manager.get('error', "Errore"),
                                 lang_manager.get('scrap_invalid_label', "Codice scheda non valido"),
                                 parent=win)
            return

        info = db_connection.get_scrap_label_info(code)
        if not info:
            messagebox.showerror(lang_manager.get('error', "Errore"),
                                 lang_manager.get('scrap_invalid_label', "Codice scheda non valido"),
                                 parent=win)
            return

        # Popola campi read-only
        order_number_var.set(getattr(info, 'OrderNumber', '') or '')
        order_date_var.set(getattr(info, 'OrderDate', '') or '')
        order_qty_var.set(str(getattr(info, 'OrderQuantity', '') or ''))
        product_code_var.set(getattr(info, 'ProductCode', '') or '')

        # Ricava IDLabelCode (se non presente, tenta con helper)
        label_id = getattr(info, 'IDLabelCode', None)
        if label_id is None:
            label_id = db_connection.get_label_id_by_code(code)
        if not label_id:
            # Non blocchiamo la UI, ma non abilitiamo salvataggio
            messagebox.showerror(lang_manager.get('error', "Errore"),
                                 "Impossibile determinare l'ID della scheda (LabelCode).",
                                 parent=win)
            return

        id_label_code_var.set(int(label_id))

        # Carica combo Area di provenienza
        areas = db_connection.fetch_origin_areas_for_scrap()
        names = []
        origin_map.clear()
        for r in areas:
            origin_map[r.ParentPhaseName] = r.idParentPhase
            names.append(r.ParentPhaseName)
        origin_area_combo['values'] = names
        if names:
            origin_area_combo.set(names[0])

        # Carica combo motivi
        reasons = db_connection.fetch_scrap_reasons()
        reason_names = []
        reason_map.clear()
        for r in reasons:
            reason_map[r.Reason] = r.ScrapReasonId
            reason_names.append(r.Reason)
        scrap_reason_combo['values'] = reason_names
        if reason_names:
            scrap_reason_combo.set(reason_names[0])

        verified.set(True)
        enable_fields()

    def select_picture():
        nonlocal picture_bytes
        path = filedialog.askopenfilename(
            title=lang_manager.get('select_picture', "Seleziona..."),
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")],
            parent=win
        )
        if path and os.path.isfile(path):
            try:
                with open(path, "rb") as f:
                    picture_bytes = f.read()
                picture_path_var.set(path)
            except Exception as e:
                picture_bytes = None
                picture_path_var.set("")
                messagebox.showerror(lang_manager.get('error', "Errore"),
                                     f"Impossibile leggere il file immagine: {e}", parent=win)

    def do_save():
        if not verified.get():
            return

        user_name = operator_var.get().strip()[:40]  # rispetto nvarchar(40)
        id_label = id_label_code_var.get()
        origin_name = origin_area_var.get()
        reason_name = scrap_reason_var.get()
        note = notes_txt.get("1.0", "end").strip()[:250]

        if not origin_name or origin_name not in origin_map:
            messagebox.showerror(lang_manager.get('error', "Errore"), "Selezionare l'Area di provenienza.", parent=win)
            return
        if not reason_name or reason_name not in reason_map:
            messagebox.showerror(lang_manager.get('error', "Errore"), "Selezionare il Motivo.", parent=win)
            return

        ok = db_connection.insert_scrap_declaration(
            user_name=user_name,
            id_label_code=id_label,
            id_parent_phase=origin_map[origin_name],
            scrap_reason_id=reason_map[reason_name],
            note=note,
            picture_bytes=picture_bytes
        )
        if ok:
            messagebox.showinfo(lang_manager.get('info', "Informazione"),
                                lang_manager.get('saved_ok', "Dichiarazione salvata"),
                                parent=win)
            win.destroy()
        else:
            messagebox.showerror(lang_manager.get('error', "Errore"),
                                 lang_manager.get('saved_ko', f"Errore nel salvataggio: {db_connection.last_error_details}"),
                                 parent=win)

    # Bind bottoni
    verify_btn.config(command=do_verify)
    select_pic_btn.config(command=select_picture)
    save_btn.config(command=do_save)

    # Layout
    for c in (0, 1):
        main.grid_columnconfigure(c, weight=1)

    label_code_entry.focus_set()
    win.wait_window()

def open_scrap_reasons_manager(parent, db, lang):
    ScrapReasonsManagerWindow(parent, db, lang)

class ScrapReasonsManagerWindow(tk.Toplevel):
    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang

        self.title(self.lang.get('scrap_reasons_mgmt_title', 'Gestione Tipi scrap'))
        self.geometry("550x400")
        self.transient(parent)
        self.grab_set()

        self.current_id = None
        self.reasons = []

        self._build_ui()
        self._load_reasons()

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill="both", expand=True)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)

        # Lista motivi
        ttk.Label(main, text=self.lang.get('scrap_reasons_list_label', 'Elenco motivi')).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,6))

        cols = ('id', 'reason')
        self.tree = ttk.Treeview(main, columns=cols, show="headings", height=12, selectmode='browse')
        self.tree.heading('id', text='ID')
        self.tree.heading('reason', text=self.lang.get('scrap_reason_label', 'Motivo'))
        self.tree.column('id', width=60, anchor='center')
        self.tree.column('reason', width=360, anchor='w')
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        scrollbar = ttk.Scrollbar(main, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=3, sticky="ns")

        # Form di dettaglio
        ttk.Label(main, text=self.lang.get('scrap_reason_label', 'Motivo')).grid(row=2, column=0, sticky="e", pady=(10,5), padx=(0,6))
        self.reason_var = tk.StringVar()
        self.reason_entry = ttk.Entry(main, textvariable=self.reason_var)
        self.reason_entry.grid(row=2, column=1, sticky="ew", pady=(10,5))
        ttk.Button(main, text=self.lang.get('new_button_short', 'Nuovo'), command=self._new).grid(row=2, column=2, sticky="w", pady=(10,5), padx=5)

        # Bottoni
        btns = ttk.Frame(main)
        btns.grid(row=3, column=0, columnspan=3, sticky="e", pady=(10,0))
        ttk.Button(btns, text=self.lang.get('save_button', 'Salva'), command=self._save).pack(side="right", padx=5)
        ttk.Button(btns, text=self.lang.get('delete_button', 'Cancella'), command=self._delete).pack(side="right", padx=5)
        ttk.Button(btns, text=self.lang.get('cancel_button', 'Chiudi'), command=self.destroy).pack(side="right")

    def _load_reasons(self):
        self.tree.delete(*self.tree.get_children())
        self.reasons = self.db.fetch_scrap_reasons() or []
        for r in self.reasons:
            self.tree.insert('', tk.END, iid=str(r.ScrapReasonId), values=(r.ScrapReasonId, r.Reason))

    def _on_select(self, event=None):
        sel = self.tree.focus()
        if not sel:
            return
        try:
            self.current_id = int(sel)
        except ValueError:
            self.current_id = None
            return
        # Valore testo
        values = self.tree.item(sel, 'values')
        self.reason_var.set(values[1] if len(values) > 1 else '')

    def _new(self):
        self.tree.selection_remove(self.tree.selection())
        self.current_id = None
        self.reason_var.set('')
        self.reason_entry.focus_set()

    def _save(self):
        text = (self.reason_var.get() or '').strip()
        if not text:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                   self.lang.get('error_reason_required', 'Inserire un motivo valido.'), parent=self)
            return

        if self.current_id is None:
            ok = self.db.insert_scrap_reason(text)
        else:
            ok = self.db.update_scrap_reason(self.current_id, text)

        if ok:
            self._load_reasons()
            # Reseleziona/posiziona
            if self.current_id is None:
                # seleziona la riga con lo stesso testo (best effort)
                for iid in self.tree.get_children():
                    vals = self.tree.item(iid, 'values')
                    if len(vals) > 1 and str(vals[1]).strip().lower() == text.lower():
                        self.tree.selection_set(iid)
                        self.tree.focus(iid)
                        break
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                                self.lang.get('info_saved_ok', 'Salvataggio eseguito.'), parent=self)
        else:
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                 self.db.last_error_details or self.lang.get('error_db_operation', 'Errore database.'),
                                 parent=self)

    def _delete(self):
        if self.current_id is None:
            messagebox.showwarning(self.lang.get('warning_title', 'Attenzione'),
                                   self.lang.get('warning_select_reason', 'Seleziona un motivo da cancellare.'), parent=self)
            return

        if not messagebox.askyesno(
            self.lang.get('confirm_title', 'Conferma'),
            self.lang.get('confirm_delete_reason', 'Sei sicuro di voler cancellare il motivo selezionato?'),
            parent=self
        ):
            return

        ok = self.db.delete_scrap_reason(self.current_id)
        if ok:
            self._new()
            self._load_reasons()
            messagebox.showinfo(self.lang.get('success_title', 'Successo'),
                                self.lang.get('info_deleted_ok', 'Cancellazione eseguita.'), parent=self)
        else:
            # Probabile vincolo FK se il motivo è usato in dichiarazioni
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                 self.db.last_error_details or self.lang.get('error_db_operation', 'Errore database.'),
                                 parent=self)