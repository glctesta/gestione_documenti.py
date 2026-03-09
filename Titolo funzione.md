# Titolo funzione
Nuova funzionalità: Compilazione in automatico rapporti di attivita’ per dipendenti terza societa’ in visita di presenza o in remoto in Vandewiele Romania.
Versione documento: 1.0  
Data: 2026-03-05  
Autore: Gianluca Testa

## 1. Scopo
Per poter pagare i servizi prestati da colleghi di una societa’ controllante e/o partecipata e/o infragruppo, allo scopo di supportare lo sviluppo tecnico professionale dei colleghi in romania, il codice fiscale rumeno prevede sia stato stipulato un contratto tra le parti e, con la base questo contratto, i vari attori devono rispettare alcuni passi. 
1. Inviare una richiesta di suppporto per la soluzione di un problema specifico
2. Accettazione della richiesta con indicazioni ,anche sommarie , del programma che si intendera’portare avanti per supportare la richiedente.
3. Registrazione dell’arrivo in loco del formatore.
4. Svolgimento del suo compito
5. Al termine (partenza dalla romania) stilare rapporto di attivita’ inerente al periodo e all’oggetto della richiesta. 
6. Tenere traccia delle documentazioni e delle presenze dei singolo formatori/verificatori
## 2. Contesto e problemi attuali
- oggi esiste un programma per la registrazione degli ospiti stranieri che sono legati a una societa’ che puo’ essere marcata quale ente che emettera’ fattura per i servizi svolti dai propri dipendenti. IL probgramma e’ un’ottima base di partenza, ma manca tutta la parte di corrispondenza e reportistica che, attualmente grava sui formatori che devono rapportare quanto hanno svolto, e su chi racccoglie queste informazioni per tradurle in una fatturazione che sia petinente con il contratto che esiste alla base del rapporto.
## 3. Obiettivi della funzione
- Obiettivo 1 sfruttare le informazioni gia’ presenti nel sistema Document Management:
1. data arrivo e partenza personaggio ospite, motivo della visita, persona di contatto che lo riceve. Conferma arrivo e conferma partenza. 
2. dati del personale in subordine della persona di contatto ricevente l’ospite, come presenza, appartenenza centro di costo,funzione
- Obiettivo 2 generare in automatico tutta la documentazione necessaria per giustificare l’operato dell’ospite al fine di permettere che la societa’ che ha erogato il servizio di formazione/verifica/consulenza etc, sulla base del contratto tra le societa’, possa fatturare i servizi prestati. 
## 5. Flusso funzionale (uso operativo)
Una volta che l’ospite arriva in VR (Romania) trovera’ all’ingresso un kiosk che gli da il benvenuto. Egli dovra’ confermare di aver preso visione delle norme di sicurezza della VR e stampare il suo badge provvisorio che gli dara’ libero accesso in fabbrica. 
Quando se ne andra’, dovra’ confermare il suo checkout in modo che il sistema lo depenni dalle persone presenti in fabbrica, lista a disposizione dell’ufficio HR in caso di eventi catastrofici.

1. il giorno successivo alla partenza dell’ospite, se la sua societa’ e’ marcata quale societa’ che fattura, il sistema preparera’:
a. Lettera di richiesta di intervento nominativa per l’ospite intervenuto, data inizio e fine, oggetto (che sara’ gia’ registrato nellat abella Visitors come scopo delle visita e persona di riferimeto, stessa tabella nel campo [sponsor]. Ovviamente questa lettera avra’ una settimana di anticipo  (in giorno lavorativo)o di piu’,come data, dalla data di arrivo dell’ospite.
b. Lettera di accettazione, successiva di un paio di giorni (lavorativi)  dove si riporteranno igli estremi del viaggio ,la permanenza, e l’oggetto della visita. I nomi che firmono e ricevono le lettere saranno da estrapolare da traceability_rs.dbo.settings con atribute = ‘chi_richiede’ e ‘chi_invia’
c. Successivamente con data successica lvorativa alla data di fine visita, il sisitema dovra’ inviare via email il rapporto di attivita’ dell’ospite che conterra’ la data, oggetto, una prefazione che fara’ riferimento al contratto tra le parti e una breve descrizione delle attivita’ svolte durante il periodo di presenza da arrivo a partenza. Utilizzera’ dei template variabili che avranno sempre come oggetto il valore della campo [scopo] della tabella visitors.
d. Questa email, sara’ inviata , estraendo i dati sempre dalla stessa tabella di prima ma con atribute ‘chi_richiede_email’ ‘ chi_invia_email’ e l’email del soggetto ospite che di fatto rappresenta essere il formatore. 

