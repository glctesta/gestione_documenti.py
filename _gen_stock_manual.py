# -*- coding: utf-8 -*-
"""Genera docs/Manual_Gestione_Giacenze.html: manuale self-contained multilingua
(it/en/ro/de/sv) per le funzionalita' Giacenze / Riordino / Consumi & Budget
dei Materiali Indiretti.
Esegui: python _gen_stock_manual.py
"""
import os

LANGS = [('it', 'Italiano'), ('en', 'English'), ('ro', 'Română'),
         ('de', 'Deutsch'), ('sv', 'Svenska')]

# Titoli pagina / intestazione
PAGE_TITLE = {
    'it': 'Manuale - Gestione Giacenze Materiali Indiretti',
    'en': 'Manual - Indirect Materials Stock Management',
    'ro': 'Manual - Gestionare Stoc Materiale Indirecte',
    'de': 'Handbuch - Bestandsverwaltung Indirektes Material',
    'sv': 'Handbok - Lagerhantering indirekta material',
}

# Sezioni: lista di (id, {lang: (titolo, html_body)})
SECTIONS = [
    ('intro', {
        'it': ("Introduzione",
               "Questo modulo gestisce le <b>giacenze</b> dei materiali indiretti tramite un "
               "<b>libro movimenti</b> (ogni carico e scarico è una riga tracciata). La giacenza "
               "corrente è la somma dei movimenti. Da qui si controllano le scorte, si impostano i "
               "livelli minimi con riordino automatico verso gli acquisti, e si analizzano i consumi "
               "con proposta di budget."),
        'en': ("Introduction",
               "This module manages indirect materials <b>stock</b> through a <b>movements ledger</b> "
               "(each load and pick is a tracked row). Current stock is the sum of movements. From here "
               "you check stock, set minimum levels with automatic reorder to purchasing, and analyse "
               "consumption with a budget proposal."),
        'ro': ("Introducere",
               "Acest modul gestionează <b>stocul</b> materialelor indirecte printr-un <b>registru de "
               "mişcări</b> (fiecare intrare şi ieşire este o linie urmărită). Stocul curent este suma "
               "mişcărilor. De aici verificaţi stocul, setaţi nivelurile minime cu recomandă automată "
               "către achiziţii şi analizaţi consumurile cu propunere de buget."),
        'de': ("Einführung",
               "Dieses Modul verwaltet den <b>Bestand</b> an indirektem Material über ein "
               "<b>Bewegungsbuch</b> (jeder Zu- und Abgang ist eine erfasste Zeile). Der aktuelle "
               "Bestand ist die Summe der Bewegungen. Hier prüfen Sie den Bestand, legen Mindestmengen "
               "mit automatischer Nachbestellung an den Einkauf fest und analysieren den Verbrauch mit "
               "Budgetvorschlag."),
        'sv': ("Introduktion",
               "Den här modulen hanterar lager för indirekta material via en <b>rörelsebok</b> (varje "
               "inleverans och uttag är en spårad rad). Aktuellt lager är summan av rörelserna. Här "
               "kontrollerar du lager, ställer in miniminivåer med automatisk beställning till inköp och "
               "analyserar förbrukning med budgetförslag."),
    }),
    ('verifica', {
        'it': ("Verifica Giacenze",
               "Menu <i>Materiali Indiretti → Verifica Giacenze</i>. Mostra la giacenza corrente di ogni "
               "codice, la scorta minima e lo stato. Le righe <b>sotto scorta minima</b> sono evidenziate "
               "in rosso. Selezionando un codice si vedono gli ultimi movimenti. Pulsanti: "
               "<b>Aggiorna</b>, <b>Esporta Excel</b>, <b>Invia riordino ora</b> (invio manuale)."),
        'en': ("Stock Check",
               "Menu <i>Indirect Materials → Check Stock</i>. Shows current stock per code, minimum stock "
               "and status. Rows <b>below minimum</b> are highlighted in red. Selecting a code shows its "
               "latest movements. Buttons: <b>Refresh</b>, <b>Export Excel</b>, <b>Send reorder now</b> "
               "(manual send)."),
        'ro': ("Verificare Stoc",
               "Meniu <i>Materiale Indirecte → Verificare Stocuri</i>. Afişează stocul curent per cod, "
               "stocul minim şi starea. Liniile <b>sub stoc minim</b> sunt evidenţiate cu roşu. Selectând "
               "un cod vedeţi ultimele mişcări. Butoane: <b>Actualizează</b>, <b>Export Excel</b>, "
               "<b>Trimite recomandă acum</b> (trimitere manuală)."),
        'de': ("Bestandsprüfung",
               "Menü <i>Indirektes Material → Bestand prüfen</i>. Zeigt aktuellen Bestand pro Code, "
               "Mindestbestand und Status. Zeilen <b>unter Minimum</b> sind rot hervorgehoben. Bei Auswahl "
               "eines Codes werden die letzten Bewegungen angezeigt. Schaltflächen: <b>Aktualisieren</b>, "
               "<b>Excel exportieren</b>, <b>Nachbestellung jetzt senden</b> (manuell)."),
        'sv': ("Lagerkontroll",
               "Meny <i>Indirekta material → Kontrollera lager</i>. Visar aktuellt lager per kod, "
               "minimilager och status. Rader <b>under minimum</b> markeras rött. Vid val av en kod visas "
               "dess senaste rörelser. Knappar: <b>Uppdatera</b>, <b>Exportera Excel</b>, "
               "<b>Skicka beställning nu</b> (manuellt)."),
    }),
    ('minimi', {
        'it': ("Configura Scorte Minime",
               "Menu <i>Materiali Indiretti → Configura Scorte Minime</i>. Per i codici dove ha senso, "
               "imposta <b>Scorta minima</b>, <b>Lotto riordino</b> e attiva/disattiva il riordino. Quando "
               "la giacenza scende sotto la scorta minima (con riordino attivo) il codice entra nell'elenco "
               "di riordino."),
        'en': ("Configure Minimum Stock",
               "Menu <i>Indirect Materials → Configure Minimum Stock</i>. For codes where it makes sense, "
               "set <b>Minimum stock</b>, <b>Reorder lot</b> and enable/disable reorder. When stock falls "
               "below the minimum (with reorder enabled), the code enters the reorder list."),
        'ro': ("Configurare Stoc Minim",
               "Meniu <i>Materiale Indirecte → Configurare Stoc Minim</i>. Pentru codurile unde are sens, "
               "setaţi <b>Stoc minim</b>, <b>Lot recomandă</b> şi activaţi/dezactivaţi recomanda. Când "
               "stocul scade sub minim (cu recomandă activă), codul intră în lista de recomandă."),
        'de': ("Mindestbestand konfigurieren",
               "Menü <i>Indirektes Material → Mindestbestand konfigurieren</i>. Für sinnvolle Codes "
               "<b>Mindestbestand</b>, <b>Nachbestellmenge</b> festlegen und Nachbestellung "
               "aktivieren/deaktivieren. Fällt der Bestand unter das Minimum (bei aktiver Nachbestellung), "
               "kommt der Code auf die Nachbestellliste."),
        'sv': ("Konfigurera minimilager",
               "Meny <i>Indirekta material → Konfigurera minimilager</i>. För koder där det är relevant, "
               "ange <b>Minimilager</b>, <b>Beställningsparti</b> och aktivera/inaktivera beställning. När "
               "lagret faller under minimum (med beställning aktiv) hamnar koden på beställningslistan."),
    }),
    ('prelievo', {
        'it': ("Prelievo e scarico di magazzino",
               "Menu <i>Materiali Indiretti → Conferma Materiali</i>. Una richiesta avanza di stato: "
               "<b>RICHIESTA → PREPARATA → PRELEVATA</b>. Alla conferma del <b>Prelievo</b> viene generato "
               "automaticamente lo <b>scarico</b> di magazzino (movimento negativo collegato alla richiesta) "
               "e la giacenza si aggiorna. È possibile anche <b>Annullare</b> una richiesta."),
        'en': ("Pick and stock-out",
               "Menu <i>Indirect Materials → Confirm Materials</i>. A request advances: "
               "<b>REQUESTED → PREPARED → PICKED</b>. On <b>Pick</b> confirmation the warehouse "
               "<b>stock-out</b> is generated automatically (negative movement linked to the request) and "
               "stock is updated. A request can also be <b>Cancelled</b>."),
        'ro': ("Ridicare şi descărcare din stoc",
               "Meniu <i>Materiale Indirecte → Confirmare Materiale</i>. O cerere avansează: "
               "<b>CERUTĂ → PREGĂTITĂ → RIDICATĂ</b>. La confirmarea <b>Ridicării</b> se generează automat "
               "<b>descărcarea</b> din stoc (mişcare negativă legată de cerere) şi stocul se actualizează. "
               "O cerere poate fi şi <b>Anulată</b>."),
        'de': ("Entnahme und Lagerabgang",
               "Menü <i>Indirektes Material → Material bestätigen</i>. Eine Anfrage durchläuft: "
               "<b>ANGEFRAGT → VORBEREITET → ENTNOMMEN</b>. Bei <b>Entnahme</b>-Bestätigung wird der "
               "<b>Lagerabgang</b> automatisch erzeugt (negative, mit der Anfrage verknüpfte Bewegung) und "
               "der Bestand aktualisiert. Eine Anfrage kann auch <b>storniert</b> werden."),
        'sv': ("Uttag och lageruttag",
               "Meny <i>Indirekta material → Bekräfta material</i>. En begäran avancerar: "
               "<b>BEGÄRD → FÖRBEREDD → UTTAGEN</b>. Vid <b>uttags</b>-bekräftelse skapas lageruttaget "
               "automatiskt (negativ rörelse kopplad till begäran) och lagret uppdateras. En begäran kan "
               "även <b>avbrytas</b>."),
    }),
    ('riordino', {
        'it': ("Riordino automatico verso gli acquisti",
               "Ogni giorno (alle 07:30, lun-sab) il sistema controlla i codici sotto scorta minima e invia "
               "una email di riordino ai responsabili acquisti. I destinatari si configurano in "
               "<b>Settings</b> con l'attributo <code>sys_email_acquista_indiretti</code> (più indirizzi "
               "separati da ; o ,). L'invio è <b>de-duplicato</b>: massimo una email al giorno per codice. "
               "È disponibile anche l'invio manuale dal pulsante <i>Invia riordino ora</i>."),
        'en': ("Automatic reorder to purchasing",
               "Every day (07:30, Mon-Sat) the system checks codes below minimum stock and emails a reorder "
               "to purchasing. Recipients are configured in <b>Settings</b> via the "
               "<code>sys_email_acquista_indiretti</code> attribute (multiple addresses separated by ; or ,). "
               "Sending is <b>de-duplicated</b>: at most one email per code per day. Manual send is also "
               "available via the <i>Send reorder now</i> button."),
        'ro': ("Recomandă automată către achiziţii",
               "În fiecare zi (07:30, Lun-Sâm) sistemul verifică codurile sub stoc minim şi trimite un email "
               "de recomandă către achiziţii. Destinatarii se configurează în <b>Settings</b> cu atributul "
               "<code>sys_email_acquista_indiretti</code> (mai multe adrese separate prin ; sau ,). "
               "Trimiterea este <b>de-duplicată</b>: maxim un email pe zi per cod. Există şi trimitere "
               "manuală din butonul <i>Trimite recomandă acum</i>."),
        'de': ("Automatische Nachbestellung an den Einkauf",
               "Täglich (07:30, Mo-Sa) prüft das System Codes unter Mindestbestand und sendet eine "
               "Nachbestell-E-Mail an den Einkauf. Empfänger werden in <b>Settings</b> über das Attribut "
               "<code>sys_email_acquista_indiretti</code> konfiguriert (mehrere Adressen durch ; oder , "
               "getrennt). Der Versand ist <b>dedupliziert</b>: höchstens eine E-Mail pro Code und Tag. "
               "Manueller Versand über die Schaltfläche <i>Nachbestellung jetzt senden</i>."),
        'sv': ("Automatisk beställning till inköp",
               "Varje dag (07:30, mån-lör) kontrollerar systemet koder under minimilager och skickar en "
               "beställning via e-post till inköp. Mottagare konfigureras i <b>Settings</b> via attributet "
               "<code>sys_email_acquista_indiretti</code> (flera adresser separerade med ; eller ,). "
               "Utskick är <b>deduplicerat</b>: högst ett mejl per kod och dag. Manuellt utskick finns via "
               "knappen <i>Skicka beställning nu</i>."),
    }),
    ('consumi', {
        'it': ("Analisi Consumi & Budget",
               "Menu <i>Materiali Indiretti → Analisi Consumi & Budget</i>. I consumi si basano sugli "
               "<b>scarichi</b> registrati. Schede: <b>Settimanale</b>, <b>Mensile</b>, <b>Annuale</b>. "
               "La scheda <b>Budget anno prossimo</b> propone per ogni codice il budget annuo e mensile "
               "partendo dal consumo degli ultimi 12 mesi, con una <b>% di crescita</b> impostabile. "
               "Tutto esportabile in Excel."),
        'en': ("Consumption & Budget Analysis",
               "Menu <i>Indirect Materials → Consumption & Budget Analysis</i>. Consumption is based on "
               "recorded <b>stock-outs</b>. Tabs: <b>Weekly</b>, <b>Monthly</b>, <b>Yearly</b>. The "
               "<b>Next year budget</b> tab proposes annual and monthly budget per code from the last "
               "12 months consumption, with a settable <b>growth %</b>. Everything is exportable to Excel."),
        'ro': ("Analiză Consumuri & Buget",
               "Meniu <i>Materiale Indirecte → Analiză Consumuri & Buget</i>. Consumurile se bazează pe "
               "<b>descărcările</b> înregistrate. File: <b>Săptămânal</b>, <b>Lunar</b>, <b>Anual</b>. Fila "
               "<b>Buget anul viitor</b> propune bugetul anual şi lunar per cod pornind de la consumul "
               "ultimelor 12 luni, cu un <b>% de creştere</b> setabil. Totul exportabil în Excel."),
        'de': ("Verbrauchs- & Budgetanalyse",
               "Menü <i>Indirektes Material → Verbrauchs- & Budgetanalyse</i>. Der Verbrauch basiert auf "
               "erfassten <b>Abgängen</b>. Registerkarten: <b>Wöchentlich</b>, <b>Monatlich</b>, "
               "<b>Jährlich</b>. Die Registerkarte <b>Budget nächstes Jahr</b> schlägt pro Code Jahres- und "
               "Monatsbudget aus dem Verbrauch der letzten 12 Monate vor, mit einstellbarem "
               "<b>Wachstum %</b>. Alles nach Excel exportierbar."),
        'sv': ("Förbruknings- & budgetanalys",
               "Meny <i>Indirekta material → Förbruknings- & budgetanalys</i>. Förbrukning baseras på "
               "registrerade <b>uttag</b>. Flikar: <b>Veckovis</b>, <b>Månatlig</b>, <b>Årlig</b>. Fliken "
               "<b>Budget nästa år</b> föreslår års- och månadsbudget per kod utifrån de senaste 12 "
               "månadernas förbrukning, med justerbar <b>tillväxt %</b>. Allt kan exporteras till Excel."),
    }),
]


def build_html():
    blocks = []
    for code, _name in LANGS:
        secs = []
        for sid, perlang in SECTIONS:
            title, body = perlang[code]
            secs.append(f"<section><h2>{title}</h2><p>{body}</p></section>")
        page = PAGE_TITLE[code]
        blocks.append(
            f'<div class="lang" id="lang-{code}" style="display:none">'
            f'<h1>{page}</h1>{"".join(secs)}</div>')

    buttons = "".join(
        f'<button onclick="showLang(\'{c}\')">{n}</button>' for c, n in LANGS)

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{PAGE_TITLE['it']}</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 900px; margin: 0 auto;
         padding: 24px; color: #222; line-height: 1.55; }}
  .langbar {{ position: sticky; top: 0; background: #fff; padding: 10px 0;
              border-bottom: 2px solid #2F6DA4; margin-bottom: 20px; }}
  .langbar button {{ font-size: 14px; margin-right: 6px; padding: 6px 12px; cursor: pointer;
                     border: 1px solid #2F6DA4; background: #eef4fa; border-radius: 4px; }}
  .langbar button:hover {{ background: #2F6DA4; color: #fff; }}
  h1 {{ color: #2F6DA4; }}
  h2 {{ color: #1f4e79; margin-top: 26px; border-left: 4px solid #2F6DA4; padding-left: 8px; }}
  code {{ background: #f0f0f0; padding: 1px 5px; border-radius: 3px; font-size: 0.95em; }}
</style>
</head>
<body>
<div class="langbar">{buttons}</div>
{"".join(blocks)}
<script>
function showLang(c) {{
  document.querySelectorAll('.lang').forEach(function(d) {{ d.style.display = 'none'; }});
  var el = document.getElementById('lang-' + c);
  if (el) el.style.display = 'block';
}}
showLang('it');
</script>
</body>
</html>"""
    return html


def main():
    os.makedirs('docs', exist_ok=True)
    path = os.path.join('docs', 'Manual_Gestione_Giacenze.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(build_html())
    print(f"Generato {path}")


if __name__ == "__main__":
    main()
