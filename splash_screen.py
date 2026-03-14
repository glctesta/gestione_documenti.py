"""
splash_screen.py
Splash screen per TraceabilityRS.
Appare immediatamente all'avvio, mostra logo + barra di progresso
mentre i moduli pesanti vengono caricati in background.
"""

import tkinter as tk
from tkinter import ttk
import threading
import os
import sys


# ── Colori app ────────────────────────────────────────────────────────────────
BG_COLOR      = "#1e2a3a"   # sfondo scuro blu-notte
ACCENT_COLOR  = "#4fc3f7"   # azzurro chiaro
TEXT_COLOR    = "#e0f7fa"   # bianco-azzurro
BAR_COLOR     = "#4fc3f7"   # barra progresso
TROUGH_COLOR  = "#2c3e50"   # sfondo barra
TITLE_COLOR   = "#ffffff"   # bianco puro per titolo


def _resource_path(relative_path: str) -> str:
    """Restituisce il percorso assoluto di una risorsa (compatibile con PyInstaller)."""
    base = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)


class SplashScreen:
    """
    Splash screen thread-safe.

    Uso:
        splash = SplashScreen(root)          # root = tk.Tk() nascosta
        splash.update_progress(30, "Caricamento...")
        splash.close()
    """

    WIDTH  = 520
    HEIGHT = 320

    def __init__(self, root: tk.Tk):
        self._root = root
        self._lock = threading.Lock()
        self._closed = False

        # ── Crea la finestra splash ───────────────────────────────────────────
        self._win = tk.Toplevel(root)
        self._win.overrideredirect(True)          # niente bordi / barra titolo
        self._win.configure(bg=BG_COLOR)
        self._win.attributes("-topmost", True)    # sempre in primo piano
        self._win.resizable(False, False)

        # Centra sullo schermo
        sw = self._win.winfo_screenwidth()
        sh = self._win.winfo_screenheight()
        x  = (sw - self.WIDTH)  // 2
        y  = (sh - self.HEIGHT) // 2
        self._win.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

        # ── Layout ────────────────────────────────────────────────────────────
        self._build_ui()

        # Forza rendering immediato
        self._win.update()

    # ── Costruzione UI ────────────────────────────────────────────────────────

    def _build_ui(self):
        win = self._win

        # Bordo sottile decorativo
        border = tk.Frame(win, bg=ACCENT_COLOR, bd=0)
        border.place(x=0, y=0, width=self.WIDTH, height=2)

        # ── Logo ──────────────────────────────────────────────────────────────
        logo_path = _resource_path("logo.png")
        self._logo_image = None   # mantieni riferimento per evitare GC

        logo_frame = tk.Frame(win, bg=BG_COLOR)
        logo_frame.pack(pady=(22, 8))

        try:
            from PIL import Image, ImageTk
            img = Image.open(logo_path)
            # Ridimensiona proporzionalmente: max 160×80
            img.thumbnail((160, 80), Image.Resampling.LANCZOS)
            self._logo_image = ImageTk.PhotoImage(img)
            tk.Label(logo_frame, image=self._logo_image, bg=BG_COLOR).pack()
        except Exception:
            # Fallback testuale se PIL non disponibile o logo mancante
            tk.Label(
                logo_frame,
                text="TraceabilityRS",
                font=("Segoe UI", 20, "bold"),
                fg=ACCENT_COLOR,
                bg=BG_COLOR,
            ).pack()

        # ── Titolo + versione ─────────────────────────────────────────────────
        try:
            # Importa APP_VERSION se già disponibile nel namespace globale
            import main as _m
            version_str = getattr(_m, "APP_VERSION", "")
        except Exception:
            version_str = ""

        tk.Label(
            win,
            text="TraceabilityRS Management Suite",
            font=("Segoe UI", 13, "bold"),
            fg=TITLE_COLOR,
            bg=BG_COLOR,
        ).pack(pady=(0, 2))

        if version_str:
            tk.Label(
                win,
                text=f"v{version_str}",
                font=("Segoe UI", 9),
                fg=ACCENT_COLOR,
                bg=BG_COLOR,
            ).pack(pady=(0, 14))
        else:
            tk.Frame(win, bg=BG_COLOR, height=14).pack()

        # ── Barra di progresso ────────────────────────────────────────────────
        bar_frame = tk.Frame(win, bg=BG_COLOR)
        bar_frame.pack(fill="x", padx=40, pady=(0, 6))

        style = ttk.Style(win)
        style.theme_use("clam")
        style.configure(
            "Splash.Horizontal.TProgressbar",
            troughcolor=TROUGH_COLOR,
            background=BAR_COLOR,
            bordercolor=BG_COLOR,
            lightcolor=BAR_COLOR,
            darkcolor=BAR_COLOR,
            thickness=10,
        )

        self._progress_var = tk.DoubleVar(value=0)
        self._progress_bar = ttk.Progressbar(
            bar_frame,
            variable=self._progress_var,
            maximum=100,
            mode="determinate",
            style="Splash.Horizontal.TProgressbar",
        )
        self._progress_bar.pack(fill="x")

        # ── Etichetta stato ───────────────────────────────────────────────────
        self._status_var = tk.StringVar(value="Avvio in corso...")
        self._status_label = tk.Label(
            win,
            textvariable=self._status_var,
            font=("Segoe UI", 9),
            fg=TEXT_COLOR,
            bg=BG_COLOR,
        )
        self._status_label.pack(pady=(0, 10))

        # ── Linea inferiore decorativa ────────────────────────────────────────
        tk.Frame(win, bg=ACCENT_COLOR, bd=0).place(
            x=0, y=self.HEIGHT - 2, width=self.WIDTH, height=2
        )

    # ── API pubblica ──────────────────────────────────────────────────────────

    def update_progress(self, value: float, message: str = ""):
        """
        Aggiorna la barra di progresso e il messaggio di stato.
        Thread-safe: può essere chiamato da qualsiasi thread.

        :param value:   Valore 0–100
        :param message: Testo da mostrare sotto la barra
        """
        with self._lock:
            if self._closed:
                return
        # Esegui l'aggiornamento nel thread principale Tk
        self._root.after(0, self._do_update, value, message)

    def _do_update(self, value: float, message: str):
        """Eseguito nel thread principale Tk."""
        with self._lock:
            if self._closed:
                return
        try:
            self._progress_var.set(value)
            if message:
                self._status_var.set(message)
            self._win.update_idletasks()
        except Exception:
            pass

    def hide(self):
        """
        Nasconde la splash screen IMMEDIATAMENTE (sincrono).
        Usare prima di mostrare messagebox/dialoghi che altrimenti
        apparirebbero dietro la splash (topmost).
        """
        try:
            self._win.attributes("-topmost", False)
            self._win.withdraw()
            self._win.update_idletasks()
        except Exception:
            pass

    def close(self):
        """
        Chiude la splash screen.
        Thread-safe: può essere chiamato da qualsiasi thread.
        """
        with self._lock:
            if self._closed:
                return
            self._closed = True
        self._root.after(0, self._do_close)

    def _do_close(self):
        """Eseguito nel thread principale Tk."""
        try:
            self._win.destroy()
        except Exception:
            pass
