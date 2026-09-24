# -*- coding: utf-8 -*-
"""Generatore per incoming/add_incoming_translations_gui.sql (5 lingue)."""
import os

# chiave -> (it, en, ro, de, sv)
T = {
 # colonne treeview / etichette comuni
 'inc_col_age': ('Età (min)', 'Age (min)', 'Vârstă (min)', 'Alter (Min)', 'Ålder (min)'),
 'inc_col_answered_by': ('Risposta di', 'Answered by', 'Răspuns de', 'Beantwortet von', 'Besvarad av'),
 'inc_col_answered_on': ('Risposto il', 'Answered on', 'Răspuns la', 'Beantwortet am', 'Besvarad den'),
 'inc_col_by': ('Richiesto da', 'Requested by', 'Solicitat de', 'Angefragt von', 'Begärd av'),
 'inc_col_ddt': ('DDT', 'Del. note', 'Aviz', 'Lieferschein', 'Fraktsedel'),
 'inc_col_mpn': ('MPN', 'MPN', 'MPN', 'MPN', 'MPN'),
 'inc_col_number': ('Numero', 'Number', 'Număr', 'Nummer', 'Nummer'),
 'inc_col_po': ('P.O.', 'P.O.', 'P.O.', 'B.O.', 'P.O.'),
 'inc_col_qty': ('Q.tà', 'Qty', 'Cant.', 'Menge', 'Antal'),
 'inc_col_status': ('Stato', 'Status', 'Stare', 'Status', 'Status'),
 'inc_col_supplier': ('Fornitore', 'Supplier', 'Furnizor', 'Lieferant', 'Leverantör'),
 'inc_col_type': ('Tipo', 'Type', 'Tip', 'Typ', 'Typ'),
 # conferma soluzioni
 'inc_conf_already_confirmed': ('Richiesta già confermata da un altro operatore.',
   'Request already confirmed by another operator.',
   'Cerere deja confirmată de alt operator.',
   'Anfrage bereits von einem anderen Bediener bestätigt.',
   'Begäran redan bekräftad av en annan operatör.'),
 'inc_conf_answer': ('Risposta ricevuta:', 'Answer received:', 'Răspuns primit:', 'Antwort erhalten:', 'Svar mottaget:'),
 'inc_conf_confirm_ko': ('Segnalare la soluzione di {0} come NON risolutiva?\nLa richiesta tornerà in stato KO.',
   'Report the solution for {0} as NOT resolving?\nThe request will be marked KO.',
   'Marcați soluția pentru {0} ca NEREZOLVANTĂ?\nCererea va trece în stare KO.',
   'Lösung für {0} als NICHT lösend melden?\nDie Anfrage wird als KO markiert.',
   'Ange lösningen för {0} som EJ lönsam?\nBegäran markeras KO.'),
 'inc_conf_confirm_ok': ('Confermare la soluzione per {0}?', 'Confirm the solution for {0}?',
   'Confirmați soluția pentru {0}?', 'Lösung für {0} bestätigen?', 'Bekräfta lösningen för {0}?'),
 'inc_conf_confirmed_on': ('Confermato il', 'Confirmed on', 'Confirmat la', 'Bestätigt am', 'Bekräftad den'),
 'inc_conf_detail': ('Dettaglio richiesta e risposta', 'Request and answer detail',
   'Detalii cerere și răspuns', 'Details zur Anfrage und Antwort', 'Detalj för begäran och svar'),
 'inc_conf_filter_status': ('Stato:', 'Status:', 'Stare:', 'Status:', 'Status:'),
 'inc_conf_ko': ('✘ Soluzione non risolutiva', '✘ Solution not resolving', '✘ Soluție nerezolvativă',
   '✘ Lösung nicht lösend', '✘ Lösning inte lönsam'),
 'inc_conf_ok': ('✔ Conferma soluzione', '✔ Confirm solution', '✔ Confirmă soluția',
   '✔ Lösung bestätigen', '✔ Bekräfta lösning'),
 'inc_conf_title': ('Conferma soluzioni — Ricezione', 'Confirm solutions — Receiving',
   'Confirmare soluții — Recepție', 'Lösungen bestätigen — Wareneingang', 'Bekräfta lösningar — Inleverans'),
 # form richiesta
 'inc_req_data': ('Dati richiesta', 'Request data', 'Date cerere', 'Anfragedaten', 'Begärandata'),
 'inc_req_component_code': ('Codice interno (componente):', 'Internal code (component):',
   'Cod intern (component):', 'Interner Code (Komponente):', 'Intern kod (komponent):'),
 'inc_req_ddt_date': ('Data DDT:', 'Delivery note date:', 'Data aviz:', 'Lieferscheindatum:', 'Fraktsedeldatum:'),
 'inc_req_ddt_date_required': ('Inserire la data DDT.', 'Enter the delivery note date.',
   'Introduceți data avizului.', 'Lieferscheindatum eingeben.', 'Ange fraktsedeldatum.'),
 'inc_req_ddt_number': ('Numero DDT:', 'Delivery note no.:', 'Număr aviz:', 'Lieferschein-Nr.:', 'Fraktsedelnr:'),
 'inc_req_ddt_required': ('Inserire il numero DDT.', 'Enter the delivery note number.',
   'Introduceți numărul avizului.', 'Lieferscheinnummer eingeben.', 'Ange fraktsedelnummer.'),
 'inc_req_field_required': ('Compilare il campo richiesto ({0}).', 'Fill in the required field ({0}).',
   'Completați câmpul obligatoriu ({0}).', 'Pflichtfeld ausfüllen ({0}).', 'Fyll i obligatoriskt fält ({0}).'),
 'inc_req_mpn': ('Codice MPN', 'MPN code', 'Cod MPN', 'MPN-Code', 'MPN-kod'),
 'inc_req_po': ('Numero P.O.', 'P.O. number', 'Număr P.O.', 'B.O.-Nummer', 'P.O.-nummer'),
 'inc_req_popup_msg': ('{0} — Fornitore: {1} — DDT: {2} — Da: {3}',
   '{0} — Supplier: {1} — Del. note: {2} — From: {3}',
   '{0} — Furnizor: {1} — Aviz: {2} — De la: {3}',
   '{0} — Lieferant: {1} — Lieferschein: {2} — Von: {3}',
   '{0} — Leverantör: {1} — Fraktsedel: {2} — Från: {3}'),
 'inc_req_popup_code': ('Codice: {0}', 'Code: {0}', 'Cod: {0}', 'Code: {0}', 'Kod: {0}'),
 'inc_req_popup_title': ('Nuova richiesta Ricezione — {0}', 'New receiving request — {0}',
   'Cerere nouă Recepție — {0}', 'Neue Wareneingang-Anfrage — {0}', 'Ny inleveransförfrågan — {0}'),
 'inc_req_qty_expected': ('Quantità attesa da P.O.', 'Qty expected per P.O.', 'Cantitate așteptată P.O.',
   'Erwartete Menge laut B.O.', 'Antal enligt P.O.'),
 'inc_req_qty_invalid': ('Quantità non valida in {0}.', 'Invalid quantity in {0}.',
   'Cantitate invalidă în {0}.', 'Ungültige Menge in {0}.', 'Ogiltigt antal i {0}.'),
 'inc_req_qty_receive': ('Quantità da ricevere', 'Qty to receive', 'Cantitate de recepționat',
   'Zu erhaltende Menge', 'Antal att ta emot'),
 'inc_req_reset': ('Azzera campi', 'Clear fields', 'Resetează câmpuri', 'Felder leeren', 'Rensa fält'),
 'inc_req_save_error': ('Errore durante il salvataggio della richiesta:\n{0}', 'Error saving the request:\n{0}',
   'Eroare la salvarea cererii:\n{0}', 'Fehler beim Speichern der Anfrage:\n{0}', 'Fel vid sparande av begäran:\n{0}'),
 'inc_req_select_supplier': ("Seleziona un fornitore dall'elenco.", 'Select a supplier from the list.',
   'Selectați un furnizor din listă.', 'Lieferanten aus der Liste wählen.', 'Välj en leverantör från listan.'),
 'inc_req_select_type': ('Seleziona il tipo di richiesta.', 'Select the request type.',
   'Selectați tipul cererii.', 'Anfrageart wählen.', 'Välj förfrågningstyp.'),
 'inc_req_send': ('📨 Invia richiesta', '📨 Send request', '📨 Trimite cererea', '📨 Anfrage senden', '📨 Skicka förfrågan'),
 'inc_req_sent': ('Richiesta {0} inviata.', 'Request {0} sent.', 'Cererea {0} a fost trimisă.',
   'Anfrage {0} gesendet.', 'Begäran {0} skickad.'),
 'inc_req_supplier': ('Fornitore:', 'Supplier:', 'Furnizor:', 'Lieferant:', 'Leverantör:'),
 'inc_req_suppliers_error': ("Impossibile caricare l'elenco fornitori.", 'Unable to load the supplier list.',
   'Imposibil de încărcat lista furnizori.', 'Lieferantenliste konnte nicht geladen werden.',
   'Det gick inte att läsa in leverantörslistan.'),
 'inc_req_title': ('Nuova richiesta — Ricezione', 'New request — Receiving', 'Cerere nouă — Recepție',
   'Neue Anfrage — Wareneingang', 'Ny förfrågan — Inleverans'),
 'inc_req_type': ('Tipo richiesta:', 'Request type:', 'Tip cerere:', 'Anfrageart:', 'Förfrågningstyp:'),
 'inc_req_wrong_mpn': ('MPN errato', 'Wrong MPN', 'MPN greșit', 'Falsche MPN', 'Felaktig MPN'),
 # soluzioni
 'inc_sol_all_types': ('(tutti)', '(all)', '(toate)', '(alle)', '(alla)'),
 'inc_sol_already_answered': ('Richiesta già risolta da un altro operatore.',
   'Request already resolved by another operator.', 'Cerere deja rezolvată de alt operator.',
   'Anfrage bereits von einem anderen Bediener gelöst.', 'Begäran redan löst av en annan operatör.'),
 'inc_sol_answer_mpn': ('MPN corretto', 'Correct MPN', 'MPN corect', 'Korrekte MPN', 'Korrekt MPN'),
 'inc_sol_answer_text': ('Soluzione / nota:', 'Solution / note:', 'Soluție / notă:',
   'Lösung / Anmerkung:', 'Lösning / anteckning:'),
 'inc_sol_confirm_send': ('Inviare la risposta a {0}?', 'Send the answer to {0}?',
   'Trimiteți răspunsul către {0}?', 'Antwort an {0} senden?', 'Skicka svaret till {0}?'),
 'inc_sol_detail': ('Dettaglio richiesta e soluzione', 'Request and solution detail',
   'Detalii cerere și soluție', 'Details zur Anfrage und Lösung', 'Detalj för begäran och lösning'),
 'inc_sol_filter_type': ('Tipo:', 'Type:', 'Tip:', 'Typ:', 'Typ:'),
 'inc_sol_mpn_required': ('Inserire il codice MPN corretto.', 'Enter the correct MPN code.',
   'Introduceți codul MPN corect.', 'Korrekten MPN-Code eingeben.', 'Ange korrekt MPN-kod.'),
 'inc_sol_outlook_email': ('📧 Crea email soluzione (Outlook)', '📧 Create solution email (Outlook)',
   '📧 Creează email soluție (Outlook)', '📧 Lösungs-E-Mail erstellen (Outlook)',
   '📧 Skapa lösningsepost (Outlook)'),
 'inc_sol_setup_recipients': ('⚙ Destinatari…', '⚙ Recipients…', '⚙ Destinatari…',
   '⚙ Empfänger…', '⚙ Mottagare…'),
 'inc_sol_outlook_failed': ('Impossibile aprire Outlook per creare la email.',
   'Unable to open Outlook to create the email.',
   'Imposibil de deschis Outlook pentru a crea emailul.',
   'Outlook konnte nicht zum Erstellen der E-Mail geöffnet werden.',
   'Det gick inte att öppna Outlook för att skapa e-posten.'),
 'inc_sol_pending': ('in attesa', 'pending', 'în așteptare', 'ausstehend', 'väntar'),
 'inc_sol_popup_msg': ('La richiesta {0} ha una risposta da {1}.\nMPN: {2}\n{3}',
   'Request {0} has an answer from {1}.\nMPN: {2}\n{3}',
   'Cererea {0} are un răspuns de la {1}.\nMPN: {2}\n{3}',
   'Anfrage {0} hat eine Antwort von {1}.\nMPN: {2}\n{3}',
   'Begäran {0} har ett svar från {1}.\nMPN: {2}\n{3}'),
 'inc_sol_popup_title': ('Risposta pronta — {0}', 'Answer ready — {0}', 'Răspuns gata — {0}',
   'Antwort bereit — {0}', 'Svar klart — {0}'),
 'inc_sol_refresh': ('🔄 Aggiorna', '🔄 Refresh', '🔄 Actualizează', '🔄 Aktualisieren', '🔄 Uppdatera'),
 'inc_sol_select': ('Seleziona una richiesta.', 'Select a request.', 'Selectați o cerere.',
   'Anfrage auswählen.', 'Välj en begäran.'),
 'inc_sol_send': ('✉ Invia risposta', '✉ Send answer', '✉ Trimite răspuns', '✉ Antwort senden', '✉ Skicka svar'),
 'inc_sol_text_required': ('Inserire una descrizione della soluzione.', 'Enter a description of the solution.',
   'Introduceți o descriere a soluției.', 'Beschreibung der Lösung eingeben.', 'Ange en beskrivning av lösningen.'),
 'inc_sol_title': ('Soluzioni — Ricezione', 'Solutions — Receiving', 'Soluții — Recepție',
   'Lösungen — Wareneingang', 'Lösningar — Inleverans'),
 # setup operatori
 'incoming_setup_col_emails': ('Email destinatari (separate da ; o ,)', 'Recipient emails (separated by ; or ,)',
   'Email destinatari (separate prin ; sau ,)', 'Empfänger-E-Mails (getrennt durch ; oder ,)',
   'Mottagarens e-post (separerade med ; eller ,)'),
 'incoming_setup_col_reminders': ('Reminder/giorno', 'Reminders/day', 'Reminder/zi',
   'Erinnerungen/Tag', 'Påminnelser/dag'),
 'incoming_setup_col_type': ('Tipo richiesta', 'Request type', 'Tip cerere', 'Anfrageart', 'Förfrågningstyp'),
 'incoming_setup_engineering_frame': ('Indirizzi email Ingegneria (destinatari in TO della email soluzione)',
   'Engineering email addresses (TO recipients of the solution email)',
   'Adrese email Inginerie (destinatari în TO al emailului de soluție)',
   'Engineering-E-Mail-Adressen (TO-Empfänger der Lösungs-E-Mail)',
   'Engineering e-postadresser (TO-mottagare av lösningsmailet)'),
 'incoming_setup_engineering_hint': ('Indirizzi Ingegneria inseriti come destinatari principali (A) '
   "dell'email preconfezionata di richiesta soluzione.",
   'Engineering addresses inserted as main recipients (To) of the pre-composed solution request email.',
   'Adresele de Inginerie introduse ca destinatari principali (Către) ai emailului predefinit de solicitare soluție.',
   'Engineering-Adressen als Hauptempfänger (An) der vorgefertigten Lösungsanfrage-E-Mail.',
   'Engineering-adresser som huvudmottagare (Till) av det förberedda lösningsförfrågan-mailet.'),
 'incoming_setup_email_frame': ('Destinatari email e reminder per tipo di richiesta',
   'Email recipients and reminders per request type', 'Destinatari email și reminder pe tip cerere',
   'E-Mail-Empfänger und Erinnerungen pro Anfrageart', 'E-postmottagare och påminnelser per förfrågningstyp'),
 'incoming_setup_header': ('Configurazione modulo Ricezione (Incoming)', 'Receiving module configuration',
   'Configurare modul Recepție (Incoming)', 'Konfiguration Wareneingang-Modul', 'Konfiguration inleveransmodul'),
 'incoming_setup_invalid_emails': ('I seguenti indirizzi non sono validi e non verranno salvati:\n{0}',
   'The following addresses are invalid and will not be saved:\n{0}',
   'Următoarele adrese nu sunt valide și nu vor fi salvate:\n{0}',
   'Die folgenden Adressen sind ungültig und werden nicht gespeichert:\n{0}',
   'Följande adresser är ogiltiga och sparas inte:\n{0}'),
 'incoming_setup_monthly_frame': ('Destinatari report mensile (soluzione problemi)',
   'Monthly report recipients (problem solving)', 'Destinatari raport lunar (soluționare probleme)',
   'Empfänger des Monatsberichts (Problemlösung)', 'Mottagare av månadsrapport (problemlösning)'),
 'incoming_setup_reminders_hint': ('I reminder sono popup/email ripetuti giornalmente per ogni richiesta ancora in sospeso.',
   'Reminders are popup/emails repeated daily for each request still pending.',
   'Reminder-ele sunt popup/email repetate zilnic pentru fiecare cerere încă în suspensie.',
   'Erinnerungen sind Popup/E-Mails, die täglich für jede ausstehende Anfrage wiederholt werden.',
   'Påminnelser är popup/e-post som upprepas dagligen för varje väntande begäran.'),
 'incoming_setup_save_error': ('Errore durante il salvataggio', 'Error while saving', 'Eroare la salvare',
   'Fehler beim Speichern', 'Fel vid sparande'),
 'incoming_setup_saved': ('Configurazione salvata con successo.', 'Configuration saved successfully.',
   'Configurare salvată cu succes.', 'Konfiguration erfolgreich gespeichert.', 'Konfigurationen sparades.'),
 'incoming_setup_title': ('Setup — Ricezione (Incoming)', 'Setup — Receiving', 'Configurare — Recepție',
   'Einrichtung — Wareneingang', 'Inställningar — Inleverans'),
 'incoming_setup_workstation_frame': ('Postazione (questo PC)', 'Workstation (this PC)', 'Stație (acest PC)',
   'Workstation (dieser PC)', 'Workstation (den här datorn)'),
 'incoming_setup_ws_none': ('nessuno', 'none', 'niciunul', 'keiner', 'ingen'),
 'incoming_setup_ws_open': ('Configura postazione…', 'Configure workstation…', 'Configurează stația…',
   'Workstation konfigurieren…', 'Konfigurera workstation…'),
 'incoming_setup_ws_roles': ('Ruoli attivi: {0}', 'Active roles: {0}', 'Roluri active: {0}',
   'Aktive Rollen: {0}', 'Aktiva roller: {0}'),
 # workstation config
 'incoming_ws_activate': ('✅ Attiva', '✅ Activate', '✅ Activează', '✅ Aktivieren', '✅ Aktivera'),
 'incoming_ws_activated': ('Ruolo attivato con successo.', 'Role activated successfully.',
   'Rol activat cu succes.', 'Rolle erfolgreich aktiviert.', 'Roll aktiverad.'),
 'incoming_ws_confirm_deactivate': ('Sei sicuro di voler disattivare questo ruolo?',
   'Are you sure you want to deactivate this role?', 'Sigur doriți să dezactivați acest rol?',
   'Diese Rolle wirklich deaktivieren?', 'Vill du verkligen inaktivera den här rollen?'),
 'incoming_ws_confirm_deactivate_all': ('Disattivare TUTTI i ruoli Incoming su questo PC?',
   'Deactivate ALL Incoming roles on this PC?', 'Dezactivați TOATE rolurile Incoming pe acest PC?',
   'ALLE Incoming-Rollen auf diesem PC deaktivieren?', 'Inaktivera ALLA Incoming-roller på den här datorn?'),
 'incoming_ws_deactivate': ('❌ Disattiva', '❌ Deactivate', '❌ Dezactivează', '❌ Deaktivieren', '❌ Inaktivera'),
 'incoming_ws_deactivate_all': ('Disattiva tutto', 'Deactivate all', 'Dezactivează tot', 'Alle deaktivieren',
   'Inaktivera alla'),
 'incoming_ws_deactivated': ('Ruolo disattivato con successo.', 'Role deactivated successfully.',
   'Rol dezactivat cu succes.', 'Rolle erfolgreich deaktiviert.', 'Roll inaktiverad.'),
 'incoming_ws_desc': ('Identifica questo computer come postazione del modulo Ricezione.\n'
   '"Ricevitore" mostra i popup delle nuove richieste ed escalation;\n'
   '"Mittente" invia le richieste dal magazzino incoming.',
   'Identify this computer as a Receiving module workstation.\n'
   '"Receiver" shows popups for new requests and escalations;\n'
   '"Sender" sends requests from the incoming warehouse.',
   'Identifică acest computer ca stație a modulului Recepție.\n'
   '"Receptor" afișează popup-uri pentru cereri noi și escaladări;\n'
   '"Expeditor" trimite cererile de la depozitul incoming.',
   'Diesen Computer als Workstation des Wareneingang-Moduls festlegen.\n'
   '"Empfänger" zeigt Popups für neue Anfragen und Eskalationen;\n'
   '"Absender" sendet Anfragen aus dem Wareneingang-Lager.',
   'Identifiera den här datorn som en workstation för inleveransmodulen.\n'
   '"Mottagare" visar popup för nya förfrågningar och eskaleringar;\n'
   '"Avsändare" skickar förfrågningar från incoming-lagret.'),
 'incoming_ws_header': ('Configurazione Postazione Ricezione', 'Receiving workstation configuration',
   'Configurare stație Recepție', 'Konfiguration Wareneingang-Workstation', 'Konfiguration inleveransworkstation'),
 'incoming_ws_inactive': ('❌ Ruolo NON attivo', '❌ Role NOT active', '❌ Rol NU este activ',
   '❌ Rolle NICHT aktiv', '❌ Roll EJ aktiv'),
 'incoming_ws_receiver_label': ('Ricevitore richieste (popup nuove richieste + escalation)',
   'Request receiver (new request + escalation popups)', 'Receptor cereri (popup cereri noi + escaladare)',
   'Anfragen-Empfänger (Popups neue Anfragen + Eskalation)', 'Förfrågningsmottagare (popup nya förfrågningar + eskalering)'),
 'incoming_ws_sender_label': ('Mittente richieste (WH incoming; popup di risposta)',
   'Request sender (WH incoming; answer popup)', 'Expeditor cereri (WH incoming; popup răspuns)',
   'Anfragen-Absender (WH incoming; Antwort-Popup)', 'Förfrågningsavsändare (WH incoming; svarspopup)'),
 'incoming_ws_title': ('Configurazione Postazione — Ricezione (Incoming)',
   'Workstation configuration — Receiving', 'Configurare stație — Recepție',
   'Workstation-Konfiguration — Wareneingang', 'Workstation-konfiguration — Inleverans'),
}

LANGS = ('it', 'en', 'ro', 'de', 'sv')

HEADER = ("-- ============================================================\n"
          "-- Traduzioni GUI del modulo Ricezione (incoming)\n"
          "-- Chiavi inc_* / incoming_setup_* / incoming_ws_*\n"
          "-- Lingue: it, en, ro, de, sv — idempotente (IF NOT EXISTS)\n"
          "-- Generato da script; pattern identico agli altri script del modulo.\n"
          "-- ============================================================\n\n"
          "USE [Traceability_RS];\nGO\n\n")


def esc(v: str) -> str:
    return v.replace("'", "''")


def main():
    out = [HEADER]
    for key in sorted(T):
        it, en, ro, de, sv = T[key]
        vals = dict(zip(LANGS, (it, en, ro, de, sv)))
        out.append(f"-- {key}\n")
        for lang in LANGS:
            out.append(
                f"IF NOT EXISTS (SELECT 1 FROM [dbo].[AppTranslations] "
                f"WHERE [LanguageCode]='{lang}' AND [TranslationKey]='{key}')\n"
                f"    INSERT INTO [dbo].[AppTranslations] "
                f"([LanguageCode],[TranslationKey],[TranslationValue]) "
                f"VALUES (N'{lang}',N'{key}',N'{esc(vals[lang])}');\nGO\n")
        out.append("\n")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'add_incoming_translations_gui.sql')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(''.join(out))
    print(f"Scritto {path}: {len(T)} chiavi x {len(LANGS)} lingue")


if __name__ == '__main__':
    main()
