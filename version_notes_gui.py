# -*- coding: utf-8 -*-
"""
version_notes_gui.py — Registro modifiche (changelog) per versione.

- Viewer LIFO: elenco cronologico inverso delle sintesi salvate in
  traceability_rs.dbo.VersionDMLogs, consultabile da Help e dalla form About.
- Editor (sotto autorizzazione): NON e' il programmatore a scrivere le note; una
  BOZZA viene generata automaticamente dai commit git tramite il modello Ollama
  locale (riusa touchup_ai.chat) e proposta al programmatore, che la rivede e
  salva.
- Popup "Novita'": mostrato una volta al primo avvio dopo un aggiornamento.

Le note vengono salvate/lette con i metodi Database.add_version_dm_log /
fetch_version_dm_logs / fetch_version_dm_log_summary.
"""
import logging
import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

logger = logging.getLogger("GTMC_DocumentManagement")


# ─── Git + AI (bozza) ────────────────────────────────────────────────────────

def _read_repo_setting(db):
    """Percorso del repo git da Settings['Sys_versionnotes_repo'] (opzionale).
    Utile quando l'app gira dall'exe installato (dove __file__ NON è il repo)."""
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT [Value] FROM traceability_rs.dbo.Settings WHERE [Atribute] = ?",
                    ('Sys_versionnotes_repo',))
        row = cur.fetchone()
        cur.close()
        if row and row[0] and str(row[0]).strip():
            return str(row[0]).strip()
    except Exception as e:
        logger.warning(f"version_notes: lettura Sys_versionnotes_repo: {e}")
    return None


def _is_git_worktree(path):
    """True se `path` è dentro una working tree git."""
    if not path or not os.path.isdir(path):
        return False
    try:
        out = subprocess.run(['git', '-C', path, 'rev-parse', '--is-inside-work-tree'],
                             capture_output=True, text=True, timeout=10)
        return out.returncode == 0 and 'true' in (out.stdout or '').lower()
    except Exception:
        return False


def resolve_git_repo(db=None):
    """Individua la working tree git da usare per le note. Prova, in ordine:
    Settings['Sys_versionnotes_repo'], la cartella del modulo, la CWD e (se
    frozen) la cartella dell'exe; per ognuna risale fino a 6 livelli cercando un
    repo git valido. Ritorna il percorso o None."""
    candidates = []
    if db is not None:
        s = _read_repo_setting(db)
        if s:
            candidates.append(s)
    candidates.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        candidates.append(os.getcwd())
    except Exception:
        pass
    if getattr(sys, 'frozen', False):
        candidates.append(os.path.dirname(sys.executable))

    seen = set()
    for base in candidates:
        d = base
        for _ in range(6):
            if not d or d in seen:
                break
            seen.add(d)
            if _is_git_worktree(d):
                return d
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
    return None


def get_recent_commits(repo, since_date=None, max_count=80):
    """Messaggi commit git ('YYYY-MM-DD | soggetto') dalla working tree `repo`,
    opzionalmente da `since_date`. Ritorna [] se il repo è None o git fallisce."""
    if not repo:
        return []
    cmd = ['git', '-C', repo, 'log', '--no-merges',
           f'--max-count={int(max_count)}', '--date=short', '--pretty=format:%ad | %s']
    if since_date:
        cmd.append(f'--since={since_date}')
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=15,
                             encoding='utf-8', errors='replace')
        if out.returncode != 0:
            logger.warning(f"version_notes: git log rc={out.returncode}: {(out.stderr or '')[:200]}")
            return []
        return [ln.strip() for ln in (out.stdout or '').splitlines() if ln.strip()]
    except Exception as e:
        logger.warning(f"version_notes: git non disponibile: {e}")
        return []


def generate_ai_draft(db, version, commits):
    """Genera una bozza user-facing (italiano) dai commit via Ollama locale.
    Solleva RuntimeError se il modello non e' raggiungibile."""
    import touchup_ai
    url, model = touchup_ai.get_config(db.conn)
    commit_block = "\n".join(f"- {c}" for c in commits) if commits else "(nessun commit trovato)"
    system = (
        "Sei un assistente che scrive note di rilascio (changelog) brevi e chiare "
        "per gli utenti finali NON tecnici di un gestionale di produzione. "
        "Dato l'elenco dei commit git, produci una sintesi in ITALIANO, come elenco "
        "puntato, di cosa e' stato AGGIUNTO o MODIFICATO dal punto di vista "
        "dell'utente. Ignora dettagli tecnici, refactor e fix interni minori. "
        "Massimo 8 punti, frasi brevi e concrete. Non inventare funzionalita' non "
        "presenti nei commit.")
    user = (
        f"Versione: {version}\n\n"
        f"Commit dall'ultima versione:\n{commit_block}\n\n"
        "Scrivi la sintesi delle novita' (solo elenco puntato, in italiano).")
    return touchup_ai.chat(system, user, url=url, model=model, timeout=180)


# ─── Viewer LIFO ─────────────────────────────────────────────────────────────

class VersionNotesViewer(tk.Toplevel):
    def __init__(self, master, db, lang, name_program):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.name_program = name_program
        L = self.lang.get
        self.title(L('vn_viewer_title', 'Registro modifiche — Novità'))
        self.geometry('820x560')
        self.minsize(640, 460)
        self.transient(master)
        self._build_ui()
        self._load()
        self.grab_set()

    def _build_ui(self):
        L = self.lang.get
        hdr = tk.Frame(self, bg='#1F3864')
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text=L('vn_viewer_title', 'Registro modifiche — Novità'),
                 bg='#1F3864', fg='white', font=('Helvetica', 13, 'bold')).pack(
            side=tk.LEFT, padx=12, pady=10)

        paned = ttk.Panedwindow(self, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        top = ttk.Frame(paned)
        cols = ('version', 'date', 'author')
        self._tree = ttk.Treeview(top, columns=cols, show='headings', height=8, selectmode='browse')
        self._tree.heading('version', text=L('vn_col_version', 'Versione'))
        self._tree.heading('date', text=L('vn_col_date', 'Data'))
        self._tree.heading('author', text=L('vn_col_author', 'Autore'))
        self._tree.column('version', width=110, anchor='center')
        self._tree.column('date', width=140, anchor='center')
        self._tree.column('author', width=180, anchor='w')
        vsb = ttk.Scrollbar(top, orient='vertical', command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side='left', fill=tk.BOTH, expand=True)
        vsb.pack(side='right', fill='y')
        self._tree.bind('<<TreeviewSelect>>', self._on_select)
        paned.add(top, weight=1)

        bottom = ttk.LabelFrame(paned, text=L('vn_detail', 'Dettaglio'))
        self._txt = tk.Text(bottom, wrap='word', font=('Segoe UI', 10), state='disabled')
        self._txt.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        paned.add(bottom, weight=1)

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Button(bar, text=L('btn_close', 'Chiudi'), command=self.destroy).pack(side=tk.RIGHT)

    def _load(self):
        self._rows = self.db.fetch_version_dm_logs(self.name_program)
        for it in self._tree.get_children():
            self._tree.delete(it)
        for i, r in enumerate(self._rows):
            dt = r.CreatedAt.strftime('%d/%m/%Y %H:%M') if getattr(r, 'CreatedAt', None) else ''
            self._tree.insert('', tk.END, iid=str(i),
                              values=(r.Version or '', dt, r.CreatedBy or ''))
        if self._rows:
            self._tree.selection_set('0')
            self._show_detail(0)
        else:
            self._set_detail(self.lang.get('vn_empty', 'Nessuna nota disponibile.'))

    def _on_select(self, _e=None):
        sel = self._tree.selection()
        if sel:
            self._show_detail(int(sel[0]))

    def _show_detail(self, idx):
        r = self._rows[idx]
        header = f"{self.lang.get('vn_col_version', 'Versione')} {r.Version}\n" + ("─" * 40) + "\n\n"
        self._set_detail(header + (r.Summary or ''))

    def _set_detail(self, text):
        self._txt.config(state='normal')
        self._txt.delete('1.0', 'end')
        self._txt.insert('1.0', text)
        self._txt.config(state='disabled')


# ─── Editor (bozza AI + salvataggio) ─────────────────────────────────────────

class VersionNotesEditor(tk.Toplevel):
    def __init__(self, master, db, lang, user_name, name_program, current_version):
        super().__init__(master)
        self.db = db
        self.lang = lang
        self.user_name = user_name or 'N/A'
        self.name_program = name_program
        L = self.lang.get
        self.title(L('vn_editor_title', 'Note di versione — bozza AI'))
        self.geometry('760x600')
        self.minsize(620, 520)
        self.transient(master)
        self._build_ui(current_version)
        self.grab_set()
        # Genera automaticamente la bozza all'apertura
        self.after(200, self._generate)

    def _build_ui(self, current_version):
        L = self.lang.get
        top = ttk.Frame(self, padding=12)
        top.pack(fill=tk.BOTH, expand=True)

        row = ttk.Frame(top)
        row.pack(fill=tk.X)
        ttk.Label(row, text=L('vn_version', 'Versione:')).pack(side=tk.LEFT)
        self._v_version = tk.StringVar(value=current_version or '')
        ttk.Entry(row, textvariable=self._v_version, width=16).pack(side=tk.LEFT, padx=(6, 16))
        self._btn_gen = ttk.Button(row, text=L('vn_regen', '🔄 Rigenera bozza (AI da git)'),
                                   command=self._generate)
        self._btn_gen.pack(side=tk.LEFT)

        ttk.Label(top, foreground='#777', wraplength=700, justify='left',
                  text=L('vn_editor_hint',
                         'La bozza è generata automaticamente dai commit git tramite AI locale. '
                         'Rivedila e correggila prima di salvare: sarà mostrata agli utenti.')
                  ).pack(anchor='w', pady=(10, 4))

        self._txt = tk.Text(top, wrap='word', font=('Segoe UI', 10), height=18)
        self._txt.pack(fill=tk.BOTH, expand=True)

        self._status = tk.Label(top, text='', anchor='w', fg='#555')
        self._status.pack(fill=tk.X, pady=(6, 0))

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=12, pady=10)
        self._btn_save = ttk.Button(bar, text=L('vn_save', '💾 Salva note'), command=self._save)
        self._btn_save.pack(side=tk.LEFT)
        ttk.Button(bar, text=L('btn_close', 'Chiudi'), command=self.destroy).pack(side=tk.RIGHT)

    def _set_status(self, text, error=False):
        self._status.config(text=text, fg='#B71C1C' if error else '#2E7D32')

    def _set_text(self, text):
        self._txt.delete('1.0', 'end')
        self._txt.insert('1.0', text)

    def _generate(self):
        L = self.lang.get
        self._btn_gen.config(state='disabled')
        self._set_status(L('vn_generating', 'Generazione bozza in corso (git + AI locale)...'))

        # since = data dell'ultima nota salvata, per riepilogare solo i commit nuovi
        since = None
        try:
            last = self.db.fetch_version_dm_logs(self.name_program, limit=1)
            if last and getattr(last[0], 'CreatedAt', None):
                since = last[0].CreatedAt.strftime('%Y-%m-%d')
        except Exception:
            pass
        version = self._v_version.get().strip()

        def worker():
            try:
                repo = resolve_git_repo(self.db)
                if not repo:
                    warn = L('vn_no_repo',
                             'Repository git non trovato. Se l\'app gira dall\'exe installato, '
                             'impostare in Settings la chiave "Sys_versionnotes_repo" col percorso '
                             'della cartella del codice sorgente. In alternativa scrivere le note a mano.')
                    self.after(0, lambda: self._done_gen(None, warn, is_warn=True))
                    return

                # Prima con filtro data (solo commit nuovi); se vuoto, ritenta senza filtro.
                commits = get_recent_commits(repo, since_date=since, max_count=80)
                if not commits:
                    commits = get_recent_commits(repo, since_date=None, max_count=40)
                if not commits:
                    warn = L('vn_no_commits',
                             'Nessun commit trovato nel repository ({0}). Verificare che git '
                             'sia disponibile e che il repo contenga cronologia.').format(repo)
                    self.after(0, lambda: self._done_gen(None, warn, is_warn=True))
                    return

                draft = generate_ai_draft(self.db, version, commits)
                self.after(0, lambda: self._done_gen(draft, None))
            except Exception as e:
                emsg = str(e)
                # Fallback: proponi comunque i commit grezzi come bozza da rivedere
                try:
                    repo = resolve_git_repo(self.db)
                    raw = get_recent_commits(repo, since_date=since) or get_recent_commits(repo)
                except Exception:
                    raw = []
                fallback = "\n".join(f"- {c}" for c in raw)
                self.after(0, lambda: self._done_gen(
                    fallback or None,
                    L('vn_ai_err', 'AI non disponibile: {0}\nProposti i commit grezzi da rivedere.')
                    .format(emsg), is_warn=True))

        threading.Thread(target=worker, daemon=True).start()

    def _done_gen(self, draft, message, is_warn=False):
        if not self.winfo_exists():
            return
        self._btn_gen.config(state='normal')
        if draft:
            self._set_text(draft)
        if message:
            self._set_status(message, error=is_warn)
        else:
            self._set_status(self.lang.get('vn_gen_ok', 'Bozza generata. Rivedere e salvare.'))

    def _save(self):
        L = self.lang.get
        version = self._v_version.get().strip()
        summary = self._txt.get('1.0', 'end').strip()
        if not version:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('vn_need_version', 'Inserire la versione.'), parent=self)
            return
        if not summary:
            messagebox.showwarning(L('warning', 'Attenzione'),
                                   L('vn_need_summary', 'La sintesi è vuota.'), parent=self)
            return
        if self.db.add_version_dm_log(self.name_program, version, summary, self.user_name):
            messagebox.showinfo(L('success', 'Fatto'),
                                L('vn_saved', 'Note salvate per la versione {0}.').format(version),
                                parent=self)
            self.destroy()
        else:
            messagebox.showerror(L('error', 'Errore'),
                                 L('vn_save_err', 'Salvataggio note fallito.'), parent=self)


# ─── Popup "Novità" (una volta dopo l'update) ────────────────────────────────

def show_version_summary_popup(master, lang, version, summary):
    """Mostra la sintesi novità della versione appena installata."""
    L = lang.get
    dlg = tk.Toplevel(master)
    dlg.title(L('vn_whatsnew_title', 'Novità di questa versione'))
    dlg.geometry('620x460')
    dlg.transient(master)
    try:
        dlg.grab_set()
    except Exception:
        pass

    hdr = tk.Frame(dlg, bg='#1F3864')
    hdr.pack(fill=tk.X)
    tk.Label(hdr, text=f"🎉 {L('vn_whatsnew_header', 'Novità')} — v{version}",
             bg='#1F3864', fg='white', font=('Helvetica', 13, 'bold')).pack(
        side=tk.LEFT, padx=12, pady=10)

    frame = ttk.Frame(dlg, padding=12)
    frame.pack(fill=tk.BOTH, expand=True)
    txt = tk.Text(frame, wrap='word', font=('Segoe UI', 10))
    txt.pack(fill=tk.BOTH, expand=True)
    txt.insert('1.0', summary or '')
    txt.config(state='disabled')

    ttk.Button(dlg, text=L('btn_close', 'Chiudi'), command=dlg.destroy).pack(pady=(0, 10))
    dlg.lift()
    dlg.attributes('-topmost', True)
    dlg.after(300, lambda: dlg.attributes('-topmost', False))


def open_version_notes_viewer(master, db, lang, name_program):
    """Entry point: viewer LIFO del registro modifiche."""
    VersionNotesViewer(master, db, lang, name_program)


def open_version_notes_editor(master, db, lang, user_name, name_program, current_version):
    """Entry point: editor con bozza AI da git."""
    VersionNotesEditor(master, db, lang, user_name, name_program, current_version)
