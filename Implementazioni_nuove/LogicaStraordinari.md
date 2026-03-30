\# Specifiche per l'implementazione della logica operativa delle ore supplementari in Python



\## Obiettivo

L'obiettivo è implementare una funzionalità in un programma Python esistente per la gestione automatizzata delle ore supplementari. La soluzione deve:

\- Eliminare i processi manuali.

\- Garantire una tracciabilità delle ore lavorate per un periodo di 4 mesi.

\- Rispettare il limite legale di 48 ore settimanali.

\- Differenziare chiaramente tra:

&nbsp; - Ore mantenute come supplementari.

&nbsp; - Ore convertite in premi.



---



\## Requisiti funzionali

\### 1. \*\*Gestione delle ore supplementari\*\*

\- \*\*Ore del weekend\*\*:

&nbsp; - Devono rimanere segnate come ore supplementari.

&nbsp; - Devono avere una richiesta approvata.

&nbsp; - Non devono essere modificate.



\- \*\*Volumi elevati durante la settimana\*\*:

&nbsp; - Se un dipendente lavora per più giorni consecutivi 12 ore al giorno o se c'è rischio di:

&nbsp;   - Superamento del limite di 48 ore settimanali.

&nbsp;   - Non conformità legale per il riposo obbligatorio.

&nbsp; - Allora:

&nbsp;   - Le ore supplementari non devono essere registrate come tali nel registro delle ore.

&nbsp;   - Devono essere calcolate e assegnate come premi.



\- \*\*Volumi controllati (es. max ~32 ore supplementari/mese)\*\*:

&nbsp; - Se non ci sono ore nel weekend e si rientra nella media di 48 ore settimanali su 4 mesi:

&nbsp;   - Le ore devono essere mantenute come supplementari.

&nbsp;   - Le ore possono essere suddivise (split) e redistribuite su più giorni, se necessario.



---



\### 2. \*\*Funzionalità richieste\*\*

1\. \*\*Richieste flessibili di ore supplementari\*\*:

&nbsp;  - Possibilità di:

&nbsp;    - Modificare la richiesta iniziale.

&nbsp;    - Generare automaticamente richieste per ore suddivise (split).



2\. \*\*Funzione di "split"\*\*:

&nbsp;  - Il sistema deve permettere:

&nbsp;    - La redistribuzione automatica delle ore su più giorni senza necessità di richieste iniziali.

&nbsp;    - Applicabile solo in assenza di un numero elevato di giorni consecutivi con ore supplementari.



3\. \*\*Monitoraggio automatico su 4 mesi\*\*:

&nbsp;  - Il sistema deve calcolare:

&nbsp;    - Totale ore lavorate a settimana (da lunedì a domenica).

&nbsp;    - Media delle ore lavorate su 4 mesi.

&nbsp;  - Deve generare un avviso se ci si avvicina al limite di 48 ore settimanali.



---



\## Logica decisionale

La logica del sistema deve seguire i seguenti passaggi:



1\. \*\*Verificare se ci sono ore nel weekend\*\*:

&nbsp;  - Se SÌ → Le ore rimangono ore supplementari.

&nbsp;  - Se NO → Passare al punto successivo.



2\. \*\*Verificare se ci sono volumi elevati durante la settimana\*\*:

&nbsp;  - Se SÌ → Convertire le ore supplementari in premi.

&nbsp;  - Se NO → Passare al punto successivo.



3\. \*\*Verificare se ci sono ore supplementari moderate\*\*:

&nbsp;  - Se SÌ → Mantenere le ore supplementari e applicare lo split, se necessario.



---



\## Struttura del codice in Python

Di seguito viene fornita una struttura di base per il codice Python che implementa la logica sopra descritta.



````code.python

\# Importazione delle librerie necessarie

from datetime import datetime, timedelta



\# Funzione per calcolare la media delle ore settimanali su 4 mesi

def calcola\_media\_ore(settimane):

&nbsp;   return sum(settimane) / len(settimane)



\# Funzione per monitorare le ore lavorate

def monitoraggio\_ore(settimane, limite=48):

&nbsp;   media = calcola\_media\_ore(settimane)

&nbsp;   if media > limite:

&nbsp;       print(f"Attenzione: la media delle ore settimanali ({media:.2f}) supera il limite di {limite} ore.")

&nbsp;   return media



\# Funzione per gestire le ore supplementari

def gestisci\_ore\_supplementari(ore\_settimanali, ore\_giornaliere, weekend=False):

&nbsp;   if weekend:

&nbsp;       return "Ore mantenute come supplementari"

&nbsp;   

&nbsp;   if any(ore > 12 for ore in ore\_giornaliere) or sum(ore\_settimanali) > 48:

&nbsp;       return "Ore convertite in premi"

&nbsp;   

&nbsp;   if sum(ore\_settimanali) <= 48:

&nbsp;       return "Ore mantenute come supplementari e suddivise se necessario"

&nbsp;   

&nbsp;   return "Errore nella logica di gestione"



\# Esempio di utilizzo

if \_\_name\_\_ == "\_\_main\_\_":

&nbsp;   # Dati di esempio

&nbsp;   ore\_settimanali = \[40, 50, 45, 42]  # Ore lavorate nelle ultime 4 settimane

&nbsp;   ore\_giornaliere = \[8, 12, 12, 8, 8, 0, 0]  # Ore lavorate in una settimana tipo

&nbsp;   

&nbsp;   # Monitoraggio delle ore

&nbsp;   media = monitoraggio\_ore(ore\_settimanali)

&nbsp;   print(f"Media ore settimanali su 4 mesi: {media:.2f} ore")

&nbsp;   

&nbsp;   # Gestione delle ore supplementari

&nbsp;   risultato = gestisci\_ore\_supplementari(ore\_settimanali, ore\_giornaliere, weekend=False)

&nbsp;   print(f"Risultato gestione ore: {risultato}")



