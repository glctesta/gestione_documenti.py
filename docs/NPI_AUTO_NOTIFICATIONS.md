# Sistema di Notifiche Automatiche NPI

## Panoramica

Sistema automatico per inviare notifiche email giornaliere ai responsabili di task NPI in scadenza o scaduti.

## Componenti

### 1. **Database** (`CREATE_NPI_TASK_NOTIFICATIONS_TABLE.sql`)
- Tabella `NpiTaskNotifications` per tracciare le email inviate
- Indici per performance e prevenzione duplicati
- Vista `vw_NpiTaskNotificationsStats` per statistiche

### 2. **Configurazione** (`npi_notifications_config.json`)
```json
{
  "notification_settings": {
    "enabled": true,
    "check_time": "08:00"  // Ora giornaliera per controllo
  },
  "recipient_types": {
    "Interno": {"send_email": true},   // Dipendenti interni
    "Cliente": {"send_email": false},  // Clienti esterni
    "Fornitore": {"send_email": false} // Fornitori
  },
  "notification_types": {
    "task_due_tomorrow": {
      "enabled": true,
      "days_before": 1  // Notifica 1 giorno prima scadenza
    },
    "task_overdue": {
      "enabled": true   // Notifica per task scaduti
    }
  }
}
```

### 3. **Servizio Python** (`npi/npi_auto_notifications_py`)
- Classe `NpiAutoNotificationService`
- Esecuzione in background thread
- Controllo giornaliero automatico
- Email HTML professionali con logo

### 4. **Modello Database** (`npi/data_models_notification.py`)
- Classe `NpiTaskNotification` per SQLAlchemy

## Funzionalità

### ✅ Notifiche Automatiche
- **Task in scadenza**: Email inviata 1 giorno prima (configurabile)
- **Task scaduti**: Email inviata ogni giorno finché non completato

### ✅ Destinatari
- **Responsabile Task**: Riceve sempre notifica
- **Responsabile Progetto**: Riceve notifica se diverso dal responsabile task

### ✅ Filtro per Tipo Soggetto
- **Interno**: Email abilitate (default)
- **Cliente**: Email disabilitate (default)
- **Fornitore**: Email disabilitate (default)

### ✅ Prevenzione Duplicati
- Indice univoco su: Task + Destinatario + Tipo + Data
- Controllo database prima di ogni invio

### ✅ Task Dipendenti Bloccati
Se un task scaduto ha task dipendenti, l'email include:
- Lista task bloccati
- Responsabili dei task bloccati
- Avviso che questi task non possono procedere

### ✅ Email Professionale
- Logo aziendale embedded
- Design responsive HTML
- Colori differenziati per urgenza:
  - **Arancione**: Task in scadenza domani
  - **Rosso**: Task scaduto
- Lingua: Inglese

## Installazione

### 1. Esegui Script SQL
```sql
-- Nel database Traceability_RS
USE [Traceability_RS];
GO
-- Esegui: CREATE_NPI_TASK_NOTIFICATIONS_TABLE.sql
```

### 2. Configurazione
Il file `npi_notifications_config.json` viene creato automaticamente con valori default se non esiste.

### 3. Integrazione in main.py
Il servizio viene avviato automaticamente all'avvio dell'applicazione (vedi sezione successiva).

## Utilizzo

### Avvio Automatico
Il servizio si avvia automaticamente quando si avvia l'applicazione principale.

```python
# In main.py è già integrato:
from npi.npi_auto_notifications import start_notification_service

# All'avvio
start_notification_service(npi_manager)
```

### Avvio Manuale
```python
from npi.npi_auto_notifications import start_notification_service, stop_notification_service

# Avvia servizio
service = start_notification_service(npi_manager, 'path/to/config.json')

# Ferma servizio
stop_notification_service()
```

### Configurazione Personalizzata

Modifica `npi_notifications_config.json`:

```json
{
  "notification_settings": {
    "enabled": true,          // true/false per abilitare/disabilitare
    "check_time": "09:30",    // Ora controllo (formato HH:MM)
    "include_logo": true      // Include logo nelle email
  },
  "recipient_types": {
    "Cliente": {
      "send_email": true      // Abilita email anche ai clienti
    }
  },
  "notification_types": {
    "task_due_tomorrow": {
      "days_before": 2        // Notifica 2 giorni prima
    }
  }
}
```

## Monitoraggio

### Query Statistiche

```sql
-- Statistiche giornaliere
SELECT * FROM vw_NpiTaskNotificationsStats
WHERE NotificationDate >= CAST(GETDATE()-7 AS DATE)
ORDER BY NotificationDate DESC;

-- Email fallite
SELECT 
    TaskProdottoID,
    RecipientName,
    RecipientEmail,
    ErrorMessage,
    SentDateTime
FROM NpiTaskNotifications
WHERE DeliveryStatus = 'Failed'
ORDER BY SentDateTime DESC;

-- Notifiche per task specifico
SELECT 
    NotificationType,
    NotificationDate,
    RecipientName,
    RecipientType,
    DeliveryStatus
FROM NpiTaskNotifications
WHERE TaskProdottoID = 123  -- ID del task
ORDER BY SentDateTime DESC;
```

### Log Applicazione

Il servizio logga in `traceability_rs.log`:

```
2026-01-14 08:00:00 | INFO | === INIZIO CONTROLLO NOTIFICHE NPI ===
2026-01-14 08:00:05 | INFO | Notifica TaskDueTomorrow inviata a Mario Rossi per task 456
2026-01-14 08:00:10 | INFO | === FINE CONTROLLO NOTIFICHE NPI ===
2026-01-14 08:00:10 | INFO | Totale email inviate: 5
```

## Struttura Email

### Header
- Logo aziendale
- Titolo "NPI Project Management System"

### Alert Box
- 🚨 **Rosso** per task scaduti
- ⚠️ **Arancione** per task in scadenza

### Dettagli Progetto
- Nome progetto
- Codice prodotto
- Responsabile progetto

### Dettagli Task
- Nome task
- Responsabile task
- Data inizio / scadenza
- Stato corrente

### Task Bloccati (se presenti)
- Lista task dipendenti
- Responsabili
- Nota su blocco

### Azioni Richieste
- Aggiornare stato task
- Coordinare con team
- Contattare project owner

## Troubleshooting

### Notifiche non inviate
1. Verificare `"enabled": true` in config
2. Controllare log per errori
3. Verificare connessione SMTP
4. Verificare email destinatari nel database

### Duplicati
- Il sistema previene automaticamente duplicati
- Controllo su tabella `NpiTaskNotifications`

### Email non ricevute
1. Verificare campo `Tipo` in tabella `Soggetti`
2. Verificare configurazione `recipient_types` nel JSON
3. Controllare spam/junk mail

## Manutenzione

### Pulizia Dati Vecchi
```sql
-- Elimina notifiche più vecchie di 90 giorni
DELETE FROM NpiTaskNotifications
WHERE NotificationDate < DATEADD(DAY, -90, GETDATE());
```

### Disabilitare Temporaneamente
```json
{
  "notification_settings": {
    "enabled": false  // Disabilita senza rimuovere configurazione
  }
}
```

## Note Tecniche

- **Thread separato**: Il servizio gira in background senza bloccare l'applicazione
- **Controllo ogni 30 secondi**: Verifica se è l'ora configurata
- **Esecuzione immediata**: Al primo avvio esegue subito un controllo
- **Gestione errori**: Continua anche in caso di errori singoli
- **Transazioni database**: Ogni notifica è registrata in transazione separata

## Sicurezza

- ✅ Prevenzione SQL Injection (uso SQLAlchemy ORM)
- ✅ Validazione tipo soggetto prima invio
- ✅ Gestione errori con logging
- ✅ Transazioni database atomiche
- ✅ No hardcoded credentials

## Performance

- Indici ottimizzati per query frequenti
- Batch processing per progetti
- Thread separato (non blocca UI)
- Session management efficiente
- Filtro early per task completati
