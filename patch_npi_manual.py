# -*- coding: utf-8 -*-
"""Patch NPI_User_Manual.html to add v2.3.6 sections."""
import os

MANUAL = os.path.join(os.path.dirname(__file__), "docs", "NPI_User_Manual.html")

with open(MANUAL, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Version bump in cover
html = html.replace("Versione 2.3.2 &mdash; Marzo 2026", "Versione 2.3.6 &mdash; Marzo 2026")

# 2. Version bump in footer
html = html.replace("NPI Module v2.3.2", "NPI Module v2.3.6")

# 3. Italian TOC - add entries 13-16
IT_TOC_OLD = '<a href="#it-12"><span class="num">12.</span> Gestione Permessi e Accesso</a>\r\n</div>'
IT_TOC_NEW = '''<a href="#it-12"><span class="num">12.</span> Gestione Permessi e Accesso</a>
<a href="#it-13"><span class="num">13.</span> Gestione Budget di Progetto</a>
<a href="#it-14"><span class="num">14.</span> Checklist NPI</a>
<a href="#it-15"><span class="num">15.</span> Gestione Avanzata Documenti (CRUD)</a>
<a href="#it-16"><span class="num">16.</span> Logica di Completamento Milestone</a>
</div>'''
html = html.replace(IT_TOC_OLD, IT_TOC_NEW)

# 4. English TOC - add entries 13-16
EN_TOC_OLD = '<a href="#en-12"><span class="num">12.</span> Permissions &amp; Access Control</a>\r\n</div>'
EN_TOC_NEW = '''<a href="#en-12"><span class="num">12.</span> Permissions &amp; Access Control</a>
<a href="#en-13"><span class="num">13.</span> Project Budget Management</a>
<a href="#en-14"><span class="num">14.</span> NPI Checklist</a>
<a href="#en-15"><span class="num">15.</span> Advanced Document Management (CRUD)</a>
<a href="#en-16"><span class="num">16.</span> Milestone Completion Logic</a>
</div>'''
html = html.replace(EN_TOC_OLD, EN_TOC_NEW)

# 5. Italian content sections 13-16
IT_SECTIONS = '''
<!-- 13. BUDGET -->
<div class="section" id="it-13">
<h2>&#x31;&#xFE0F;&#x20E3;&#x33;&#xFE0F;&#x20E3; Gestione Budget di Progetto</h2>
<p>Il modulo <strong>Budget Management</strong> (v2.3.4+) consente di definire, monitorare e controllare il budget associato a ciascun progetto NPI. Ogni progetto puo' avere un budget pianificato e i costi effettivi vengono tracciati in tempo reale.</p>
<h3>Funzionalita' Principali</h3>
<table>
<tr><th>Funzione</th><th>Descrizione</th></tr>
<tr><td><strong>Budget Pianificato</strong></td><td>Definizione del budget totale previsto per il progetto, suddiviso per categoria di costo</td></tr>
<tr><td><strong>Costi Effettivi</strong></td><td>Registrazione dei costi reali sostenuti, con confronto automatico rispetto al pianificato</td></tr>
<tr><td><strong>Varianza</strong></td><td>Calcolo automatico della varianza tra budget pianificato e costi effettivi con indicatori visivi (verde/giallo/rosso)</td></tr>
<tr><td><strong>Report Budget</strong></td><td>Esportazione del riepilogo budget in formato Excel con grafici di confronto</td></tr>
</table>
<h3>Categorie di Costo</h3>
<ul class="field-list">
<li><strong>Materiali</strong> &mdash; Costi per materie prime, componenti e materiali di consumo</li>
<li><strong>Manodopera</strong> &mdash; Ore di lavoro del personale coinvolto nel progetto</li>
<li><strong>Attrezzature</strong> &mdash; Investimenti in macchinari, stampi e attrezzature specifiche</li>
<li><strong>Test e Certificazioni</strong> &mdash; Costi per prove, test di laboratorio e certificazioni</li>
<li><strong>Altro</strong> &mdash; Costi vari non classificabili nelle categorie precedenti</li>
</ul>
<div class="info-box blue">
<strong>&#x1F4CC; Accesso</strong>
Il modulo Budget e' accessibile dalla finestra del progetto tramite il pulsante "Budget" nella toolbar. Solo il Project Owner e gli utenti con permessi di amministrazione possono modificare il budget pianificato.
</div>
<div class="info-box orange">
<strong>&#x26A0;&#xFE0F; Attenzione</strong>
Quando la varianza supera il 10% del budget pianificato, il sistema genera automaticamente un warning visivo nella Dashboard e invia una notifica al Project Owner.
</div>
</div>

<!-- 14. CHECKLIST NPI -->
<div class="section" id="it-14">
<h2>&#x31;&#xFE0F;&#x20E3;&#x34;&#xFE0F;&#x20E3; Checklist NPI</h2>
<p>La <strong>Checklist NPI</strong> (v2.3.3+) fornisce un sistema strutturato per la verifica e validazione di tutte le fasi del processo di introduzione di un nuovo prodotto. Ogni progetto dispone di una checklist personalizzabile basata su template predefiniti.</p>
<h3>Struttura della Checklist</h3>
<table>
<tr><th>Elemento</th><th>Descrizione</th></tr>
<tr><td><strong>Fase</strong></td><td>Le macro-fasi del processo NPI (Design, Prototipazione, Validazione, Pre-serie, Produzione)</td></tr>
<tr><td><strong>Punto di Verifica</strong></td><td>Singolo elemento da verificare all'interno di una fase</td></tr>
<tr><td><strong>Stato</strong></td><td>OK / NOK / N/A &mdash; con data di verifica e responsabile</td></tr>
<tr><td><strong>Evidenza</strong></td><td>Possibilita' di allegare documenti o note come evidenza della verifica</td></tr>
<tr><td><strong>Gate Review</strong></td><td>Approvazione formale del passaggio alla fase successiva</td></tr>
</table>
<h3>Procedura Operativa</h3>
<div class="info-box blue">
<strong>&#x1F4CC; Flusso di Verifica</strong>
1. <strong>Selezione Template</strong> &rarr; Al momento della creazione del progetto, selezionare il template di checklist appropriato<br>
2. <strong>Assegnazione Responsabili</strong> &rarr; Ogni punto di verifica viene assegnato a un responsabile specifico<br>
3. <strong>Esecuzione Verifiche</strong> &rarr; I responsabili compilano i punti della checklist con stato e evidenze<br>
4. <strong>Gate Review</strong> &rarr; Il Project Owner approva il passaggio alla fase successiva verificando il completamento di tutti i punti<br>
5. <strong>Report Finale</strong> &rarr; Al completamento, viene generato un report PDF della checklist con tutte le evidenze
</div>
<div class="info-box green">
<strong>&#x2705; Best Practice</strong>
La checklist deve essere configurata dal responsabile NPI prima dell'avvio del progetto. Tutti i punti NOK devono essere risolti prima di procedere alla fase successiva tramite Gate Review.
</div>
</div>

<!-- 15. GESTIONE DOCUMENTI AVANZATA -->
<div class="section" id="it-15">
<h2>&#x31;&#xFE0F;&#x20E3;&#x35;&#xFE0F;&#x20E3; Gestione Avanzata Documenti (CRUD)</h2>
<p>A partire dalla versione <strong>v2.3.2.14+</strong>, il sistema di gestione documenti e' stato completamente rinnovato con operazioni CRUD complete (Creazione, Lettura, Aggiornamento, Eliminazione) e funzionalita' avanzate di ricerca e filtro.</p>
<h3>Operazioni Disponibili</h3>
<table>
<tr><th>Operazione</th><th>Descrizione</th></tr>
<tr><td><strong>Crea Documento</strong></td><td>Aggiunta di un nuovo documento con metadati completi (titolo, tipo, valore, descrizione)</td></tr>
<tr><td><strong>Modifica Documento</strong></td><td>Aggiornamento dei metadati e sostituzione del file allegato</td></tr>
<tr><td><strong>Elimina (Soft Delete)</strong></td><td>Eliminazione logica del documento con possibilita' di ripristino</td></tr>
<tr><td><strong>Ripristina</strong></td><td>Recupero di un documento precedentemente eliminato</td></tr>
<tr><td><strong>Ricerca e Filtro</strong></td><td>Ricerca full-text su titolo e descrizione, filtro per tipo documento</td></tr>
<tr><td><strong>Ordinamento</strong></td><td>Ordinamento per colonna (titolo, tipo, data, valore) con click sull'intestazione</td></tr>
</table>
<h3>Campi del Documento</h3>
<ul class="field-list">
<li><strong>Titolo *</strong> &mdash; Nome identificativo del documento (obbligatorio)</li>
<li><strong>Tipo Documento *</strong> &mdash; Classificazione del tipo (es. Disegno, Specifica, Report, Certificato)</li>
<li><strong>Valore</strong> &mdash; Valore numerico associato al documento (es. costo, quantita')</li>
<li><strong>Descrizione</strong> &mdash; Note aggiuntive e descrizione dettagliata del contenuto</li>
<li><strong>File Allegato</strong> &mdash; File binario associato al documento</li>
</ul>
<div class="info-box blue">
<strong>&#x1F4CC; Riepilogo Valori</strong>
La finestra dei documenti include un pannello riepilogativo che mostra la somma totale dei valori di tutti i documenti attivi del progetto, utile per il monitoraggio dei costi documentali.
</div>
</div>

<!-- 16. MILESTONE COMPLETION -->
<div class="section" id="it-16">
<h2>&#x31;&#xFE0F;&#x20E3;&#x36;&#xFE0F;&#x20E3; Logica di Completamento Milestone</h2>
<p>Il sistema implementa una logica avanzata per il <strong>completamento automatico delle milestone</strong> di progetto, basata sullo stato dei task figli nella gerarchia del progetto.</p>
<h3>Regole di Completamento</h3>
<table>
<tr><th>Regola</th><th>Logica</th></tr>
<tr><td><strong>Milestone Auto-Complete</strong></td><td>Una milestone viene automaticamente marcata come completata quando tutti i task figli raggiungono lo stato 'Completato'</td></tr>
<tr><td><strong>Calcolo % Avanzamento</strong></td><td>La percentuale di avanzamento della milestone e' calcolata come media ponderata dei task figli completati</td></tr>
<tr><td><strong>Propagazione Stato</strong></td><td>Lo stato di ritardo si propaga automaticamente dalla milestone ai task padre nella gerarchia</td></tr>
<tr><td><strong>Verifica Dipendenze</strong></td><td>Il completamento verifica che tutte le dipendenze precedenti siano state soddisfatte</td></tr>
</table>
<h3>Metriche di Performance</h3>
<div class="info-box blue">
<strong>&#x1F4CC; Algoritmo di Valutazione</strong>
<strong>Completati in Tempo:</strong> Task con Stato = 'Completato' e DataCompletamento &le; DataScadenza<br>
<strong>Completati in Ritardo:</strong> Task con Stato = 'Completato' e DataCompletamento &gt; DataScadenza<br>
<strong>In Ritardo:</strong> Task con Stato &ne; 'Completato' e DataScadenza &lt; Oggi<br>
<strong>% Avanzamento:</strong> ((Completati in Tempo + Completati in Ritardo) / Task Totali) &times; 100
</div>
<div class="info-box orange">
<strong>&#x26A0;&#xFE0F; Target NPI</strong>
Il Target NPI rappresenta la milestone finale del progetto. Quando viene raggiunto (tutti i task completati), il progetto puo' essere chiuso dal Project Owner tramite la Dashboard.
</div>
</div>

'''
html = html.replace('</div><!-- end Italian content -->', IT_SECTIONS + '</div><!-- end Italian content -->')

# 6. English content sections 13-16
EN_SECTIONS = '''
<!-- 13. BUDGET -->
<div class="section" id="en-13">
<h2>&#x31;&#xFE0F;&#x20E3;&#x33;&#xFE0F;&#x20E3; Project Budget Management</h2>
<p>The <strong>Budget Management</strong> module (v2.3.4+) enables definition, monitoring and control of the budget associated with each NPI project. Each project can have a planned budget and actual costs are tracked in real time.</p>
<h3>Key Features</h3>
<table>
<tr><th>Feature</th><th>Description</th></tr>
<tr><td><strong>Planned Budget</strong></td><td>Definition of total planned budget for the project, broken down by cost category</td></tr>
<tr><td><strong>Actual Costs</strong></td><td>Recording of actual costs incurred, with automatic comparison against planned</td></tr>
<tr><td><strong>Variance</strong></td><td>Automatic variance calculation between planned budget and actual costs with visual indicators (green/yellow/red)</td></tr>
<tr><td><strong>Budget Report</strong></td><td>Budget summary export in Excel format with comparison charts</td></tr>
</table>
<h3>Cost Categories</h3>
<ul class="field-list">
<li><strong>Materials</strong> &mdash; Costs for raw materials, components and consumables</li>
<li><strong>Labor</strong> &mdash; Working hours of personnel involved in the project</li>
<li><strong>Equipment</strong> &mdash; Investments in machinery, molds and specific equipment</li>
<li><strong>Testing &amp; Certifications</strong> &mdash; Costs for testing, laboratory tests and certifications</li>
<li><strong>Other</strong> &mdash; Miscellaneous costs not classifiable in previous categories</li>
</ul>
<div class="info-box blue">
<strong>&#x1F4CC; Access</strong>
The Budget module is accessible from the project window via the "Budget" button in the toolbar. Only the Project Owner and users with administration permissions can modify the planned budget.
</div>
<div class="info-box orange">
<strong>&#x26A0;&#xFE0F; Warning</strong>
When variance exceeds 10% of the planned budget, the system automatically generates a visual warning on the Dashboard and sends a notification to the Project Owner.
</div>
</div>

<!-- 14. NPI CHECKLIST -->
<div class="section" id="en-14">
<h2>&#x31;&#xFE0F;&#x20E3;&#x34;&#xFE0F;&#x20E3; NPI Checklist</h2>
<p>The <strong>NPI Checklist</strong> (v2.3.3+) provides a structured system for verification and validation of all phases of the new product introduction process. Each project has a customizable checklist based on predefined templates.</p>
<h3>Checklist Structure</h3>
<table>
<tr><th>Element</th><th>Description</th></tr>
<tr><td><strong>Phase</strong></td><td>The macro-phases of the NPI process (Design, Prototyping, Validation, Pre-series, Production)</td></tr>
<tr><td><strong>Verification Point</strong></td><td>Individual item to be verified within a phase</td></tr>
<tr><td><strong>Status</strong></td><td>OK / NOK / N/A &mdash; with verification date and responsible person</td></tr>
<tr><td><strong>Evidence</strong></td><td>Ability to attach documents or notes as verification evidence</td></tr>
<tr><td><strong>Gate Review</strong></td><td>Formal approval for progression to the next phase</td></tr>
</table>
<h3>Operational Procedure</h3>
<div class="info-box blue">
<strong>&#x1F4CC; Verification Flow</strong>
1. <strong>Template Selection</strong> &rarr; When creating the project, select the appropriate checklist template<br>
2. <strong>Assign Responsible</strong> &rarr; Each verification point is assigned to a specific responsible person<br>
3. <strong>Execute Verifications</strong> &rarr; Responsible persons complete checklist items with status and evidence<br>
4. <strong>Gate Review</strong> &rarr; The Project Owner approves progression to the next phase after verifying all points are complete<br>
5. <strong>Final Report</strong> &rarr; Upon completion, a PDF report of the checklist with all evidence is generated
</div>
<div class="info-box green">
<strong>&#x2705; Best Practice</strong>
The checklist should be configured by the NPI manager before project start. All NOK points must be resolved before proceeding to the next phase via Gate Review.
</div>
</div>

<!-- 15. ADVANCED DOCUMENT MANAGEMENT -->
<div class="section" id="en-15">
<h2>&#x31;&#xFE0F;&#x20E3;&#x35;&#xFE0F;&#x20E3; Advanced Document Management (CRUD)</h2>
<p>Starting from version <strong>v2.3.2.14+</strong>, the document management system has been completely redesigned with full CRUD operations (Create, Read, Update, Delete) and advanced search and filter capabilities.</p>
<h3>Available Operations</h3>
<table>
<tr><th>Operation</th><th>Description</th></tr>
<tr><td><strong>Create Document</strong></td><td>Add a new document with complete metadata (title, type, value, description)</td></tr>
<tr><td><strong>Edit Document</strong></td><td>Update metadata and replace attached file</td></tr>
<tr><td><strong>Delete (Soft Delete)</strong></td><td>Logical deletion of the document with possibility to restore</td></tr>
<tr><td><strong>Restore</strong></td><td>Recovery of a previously deleted document</td></tr>
<tr><td><strong>Search &amp; Filter</strong></td><td>Full-text search on title and description, filter by document type</td></tr>
<tr><td><strong>Sorting</strong></td><td>Sort by column (title, type, date, value) by clicking column header</td></tr>
</table>
<h3>Document Fields</h3>
<ul class="field-list">
<li><strong>Title *</strong> &mdash; Document identification name (required)</li>
<li><strong>Document Type *</strong> &mdash; Type classification (e.g., Drawing, Specification, Report, Certificate)</li>
<li><strong>Value</strong> &mdash; Numeric value associated with the document (e.g., cost, quantity)</li>
<li><strong>Description</strong> &mdash; Additional notes and detailed content description</li>
<li><strong>Attached File</strong> &mdash; Binary file associated with the document</li>
</ul>
<div class="info-box blue">
<strong>&#x1F4CC; Value Summary</strong>
The documents window includes a summary panel showing the total sum of values of all active project documents, useful for monitoring document-related costs.
</div>
</div>

<!-- 16. MILESTONE COMPLETION -->
<div class="section" id="en-16">
<h2>&#x31;&#xFE0F;&#x20E3;&#x36;&#xFE0F;&#x20E3; Milestone Completion Logic</h2>
<p>The system implements advanced logic for <strong>automatic milestone completion</strong>, based on the status of child tasks within the project hierarchy.</p>
<h3>Completion Rules</h3>
<table>
<tr><th>Rule</th><th>Logic</th></tr>
<tr><td><strong>Milestone Auto-Complete</strong></td><td>A milestone is automatically marked as completed when all child tasks reach 'Completed' status</td></tr>
<tr><td><strong>Progress % Calculation</strong></td><td>Milestone progress percentage is calculated as the weighted average of completed child tasks</td></tr>
<tr><td><strong>Status Propagation</strong></td><td>Overdue status automatically propagates from milestone to parent tasks in the hierarchy</td></tr>
<tr><td><strong>Dependency Verification</strong></td><td>Completion verifies that all predecessor dependencies have been satisfied</td></tr>
</table>
<h3>Performance Metrics</h3>
<div class="info-box blue">
<strong>&#x1F4CC; Evaluation Algorithm</strong>
<strong>Completed On-Time:</strong> Tasks with Status = 'Completed' and CompletionDate &le; DueDate<br>
<strong>Completed Late:</strong> Tasks with Status = 'Completed' and CompletionDate &gt; DueDate<br>
<strong>Overdue:</strong> Tasks with Status &ne; 'Completed' and DueDate &lt; Today<br>
<strong>Progress %:</strong> ((Completed On-Time + Completed Late) / Total Tasks) &times; 100
</div>
<div class="info-box orange">
<strong>&#x26A0;&#xFE0F; NPI Target</strong>
The NPI Target represents the final milestone of the project. When reached (all tasks completed), the project can be closed by the Project Owner via the Dashboard.
</div>
</div>

'''
html = html.replace('</div><!-- end English content -->', EN_SECTIONS + '</div><!-- end English content -->')

with open(MANUAL, "w", encoding="utf-8") as f:
    f.write(html)

print("NPI_User_Manual.html patched successfully!")
print(f"  File size: {os.path.getsize(MANUAL):,} bytes")
