"""
update_dialog.py
Dialogo professionale per la notifica aggiornamenti.

Riferimento: finestra moderna con logo aziendale in alto a sinistra,
freccia verde in cerchio, versioni corrente/nuova, link "Novità",
bottoni Download e Skip Later (nascosto se aggiornamento obbligatorio).
"""
import logging
import os
import tkinter as tk
from tkinter import ttk, font as tkfont
from datetime import datetime
from typing import Callable, Optional

try:
    from PIL import Image, ImageTk
    _HAS_PIL = True
except Exception:
    _HAS_PIL = False

logger = logging.getLogger(__name__)

DEFAULT_LOGO_PATHS = [
    "assets/logo_gtmc_green.png",
    "assets/logo_gtmc_green.jpg",
    "docs/logo_gtmc_green.png",
    "docs/logo_gtmc_green.jpg",
]


class UpdateDialog:
    """Dialogo di notifica aggiornamento."""

    def __init__(self, parent, lang, current_version: str, new_version: str,
                 whatsnew: Optional[str] = None, mandatory: bool = False,
                 countdown_seconds: int = 60,
                 on_download: Optional[Callable] = None,
                 on_skip: Optional[Callable] = None,
                 logo_path: Optional[str] = None,
                 ready: bool = False):
        self.parent = parent
        self.lang = lang
        self.current_version = current_version
        self.new_version = new_version
        self.whatsnew = whatsnew
        self.mandatory = mandatory
        self.countdown_seconds = countdown_seconds
        self.on_download = on_download
        self.on_skip = on_skip
        self.logo_path = logo_path
        self.ready = ready

        self.result = None
        self._tick_job = None
        self._remaining = countdown_seconds

        self._build()

    def _build(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.lang.get('update_ready_title', 'Aggiornamento Pronto'))
        self.dialog.resizable(False, False)
        self.dialog.configure(bg='#E8EAF6')

        # Frame principale con padding generoso
        main = tk.Frame(self.dialog, bg='#E8EAF6', padx=32, pady=24)
        main.pack(fill=tk.BOTH, expand=True)

        # Logo in alto a sinistra (sopra la freccia)
        self._load_logo(main)

        # Spazio
        tk.Frame(main, height=10, bg='#E8EAF6').pack()

        # Icona: cerchio verde con freccia bianca verso l'alto
        self._draw_arrow_icon(main)

        # Spazio
        tk.Frame(main, height=16, bg='#E8EAF6').pack()

        # Titolo
        title_key = 'update_ready_title' if self.ready else 'update_new_version_title'
        title_default = 'Nuova versione pronta!' if self.ready else 'New version is available!'
        title = tk.Label(
            main,
            text=self.lang.get(title_key, title_default),
            bg='#E8EAF6',
            fg='#1A237E',
            font=('Segoe UI', 16, 'bold')
        )
        title.pack()

        # Versioni
        versions = tk.Frame(main, bg='#E8EAF6')
        versions.pack(pady=(12, 6))
        tk.Label(versions, text=self.lang.get('update_current_version', 'Current version:'),
                 bg='#E8EAF6', fg='#37474F', font=('Segoe UI', 10)).grid(row=0, column=0, sticky='e')
        tk.Label(versions, text=self.current_version,
                 bg='#E8EAF6', fg='#37474F', font=('Segoe UI', 10, 'bold')).grid(row=0, column=1, sticky='w', padx=(6, 0))
        tk.Label(versions, text=self.lang.get('update_new_version', 'New version:'),
                 bg='#E8EAF6', fg='#37474F', font=('Segoe UI', 10)).grid(row=1, column=0, sticky='e', pady=(4, 0))
        tk.Label(versions, text=self.new_version,
                 bg='#E8EAF6', fg='#2E7D32', font=('Segoe UI', 10, 'bold')).grid(row=1, column=1, sticky='w', padx=(6, 0), pady=(4, 0))

        # Countdown (piccolo, sotto le versioni) — nascosto se già pronto
        if self.ready:
            ready_msg = self.lang.get('update_ready_msg',
                                      'Tutto pronto: premi "Installa ora" per aggiornare.')
        else:
            ready_msg = self._countdown_text(self._remaining)
        self.countdown_lbl = tk.Label(
            main,
            text=ready_msg,
            bg='#E8EAF6',
            fg='#546E7A',
            font=('Segoe UI', 9)
        )
        self.countdown_lbl.pack(pady=(6, 0))

        # Link "Novità" / What's New
        if self.whatsnew:
            whatsnew_lbl = tk.Label(
                main,
                text=self.lang.get('update_whatsnew_link', "What's New?"),
                bg='#E8EAF6',
                fg='#1565C0',
                cursor='hand2',
                font=('Segoe UI', 10, 'underline')
            )
            whatsnew_lbl.pack(pady=(14, 0))
            whatsnew_lbl.bind('<Button-1>', lambda e: self._show_whatsnew())

        # Spazio elastico
        tk.Frame(main, bg='#E8EAF6').pack(fill=tk.BOTH, expand=True)

        # Bottoni
        btn_frame = tk.Frame(main, bg='#E8EAF6')
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        # Download / Installa ora button (stile primario, a sinistra)
        btn_text = self.lang.get('update_install_now_btn', 'Installa ora') \
            if self.ready else self.lang.get('update_download_btn', 'Download')
        download_btn = tk.Button(
            btn_frame,
            text=btn_text,
            bg='#4CAF50',
            fg='white',
            activebackground='#388E3C',
            activeforeground='white',
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self._on_download
        )
        download_btn.pack(side=tk.LEFT)

        # Skip Later button (a destra, nascosto se obbligatorio)
        if not self.mandatory:
            skip_btn = tk.Button(
                btn_frame,
                text=self.lang.get('update_skip_later_btn', 'Skip Later'),
                bg='#CFD8DC',
                fg='#37474F',
                activebackground='#B0BEC5',
                activeforeground='#37474F',
                font=('Segoe UI', 10),
                relief=tk.FLAT,
                padx=20,
                pady=8,
                cursor='hand2',
                command=self._on_skip
            )
            skip_btn.pack(side=tk.RIGHT)

        # Se obbligatorio, la X non chiude la finestra
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)

        # Centra e metti in primo piano
        self.dialog.update_idletasks()
        w = 460
        h = 520
        sw = self.dialog.winfo_screenwidth()
        sh = self.dialog.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.dialog.geometry(f"{w}x{h}+{x}+{y}")
        self.dialog.lift()
        self.dialog.attributes('-topmost', True)
        try:
            self.dialog.focus_force()
        except Exception:
            pass

        # Mantieni in primo piano
        self._keep_on_top()

        # Avvia countdown solo se non è già pronto
        if not self.ready:
            self._schedule_tick()

    def _load_logo(self, parent):
        """Carica il logo dell'azienda in alto a sinistra."""
        paths = []
        if self.logo_path:
            paths.append(self.logo_path)
        paths.extend(DEFAULT_LOGO_PATHS)

        for p in paths:
            if not os.path.isfile(p):
                continue
            try:
                if not _HAS_PIL:
                    logger.warning("PIL non disponibile, impossibile caricare il logo.")
                    break
                img = Image.open(p)
                # Ridimensiona mantenendo aspect ratio, max 220x70
                img.thumbnail((220, 70), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(parent, image=photo, bg='#E8EAF6')
                lbl.image = photo  # keep reference
                lbl.pack(anchor='nw')
                logger.info("Logo update dialog caricato: %s", p)
                return
            except Exception as e:
                logger.warning("Errore caricamento logo %s: %s", p, e)

        # Fallback: testo se nessun logo trovato
        tk.Label(parent, text=self.lang.get('update_logo_missing', ''),
                 bg='#E8EAF6', fg='#1A237E', font=('Segoe UI', 12, 'bold')).pack(anchor='nw')

    def _draw_arrow_icon(self, parent):
        """Disegna il cerchio verde con freccia bianca verso l'alto."""
        size = 96
        canvas = tk.Canvas(parent, width=size, height=size, bg='#E8EAF6',
                           highlightthickness=0)
        canvas.pack()

        pad = 4
        # Cerchio verde
        canvas.create_oval(pad, pad, size - pad, size - pad,
                           fill='#4CAF50', outline='#388E3C', width=2)

        # Freccia bianca verso l'alto (stile "upload")
        cx = size // 2
        head_w = 28
        head_h = 24
        shaft_w = 10
        shaft_h = 36
        top_y = 22
        bottom_y = top_y + head_h + shaft_h

        # Punta della freccia (triangolo)
        points = [
            cx, top_y,
            cx - head_w // 2, top_y + head_h,
            cx + head_w // 2, top_y + head_h,
        ]
        canvas.create_polygon(points, fill='white', outline='white')
        # Asta della freccia
        canvas.create_rectangle(cx - shaft_w // 2, top_y + head_h,
                                cx + shaft_w // 2, bottom_y,
                                fill='white', outline='white')

    def _countdown_text(self, seconds: int) -> str:
        m, s = divmod(max(0, seconds), 60)
        time_str = f"{m:02d}:{s:02d}"
        base = self.lang.get(
            'update_countdown_msg',
            "L'aggiornamento partirà automaticamente tra {0}."
        )
        try:
            return base.format(time_str)
        except Exception:
            return base

    def _schedule_tick(self):
        if self._tick_job is not None:
            return
        self._tick_job = self.parent.after(1000, self._tick)

    def _tick(self):
        self._tick_job = None
        if not self.dialog.winfo_exists():
            return
        self._remaining -= 1
        self.countdown_lbl.config(text=self._countdown_text(self._remaining))
        if self._remaining <= 0:
            self._on_download()
            return
        self._schedule_tick()

    def _keep_on_top(self):
        if not self.dialog.winfo_exists():
            return
        try:
            self.dialog.lift()
            self.dialog.attributes('-topmost', True)
        except Exception:
            return
        self.dialog.after(1500, self._keep_on_top)

    def _show_whatsnew(self):
        if not self.whatsnew:
            return
        # Mostra le novità in una piccola finestra di testo
        dlg = tk.Toplevel(self.dialog)
        dlg.title(self.lang.get('update_whatsnew_title', 'Novità della versione'))
        dlg.geometry("520x360")
        dlg.transient(self.dialog)
        dlg.grab_set()
        text = tk.Text(dlg, wrap='word', padx=10, pady=10, font=('Segoe UI', 10))
        text.insert('1.0', self.whatsnew)
        text.config(state='disabled')
        text.pack(fill=tk.BOTH, expand=True)
        ttk.Button(dlg, text=self.lang.get('close', 'Chiudi'), command=dlg.destroy).pack(pady=8)

    def _on_download(self):
        self.result = 'download'
        self._close()

    def _on_skip(self):
        self.result = 'skip'
        self._close()

    def _on_close(self):
        if self.mandatory:
            # Se obbligatorio, la X non chiude e non fa nulla
            return
        self.result = 'skip'
        self._close()

    def _close(self):
        if self._tick_job is not None:
            try:
                self.parent.after_cancel(self._tick_job)
            except Exception:
                pass
            self._tick_job = None
        try:
            self.dialog.destroy()
        except Exception:
            pass

    def show(self) -> str:
        """Mostra il dialogo modale e ritorna 'download' o 'skip'."""
        self.dialog.wait_window()
        return self.result or 'skip'


def show_update_dialog(parent, lang, current_version: str, new_version: str,
                       whatsnew: Optional[str] = None, mandatory: bool = False,
                       countdown_seconds: int = 60,
                       on_download: Optional[Callable] = None,
                       on_skip: Optional[Callable] = None,
                       logo_path: Optional[str] = None,
                       ready: bool = False) -> str:
    """Funzione di comodo per mostrare il dialogo."""
    dlg = UpdateDialog(parent, lang, current_version, new_version,
                       whatsnew, mandatory, countdown_seconds,
                       on_download, on_skip, logo_path, ready)
    return dlg.show()
