# -*- coding: utf-8 -*-
"""Traduzioni aggiuntive FQC: checkbox 'solo con piano', filtro Ordine nel report,
form Copia Documentazione (fqc_copy_docs_gui)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('fqc_only_with_plan',
     'Solo codici con piano di verifica caricato', 'Only codes with a verification plan',
     'Doar coduri cu plan de verificare', 'Nur Codes mit Prüfplan',
     'Endast koder med kontrollplan'),
    ('fqc_report_order', 'Ordine:', 'Order:', 'Comandă:', 'Auftrag:', 'Order:'),

    # ── Copy documentation (fqc_copy_docs_gui) ─────────────────────────────
    ('fqc_copy_docs_title',
     'FQC Prodotti — Copia Documentazione', 'FQC Products — Copy Documentation',
     'FQC Produse — Copiere Documentație', 'FQC Produkte — Dokumentation kopieren',
     'FQC Produkter — Kopiera dokumentation'),
    ('fqc_copy_docs_btn',
     '📋 Copia documentazione', '📋 Copy documentation',
     '📋 Copiere documentație', '📋 Dokumentation kopieren',
     '📋 Kopiera dokumentation'),
    ('fqc_copy_source',
     'Prodotto sorgente (con checklist):', 'Source product (with checklist):',
     'Produs sursă (cu listă de verificare):', 'Quellprodukt (mit Checkliste):',
     'Källprodukt (med checklista):'),
    ('fqc_copy_dest',
     'Prodotto destinazione:', 'Destination product:',
     'Produs destinație:', 'Zielprodukt:', 'Målprodukt:'),
    ('fqc_copy_items_section',
     'DOCUMENTAZIONE DA COPIARE', 'DOCUMENTATION TO COPY',
     'DOCUMENTAȚIE DE COPIAT', 'ZU KOPIERENDE DOKUMENTATION',
     'DOKUMENTATION ATT KOPIERA'),
    ('fqc_copy_col_sel',
     '✓', '✓', '✓', '✓', '✓'),
    ('fqc_copy_col_num',
     'N°', 'No.', 'Nr.', 'Nr.', 'Nr.'),
    ('fqc_copy_select_all',
     'Seleziona tutto', 'Select all',
     'Selectează tot', 'Alle auswählen', 'Markera alla'),
    ('fqc_copy_select_none',
     'Deseleziona tutto', 'Deselect all',
     'Deselectează tot', 'Auswahl aufheben', 'Avmarkera alla'),
    ('fqc_copy_history',
     'STORICO COPIE SUL PRODOTTO DESTINAZIONE', 'COPY HISTORY ON DESTINATION PRODUCT',
     'ISTORIC COPIERI PE PRODUSUL DESTINAȚIE', 'KOPIERHISTORIE ZUM ZIELPRODUKT',
     'KOPIERINGSHISTORIK FÖR MÅLPRODUKT'),
    ('fqc_copy_hist_when',
     'Data', 'When', 'Data', 'Wann', 'När'),
    ('fqc_copy_hist_from',
     'Da', 'From', 'De la', 'Von', 'Från'),
    ('fqc_copy_hist_user',
     'Utente', 'User', 'Utilizator', 'Benutzer', 'Användare'),
    ('fqc_copy_hist_items',
     'N° item', 'N° items', 'Nr. elemente', 'Anzahl Positionen', 'Antal poster'),
    ('fqc_copy_no_history',
     'Nessuna copia precedente su questo prodotto.', 'No previous copies on this product.',
     'Nicio copiere anterioară pe acest produs.', 'Keine früheren Kopien für dieses Produkt.',
     'Inga tidigare kopieringar på denna produkt.'),
    ('fqc_copy_do_copy',
     '📋 Copia documentazione selezionata', '📋 Copy selected documentation',
     '📋 Copiază documentația selectată', '📋 Ausgewählte Dokumentation kopieren',
     '📋 Kopiera vald dokumentation'),
    ('fqc_copy_confirm_msg',
     'Copiare {n} item da "{src}" a "{dst}"?', 'Copy {n} item(s) from "{src}" to "{dst}"?',
     'Copiați {n} elemente de la "{src}" la "{dst}"?', '{n} Position(en) von "{src}" nach "{dst}" kopieren?',
     'Kopiera {n} poster från "{src}" till "{dst}"?'),
    ('fqc_copy_new_cl_msg',
     'Verrà creata una nuova checklist: {name}', 'A new checklist will be created: {name}',
     'Va fi creată o nouă listă de verificare: {name}', 'Eine neue Checkliste wird erstellt: {name}',
     'En ny checklista kommer att skapas: {name}'),
    ('fqc_copy_success',
     'Documentazione copiata con successo.', 'Documentation copied successfully.',
     'Documentație copiată cu succes.', 'Dokumentation erfolgreich kopiert.',
     'Dokumentationen har kopierats.'),
    ('fqc_copy_err_select_source',
     'Seleziona un prodotto sorgente con checklist attiva.', 'Select a source product with an active checklist.',
     'Selectați un produs sursă cu listă de verificare activă.', 'Wählen Sie ein Quellprodukt mit aktiver Checkliste.',
     'Välj ett källprodukt med aktiv checklista.'),
    ('fqc_copy_err_select_dest',
     'Seleziona un prodotto destinazione.', 'Select a destination product.',
     'Selectați un produs destinație.', 'Wählen Sie ein Zielprodukt.',
     'Välj ett målprodukt.'),
    ('fqc_copy_err_same_product',
     'I prodotti sorgente e destinazione devono essere diversi.', 'Source and destination products must be different.',
     'Produsele sursă și destinație trebuie să fie diferite.', 'Quell- und Zielprodukt müssen unterschiedlich sein.',
     'Käll- och målprodukt måste vara olika.'),
    ('fqc_copy_err_no_items',
     'Seleziona almeno un item da copiare.', 'Select at least one item to copy.',
     'Selectați cel puțin un element de copiat.', 'Wählen Sie mindestens eine Position zum Kopieren.',
     'Välj minst en post att kopiera.'),
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
    print(f"[OK] FQC extra translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
