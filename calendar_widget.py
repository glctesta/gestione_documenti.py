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
        try:
            date_str = self.date_var.get()
            # Valida il formato
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            logger.error(f"Formato data non valido: {self.date_var.get()}")
            return None

    def set(self, date_str: str):
        """Imposta una data nel formato YYYY-MM-DD"""
        try:
            # Valida il formato
            datetime.strptime(date_str, '%Y-%m-%d')
            self.date_var.set(date_str)
        except ValueError:
            logger.error(f"Formato data non valido: {date_str}")

    def clear(self):
        """Resetta la data a oggi"""
        self.date_var.set(datetime.now().strftime('%Y-%m-%d'))