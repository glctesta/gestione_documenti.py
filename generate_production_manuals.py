# -*- coding: utf-8 -*-
"""
Genera i manuali PDF per la sezione 'Produzione' in 5 lingue.
Produce: manuals/{lang}/produzione_calibrazioni.pdf
         manuals/{lang}/produzione_coating.pdf
         manuals/{lang}/produzione_kanban.pdf
         manuals/{lang}/produzione_paste.pdf
         manuals/{lang}/produzione_rapporti.pdf
         manuals/{lang}/produzione_tracciabilita.pdf
         manuals/{lang}/produzione_verifiche.pdf
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

MANUALS = [
    ("produzione_calibrazioni", "cal"),
    ("produzione_coating", "coat"),
    ("produzione_kanban", "kan"),
    ("produzione_paste", "paste"),
    ("produzione_rapporti", "rap"),
    ("produzione_tracciabilita", "trace"),
    ("produzione_verifiche", "ver"),
]

TEXTS = {}
for lang, (footer, field_l, desc_l, titles, subtitles, descs, steps, fields, notes, warns) in {
    "it": ("TraceabilityRS - Produzione", "Campo", "Descrizione",
        {"cal":"Calibrazioni","coat":"Coating","kan":"KanBan","paste":"Gestione Paste","rap":"Rapporti di Produzione","trace":"Tracciabilita'","ver":"Verifiche Prodotti"},
        {"cal":"Gestione calibrazioni strumenti","coat":"Gestione processi di coating","kan":"Gestione schede KanBan","paste":"Gestione delle paste di saldatura","rap":"Report e statistiche di produzione","trace":"Tracciabilita' dei prodotti","ver":"Verifiche e controlli sui prodotti"},
        {"cal":"Il modulo Calibrazioni permette di gestire le calibrazioni periodiche degli strumenti di misura. Ogni strumento ha un piano di calibrazione con scadenze automatiche e notifiche.",
         "coat":"Il modulo Coating gestisce i processi di rivestimento (coating) dei prodotti. Consente di tracciare i lotti, i parametri di processo e i risultati dei controlli qualita'.",
         "kan":"Il modulo KanBan implementa un sistema di gestione visuale della produzione basato su schede KanBan. Permette di monitorare il flusso dei materiali e lo stato di avanzamento.",
         "paste":"Il modulo Paste permette di gestire le paste per saldatura (solder paste), tracciando lotti, date di scadenza, temperature di stoccaggio e utilizzo in produzione.",
         "rap":"Il modulo Rapporti genera report e statistiche sulla produzione. Permette di analizzare rendimenti, scarti, tempi di produzione e trend nel tempo.",
         "trace":"Il modulo Tracciabilita' consente di tracciare ogni prodotto dal ricevimento delle materie prime alla spedizione del prodotto finito, con registrazione completa di ogni fase.",
         "ver":"Il modulo Verifiche Prodotti gestisce i controlli qualita' sui prodotti in diverse fasi della produzione. Definisce i piani di controllo e registra i risultati."},
        {"cal":["1. Elenco Strumenti / Visualizzare la lista degli strumenti con stato calibrazione.","2. Nuova Calibrazione / Registrare una nuova calibrazione per uno strumento.","3. Certificati / Allegare il certificato di calibrazione.","4. Scadenze / Il sistema avvisa automaticamente delle calibrazioni in scadenza."],
         "coat":["1. Nuovo Lotto / Creare un nuovo lotto di coating associandolo al prodotto.","2. Parametri / Registrare i parametri di processo (temperatura, tempo, spessore).","3. Controllo / Eseguire e registrare i controlli qualita' sul rivestimento.","4. Report / Generare report sui lotti processati."],
         "kan":["1. Schede KanBan / Visualizzare la lavagna KanBan con le schede attive.","2. Nuova Scheda / Creare una nuova scheda KanBan per un ordine.","3. Movimentazione / Spostare le schede tra le colonne (Da Fare, In Corso, Completato).","4. Storico / Consultare lo storico delle schede completate."],
         "paste":["1. Gestione Lotti / Registrare nuovi lotti di pasta con data scadenza e lotto fornitore.","2. Stoccaggio / Monitorare le temperature di stoccaggio.","3. Utilizzo / Registrare il prelievo e l'utilizzo in produzione.","4. Scadenze / Il sistema segnala le paste in scadenza o scadute."],
         "rap":["1. Selezione Periodo / Selezionare il periodo di analisi.","2. Tipo Report / Scegliere il tipo di report (rendimento, scarti, tempi).","3. Filtri / Applicare filtri per prodotto, linea o turno.","4. Esportazione / Esportare il report in Excel o PDF."],
         "trace":["1. Ricerca / Cercare un prodotto per numero di serie o lotto.","2. Albero Genealogico / Visualizzare la genealogia completa del prodotto.","3. Fasi / Consultare i dettagli di ogni fase di produzione.","4. Report / Generare il report di tracciabilita' completo."],
         "ver":["1. Piano di Controllo / Definire i punti di controllo per ogni prodotto.","2. Esecuzione / Eseguire le verifiche registrandone i risultati.","3. Non Conformita' / Gestire le non conformita' riscontrate.","4. Statistiche / Analizzare le statistiche dei controlli."]},
        {"cal":[("Codice Strumento *","Codice univoco dello strumento"),("Tipo *","Tipologia dello strumento"),("Ultima Calibrazione","Data dell'ultima calibrazione"),("Prossima Scadenza","Data della prossima calibrazione"),("Stato","Stato della calibrazione (Valida, In Scadenza, Scaduta)")],
         "coat":[("Lotto *","Codice del lotto di coating"),("Prodotto *","Prodotto da rivestire"),("Temperatura *","Temperatura di processo"),("Tempo *","Durata del processo"),("Spessore","Spessore del rivestimento")],
         "kan":[("Codice Scheda *","Codice della scheda KanBan"),("Ordine *","Ordine di produzione associato"),("Prodotto *","Prodotto da produrre"),("Quantita' *","Quantita' da produrre"),("Stato","Stato della scheda")],
         "paste":[("Lotto Pasta *","Codice del lotto di pasta"),("Fornitore *","Fornitore della pasta"),("Data Scadenza *","Data di scadenza"),("Temperatura","Temperatura di stoccaggio attuale"),("Stato","Stato (Disponibile, In Uso, Scaduta)")],
         "rap":[("Periodo *","Periodo di analisi"),("Tipo Report *","Tipologia del report"),("Prodotto","Filtro per prodotto"),("Linea","Filtro per linea di produzione"),("Formato","Formato di esportazione")],
         "trace":[("Seriale / Lotto *","Numero di serie o lotto del prodotto"),("Prodotto *","Tipologia di prodotto"),("Fase","Fase di produzione specifica"),("Data","Data della registrazione"),("Operatore","Operatore che ha eseguito la fase")],
         "ver":[("Prodotto *","Prodotto da verificare"),("Punto di Controllo *","Punto di controllo specifico"),("Risultato *","Risultato della verifica (OK/NOK)"),("Misura","Valore misurato"),("Note","Note aggiuntive")]},
        {"cal":"NOTA: Le calibrazioni scadute impediscono l'utilizzo dello strumento fino al rinnovo.","coat":"NOTA: I parametri di processo devono rispettare le specifiche del prodotto.","kan":"NOTA: Le schede KanBan completate vengono archiviate automaticamente dopo 30 giorni.","paste":"NOTA: Le paste scadute devono essere smaltite secondo le procedure ambientali.","rap":"NOTA: I report possono essere programmati per l'invio automatico via email.","trace":"NOTA: La tracciabilita' completa e' obbligatoria per i prodotti automotive.","ver":"NOTA: Le non conformita' critiche bloccano automaticamente la produzione."},
        {"cal":"ATTENZIONE: Utilizzare uno strumento con calibrazione scaduta puo' invalidare la produzione.","coat":"ATTENZIONE: Parametri fuori specifica richiedono lo scarto del lotto.","kan":"ATTENZIONE: Le schede in ritardo vengono evidenziate in rosso.","paste":"ATTENZIONE: L'utilizzo di paste scadute e' severamente vietato.","rap":"ATTENZIONE: I dati dei report sono aggregati e non modificabili.","trace":"ATTENZIONE: Lacune nella tracciabilita' possono causare il richiamo del prodotto.","ver":"ATTENZIONE: I prodotti NOK devono essere segregati immediatamente."}),
    "ro": ("TraceabilityRS - Productie", "Camp", "Descriere",
        {"cal":"Calibrari","coat":"Coating","kan":"KanBan","paste":"Gestionare Paste","rap":"Rapoarte de Productie","trace":"Trasabilitate","ver":"Verificari Produse"},
        {"cal":"Gestionarea calibrarilor instrumentelor","coat":"Gestionarea proceselor de coating","kan":"Gestionarea fiselor KanBan","paste":"Gestionarea pastelor de lipit","rap":"Rapoarte si statistici de productie","trace":"Trasabilitatea produselor","ver":"Verificari si controale ale produselor"},
        {"cal":"Modulul Calibrari permite gestionarea calibrarilor periodice ale instrumentelor de masura.","coat":"Modulul Coating gestioneaza procesele de acoperire a produselor.","kan":"Modulul KanBan implementeaza un sistem vizual de gestionare a productiei.","paste":"Modulul Paste permite gestionarea pastelor de lipit.","rap":"Modulul Rapoarte genereaza rapoarte si statistici despre productie.","trace":"Modulul Trasabilitate permite urmarirea fiecarui produs.","ver":"Modulul Verificari gestioneaza controalele de calitate."},
        {"cal":["1. Lista Instrumente / Vizualizati lista instrumentelor.","2. Calibrare Noua / Inregistrati o calibrare noua.","3. Certificate / Atasati certificatul.","4. Expirari / Sistemul avertizeaza automat."],
         "coat":["1. Lot Nou / Creati un lot nou de coating.","2. Parametri / Inregistrati parametrii procesului.","3. Control / Efectuati controalele de calitate.","4. Raport / Generati rapoarte."],
         "kan":["1. Fise KanBan / Vizualizati tabla KanBan.","2. Fisa Noua / Creati o fisa noua.","3. Mutare / Mutati fisele intre coloane.","4. Istoric / Consultati istoricul."],
         "paste":["1. Gestionare Loturi / Inregistrati loturi noi.","2. Depozitare / Monitorizati temperaturile.","3. Utilizare / Inregistrati preluarea.","4. Expirari / Sistemul semnaleaza pastele expirate."],
         "rap":["1. Selectare Perioada / Selectati perioada.","2. Tip Raport / Alegeti tipul.","3. Filtre / Aplicati filtre.","4. Export / Exportati raportul."],
         "trace":["1. Cautare / Cautati un produs.","2. Arbore Genealogic / Vizualizati genealogia.","3. Faze / Consultati detaliile.","4. Raport / Generati raportul complet."],
         "ver":["1. Plan de Control / Definiti punctele de control.","2. Executare / Efectuati verificarile.","3. Neconformitati / Gestionati neconformitatile.","4. Statistici / Analizati statisticile."]},
        {"cal":[("Cod Instrument *","Codul unic"),("Tip *","Tipul instrumentului"),("Ultima Calibrare","Data ultimei calibrari"),("Urmatoarea Expirare","Data urmatoarei calibrari"),("Stare","Starea calibrarii")],
         "coat":[("Lot *","Codul lotului"),("Produs *","Produsul"),("Temperatura *","Temperatura"),("Timp *","Durata"),("Grosime","Grosimea")],
         "kan":[("Cod Fisa *","Codul fisei"),("Comanda *","Comanda asociata"),("Produs *","Produsul"),("Cantitate *","Cantitatea"),("Stare","Starea fisei")],
         "paste":[("Lot Pasta *","Codul lotului"),("Furnizor *","Furnizorul"),("Data Expirare *","Data expirarii"),("Temperatura","Temperatura actuala"),("Stare","Starea")],
         "rap":[("Perioada *","Perioada de analiza"),("Tip Raport *","Tipul raportului"),("Produs","Filtru produs"),("Linie","Filtru linie"),("Format","Formatul de export")],
         "trace":[("Serie / Lot *","Numarul de serie sau lot"),("Produs *","Tipul produsului"),("Faza","Faza de productie"),("Data","Data inregistrarii"),("Operator","Operatorul")],
         "ver":[("Produs *","Produsul de verificat"),("Punct Control *","Punctul de control"),("Rezultat *","Rezultatul (OK/NOK)"),("Masura","Valoarea masurata"),("Note","Note suplimentare")]},
        {"cal":"NOTA: Calibrarile expirate impiedica utilizarea instrumentului.","coat":"NOTA: Parametrii trebuie sa respecte specificatiile.","kan":"NOTA: Fisele completate sunt arhivate automat.","paste":"NOTA: Pastele expirate trebuie eliminate.","rap":"NOTA: Rapoartele pot fi programate automat.","trace":"NOTA: Trasabilitatea completa este obligatorie.","ver":"NOTA: Neconformitatile critice blocheaza productia."},
        {"cal":"ATENTIE: Utilizarea unui instrument expirat poate invalida productia.","coat":"ATENTIE: Parametrii in afara specificatiilor necesita refacerea lotului.","kan":"ATENTIE: Fisele intarziate sunt evidentiate in rosu.","paste":"ATENTIE: Utilizarea pastelor expirate este strict interzisa.","rap":"ATENTIE: Datele rapoartelor sunt agregate si nemodificabile.","trace":"ATENTIE: Lacunele in trasabilitate pot cauza retragerea produsului.","ver":"ATENTIE: Produsele NOK trebuie segregate imediat."}),
    "en": ("TraceabilityRS - Production", "Field", "Description",
        {"cal":"Calibrations","coat":"Coating","kan":"KanBan","paste":"Paste Management","rap":"Production Reports","trace":"Traceability","ver":"Product Checks"},
        {"cal":"Instrument calibration management","coat":"Coating process management","kan":"KanBan card management","paste":"Solder paste management","rap":"Production reports and statistics","trace":"Product traceability","ver":"Product checks and controls"},
        {"cal":"The Calibrations module manages periodic calibrations of measuring instruments.","coat":"The Coating module manages product coating processes.","kan":"The KanBan module implements a visual production management system.","paste":"The Paste module manages solder pastes, tracking lots and expiry dates.","rap":"The Reports module generates production reports and statistics.","trace":"The Traceability module enables tracking every product from raw materials to shipment.","ver":"The Product Checks module manages quality controls at various production stages."},
        {"cal":["1. Instrument List / View instruments with calibration status.","2. New Calibration / Register a new calibration.","3. Certificates / Attach the calibration certificate.","4. Expirations / The system automatically warns of upcoming expirations."],
         "coat":["1. New Lot / Create a new coating lot.","2. Parameters / Record process parameters.","3. Control / Perform quality checks.","4. Report / Generate reports."],
         "kan":["1. KanBan Cards / View the KanBan board.","2. New Card / Create a new KanBan card.","3. Move / Move cards between columns.","4. History / Browse completed cards."],
         "paste":["1. Lot Management / Register new paste lots.","2. Storage / Monitor storage temperatures.","3. Usage / Record usage in production.","4. Expirations / The system flags expired pastes."],
         "rap":["1. Select Period / Choose the analysis period.","2. Report Type / Select the report type.","3. Filters / Apply filters.","4. Export / Export the report."],
         "trace":["1. Search / Search by serial number or lot.","2. Genealogy Tree / View complete product genealogy.","3. Phases / Browse phase details.","4. Report / Generate the complete report."],
         "ver":["1. Control Plan / Define control points.","2. Execution / Perform checks and record results.","3. Non-Conformities / Manage non-conformities.","4. Statistics / Analyze check statistics."]},
        {"cal":[("Instrument Code *","Unique code"),("Type *","Instrument type"),("Last Calibration","Last date"),("Next Expiry","Next calibration date"),("Status","Calibration status")],
         "coat":[("Lot *","Lot code"),("Product *","Product"),("Temperature *","Process temperature"),("Time *","Process duration"),("Thickness","Coating thickness")],
         "kan":[("Card Code *","Card code"),("Order *","Associated order"),("Product *","Product"),("Quantity *","Quantity"),("Status","Card status")],
         "paste":[("Paste Lot *","Lot code"),("Supplier *","Supplier"),("Expiry Date *","Expiry date"),("Temperature","Current storage temp"),("Status","Status")],
         "rap":[("Period *","Analysis period"),("Report Type *","Report type"),("Product","Product filter"),("Line","Line filter"),("Format","Export format")],
         "trace":[("Serial / Lot *","Serial number or lot"),("Product *","Product type"),("Phase","Production phase"),("Date","Registration date"),("Operator","Operator")],
         "ver":[("Product *","Product to check"),("Control Point *","Specific control point"),("Result *","Result (OK/NOK)"),("Measure","Measured value"),("Notes","Additional notes")]},
        {"cal":"NOTE: Expired calibrations prevent instrument use.","coat":"NOTE: Process parameters must meet product specifications.","kan":"NOTE: Completed cards are automatically archived after 30 days.","paste":"NOTE: Expired pastes must be disposed of properly.","rap":"NOTE: Reports can be scheduled for automatic email.","trace":"NOTE: Complete traceability is mandatory for automotive products.","ver":"NOTE: Critical non-conformities automatically halt production."},
        {"cal":"WARNING: Using an expired instrument may invalidate production.","coat":"WARNING: Out-of-spec parameters require lot rejection.","kan":"WARNING: Delayed cards are highlighted in red.","paste":"WARNING: Use of expired pastes is strictly prohibited.","rap":"WARNING: Report data is aggregated and non-editable.","trace":"WARNING: Traceability gaps may cause product recall.","ver":"WARNING: NOK products must be segregated immediately."}),
    "de": ("TraceabilityRS - Produktion", "Feld", "Beschreibung",
        {"cal":"Kalibrierungen","coat":"Beschichtung","kan":"KanBan","paste":"Pastenverwaltung","rap":"Produktionsberichte","trace":"Rueckverfolgbarkeit","ver":"Produktpruefungen"},
        {"cal":"Verwaltung von Instrumentenkalibrierungen","coat":"Verwaltung von Beschichtungsprozessen","kan":"KanBan-Kartenverwaltung","paste":"Verwaltung von Loetpasten","rap":"Produktionsberichte und Statistiken","trace":"Produktrueckverfolgbarkeit","ver":"Produktpruefungen und Kontrollen"},
        {"cal":"Das Kalibrierungsmodul verwaltet periodische Kalibrierungen von Messinstrumenten.","coat":"Das Beschichtungsmodul verwaltet Beschichtungsprozesse.","kan":"Das KanBan-Modul implementiert ein visuelles Produktionsmanagementsystem.","paste":"Das Pastenmodul verwaltet Loetpasten mit Verfallsdaten.","rap":"Das Berichtsmodul erstellt Produktionsberichte und Statistiken.","trace":"Das Rueckverfolgbarkeitsmodul ermoeglicht die Verfolgung jedes Produkts.","ver":"Das Pruefungsmodul verwaltet Qualitaetskontrollen."},
        {"cal":["1. Instrumentenliste / Instrumente mit Kalibrierungsstatus anzeigen.","2. Neue Kalibrierung / Neue Kalibrierung registrieren.","3. Zertifikate / Kalibrierungszertifikat anhaengen.","4. Ablauf / Automatische Ablaufwarnungen."],
         "coat":["1. Neues Los / Neues Beschichtungslos erstellen.","2. Parameter / Prozessparameter erfassen.","3. Kontrolle / Qualitaetskontrolle durchfuehren.","4. Bericht / Berichte erstellen."],
         "kan":["1. KanBan-Karten / KanBan-Tafel anzeigen.","2. Neue Karte / Neue KanBan-Karte erstellen.","3. Verschieben / Karten zwischen Spalten verschieben.","4. Historie / Abgeschlossene Karten durchsuchen."],
         "paste":["1. Losverwaltung / Neue Pastenlose registrieren.","2. Lagerung / Lagertemperaturen ueberwachen.","3. Verwendung / Verwendung in der Produktion erfassen.","4. Ablauf / Abgelaufene Pasten werden markiert."],
         "rap":["1. Zeitraum waehlen / Analysezeitraum waehlen.","2. Berichtstyp / Berichtstyp auswaehlen.","3. Filter / Filter anwenden.","4. Export / Bericht exportieren."],
         "trace":["1. Suche / Nach Seriennummer oder Los suchen.","2. Stammbaum / Vollstaendige Produktgenealogie anzeigen.","3. Phasen / Phasendetails durchsuchen.","4. Bericht / Vollstaendigen Bericht erstellen."],
         "ver":["1. Kontrollplan / Kontrollpunkte definieren.","2. Durchfuehrung / Pruefungen durchfuehren.","3. Abweichungen / Abweichungen verwalten.","4. Statistiken / Pruefstatistiken analysieren."]},
        {"cal":[("Instrumentencode *","Eindeutiger Code"),("Typ *","Instrumententyp"),("Letzte Kalibrierung","Letztes Datum"),("Naechster Ablauf","Naechstes Kalibrierungsdatum"),("Status","Kalibrierungsstatus")],
         "coat":[("Los *","Loscode"),("Produkt *","Produkt"),("Temperatur *","Prozesstemperatur"),("Zeit *","Prozessdauer"),("Dicke","Beschichtungsdicke")],
         "kan":[("Kartencode *","Kartencode"),("Auftrag *","Zugeordneter Auftrag"),("Produkt *","Produkt"),("Menge *","Menge"),("Status","Kartenstatus")],
         "paste":[("Pastenlos *","Loscode"),("Lieferant *","Lieferant"),("Ablaufdatum *","Ablaufdatum"),("Temperatur","Aktuelle Lagertemperatur"),("Status","Status")],
         "rap":[("Zeitraum *","Analysezeitraum"),("Berichtstyp *","Berichtstyp"),("Produkt","Produktfilter"),("Linie","Linienfilter"),("Format","Exportformat")],
         "trace":[("Serie / Los *","Seriennummer oder Los"),("Produkt *","Produkttyp"),("Phase","Produktionsphase"),("Datum","Registrierungsdatum"),("Bediener","Bediener")],
         "ver":[("Produkt *","Zu pruefendes Produkt"),("Kontrollpunkt *","Spezifischer Kontrollpunkt"),("Ergebnis *","Ergebnis (OK/NOK)"),("Messwert","Gemessener Wert"),("Notizen","Zusaetzliche Notizen")]},
        {"cal":"HINWEIS: Abgelaufene Kalibrierungen verhindern die Instrumentennutzung.","coat":"HINWEIS: Prozessparameter muessen die Spezifikationen erfuellen.","kan":"HINWEIS: Abgeschlossene Karten werden nach 30 Tagen automatisch archiviert.","paste":"HINWEIS: Abgelaufene Pasten muessen ordnungsgemaess entsorgt werden.","rap":"HINWEIS: Berichte koennen fuer automatischen E-Mail-Versand geplant werden.","trace":"HINWEIS: Vollstaendige Rueckverfolgbarkeit ist fuer Automobilprodukte obligatorisch.","ver":"HINWEIS: Kritische Abweichungen stoppen die Produktion automatisch."},
        {"cal":"ACHTUNG: Die Verwendung abgelaufener Instrumente kann die Produktion ungueltig machen.","coat":"ACHTUNG: Parameter ausserhalb der Spezifikation erfordern Losabweisung.","kan":"ACHTUNG: Verspaetete Karten werden rot hervorgehoben.","paste":"ACHTUNG: Die Verwendung abgelaufener Pasten ist streng verboten.","rap":"ACHTUNG: Berichtsdaten sind aggregiert und nicht bearbeitbar.","trace":"ACHTUNG: Luecken in der Rueckverfolgbarkeit koennen Produktrueckrufe verursachen.","ver":"ACHTUNG: NOK-Produkte muessen sofort separiert werden."}),
    "sv": ("TraceabilityRS - Produktion", "Faelt", "Beskrivning",
        {"cal":"Kalibreringar","coat":"Belaggning","kan":"KanBan","paste":"Pastahantering","rap":"Produktionsrapporter","trace":"Spoerbarhet","ver":"Produktkontroller"},
        {"cal":"Hantering av instrumentkalibreringar","coat":"Hantering av belaggningsprocesser","kan":"Hantering av KanBan-kort","paste":"Hantering av loedpasta","rap":"Produktionsrapporter och statistik","trace":"Produktspoerbarhet","ver":"Produktkontroller och inspektioner"},
        {"cal":"Kalibreringsmodulen hanterar periodiska kalibreringar av maetinstrument.","coat":"Belaggningsmodulen hanterar produkters belaggningsprocesser.","kan":"KanBan-modulen implementerar ett visuellt produktionshanteringssystem.","paste":"Pastamodulen hanterar loedpasta med utgongsdatum.","rap":"Rapportmodulen genererar produktionsrapporter och statistik.","trace":"Spoerbarhetmodulen goer det moejligt att spoera varje produkt.","ver":"Kontrollmodulen hanterar kvalitetskontroller."},
        {"cal":["1. Instrumentlista / Visa instrument med kalibreringsstatus.","2. Ny kalibrering / Registrera en ny kalibrering.","3. Certifikat / Bifoga kalibreringscertifikatet.","4. Utgong / Automatiska varningar."],
         "coat":["1. Nytt parti / Skapa nytt belaggningsparti.","2. Parametrar / Registrera processparametrar.","3. Kontroll / Utfoer kvalitetskontroll.","4. Rapport / Generera rapporter."],
         "kan":["1. KanBan-kort / Visa KanBan-tavlan.","2. Nytt kort / Skapa nytt kort.","3. Flytta / Flytta kort mellan kolumner.","4. Historik / Blaeddra bland slutfoerda kort."],
         "paste":["1. Partihantering / Registrera nya pastapartier.","2. Lagring / Oevervaka lagringstemperaturer.","3. Anvaendning / Registrera anvaendning i produktion.","4. Utgong / Systemet flaggar utgongna pastor."],
         "rap":["1. Vaelj period / Vaelj analysperiod.","2. Rapporttyp / Vaelj rapporttyp.","3. Filter / Tillaemp filter.","4. Export / Exportera rapporten."],
         "trace":["1. Soek / Soek efter serienummer eller parti.","2. Genealogi / Visa komplett produktgenealogin.","3. Faser / Blaeddra fasdetaljer.","4. Rapport / Generera komplett rapport."],
         "ver":["1. Kontrollplan / Definiera kontrollpunkter.","2. Genomfoerande / Utfoer kontroller.","3. Avvikelser / Hantera avvikelser.","4. Statistik / Analysera kontrollstatistik."]},
        {"cal":[("Instrumentkod *","Unik kod"),("Typ *","Instrumenttyp"),("Senaste kalibrering","Senaste datum"),("Naesta utgong","Naesta kalibreringsdatum"),("Status","Kalibreringsstatus")],
         "coat":[("Parti *","Partikod"),("Produkt *","Produkt"),("Temperatur *","Processtemperatur"),("Tid *","Processtid"),("Tjocklek","Belaggningstjocklek")],
         "kan":[("Kortkod *","Kortkod"),("Order *","Tillhoerande order"),("Produkt *","Produkt"),("Kvantitet *","Kvantitet"),("Status","Kortstatus")],
         "paste":[("Pastaparti *","Partikod"),("Leverantoer *","Leverantoer"),("Utgongsdatum *","Utgongsdatum"),("Temperatur","Aktuell lagringstemperatur"),("Status","Status")],
         "rap":[("Period *","Analysperiod"),("Rapporttyp *","Rapporttyp"),("Produkt","Produktfilter"),("Linje","Linjefilter"),("Format","Exportformat")],
         "trace":[("Serie / Parti *","Serienummer eller parti"),("Produkt *","Produkttyp"),("Fas","Produktionsfas"),("Datum","Registreringsdatum"),("Operatoer","Operatoer")],
         "ver":[("Produkt *","Produkt att kontrollera"),("Kontrollpunkt *","Specifik kontrollpunkt"),("Resultat *","Resultat (OK/NOK)"),("Maetvaerde","Uppmatt vaerde"),("Anteckningar","Ytterligare anteckningar")]},
        {"cal":"NOTERA: Utgongna kalibreringar foerhindrar instrumentanvaendning.","coat":"NOTERA: Processparametrar moeste uppfylla specifikationerna.","kan":"NOTERA: Slutfoerda kort arkiveras automatiskt efter 30 dagar.","paste":"NOTERA: Utgongna pastor moeste kasseras korrekt.","rap":"NOTERA: Rapporter kan schemalaegas foer automatisk e-post.","trace":"NOTERA: Fullstaendig spoerbarhet aer obligatorisk foer fordonsprodukter.","ver":"NOTERA: Kritiska avvikelser stoppar produktionen automatiskt."},
        {"cal":"VARNING: Anvaendning av utgonget instrument kan ogiltigfoerklara produktion.","coat":"VARNING: Parametrar utanfoer specifikation kraever partikassering.","kan":"VARNING: Foersenade kort markeras i roett.","paste":"VARNING: Anvaendning av utgongna pastor aer straengt foerbjudet.","rap":"VARNING: Rapportdata aer aggregerad och ej redigerbar.","trace":"VARNING: Luckor i spoerbarhet kan orsaka produktoeterkallelese.","ver":"VARNING: NOK-produkter moeste separeras omedelbart."}),
}.items():
    T = {"app":"TraceabilityRS","ver":"Versione 2.3.6" if lang=="it" else ("Versiunea 2.3.6" if lang=="ro" else "Version 2.3.6"),
         "footer":footer,"field":field_l,"description":desc_l}
    for key in ("cal","coat","kan","paste","rap","trace","ver"):
        T[f"{key}_title"] = titles[key]
        T[f"{key}_subtitle"] = subtitles[key]
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
