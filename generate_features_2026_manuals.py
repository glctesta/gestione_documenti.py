# -*- coding: utf-8 -*-
"""
Genera i manuali PDF per le funzionalita' aggiunte/aggiornate (2026) in 5 lingue.
Produce, per ogni lingua (it, ro, en, de, sv):
    manuals/{lang}/operazioni_conferma_spedizioni.pdf
    manuals/{lang}/materiali_validazione_scorie.pdf
    manuals/{lang}/produzione_fqc_aggiornamenti.pdf
Stesso layout dei generatori esistenti (generate_ops_manuals.py).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

LOGO_PATH = os.path.join(os.path.dirname(__file__), "Logo.png")
BASE_DIR = os.path.join(os.path.dirname(__file__), "manuals")

BLUE_DARK = HexColor("#1a237e")
BLUE_MED  = HexColor("#283593")
BLUE_LIGHT = HexColor("#e8eaf6")
GRAY_MED  = HexColor("#e0e0e0")
ORANGE    = HexColor("#e65100")

WINFONTS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
pdfmetrics.registerFont(TTFont("Arial",      os.path.join(WINFONTS, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(WINFONTS, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", os.path.join(WINFONTS, "ariali.ttf")))

title_style = ParagraphStyle("T", fontName="Arial-Bold", fontSize=22, textColor=BLUE_DARK,
    spaceAfter=4*mm, alignment=TA_CENTER)
sub_style = ParagraphStyle("S", fontName="Arial-Bold", fontSize=13, textColor=BLUE_MED,
    spaceAfter=8*mm, alignment=TA_CENTER)
h1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15, textColor=white,
    spaceAfter=4*mm, spaceBefore=6*mm, leftIndent=4*mm, leading=20,
    backColor=BLUE_DARK, borderPadding=(3*mm, 3*mm, 2*mm, 3*mm))
h2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=12, textColor=BLUE_MED,
    spaceAfter=2*mm, spaceBefore=5*mm, leading=16)
body = ParagraphStyle("B", fontName="Arial", fontSize=10, textColor=black,
    spaceAfter=2*mm, leading=14, alignment=TA_JUSTIFY)
note = ParagraphStyle("N", fontName="Arial-Italic", fontSize=9, textColor=HexColor("#1565c0"),
    spaceAfter=3*mm, spaceBefore=2*mm, leftIndent=6*mm, leading=12,
    backColor=BLUE_LIGHT, borderPadding=(2*mm, 2*mm, 2*mm, 2*mm))
warn = ParagraphStyle("W", fontName="Arial-Bold", fontSize=9, textColor=ORANGE,
    spaceAfter=3*mm, spaceBefore=2*mm, leftIndent=6*mm, leading=12,
    backColor=HexColor("#fff3e0"), borderPadding=(2*mm, 2*mm, 2*mm, 2*mm))


def sp(v=3): return Spacer(1, v*mm)
def hr(): return HRFlowable(width="100%", thickness=0.5, color=GRAY_MED, spaceBefore=3*mm, spaceAfter=3*mm)


def on_page(canvas_obj, doc, footer_text):
    canvas_obj.saveState()
    canvas_obj.setFont("Arial", 8)
    canvas_obj.setFillColor(HexColor("#9e9e9e"))
    canvas_obj.drawCentredString(A4[0]/2, 12*mm, "%s - Pagina %d" % (footer_text, doc.page))
    canvas_obj.setStrokeColor(BLUE_LIGHT)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(15*mm, A4[1]-12*mm, A4[0]-15*mm, A4[1]-12*mm)
    canvas_obj.restoreState()


# ==============================================================================
#  CONTENUTI (5 lingue). Ogni sezione: title, subtitle, desc, steps[(t,txt)], note, warn
# ==============================================================================
APP = "TraceabilityRS"
VER = {"it": "Versione 2.3.6", "ro": "Versiunea 2.3.6", "en": "Version 2.3.6",
       "de": "Version 2.3.6", "sv": "Version 2.3.6"}
FOOTER = {"it": "TraceabilityRS - Guida funzionalita'", "ro": "TraceabilityRS - Ghid functionalitati",
          "en": "TraceabilityRS - Features guide", "de": "TraceabilityRS - Funktionsleitfaden",
          "sv": "TraceabilityRS - Funktionsguide"}

SECTIONS = {
    "sped": {
        "it": {
            "title": "Conferma Spedizioni",
            "subtitle": "Conferma su pallet, documenti e correzioni",
            "desc": "La form 'Conferma Shipping' raggruppa gli ordini di produzione da spedire e mostra, per ogni "
                    "ordine, la quantita' da spedire, quella gia' confermata e il residuo. La conferma avviene su "
                    "uno o piu' pallet; una spedizione puo' contenere piu' ordini.",
            "steps": [
                ("1. Filtri e selezione ordine", "Usare i filtri Ordine e Prodotto per trovare l'ordine. La lista "
                 "mostra Qta da spedire, Confermato e Residuo. Selezionare la riga dell'ordine."),
                ("2. Aggiungere pallet", "Inserire il Codice Pallet (con suggerimento progressivo, univoco solo "
                 "entro la spedizione) e la quantita' spedita, poi 'Aggiungi a spedizione': il residuo si scala. "
                 "L'eccesso oltre la quantita' da spedire e' consentito con avviso."),
                ("3. Finalizzare", "Impostare la data di spedizione e premere 'Finalizza spedizione': vengono "
                 "generati due PDF (lista per pallet e riepilogo) con logo, data e operatore, e inviata l'email ai "
                 "destinatari configurati (Sys_shipment_email) con i PDF allegati."),
                ("4. Recupero e correzione", "Con 'Recupera spedizione...' si cerca una spedizione per data, si "
                 "modificano i pallet, si ristampano i documenti e si invia un'email di correzione."),
            ],
            "note": "I documenti sono archiviati e sempre ristampabili: vengono rigenerati dagli snapshot salvati, "
                    "quindi restano stabili nel tempo.",
            "warn": "I codici pallet devono essere univoci solo all'interno della stessa spedizione; in spedizioni "
                    "o giorni diversi possono ripetersi.",
        },
        "en": {
            "title": "Shipment Confirmation",
            "subtitle": "Pallet confirmation, documents and corrections",
            "desc": "The 'Confirm Shipping' form groups the production orders to ship and shows, per order, the "
                    "quantity to ship, the already confirmed amount and the remaining. Confirmation is done on one "
                    "or more pallets; a shipment may contain several orders.",
            "steps": [
                ("1. Filters and order selection", "Use the Order and Product filters to find the order. The list "
                 "shows Qty to ship, Confirmed and Remaining. Select the order row."),
                ("2. Add pallet", "Enter the Pallet Code (auto-incremented suggestion, unique only within the "
                 "shipment) and the shipped quantity, then 'Add to shipment': the remaining decreases. Exceeding the "
                 "quantity to ship is allowed with a warning."),
                ("3. Finalize", "Set the shipment date and click 'Finalize shipment': two PDFs are generated (pallet "
                 "list and summary) with logo, date and operator, and an email is sent to the configured recipients "
                 "(Sys_shipment_email) with the PDFs attached."),
                ("4. Retrieve and correct", "With 'Retrieve shipment...' you search a shipment by date, edit pallets, "
                 "reprint documents and send a correction email."),
            ],
            "note": "Documents are archived and always reprintable: they are regenerated from saved snapshots, so "
                    "they stay stable over time.",
            "warn": "Pallet codes must be unique only within the same shipment; they may repeat in different "
                    "shipments or days.",
        },
        "ro": {
            "title": "Confirmare Expedieri",
            "subtitle": "Confirmare pe palet, documente si corectii",
            "desc": "Formularul 'Confirmare Shipping' grupeaza comenzile de productie de expediat si arata, pentru "
                    "fiecare comanda, cantitatea de expediat, cea deja confirmata si restul. Confirmarea se face pe "
                    "unul sau mai multi paleti; o expediere poate contine mai multe comenzi.",
            "steps": [
                ("1. Filtre si selectie comanda", "Folositi filtrele Comanda si Produs. Lista arata Cant. de "
                 "expediat, Confirmat si Rest. Selectati randul comenzii."),
                ("2. Adaugare palet", "Introduceti Codul Paletului (sugestie progresiva, unic doar in cadrul "
                 "expedierii) si cantitatea expediata, apoi 'Adauga la expediere': restul scade. Depasirea "
                 "cantitatii de expediat este permisa cu avertizare."),
                ("3. Finalizare", "Setati data expedierii si apasati 'Finalizeaza expedierea': se genereaza doua "
                 "PDF-uri (lista pe palet si rezumat) cu logo, data si operator, si se trimite e-mail catre "
                 "destinatarii configurati (Sys_shipment_email) cu PDF-urile atasate."),
                ("4. Recuperare si corectie", "Cu 'Recuperare expediere...' cautati o expediere dupa data, "
                 "modificati paletii, reimprimati documentele si trimiteti un e-mail de corectie."),
            ],
            "note": "Documentele sunt arhivate si pot fi reimprimate oricand: se regenereaza din datele salvate, "
                    "deci raman stabile in timp.",
            "warn": "Codurile de palet trebuie sa fie unice doar in cadrul aceleiasi expedieri; in expedieri sau "
                    "zile diferite se pot repeta.",
        },
        "de": {
            "title": "Sendungsbestaetigung",
            "subtitle": "Palettenbestaetigung, Dokumente und Korrekturen",
            "desc": "Das Formular 'Confirm Shipping' gruppiert die zu versendenden Produktionsauftraege und zeigt "
                    "je Auftrag die zu versendende Menge, die bereits bestaetigte Menge und den Rest. Die "
                    "Bestaetigung erfolgt auf einer oder mehreren Paletten; eine Sendung kann mehrere Auftraege "
                    "enthalten.",
            "steps": [
                ("1. Filter und Auftragsauswahl", "Nutzen Sie die Filter Auftrag und Produkt. Die Liste zeigt zu "
                 "versendende Menge, Bestaetigt und Rest. Waehlen Sie die Auftragszeile."),
                ("2. Palette hinzufuegen", "Geben Sie den Palettencode (fortlaufender Vorschlag, nur innerhalb der "
                 "Sendung eindeutig) und die versandte Menge ein, dann 'Zur Sendung hinzufuegen': der Rest sinkt. "
                 "Ueberschreiten der zu versendenden Menge ist mit Warnung erlaubt."),
                ("3. Abschliessen", "Versanddatum setzen und 'Sendung abschliessen' klicken: zwei PDFs werden "
                 "erstellt (Palettenliste und Zusammenfassung) mit Logo, Datum und Bediener, und eine E-Mail wird "
                 "an die konfigurierten Empfaenger (Sys_shipment_email) mit den PDFs gesendet."),
                ("4. Abrufen und korrigieren", "Mit 'Sendung abrufen...' suchen Sie eine Sendung nach Datum, "
                 "bearbeiten Paletten, drucken Dokumente neu und senden eine Korrektur-E-Mail."),
            ],
            "note": "Dokumente werden archiviert und sind jederzeit neu druckbar: sie werden aus gespeicherten "
                    "Snapshots neu erstellt und bleiben so stabil.",
            "warn": "Palettencodes muessen nur innerhalb derselben Sendung eindeutig sein; in anderen Sendungen "
                    "oder Tagen koennen sie sich wiederholen.",
        },
        "sv": {
            "title": "Leveransbekraeftelse",
            "subtitle": "Pallbekraeftelse, dokument och korrigeringar",
            "desc": "Formulaeret 'Confirm Shipping' grupperar produktionsordrarna som ska skickas och visar per "
                    "order kvantitet att skicka, redan bekraeftat och aterstaende. Bekraeftelse goers paa en eller "
                    "flera pallar; en leverans kan innehaalla flera ordrar.",
            "steps": [
                ("1. Filter och orderval", "Anvaend filtren Order och Produkt. Listan visar kvantitet att skicka, "
                 "Bekraeftat och Aterstaende. Vaelj orderraden."),
                ("2. Laegg till pall", "Ange Pallkod (loepande foerslag, unik endast inom leveransen) och skickad "
                 "kvantitet, sedan 'Laegg till i leverans': aterstaende minskar. Att oeverstiga kvantiteten att "
                 "skicka aer tillaatet med varning."),
                ("3. Slutfoer", "Saett leveransdatum och klicka 'Slutfoer leverans': tvaa PDF:er skapas (pall-lista "
                 "och sammanfattning) med logotyp, datum och operatoer, och ett e-postmeddelande skickas till de "
                 "konfigurerade mottagarna (Sys_shipment_email) med PDF:erna bifogade."),
                ("4. Haemta och korrigera", "Med 'Haemta leverans...' soeker du en leverans efter datum, redigerar "
                 "pallar, skriver ut dokument igen och skickar ett korrigerings-e-postmeddelande."),
            ],
            "note": "Dokument arkiveras och kan alltid skrivas ut igen: de aterskapas fraan sparade oegonblicksbilder "
                    "och foerblir stabila oever tid.",
            "warn": "Pallkoder behoever vara unika endast inom samma leverans; i andra leveranser eller dagar kan de "
                    "upprepas.",
        },
    },
    "scor": {
        "it": {
            "title": "Convalida Quantita' Dichiarate (Scorie/Rientri)",
            "subtitle": "Validazione scorie e blocco preparazione/rilascio",
            "desc": "I materiali legati al ritorno di altri materiali (o dello stesso codice) richiedono che le "
                    "scorie/rientri dichiarati siano CONFERMATI dal controllore. Senza conferma, la richiesta del "
                    "materiale non puo' essere ne' preparata ne' rilasciata.",
            "steps": [
                ("1. Dichiarazione (magazzino)", "Nella form Scorie il magazzino dichiara i kg rientrati per il "
                 "codice scoria (MustCode), come in precedenza."),
                ("2. Convalida (controllo)", "Dal menu Materiali Indiretti > 'Convalida Quantita' Dichiarate', "
                 "selezionare la registrazione, inserire il Peso rilevato e premere 'Convalida': il sistema salva "
                 "il peso confermato, l'utente e l'esito (conforme se il peso corrisponde)."),
                ("3. Effetto su prep/rilascio", "In 'Conferma Materiali', la preparazione e il rilascio di una "
                 "richiesta vengono bloccati finche' le scorie collegate non risultano confermate; un messaggio "
                 "indica di usare 'Convalida Quantita' Dichiarate'."),
            ],
            "note": "La voce di menu 'Conferma Materiali' richiede ora l'autorizzazione 'rilascia_materiali'.",
            "warn": "Senza convalida (esito conforme) il materiale legato a un ritorno resta bloccato in "
                    "preparazione e rilascio.",
        },
        "en": {
            "title": "Validate Declared Quantities (Scrap/Returns)",
            "subtitle": "Scrap validation and preparation/release gating",
            "desc": "Materials linked to the return of other materials (or the same code) require the declared "
                    "scrap/returns to be CONFIRMED by the controller. Without confirmation, the material request "
                    "cannot be prepared nor released.",
            "steps": [
                ("1. Declaration (warehouse)", "In the Scrap form the warehouse declares the returned kg for the "
                 "scrap code (MustCode), as before."),
                ("2. Validation (control)", "From Indirect Materials > 'Validate Declared Quantities', select the "
                 "record, enter the Measured weight and click 'Validate': the system saves the confirmed weight, "
                 "the user and the result (compliant if the weight matches)."),
                ("3. Effect on prep/release", "In 'Confirm Materials', preparation and release of a request are "
                 "blocked until the linked scrap is confirmed; a message tells you to use 'Validate Declared "
                 "Quantities'."),
            ],
            "note": "The 'Confirm Materials' menu item now requires the 'rilascia_materiali' authorization.",
            "warn": "Without validation (compliant result) a material linked to a return stays blocked in "
                    "preparation and release.",
        },
        "ro": {
            "title": "Validare Cantitati Declarate (Deseuri/Retururi)",
            "subtitle": "Validarea deseurilor si blocarea pregatirii/eliberarii",
            "desc": "Materialele legate de returul altor materiale (sau al aceluiasi cod) necesita ca "
                    "deseurile/retururile declarate sa fie CONFIRMATE de controlor. Fara confirmare, cererea "
                    "materialului nu poate fi nici pregatita, nici eliberata.",
            "steps": [
                ("1. Declarare (depozit)", "In formularul Deseuri, depozitul declara kg returnati pentru codul de "
                 "deseu (MustCode), ca si pana acum."),
                ("2. Validare (control)", "Din Materiale Indirecte > 'Validare Cantitati Declarate', selectati "
                 "inregistrarea, introduceti Greutatea masurata si apasati 'Validare': sistemul salveaza greutatea "
                 "confirmata, utilizatorul si rezultatul (conform daca greutatea corespunde)."),
                ("3. Efect asupra pregatirii/eliberarii", "In 'Confirmare Materiale', pregatirea si eliberarea unei "
                 "cereri sunt blocate pana cand deseurile legate sunt confirmate; un mesaj indica folosirea "
                 "'Validare Cantitati Declarate'."),
            ],
            "note": "Optiunea de meniu 'Confirmare Materiale' necesita acum autorizarea 'rilascia_materiali'.",
            "warn": "Fara validare (rezultat conform) materialul legat de un retur ramane blocat la pregatire si "
                    "eliberare.",
        },
        "de": {
            "title": "Deklarierte Mengen validieren (Ausschuss/Rueckgaben)",
            "subtitle": "Ausschussvalidierung und Sperre fuer Vorbereitung/Freigabe",
            "desc": "Materialien, die mit der Rueckgabe anderer Materialien (oder desselben Codes) verknuepft sind, "
                    "erfordern, dass der deklarierte Ausschuss vom Pruefer BESTAETIGT wird. Ohne Bestaetigung kann "
                    "die Materialanforderung weder vorbereitet noch freigegeben werden.",
            "steps": [
                ("1. Deklaration (Lager)", "Im Ausschuss-Formular deklariert das Lager die zurueckgegebenen kg fuer "
                 "den Ausschusscode (MustCode), wie bisher."),
                ("2. Validierung (Kontrolle)", "Unter Indirekte Materialien > 'Deklarierte Mengen validieren' den "
                 "Eintrag waehlen, das gemessene Gewicht eingeben und 'Validieren' klicken: das System speichert "
                 "das bestaetigte Gewicht, den Benutzer und das Ergebnis (konform bei Uebereinstimmung)."),
                ("3. Auswirkung auf Vorbereitung/Freigabe", "In 'Materialien bestaetigen' werden Vorbereitung und "
                 "Freigabe einer Anforderung gesperrt, bis der verknuepfte Ausschuss bestaetigt ist; eine Meldung "
                 "verweist auf 'Deklarierte Mengen validieren'."),
            ],
            "note": "Der Menuepunkt 'Materialien bestaetigen' erfordert nun die Berechtigung 'rilascia_materiali'.",
            "warn": "Ohne Validierung (konformes Ergebnis) bleibt ein mit einer Rueckgabe verknuepftes Material in "
                    "Vorbereitung und Freigabe gesperrt.",
        },
        "sv": {
            "title": "Validera deklarerade kvantiteter (Skrot/Returer)",
            "subtitle": "Skrotvalidering och spaerr foer beredning/frislaeppning",
            "desc": "Material kopplade till retur av andra material (eller samma kod) kraever att det deklarerade "
                    "skrotet BEKRAEFTAS av kontrollanten. Utan bekraeftelse kan materialfoerfraagan varken beredas "
                    "eller frislaeppas.",
            "steps": [
                ("1. Deklaration (lager)", "I Skrot-formulaeret deklarerar lagret returnerade kg foer skrotkoden "
                 "(MustCode), som tidigare."),
                ("2. Validering (kontroll)", "Fraan Indirekta Material > 'Validera deklarerade kvantiteter', vaelj "
                 "posten, ange Uppmaett vikt och klicka 'Validera': systemet sparar bekraeftad vikt, anvaendare och "
                 "resultat (oeverensstaemmande om vikten matchar)."),
                ("3. Effekt paa beredning/frislaeppning", "I 'Bekraefta material' spaerras beredning och "
                 "frislaeppning av en foerfraagan tills kopplat skrot aer bekraeftat; ett meddelande haenvisar till "
                 "'Validera deklarerade kvantiteter'."),
            ],
            "note": "Menyalternativet 'Bekraefta material' kraever nu behoerigheten 'rilascia_materiali'.",
            "warn": "Utan validering (oeverensstaemmande resultat) foerblir ett material kopplat till en retur "
                    "spaerrat i beredning och frislaeppning.",
        },
    },
    "fqc": {
        "it": {
            "title": "FQC Prodotti - Aggiornamenti",
            "subtitle": "Filtro piano, report per ordine, sessione continua",
            "desc": "Aggiornamenti all'esecuzione dei controlli FQC Prodotti e al relativo report.",
            "steps": [
                ("1. Filtro 'solo codici con piano'", "Nella schermata di esecuzione e' disponibile una casella di "
                 "spunta che filtra l'elenco prodotti mostrando solo i codici che hanno un piano di verifica "
                 "(checklist) caricato."),
                ("2. Sessione continua", "Dopo aver confermato e salvato un FQC, la finestra NON si chiude piu': si "
                 "azzera automaticamente (LabelCode ed esiti) mantenendo cliente/prodotto/checklist, pronta per la "
                 "scheda successiva."),
                ("3. Report per ordine", "Nel report 'Schede Validate' e' stato aggiunto il filtro Ordine, oltre ai "
                 "filtri esistenti (periodo, codice prodotto, LabelCode)."),
            ],
            "note": "Le altre funzioni dell'esecuzione FQC restano invariate.",
            "warn": "Verificare sempre il LabelCode prima di salvare i risultati della checklist.",
        },
        "en": {
            "title": "FQC Products - Updates",
            "subtitle": "Plan filter, report by order, continuous session",
            "desc": "Updates to the FQC Products checks execution and its report.",
            "steps": [
                ("1. 'Only codes with a plan' filter", "In the execution screen a checkbox filters the product list "
                 "to show only codes that have a verification plan (checklist) loaded."),
                ("2. Continuous session", "After confirming and saving an FQC, the window no longer closes: it "
                 "automatically resets (LabelCode and results) keeping client/product/checklist, ready for the next "
                 "card."),
                ("3. Report by order", "In the 'Validated Cards' report an Order filter was added, in addition to "
                 "the existing filters (period, product code, LabelCode)."),
            ],
            "note": "The other FQC execution functions remain unchanged.",
            "warn": "Always verify the LabelCode before saving the checklist results.",
        },
        "ro": {
            "title": "FQC Produse - Actualizari",
            "subtitle": "Filtru plan, raport pe comanda, sesiune continua",
            "desc": "Actualizari la executarea controalelor FQC Produse si la raportul aferent.",
            "steps": [
                ("1. Filtru 'doar coduri cu plan'", "In ecranul de executare exista o casuta care filtreaza lista "
                 "de produse afisand doar codurile care au un plan de verificare (lista) incarcat."),
                ("2. Sesiune continua", "Dupa confirmarea si salvarea unui FQC, fereastra NU se mai inchide: se "
                 "reseteaza automat (LabelCode si rezultate) pastrand client/produs/lista, gata pentru fisa "
                 "urmatoare."),
                ("3. Raport pe comanda", "In raportul 'Fise Validate' a fost adaugat filtrul Comanda, pe langa "
                 "filtrele existente (perioada, cod produs, LabelCode)."),
            ],
            "note": "Celelalte functii ale executarii FQC raman neschimbate.",
            "warn": "Verificati intotdeauna LabelCode inainte de a salva rezultatele listei.",
        },
        "de": {
            "title": "FQC Produkte - Aktualisierungen",
            "subtitle": "Planfilter, Bericht nach Auftrag, fortlaufende Sitzung",
            "desc": "Aktualisierungen der FQC-Produktpruefungen und des zugehoerigen Berichts.",
            "steps": [
                ("1. Filter 'nur Codes mit Plan'", "Im Ausfuehrungsbildschirm filtert ein Kontrollkaestchen die "
                 "Produktliste und zeigt nur Codes mit geladenem Pruefplan (Checkliste)."),
                ("2. Fortlaufende Sitzung", "Nach Bestaetigen und Speichern eines FQC schliesst sich das Fenster "
                 "nicht mehr: es setzt sich automatisch zurueck (LabelCode und Ergebnisse) und behaelt "
                 "Kunde/Produkt/Checkliste fuer die naechste Karte."),
                ("3. Bericht nach Auftrag", "Im Bericht 'Validierte Karten' wurde der Filter Auftrag hinzugefuegt, "
                 "zusaetzlich zu den bestehenden Filtern (Zeitraum, Produktcode, LabelCode)."),
            ],
            "note": "Die uebrigen Funktionen der FQC-Ausfuehrung bleiben unveraendert.",
            "warn": "Pruefen Sie immer den LabelCode, bevor Sie die Checklisten-Ergebnisse speichern.",
        },
        "sv": {
            "title": "FQC Produkter - Uppdateringar",
            "subtitle": "Planfilter, rapport per order, kontinuerlig session",
            "desc": "Uppdateringar av FQC-produktkontrollernas genomfoerande och tillhoerande rapport.",
            "steps": [
                ("1. Filter 'endast koder med plan'", "I genomfoerandevyn filtrerar en kryssruta produktlistan och "
                 "visar endast koder som har en kontrollplan (checklista) laddad."),
                ("2. Kontinuerlig session", "Efter att ha bekraeftat och sparat en FQC staengs foenstret inte "
                 "laengre: det aaterstaells automatiskt (LabelCode och resultat) och behaaller "
                 "kund/produkt/checklista, redo foer naesta kort."),
                ("3. Rapport per order", "I rapporten 'Validerade kort' har ett Order-filter lagts till, utoever de "
                 "befintliga filtren (period, produktkod, LabelCode)."),
            ],
            "note": "Oevriga funktioner i FQC-genomfoerandet aer ofoeraendrade.",
            "warn": "Verifiera alltid LabelCode innan du sparar checklistans resultat.",
        },
    },
}

FILENAMES = {
    "sped": "operazioni_conferma_spedizioni.pdf",
    "scor": "materiali_validazione_scorie.pdf",
    "fqc":  "produzione_fqc_aggiornamenti.pdf",
}


def build_section(lang, pfx):
    s = SECTIONS[pfx][lang]
    out = os.path.join(BASE_DIR, lang, FILENAMES[pfx])
    doc = SimpleDocTemplate(out, pagesize=A4,
        topMargin=18*mm, bottomMargin=20*mm, leftMargin=15*mm, rightMargin=15*mm)
    story = []
    story.append(sp(20))
    if os.path.exists(LOGO_PATH):
        story.append(Image(LOGO_PATH, width=50*mm, height=50*mm))
        story.append(sp(6))
    story.append(Paragraph(APP, title_style))
    story.append(Paragraph(VER[lang], sub_style))
    story.append(Paragraph(s["title"], title_style))
    story.append(Paragraph(s["subtitle"], sub_style))
    story.append(hr())
    story.append(Paragraph(s["desc"], body))
    story.append(sp(4))
    for (st_t, st_x) in s["steps"]:
        story.append(Paragraph(st_t, h2))
        story.append(Paragraph(st_x, body))
    story.append(hr())
    story.append(Paragraph(s["note"], note))
    story.append(Paragraph(s["warn"], warn))
    doc.build(story, onFirstPage=lambda c, d: on_page(c, d, FOOTER[lang]),
              onLaterPages=lambda c, d: on_page(c, d, FOOTER[lang]))
    print(f"  -> {out}")


if __name__ == "__main__":
    count = 0
    for lang in ("it", "ro", "en", "de", "sv"):
        os.makedirs(os.path.join(BASE_DIR, lang), exist_ok=True)
        print(f"[{lang}]")
        for pfx in ("sped", "scor", "fqc"):
            build_section(lang, pfx)
            count += 1
    print(f"\nDone! {count} PDF generati.")
