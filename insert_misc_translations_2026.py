# -*- coding: utf-8 -*-
"""Traduzioni: multi-assegnazione cliente a prodotti + pulsante gestione clienti nella form AM."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('button_assign_client_multi', 'Assegna Cliente a Selezionati', 'Assign Client to Selected',
     'Atribuie Client la Selectate', 'Kunde den Ausgewaehlten zuweisen', 'Tilldela kund till valda'),
    ('assign_client_hint',
     "Selezione multipla: Ctrl/Shift + clic. Il codice cliente sara' impostato uguale al codice prodotto "
     "(modificabile poi singolarmente).",
     'Multi-selection: Ctrl/Shift + click. The customer code will be set equal to the product code '
     '(editable individually afterwards).',
     'Selectie multipla: Ctrl/Shift + clic. Codul clientului va fi setat egal cu codul produsului '
     '(modificabil ulterior individual).',
     'Mehrfachauswahl: Strg/Umschalt + Klick. Der Kundencode wird gleich dem Produktcode gesetzt '
     '(danach einzeln bearbeitbar).',
     'Flerval: Ctrl/Shift + klick. Kundkoden saetts lika med produktkoden (kan redigeras individuellt efterat).'),
    ('cam_manage_clients', '➕ Aggiungi/Gestisci Clienti', '➕ Add/Manage Clients',
     '➕ Adauga/Gestioneaza Clienti', '➕ Kunden hinzufuegen/verwalten', '➕ Laegg till/hantera kunder'),
    ('cam_no_manage_customers', 'Funzione gestione clienti non disponibile.',
     'Client management function not available.', 'Functia de gestionare clienti nu este disponibila.',
     'Kundenverwaltungsfunktion nicht verfuegbar.', 'Kundhanteringsfunktion ej tillgaenglig.'),
    ('ind_req_reprint_by_requester_ok',
     '{0} lista/e generata/e (una per richiedente) e inviata/e in stampa.',
     '{0} list(s) generated (one per requester) and sent to print.',
     '{0} lista/e generata/e (una per solicitant) si trimisa/e la imprimare.',
     '{0} Liste(n) erstellt (eine pro Anforderer) und zum Druck gesendet.',
     '{0} lista/or genererad(e) (en per bestaellare) och skickad(e) till utskrift.'),
    ('ind_req_filter_from', 'Da:', 'From:', 'De la:', 'Von:', 'Från:'),
    ('ind_req_filter_to', 'A:', 'To:', 'Până la:', 'Bis:', 'Till:'),
    ('ind_req_filter_code', 'Codice:', 'Code:', 'Cod:', 'Code:', 'Kod:'),
    ('ind_req_filter_requester', 'Richiedente:', 'Requester:', 'Solicitant:', 'Anforderer:', 'Bestaellare:'),
    ('ind_req_col_prints', 'Stampe', 'Prints', 'Tipariri', 'Drucke', 'Utskrifter'),
]
LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    ins = skip = 0
    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            cur.execute("SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                        "WHERE LanguageCode = ? AND TranslationKey = ?", (lang, key))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO Traceability_rs.dbo.AppTranslations "
                            "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                            (lang, key, row[i + 1]))
                ins += 1
            else:
                skip += 1
    conn.commit(); conn.close()
    print(f"[OK] Misc translations 2026 - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
