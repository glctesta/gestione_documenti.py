# File: npi/windows/npi_checklist_window.py
# NPI Summary Sheet (MD.RAQ.089) — Digitized Checklist Window
# Dynamic version: tabs generated from FamilyNpis.ChecklistSection
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class NpiChecklistWindow(tk.Toplevel):
    """Finestra per la gestione della checklist NPI (Summary Sheet MD.RAQ.089).
    Le sezioni (tab) vengono generate dinamicamente in base alla configurazione
    delle famiglie NPI del progetto (FamilyNpis.ChecklistSection)."""

    def __init__(self, parent, npi_manager, project_id, project_name, product_code,
                 logged_in_user, lang, is_owner=False, **kwargs):
        super().__init__(parent)
        self.npi_manager = npi_manager
        self.project_id = project_id
        self.project_name = project_name
        self.product_code = product_code
        self.logged_in_user = logged_in_user
        self.lang = lang
        self.is_owner = is_owner

        self._current_session_id = None
        self._orders_cache = []
        self._family_sections = []  # [{family_id, family_name, section, has_programs, ...}]
        self._section_widgets = {}  # section_key → {programs, materials, production, ...}

        self.title(f"📋 NPI Checklist — {project_name}")
        self.geometry("1200x850")
        self.minsize(1000, 700)
        self.transient(parent)

        self._load_family_config()
        self._build_ui()
        self._load_sessions()

    def _load_family_config(self):
        """Carica la configurazione checklist dalle famiglie del progetto."""
        try:
            self._family_sections = self.npi_manager.get_checklist_families_for_project(self.project_id)
            logger.info(f"Checklist families for project {self.project_id}: {len(self._family_sections)} sezioni")
        except Exception as e:
            logger.error(f"Errore caricamento famiglie checklist: {e}", exc_info=True)
            self._family_sections = []

    def _build_ui(self):
        """Costruisce l'interfaccia principale."""
        # Top bar: session selector
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(top_frame, text=self.lang.get('cl_session', 'Sessione:'),
                  font=("Segoe UI", 10, "bold")).pack(side="left")
        self.session_combo = ttk.Combobox(top_frame, state='readonly', width=50)
        self.session_combo.pack(side="left", padx=5)
        self.session_combo.bind("<<ComboboxSelected>>", self._on_session_selected)

        ttk.Button(top_frame, text=self.lang.get('cl_new', '➕ Nuova'),
                   command=self._new_session).pack(side="left", padx=3)
        ttk.Button(top_frame, text=self.lang.get('cl_save', '💾 Salva'),
                   command=self._save_session).pack(side="left", padx=3)
        ttk.Button(top_frame, text=self.lang.get('cl_delete', '🗑️ Elimina'),
                   command=self._delete_session).pack(side="left", padx=3)

        if self.is_owner:
            ttk.Button(top_frame, text=self.lang.get('cl_approve', '✅ Approva'),
                       command=self._approve_session).pack(side="left", padx=3)

        self.status_label = ttk.Label(top_frame, text="", font=("Segoe UI", 10))
        self.status_label.pack(side="right", padx=10)

        # Notebook tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab 1: Header (always present)
        self._build_tab_header()

        # Dynamic tabs from family config
        for fam in self._family_sections:
            self._build_dynamic_tab(fam)

        # Tab last: Actions/Rework (always present)
        self._build_tab_actions_rework()

    # ================================================================ #
    #  TAB 1 — Header (Intestazione) — always present                   #
    # ================================================================ #
    def _build_tab_header(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=self.lang.get('cl_tab_header', '📋 Intestazione'))

        frm = ttk.LabelFrame(tab, text=self.lang.get('cl_header_info', 'Informazioni Progetto'))
        frm.pack(fill="x", padx=15, pady=10)

        r = 0
        ttk.Label(frm, text="PN:", font=("Segoe UI", 10, "bold")).grid(row=r, column=0, sticky="w", padx=10, pady=5)
        self.pn_var = tk.StringVar(value=self.product_code or '')
        ttk.Label(frm, textvariable=self.pn_var, font=("Segoe UI", 12, "bold"),
                  foreground="#1a5276").grid(row=r, column=1, sticky="w", padx=5)

        r += 1
        ttk.Label(frm, text="Nr. KIT (Ordine):", font=("Segoe UI", 10, "bold")).grid(
            row=r, column=0, sticky="w", padx=10, pady=5)
        self.order_combo = ttk.Combobox(frm, state='readonly', width=45)
        self.order_combo.grid(row=r, column=1, sticky="w", padx=5)
        self.order_combo.bind("<<ComboboxSelected>>", self._on_order_selected)

        r += 1
        ttk.Label(frm, text="QTY:", font=("Segoe UI", 10, "bold")).grid(
            row=r, column=0, sticky="w", padx=10, pady=5)
        self.qty_var = tk.StringVar()
        ttk.Label(frm, textvariable=self.qty_var, font=("Segoe UI", 11)).grid(
            row=r, column=1, sticky="w", padx=5)

        r += 1
        ttk.Label(frm, text=self.lang.get('cl_date', 'Data:'), font=("Segoe UI", 10, "bold")).grid(
            row=r, column=0, sticky="w", padx=10, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime('%d/%m/%Y'))
        ttk.Entry(frm, textvariable=self.date_var, width=15).grid(row=r, column=1, sticky="w", padx=5)

        # Responsabili approvazione finale
        resp_frm = ttk.LabelFrame(tab, text=self.lang.get('cl_responsabili', 'Responsabili'))
        resp_frm.pack(fill="x", padx=15, pady=5)

        self.resp_qualita_var = tk.StringVar()
        self.resp_produzione_var = tk.StringVar()
        self.resp_ingegneria_var = tk.StringVar()

        for i, (label, var) in enumerate([
            ('Responsabil Calitate Proces', self.resp_qualita_var),
            ('Responsabil Producție', self.resp_produzione_var),
            ('Responsabil Inginer Process', self.resp_ingegneria_var),
        ]):
            ttk.Label(resp_frm, text=f"{label}:").grid(row=i, column=0, sticky="w", padx=10, pady=3)
            ttk.Entry(resp_frm, textvariable=var, width=40).grid(row=i, column=1, sticky="w", padx=5, pady=3)

        # Active sections info
        if self._family_sections:
            info_frm = ttk.LabelFrame(tab, text=self.lang.get('cl_phases', 'Fasi Processo'))
            info_frm.pack(fill="x", padx=15, pady=5)
            sections_text = ", ".join([f.get('section', f.get('family_name', '')) for f in self._family_sections])
            ttk.Label(info_frm, text=sections_text, font=("Segoe UI", 10),
                      foreground="#2e86c1").pack(padx=10, pady=5)
        else:
            warn_frm = ttk.Frame(tab)
            warn_frm.pack(fill="x", padx=15, pady=10)
            ttk.Label(warn_frm,
                      text="⚠️ Nessuna famiglia con ChecklistSection configurata per questo progetto.\n"
                           "Configurare le famiglie NPI nella sezione Configurazione.",
                      foreground="#e74c3c", font=("Segoe UI", 10)).pack(padx=10, pady=5)

        self._load_orders()

    def _load_orders(self):
        try:
            self._orders_cache = self.npi_manager.get_orders_for_project(self.project_id)
            display = [f"{o['order_code']} (Qty: {o['quantity']})" for o in self._orders_cache]
            self.order_combo['values'] = display
        except Exception as e:
            logger.error(f"Errore caricamento ordini: {e}", exc_info=True)

    def _on_order_selected(self, event=None):
        idx = self.order_combo.current()
        if 0 <= idx < len(self._orders_cache):
            self.qty_var.set(str(self._orders_cache[idx]['quantity'] or ''))

    # ================================================================ #
    #  DYNAMIC TAB — Built from family config                           #
    # ================================================================ #
    def _build_dynamic_tab(self, family_config):
        """Costruisce un tab dinamico per una famiglia checklist."""
        section_key = family_config['section']
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"🔧 {section_key}")

        # Scrollable content
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel scroll
        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        widgets = {'section': section_key, 'family_id': family_config['family_id']}

        # Programs section
        if family_config.get('has_programs'):
            widgets['programs'] = self._build_program_section(scroll_frame, section_key)

        # Materials section
        if family_config.get('has_materials'):
            widgets['materials'] = self._build_material_section(scroll_frame, section_key)

        # Preforming checks
        if family_config.get('has_preforming_checks'):
            widgets['preforming'] = self._build_preforming_section(scroll_frame, section_key)

        # Production data
        if family_config.get('has_production_data'):
            widgets['production'] = self._build_production_section(scroll_frame, section_key)

        # Coating info
        if family_config.get('has_coating'):
            widgets['coating'] = self._build_coating_section(scroll_frame, section_key)

        # Verification
        if family_config.get('has_verification'):
            widgets['verification'] = self._build_verification_section(scroll_frame, section_key)

        self._section_widgets[section_key] = widgets

    # ================================================================ #
    #  Reusable builders                                                #
    # ================================================================ #
    def _build_program_section(self, parent, section_key):
        """Sezione programmi — Treeview editabile per aggiungere righe liberamente."""
        frm = ttk.LabelFrame(parent, text=f'Programs — {section_key}')
        frm.pack(fill="x", padx=10, pady=5)

        cols = ('step', 'line_nr', 'program_name', 'result', 'responsible', 'date', 'note')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=6)
        for col, heading, w in [
            ('step', 'Process Step', 120), ('line_nr', 'Line nr', 80),
            ('program_name', 'Program name', 200), ('result', 'Result', 80),
            ('responsible', 'Responsible', 120), ('date', 'Date', 90), ('note', 'Note', 150)
        ]:
            tree.heading(col, text=heading)
            tree.column(col, width=w)
        tree.pack(fill="x", padx=5, pady=3)

        btn_frm = ttk.Frame(frm)
        btn_frm.pack(fill="x", padx=5, pady=2)
        ttk.Button(btn_frm, text='➕', width=3,
                   command=lambda: self._add_program_row(tree, section_key)).pack(side="left", padx=2)
        ttk.Button(btn_frm, text='✏️', width=3,
                   command=lambda: self._edit_tree_row(tree, cols)).pack(side="left", padx=2)
        ttk.Button(btn_frm, text='❌', width=3,
                   command=lambda: self._remove_tree_row(tree)).pack(side="left", padx=2)
        return tree

    def _build_material_section(self, parent, section_key):
        """Sezione materiali — Treeview."""
        frm = ttk.LabelFrame(parent, text=f'Materials / Fixtures / Tools — {section_key}')
        frm.pack(fill="x", padx=10, pady=5)

        cols = ('type', 'code_pn', 'note')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=5)
        tree.heading('type', text='Material / Tool')
        tree.heading('code_pn', text='Code / PN')
        tree.heading('note', text='Note')
        tree.column('type', width=200)
        tree.column('code_pn', width=250)
        tree.column('note', width=250)
        tree.pack(fill="x", padx=5, pady=3)

        btn_frm = ttk.Frame(frm)
        btn_frm.pack(fill="x", padx=5, pady=2)
        ttk.Button(btn_frm, text='➕', width=3,
                   command=lambda: self._add_material_row(tree, section_key)).pack(side="left", padx=2)
        ttk.Button(btn_frm, text='✏️', width=3,
                   command=lambda: self._edit_tree_row(tree, cols)).pack(side="left", padx=2)
        ttk.Button(btn_frm, text='❌', width=3,
                   command=lambda: self._remove_tree_row(tree)).pack(side="left", padx=2)
        return tree

    def _build_preforming_section(self, parent, section_key):
        """Sezione preforming checks con OK/Not OK."""
        frm = ttk.LabelFrame(parent, text=f'Preforming / Pre-assembly — {section_key}')
        frm.pack(fill="x", padx=10, pady=5)

        cols = ('item', 'result', 'note')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=5)
        tree.heading('item', text='Check Item')
        tree.heading('result', text='Result (OK/Not OK)')
        tree.heading('note', text='Note')
        tree.column('item', width=350)
        tree.column('result', width=130)
        tree.column('note', width=250)
        tree.pack(fill="x", padx=5, pady=3)

        btn_frm = ttk.Frame(frm)
        btn_frm.pack(fill="x", padx=5, pady=2)
        ttk.Button(btn_frm, text='➕', width=3,
                   command=lambda: self._add_preforming_row(tree, section_key)).pack(side="left", padx=2)
        ttk.Button(btn_frm, text='✏️', width=3,
                   command=lambda: self._edit_tree_row(tree, cols)).pack(side="left", padx=2)
        ttk.Button(btn_frm, text='❌', width=3,
                   command=lambda: self._remove_tree_row(tree)).pack(side="left", padx=2)
        return tree

    def _build_production_section(self, parent, section_key):
        """Sezione dati produzione."""
        frm = ttk.LabelFrame(parent, text=f'Production Data — {section_key}')
        frm.pack(fill="x", padx=10, pady=5)

        cols = ('process', 'date', 'produced', 'inspected', 'passed', 'failed', 'note')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=5)
        for col, heading, w in [
            ('process', 'Process', 180), ('date', 'Date', 90),
            ('produced', 'Produced', 80), ('inspected', 'Inspected', 80),
            ('passed', 'Pass', 80), ('failed', 'Fail', 80), ('note', 'Note', 150)
        ]:
            tree.heading(col, text=heading)
            tree.column(col, width=w)
        tree.pack(fill="x", padx=5, pady=3)

        btn_frm = ttk.Frame(frm)
        btn_frm.pack(fill="x", padx=5, pady=2)
        ttk.Button(btn_frm, text='➕', width=3,
                   command=lambda: self._add_production_row(tree, section_key)).pack(side="left", padx=2)
        ttk.Button(btn_frm, text='✏️', width=3,
                   command=lambda: self._edit_tree_row(tree, cols)).pack(side="left", padx=2)
        ttk.Button(btn_frm, text='❌', width=3,
                   command=lambda: self._remove_tree_row(tree)).pack(side="left", padx=2)
        return tree

    def _build_coating_section(self, parent, section_key):
        """Sezione coating."""
        frm = ttk.LabelFrame(parent, text=f'Coating — {section_key}')
        frm.pack(fill="x", padx=10, pady=5)

        supplier_var = tk.StringVar()
        date_var = tk.StringVar()
        ttk.Label(frm, text='Furnizor:').grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(frm, textvariable=supplier_var, width=25).grid(row=0, column=1, padx=5)
        ttk.Label(frm, text='Date:').grid(row=0, column=2, padx=10)
        ttk.Entry(frm, textvariable=date_var, width=15).grid(row=0, column=3, padx=5)

        return {'supplier_var': supplier_var, 'date_var': date_var}

    def _build_verification_section(self, parent, section_key):
        """Sezione verifica BOM / FQC."""
        frm = ttk.LabelFrame(parent, text=f'Verification — {section_key}')
        frm.pack(fill="x", padx=10, pady=5)

        cols = ('section_name', 'conform', 'inspected_qty', 'result', 'cq_resp', 'date', 'note')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=4)
        for col, heading, w in [
            ('section_name', 'Section', 130), ('conform', 'Conform', 100),
            ('inspected_qty', 'Insp. Qty', 80), ('result', 'Result', 80),
            ('cq_resp', 'CQ Responsible', 150), ('date', 'Date', 90), ('note', 'Note', 150)
        ]:
            tree.heading(col, text=heading)
            tree.column(col, width=w)
        tree.pack(fill="x", padx=5, pady=3)

        btn_frm = ttk.Frame(frm)
        btn_frm.pack(fill="x", padx=5, pady=2)
        ttk.Button(btn_frm, text='➕', width=3,
                   command=lambda: self._add_verification_row(tree, section_key)).pack(side="left", padx=2)
        ttk.Button(btn_frm, text='✏️', width=3,
                   command=lambda: self._edit_tree_row(tree, cols)).pack(side="left", padx=2)
        ttk.Button(btn_frm, text='❌', width=3,
                   command=lambda: self._remove_tree_row(tree)).pack(side="left", padx=2)
        return tree

    # ================================================================ #
    #  TAB Actions/Rework — always present                              #
    # ================================================================ #
    def _build_tab_actions_rework(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=self.lang.get('cl_tab_actions', '📝 Azioni/Rework'))

        # Actions
        act_frm = ttk.LabelFrame(tab, text='Comentarii / Acțiuni')
        act_frm.pack(fill="both", expand=True, padx=10, pady=5)

        act_cols = ('comment', 'responsible', 'close_date', 'status')
        self.actions_tree = ttk.Treeview(act_frm, columns=act_cols, show='headings', height=6)
        self.actions_tree.heading('comment', text='Comentarii / Acțiuni')
        self.actions_tree.heading('responsible', text='Responsabil')
        self.actions_tree.heading('close_date', text='Data închidere')
        self.actions_tree.heading('status', text='Status')
        self.actions_tree.column('comment', width=350)
        self.actions_tree.column('responsible', width=150)
        self.actions_tree.column('close_date', width=120, anchor="center")
        self.actions_tree.column('status', width=100, anchor="center")
        self.actions_tree.pack(fill="both", expand=True, padx=5, pady=5)

        act_btn = ttk.Frame(act_frm)
        act_btn.pack(fill="x", padx=5, pady=3)
        ttk.Button(act_btn, text='➕', width=3, command=self._add_action).pack(side="left", padx=2)
        ttk.Button(act_btn, text='✏️', width=3,
                   command=lambda: self._edit_tree_row(self.actions_tree, act_cols)).pack(side="left", padx=2)
        ttk.Button(act_btn, text='❌', width=3,
                   command=lambda: self._remove_tree_row(self.actions_tree)).pack(side="left", padx=2)

        # Rework
        rw_frm = ttk.LabelFrame(tab, text='REWORK')
        rw_frm.pack(fill="both", expand=True, padx=10, pady=5)

        rw_cols = ('serial', 'fail_ict', 'fail_fct', 'diagnosis', 'reference', 'rework_resp')
        self.rework_tree = ttk.Treeview(rw_frm, columns=rw_cols, show='headings', height=6)
        self.rework_tree.heading('serial', text='Serial nr.')
        self.rework_tree.heading('fail_ict', text='FAIL ICT')
        self.rework_tree.heading('fail_fct', text='FAIL FCT')
        self.rework_tree.heading('diagnosis', text='Diagnoză')
        self.rework_tree.heading('reference', text='Referință')
        self.rework_tree.heading('rework_resp', text='Rework resp.')
        for c in rw_cols:
            self.rework_tree.column(c, width=120)
        self.rework_tree.pack(fill="both", expand=True, padx=5, pady=5)

        rw_btn = ttk.Frame(rw_frm)
        rw_btn.pack(fill="x", padx=5, pady=3)
        ttk.Button(rw_btn, text='➕', width=3, command=self._add_rework).pack(side="left", padx=2)
        ttk.Button(rw_btn, text='✏️', width=3,
                   command=lambda: self._edit_tree_row(self.rework_tree, rw_cols)).pack(side="left", padx=2)
        ttk.Button(rw_btn, text='❌', width=3,
                   command=lambda: self._remove_tree_row(self.rework_tree)).pack(side="left", padx=2)

    # ================================================================ #
    #  Generic Treeview helpers                                         #
    # ================================================================ #
    def _remove_tree_row(self, tree):
        sel = tree.selection()
        if sel:
            tree.delete(sel[0])

    def _edit_tree_row(self, tree, columns):
        """Apre un dialog per modificare la riga selezionata."""
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0], 'values')

        dlg = tk.Toplevel(self)
        dlg.title('Modifica')
        dlg.geometry("450x" + str(50 + len(columns) * 35))
        dlg.transient(self)
        dlg.grab_set()

        vars_ = {}
        for i, col in enumerate(columns):
            ttk.Label(dlg, text=col.replace('_', ' ').title() + ':').grid(
                row=i, column=0, padx=10, pady=3, sticky="w")
            v = tk.StringVar(value=vals[i] if i < len(vals) else '')
            ttk.Entry(dlg, textvariable=v, width=35).grid(row=i, column=1, padx=5, pady=3)
            vars_[col] = v

        def save():
            tree.item(sel[0], values=tuple(vars_[c].get() for c in columns))
            dlg.destroy()

        ttk.Button(dlg, text='Salva', command=save).grid(
            row=len(columns), column=1, pady=10, sticky="w")

    # ================================================================ #
    #  Add row dialogs                                                  #
    # ================================================================ #
    def _add_program_row(self, tree, section_key):
        self._add_row_dialog(tree, 'Nuovo Programma',
            [('Process Step', 'step'), ('Line nr', 'line_nr'), ('Program name', 'program_name'),
             ('Result (OK/Not OK)', 'result'), ('Responsible', 'responsible'),
             ('Date', 'date'), ('Note', 'note')])

    def _add_material_row(self, tree, section_key):
        self._add_row_dialog(tree, 'Nuovo Materiale',
            [('Material / Tool', 'type'), ('Code / PN', 'code_pn'), ('Note', 'note')])

    def _add_preforming_row(self, tree, section_key):
        self._add_row_dialog(tree, 'Nuovo Check',
            [('Check Item', 'item'), ('Result (OK/Not OK)', 'result'), ('Note', 'note')])

    def _add_production_row(self, tree, section_key):
        self._add_row_dialog(tree, 'Nuovi Dati Produzione',
            [('Process', 'process'), ('Date', 'date'), ('Produced', 'produced'),
             ('Inspected', 'inspected'), ('Pass', 'passed'), ('Fail', 'failed'), ('Note', 'note')])

    def _add_verification_row(self, tree, section_key):
        self._add_row_dialog(tree, 'Nuova Verifica',
            [('Section', 'section_name'), ('Conform/Neconform', 'conform'),
             ('Inspected Qty', 'inspected_qty'), ('Result (OK/NC)', 'result'),
             ('CQ Responsible', 'cq_resp'), ('Date', 'date'), ('Note', 'note')])

    def _add_action(self):
        self._add_row_dialog(self.actions_tree, 'Nuova Azione',
            [('Commento', 'comment'), ('Responsabile', 'responsible'),
             ('Data chiusura', 'close_date'), ('Status', 'status')])

    def _add_rework(self):
        self._add_row_dialog(self.rework_tree, 'Nuovo Rework',
            [('Serial nr', 'serial'), ('FAIL ICT', 'fail_ict'), ('FAIL FCT', 'fail_fct'),
             ('Diagnoză', 'diagnosis'), ('Referință', 'reference'), ('Rework resp', 'rework_resp')])

    def _add_row_dialog(self, tree, title, fields):
        """Dialog generico per aggiungere una riga a un Treeview."""
        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.geometry("450x" + str(60 + len(fields) * 35))
        dlg.transient(self)
        dlg.grab_set()

        vars_ = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(dlg, text=f'{label}:').grid(row=i, column=0, padx=10, pady=3, sticky="w")
            v = tk.StringVar()
            ttk.Entry(dlg, textvariable=v, width=35).grid(row=i, column=1, padx=5, pady=3)
            vars_[key] = v

        def save():
            tree.insert('', 'end', values=tuple(vars_[f[1]].get() for f in fields))
            dlg.destroy()

        ttk.Button(dlg, text='Salva', command=save).grid(
            row=len(fields), column=1, pady=10, sticky="w")

    # ================================================================ #
    #  Session Management                                               #
    # ================================================================ #
    def _load_sessions(self):
        try:
            sessions = self.npi_manager.get_checklist_sessions(self.project_id)
            self._sessions_list = sessions
            display = [f"#{s['session_id']} — {s['check_date']} — {s['status']} ({s['created_by']})"
                       for s in sessions]
            self.session_combo['values'] = display
            if display:
                self.session_combo.current(0)
                self._on_session_selected()
        except Exception as e:
            logger.error(f"Errore caricamento sessioni: {e}", exc_info=True)

    def _on_session_selected(self, event=None):
        idx = self.session_combo.current()
        if idx < 0 or idx >= len(self._sessions_list):
            return
        info = self._sessions_list[idx]
        self._current_session_id = info['session_id']
        self.status_label.configure(text=f"Status: {info['status']}")
        self._load_session_data(self._current_session_id)

    def _load_session_data(self, session_id):
        """Popola tutti i widget con i dati della sessione."""
        try:
            data = self.npi_manager.load_checklist_session(session_id)
            if not data:
                return
            hdr = data['session']

            # Header
            self.pn_var.set(hdr.get('product_code') or self.product_code or '')
            if hdr.get('order_id'):
                for i, o in enumerate(self._orders_cache):
                    if o['order_id'] == hdr['order_id']:
                        self.order_combo.current(i)
                        break
            self.qty_var.set(str(hdr.get('order_qty') or ''))
            if hdr.get('check_date'):
                cd = hdr['check_date']
                self.date_var.set(cd.strftime('%d/%m/%Y') if hasattr(cd, 'strftime') else str(cd))

            self.resp_qualita_var.set(hdr.get('resp_qualita') or '')
            self.resp_produzione_var.set(hdr.get('resp_produzione') or '')
            self.resp_ingegneria_var.set(hdr.get('resp_ingegneria') or '')

            # Dynamic section data
            for section_key, widgets in self._section_widgets.items():
                # Programs
                if 'programs' in widgets:
                    tree = widgets['programs']
                    tree.delete(*tree.get_children())
                    for p in data.get('programs', []):
                        if p.get('section') == section_key:
                            d = p.get('date')
                            ds = d.strftime('%d/%m/%Y') if d and hasattr(d, 'strftime') else (d or '')
                            tree.insert('', 'end', values=(
                                p.get('step', ''), p.get('line_nr', ''), p.get('program_name', ''),
                                p.get('result', ''), p.get('responsible', ''), ds, p.get('note', '')))

                # Materials
                if 'materials' in widgets:
                    tree = widgets['materials']
                    tree.delete(*tree.get_children())
                    for m in data.get('materials', []):
                        if m.get('section') == section_key:
                            tree.insert('', 'end', values=(
                                m.get('type', ''), m.get('code_pn', ''), m.get('note', '')))

                # Preforming
                if 'preforming' in widgets:
                    tree = widgets['preforming']
                    tree.delete(*tree.get_children())
                    for pc in data.get('preforming_checks', []):
                        tree.insert('', 'end', values=(
                            pc.get('item', ''), pc.get('result', ''), pc.get('note', '')))

                # Production data
                if 'production' in widgets:
                    tree = widgets['production']
                    tree.delete(*tree.get_children())
                    for pd in data.get('production_data', []):
                        if pd.get('process', '').startswith(section_key):
                            d = pd.get('date')
                            ds = d.strftime('%d/%m/%Y') if d and hasattr(d, 'strftime') else (d or '')
                            tree.insert('', 'end', values=(
                                pd.get('process', ''), ds,
                                pd.get('produced', ''), pd.get('inspected', ''),
                                pd.get('passed', ''), pd.get('failed', ''), pd.get('note', '')))

                # Verification
                if 'verification' in widgets:
                    tree = widgets['verification']
                    tree.delete(*tree.get_children())
                    for v in data.get('verifications', []):
                        if v.get('section', '').startswith(section_key):
                            d = v.get('date')
                            ds = d.strftime('%d/%m/%Y') if d and hasattr(d, 'strftime') else (d or '')
                            tree.insert('', 'end', values=(
                                v.get('section', ''), v.get('conform', ''),
                                v.get('inspected_qty', ''), v.get('result', ''),
                                v.get('cq_resp', ''), ds, v.get('note', '')))

            # Actions
            self.actions_tree.delete(*self.actions_tree.get_children())
            for a in data.get('actions', []):
                d = a.get('close_date')
                ds = d.strftime('%d/%m/%Y') if d and hasattr(d, 'strftime') else (d or '')
                self.actions_tree.insert('', 'end', values=(
                    a.get('comment', ''), a.get('responsible', ''), ds, a.get('status', '')))

            # Rework
            self.rework_tree.delete(*self.rework_tree.get_children())
            for r in data.get('rework', []):
                self.rework_tree.insert('', 'end', values=(
                    r.get('serial', ''), r.get('fail_ict', ''), r.get('fail_fct', ''),
                    r.get('diagnosis', ''), r.get('reference', ''), r.get('rework_resp', '')))

        except Exception as e:
            logger.error(f"Errore load_session_data: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    # ================================================================ #
    #  Collect data from UI → dict                                      #
    # ================================================================ #
    def _collect_data(self):
        """Raccoglie tutti i dati dall'interfaccia in un dict salvabile."""
        data = {'session': {}, 'programs': [], 'materials': [],
                'production_data': [], 'verifications': [],
                'preforming_checks': [], 'actions': [], 'rework': []}

        # Header
        idx = self.order_combo.current()
        if 0 <= idx < len(self._orders_cache):
            data['session']['order_id'] = self._orders_cache[idx]['order_id']
        data['session']['product_code'] = self.pn_var.get()
        try:
            data['session']['order_qty'] = int(self.qty_var.get()) if self.qty_var.get() else None
        except ValueError:
            data['session']['order_qty'] = None
        try:
            data['session']['check_date'] = datetime.strptime(self.date_var.get(), '%d/%m/%Y')
        except ValueError:
            data['session']['check_date'] = datetime.now()
        data['session']['resp_qualita'] = self.resp_qualita_var.get()
        data['session']['resp_produzione'] = self.resp_produzione_var.get()
        data['session']['resp_ingegneria'] = self.resp_ingegneria_var.get()

        # Dynamic sections
        for section_key, widgets in self._section_widgets.items():
            # Programs
            if 'programs' in widgets:
                tree = widgets['programs']
                for iid in tree.get_children():
                    v = tree.item(iid, 'values')
                    data['programs'].append({
                        'section': section_key, 'step': v[0], 'line_nr': v[1],
                        'program_name': v[2], 'result': v[3], 'responsible': v[4],
                        'date': v[5] or None, 'note': v[6]
                    })

            # Materials
            if 'materials' in widgets:
                tree = widgets['materials']
                for iid in tree.get_children():
                    v = tree.item(iid, 'values')
                    data['materials'].append({
                        'section': section_key, 'type': v[0], 'code_pn': v[1], 'note': v[2]
                    })

            # Preforming checks
            if 'preforming' in widgets:
                tree = widgets['preforming']
                for iid in tree.get_children():
                    v = tree.item(iid, 'values')
                    data['preforming_checks'].append({
                        'item': v[0], 'result': v[1], 'note': v[2]
                    })

            # Production data
            if 'production' in widgets:
                tree = widgets['production']
                for iid in tree.get_children():
                    v = tree.item(iid, 'values')
                    data['production_data'].append({
                        'process': v[0], 'date': v[1] or None,
                        'produced': int(v[2]) if v[2] else None,
                        'inspected': int(v[3]) if v[3] else None,
                        'passed': int(v[4]) if v[4] else None,
                        'failed': int(v[5]) if v[5] else None,
                        'note': v[6]
                    })

            # Verification
            if 'verification' in widgets:
                tree = widgets['verification']
                for iid in tree.get_children():
                    v = tree.item(iid, 'values')
                    data['verifications'].append({
                        'section': v[0], 'conform': v[1],
                        'inspected_qty': int(v[2]) if v[2] else None,
                        'result': v[3], 'cq_resp': v[4],
                        'date': v[5] or None, 'note': v[6]
                    })

        # Actions
        for iid in self.actions_tree.get_children():
            v = self.actions_tree.item(iid, 'values')
            data['actions'].append({
                'comment': v[0], 'responsible': v[1], 'close_date': v[2] or None, 'status': v[3]
            })

        # Rework
        for iid in self.rework_tree.get_children():
            v = self.rework_tree.item(iid, 'values')
            data['rework'].append({
                'serial': v[0], 'fail_ict': v[1], 'fail_fct': v[2],
                'diagnosis': v[3], 'reference': v[4], 'rework_resp': v[5]
            })

        return data

    # ================================================================ #
    #  CRUD Operations                                                  #
    # ================================================================ #
    def _new_session(self):
        try:
            sid = self.npi_manager.create_checklist_session(
                self.project_id, self.logged_in_user, product_code=self.product_code)
            self._load_sessions()
            for i, s in enumerate(self._sessions_list):
                if s['session_id'] == sid:
                    self.session_combo.current(i)
                    self._on_session_selected()
                    break
            messagebox.showinfo(self.lang.get('info', 'Info'),
                                f"Sessione #{sid} creata.", parent=self)
        except Exception as e:
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    def _save_session(self):
        if not self._current_session_id:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   'Selezionare o creare una sessione.', parent=self)
            return
        try:
            data = self._collect_data()
            self.npi_manager.save_checklist_session(
                self._current_session_id, data, self.logged_in_user)
            messagebox.showinfo(self.lang.get('info', 'Info'),
                                self.lang.get('cl_saved', 'Sessione salvata con successo.'), parent=self)
            self._load_sessions()
        except Exception as e:
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    def _delete_session(self):
        if not self._current_session_id:
            return
        if not messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                                    'Eliminare questa sessione?', parent=self):
            return
        try:
            self.npi_manager.delete_checklist_session(
                self._current_session_id, self.logged_in_user)
            self._current_session_id = None
            self._load_sessions()
        except Exception as e:
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    def _approve_session(self):
        if not self._current_session_id:
            return
        if not messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
                                    'Approvare questa checklist? Non sarà più modificabile.', parent=self):
            return
        try:
            data = self._collect_data()
            self.npi_manager.save_checklist_session(
                self._current_session_id, data, self.logged_in_user)
            self.npi_manager.approve_checklist_session(
                self._current_session_id, self.logged_in_user)
            messagebox.showinfo(self.lang.get('info', 'Info'), 'Checklist approvata.', parent=self)
            self._load_sessions()
        except Exception as e:
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)
