# calendar_widget.py
"""
Widget calendario personalizzato con ttkbootstrap
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DatePickerEntry(ttk.Frame):
    """
    Widget personalizzato che combina Entry + Calendario
    Consente di selezionare una data tramite calendario o inserirla manualmente
    """

    def __init__(self, parent, lang=None, **kwargs):
        super().__init__(parent)

        self.lang = lang
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))

        # Frame interno
        inner_frame = ttk.Frame(self)
        inner_frame.pack(fill=tk.X, expand=True)

        # Entry per la data
        self.entry = DateEntry(
            inner_frame,
            textvariable=self.date_var,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            **kwargs
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def get(self):
        """Restituisce la data selezionata nel formato YYYY-MM-DD"""
        # Il DateEntry mostra la data nel formato locale (es. 9/15/26), quindi
        # la leggiamo direttamente dal widget: interpreta sia la selezione dal
        # calendario sia la digitazione manuale.
        try:
            return self.entry.get_date().strftime('%Y-%m-%d')
        except (ValueError, tk.TclError):
            pass
        # Fallback: interpreta i formati più comuni digitati a mano
        raw = (self.entry.get() or '').strip() or self.date_var.get().strip()
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d.%m.%Y',
                    '%d/%m/%y', '%m/%d/%y', '%d.%m.%y'):
            try:
                return datetime.strptime(raw, fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        logger.error(f"Formato data non valido: {raw!r}")
        return None

    def set(self, date_str: str):
        """Imposta una data nel formato YYYY-MM-DD"""
        try:
            self.entry.set_date(datetime.strptime(date_str, '%Y-%m-%d').date())
        except ValueError:
            logger.error(f"Formato data non valido: {date_str}")

    def clear(self):
        """Resetta la data a oggi"""
        self.date_var.set(datetime.now().strftime('%Y-%m-%d'))