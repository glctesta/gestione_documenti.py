"""
insert_material_consumption_translations.py
Inserisce le traduzioni del modulo Material Consumption in AppTranslations.
Usa lo stesso sistema criptato di config_manager.py.
Eseguire con:
  .venv\\Scripts\\python.exe insert_material_consumption_translations.py
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
    ('menu_consumption_ctrl',
        'Controllo Consumi',
        'Consumption Control',
        'Control Consum',
        'Verbrauchskontrolle',
        'Förbrukningskontroll'),
    ('menu_consumption_data',
        'Gestione Dati',
        'Data Management',
        'Gestionare Date',
        'Datenverwaltung',
        'Datahantering'),
    ('menu_consumption_reports',
        'Rapporti',
        'Reports',
        'Rapoarte',
        'Berichte',
        'Rapporter'),

    # ── Form title ────────────────────────────────────────────────────────────
    ('mat_cons_title',
        'Gestione Consumi Materiali',
        'Material Consumption Management',
        'Gestionare Consum Materiale',
        'Materialverbrauchsverwaltung',
        'Materialförbrukningshantering'),

    # ── Section headers ───────────────────────────────────────────────────────
    ('mat_cons_search',
        'RICERCA PRODOTTO',
        'PRODUCT SEARCH',
        'C\u0102UTARE PRODUS',
        'PRODUKTSUCHE',
        'PRODUKTS\u00d6KNING'),
    ('mat_cons_info',
        'INFO PRODOTTO',
        'PRODUCT INFO',
        'INFO PRODUS',
        'PRODUKTINFO',
        'PRODUKTINFO'),
    ('mat_cons_data',
        'DATI DI CONSUMO',
        'CONSUMPTION DATA',
        'DATE CONSUM',
        'VERBRAUCHSDATEN',
        'F\u00d6RBRUKNINGSDATA'),

    # ── Field labels ─────────────────────────────────────────────────────────
    ('mat_cons_labelcode',
        'Label Code:',
        'Label Code:',
        'Cod Etichet\u0103:',
        'Etikett-Code:',
        'Etikettskod:'),
    ('mat_cons_validate',
        'Valida',
        'Validate',
        'Valideaz\u0103',
        'Pr\u00fcfen',
        'Validera'),
    ('mat_cons_or',
        'oppure',
        'or',
        'sau',
        'oder',
        'eller'),
    ('mat_cons_product',
        'Prodotto:',
        'Product:',
        'Produs:',
        'Produkt:',
        'Produkt:'),
    ('mat_cons_pcode',
        'Codice Prodotto',
        'Product Code',
        'Cod Produs',
        'Produktcode',
        'Produktkod'),
    ('mat_cons_alloy',
        'Lega (Alloy_GR)',
        'Alloy (Alloy_GR)',
        'Aliaj (Alloy_GR)',
        'Legierung (Alloy_GR)',
        'Legering (Alloy_GR)'),
    ('mat_cons_flux',
        'Flux (Flux_GR)',
        'Flux (Flux_GR)',
        'Flux (Flux_GR)',
        'Flussmittel (Flux_GR)',
        'Flux (Flux_GR)'),
    ('mat_cons_value',
        'Valore (gr):',
        'Value (gr):',
        'Valoare (gr):',
        'Wert (gr):',
        'V\u00e4rde (gr):'),

    # ── Status / feedback ─────────────────────────────────────────────────────
    ('mat_cons_lc_not_found',
        '\u274c Label non trovato nel database',
        '\u274c Label not found in database',
        '\u274c Etichet\u0103 negasit\u0103 \u00een baza de date',
        '\u274c Etikett nicht in Datenbank gefunden',
        '\u274c Etiketten hittades inte i databasen'),
    ('mat_cons_products_count',
        'Prodotti configurati',
        'Products configured',
        'Produse configurate',
        'Konfigurierte Produkte',
        'Konfigurerade produkter'),

    # ── Dialogs ───────────────────────────────────────────────────────────────
    ('mat_cons_no_product',
        'Selezionare prima un prodotto.',
        'Please select a product first.',
        'V\u0103 rug\u0103m s\u0103 selecta\u021bi mai \u00eent\u00e2i un produs.',
        'Bitte zuerst ein Produkt ausw\u00e4hlen.',
        'V\u00e4lj ett produkt f\u00f6rst.'),
    ('mat_cons_no_value',
        'Inserire un valore di consumo.',
        'Please enter a consumption value.',
        'V\u0103 rug\u0103m s\u0103 introduce\u021bi o valoare de consum.',
        'Bitte einen Verbrauchswert eingeben.',
        'Ange ett f\u00f6rbrukningsv\u00e4rde.'),
    ('mat_cons_invalid_value',
        'Il valore deve essere un numero.',
        'Value must be a number.',
        'Valoarea trebuie s\u0103 fie un num\u0103r.',
        'Der Wert muss eine Zahl sein.',
        'V\u00e4rdet m\u00e5ste vara ett tal.'),
    ('mat_cons_exists_title',
        'Record esistente',
        'Existing Record Found',
        '\u00cenregistrare existent\u0103',
        'Vorhandener Datensatz',
        'Befintlig post hittad'),
    ('mat_cons_exists_msg',
        'Esiste gi\u00e0 un record per questo prodotto',
        'A record already exists for this product',
        'Exist\u0103 deja o \u00eenregistrare pentru acest produs',
        'Es existiert bereits ein Datensatz f\u00fcr dieses Produkt',
        'En post finns redan f\u00f6r denna produkt'),
    ('mat_cons_overwrite',
        'Vuoi sostituirlo con il nuovo valore?',
        'Do you want to replace it with the new value?',
        'Dori\u021bi s\u0103 \u00eenlocui\u021bi cu noua valoare?',
        'M\u00f6chten Sie es durch den neuen Wert ersetzen?',
        'Vill du ers\u00e4tta det med det nya v\u00e4rdet?'),
    ('mat_cons_saved',
        'Dati salvati con successo.',
        'Data saved successfully.',
        'Date salvate cu succes.',
        'Daten erfolgreich gespeichert.',
        'Data sparades.'),
    ('mat_cons_save_error',
        'Errore durante il salvataggio',
        'Save error',
        'Eroare la salvare',
        'Speicherfehler',
        'Sparfel'),

    # ── Authorization key (used by _execute_authorized_action) ───────────────
    ('gestione_mat_consumo',
        'Gestione Consumi Materiali',
        'Material Consumption Management',
        'Gestionare Consum Materiale',
        'Materialverbrauchsverwaltung',
        'Materialförbrukningshantering'),

    # ── Generic (may already exist — safe to skip) ────────────────────────────
    ('coming_soon',
        'Funzionalit\u00e0 in sviluppo',
        'Feature under development',
        'Func\u021bionalitate \u00een curs de dezvoltare',
        'Funktion in Entwicklung',
        'Funktion under utveckling'),
    ('warning',
        'Attenzione',
        'Warning',
        'Aten\u021bie',
        'Warnung',
        'Varning'),
    ('success',
        'Successo',
        'Success',
        'Succes',
        'Erfolg',
        'Framg\u00e5ng'),
    ('error',
        'Errore',
        'Error',
        'Eroare',
        'Fehler',
        'Fel'),
    ('info',
        'Informazione',
        'Info',
        'Informa\u021bie',
        'Info',
        'Info'),
    ('close',
        'Chiudi',
        'Close',
        '\u00cenchide',
        'Schlie\u00dfen',
        'St\u00e4ng'),
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
