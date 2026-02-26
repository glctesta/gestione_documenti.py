# simple_local_check.py
import os
import sys
import socket
from typing import List
import tkinter as tk


class SimpleSecurityWindow:
    """Finestra di sicurezza semplificata"""

    def show(self, blocked_ips: List[str] = None):
        """Mostra finestra di sicurezza"""
        root = tk.Tk()
        root.title("Accesso Bloccato")
        root.geometry("450x220")
        root.resizable(False, False)
        root.configure(bg='#f8d7da')  # Sfondo rosso chiaro

        # Centra la finestra
        root.eval('tk::PlaceWindow . center')

        # Contenuto
        tk.Label(root, text="🚫 ACCESSO BLOCCATO",
                 font=('Arial', 12, 'bold'),
                 fg='#721c24',
                 bg='#f8d7da').pack(pady=20)

        message = "Questa applicazione non può essere eseguita\n" \
                  "da reti remote o posizioni non autorizzate."
        tk.Label(root, text=message,
                 font=('Arial', 10),
                 fg='#721c24',
                 bg='#f8d7da').pack(pady=10)

        # Dettagli IP bloccati
        if blocked_ips:
            details = f"Reti bloccate: {', '.join(blocked_ips)}"
            tk.Label(root, text=details,
                     font=('Arial', 8),
                     fg='#856404',
                     bg='#f8d7da').pack(pady=5)

        # Bottone OK
        def close_app():
            root.destroy()
            sys.exit(1)

        tk.Button(root, text="CHIUDI",
                  command=close_app,
                  font=('Arial', 10, 'bold'),
                  bg='#dc3545',
                  fg='white',
                  width=15,
                  height=2).pack(pady=20)

        # Bind tasti
        root.bind('<Return>', lambda e: close_app())
        root.bind('<Escape>', lambda e: close_app())

        root.mainloop()


def is_local_execution_simple(not_allowed_ips: List[str] = None):
    """Verifica se l'IP della macchina è nella lista degli IP bloccati.
    
    Blocca SOLO gli IP specifici nella lista, non le sessioni remote in generale.
    """
    not_allowed_ips = not_allowed_ips or []

    try:
        # Ottieni IP locale
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Verifica sicurezza: IP locale = {local_ip}")

        # Controlla se l'IP locale è nella lista bloccata
        if local_ip in not_allowed_ips:
            print(f"IP {local_ip} è nella lista bloccata!")
            return False

        return True

    except Exception:
        return True


def verify_simple(not_allowed_ips: List[str] = None):
    """Verifica semplificata con finestra messaggio"""
    if not is_local_execution_simple(not_allowed_ips=not_allowed_ips):
        print("Bloccata esecuzione da posizione non autorizzata")

        # Mostra finestra di sicurezza
        security_window = SimpleSecurityWindow()
        security_window.show(not_allowed_ips)

        sys.exit(1)

    print("✓ Verifica sicurezza superata")
    return True