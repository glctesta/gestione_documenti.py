# -*- coding: utf-8 -*-
"""Traduzioni per l'avviso di chiusura in corso mostrato al posto dello slideshow
mentre vengono fermati i servizi/monitor attivi."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('shutdown_in_progress',
     'Chiusura del programma in corso...',
     'Shutting down the application...',
     'Închiderea programului în curs...',
     'Das Programm wird beendet...',
     'Programmet stängs av...'),
    ('shutdown_stopping_services',
     'Arresto dei servizi attivi, attendere prego...',
     'Stopping active services, please wait...',
     'Se opresc serviciile active, vă rugăm așteptați...',
     'Aktive Dienste werden beendet, bitte warten...',
     'Aktiva tjänster stoppas, vänligen vänta...'),
    ('shutdown_closing_session',
     'Chiusura sessione e disconnessione database...',
     'Closing session and disconnecting database...',
     'Se închide sesiunea și se deconectează baza de date...',
     'Sitzung wird geschlossen und Datenbank getrennt...',
     'Sessionen avslutas och databasen kopplas från...'),
    ('shutdown_svc_wh_monitor',
     'Monitoraggio giacenze materiali indiretti',
     'Indirect materials stock monitor',
     'Monitorizare stocuri materiale indirecte',
     'Bestandsüberwachung indirekte Materialien',
     'Lagerövervakning indirekt material'),
    ('shutdown_svc_requester_monitor',
     'Monitoraggio richieste materiali',
     'Material requests monitor',
     'Monitorizare cereri de materiale',
     'Überwachung der Materialanforderungen',
     'Övervakning av materialbeställningar'),
    ('shutdown_svc_budget_monitor',
     'Monitoraggio approvazioni budget NPI',
     'NPI budget approvals monitor',
     'Monitorizare aprobări buget NPI',
     'Überwachung der NPI-Budgetfreigaben',
     'Övervakning av NPI-budgetgodkännanden'),
    ('shutdown_svc_handover_monitor',
     'Monitoraggio consegna turno',
     'Shift handover monitor',
     'Monitorizare predare tură',
     'Überwachung der Schichtübergabe',
     'Övervakning av skiftöverlämning'),
    ('shutdown_svc_kit_dashboard',
     'Kit Dashboard', 'Kit Dashboard', 'Kit Dashboard',
     'Kit Dashboard', 'Kit Dashboard'),
    ('shutdown_svc_background_tasks',
     'Attività in background',
     'Background tasks',
     'Activități în fundal',
     'Hintergrundaufgaben',
     'Bakgrundsaktiviteter'),
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
    print(f"[OK] Shutdown notice translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
