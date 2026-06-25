# -*- coding: utf-8 -*-
"""
Genera il manuale PDF della sezione 'Touch-up' (sotto Operazioni > Produzione >
Dichiarazioni) in 5 lingue. Riusa lo stile/impaginazione di generate_decl_manuals.

Produce per ogni lingua un PDF completo `operazioni_touchup.pdf` e ne copia gli
alias per ciascuna voce di sottomenu (problemi, soluzioni, rapporti, workstation,
gestione), così ogni voce del menu Aiuto > Manuali apre la guida Touch-up.
"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_decl_manuals import (
    cover, build_pdf, sp, hrl, bul, tbl, H1, H2, B, N, W, BASE,
)

ALIASES = [
    "operazioni_touchup_problemi",
    "operazioni_touchup_soluzioni",
    "operazioni_touchup_rapporti",
    "operazioni_touchup_workstation",
    "operazioni_touchup_gestione",
]

T = {
 "it": {
   "a": "TraceabilityRS", "v": "Versione 2.4.2", "ft": "TraceabilityRS - Touch-up",
   "login": "Necessita autenticazione (login) con chiavi dedicate",
   "title": "Touch-up", "subtitle": "Segnalazione problemi schede e instradamento ai tecnici",
   "intro": "Il modulo Touch-up consente agli operatori dell'area touch-up di segnalare i problemi "
            "riscontrati sulle schede elettroniche. Il sistema instrada automaticamente la segnalazione "
            "ai tecnici del reparto competente (in base al tipo di problema), attiva i popup sulle "
            "postazioni configurate e gestisce ricorrenze, riaperture ed escalation al responsabile.",
   "m1_t": "1. Problemi rivelati (operatore)",
   "m1": "Inserire una o più schede tramite il loro <b>LabelCode</b> (verificato dal sistema come nei FAI) "
         "e selezionare uno o più problemi dall'elenco. Al salvataggio la segnalazione viene creata e, se "
         "necessario, attiva i popup e invia le email.",
   "m1_steps": [
       "Digitare il <b>LabelCode</b> e premere 'Verifica e aggiungi' (mostra ordine e prodotto)",
       "Aggiungere altre schede se la stessa problematica riguarda più schede",
       "Selezionare uno o più <b>problemi</b> dall'elenco (selezione multipla)",
       "Premere <b>Salva segnalazione</b>",
   ],
   "m1_note": "NOTA: il LabelCode deve esistere nel sistema. Le schede dello stesso ordine con lo stesso "
              "problema vengono riconosciute come RICORRENTI.",
   "m2_t": "2. Soluzioni adottate (tecnico)",
   "m2": "Il tecnico vede le segnalazioni aperte (NEW/REOPENED), apre il dettaglio (schede, ordine, prodotto, "
         "problemi), scrive le azioni intraprese e conferma. Alla conferma la segnalazione viene CHIUSA e "
         "viene registrato il tempo di reazione.",
   "m3_t": "3. Rapporti",
   "m3": "Sezione di reportistica Touch-up (tempi di reazione, ricorrenze, riaperture). In arrivo.",
   "m4_t": "4. Setup workstation",
   "m4": "Attiva o disattiva su QUESTO PC la ricezione dei popup Touch-up. Stessa logica della postazione "
         "Materiali Indiretti / Cambio Turno: un semplice Attiva/Disattiva (marker locale touchup_host.json).",
   "m5_t": "5. Gestione",
   "m5": "Configurazione del modulo, riservata ai responsabili:",
   "m5_items": [
       ("Problemi", "Anagrafica dei problemi mostrati nel combo (nuovo / modifica / disattiva)"),
       ("Instradamento", "Per ogni problema, i reparti destinatari (CdC / SubCdC) a cui inviare popup ed email"),
       ("Parametri escalation", "Minuti senza risposta prima dell'escalation al responsabile e soglia ricorrenze/giorno"),
   ],
   "esc_t": "Ricorrenze, riaperture ed escalation",
   "esc_items": [
       "RICORRENZA: stessa coppia ordine+problema già segnalata → priorità alta + email di avviso",
       "RIAPERTURA: stesso prodotto+problema su una segnalazione già chiusa → stato REOPENED e conteggio riaperture",
       "SOGLIA GIORNALIERA: stesso problema oltre N volte nel giorno di produzione (07:30→07:30) → escalation al responsabile",
       "NESSUNA RISPOSTA: segnalazione aperta oltre i minuti configurati → email automatica al responsabile",
   ],
   "esc_note": "Le email di avviso vengono inviate ai destinatari del reparto instradato (tecnici) con il "
               "responsabile in copia; l'indirizzo di servizio è la chiave 'Sys_email_TouchUp_warning'.",
   "auth_note": "ACCESSO: voce 1 chiave 'operatore_touchup'; voce 2 'tecnico_risponde_touchup'; "
                "voce 4 'attiva_workstation_tecnici'; voce 5 'set_up_touchup'. La voce 3 (Rapporti) è senza login.",
   "step": "Passo", "desc": "Descrizione", "item": "Voce",
 },
 "en": {
   "a": "TraceabilityRS", "v": "Version 2.4.2", "ft": "TraceabilityRS - Touch-up",
   "login": "Requires authentication (login) with dedicated keys",
   "title": "Touch-up", "subtitle": "Board problem reporting and routing to technicians",
   "intro": "The Touch-up module lets touch-up operators report problems found on electronic boards. "
            "The system automatically routes the report to the technicians of the competent department "
            "(by problem type), triggers popups on the configured workstations and handles recurrences, "
            "reopenings and escalation to the supervisor.",
   "m1_t": "1. Detected problems (operator)",
   "m1": "Enter one or more boards by their <b>LabelCode</b> (verified by the system as in FAI) and select "
         "one or more problems from the list. On save the report is created and, if needed, triggers popups "
         "and sends emails.",
   "m1_steps": [
       "Type the <b>LabelCode</b> and press 'Verify and add' (shows order and product)",
       "Add more boards if the same problem affects several boards",
       "Select one or more <b>problems</b> from the list (multi-select)",
       "Press <b>Save report</b>",
   ],
   "m1_note": "NOTE: the LabelCode must exist in the system. Boards of the same order with the same problem "
              "are recognized as RECURRENT.",
   "m2_t": "2. Solutions taken (technician)",
   "m2": "The technician sees the open reports (NEW/REOPENED), opens the detail (boards, order, product, "
         "problems), writes the actions taken and confirms. On confirmation the report is CLOSED and the "
         "reaction time is recorded.",
   "m3_t": "3. Reports",
   "m3": "Touch-up reporting section (reaction times, recurrences, reopenings). Coming soon.",
   "m4_t": "4. Workstation setup",
   "m4": "Enable or disable Touch-up popups on THIS PC. Same logic as the Indirect Materials / Shift Handover "
         "workstation: a simple Enable/Disable (local marker touchup_host.json).",
   "m5_t": "5. Management",
   "m5": "Module configuration, restricted to supervisors:",
   "m5_items": [
       ("Problems", "Catalog of problems shown in the combo (new / edit / deactivate)"),
       ("Routing", "For each problem, the destination departments (CdC / SubCdC) to receive popups and emails"),
       ("Escalation params", "Minutes without response before escalation to supervisor and recurrence/day threshold"),
   ],
   "esc_t": "Recurrences, reopenings and escalation",
   "esc_items": [
       "RECURRENCE: same order+problem pair already reported → high priority + warning email",
       "REOPENING: same product+problem on an already closed report → REOPENED status and reopen count",
       "DAILY THRESHOLD: same problem more than N times in the production day (07:30→07:30) → escalation to supervisor",
       "NO RESPONSE: report open beyond the configured minutes → automatic email to the supervisor",
   ],
   "esc_note": "Warning emails are sent to the routed department recipients (technicians) with the supervisor "
               "in copy; the service address is the 'Sys_email_TouchUp_warning' key.",
   "auth_note": "ACCESS: item 1 key 'operatore_touchup'; item 2 'tecnico_risponde_touchup'; "
                "item 4 'attiva_workstation_tecnici'; item 5 'set_up_touchup'. Item 3 (Reports) has no login.",
   "step": "Step", "desc": "Description", "item": "Item",
 },
 "ro": {
   "a": "TraceabilityRS", "v": "Versiunea 2.4.2", "ft": "TraceabilityRS - Touch-up",
   "login": "Necesita autentificare (login) cu chei dedicate",
   "title": "Touch-up", "subtitle": "Raportarea problemelor placilor si directionarea catre tehnicieni",
   "intro": "Modulul Touch-up permite operatorilor din zona touch-up sa raporteze problemele gasite pe placile "
            "electronice. Sistemul directioneaza automat raportul catre tehnicienii departamentului competent "
            "(dupa tipul problemei), activeaza popup-uri pe statiile configurate si gestioneaza recurentele, "
            "redeschiderile si escaladarea catre responsabil.",
   "m1_t": "1. Probleme detectate (operator)",
   "m1": "Introduceti una sau mai multe placi prin <b>LabelCode</b> (verificat de sistem ca la FAI) si "
         "selectati una sau mai multe probleme din lista. La salvare raportul este creat si, daca este nevoie, "
         "activeaza popup-uri si trimite email-uri.",
   "m1_steps": [
       "Tastati <b>LabelCode</b> si apasati 'Verifica si adauga' (afiseaza comanda si produsul)",
       "Adaugati alte placi daca aceeasi problema priveste mai multe placi",
       "Selectati una sau mai multe <b>probleme</b> din lista (selectie multipla)",
       "Apasati <b>Salveaza raportul</b>",
   ],
   "m1_note": "NOTA: LabelCode trebuie sa existe in sistem. Placile aceleiasi comenzi cu aceeasi problema "
              "sunt recunoscute ca RECURENTE.",
   "m2_t": "2. Solutii adoptate (tehnician)",
   "m2": "Tehnicianul vede rapoartele deschise (NEW/REOPENED), deschide detaliul (placi, comanda, produs, "
         "probleme), scrie actiunile intreprinse si confirma. La confirmare raportul este INCHIS si se "
         "inregistreaza timpul de reactie.",
   "m3_t": "3. Rapoarte",
   "m3": "Sectiunea de raportare Touch-up (timpi de reactie, recurente, redeschideri). In curand.",
   "m4_t": "4. Setare statie",
   "m4": "Activeaza sau dezactiveaza pe ACEST PC primirea popup-urilor Touch-up. Aceeasi logica precum statia "
         "Materiale Indirecte / Schimb Tura: un simplu Activare/Dezactivare (marker local touchup_host.json).",
   "m5_t": "5. Gestionare",
   "m5": "Configurarea modulului, rezervata responsabililor:",
   "m5_items": [
       ("Probleme", "Catalogul problemelor afisate in combo (nou / modificare / dezactivare)"),
       ("Directionare", "Pentru fiecare problema, departamentele destinatare (CdC / SubCdC) pentru popup si email"),
       ("Parametri escaladare", "Minute fara raspuns inainte de escaladare si pragul recurente/zi"),
   ],
   "esc_t": "Recurente, redeschideri si escaladare",
   "esc_items": [
       "RECURENTA: aceeasi pereche comanda+problema deja raportata -> prioritate mare + email de avertizare",
       "REDESCHIDERE: acelasi produs+problema pe un raport deja inchis -> stare REOPENED si numar redeschideri",
       "PRAG ZILNIC: aceeasi problema de peste N ori in ziua de productie (07:30->07:30) -> escaladare la responsabil",
       "FARA RASPUNS: raport deschis peste minutele configurate -> email automat catre responsabil",
   ],
   "esc_note": "Email-urile de avertizare se trimit catre destinatarii departamentului directionat (tehnicieni) "
               "cu responsabilul in copie; adresa de serviciu este cheia 'Sys_email_TouchUp_warning'.",
   "auth_note": "ACCES: punctul 1 cheia 'operatore_touchup'; punctul 2 'tecnico_risponde_touchup'; "
                "punctul 4 'attiva_workstation_tecnici'; punctul 5 'set_up_touchup'. Punctul 3 (Rapoarte) fara login.",
   "step": "Pas", "desc": "Descriere", "item": "Element",
 },
 "de": {
   "a": "TraceabilityRS", "v": "Version 2.4.2", "ft": "TraceabilityRS - Touch-up",
   "login": "Erfordert Authentifizierung (Login) mit dedizierten Schluesseln",
   "title": "Touch-up", "subtitle": "Meldung von Platinenproblemen und Weiterleitung an Techniker",
   "intro": "Das Touch-up-Modul ermoeglicht den Bedienern im Touch-up-Bereich, an Platinen festgestellte "
            "Probleme zu melden. Das System leitet die Meldung automatisch an die Techniker der zustaendigen "
            "Abteilung weiter (nach Problemtyp), loest Popups an den konfigurierten Arbeitsplaetzen aus und "
            "verwaltet Wiederholungen, Wiedereroeffnungen und Eskalation an den Vorgesetzten.",
   "m1_t": "1. Erkannte Probleme (Bediener)",
   "m1": "Eine oder mehrere Platinen ueber ihren <b>LabelCode</b> eingeben (vom System wie bei FAI geprueft) "
         "und ein oder mehrere Probleme aus der Liste waehlen. Beim Speichern wird die Meldung erstellt und "
         "loest bei Bedarf Popups aus und versendet E-Mails.",
   "m1_steps": [
       "<b>LabelCode</b> eingeben und 'Pruefen und hinzufuegen' druecken (zeigt Auftrag und Produkt)",
       "Weitere Platinen hinzufuegen, wenn dasselbe Problem mehrere Platinen betrifft",
       "Ein oder mehrere <b>Probleme</b> aus der Liste waehlen (Mehrfachauswahl)",
       "<b>Meldung speichern</b> druecken",
   ],
   "m1_note": "HINWEIS: Der LabelCode muss im System existieren. Platinen desselben Auftrags mit demselben "
              "Problem werden als WIEDERHOLT erkannt.",
   "m2_t": "2. Ergriffene Loesungen (Techniker)",
   "m2": "Der Techniker sieht die offenen Meldungen (NEW/REOPENED), oeffnet das Detail (Platinen, Auftrag, "
         "Produkt, Probleme), traegt die ergriffenen Massnahmen ein und bestaetigt. Bei Bestaetigung wird die "
         "Meldung GESCHLOSSEN und die Reaktionszeit erfasst.",
   "m3_t": "3. Berichte",
   "m3": "Touch-up-Berichtsbereich (Reaktionszeiten, Wiederholungen, Wiedereroeffnungen). Demnaechst.",
   "m4_t": "4. Arbeitsplatz-Einrichtung",
   "m4": "Touch-up-Popups an DIESEM PC aktivieren oder deaktivieren. Gleiche Logik wie der Arbeitsplatz "
         "Indirekte Materialien / Schichtuebergabe: ein einfaches Aktivieren/Deaktivieren (lokaler Marker touchup_host.json).",
   "m5_t": "5. Verwaltung",
   "m5": "Modulkonfiguration, den Vorgesetzten vorbehalten:",
   "m5_items": [
       ("Probleme", "Katalog der im Kombinationsfeld angezeigten Probleme (neu / bearbeiten / deaktivieren)"),
       ("Weiterleitung", "Pro Problem die Zielabteilungen (CdC / SubCdC) fuer Popups und E-Mails"),
       ("Eskalationsparameter", "Minuten ohne Antwort vor Eskalation und Schwelle Wiederholungen/Tag"),
   ],
   "esc_t": "Wiederholungen, Wiedereroeffnungen und Eskalation",
   "esc_items": [
       "WIEDERHOLUNG: gleiches Paar Auftrag+Problem bereits gemeldet -> hohe Prioritaet + Warn-E-Mail",
       "WIEDEREROEFFNUNG: gleiches Produkt+Problem bei einer bereits geschlossenen Meldung -> Status REOPENED und Zaehler",
       "TAGESSCHWELLE: gleiches Problem mehr als N-mal am Produktionstag (07:30->07:30) -> Eskalation an Vorgesetzten",
       "KEINE ANTWORT: Meldung laenger als die konfigurierten Minuten offen -> automatische E-Mail an den Vorgesetzten",
   ],
   "esc_note": "Warn-E-Mails gehen an die Empfaenger der weitergeleiteten Abteilung (Techniker) mit dem "
               "Vorgesetzten in Kopie; die Dienstadresse ist der Schluessel 'Sys_email_TouchUp_warning'.",
   "auth_note": "ZUGRIFF: Punkt 1 Schluessel 'operatore_touchup'; Punkt 2 'tecnico_risponde_touchup'; "
                "Punkt 4 'attiva_workstation_tecnici'; Punkt 5 'set_up_touchup'. Punkt 3 (Berichte) ohne Login.",
   "step": "Schritt", "desc": "Beschreibung", "item": "Punkt",
 },
 "sv": {
   "a": "TraceabilityRS", "v": "Version 2.4.2", "ft": "TraceabilityRS - Touch-up",
   "login": "Kraever autentisering (inloggning) med dedikerade nycklar",
   "title": "Touch-up", "subtitle": "Rapportering av kortproblem och dirigering till tekniker",
   "intro": "Touch-up-modulen laater touch-up-operatoerer rapportera problem som hittats paa elektronikkort. "
            "Systemet dirigerar automatiskt rapporten till teknikerna paa raett avdelning (efter problemtyp), "
            "utloeser popup-fönster paa konfigurerade arbetsstationer och hanterar aaterkommande fall, "
            "aateroeppningar och eskalering till ansvarig.",
   "m1_t": "1. Upptaeckta problem (operatoer)",
   "m1": "Ange ett eller flera kort via deras <b>LabelCode</b> (verifierad av systemet som i FAI) och vaelj "
         "ett eller flera problem fraan listan. Vid sparande skapas rapporten och utloeser vid behov popup "
         "och skickar e-post.",
   "m1_steps": [
       "Skriv <b>LabelCode</b> och tryck 'Verifiera och laegg till' (visar order och produkt)",
       "Laegg till fler kort om samma problem gaeller flera kort",
       "Vaelj ett eller flera <b>problem</b> fraan listan (flerval)",
       "Tryck <b>Spara rapport</b>",
   ],
   "m1_note": "OBS: LabelCode maaste finnas i systemet. Kort fraan samma order med samma problem identifieras "
              "som AATERKOMMANDE.",
   "m2_t": "2. Vidtagna loesningar (tekniker)",
   "m2": "Teknikern ser de oeppna rapporterna (NEW/REOPENED), oeppnar detaljen (kort, order, produkt, problem), "
         "skriver de vidtagna aatgaerderna och bekraeftar. Vid bekraeftelse STAENGS rapporten och reaktionstiden "
         "registreras.",
   "m3_t": "3. Rapporter",
   "m3": "Touch-up-rapportsektion (reaktionstider, aaterkommande fall, aateroeppningar). Kommer snart.",
   "m4_t": "4. Arbetsstationsinstaellning",
   "m4": "Aktivera eller inaktivera Touch-up-popup paa DENNA PC. Samma logik som arbetsstationen Indirekta "
         "Material / Skiftoeverlaemning: en enkel Aktivera/Inaktivera (lokal markoer touchup_host.json).",
   "m5_t": "5. Hantering",
   "m5": "Modulkonfiguration, foerbehaallen ansvariga:",
   "m5_items": [
       ("Problem", "Katalog oever problem som visas i komboboxen (ny / aendra / inaktivera)"),
       ("Dirigering", "Foer varje problem, mottagaravdelningar (CdC / SubCdC) foer popup och e-post"),
       ("Eskaleringsparametrar", "Minuter utan svar foere eskalering och troeskel aaterkommande/dag"),
   ],
   "esc_t": "Aaterkommande fall, aateroeppningar och eskalering",
   "esc_items": [
       "AATERKOMMANDE: samma par order+problem redan rapporterat -> hoeg prioritet + varningsmail",
       "AATEROEPPNING: samma produkt+problem paa en redan staengd rapport -> status REOPENED och raeknare",
       "DAGSTROESKEL: samma problem mer aen N gaanger paa produktionsdagen (07:30->07:30) -> eskalering till ansvarig",
       "INGET SVAR: rapport oeppen oever de konfigurerade minuterna -> automatiskt mail till ansvarig",
   ],
   "esc_note": "Varningsmail skickas till den dirigerade avdelningens mottagare (tekniker) med ansvarig i kopia; "
               "serviceadressen aer nyckeln 'Sys_email_TouchUp_warning'.",
   "auth_note": "AATKOMST: punkt 1 nyckel 'operatore_touchup'; punkt 2 'tecnico_risponde_touchup'; "
                "punkt 4 'attiva_workstation_tecnici'; punkt 5 'set_up_touchup'. Punkt 3 (Rapporter) utan inloggning.",
   "step": "Steg", "desc": "Beskrivning", "item": "Element",
 },
}


def gen_touchup(lang, t):
    out = os.path.join(BASE, lang, "operazioni_touchup.pdf")

    def story(s, wid):
        cover(s, t["title"], t["subtitle"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Acces: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["intro"], B))

        s.append(Paragraph(t["m1_t"], H1))
        s.append(Paragraph(t["m1"], B))
        for st in t["m1_steps"]:
            s.append(bul(st))
        s.append(Paragraph(t["m1_note"], N))

        s.append(Paragraph(t["m2_t"], H1))
        s.append(Paragraph(t["m2"], B))

        s.append(Paragraph(t["m3_t"], H1))
        s.append(Paragraph(t["m3"], B))

        s.append(Paragraph(t["m4_t"], H1))
        s.append(Paragraph(t["m4"], B))

        s.append(Paragraph(t["m5_t"], H1))
        s.append(Paragraph(t["m5"], B))
        s.append(tbl([t["item"], t["desc"]], [list(i) for i in t["m5_items"]], wid))

        s.append(Paragraph(t["esc_t"], H1))
        for it in t["esc_items"]:
            s.append(bul(it))
        s.append(Paragraph(t["esc_note"], N))
        s.append(sp(2)); s.append(Paragraph(t["auth_note"], W))

    build_pdf(out, story, t["ft"])
    d = os.path.dirname(out)
    for alias in ALIASES:
        shutil.copy2(out, os.path.join(d, alias + ".pdf"))
    print("  [%s] Touch-up (1 + %d alias)" % (lang.upper(), len(ALIASES)))


# build_pdf/story usano Paragraph importato qui sotto
from reportlab.platypus import Paragraph  # noqa: E402

if __name__ == "__main__":
    print("Generazione manuale 'Touch-up' in 5 lingue...")
    for lc, tx in T.items():
        os.makedirs(os.path.join(BASE, lc), exist_ok=True)
        gen_touchup(lc, tx)
    print("\nCompletato! %d PDF generati (%d per lingua x 5 lingue)" % (6 * 5, 6))
