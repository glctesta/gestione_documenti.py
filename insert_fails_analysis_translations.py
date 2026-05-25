"""
insert_fails_analysis_translations.py
Inserisce le traduzioni del modulo Analisi Fails in AppTranslations.
Usa lo stesso sistema criptato di config_manager.py.
Eseguire con:
  .venv\Scripts\python.exe insert_fails_analysis_translations.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager

def get_conn():
    cfg = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc').load_config()
    conn_str = (f"DRIVER={cfg['driver']};SERVER={cfg['server']};"
                f"DATABASE={cfg['database']};UID={cfg['username']};PWD={cfg['password']};"
                f"MARS_Connection=Yes;TrustServerCertificate=Yes")
    return pyodbc.connect(conn_str)

# (key, IT, EN, RO, DE, SV)
TRANSLATIONS = [
    # ── Menu ──────────────────────────────────────────────────────────────────
    ('menu_analisi_fails',
        '\U0001f4c8 Analisi Fails',
        '\U0001f4c8 Fail Analysis',
        '\U0001f4c8 Analiz\u0103 E\u0219ecuri',
        '\U0001f4c8 Fehleranalyse',
        '\U0001f4c8 Felanalys'),
    # ── Titolo finestra ───────────────────────────────────────────────────────
    ('fa_title',
        'Analisi Schede FAIL',
        'FAIL Board Analysis',
        'Analiz\u0103 Fi\u0219e FAIL',
        'FAIL-Platinen Analyse',
        'FAIL-kort Analys'),
    # ── Label barra superiore ─────────────────────────────────────────────────
    ('fa_date_from',
        'Da:',
        'From:',
        'De la:',
        'Von:',
        'Fr\u00e5n:'),
    ('fa_date_to',
        'A:',
        'To:',
        'P\u00e2n\u0103 la:',
        'Bis:',
        'Till:'),
    ('fa_load_btn',
        '\U0001f504 Carica / Aggiorna',
        '\U0001f504 Load / Refresh',
        '\U0001f504 \u00cencasc\u0103 / Actualizeaz\u0103',
        '\U0001f504 Laden / Aktualisieren',
        '\U0001f504 Ladda / Uppdatera'),
    ('fa_export_btn',
        '\U0001f4ca Esporta Excel',
        '\U0001f4ca Export Excel',
        '\U0001f4ca Export Excel',
        '\U0001f4ca Excel Export',
        '\U0001f4ca Exportera Excel'),
    # ── Tab notebook ──────────────────────────────────────────────────────────
    ('fa_tab_raw',
        'Dati Grezzi',
        'Raw Data',
        'Date Brute',
        'Rohdaten',
        'R\u00e5data'),
    ('fa_tab_repaired',
        'Schede Riparate',
        'Repaired Boards',
        'Fi\u0219e Reparate',
        'Reparierte Platinen',
        'Reparerade kort'),
    ('fa_tab_stats',
        'Statistiche',
        'Statistics',
        'Statistici',
        'Statistiken',
        'Statistik'),
    # ── Messaggi stato ────────────────────────────────────────────────────────
    ('fa_status_loading',
        'Caricamento in corso...',
        'Loading...',
        'Se \u00eencasc\u0103...',
        'Wird geladen...',
        'Laddar...'),
    ('fa_status_ready',
        '{0} schede FAIL \u2014 {1} riparate ({2:.1f}%)',
        '{0} FAIL boards \u2014 {1} repaired ({2:.1f}%)',
        '{0} fi\u0219e FAIL \u2014 {1} reparate ({2:.1f}%)',
        '{0} FAIL-Platinen \u2014 {1} repariert ({2:.1f}%)',
        '{0} FAIL-kort \u2014 {1} reparerade ({2:.1f}%)'),
    ('fa_no_data',
        'Nessun dato trovato per il periodo selezionato',
        'No data found for the selected period',
        'Niciun date g\u0103site pentru perioada selectat\u0103',
        'Keine Daten f\u00fcr den gew\u00e4hlten Zeitraum gefunden',
        'Inga data hittades f\u00f6r den valda perioden'),
    ('fa_confirm_reload',
        'Cache esistente',
        'Existing cache',
        'Cache existent',
        'Cache vorhanden',
        'Cache finns'),
    ('fa_confirm_reload_msg',
        'Trovati {0} record in cache per questo periodo.\nRicaricare dal database?',
        'Found {0} cached records for this period.\nReload from database?',
        'G\u0103site {0} \u00eenregistr\u0103ri \u00een cache.\nRe\u00eencasc\u0103 din baza de date?',
        '{0} Datens\u00e4tze im Cache gefunden.\nAus Datenbank neu laden?',
        'Hittade {0} cachade poster.\nLadda om fr\u00e5n databasen?'),
    # ── Colonne Treeview Tab Grezzi ────────────────────────────────────────────
    ('fa_col_order',
        'N. Ordine',
        'Order No.',
        'Nr. Comand\u0103',
        'Auftr.-Nr.',
        'Order nr.'),
    ('fa_col_product',
        'Prodotto',
        'Product',
        'Produs',
        'Produkt',
        'Produkt'),
    ('fa_col_qty',
        'Qty',
        'Qty',
        'Cant.',
        'Menge',
        'Antal'),
    ('fa_col_phase',
        'Fase',
        'Phase',
        'Faz\u0103',
        'Phase',
        'Fas'),
    ('fa_col_idboard',
        'IDBoard',
        'IDBoard',
        'IDBoard',
        'IDBoard',
        'IDBoard'),
    ('fa_col_labels',
        'Label',
        'Label',
        'Etichet\u0103',
        'Etikett',
        'Etikett'),
    ('fa_col_scanres',
        'Risultato',
        'Result',
        'Rezultat',
        'Ergebnis',
        'Resultat'),
    ('fa_col_scantime',
        'Data Scan',
        'Scan Date',
        'Data Scan',
        'Scan-Datum',
        'Skan datum'),
    ('fa_col_repair',
        'Riparazione',
        'Repair',
        'Repara\u021bie',
        'Reparatur',
        'Reparation'),
    ('fa_col_defect',
        'Difetto',
        'Defect',
        'Defect',
        'Defekt',
        'Defekt'),
    ('fa_col_codref',
        'Cod.Rif.',
        'Ref.Code',
        'Cod.Ref.',
        'Ref.-Code',
        'Ref.kod'),
    # ── Colonne Treeview Tab Riparate ─────────────────────────────────────────
    ('fa_col_resolved',
        'Data Risoluz.',
        'Resolved On',
        'Data Rezolv\u0103rii',
        'Gel\u00f6st am',
        'L\u00f6st datum'),
    ('fa_col_days',
        'Giorni',
        'Days',
        'Zile',
        'Tage',
        'Dagar'),
]

LANGS = ['it', 'en', 'ro', 'de', 'sv']


def main():
    print("Connessione al database...")
    try:
        conn = get_conn()
    except Exception as e:
        print(f"Errore connessione: {e}")
        sys.exit(1)

    cursor = conn.cursor()
    inserted = 0
    skipped  = 0

    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            value = row[i + 1]
            cursor.execute(
                "SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                "WHERE LanguageCode=? AND TranslationKey=?",
                (lang, key)
            )
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO Traceability_rs.dbo.AppTranslations "
                    "(LanguageCode, TranslationKey, TranslationValue) VALUES (?,?,?)",
                    (lang, key, value)
                )
                inserted += 1
            else:
                skipped += 1

    conn.commit()
    conn.close()
    print(f"[OK] Completato - Inserite: {inserted}  |  Gia' presenti (skip): {skipped}")
    print(f"     Totale chiavi: {len(TRANSLATIONS)}  x  {len(LANGS)} lingue = {len(TRANSLATIONS)*len(LANGS)} record")


if __name__ == '__main__':
    main()
