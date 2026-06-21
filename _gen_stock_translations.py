# -*- coding: utf-8 -*-
"""Generatore di indirect_materials_stock_translations.sql.
Esegui: python _gen_stock_translations.py
Crea/sovrascrive lo script SQL con INSERT idempotenti per le 5 lingue.
"""

# key -> (it, en, ro, de, sv)
T = {
    # --- Voci di menu ---
    "submenu_check_stock": (
        "\U0001F4E6 Verifica Giacenze", "\U0001F4E6 Check Stock",
        "\U0001F4E6 Verificare Stocuri", "\U0001F4E6 Bestand prüfen",
        "\U0001F4E6 Kontrollera lager"),
    "submenu_min_stock_config": (
        "⚙ Configura Scorte Minime", "⚙ Configure Minimum Stock",
        "⚙ Configurare Stoc Minim", "⚙ Mindestbestand konfigurieren",
        "⚙ Konfigurera minimilager"),
    "submenu_consumption_indirect_materials": (
        "\U0001F4C9 Analisi Consumi & Budget", "\U0001F4C9 Consumption & Budget Analysis",
        "\U0001F4C9 Analiză Consumuri & Buget", "\U0001F4C9 Verbrauchs- & Budgetanalyse",
        "\U0001F4C9 Förbruknings- & budgetanalys"),

    # --- Verifica Giacenze ---
    "ind_stock_title": (
        "Verifica Giacenze Materiali Indiretti", "Indirect Materials Stock Check",
        "Verificare Stoc Materiale Indirecte", "Bestandsprüfung Indirektes Material",
        "Lagerkontroll indirekta material"),
    "ind_stock_header": (
        "Giacenze Materiali Indiretti", "Indirect Materials Stock",
        "Stoc Materiale Indirecte", "Bestand Indirektes Material",
        "Lager indirekta material"),
    "ind_stock_export": (
        "\U0001F4CA Esporta Excel", "\U0001F4CA Export Excel",
        "\U0001F4CA Export Excel", "\U0001F4CA Excel exportieren",
        "\U0001F4CA Exportera Excel"),
    "ind_stock_send_reorder": (
        "\U0001F4E4 Invia riordino ora", "\U0001F4E4 Send reorder now",
        "\U0001F4E4 Trimite recomandă acum", "\U0001F4E4 Nachbestellung jetzt senden",
        "\U0001F4E4 Skicka beställning nu"),
    "ind_stock_only_below": (
        "Solo sotto scorta minima", "Only below minimum stock",
        "Doar sub stoc minim", "Nur unter Mindestbestand",
        "Endast under minimilager"),
    "ind_stock_col_stock": ("Giacenza", "Stock", "Stoc", "Bestand", "Lager"),
    "ind_stock_col_status": ("Stato", "Status", "Stare", "Status", "Status"),
    "ind_stock_col_movtype": ("Tipo", "Type", "Tip", "Typ", "Typ"),
    "ind_stock_below": (
        "⚠ Sotto minimo", "⚠ Below minimum",
        "⚠ Sub minim", "⚠ Unter Minimum", "⚠ Under minimum"),
    "ind_stock_ok": ("OK", "OK", "OK", "OK", "OK"),
    "ind_stock_unmanaged": (
        "Non gestito", "Not managed", "Negestionat", "Nicht verwaltet", "Ej hanterad"),
    "ind_stock_movements": (
        "Ultimi movimenti", "Recent movements", "Mişcări recente",
        "Letzte Bewegungen", "Senaste rörelser"),
    "ind_stock_status": (
        "{0} materiali · {1} sotto scorta minima",
        "{0} materials · {1} below minimum stock",
        "{0} materiale · {1} sub stoc minim",
        "{0} Materialien · {1} unter Mindestbestand",
        "{0} material · {1} under minimilager"),
    "ind_stock_reorder_confirm": (
        "Inviare ora la richiesta di riordino per i materiali sotto scorta minima?",
        "Send the reorder request now for materials below minimum stock?",
        "Trimiteți acum cererea de recomandă pentru materialele sub stoc minim?",
        "Nachbestellung für Materialien unter Mindestbestand jetzt senden?",
        "Skicka beställning nu för material under minimilager?"),
    "ind_stock_reorder_sent": (
        "Riordino inviato per {0} materiali a {1} destinatari.",
        "Reorder sent for {0} materials to {1} recipients.",
        "Recomandă trimisă pentru {0} materiale către {1} destinatari.",
        "Nachbestellung für {0} Materialien an {1} Empfänger gesendet.",
        "Beställning skickad för {0} material till {1} mottagare."),
    "ind_stock_reorder_none": (
        "Nessun materiale sotto scorta minima.", "No materials below minimum stock.",
        "Niciun material sub stoc minim.", "Keine Materialien unter Mindestbestand.",
        "Inga material under minimilager."),
    "ind_stock_reorder_no_recipients": (
        "Nessun destinatario configurato (Settings: {0}).",
        "No recipient configured (Settings: {0}).",
        "Niciun destinatar configurat (Settings: {0}).",
        "Kein Empfänger konfiguriert (Settings: {0}).",
        "Ingen mottagare konfigurerad (Settings: {0})."),
    "ind_stock_reorder_error": (
        "Invio riordino non riuscito: {0}", "Reorder sending failed: {0}",
        "Trimiterea recomenzării a eşuat: {0}", "Nachbestellung fehlgeschlagen: {0}",
        "Beställning misslyckades: {0}"),
    "ind_stock_save_excel": (
        "Salva Giacenze Excel", "Save Stock Excel", "Salvați Stoc Excel",
        "Bestand Excel speichern", "Spara lager Excel"),
    "ind_stock_export_ok": (
        "Export completato:\n{0}", "Export completed:\n{0}",
        "Export finalizat:\n{0}", "Export abgeschlossen:\n{0}", "Export klar:\n{0}"),

    # --- Configura Scorte Minime ---
    "ind_min_title": (
        "Configura Scorte Minime", "Configure Minimum Stock",
        "Configurare Stoc Minim", "Mindestbestand konfigurieren",
        "Konfigurera minimilager"),
    "ind_min_header": (
        "Scorte minime materiali indiretti", "Indirect materials minimum stock",
        "Stoc minim materiale indirecte", "Mindestbestand indirektes Material",
        "Minimilager indirekta material"),
    "ind_min_col_min": (
        "Scorta minima", "Minimum stock", "Stoc minim", "Mindestbestand", "Minimilager"),
    "ind_min_col_lot": (
        "Lotto riordino", "Reorder lot", "Lot recomandă",
        "Nachbestellmenge", "Beställningsparti"),
    "ind_min_col_active": (
        "Riordino attivo", "Reorder active", "Recomandă activă",
        "Nachbestellung aktiv", "Beställning aktiv"),
    "ind_min_editor": (
        "Configurazione codice selezionato", "Selected code configuration",
        "Configurare cod selectat", "Konfiguration ausgewählter Code",
        "Konfiguration vald kod"),
    "ind_min_no_sel": (
        "Nessun codice selezionato", "No code selected", "Niciun cod selectat",
        "Kein Code ausgewählt", "Ingen kod vald"),
    "ind_min_invalid_min": (
        "Scorta minima non valida.", "Invalid minimum stock.",
        "Stoc minim invalid.", "Ungültiger Mindestbestand.", "Ogiltigt minimilager."),
    "ind_min_invalid_lot": (
        "Lotto riordino non valido.", "Invalid reorder lot.",
        "Lot recomandă invalid.", "Ungültige Nachbestellmenge.",
        "Ogiltigt beställningsparti."),
    "ind_min_saved": (
        "Configurazione salvata.", "Configuration saved.",
        "Configurare salvată.", "Konfiguration gespeichert.", "Konfiguration sparad."),

    # --- Email riordino ---
    "ind_reorder_email_subject": (
        "Richiesta riordino materiali indiretti sotto scorta minima",
        "Reorder request: indirect materials below minimum stock",
        "Cerere recomandă materiale indirecte sub stoc minim",
        "Nachbestellanforderung: indirektes Material unter Mindestbestand",
        "Beställningsförfrågan: indirekta material under minimilager"),
    "ind_reorder_email_intro": (
        "I seguenti materiali indiretti sono scesi sotto la scorta minima e necessitano di riordino:",
        "The following indirect materials are below minimum stock and need reordering:",
        "Următoarele materiale indirecte sunt sub stocul minim şi necesită recomandă:",
        "Die folgenden indirekten Materialien sind unter dem Mindestbestand und müssen nachbestellt werden:",
        "Följande indirekta material är under minimilager och behöver beställas:"),
    "ind_reorder_email_footer": (
        "Email generata automaticamente dal sistema Document Management.",
        "Email generated automatically by the Document Management system.",
        "Email generat automat de sistemul Document Management.",
        "E-Mail automatisch vom Document-Management-System generiert.",
        "E-post genererad automatiskt av Document Management-systemet."),

    # --- Richieste: avanzamento stato ---
    "ind_req_btn_prepared": (
        "Segna Preparata", "Mark Prepared", "Marchează Pregătită",
        "Als vorbereitet markieren", "Markera förberedd"),
    "ind_req_btn_picked": (
        "✅ Conferma Prelievo (scarico)", "✅ Confirm Pick (stock out)",
        "✅ Confirmă Ridicare (descărcare)", "✅ Entnahme bestätigen (Abgang)",
        "✅ Bekräfta uttag (lageruttag)"),
    "ind_req_btn_cancel": (
        "Annulla richiesta", "Cancel request", "Anulează cererea",
        "Anfrage stornieren", "Avbryt begäran"),
    "ind_req_select_row": (
        "Seleziona una richiesta.", "Select a request.", "Selectați o cerere.",
        "Wählen Sie eine Anfrage.", "Välj en begäran."),
    "ind_req_state_no_change": (
        "Impossibile cambiare lo stato (già prelevata o annullata?).",
        "Cannot change status (already picked or cancelled?).",
        "Nu se poate schimba starea (deja ridicată sau anulată?).",
        "Status kann nicht geändert werden (bereits entnommen oder storniert?).",
        "Kan inte ändra status (redan uttagen eller avbruten?)."),
    "ind_req_confirm_pick": (
        "Confermare il prelievo? Verrà generato lo scarico di magazzino.",
        "Confirm pick? A stock-out movement will be generated.",
        "Confirmați ridicarea? Se va genera descărcarea din stoc.",
        "Entnahme bestätigen? Ein Lagerabgang wird erzeugt.",
        "Bekräfta uttag? Ett lageruttag genereras."),
    "ind_req_pick_ok": (
        "Prelievo confermato e scarico registrato.",
        "Pick confirmed and stock-out recorded.",
        "Ridicare confirmată şi descărcare înregistrată.",
        "Entnahme bestätigt und Abgang erfasst.",
        "Uttag bekräftat och lageruttag registrerat."),
    "ind_req_already_picked": (
        "Richiesta già prelevata.", "Request already picked.",
        "Cererea a fost deja ridicată.", "Anfrage bereits entnommen.",
        "Begäran redan uttagen."),
    "ind_req_is_cancelled": (
        "La richiesta è annullata.", "The request is cancelled.",
        "Cererea este anulată.", "Die Anfrage ist storniert.",
        "Begäran är avbruten."),
    "ind_req_pick_error": (
        "Scarico non riuscito: {0}", "Stock-out failed: {0}",
        "Descărcarea a eşuat: {0}", "Abgang fehlgeschlagen: {0}",
        "Lageruttag misslyckades: {0}"),
    "ind_req_confirm_cancel": (
        "Annullare la richiesta selezionata?", "Cancel the selected request?",
        "Anulați cererea selectată?", "Ausgewählte Anfrage stornieren?",
        "Avbryt vald begäran?"),
    "ind_req_col_note": ("Note", "Notes", "Note", "Notizen", "Anteckningar"),
    "ind_req_col_type": ("Tipo", "Type", "Tip", "Typ", "Typ"),

    # --- Analisi Consumi & Budget ---
    "ind_cons_title": (
        "Analisi Consumi & Budget Materiali Indiretti",
        "Indirect Materials Consumption & Budget Analysis",
        "Analiză Consumuri & Buget Materiale Indirecte",
        "Verbrauchs- & Budgetanalyse Indirektes Material",
        "Förbruknings- & budgetanalys indirekta material"),
    "ind_cons_header": (
        "Analisi Consumi", "Consumption Analysis", "Analiză Consumuri",
        "Verbrauchsanalyse", "Förbruksanalys"),
    "ind_cons_export": (
        "\U0001F4CA Esporta Excel", "\U0001F4CA Export Excel", "\U0001F4CA Export Excel",
        "\U0001F4CA Excel exportieren", "\U0001F4CA Exportera Excel"),
    "ind_cons_tab_week": ("Settimanale", "Weekly", "Săptămânal", "Wöchentlich", "Veckovis"),
    "ind_cons_tab_month": ("Mensile", "Monthly", "Lunar", "Monatlich", "Månatlig"),
    "ind_cons_tab_year": ("Annuale", "Yearly", "Anual", "Jährlich", "Årlig"),
    "ind_cons_tab_budget": (
        "Budget anno prossimo", "Next year budget", "Buget anul viitor",
        "Budget nächstes Jahr", "Budget nästa år"),
    "ind_cons_col_period": ("Periodo", "Period", "Perioadă", "Zeitraum", "Period"),
    "ind_cons_col_consumption": ("Consumo", "Consumption", "Consum", "Verbrauch", "Förbrukning"),
    "ind_cons_col_moves": ("N. movimenti", "No. movements", "Nr. mişcări",
                           "Anz. Bewegungen", "Antal rörelser"),
    "ind_cons_col_year": ("Anno", "Year", "An", "Jahr", "År"),
    "ind_cons_growth": (
        "Crescita % attesa:", "Expected growth %:", "Creştere % aşteptată:",
        "Erwartetes Wachstum %:", "Förväntad tillväxt %:"),
    "ind_cons_recalc": (
        "Ricalcola budget", "Recalculate budget", "Recalculează buget",
        "Budget neu berechnen", "Beräkna om budget"),
    "ind_cons_col_12m": (
        "Consumo 12 mesi", "12-month consumption", "Consum 12 luni",
        "Verbrauch 12 Monate", "Förbrukning 12 månader"),
    "ind_cons_col_budget_year": (
        "Budget annuo", "Annual budget", "Buget anual", "Jahresbudget", "Årsbudget"),
    "ind_cons_col_budget_month": (
        "Budget mensile", "Monthly budget", "Buget lunar", "Monatsbudget", "Månadsbudget"),
    "ind_cons_save_excel": (
        "Salva Consumi Excel", "Save Consumption Excel", "Salvați Consumuri Excel",
        "Verbrauch Excel speichern", "Spara förbrukning Excel"),
    "ind_cons_export_ok": (
        "Export completato:\n{0}", "Export completed:\n{0}",
        "Export finalizat:\n{0}", "Export abgeschlossen:\n{0}", "Export klar:\n{0}"),

    # --- Menu Help ---
    "menu_stock_management_manual": (
        "Gestione Giacenze & Riordino (Manuale)", "Stock Management & Reorder (Manual)",
        "Gestionare Stoc & Recomandă (Manual)", "Bestandsverwaltung & Nachbestellung (Handbuch)",
        "Lagerhantering & beställning (Handbok)"),
    "stock_management_manual_not_found": (
        "Il manuale Gestione Giacenze non è stato trovato.",
        "The Stock Management manual was not found.",
        "Manualul Gestionare Stoc nu a fost găsit.",
        "Das Handbuch zur Bestandsverwaltung wurde nicht gefunden.",
        "Handboken för lagerhantering hittades inte."),

    # --- Comuni eventualmente mancanti (idempotenti) ---
    "yes": ("Sì", "Yes", "Da", "Ja", "Ja"),
    "no": ("No", "No", "Nu", "Nein", "Nej"),
    "btn_save": ("Salva", "Save", "Salvează", "Speichern", "Spara"),
    "btn_refresh": ("Aggiorna", "Refresh", "Actualizează", "Aktualisieren", "Uppdatera"),
}

LANGS = ['it', 'en', 'ro', 'de', 'sv']


def esc(s):
    return s.replace("'", "''")


def main():
    lines = [
        "-- ============================================================================",
        "-- Traduzioni per Giacenze / Riordino / Consumi Materiali Indiretti",
        "-- Tabella: [Traceability_RS].[dbo].[AppTranslations]",
        "-- Generato da _gen_stock_translations.py",
        "-- ============================================================================",
        "",
    ]
    for key, vals in T.items():
        lines.append(f"-- {key}")
        for lang, val in zip(LANGS, vals):
            v = esc(val)
            lines.append(
                "IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] "
                f"WHERE TranslationKey = '{key}' AND LanguageCode = '{lang}')")
            lines.append(
                "    INSERT INTO [dbo].[AppTranslations] (LanguageCode, TranslationKey, TranslationValue) "
                f"VALUES ('{lang}', '{key}', N'{v}');")
        lines.append("")
    lines.append("PRINT 'Traduzioni giacenze/riordino/consumi inserite.';")

    out = "\n".join(lines)
    with open("indirect_materials_stock_translations.sql", "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Generato indirect_materials_stock_translations.sql ({len(T)} chiavi, {len(T)*5} insert).")


if __name__ == "__main__":
    main()
