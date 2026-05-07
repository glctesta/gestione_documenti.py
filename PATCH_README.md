# Patch: Plan Alert Escalation — invio solo 30 min prima fine turno

## Cosa cambia

Le email di escalation del piano produzione (`[ESCALARE MANAGEMENT] Alerte plan producție...`)
venivano inviate troppo frequentemente. Con questa patch:

- **1 sola email per turno**, nei **30 minuti prima della fine turno**:
  - Turno 1: finestra 15:00 - 15:30 (fine turno 15:30)
  - Turno 2: finestra 23:00 - 23:30 (fine turno 23:30)
- **Nessun invio** nei giorni non lavorativi (weekend / festivi RO).
- Email **più compatta**: summary in testa con conteggio per fase, tabelle
  limitate alle **top 10 alert per deficit** per ogni fase (con conteggio
  delle righe nascoste).

## File modificati

| File | Descrizione |
|---|---|
| `plan_alert_escalation.py` | Gate temporale + dedup per turno + HTML compatto |
| `main.py` | Finestra operativa del worker estesa per coprire fine turno 2 |

## Deploy

1. Fermare il servizio / app che usa il modulo.
2. Sostituire i file `plan_alert_escalation.py` e `main.py` nella directory
   di installazione con quelli forniti in questo zip.
3. Riavviare.

## Verifica

- Durante l'orario `15:00-15:30` di un giorno lavorativo, al primo ciclo del
  worker deve partire al massimo UNA email (fine turno 1).
- Idem per `23:00-23:30` (fine turno 2).
- Fuori finestra il worker logga "turno X gia' notificato" oppure non fa nulla.
