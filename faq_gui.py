# -*- coding: utf-8 -*-
"""
faq_gui.py
FAQ system — viewer (public) + management (authorized).

Tables used (Employee.faq schema):
  FaqHeathers   (FaqHeatherId, FaqTitle, DateOut)
  FaqSubTitleS  (FaqSubTitleId, FaqHeatherId, FaqSubTile, NrRow, Dateout, DateSys)
  FaqAnswers    (FaqAnswerId,   FaqSubTitleId, Answer,     Dateout, DateSys)
"""
from __future__ import annotations

import logging
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any

logger = logging.getLogger("TraceabilityRS")


# ─── DB helpers ────────────────────────────────────────────────────────────────

def _q(conn, sql: str, params: tuple = ()) -> list:
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows


def _exec(conn, sql: str, params: tuple = ()) -> None:
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    cur.close()


# ─── Multi-line text dialog ────────────────────────────────────────────────────

class _TextDialog(tk.Toplevel):
    """Simple multi-line text input dialog."""

    def __init__(self, parent, title: str, prompt: str, initial: str = ''):
        super().__init__(parent)
        self.result: str | None = None
        self.title(title)
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text=prompt, anchor='w', wraplength=420,
                 font=('Segoe UI', 9)).pack(fill='x', padx=12, pady=(12, 4))

        self._txt = tk.Text(self, height=6, wrap='word', font=('Segoe UI', 10))
        self._txt.pack(fill='both', expand=True, padx=12, pady=4)
        if initial:
            self._txt.insert('1.0', initial)
        self._txt.focus_set()

        bf = tk.Frame(self)
        bf.pack(fill='x', padx=12, pady=(4, 10))
        tk.Button(bf, text='OK',      command=self._ok,     bg='#2980b9', fg='white',
                  padx=14).pack(side='right', padx=4)
        tk.Button(bf, text='Annulla', command=self.destroy, bg='#95a5a6', fg='white',
                  padx=10).pack(side='right', padx=4)

        self.bind('<Control-Return>', lambda _: self._ok())
        self.update_idletasks()
        self.minsize(460, 220)
        self.wait_window()

    def _ok(self) -> None:
        self.result = self._txt.get('1.0', 'end').rstrip('\n')
        self.destroy()


def _ask_text(parent, title: str, prompt: str, initial: str = '') -> str | None:
    dlg = _TextDialog(parent, title, prompt, initial)
    return dlg.result if dlg.result and dlg.result.strip() else None


# ─── FAQ Viewer (public — no login) ────────────────────────────────────────────

class FaqViewerWindow(tk.Toplevel):
    """Read-only FAQ browser: chapter tree on the left, answers on the right."""

    def __init__(self, parent, db: Any, lang: Any):
        super().__init__(parent)
        self.db   = db
        self.lang = lang
        self.title(lang.get('faq_viewer_title', 'Domande Frequenti — FAQ'))
        self.geometry('860x560')
        self.minsize(640, 400)
        self.resizable(True, True)
        self.transient(parent)
        self._build()
        self._load()

    # ── Layout ─────────────────────────────────────────────────────────────────

    def _build(self) -> None:
        # Header
        hdr = tk.Frame(self, bg='#1f3864', height=50)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr, text='❓  ' + self.lang.get('faq_viewer_title', 'Domande Frequenti — FAQ'),
                 bg='#1f3864', fg='white',
                 font=('Segoe UI', 13, 'bold')).pack(side='left', padx=16, pady=10)

        # Search bar
        sf = tk.Frame(self, bg='#f0f4fa', pady=6)
        sf.pack(fill='x', padx=12)
        tk.Label(sf, text='🔍', bg='#f0f4fa', font=('Segoe UI', 11)).pack(side='left')
        self._search_var = tk.StringVar()
        self._search_var.trace_add('write', lambda *_: self._filter())
        tk.Entry(sf, textvariable=self._search_var, width=40,
                 font=('Segoe UI', 10)).pack(side='left', padx=6)
        tk.Button(sf, text='✕', command=lambda: self._search_var.set(''),
                  bd=0, bg='#f0f4fa', cursor='hand2').pack(side='left')

        # Paned area
        pw = tk.PanedWindow(self, orient='horizontal', sashwidth=6, bg='#c8ccd0')
        pw.pack(fill='both', expand=True, padx=8, pady=6)

        # Left: tree
        lf = tk.Frame(pw, bd=0)
        pw.add(lf, minsize=220)
        tk.Label(lf, text=self.lang.get('faq_chapters', 'Capitoli'),
                 font=('Segoe UI', 9, 'bold'), anchor='w',
                 bg='#e8ecf2', pady=4, padx=6).pack(fill='x')
        self._tree = ttk.Treeview(lf, show='tree', selectmode='browse')
        vsb = ttk.Scrollbar(lf, orient='vertical', command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self._tree.pack(fill='both', expand=True)
        self._tree.bind('<<TreeviewSelect>>', self._on_select)

        # Right: answer panel
        rf = tk.Frame(pw, bd=0)
        pw.add(rf, minsize=340)
        self._subtitle_lbl = tk.Label(rf, text='',
                                       font=('Segoe UI', 10, 'bold'),
                                       wraplength=500, justify='left', anchor='w',
                                       bg='#dce8fb', pady=7, padx=10)
        self._subtitle_lbl.pack(fill='x')

        self._answer_txt = tk.Text(rf, wrap='word', state='disabled',
                                    font=('Segoe UI', 10), bd=0, bg='#fdfdfd',
                                    relief='flat', padx=12, pady=10)
        vsb2 = ttk.Scrollbar(rf, orient='vertical', command=self._answer_txt.yview)
        self._answer_txt.configure(yscrollcommand=vsb2.set)
        vsb2.pack(side='right', fill='y')
        self._answer_txt.pack(fill='both', expand=True)

        # Treeview style
        style = ttk.Style()
        style.configure('Treeview', font=('Segoe UI', 9), rowheight=24)

    # ── Data ───────────────────────────────────────────────────────────────────

    def _load(self) -> None:
        conn = self.db.conn
        self._chapters = _q(conn, """
            SELECT FaqHeatherId, FaqTitle
            FROM Employee.faq.FaqHeathers
            WHERE DateOut IS NULL
            ORDER BY FaqTitle
        """)
        self._subtitles = _q(conn, """
            SELECT FaqSubTitleId, FaqHeatherId, FaqSubTile, NrRow
            FROM Employee.faq.FaqSubTitleS
            WHERE Dateout IS NULL
            ORDER BY FaqHeatherId, NrRow, FaqSubTile
        """)
        self._answers = _q(conn, """
            SELECT FaqAnswerId, FaqSubTitleId, Answer
            FROM Employee.faq.FaqAnswers
            WHERE Dateout IS NULL
            ORDER BY FaqSubTitleId, FaqAnswerId
        """)
        self._populate_tree()

    def _populate_tree(self, filter_text: str = '') -> None:
        self._tree.delete(*self._tree.get_children())
        ft = filter_text.lower().strip()
        for ch_id, ch_title in self._chapters:
            subs = [s for s in self._subtitles if s[1] == ch_id]
            if ft:
                matched = []
                for s in subs:
                    ans_texts = [a[2] or '' for a in self._answers if a[1] == s[0]]
                    if ft in s[2].lower() or any(ft in a.lower() for a in ans_texts):
                        matched.append(s)
                if not matched and ft not in ch_title.lower():
                    continue
                subs = matched if matched else subs

            ch_node = self._tree.insert(
                '', 'end', iid=f'ch_{ch_id}',
                text=f'📂  {ch_title}', open=bool(ft),
                values=(ch_id, 'chapter'),
            )
            for s_id, _, s_title, _ in subs:
                self._tree.insert(
                    ch_node, 'end', iid=f'sub_{s_id}',
                    text=f'    ❓  {s_title}',
                    values=(s_id, 'subtitle'),
                )

    def _filter(self) -> None:
        self._populate_tree(self._search_var.get())

    def _on_select(self, _event=None) -> None:
        sel = self._tree.selection()
        if not sel:
            return
        vals = self._tree.item(sel[0], 'values')
        if not vals or vals[1] != 'subtitle':
            self._subtitle_lbl.config(text='')
            self._answer_txt.configure(state='normal')
            self._answer_txt.delete('1.0', 'end')
            self._answer_txt.configure(state='disabled')
            return

        sub_id    = int(vals[0])
        sub_title = next((s[2] for s in self._subtitles if s[0] == sub_id), '')
        answers   = [a[2] for a in self._answers if a[1] == sub_id and a[2]]

        self._subtitle_lbl.config(text=sub_title)
        self._answer_txt.configure(state='normal')
        self._answer_txt.delete('1.0', 'end')
        if answers:
            for ans in answers:
                self._answer_txt.insert('end', f'{ans}\n\n')
        else:
            self._answer_txt.insert('end',
                self.lang.get('faq_no_answers', 'Nessuna risposta disponibile.'))
        self._answer_txt.configure(state='disabled')


# ─── FAQ Management (authorized) ───────────────────────────────────────────────

class FaqManagementWindow(tk.Toplevel):
    """CRUD management for Chapters → Sub-titles → Answers."""

    def __init__(self, parent, db: Any, lang: Any):
        super().__init__(parent)
        self.db   = db
        self.lang = lang
        self.title(lang.get('faq_mgmt_title', 'Gestione FAQ'))
        self.geometry('920x600')
        self.minsize(720, 460)
        self.resizable(True, True)
        self.transient(parent)
        self._build()
        self._refresh_all()

    # ── Layout ─────────────────────────────────────────────────────────────────

    def _build(self) -> None:
        hdr = tk.Frame(self, bg='#1f3864', height=50)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr, text='⚙️  ' + self.lang.get('faq_mgmt_title', 'Gestione FAQ'),
                 bg='#1f3864', fg='white',
                 font=('Segoe UI', 13, 'bold')).pack(side='left', padx=16, pady=10)

        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=8, pady=8)

        self._tab_ch  = self._build_chapter_tab(nb)
        self._tab_sub = self._build_subtitle_tab(nb)
        self._tab_ans = self._build_answer_tab(nb)

        nb.add(self._tab_ch,  text='  ' + self.lang.get('faq_tab_chapters',  'Capitoli')   + '  ')
        nb.add(self._tab_sub, text='  ' + self.lang.get('faq_tab_subtitles', 'Domande')    + '  ')
        nb.add(self._tab_ans, text='  ' + self.lang.get('faq_tab_answers',   'Risposte')   + '  ')
        nb.bind('<<NotebookTabChanged>>', lambda _: self._refresh_chapter_combos())

    # ── Chapters tab ───────────────────────────────────────────────────────────

    def _build_chapter_tab(self, parent: ttk.Notebook) -> tk.Frame:
        f = tk.Frame(parent)
        self._ch_tree = ttk.Treeview(f, columns=('id', 'title'),
                                      show='headings', selectmode='browse')
        self._ch_tree.heading('id',    text='ID',      anchor='w')
        self._ch_tree.heading('title', text='Capitolo', anchor='w')
        self._ch_tree.column('id',    width=60,  stretch=False)
        self._ch_tree.column('title', stretch=True)
        vsb = ttk.Scrollbar(f, orient='vertical', command=self._ch_tree.yview)
        self._ch_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self._ch_tree.pack(fill='both', expand=True)

        bf = tk.Frame(f)
        bf.pack(fill='x', pady=4, padx=4)
        tk.Button(bf, text='➕  Aggiungi',   command=self._ch_add,
                  bg='#27ae60', fg='white', padx=10).pack(side='left', padx=4)
        tk.Button(bf, text='✏️  Rinomina',   command=self._ch_edit,
                  bg='#2980b9', fg='white', padx=10).pack(side='left', padx=4)
        tk.Button(bf, text='🗑️  Archivia',  command=self._ch_delete,
                  bg='#e74c3c', fg='white', padx=10).pack(side='left', padx=4)
        return f

    def _ch_add(self) -> None:
        title = _ask_text(self,
                          self.lang.get('faq_add_chapter', 'Nuovo Capitolo'),
                          self.lang.get('faq_chapter_title_prompt', 'Titolo del capitolo:'))
        if not title:
            return
        _exec(self.db.conn,
              "INSERT INTO Employee.faq.FaqHeathers (FaqTitle) VALUES (?)",
              (title,))
        self._refresh_chapters()
        self._refresh_chapter_combos()

    def _ch_edit(self) -> None:
        sel = self._ch_tree.selection()
        if not sel:
            return messagebox.showwarning(
                '', self.lang.get('faq_select_chapter', 'Seleziona un capitolo'), parent=self)
        ch_id = int(self._ch_tree.item(sel[0], 'values')[0])
        old   = self._ch_tree.item(sel[0], 'values')[1]
        title = _ask_text(self,
                          self.lang.get('faq_edit_chapter', 'Modifica Capitolo'),
                          self.lang.get('faq_chapter_title_prompt', 'Titolo del capitolo:'),
                          initial=old)
        if not title:
            return
        _exec(self.db.conn,
              "UPDATE Employee.faq.FaqHeathers SET FaqTitle=? WHERE FaqHeatherId=?",
              (title, ch_id))
        self._refresh_chapters()
        self._refresh_chapter_combos()

    def _ch_delete(self) -> None:
        sel = self._ch_tree.selection()
        if not sel:
            return messagebox.showwarning(
                '', self.lang.get('faq_select_chapter', 'Seleziona un capitolo'), parent=self)
        ch_id = int(self._ch_tree.item(sel[0], 'values')[0])
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('faq_archive_confirm',
                          'Archiviare il capitolo e tutto il suo contenuto (domande e risposte)?'),
            parent=self,
        ):
            return
        conn = self.db.conn
        _exec(conn, """
            UPDATE Employee.faq.FaqAnswers
            SET Dateout = GETDATE()
            WHERE Dateout IS NULL
              AND FaqSubTitleId IN (
                  SELECT FaqSubTitleId FROM Employee.faq.FaqSubTitleS WHERE FaqHeatherId = ?
              )
        """, (ch_id,))
        _exec(conn,
              "UPDATE Employee.faq.FaqSubTitleS SET Dateout=GETDATE() "
              "WHERE FaqHeatherId=? AND Dateout IS NULL",
              (ch_id,))
        _exec(conn,
              "UPDATE Employee.faq.FaqHeathers SET DateOut=GETDATE() WHERE FaqHeatherId=?",
              (ch_id,))
        self._refresh_chapters()
        self._refresh_chapter_combos()

    def _refresh_chapters(self) -> None:
        self._chapters = _q(self.db.conn, """
            SELECT FaqHeatherId, FaqTitle
            FROM Employee.faq.FaqHeathers
            WHERE DateOut IS NULL
            ORDER BY FaqTitle
        """)
        for item in self._ch_tree.get_children():
            self._ch_tree.delete(item)
        for ch_id, title in self._chapters:
            self._ch_tree.insert('', 'end', values=(ch_id, title))

    # ── Sub-titles tab ─────────────────────────────────────────────────────────

    def _build_subtitle_tab(self, parent: ttk.Notebook) -> tk.Frame:
        f = tk.Frame(parent)

        ff = tk.Frame(f)
        ff.pack(fill='x', padx=6, pady=4)
        tk.Label(ff, text=self.lang.get('faq_filter_chapter', 'Capitolo:'),
                 font=('Segoe UI', 9)).pack(side='left')
        self._sub_ch_var = tk.StringVar()
        self._sub_ch_cb  = ttk.Combobox(ff, textvariable=self._sub_ch_var,
                                         state='readonly', width=40)
        self._sub_ch_cb.pack(side='left', padx=6)
        self._sub_ch_cb.bind('<<ComboboxSelected>>', lambda _: self._refresh_subtitles())

        self._sub_tree = ttk.Treeview(f, columns=('id', 'row', 'title'),
                                       show='headings', selectmode='browse')
        self._sub_tree.heading('id',    text='ID',   anchor='w')
        self._sub_tree.heading('row',   text='Ord.', anchor='w')
        self._sub_tree.heading('title', text='Domanda / Sottotitolo', anchor='w')
        self._sub_tree.column('id',    width=55,  stretch=False)
        self._sub_tree.column('row',   width=55,  stretch=False)
        self._sub_tree.column('title', stretch=True)
        vsb = ttk.Scrollbar(f, orient='vertical', command=self._sub_tree.yview)
        self._sub_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self._sub_tree.pack(fill='both', expand=True)

        bf = tk.Frame(f)
        bf.pack(fill='x', pady=4, padx=4)
        tk.Button(bf, text='➕  Aggiungi',  command=self._sub_add,
                  bg='#27ae60', fg='white', padx=10).pack(side='left', padx=4)
        tk.Button(bf, text='✏️  Modifica',  command=self._sub_edit,
                  bg='#2980b9', fg='white', padx=10).pack(side='left', padx=4)
        tk.Button(bf, text='🗑️  Archivia', command=self._sub_delete,
                  bg='#e74c3c', fg='white', padx=10).pack(side='left', padx=4)
        return f

    def _sub_add(self) -> None:
        ch_id = self._get_sub_chapter_id()
        if ch_id is None:
            return messagebox.showwarning(
                '', self.lang.get('faq_select_chapter', 'Seleziona prima un capitolo'), parent=self)
        title = _ask_text(self,
                          self.lang.get('faq_add_subtitle', 'Nuova Domanda'),
                          self.lang.get('faq_subtitle_prompt', 'Testo della domanda:'))
        if not title:
            return
        rows = _q(self.db.conn,
                  "SELECT ISNULL(MAX(NrRow),0)+1 "
                  "FROM Employee.faq.FaqSubTitleS WHERE FaqHeatherId=? AND Dateout IS NULL",
                  (ch_id,))
        next_row = rows[0][0] if rows else 1
        _exec(self.db.conn,
              "INSERT INTO Employee.faq.FaqSubTitleS (FaqHeatherId, FaqSubTile, NrRow) VALUES (?,?,?)",
              (ch_id, title, next_row))
        self._refresh_subtitles()
        self._refresh_ans_subtitles()

    def _sub_edit(self) -> None:
        sel = self._sub_tree.selection()
        if not sel:
            return messagebox.showwarning(
                '', self.lang.get('faq_select_subtitle', 'Seleziona una domanda'), parent=self)
        vals  = self._sub_tree.item(sel[0], 'values')
        sub_id, old_title = int(vals[0]), vals[2]
        title = _ask_text(self,
                          self.lang.get('faq_edit_subtitle', 'Modifica Domanda'),
                          self.lang.get('faq_subtitle_prompt', 'Testo della domanda:'),
                          initial=old_title)
        if not title:
            return
        _exec(self.db.conn,
              "UPDATE Employee.faq.FaqSubTitleS SET FaqSubTile=? WHERE FaqSubTitleId=?",
              (title, sub_id))
        self._refresh_subtitles()
        self._refresh_ans_subtitles()

    def _sub_delete(self) -> None:
        sel = self._sub_tree.selection()
        if not sel:
            return messagebox.showwarning(
                '', self.lang.get('faq_select_subtitle', 'Seleziona una domanda'), parent=self)
        sub_id = int(self._sub_tree.item(sel[0], 'values')[0])
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('faq_archive_subtitle_confirm',
                          'Archiviare questa domanda e tutte le sue risposte?'),
            parent=self,
        ):
            return
        _exec(self.db.conn,
              "UPDATE Employee.faq.FaqAnswers SET Dateout=GETDATE() "
              "WHERE FaqSubTitleId=? AND Dateout IS NULL",
              (sub_id,))
        _exec(self.db.conn,
              "UPDATE Employee.faq.FaqSubTitleS SET Dateout=GETDATE() WHERE FaqSubTitleId=?",
              (sub_id,))
        self._refresh_subtitles()
        self._refresh_ans_subtitles()

    def _refresh_subtitles(self) -> None:
        ch_id = self._get_sub_chapter_id()
        for item in self._sub_tree.get_children():
            self._sub_tree.delete(item)
        if ch_id is None:
            return
        subs = _q(self.db.conn, """
            SELECT FaqSubTitleId, NrRow, FaqSubTile
            FROM Employee.faq.FaqSubTitleS
            WHERE FaqHeatherId = ? AND Dateout IS NULL
            ORDER BY NrRow, FaqSubTile
        """, (ch_id,))
        for sub_id, row, title in subs:
            self._sub_tree.insert('', 'end', values=(sub_id, row, title))

    def _get_sub_chapter_id(self) -> int | None:
        val = self._sub_ch_var.get()
        try:
            return int(val.split('—')[0].strip()) if val else None
        except Exception:
            return None

    # ── Answers tab ────────────────────────────────────────────────────────────

    def _build_answer_tab(self, parent: ttk.Notebook) -> tk.Frame:
        f = tk.Frame(parent)

        ff = tk.Frame(f)
        ff.pack(fill='x', padx=6, pady=4)
        tk.Label(ff, text=self.lang.get('faq_filter_chapter', 'Capitolo:'),
                 font=('Segoe UI', 9)).pack(side='left')
        self._ans_ch_var = tk.StringVar()
        self._ans_ch_cb  = ttk.Combobox(ff, textvariable=self._ans_ch_var,
                                         state='readonly', width=28)
        self._ans_ch_cb.pack(side='left', padx=4)
        self._ans_ch_cb.bind('<<ComboboxSelected>>', lambda _: self._refresh_ans_subtitles())

        tk.Label(ff, text='  ' + self.lang.get('faq_question_label', 'Domanda:'),
                 font=('Segoe UI', 9)).pack(side='left')
        self._ans_sub_var = tk.StringVar()
        self._ans_sub_cb  = ttk.Combobox(ff, textvariable=self._ans_sub_var,
                                          state='readonly', width=30)
        self._ans_sub_cb.pack(side='left', padx=4)
        self._ans_sub_cb.bind('<<ComboboxSelected>>', lambda _: self._refresh_answers())

        self._ans_tree = ttk.Treeview(f, columns=('id', 'answer'),
                                       show='headings', selectmode='browse')
        self._ans_tree.heading('id',     text='ID', anchor='w')
        self._ans_tree.heading('answer', text='Risposta', anchor='w')
        self._ans_tree.column('id',     width=55,  stretch=False)
        self._ans_tree.column('answer', stretch=True)
        vsb = ttk.Scrollbar(f, orient='vertical', command=self._ans_tree.yview)
        self._ans_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self._ans_tree.pack(fill='both', expand=True)

        bf = tk.Frame(f)
        bf.pack(fill='x', pady=4, padx=4)
        tk.Button(bf, text='➕  Aggiungi',  command=self._ans_add,
                  bg='#27ae60', fg='white', padx=10).pack(side='left', padx=4)
        tk.Button(bf, text='✏️  Modifica',  command=self._ans_edit,
                  bg='#2980b9', fg='white', padx=10).pack(side='left', padx=4)
        tk.Button(bf, text='🗑️  Archivia', command=self._ans_delete,
                  bg='#e74c3c', fg='white', padx=10).pack(side='left', padx=4)
        return f

    def _ans_add(self) -> None:
        sub_id = self._get_ans_subtitle_id()
        if sub_id is None:
            return messagebox.showwarning(
                '', self.lang.get('faq_select_subtitle', 'Seleziona prima una domanda'), parent=self)
        answer = _ask_text(self,
                           self.lang.get('faq_add_answer', 'Nuova Risposta'),
                           self.lang.get('faq_answer_prompt', 'Testo della risposta:'))
        if not answer:
            return
        _exec(self.db.conn,
              "INSERT INTO Employee.faq.FaqAnswers (FaqSubTitleId, Answer) VALUES (?,?)",
              (sub_id, answer))
        self._refresh_answers()

    def _ans_edit(self) -> None:
        sel = self._ans_tree.selection()
        if not sel:
            return messagebox.showwarning(
                '', self.lang.get('faq_select_answer', 'Seleziona una risposta'), parent=self)
        vals   = self._ans_tree.item(sel[0], 'values')
        ans_id, old = int(vals[0]), vals[1]
        answer = _ask_text(self,
                           self.lang.get('faq_edit_answer', 'Modifica Risposta'),
                           self.lang.get('faq_answer_prompt', 'Testo della risposta:'),
                           initial=old)
        if not answer:
            return
        _exec(self.db.conn,
              "UPDATE Employee.faq.FaqAnswers SET Answer=? WHERE FaqAnswerId=?",
              (answer, ans_id))
        self._refresh_answers()

    def _ans_delete(self) -> None:
        sel = self._ans_tree.selection()
        if not sel:
            return messagebox.showwarning(
                '', self.lang.get('faq_select_answer', 'Seleziona una risposta'), parent=self)
        ans_id = int(self._ans_tree.item(sel[0], 'values')[0])
        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('faq_archive_answer_confirm', 'Archiviare questa risposta?'),
            parent=self,
        ):
            return
        _exec(self.db.conn,
              "UPDATE Employee.faq.FaqAnswers SET Dateout=GETDATE() WHERE FaqAnswerId=?",
              (ans_id,))
        self._refresh_answers()

    def _refresh_ans_subtitles(self) -> None:
        ch_id = self._get_ans_chapter_id()
        self._ans_sub_cb['values'] = []
        self._ans_sub_var.set('')
        if ch_id is None:
            return
        subs = _q(self.db.conn, """
            SELECT FaqSubTitleId, FaqSubTile
            FROM Employee.faq.FaqSubTitleS
            WHERE FaqHeatherId = ? AND Dateout IS NULL
            ORDER BY NrRow, FaqSubTile
        """, (ch_id,))
        self._ans_sub_cb['values'] = [f'{s[0]} — {s[1]}' for s in subs]

    def _refresh_answers(self) -> None:
        sub_id = self._get_ans_subtitle_id()
        for item in self._ans_tree.get_children():
            self._ans_tree.delete(item)
        if sub_id is None:
            return
        answers = _q(self.db.conn, """
            SELECT FaqAnswerId, Answer
            FROM Employee.faq.FaqAnswers
            WHERE FaqSubTitleId = ? AND Dateout IS NULL
            ORDER BY FaqAnswerId
        """, (sub_id,))
        for ans_id, text in answers:
            self._ans_tree.insert('', 'end', values=(ans_id, text or ''))

    def _get_ans_chapter_id(self) -> int | None:
        val = self._ans_ch_var.get()
        try:
            return int(val.split('—')[0].strip()) if val else None
        except Exception:
            return None

    def _get_ans_subtitle_id(self) -> int | None:
        val = self._ans_sub_var.get()
        try:
            return int(val.split('—')[0].strip()) if val else None
        except Exception:
            return None

    # ── Global refresh ─────────────────────────────────────────────────────────

    def _refresh_all(self) -> None:
        self._refresh_chapters()
        self._refresh_chapter_combos()

    def _refresh_chapter_combos(self) -> None:
        chapters = _q(self.db.conn, """
            SELECT FaqHeatherId, FaqTitle
            FROM Employee.faq.FaqHeathers
            WHERE DateOut IS NULL ORDER BY FaqTitle
        """)
        labels = [f'{r[0]} — {r[1]}' for r in chapters]
        self._sub_ch_cb['values'] = labels
        self._ans_ch_cb['values'] = labels


# ─── Public entry points ────────────────────────────────────────────────────────

def open_faq_viewer(parent: Any, db: Any, lang: Any) -> None:
    """Open the read-only FAQ viewer (no login required)."""
    try:
        FaqViewerWindow(parent, db, lang).focus_set()
    except Exception as e:
        logger.error(f"open_faq_viewer: {e}", exc_info=True)
        messagebox.showerror(lang.get('error', 'Errore'), str(e), parent=parent)


def open_faq_management(parent: Any, db: Any, lang: Any) -> None:
    """Open the FAQ management window (requires prior authorization)."""
    try:
        FaqManagementWindow(parent, db, lang).focus_set()
    except Exception as e:
        logger.error(f"open_faq_management: {e}", exc_info=True)
        messagebox.showerror(lang.get('error', 'Errore'), str(e), parent=parent)
