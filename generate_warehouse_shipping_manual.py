# -*- coding: utf-8 -*-
"""
Genera il manuale PDF 'Spedizioni da magazzino' (Operazioni > Ordini > Urgenze /
Spedizioni) in 5 lingue, riusando stile/impaginazione di generate_decl_manuals.

Descrive la funzionalità che aggiunge alla lista spedizioni gli ordini finiti e
versati a magazzino non ancora spediti (righe gialle "da abbinare"), la
segnalazione rossa degli urgenti già a magazzino, l'abbinamento manuale a un
ordine di vendita, la destinazione direct/normal e la correzione "già spedito".

Output: manuals/{lang}/operazioni_spedizioni_magazzino.pdf
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_decl_manuals import (
    cover, build_pdf, sp, bul, tbl, H1, B, N, W, BASE,
)
from reportlab.platypus import Paragraph

T = {
 "it": {
   "a": "TraceabilityRS", "v": "Versione 2.4.2", "ft": "TraceabilityRS - Spedizioni da magazzino",
   "login": "Necessita autenticazione (chiave menu Urgenze/Ordini)",
   "title": "Spedizioni da magazzino",
   "subtitle": "Ordini finiti e versati a magazzino nella lista spedizioni",
   "intro": "La lista spedizioni (Ordini > Urgenze) mostrava solo gli ordini già abbinati dai planner "
            "(ordine di vendita ↔ ordine di produzione). Ora include anche, senza duplicare, gli ordini "
            "che hanno terminato la produzione e sono stati versati a magazzino ma non ancora spediti. "
            "L'addetto alla spedizione li abbina a un ordine di vendita, imposta la destinazione e procede "
            "come con gli ordini dei planner.",
   "leg_t": "Colori delle righe",
   "leg_items": [
       "GIALLO = riga 'da abbinare': ordine a magazzino senza ordine di vendita. La quantità mostrata è "
       "quella disponibile (versato a magazzino meno già abbinato e già spedito).",
       "ROSSO = ordine urgente (già a piano) la cui merce risulta già a magazzino: pronto da spedire "
       "(il confronto è per ordine, anche se la quantità a magazzino è diversa da quella richiesta).",
   ],
   "m1_t": "1. Abbinare un ordine a magazzino",
   "m1": "Selezionare una riga gialla e fare doppio click (oppure usare il bottone 'Abbina / Correggi'). "
         "Si sceglie l'ordine di vendita con lo stesso prodotto e la quantità.",
   "m1_steps": [
       "Doppio click sulla riga gialla (o bottone <b>Abbina / Correggi</b>)",
       "Scegliere l'<b>ordine di vendita</b> dall'elenco (stesso prodotto, con residuo disponibile)",
       "Indicare la <b>quantità</b> (non superiore al minimo tra disponibile a magazzino e residuo dell'ordine)",
       "Impostare <b>data/ora</b> e <b>destinazione</b> (Normal Shipment / Direct to final Customer)",
       "Premere <b>Abbina e crea regola</b>",
   ],
   "m1_note": "NOTA: l'ordine di vendita deve avere lo STESSO prodotto (stesso codice, senza il suffisso di "
              "versione). Se non esiste ancora un ordine di vendita per quel prodotto, la riga resta da "
              "abbinare finché il relativo ordine non viene importato.",
   "m2_t": "2. Correzione 'già spedito' (allineamento)",
   "m2": "Finché non tutte le spedizioni passano dal sistema, la merce già spedita fuori dal sistema "
         "resterebbe erroneamente disponibile. Dalla stessa finestra, il pulsante 'Già spedito' permette di "
         "dichiarare quanta parte dell'ordine è già stata spedita: quella quantità esce dalla disponibilità. "
         "La correzione è registrata con utente, data e nota.",
   "date_t": "Data di partenza",
   "date": "La disponibilità considera solo la merce versata a magazzino a partire da una data 'punto zero' "
           "(impostazione 'data_inizio_spedizioni'): prima di quella data si assume tutto già spedito. La "
           "correzione 'già spedito' serve proprio ad allineare i casi versati dopo tale data e già spediti.",
   "email_t": "Destinazione nell'email",
   "email": "Alla conferma della spedizione, l'email riporta per ogni pallet la destinazione (Normal Shipment "
            "o Direct to final Customer); la spedizione diretta al cliente finale è evidenziata.",
   "step": "Passo", "desc": "Descrizione", "item": "Voce",
 },
 "en": {
   "a": "TraceabilityRS", "v": "Version 2.4.2", "ft": "TraceabilityRS - Warehouse shipping",
   "login": "Requires authentication (Urgent/Orders menu key)",
   "title": "Warehouse shipping",
   "subtitle": "Finished, warehoused orders in the shipping list",
   "intro": "The shipping list (Orders > Urgent) used to show only the orders already matched by the planners "
            "(sales order <-> production order). It now also includes, without duplication, the orders that "
            "finished production and were loaded into the warehouse but not yet shipped. The shipping clerk "
            "matches them to a sales order, sets the destination and proceeds as with the planners' orders.",
   "leg_t": "Row colors",
   "leg_items": [
       "YELLOW = 'to match' row: a warehouse order with no sales order. The shown quantity is the available "
       "one (warehoused minus already matched and already shipped).",
       "RED = urgent order (already planned) whose goods are already in the warehouse: ready to ship "
       "(compared by order, even if the warehoused quantity differs from the requested one).",
   ],
   "m1_t": "1. Matching a warehouse order",
   "m1": "Select a yellow row and double-click (or use the 'Match / Correct' button). You pick the sales "
         "order with the same product and the quantity.",
   "m1_steps": [
       "Double-click the yellow row (or the <b>Match / Correct</b> button)",
       "Choose the <b>sales order</b> from the list (same product, with available remainder)",
       "Enter the <b>quantity</b> (not above the minimum of warehouse-available and order remainder)",
       "Set <b>date/time</b> and <b>destination</b> (Normal Shipment / Direct to final Customer)",
       "Press <b>Match and create rule</b>",
   ],
   "m1_note": "NOTE: the sales order must have the SAME product (same code, without the version suffix). If "
              "no sales order exists yet for that product, the row stays to be matched until the related "
              "order is imported.",
   "m2_t": "2. 'Already shipped' correction (alignment)",
   "m2": "Until all shipments go through the system, goods already shipped outside the system would remain "
         "wrongly available. From the same window, the 'Already shipped' button lets you declare how much of "
         "the order has already been shipped: that quantity leaves the availability. The correction is "
         "recorded with user, date and note.",
   "date_t": "Start date",
   "date": "Availability considers only goods warehoused from a 'zero point' date onward "
           "('data_inizio_spedizioni' setting): before that date everything is assumed already shipped. The "
           "'already shipped' correction serves precisely to align cases warehoused after that date and "
           "already shipped.",
   "email_t": "Destination in the email",
   "email": "On shipment confirmation, the email shows for each pallet the destination (Normal Shipment or "
            "Direct to final Customer); direct-to-final-customer shipments are highlighted.",
   "step": "Step", "desc": "Description", "item": "Item",
 },
 "ro": {
   "a": "TraceabilityRS", "v": "Versiunea 2.4.2", "ft": "TraceabilityRS - Expedieri din depozit",
   "login": "Necesita autentificare (cheia meniu Urgente/Comenzi)",
   "title": "Expedieri din depozit",
   "subtitle": "Comenzi finalizate si depozitate in lista de expediere",
   "intro": "Lista de expediere (Comenzi > Urgente) afisa doar comenzile deja asociate de planificatori "
            "(comanda de vanzare <-> comanda de productie). Acum include, fara duplicare, si comenzile care "
            "au terminat productia si au fost depuse in depozit, dar nu au fost inca expediate. Operatorul de "
            "expediere le asociaza unei comenzi de vanzare, seteaza destinatia si continua ca la comenzile "
            "planificatorilor.",
   "leg_t": "Culorile randurilor",
   "leg_items": [
       "GALBEN = rand 'de asociat': comanda din depozit fara comanda de vanzare. Cantitatea afisata este cea "
       "disponibila (depozitat minus deja asociat si deja expediat).",
       "ROSU = comanda urgenta (deja planificata) a carei marfa este deja in depozit: gata de expediere "
       "(comparatie pe comanda, chiar daca cantitatea din depozit difera de cea ceruta).",
   ],
   "m1_t": "1. Asocierea unei comenzi din depozit",
   "m1": "Selectati un rand galben si dublu clic (sau folositi butonul 'Asociaza / Corecteaza'). Se alege "
         "comanda de vanzare cu acelasi produs si cantitatea.",
   "m1_steps": [
       "Dublu clic pe randul galben (sau butonul <b>Asociaza / Corecteaza</b>)",
       "Alegeti <b>comanda de vanzare</b> din lista (acelasi produs, cu rest disponibil)",
       "Introduceti <b>cantitatea</b> (nu mai mare decat minimul dintre disponibilul din depozit si restul comenzii)",
       "Setati <b>data/ora</b> si <b>destinatia</b> (Normal Shipment / Direct to final Customer)",
       "Apasati <b>Asociaza si creeaza regula</b>",
   ],
   "m1_note": "NOTA: comanda de vanzare trebuie sa aiba ACELASI produs (acelasi cod, fara sufixul de versiune). "
              "Daca nu exista inca o comanda de vanzare pentru acel produs, randul ramane de asociat pana la "
              "importul comenzii respective.",
   "m2_t": "2. Corectie 'deja expediat' (aliniere)",
   "m2": "Pana cand toate expedierile trec prin sistem, marfa deja expediata in afara sistemului ar ramane "
         "gresit disponibila. Din aceeasi fereastra, butonul 'Deja expediat' permite declararea cat din "
         "comanda a fost deja expediata: acea cantitate iese din disponibilitate. Corectia este inregistrata "
         "cu utilizator, data si nota.",
   "date_t": "Data de start",
   "date": "Disponibilitatea considera doar marfa depozitata incepand cu o data 'punct zero' (setarea "
           "'data_inizio_spedizioni'): inainte de acea data se presupune totul deja expediat. Corectia 'deja "
           "expediat' serveste tocmai la alinierea cazurilor depozitate dupa acea data si deja expediate.",
   "email_t": "Destinatia in email",
   "email": "La confirmarea expedierii, email-ul arata pentru fiecare palet destinatia (Normal Shipment sau "
            "Direct to final Customer); expedierile directe catre clientul final sunt evidentiate.",
   "step": "Pas", "desc": "Descriere", "item": "Element",
 },
 "de": {
   "a": "TraceabilityRS", "v": "Version 2.4.2", "ft": "TraceabilityRS - Lagerversand",
   "login": "Erfordert Authentifizierung (Menue-Schluessel Dringend/Auftraege)",
   "title": "Lagerversand",
   "subtitle": "Fertige, eingelagerte Auftraege in der Versandliste",
   "intro": "Die Versandliste (Auftraege > Dringend) zeigte nur die von den Planern zugeordneten Auftraege "
            "(Verkaufsauftrag <-> Fertigungsauftrag). Sie enthaelt nun auch, ohne Duplikate, die Auftraege, "
            "die die Produktion abgeschlossen haben und ins Lager eingebucht, aber noch nicht versandt wurden. "
            "Der Versandmitarbeiter ordnet sie einem Verkaufsauftrag zu, legt das Ziel fest und faehrt wie bei "
            "den Auftraegen der Planer fort.",
   "leg_t": "Zeilenfarben",
   "leg_items": [
       "GELB = Zeile 'zuzuordnen': Lagerauftrag ohne Verkaufsauftrag. Die angezeigte Menge ist die verfuegbare "
       "(eingelagert minus bereits zugeordnet und bereits versandt).",
       "ROT = dringender Auftrag (bereits geplant), dessen Ware bereits im Lager ist: versandbereit "
       "(Vergleich pro Auftrag, auch wenn die Lagermenge von der angeforderten abweicht).",
   ],
   "m1_t": "1. Einen Lagerauftrag zuordnen",
   "m1": "Eine gelbe Zeile auswaehlen und doppelklicken (oder die Schaltflaeche 'Zuordnen / Korrigieren' "
         "verwenden). Man waehlt den Verkaufsauftrag mit demselben Produkt und die Menge.",
   "m1_steps": [
       "Doppelklick auf die gelbe Zeile (oder Schaltflaeche <b>Zuordnen / Korrigieren</b>)",
       "Den <b>Verkaufsauftrag</b> aus der Liste waehlen (gleiches Produkt, mit verfuegbarem Rest)",
       "Die <b>Menge</b> eingeben (nicht groesser als das Minimum aus Lagerverfuegbarkeit und Auftragsrest)",
       "<b>Datum/Uhrzeit</b> und <b>Ziel</b> festlegen (Normal Shipment / Direct to final Customer)",
       "<b>Zuordnen und Regel erstellen</b> druecken",
   ],
   "m1_note": "HINWEIS: Der Verkaufsauftrag muss dasselbe Produkt haben (gleicher Code, ohne Versionssuffix). "
              "Existiert noch kein Verkaufsauftrag fuer dieses Produkt, bleibt die Zeile zuzuordnen, bis der "
              "entsprechende Auftrag importiert wird.",
   "m2_t": "2. Korrektur 'bereits versandt' (Abgleich)",
   "m2": "Solange nicht alle Versendungen ueber das System laufen, wuerde bereits ausserhalb des Systems "
         "versandte Ware faelschlich verfuegbar bleiben. Im selben Fenster erlaubt die Schaltflaeche 'Bereits "
         "versandt', anzugeben, wie viel des Auftrags bereits versandt wurde: diese Menge verlaesst die "
         "Verfuegbarkeit. Die Korrektur wird mit Benutzer, Datum und Notiz erfasst.",
   "date_t": "Startdatum",
   "date": "Die Verfuegbarkeit beruecksichtigt nur Ware, die ab einem 'Nullpunkt'-Datum eingelagert wurde "
           "(Einstellung 'data_inizio_spedizioni'): vor diesem Datum wird alles als bereits versandt "
           "angenommen. Die Korrektur 'bereits versandt' dient genau dem Abgleich der nach diesem Datum "
           "eingelagerten und bereits versandten Faelle.",
   "email_t": "Ziel in der E-Mail",
   "email": "Bei der Versandbestaetigung zeigt die E-Mail fuer jede Palette das Ziel (Normal Shipment oder "
            "Direct to final Customer); Direktlieferungen an den Endkunden werden hervorgehoben.",
   "step": "Schritt", "desc": "Beschreibung", "item": "Punkt",
 },
 "sv": {
   "a": "TraceabilityRS", "v": "Version 2.4.2", "ft": "TraceabilityRS - Lagerfrakt",
   "login": "Kraever autentisering (menynyckel Bradskande/Order)",
   "title": "Lagerfrakt",
   "subtitle": "Faerdiga, inlagrade order i fraktlistan",
   "intro": "Fraktlistan (Order > Bradskande) visade endast de order som redan matchats av planerarna "
            "(foersaeljningsorder <-> tillverkningsorder). Den inkluderar nu ocksaa, utan dubbletter, de order "
            "som slutfoert produktionen och lagts in i lagret men aennu inte skickats. Fraktoperatoeren "
            "matchar dem mot en foersaeljningsorder, saetter destinationen och fortsaetter som med planerarnas "
            "order.",
   "leg_t": "Radfaerger",
   "leg_items": [
       "GUL = rad 'att matcha': en lagerorder utan foersaeljningsorder. Den visade kvantiteten aer den "
       "tillgaengliga (inlagrat minus redan matchat och redan skickat).",
       "ROED = bradskande order (redan planerad) vars vara redan finns i lagret: redo att skickas "
       "(jaemfoerelse per order, aeven om lagerkvantiteten skiljer sig fraan den begaerda).",
   ],
   "m1_t": "1. Matcha en lagerorder",
   "m1": "Vaelj en gul rad och dubbelklicka (eller anvaend knappen 'Matcha / Korrigera'). Du vaeljer "
         "foersaeljningsordern med samma produkt och kvantiteten.",
   "m1_steps": [
       "Dubbelklicka paa den gula raden (eller knappen <b>Matcha / Korrigera</b>)",
       "Vaelj <b>foersaeljningsorder</b> fraan listan (samma produkt, med tillgaengligt aaterstaaende)",
       "Ange <b>kvantitet</b> (inte mer aen minimum av lagertillgaengligt och orderns aaterstaaende)",
       "Saett <b>datum/tid</b> och <b>destination</b> (Normal Shipment / Direct to final Customer)",
       "Tryck <b>Matcha och skapa regel</b>",
   ],
   "m1_note": "OBS: foersaeljningsordern maaste ha SAMMA produkt (samma kod, utan versionssuffix). Om ingen "
              "foersaeljningsorder aennu finns foer den produkten foerblir raden att matcha tills relaterad "
              "order importeras.",
   "m2_t": "2. Korrigering 'redan skickat' (justering)",
   "m2": "Tills alla leveranser gaar genom systemet skulle varor som redan skickats utanfoer systemet felaktigt "
         "foerbli tillgaengliga. Fraan samma foenster laater knappen 'Redan skickat' dig ange hur mycket av "
         "ordern som redan skickats: den kvantiteten laemnar tillgaengligheten. Korrigeringen registreras med "
         "anvaendare, datum och anteckning.",
   "date_t": "Startdatum",
   "date": "Tillgaengligheten beaktar endast varor inlagrade fraan ett 'nollpunkt'-datum "
           "(instaellningen 'data_inizio_spedizioni'): foere det datumet antas allt redan skickat. "
           "Korrigeringen 'redan skickat' tjaenar just till att justera fall som lagrats efter det datumet och "
           "redan skickats.",
   "email_t": "Destination i e-posten",
   "email": "Vid fraktbekraeftelse visar e-posten foer varje pall destinationen (Normal Shipment eller Direct "
            "to final Customer); direktleveranser till slutkund markeras.",
   "step": "Steg", "desc": "Beskrivning", "item": "Element",
 },
}


def gen(lang, t):
    out = os.path.join(BASE, lang, "operazioni_spedizioni_magazzino.pdf")

    def story(s, wid):
        cover(s, t["title"], t["subtitle"], t["a"], t["v"])
        s.append(Paragraph(
            '<font name="Arial-Bold" size="9" color="#616161">Login: </font>'
            '<font name="Arial-Italic" size="9">%s</font>' % t["login"], B))
        s.append(sp(2)); s.append(Paragraph(t["intro"], B))

        s.append(Paragraph(t["leg_t"], H1))
        for it in t["leg_items"]:
            s.append(bul(it))

        s.append(Paragraph(t["m1_t"], H1))
        s.append(Paragraph(t["m1"], B))
        for st in t["m1_steps"]:
            s.append(bul(st))
        s.append(Paragraph(t["m1_note"], N))

        s.append(Paragraph(t["m2_t"], H1))
        s.append(Paragraph(t["m2"], B))

        s.append(Paragraph(t["date_t"], H1))
        s.append(Paragraph(t["date"], B))

        s.append(Paragraph(t["email_t"], H1))
        s.append(Paragraph(t["email"], B))

    build_pdf(out, story, t["ft"])
    print("  [%s] Spedizioni da magazzino" % lang.upper())


if __name__ == "__main__":
    print("Generazione manuale 'Spedizioni da magazzino' in 5 lingue...")
    for lc, tx in T.items():
        os.makedirs(os.path.join(BASE, lc), exist_ok=True)
        gen(lc, tx)
    print("\nCompletato! 5 PDF generati (1 per lingua x 5 lingue)")
