# -*- coding: utf-8 -*-
"""
Imposta l'intervallo dello slideshow (settings.SlideshowIntervalMinutes).

Perche': con la cartella immagini su una share di rete ogni cambio immagine era
un download dal server. Con l'intervallo a 2 minuti sono 30 letture/ora per
postazione (~6,6 MB/h, ~53 MB a turno). Portandolo a 10 minuti il traffico
scende subito di 5 volte su TUTTI i client gia' installati, senza aspettare il
prossimo deploy della cache locale delle immagini.

Uso:
    python imposta_slideshow_interval.py            # imposta il default (10)
    python imposta_slideshow_interval.py 15         # imposta un valore diverso
    python imposta_slideshow_interval.py --show     # mostra il valore attuale
"""
import sys

import pyodbc

import database_config as dc

ATTRIBUTE = 'SlideshowIntervalMinutes'
DEFAULT_MINUTES = 10


def read_current(cursor):
    cursor.execute(
        "SELECT IDSettings, [Value] FROM traceability_rs.dbo.settings WHERE Atribute = ?",
        ATTRIBUTE)
    return cursor.fetchone()


def main(argv):
    show_only = '--show' in argv
    args = [a for a in argv if not a.startswith('-')]
    minutes = int(args[0]) if args else DEFAULT_MINUTES
    if minutes < 1:
        print("L'intervallo deve essere di almeno 1 minuto.")
        return 2

    conn = pyodbc.connect(dc.db_config.get_connection_string(), timeout=15)
    cursor = conn.cursor()
    try:
        row = read_current(cursor)
        if not row:
            print(f"ATTENZIONE: '{ATTRIBUTE}' non presente in settings.")
            return 1
        print(f"Valore attuale: {ATTRIBUTE} = {row[1]}  (IDSettings={row[0]})")
        if show_only:
            return 0
        if str(row[1]).strip() == str(minutes):
            print("Gia' impostato, nessuna modifica.")
            return 0

        cursor.execute(
            "UPDATE traceability_rs.dbo.settings SET [Value] = ? WHERE Atribute = ?",
            str(minutes), ATTRIBUTE)
        updated = cursor.rowcount
        conn.commit()
        print(f"Righe aggiornate: {updated}")
        print(f"Nuovo valore  : {ATTRIBUTE} = {read_current(cursor)[1]}")
    finally:
        cursor.close()
        conn.close()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
