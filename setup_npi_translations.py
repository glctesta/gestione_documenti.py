# -*- coding: utf-8 -*-
"""
setup_npi_translations.py

Inserisce in Traceability_rs.dbo.AppTranslations le chiavi di traduzione delle
nuove funzionalita' NPI (bottone "Task in scadenza", form Task in scadenza,
filtro Stato e layout della selezione progetti), per tutte le lingue: it, en,
ro, de, sv. Idempotente: inserisce solo le coppie (lingua, chiave) mancanti, cosi'
non tocca eventuali traduzioni gia' presenti/riviste.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

# key -> {lang: value}. L'ordine lingue: it, en, ro, de, sv
KEYS = {
    # Dashboard NPI
    'btn_upcoming_tasks': {
        'it': '⏳ Task in scadenza', 'en': '⏳ Upcoming Tasks',
        'ro': '⏳ Sarcini în curs de expirare', 'de': '⏳ Anstehende Aufgaben',
        'sv': '⏳ Kommande uppgifter'},

    # Form "Task in scadenza" (upcoming_tasks_window.py)
    'npi_upcoming_title': {
        'it': 'NPI — Task in scadenza', 'en': 'NPI — Upcoming Tasks',
        'ro': 'NPI — Sarcini în curs de expirare', 'de': 'NPI — Anstehende Aufgaben',
        'sv': 'NPI — Kommande uppgifter'},
    'npi_upcoming_col_project': {'it': 'Progetto NPI', 'en': 'NPI Project', 'ro': 'Proiect NPI', 'de': 'NPI-Projekt', 'sv': 'NPI-projekt'},
    'npi_upcoming_col_customer': {'it': 'Cliente', 'en': 'Customer', 'ro': 'Client', 'de': 'Kunde', 'sv': 'Kund'},
    'npi_upcoming_col_product': {'it': 'Prodotto', 'en': 'Product', 'ro': 'Produs', 'de': 'Produkt', 'sv': 'Produkt'},
    'npi_upcoming_col_family': {'it': 'Famiglia', 'en': 'Family', 'ro': 'Familie', 'de': 'Familie', 'sv': 'Familj'},
    'npi_upcoming_col_task': {'it': 'Task', 'en': 'Task', 'ro': 'Sarcină', 'de': 'Aufgabe', 'sv': 'Uppgift'},
    'npi_upcoming_col_owner': {'it': 'Responsabile', 'en': 'Owner', 'ro': 'Responsabil', 'de': 'Verantwortlicher', 'sv': 'Ansvarig'},
    'npi_upcoming_col_due_date': {'it': 'Scadenza', 'en': 'Due Date', 'ro': 'Termen', 'de': 'Fälligkeit', 'sv': 'Förfallodatum'},
    'npi_upcoming_col_days_left': {'it': 'Giorni', 'en': 'Days', 'ro': 'Zile', 'de': 'Tage', 'sv': 'Dagar'},
    'npi_upcoming_col_status': {'it': 'Stato', 'en': 'Status', 'ro': 'Stare', 'de': 'Status', 'sv': 'Status'},
    'npi_upcoming_filters': {'it': 'Filtro scadenze', 'en': 'Deadline filter', 'ro': 'Filtru termene', 'de': 'Fristfilter', 'sv': 'Deadline-filter'},
    'npi_upcoming_days_label': {
        'it': 'Giorni di anticipo (0-5):', 'en': 'Days ahead (0-5):', 'ro': 'Zile în avans (0-5):',
        'de': 'Tage im Voraus (0-5):', 'sv': 'Dagar i förväg (0-5):'},
    'npi_upcoming_hint': {
        'it': 'Doppio click su una riga per aprire il progetto (con login NPI).',
        'en': 'Double-click a row to open the project (NPI login).',
        'ro': 'Dublu-clic pe un rând pentru a deschide proiectul (autentificare NPI).',
        'de': 'Doppelklick auf eine Zeile, um das Projekt zu öffnen (NPI-Login).',
        'sv': 'Dubbelklicka på en rad för att öppna projektet (NPI-inloggning).'},
    'npi_upcoming_open': {
        'it': '📂 Apri progetto selezionato', 'en': '📂 Open selected project',
        'ro': '📂 Deschide proiectul selectat', 'de': '📂 Ausgewähltes Projekt öffnen',
        'sv': '📂 Öppna valt projekt'},
    'npi_upcoming_status': {
        'it': '{0} task in scadenza entro {1} giorni', 'en': '{0} tasks due within {1} days',
        'ro': '{0} sarcini care expiră în {1} zile', 'de': '{0} Aufgaben fällig in {1} Tagen',
        'sv': '{0} uppgifter förfaller inom {1} dagar'},
    'npi_upcoming_load_error': {
        'it': 'Impossibile caricare i task', 'en': 'Unable to load tasks',
        'ro': 'Imposibil de încărcat sarcinile', 'de': 'Aufgaben können nicht geladen werden',
        'sv': 'Kan inte ladda uppgifter'},
    'npi_upcoming_select': {
        'it': 'Selezionare un task dalla lista.', 'en': 'Select a task from the list.',
        'ro': 'Selectați o sarcină din listă.', 'de': 'Wählen Sie eine Aufgabe aus der Liste.',
        'sv': 'Välj en uppgift från listan.'},
    'npi_upcoming_no_project': {
        'it': 'Progetto non individuato per il task selezionato.',
        'en': 'No project found for the selected task.',
        'ro': 'Niciun proiect găsit pentru sarcina selectată.',
        'de': 'Kein Projekt für die ausgewählte Aufgabe gefunden.',
        'sv': 'Inget projekt hittades för den valda uppgiften.'},

    # Selezione progetti NPI (open_npi_project_management)
    'npi_select_title': {
        'it': 'Gestione Progetti NPI — Seleziona progetto', 'en': 'NPI Project Management — Select project',
        'ro': 'Gestionare Proiecte NPI — Selectați proiectul', 'de': 'NPI-Projektverwaltung — Projekt auswählen',
        'sv': 'NPI-projekthantering — Välj projekt'},
    'npi_select_header': {
        'it': 'Gestione Progetti NPI', 'en': 'NPI Project Management',
        'ro': 'Gestionare Proiecte NPI', 'de': 'NPI-Projektverwaltung', 'sv': 'NPI-projekthantering'},
    'npi_select_subtitle': {
        'it': 'Seleziona il progetto da gestire', 'en': 'Select the project to manage',
        'ro': 'Selectați proiectul de gestionat', 'de': 'Wählen Sie das zu verwaltende Projekt',
        'sv': 'Välj projektet att hantera'},
    'npi_state_filter': {'it': 'Stato:', 'en': 'Status:', 'ro': 'Stare:', 'de': 'Status:', 'sv': 'Status:'},
    'npi_state_all': {'it': 'Tutti gli stati', 'en': 'All statuses', 'ro': 'Toate stările', 'de': 'Alle Status', 'sv': 'Alla statusar'},
    'npi_state_closed': {'it': 'Solo chiusi', 'en': 'Closed only', 'ro': 'Doar închise', 'de': 'Nur geschlossene', 'sv': 'Endast stängda'},
    'npi_state_expiring': {
        'it': 'Solo in scadenza tra n giorni', 'en': 'Only expiring within n days',
        'ro': 'Doar care expiră în n zile', 'de': 'Nur fällig in n Tagen', 'sv': 'Endast som förfaller inom n dagar'},
    'npi_state_not_closed': {
        'it': 'Solo non ancora chiusi', 'en': 'Only not yet closed', 'ro': 'Doar neînchise încă',
        'de': 'Nur noch nicht geschlossene', 'sv': 'Endast ännu inte stängda'},
    'npi_state_days': {'it': 'Giorni (0-5):', 'en': 'Days (0-5):', 'ro': 'Zile (0-5):', 'de': 'Tage (0-5):', 'sv': 'Dagar (0-5):'},
    'npi_search': {'it': 'Cerca:', 'en': 'Search:', 'ro': 'Caută:', 'de': 'Suchen:', 'sv': 'Sök:'},
    'npi_projects': {'it': 'Progetti', 'en': 'Projects', 'ro': 'Proiecte', 'de': 'Projekte', 'sv': 'Projekt'},
    'npi_projects_count': {'it': '{0} progetti', 'en': '{0} projects', 'ro': '{0} proiecte', 'de': '{0} Projekte', 'sv': '{0} projekt'},
    'npi_select_invalid': {
        'it': 'Seleziona un progetto valido dalla lista.', 'en': 'Select a valid project from the list.',
        'ro': 'Selectați un proiect valid din listă.', 'de': 'Wählen Sie ein gültiges Projekt aus der Liste.',
        'sv': 'Välj ett giltigt projekt från listan.'},
    'btn_open': {'it': '📂 Apri', 'en': '📂 Open', 'ro': '📂 Deschide', 'de': '📂 Öffnen', 'sv': '📂 Öppna'},
    # Chiavi eventualmente gia' presenti (inserite solo se mancanti):
    'npi_client_filter': {'it': 'Cliente:', 'en': 'Customer:', 'ro': 'Client:', 'de': 'Kunde:', 'sv': 'Kund:'},
    'npi_project_deadline': {'it': 'Scadenza', 'en': 'Deadline', 'ro': 'Termen', 'de': 'Fälligkeit', 'sv': 'Förfallodatum'},
    'npi_no_deadline': {'it': 'n/d', 'en': 'n/a', 'ro': 'n/a', 'de': 'k.A.', 'sv': 'ej def.'},
    'npi_status_closed': {'it': 'Chiuso', 'en': 'Closed', 'ro': 'Închis', 'de': 'Geschlossen', 'sv': 'Stängd'},
    'npi_status_open': {'it': 'Aperto', 'en': 'Open', 'ro': 'Deschis', 'de': 'Offen', 'sv': 'Öppen'},
}


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    ins = 0
    skipped = 0
    for key, langs in KEYS.items():
        for lang, value in langs.items():
            cur.execute("SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                        "WHERE LanguageCode=? AND TranslationKey=?", (lang, key))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO Traceability_rs.dbo.AppTranslations "
                            "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                            (lang, key, value))
                ins += 1
            else:
                skipped += 1
    conn.commit()
    conn.close()
    print(f"[OK] Traduzioni NPI - Inserite: {ins}, Gia' presenti (saltate): {skipped}")


if __name__ == '__main__':
    main()
