# -*- coding: utf-8 -*-
"""
insert_fqc_products_translations.py
Inserts all UI translation keys for the FQC Products module
into Traceability_rs.dbo.AppTranslations (5 languages: it, en, ro, de, sv).

Run once:  python insert_fqc_products_translations.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# ── DB connection (reuse the project helper) ──────────────────────────────────
def _get_conn():
    try:
        from utils import get_db_connection
        return get_db_connection()
    except Exception:
        pass
    try:
        import pyodbc
        dsn = open(os.path.join(os.path.dirname(__file__), 'db.conf'),
                   encoding='utf-8').read().strip()
        return pyodbc.connect(dsn)
    except Exception as exc:
        print(f'[ERROR] Cannot connect to DB: {exc}')
        sys.exit(1)

# ── Translation table ─────────────────────────────────────────────────────────
# Each row: (key, it, en, ro, de, sv)
TRANSLATIONS = [
    # ── Menu labels ────────────────────────────────────────────────────────────
    ('menu_fqc_products',
     'FQC Prodotti',
     'FQC Products',
     'FQC Produse',
     'FQC Produkte',
     'FQC Produkter'),

    ('menu_fqc_execution',
     '▶ Esecuzione Controlli',
     '▶ Execute Checks',
     '▶ Executare Verificari',
     '▶ Kontrollen durchführen',
     '▶ Utför kontroller'),

    ('menu_fqc_master',
     '⚙ Gestione Anagrafica',
     '⚙ Manage Checklists',
     '⚙ Gestionare Liste de Verificare',
     '⚙ Checklisten verwalten',
     '⚙ Hantera checklistor'),

    ('menu_fqc_feedback',
     '💬 Feedback Cliente',
     '💬 Customer Feedback',
     '💬 Feedback Client',
     '💬 Kundenfeedback',
     '💬 Kundfeedback'),

    # ── Authorization key ──────────────────────────────────────────────────────
    ('fqc_master',
     'Gestione Anagrafica FQC',
     'FQC Checklist Management',
     'Gestionare Liste de Verificare FQC',
     'FQC Checklisten-Verwaltung',
     'FQC checklisthantering'),

    # ── Form titles ────────────────────────────────────────────────────────────
    ('fqc_exec_title',
     'FQC Prodotti — Esecuzione Checklist',
     'FQC Products — Checklist Execution',
     'FQC Produse — Executare Lista de Verificare',
     'FQC Produkte — Checklisten-Ausführung',
     'FQC Produkter — Checklistautförande'),

    ('fqc_master_title',
     'FQC Prodotti — Gestione Checklist',
     'FQC Products — Checklist Management',
     'FQC Produse — Gestionare Lista de Verificare',
     'FQC Produkte — Checklisten-Verwaltung',
     'FQC Produkter — Checklisthantering'),

    ('fqc_feedback_title',
     'FQC Prodotti — Feedback Cliente',
     'FQC Products — Customer Feedback',
     'FQC Produse — Feedback Client',
     'FQC Produkte — Kundenfeedback',
     'FQC Produkter — Kundfeedback'),

    # ── Selection area ─────────────────────────────────────────────────────────
    ('fqc_selection',
     'SELEZIONE PRODOTTO',
     'PRODUCT SELECTION',
     'SELECTIE PRODUS',
     'PRODUKTAUSWAHL',
     'PRODUKTVAL'),

    ('fqc_client',
     'Cliente:',
     'Client:',
     'Client:',
     'Kunde:',
     'Kund:'),

    ('fqc_product',
     'Prodotto:',
     'Product:',
     'Produs:',
     'Produkt:',
     'Produkt:'),

    ('fqc_operator',
     'Operatore',
     'Operator',
     'Operator',
     'Operator',
     'Operatör'),

    # ── Checklist area ─────────────────────────────────────────────────────────
    ('fqc_checklist',
     'CHECKLIST',
     'CHECKLIST',
     'LISTA DE VERIFICARE',
     'CHECKLISTE',
     'CHECKLISTA'),

    ('fqc_cl_header_section',
     'INTESTAZIONE CHECKLIST',
     'CHECKLIST HEADER',
     'ANTET LISTA DE VERIFICARE',
     'CHECKLISTEN-KOPF',
     'CHECKLISTHUVUD'),

    ('fqc_cl_name',
     'Nome Checklist:',
     'Checklist Name:',
     'Nume Lista de Verificare:',
     'Checklistenname:',
     'Checklistnamn:'),

    ('fqc_items_list',
     'VOCI CHECKLIST',
     'CHECKLIST ITEMS',
     'ELEMENTE LISTA DE VERIFICARE',
     'CHECKLISTENPUNKTE',
     'CHECKLISTOBJEKT'),

    ('fqc_item_editor',
     'EDITOR VOCE',
     'ITEM EDITOR',
     'EDITOR ELEMENT',
     'ELEMENT-EDITOR',
     'OBJEKTREDIGERARE'),

    # ── Column headers ─────────────────────────────────────────────────────────
    ('fqc_col_desc',
     'Descrizione',
     'Description',
     'Descriere',
     'Beschreibung',
     'Beskrivning'),

    ('fqc_col_photo',
     'Foto',
     'Photo',
     'Fotografie',
     'Foto',
     'Foto'),

    ('fqc_col_note',
     'Nota (obbligatoria se NOK)',
     'Note (required if NOK)',
     'Nota (obligatorie daca NOK)',
     'Notiz (erforderlich bei NOK)',
     'Anteckning (obligatorisk vid NOK)'),

    # ── Item editor labels ─────────────────────────────────────────────────────
    ('fqc_item_desc',
     'Descrizione:',
     'Description:',
     'Descriere:',
     'Beschreibung:',
     'Beskrivning:'),

    ('fqc_browse_photo',
     '📷 Sfoglia foto...',
     '📷 Browse photo...',
     '📷 Cauta fotografie...',
     '📷 Foto durchsuchen...',
     '📷 Bläddra foto...'),

    ('fqc_no_photo',
     'Nessuna foto',
     'No photo',
     'Fara fotografie',
     'Kein Foto',
     'Inget foto'),

    ('fqc_select_photo',
     'Seleziona foto',
     'Select photo',
     'Selectati fotografia',
     'Foto auswählen',
     'Välj foto'),

    # ── Buttons ────────────────────────────────────────────────────────────────
    ('fqc_save_checklist',
     '✔ Salva Risultati',
     '✔ Save Results',
     '✔ Salveaza Rezultatele',
     '✔ Ergebnisse speichern',
     '✔ Spara resultat'),

    ('fqc_save_header',
     '💾 Salva Intestazione',
     '💾 Save Header',
     '💾 Salveaza Antet',
     '💾 Kopf speichern',
     '💾 Spara rubrik'),

    ('fqc_add_item',
     '+ Aggiungi Voce',
     '+ Add Item',
     '+ Adauga Element',
     '+ Element hinzufügen',
     '+ Lägg till objekt'),

    ('fqc_edit_item',
     '✏ Modifica',
     '✏ Edit',
     '✏ Modifica',
     '✏ Bearbeiten',
     '✏ Redigera'),

    ('fqc_delete_item',
     '🗑 Elimina (logico)',
     '🗑 Delete (logical)',
     '🗑 Sterge (logic)',
     '🗑 Löschen (logisch)',
     '🗑 Ta bort (logisk)'),

    ('fqc_save_item',
     '💾 Salva Voce',
     '💾 Save Item',
     '💾 Salveaza Elementul',
     '💾 Element speichern',
     '💾 Spara objekt'),

    ('fqc_save_feedback',
     '💾 Salva Feedback',
     '💾 Save Feedback',
     '💾 Salveaza Feedback',
     '💾 Feedback speichern',
     '💾 Spara feedback'),

    # ── Status / info messages ─────────────────────────────────────────────────
    ('fqc_select_product',
     'Selezionare un cliente e un prodotto per caricare la checklist.',
     'Select a client and product to load the checklist.',
     'Selectati un client si un produs pentru a incarca lista de verificare.',
     'Wählen Sie einen Kunden und ein Produkt, um die Checkliste zu laden.',
     'Välj en kund och ett produkt för att läsa in checklistan.'),

    ('fqc_no_checklist',
     '⚠ Nessuna checklist attiva per questo prodotto.',
     '⚠ No active checklist for this product.',
     '⚠ Nu exista o lista de verificare activa pentru acest produs.',
     '⚠ Keine aktive Checkliste für dieses Produkt.',
     '⚠ Ingen aktiv checklista för denna produkt.'),

    ('fqc_no_checklist_admin',
     '⚠ Nessuna checklist — inserire il nome e cliccare Salva Intestazione per creare.',
     '⚠ No checklist — enter name and click Save Header to create.',
     '⚠ Nicio lista — introduceti numele si apasati Salveaza Antet pentru a crea.',
     '⚠ Keine Checkliste — Name eingeben und Kopf speichern klicken zum Erstellen.',
     '⚠ Ingen checklista — ange namn och klicka Spara rubrik för att skapa.'),

    ('fqc_select_product_first',
     'Selezionare prima un prodotto.',
     'Please select a product first.',
     'Va rugam sa selectati mai intai un produs.',
     'Bitte zuerst ein Produkt auswählen.',
     'Välj ett produkt först.'),

    ('fqc_save_header_first',
     'Salvare prima l\'intestazione della checklist.',
     'Save the checklist header first.',
     'Salvati mai intai antetul listei de verificare.',
     'Bitte zuerst den Checklisten-Kopf speichern.',
     'Spara checklisthuvudet först.'),

    ('fqc_select_item',
     'Selezionare prima una voce dall\'elenco.',
     'Select an item from the list first.',
     'Selectati mai intai un element din lista.',
     'Bitte zuerst ein Element aus der Liste auswählen.',
     'Välj ett objekt från listan först.'),

    ('fqc_confirm_delete',
     'Contrassegnare questa voce come eliminata? (eliminazione logica)',
     'Mark this item as deleted? (soft delete)',
     'Marcati acest element ca sters? (stergere logica)',
     'Dieses Element als gelöscht markieren? (Soft-Delete)',
     'Markera detta objekt som borttaget? (mjuk borttagning)'),

    # ── Validation ─────────────────────────────────────────────────────────────
    ('fqc_unanswered',
     'Rispondere a tutte le voci prima di salvare.',
     'Please answer all items before saving.',
     'Va rugam sa raspundeti la toate elementele inainte de a salva.',
     'Bitte alle Elemente beantworten, bevor Sie speichern.',
     'Svara på alla objekt innan du sparar.'),

    ('fqc_note_required',
     'Una nota è obbligatoria per tutte le voci NOK.',
     'A note is required for all NOK items.',
     'O nota este obligatorie pentru toate elementele NOK.',
     'Eine Notiz ist für alle NOK-Elemente erforderlich.',
     'En anteckning krävs för alla NOK-objekt.'),

    ('fqc_desc_required',
     'La descrizione è obbligatoria.',
     'Description is required.',
     'Descrierea este obligatorie.',
     'Beschreibung ist erforderlich.',
     'Beskrivning krävs.'),

    ('fqc_cl_name_required',
     'Il nome della checklist è obbligatorio.',
     'Checklist name is required.',
     'Numele listei de verificare este obligatoriu.',
     'Checklistenname ist erforderlich.',
     'Checklistnamn krävs.'),

    ('fqc_photo_required',
     'È necessaria una foto per ogni voce della checklist.',
     'A photo is required for each checklist item.',
     'O fotografie este necesara pentru fiecare element al listei de verificare.',
     'Für jedes Checklistenelement ist ein Foto erforderlich.',
     'Ett foto krävs för varje checklistobjekt.'),

    ('fqc_fb_text_required',
     'Il testo del feedback è obbligatorio.',
     'Feedback text is required.',
     'Textul de feedback este obligatoriu.',
     'Feedback-Text ist erforderlich.',
     'Feedbacktext krävs.'),

    ('fqc_date_format',
     'La data deve essere nel formato YYYY-MM-DD.',
     'Date must be in YYYY-MM-DD format.',
     'Data trebuie sa fie in formatul AAAA-LL-ZZ.',
     'Datum muss im Format JJJJ-MM-TT sein.',
     'Datum måste vara i formatet ÅÅÅÅ-MM-DD.'),

    # ── Success messages ───────────────────────────────────────────────────────
    ('fqc_saved',
     'Risultati checklist salvati con successo.',
     'Checklist results saved successfully.',
     'Rezultatele listei de verificare au fost salvate cu succes.',
     'Checklisten-Ergebnisse erfolgreich gespeichert.',
     'Checklistresultat sparades framgångsrikt.'),

    ('fqc_feedback_saved',
     'Feedback salvato con successo.',
     'Feedback saved successfully.',
     'Feedback-ul a fost salvat cu succes.',
     'Feedback erfolgreich gespeichert.',
     'Feedback sparades framgångsrikt.'),

    # ── Feedback form ──────────────────────────────────────────────────────────
    ('fqc_nok_logs',
     'RISULTATI CHECKLIST NOK',
     'NOK CHECKLIST RESULTS',
     'REZULTATE LISTA DE VERIFICARE NOK',
     'NOK-CHECKLISTENERGEBNISSE',
     'NOK CHECKLISTRESULTAT'),

    ('fqc_feedback_form',
     'FEEDBACK CLIENTE',
     'CUSTOMER FEEDBACK',
     'FEEDBACK CLIENT',
     'KUNDENFEEDBACK',
     'KUNDFEEDBACK'),

    ('fqc_feedback_text',
     'Feedback:',
     'Feedback:',
     'Feedback:',
     'Feedback:',
     'Feedback:'),

    ('fqc_fb_from',
     'Da:',
     'From:',
     'De la:',
     'Von:',
     'Från:'),

    ('fqc_fb_date',
     'Data:',
     'Date:',
     'Data:',
     'Datum:',
     'Datum:'),

    ('fqc_date',
     'Data',
     'Date',
     'Data',
     'Datum',
     'Datum'),

    ('fqc_item',
     'Voce',
     'Item',
     'Element',
     'Element',
     'Objekt'),

    ('fqc_user',
     'Utente',
     'User',
     'Utilizator',
     'Benutzer',
     'Användare'),

    ('fqc_note_fb',
     'Nota NOK',
     'NOK Note',
     'Nota NOK',
     'NOK-Notiz',
     'NOK-anteckning'),

    ('fqc_photo_preview',
     'Anteprima Foto',
     'Photo Preview',
     'Previzualizare Fotografie',
     'Fotovorschau',
     'Fotoförhandsvisning'),
]

LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = _get_conn()
    cur  = conn.cursor()
    inserted = skipped = 0

    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            val = row[i + 1]
            cur.execute(
                "SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                "WHERE LanguageCode = ? AND TranslationKey = ?",
                (lang, key)
            )
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "INSERT INTO Traceability_rs.dbo.AppTranslations "
                    "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                    (lang, key, val)
                )
                inserted += 1
            else:
                skipped += 1

    conn.commit()
    conn.close()
    print(f'[OK] FQC translations — Inserted: {inserted}, Skipped (already present): {skipped}')


if __name__ == '__main__':
    main()
