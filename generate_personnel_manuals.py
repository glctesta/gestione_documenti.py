# -*- coding: utf-8 -*-
"""
Genera i manuali PDF per la sezione 'Personale' in 5 lingue.
Produce: manuals/{lang}/personale_assenze.pdf
         manuals/{lang}/personale_messaggi.pdf
         manuals/{lang}/personale_note_disciplinari.pdf
         manuals/{lang}/personale_ospiti.pdf
         manuals/{lang}/personale_straordinari.pdf
         manuals/{lang}/personale_programmi_esterni.pdf
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

LOGO_PATH = os.path.join(os.path.dirname(__file__), "Logo.png")
BASE_DIR = os.path.join(os.path.dirname(__file__), "manuals")
BLUE_DARK = HexColor("#1a237e"); BLUE_MED = HexColor("#283593"); BLUE_LIGHT = HexColor("#e8eaf6")
GRAY_LIGHT = HexColor("#f5f5f5"); GRAY_MED = HexColor("#e0e0e0"); ACCENT = HexColor("#0d47a1")
ORANGE = HexColor("#e65100"); GREEN_D = HexColor("#2e7d32")
WINFONTS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
pdfmetrics.registerFont(TTFont("Arial", os.path.join(WINFONTS, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(WINFONTS, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", os.path.join(WINFONTS, "ariali.ttf")))

title_style = ParagraphStyle("T", fontName="Arial-Bold", fontSize=22, textColor=BLUE_DARK, spaceAfter=4*mm, alignment=TA_CENTER)
sub_style = ParagraphStyle("S", fontName="Arial-Bold", fontSize=14, textColor=BLUE_MED, spaceAfter=8*mm, alignment=TA_CENTER)
h1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=16, textColor=white, spaceAfter=4*mm, spaceBefore=6*mm, leftIndent=4*mm, leading=20, backColor=BLUE_DARK, borderPadding=(3*mm,3*mm,2*mm,3*mm))
h2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=12, textColor=BLUE_MED, spaceAfter=2*mm, spaceBefore=5*mm, leading=16)
body = ParagraphStyle("B", fontName="Arial", fontSize=10, textColor=black, spaceAfter=2*mm, leading=14, alignment=TA_JUSTIFY)
note_s = ParagraphStyle("N", fontName="Arial-Italic", fontSize=9, textColor=HexColor("#1565c0"), spaceAfter=3*mm, spaceBefore=2*mm, leftIndent=6*mm, leading=12, backColor=BLUE_LIGHT, borderPadding=(2*mm,2*mm,2*mm,2*mm))
warn_s = ParagraphStyle("W", fontName="Arial-Bold", fontSize=9, textColor=ORANGE, spaceAfter=3*mm, spaceBefore=2*mm, leftIndent=6*mm, leading=12, backColor=HexColor("#fff3e0"), borderPadding=(2*mm,2*mm,2*mm,2*mm))

def sp(v=3): return Spacer(1, v*mm)
def hr(): return HRFlowable(width="100%", thickness=0.5, color=GRAY_MED, spaceBefore=3*mm, spaceAfter=3*mm)
def make_table(headers, rows, W):
    data = [headers] + rows
    t = Table(data, colWidths=[42*mm, W-42*mm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),BLUE_DARK),("TEXTCOLOR",(0,0),(-1,0),white),("FONTNAME",(0,0),(-1,0),"Arial-Bold"),("FONTSIZE",(0,0),(-1,0),10),("FONTNAME",(0,1),(-1,-1),"Arial"),("FONTSIZE",(0,1),(-1,-1),9),("ROWBACKGROUNDS",(0,1),(-1,-1),[white,GRAY_LIGHT]),("GRID",(0,0),(-1,-1),0.5,GRAY_MED),("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),("LEFTPADDING",(0,0),(-1,-1),4)]))
    return t
def on_page(c, d, ft):
    c.saveState(); c.setFont("Arial",8); c.setFillColor(HexColor("#9e9e9e"))
    c.drawCentredString(A4[0]/2,12*mm,"%s - Pagina %d"%(ft,d.page))
    c.setStrokeColor(BLUE_LIGHT); c.setLineWidth(0.5); c.line(15*mm,A4[1]-12*mm,A4[0]-15*mm,A4[1]-12*mm); c.restoreState()

# Each manual definition: (section_key, title_key_prefix)
MANUALS = [
    ("personale_assenze", "abs"),
    ("personale_messaggi", "msg"),
    ("personale_note_disciplinari", "disc"),
    ("personale_ospiti", "osp"),
    ("personale_straordinari", "str"),
    ("personale_programmi_esterni", "prog"),
]

TEXTS = {}
for lang, (footer, field_l, desc_l, titles, descs, steps, fields, notes, warns) in {
    "it": ("TraceabilityRS - Personale", "Campo", "Descrizione",
        {"abs":"Gestione Assenze","msg":"Gestione Messaggi","disc":"Note Disciplinari","osp":"Gestione Ospiti","str":"Gestione Straordinari","prog":"Programmi Esterni"},
        {"abs":"Il modulo Assenze consente di registrare e gestire le assenze del personale, inclusi permessi, ferie, malattia e altre tipologie. Il responsabile puo' approvare o rifiutare le richieste.",
         "msg":"Il modulo Messaggi permette di inviare comunicazioni interne al personale, con possibilita' di allegare documenti e impostare priorita'.",
         "disc":"Il modulo Note Disciplinari consente di registrare provvedimenti disciplinari (Referat), generare documenti PDF formali e inviare notifiche via email.",
         "osp":"Il modulo Ospiti gestisce la registrazione dei visitatori, inclusa la prenotazione di hotel, trasferimenti e la gestione del programma di visita.",
         "str":"Il modulo Straordinari permette di registrare e gestire le ore di lavoro straordinario del personale, con approvazione gerarchica e reportistica.",
         "prog":"Il modulo Programmi Esterni consente di gestire i programmi di formazione esterni, esami e certificazioni del personale."},
        {"abs":["1. Nuova Richiesta / Registrare una nuova assenza compilando tipo, date e motivo.","2. Approvazione / Il responsabile verifica e approva o rifiuta la richiesta.","3. Calendario / Visualizzare il calendario assenze del reparto.","4. Report / Generare report riepilogativi per periodo."],
         "msg":["1. Nuovo Messaggio / Compilare oggetto, testo e selezionare i destinatari.","2. Allegati / Aggiungere eventuali allegati al messaggio.","3. Invio / Inviare il messaggio. I destinatari riceveranno una notifica.","4. Archivio / Consultare i messaggi inviati e ricevuti."],
         "disc":["1. Nuova Nota / Creare una nuova nota disciplinare selezionando il dipendente e il tipo di provvedimento.","2. Compilazione / Inserire la descrizione dettagliata dell'evento e le azioni previste.","3. Generazione PDF / Il sistema genera automaticamente il documento formale (Referat).","4. Notifica / Il dipendente e i responsabili vengono notificati via email."],
         "osp":["1. Registrazione Ospite / Inserire i dati dell'ospite: nome, azienda, data visita.","2. Prenotazioni / Gestire prenotazioni hotel e trasferimenti se necessario.","3. Programma / Definire il programma della visita con orari e responsabili.","4. Check-in/out / Registrare arrivo e partenza dell'ospite."],
         "str":["1. Richiesta Straordinario / Inserire data, ore previste e motivo.","2. Approvazione / Il responsabile approva la richiesta di straordinario.","3. Consuntivo / Registrare le ore effettivamente lavorate.","4. Report / Generare il report mensile degli straordinari."],
         "prog":["1. Nuovo Programma / Registrare un nuovo programma di formazione o esame.","2. Iscrizione / Iscrivere i dipendenti al programma.","3. Valutazione / Registrare i risultati delle valutazioni.","4. Certificazione / Gestire le certificazioni ottenute."]},
        {"abs":[("Tipo *","Tipo di assenza (Ferie, Malattia, Permesso, ecc.)"),("Data Inizio *","Data di inizio dell'assenza"),("Data Fine *","Data di fine dell'assenza"),("Motivo","Motivazione dell'assenza"),("Stato","Stato della richiesta (Pendente, Approvata, Rifiutata)")],
         "msg":[("Oggetto *","Oggetto del messaggio"),("Testo *","Corpo del messaggio"),("Destinatari *","Lista dei destinatari"),("Priorita'","Livello di priorita' del messaggio"),("Allegati","File allegati al messaggio")],
         "disc":[("Dipendente *","Dipendente oggetto del provvedimento"),("Tipo *","Tipo di provvedimento disciplinare"),("Data *","Data del provvedimento"),("Descrizione *","Descrizione dettagliata dell'evento"),("Azioni","Azioni disciplinari previste")],
         "osp":[("Nome *","Nome dell'ospite"),("Azienda *","Azienda di appartenenza"),("Data Visita *","Data prevista della visita"),("Responsabile *","Responsabile interno della visita"),("Note","Note aggiuntive sulla visita")],
         "str":[("Data *","Data dello straordinario"),("Ore Previste *","Numero di ore previste"),("Motivo *","Motivazione dello straordinario"),("Turno","Turno di lavoro"),("Stato","Stato della richiesta")],
         "prog":[("Programma *","Nome del programma formativo"),("Tipo *","Tipo (Formazione, Esame, Certificazione)"),("Data *","Data del programma"),("Partecipanti","Elenco dei partecipanti"),("Risultato","Esito del programma")]},
        {"abs":"NOTA: Le assenze approvate vengono automaticamente riportate nel calendario aziendale.",
         "msg":"NOTA: I messaggi con priorita' alta generano una notifica immediata.",
         "disc":"NOTA: Le note disciplinari vengono archiviate nel fascicolo personale del dipendente.",
         "osp":"NOTA: Gli ospiti devono compilare il modulo di registrazione all'ingresso.",
         "str":"NOTA: Gli straordinari devono essere approvati prima dell'inizio del lavoro.",
         "prog":"NOTA: Le certificazioni in scadenza generano un avviso automatico."},
        {"abs":"ATTENZIONE: Le assenze non approvate entro 48 ore vengono automaticamente rifiutate.",
         "msg":"ATTENZIONE: I messaggi non possono essere modificati dopo l'invio.",
         "disc":"ATTENZIONE: Le note disciplinari non possono essere eliminate dopo la generazione del PDF.",
         "osp":"ATTENZIONE: Le prenotazioni hotel devono essere confermate almeno 24 ore prima dell'arrivo.",
         "str":"ATTENZIONE: Il superamento del limite mensile di straordinari richiede l'approvazione della direzione.",
         "prog":"ATTENZIONE: L'iscrizione a un esame deve essere confermata almeno 7 giorni prima."}),
    "ro": ("TraceabilityRS - Personal", "Camp", "Descriere",
        {"abs":"Gestionare Absente","msg":"Gestionare Mesaje","disc":"Note Disciplinare","osp":"Gestionare Vizitatori","str":"Gestionare Ore Suplimentare","prog":"Programe Externe"},
        {"abs":"Modulul Absente permite inregistrarea si gestionarea absentelor personalului.","msg":"Modulul Mesaje permite trimiterea comunicarilor interne catre personal.","disc":"Modulul Note Disciplinare permite inregistrarea masurilor disciplinare si generarea documentelor PDF.","osp":"Modulul Vizitatori gestioneaza inregistrarea vizitatorilor, inclusiv rezervarile de hotel.","str":"Modulul Ore Suplimentare permite inregistrarea si gestionarea orelor suplimentare.","prog":"Modulul Programe Externe permite gestionarea programelor de formare externe."},
        {"abs":["1. Cerere noua / Inregistrati o noua absenta.","2. Aprobare / Responsabilul verifica si aproba.","3. Calendar / Vizualizati calendarul absentelor.","4. Rapoarte / Generati rapoarte."],
         "msg":["1. Mesaj nou / Completati subiectul si textul.","2. Atasamente / Adaugati fisiere.","3. Trimitere / Trimiteti mesajul.","4. Arhiva / Consultati mesajele."],
         "disc":["1. Nota noua / Creati o nota disciplinara.","2. Completare / Inserati descrierea detaliata.","3. Generare PDF / Sistemul genereaza documentul.","4. Notificare / Angajatul este notificat."],
         "osp":["1. Inregistrare / Inserati datele vizitatorului.","2. Rezervari / Gestionati rezervarile.","3. Program / Definiti programul vizitei.","4. Check-in/out / Inregistrati sosirea."],
         "str":["1. Cerere / Inserati data si orele.","2. Aprobare / Responsabilul aproba.","3. Consuntiv / Inregistrati orele efective.","4. Raport / Generati raportul lunar."],
         "prog":["1. Program nou / Inregistrati un program.","2. Inscriere / Inscrieti angajatii.","3. Evaluare / Inregistrati rezultatele.","4. Certificare / Gestionati certificarile."]},
        {"abs":[("Tip *","Tipul absentei"),("Data Start *","Data de inceput"),("Data Sfarsit *","Data de sfarsit"),("Motiv","Motivul absentei"),("Stare","Starea cererii")],
         "msg":[("Subiect *","Subiectul mesajului"),("Text *","Corpul mesajului"),("Destinatari *","Lista destinatarilor"),("Prioritate","Nivel de prioritate"),("Atasamente","Fisiere atasate")],
         "disc":[("Angajat *","Angajatul vizat"),("Tip *","Tipul masurii"),("Data *","Data masurii"),("Descriere *","Descrierea detaliata"),("Actiuni","Actiuni disciplinare")],
         "osp":[("Nume *","Numele vizitatorului"),("Companie *","Compania"),("Data Vizita *","Data vizitei"),("Responsabil *","Responsabil intern"),("Note","Note suplimentare")],
         "str":[("Data *","Data"),("Ore Prevazute *","Numarul de ore"),("Motiv *","Motivul"),("Tura","Tura de lucru"),("Stare","Starea cererii")],
         "prog":[("Program *","Numele programului"),("Tip *","Tipul"),("Data *","Data"),("Participanti","Lista participantilor"),("Rezultat","Rezultatul")]},
        {"abs":"NOTA: Absentele aprobate sunt raportate automat in calendarul companiei.","msg":"NOTA: Mesajele cu prioritate mare genereaza notificare imediata.","disc":"NOTA: Notele disciplinare sunt arhivate in dosarul personal.","osp":"NOTA: Vizitatorii trebuie sa completeze formularul la intrare.","str":"NOTA: Orele suplimentare trebuie aprobate inainte de inceperea lucrului.","prog":"NOTA: Certificarile care expira genereaza un avertisment automat."},
        {"abs":"ATENTIE: Cererile neaprobate in 48h sunt refuzate automat.","msg":"ATENTIE: Mesajele nu pot fi modificate dupa trimitere.","disc":"ATENTIE: Notele nu pot fi sterse dupa generarea PDF.","osp":"ATENTIE: Rezervarile hotel trebuie confirmate cu 24h inainte.","str":"ATENTIE: Depasirea limitei lunare necesita aprobarea conducerii.","prog":"ATENTIE: Inscrierea la examen trebuie confirmata cu 7 zile inainte."}),
    "en": ("TraceabilityRS - Personnel", "Field", "Description",
        {"abs":"Absence Management","msg":"Messages Management","disc":"Disciplinary Notes","osp":"Guest Management","str":"Overtime Management","prog":"External Programs"},
        {"abs":"The Absence module allows recording and managing personnel absences.","msg":"The Messages module enables sending internal communications to personnel.","disc":"The Disciplinary Notes module allows recording disciplinary measures and generating formal PDF documents.","osp":"The Guest module manages visitor registration, including hotel bookings.","str":"The Overtime module allows recording and managing overtime hours.","prog":"The External Programs module manages external training programs and certifications."},
        {"abs":["1. New Request / Register a new absence.","2. Approval / The manager verifies and approves.","3. Calendar / View the department absence calendar.","4. Reports / Generate summary reports."],
         "msg":["1. New Message / Fill in subject and text.","2. Attachments / Add file attachments.","3. Send / Send the message.","4. Archive / Browse sent and received messages."],
         "disc":["1. New Note / Create a new disciplinary note.","2. Fill In / Enter the detailed description.","3. PDF Generation / The system generates the formal document.","4. Notification / The employee is notified via email."],
         "osp":["1. Registration / Enter the guest data.","2. Bookings / Manage hotel and transfer bookings.","3. Schedule / Define the visit schedule.","4. Check-in/out / Record arrival and departure."],
         "str":["1. Request / Enter date and hours.","2. Approval / The manager approves.","3. Actual / Record actual hours worked.","4. Report / Generate the monthly report."],
         "prog":["1. New Program / Register a new program.","2. Enrollment / Enroll employees.","3. Evaluation / Record results.","4. Certification / Manage certifications."]},
        {"abs":[("Type *","Absence type"),("Start Date *","Start date"),("End Date *","End date"),("Reason","Reason"),("Status","Request status")],
         "msg":[("Subject *","Message subject"),("Text *","Message body"),("Recipients *","Recipient list"),("Priority","Priority level"),("Attachments","Attached files")],
         "disc":[("Employee *","Target employee"),("Type *","Measure type"),("Date *","Date"),("Description *","Detailed description"),("Actions","Disciplinary actions")],
         "osp":[("Name *","Guest name"),("Company *","Company"),("Visit Date *","Visit date"),("Responsible *","Internal responsible"),("Notes","Additional notes")],
         "str":[("Date *","Date"),("Planned Hours *","Number of hours"),("Reason *","Reason"),("Shift","Work shift"),("Status","Request status")],
         "prog":[("Program *","Program name"),("Type *","Type"),("Date *","Date"),("Participants","Participant list"),("Result","Program result")]},
        {"abs":"NOTE: Approved absences are automatically reported.","msg":"NOTE: High-priority messages generate immediate notification.","disc":"NOTE: Disciplinary notes are archived in the personal file.","osp":"NOTE: Guests must complete the registration form.","str":"NOTE: Overtime must be approved before work begins.","prog":"NOTE: Expiring certifications generate an automatic warning."},
        {"abs":"WARNING: Requests not approved within 48h are automatically rejected.","msg":"WARNING: Messages cannot be edited after sending.","disc":"WARNING: Notes cannot be deleted after PDF generation.","osp":"WARNING: Hotel bookings must be confirmed 24h in advance.","str":"WARNING: Exceeding the monthly limit requires management approval.","prog":"WARNING: Exam enrollment must be confirmed 7 days in advance."}),
    "de": ("TraceabilityRS - Personal", "Feld", "Beschreibung",
        {"abs":"Abwesenheitsverwaltung","msg":"Nachrichtenverwaltung","disc":"Disziplinarnotizen","osp":"Gaesteverwaltung","str":"Ueberstundenverwaltung","prog":"Externe Programme"},
        {"abs":"Das Abwesenheitsmodul ermoeglicht die Erfassung und Verwaltung von Personalabwesenheiten.","msg":"Das Nachrichtenmodul ermoeglicht das Senden interner Mitteilungen.","disc":"Das Disziplinarmodul ermoeglicht die Erfassung disziplinarischer Massnahmen und die Erstellung formeller PDF-Dokumente.","osp":"Das Gaestemodul verwaltet die Besucherregistrierung.","str":"Das Ueberstundenmodul ermoeglicht die Erfassung und Verwaltung von Ueberstunden.","prog":"Das Modul Externe Programme verwaltet externe Schulungsprogramme."},
        {"abs":["1. Neuer Antrag / Neue Abwesenheit erfassen.","2. Genehmigung / Der Vorgesetzte prueft und genehmigt.","3. Kalender / Abteilungskalender anzeigen.","4. Berichte / Zusammenfassende Berichte erstellen."],
         "msg":["1. Neue Nachricht / Betreff und Text ausfuellen.","2. Anhaenge / Dateianhaenge hinzufuegen.","3. Senden / Nachricht senden.","4. Archiv / Gesendete und empfangene Nachrichten durchsuchen."],
         "disc":["1. Neue Notiz / Neue Disziplinarnotiz erstellen.","2. Ausfuellen / Detaillierte Beschreibung eingeben.","3. PDF-Erstellung / Das System erstellt das Dokument.","4. Benachrichtigung / Der Mitarbeiter wird per E-Mail benachrichtigt."],
         "osp":["1. Registrierung / Gastedaten eingeben.","2. Buchungen / Hotel- und Transferbuchungen verwalten.","3. Programm / Besuchsprogramm definieren.","4. Check-in/out / An- und Abreise erfassen."],
         "str":["1. Antrag / Datum und Stunden eingeben.","2. Genehmigung / Der Vorgesetzte genehmigt.","3. Ist / Tatsaechliche Stunden erfassen.","4. Bericht / Monatsbericht erstellen."],
         "prog":["1. Neues Programm / Neues Programm registrieren.","2. Anmeldung / Mitarbeiter anmelden.","3. Bewertung / Ergebnisse erfassen.","4. Zertifizierung / Zertifizierungen verwalten."]},
        {"abs":[("Typ *","Abwesenheitsart"),("Startdatum *","Startdatum"),("Enddatum *","Enddatum"),("Grund","Grund"),("Status","Antragsstatus")],
         "msg":[("Betreff *","Nachrichtenbetreff"),("Text *","Nachrichtentext"),("Empfaenger *","Empfaengerliste"),("Prioritaet","Prioritaetsstufe"),("Anhaenge","Angehaengte Dateien")],
         "disc":[("Mitarbeiter *","Betroffener Mitarbeiter"),("Typ *","Art der Massnahme"),("Datum *","Datum"),("Beschreibung *","Detaillierte Beschreibung"),("Massnahmen","Disziplinarische Massnahmen")],
         "osp":[("Name *","Gastname"),("Firma *","Firma"),("Besuchsdatum *","Besuchsdatum"),("Verantwortlicher *","Interner Verantwortlicher"),("Notizen","Zusaetzliche Notizen")],
         "str":[("Datum *","Datum"),("Geplante Stunden *","Stundenanzahl"),("Grund *","Grund"),("Schicht","Arbeitsschicht"),("Status","Antragsstatus")],
         "prog":[("Programm *","Programmname"),("Typ *","Typ"),("Datum *","Datum"),("Teilnehmer","Teilnehmerliste"),("Ergebnis","Programmergebnis")]},
        {"abs":"HINWEIS: Genehmigte Abwesenheiten werden automatisch gemeldet.","msg":"HINWEIS: Nachrichten mit hoher Prioritaet erzeugen sofortige Benachrichtigung.","disc":"HINWEIS: Disziplinarnotizen werden in der Personalakte archiviert.","osp":"HINWEIS: Gaeste muessen das Registrierungsformular ausfuellen.","str":"HINWEIS: Ueberstunden muessen vor Arbeitsbeginn genehmigt werden.","prog":"HINWEIS: Ablaufende Zertifizierungen erzeugen eine automatische Warnung."},
        {"abs":"ACHTUNG: Nicht genehmigte Antraege werden nach 48h automatisch abgelehnt.","msg":"ACHTUNG: Nachrichten koennen nach dem Senden nicht bearbeitet werden.","disc":"ACHTUNG: Notizen koennen nach der PDF-Erstellung nicht geloescht werden.","osp":"ACHTUNG: Hotelbuchungen muessen 24h vorher bestaetigt werden.","str":"ACHTUNG: Ueberschreitung des Monatslimits erfordert Genehmigung der Geschaeftsfuehrung.","prog":"ACHTUNG: Pruefungsanmeldung muss 7 Tage vorher bestaetigt werden."}),
    "sv": ("TraceabilityRS - Personal", "Faelt", "Beskrivning",
        {"abs":"Franvarohantering","msg":"Meddelandehantering","disc":"Disciplinaera Anteckningar","osp":"Gaesthantering","str":"Oevertidshantering","prog":"Externa Program"},
        {"abs":"Franvaromodulen goer det moejligt att registrera och hantera personalens franvaro.","msg":"Meddelandemodulen goer det moejligt att skicka intern kommunikation.","disc":"Disciplinmodulen goer det moejligt att registrera disciplinaera oetgaerder och skapa formella PDF-dokument.","osp":"Gaestmodulen hanterar besoeksregistrering.","str":"Oevertidsmodulen goer det moejligt att registrera och hantera oevertid.","prog":"Modulen Externa Program hanterar externa utbildningsprogram."},
        {"abs":["1. Ny begoern / Registrera ny franvaro.","2. Godkaennande / Chefen granskar och godkaenner.","3. Kalender / Visa avdelningskalendern.","4. Rapporter / Generera sammanfattande rapporter."],
         "msg":["1. Nytt meddelande / Fyll i aemne och text.","2. Bilagor / Laegg till filbilagor.","3. Skicka / Skicka meddelandet.","4. Arkiv / Blaeddra bland meddelanden."],
         "disc":["1. Ny anteckning / Skapa ny disciplinaer anteckning.","2. Fyll i / Ange detaljerad beskrivning.","3. PDF-skapande / Systemet skapar dokumentet.","4. Notifiering / Medarbetaren notifieras via e-post."],
         "osp":["1. Registrering / Ange gaestdata.","2. Bokningar / Hantera hotell- och transferbokningar.","3. Schema / Definiera besoeksschemat.","4. In-/utcheckning / Registrera ankomst och avresa."],
         "str":["1. Begoern / Ange datum och timmar.","2. Godkaennande / Chefen godkaenner.","3. Faktiskt / Registrera faktiska timmar.","4. Rapport / Generera maonadsrapport."],
         "prog":["1. Nytt program / Registrera nytt program.","2. Anmaelning / Anmael medarbetare.","3. Utvaerdering / Registrera resultat.","4. Certifiering / Hantera certifieringar."]},
        {"abs":[("Typ *","Franvarotyp"),("Startdatum *","Startdatum"),("Slutdatum *","Slutdatum"),("Orsak","Orsak"),("Status","Status")],
         "msg":[("Aemne *","Aemne"),("Text *","Meddelandetext"),("Mottagare *","Mottagarlista"),("Prioritet","Prioritetsnivoe"),("Bilagor","Bifogade filer")],
         "disc":[("Medarbetare *","Beroerd medarbetare"),("Typ *","Typ av oetgaerd"),("Datum *","Datum"),("Beskrivning *","Detaljerad beskrivning"),("Oetgaerder","Disciplinaera oetgaerder")],
         "osp":[("Namn *","Gaestnamn"),("Foeretag *","Foeretag"),("Besoeksdatum *","Besoeksdatum"),("Ansvarig *","Intern ansvarig"),("Anteckningar","Ytterligare anteckningar")],
         "str":[("Datum *","Datum"),("Planerade timmar *","Antal timmar"),("Orsak *","Orsak"),("Skift","Arbetsskift"),("Status","Status")],
         "prog":[("Program *","Programnamn"),("Typ *","Typ"),("Datum *","Datum"),("Deltagare","Deltagarlista"),("Resultat","Programresultat")]},
        {"abs":"NOTERA: Godkaenda franvaron rapporteras automatiskt.","msg":"NOTERA: Meddelanden med hoeg prioritet genererar omedelbar notifiering.","disc":"NOTERA: Disciplinaera anteckningar arkiveras i personalakten.","osp":"NOTERA: Gaester moeste fylla i registreringsformulaeret.","str":"NOTERA: Oevertid moeste godkaennas foere arbetets boerjan.","prog":"NOTERA: Utgoeende certifieringar genererar en automatisk varning."},
        {"abs":"VARNING: Begoeranden som inte godkaenns inom 48h avsloes automatiskt.","msg":"VARNING: Meddelanden kan inte redigeras efter saendning.","disc":"VARNING: Anteckningar kan inte raderas efter PDF-skapande.","osp":"VARNING: Hotellbokningar moeste bekraeftas 24 timmar i forvaeg.","str":"VARNING: Oeverskridande av maonadsgraensen kraever ledningens godkaennande.","prog":"VARNING: Examenanmaelning moeste bekraeftas 7 dagar i forvaeg."}),
}.items():
    T = {"app":"TraceabilityRS","ver":"Versione 2.3.6" if lang=="it" else ("Versiunea 2.3.6" if lang=="ro" else "Version 2.3.6"),
         "footer":footer,"field":field_l,"description":desc_l}
    for key in ("abs","msg","disc","osp","str","prog"):
        T[f"{key}_title"] = titles[key]
        T[f"{key}_subtitle"] = titles[key]
        T[f"{key}_desc"] = descs[key]
        T[f"{key}_steps"] = steps[key]
        T[f"{key}_fields"] = fields[key]
        T[f"{key}_note"] = notes[key]
        T[f"{key}_warn"] = warns[key]
    TEXTS[lang] = T


def _cover(story, T):
    story.append(sp(20))
    if os.path.exists(LOGO_PATH):
        story.append(Image(LOGO_PATH, width=50*mm, height=50*mm)); story.append(sp(6))
    story.append(Paragraph(T["app"], title_style))
    story.append(Paragraph(T["ver"], sub_style))


def build_manual(lang, T, section_key, prefix):
    out = os.path.join(BASE_DIR, lang, f"{section_key}.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4, topMargin=18*mm, bottomMargin=20*mm, leftMargin=15*mm, rightMargin=15*mm)
    W = A4[0] - 30*mm
    story = []
    _cover(story, T)
    story.append(Paragraph(T[f"{prefix}_title"], title_style))
    story.append(Paragraph(T[f"{prefix}_subtitle"], sub_style))
    story.append(hr())
    story.append(Paragraph(T[f"{prefix}_desc"], body))
    story.append(sp(4))
    story.append(Paragraph(T[f"{prefix}_title"], h1))
    for step_text in T[f"{prefix}_steps"]:
        parts = step_text.split(" / ", 1)
        story.append(Paragraph(parts[0], h2))
        if len(parts) > 1:
            story.append(Paragraph(parts[1], body))
    story.append(hr())
    story.append(Paragraph(T["field"], h1))
    rows = []
    for fname, fdesc in T[f"{prefix}_fields"]:
        rows.append([Paragraph(fname, body), Paragraph(fdesc, body)])
    story.append(make_table([Paragraph(T["field"], body), Paragraph(T["description"], body)], rows, W))
    story.append(sp(4))
    story.append(Paragraph(T[f"{prefix}_note"], note_s))
    story.append(Paragraph(T[f"{prefix}_warn"], warn_s))
    doc.build(story, onFirstPage=lambda c,d: on_page(c,d,T["footer"]), onLaterPages=lambda c,d: on_page(c,d,T["footer"]))
    print(f"  -> {out}")


if __name__ == "__main__":
    for lang in ("it","ro","en","de","sv"):
        os.makedirs(os.path.join(BASE_DIR, lang), exist_ok=True)
        T = TEXTS[lang]
        print(f"[{lang}]")
        for section_key, prefix in MANUALS:
            build_manual(lang, T, section_key, prefix)
    print(f"\nDone! {len(MANUALS)*5} PDF generati.")
