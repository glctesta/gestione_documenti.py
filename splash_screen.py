"""
splash_screen.py
Splash screen per TraceabilityRS.
Appare immediatamente all'avvio, mostra logo + barra di progresso
mentre i moduli pesanti vengono caricati in background.
"""

import tkinter as tk
from tkinter import ttk
import random
import threading
import os
import sys


# ── Colori app ────────────────────────────────────────────────────────────────
# Palette di default (prima della lista casuale): blu-notte.
BG_COLOR      = "#1e2a3a"   # sfondo scuro blu-notte
ACCENT_COLOR  = "#4fc3f7"   # azzurro chiaro
TEXT_COLOR    = "#e0f7fa"   # bianco-azzurro
BAR_COLOR     = "#4fc3f7"   # barra progresso
TROUGH_COLOR  = "#2c3e50"   # sfondo barra
TITLE_COLOR   = "#ffffff"   # bianco puro per titolo

# Rose di palette (bg, accent, text, bar, trough, title): a ogni apertura
# viene scelta una a caso, cosi' lo splash ha un colore di fondo diverso
# (colori decisi, contrasto leggibile con testo chiaro).
_SPLASH_PALETTES = [
    ("#1e2a3a", "#4fc3f7", "#e0f7fa", "#4fc3f7", "#2c3e50", "#ffffff"),  # blu notte
    ("#14532d", "#4ade80", "#dcfce7", "#4ade80", "#166534", "#ffffff"),  # verde bosco
    ("#7f1d1d", "#f87171", "#fee2e2", "#f87171", "#991b1b", "#ffffff"),  # rosso mattone
    ("#4c1d95", "#c084fc", "#ede9fe", "#c084fc", "#5b21b6", "#ffffff"),  # viola
    ("#7c2d12", "#fb923c", "#ffedd5", "#fb923c", "#9a3412", "#ffffff"),  # arancio tramonto
    ("#134e4a", "#2dd4bf", "#ccfbf1", "#2dd4bf", "#115e59", "#ffffff"),  # petrolio
    ("#1e3a8a", "#60a5fa", "#dbeafe", "#60a5fa", "#1e40af", "#ffffff"),  # blu royal
    ("#831843", "#f472b6", "#fce7f3", "#f472b6", "#9d174d", "#ffffff"),  # fucsia
    ("#713f12", "#facc15", "#fef9c3", "#facc15", "#854d0e", "#ffffff"),  # oro
    ("#312e81", "#818cf8", "#e0e7ff", "#818cf8", "#3730a3", "#ffffff"),  # indaco
    ("#3f6212", "#a3e635", "#ecfccb", "#a3e635", "#4d7c0f", "#ffffff"),  # lime scuro
    ("#27272a", "#ef4444", "#fafafa", "#ef4444", "#3f3f46", "#ffffff"),  # grafite/rosso
]


def _random_palette() -> dict:
    """Palette casuale per lo splash (una diversa a ogni apertura)."""
    bg, accent, text, bar, trough, title = random.choice(_SPLASH_PALETTES)
    return {
        'bg': bg, 'accent': accent, 'text': text,
        'bar': bar, 'trough': trough, 'title': title,
    }


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

        # Colore di fondo casuale a ogni apertura
        self._palette = _random_palette()
        self.bg_color     = self._palette['bg']
        self.accent_color = self._palette['accent']
        self.text_color   = self._palette['text']
        self.bar_color    = self._palette['bar']
        self.trough_color = self._palette['trough']
        self.title_color  = self._palette['title']

        # ── Crea la finestra splash ───────────────────────────────────────────
        self._win = tk.Toplevel(root)
        self._win.overrideredirect(True)          # niente bordi / barra titolo
        self._win.configure(bg=self.bg_color)
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
        BG = self.bg_color

        # Bordo sottile decorativo
        border = tk.Frame(win, bg=self.accent_color, bd=0)
        border.place(x=0, y=0, width=self.WIDTH, height=2)

        # ── Logo ──────────────────────────────────────────────────────────────
        logo_path = _resource_path("logo.png")
        self._logo_image = None   # mantieni riferimento per evitare GC

        logo_frame = tk.Frame(win, bg=BG)
        logo_frame.pack(pady=(22, 8))

        try:
            from PIL import Image, ImageTk
            img = Image.open(logo_path)
            # Ridimensiona proporzionalmente: max 160×80
            img.thumbnail((160, 80), Image.Resampling.LANCZOS)
            self._logo_image = ImageTk.PhotoImage(img)
            tk.Label(logo_frame, image=self._logo_image, bg=BG).pack()
        except Exception:
            # Fallback testuale se PIL non disponibile o logo mancante
            tk.Label(
                logo_frame,
                text="TraceabilityRS",
                font=("Segoe UI", 20, "bold"),
                fg=self.accent_color,
                bg=BG,
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
            fg=self.title_color,
            bg=BG,
        ).pack(pady=(0, 2))

        if version_str:
            tk.Label(
                win,
                text=f"v{version_str}",
                font=("Segoe UI", 9),
                fg=self.accent_color,
                bg=BG,
            ).pack(pady=(0, 14))
        else:
            tk.Frame(win, bg=BG, height=14).pack()

        # ── Barra di progresso ────────────────────────────────────────────────
        bar_frame = tk.Frame(win, bg=BG)
        bar_frame.pack(fill="x", padx=40, pady=(0, 6))

        style = ttk.Style(win)
        style.theme_use("clam")
        style.configure(
            "Splash.Horizontal.TProgressbar",
            troughcolor=self.trough_color,
            background=self.bar_color,
            bordercolor=BG,
            lightcolor=self.bar_color,
            darkcolor=self.bar_color,
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
            fg=self.text_color,
            bg=BG,
        )
        self._status_label.pack(pady=(0, 10))

        # ── Linea inferiore decorativa ────────────────────────────────────────
        tk.Frame(win, bg=self.accent_color, bd=0).place(
            x=0, y=self.HEIGHT - 2, width=self.WIDTH, height=2
        )

    # ── API pubblica ──────────────────────────────────────────────────────────

    def update_progress(self, value: float, message: str = ""):
        """
        Aggiorna la barra di progresso e il messaggio di stato.
        Chiamata dal thread principale durante l'init: aggiornamento SINCRONO
        con win.update() per garantire il ridisegno immediato.
        """
        with self._lock:
            if self._closed:
                return
        import threading
        if threading.current_thread() is threading.main_thread():
            # Siamo nel thread principale: anima fluidamente da valore corrente
            self._smooth_to(value, message)
        else:
            # Thread secondario: schedula via after
            self._root.after(0, self._do_update, value, message)

    def _smooth_to(self, target: float, message: str, steps: int = 12, delay_ms: int = 18):
        """Anima la barra fluidamente dal valore corrente al target (sincrono, thread principale)."""
        try:
            current = self._progress_var.get()
            if message:
                self._status_var.set(message)
            if target <= current:
                self._progress_var.set(target)
                self._win.update()
                return
            step = (target - current) / steps
            val = current
            for _ in range(steps):
                val = min(val + step, target)
                self._progress_var.set(val)
                self._win.update()
                import time
                time.sleep(delay_ms / 1000.0)
            self._progress_var.set(target)
            self._win.update()
        except Exception:
            pass

    def _do_update(self, value: float, message: str):
        """Eseguito nel thread principale Tk (via after, per chiamate da thread secondari)."""
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
