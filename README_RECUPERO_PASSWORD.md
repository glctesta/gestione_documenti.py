# Modulo Recupero Password

## Descrizione
Il modulo di recupero password consente agli utenti di recuperare le proprie credenziali di accesso tramite email, senza necessità di autenticazione.

## Accesso
**Menu:** Aiuto → Recupera Password

## Funzionalità

### Ricerca Multi-Criterio
L'utente può inserire uno o più dei seguenti campi per identificarsi:
- **ID Utente**: Username del sistema
- **Numero Badge**: Numero del badge aziendale (viene automaticamente normalizzato a 10 caratteri)
- **Nome e Cognome**: Nome completo del dipendente
- **Email Aziendale**: Indirizzo email lavorativo (WorkEmail)
- **CNP**: Codice Numerico Personale

### Normalizzazione Badge
Se il numero badge inserito ha meno di 10 caratteri, il sistema aggiunge automaticamente zeri davanti fino a raggiungere i 10 caratteri.

**Esempio:**
- Input: `123` → Output: `0000000123`
- Input: `45678` → Output: `0000045678`

### Invio Email
Se la ricerca ha successo e l'utente ha un indirizzo WorkEmail valido registrato, il sistema invia un'email professionale contenente:
- Logo aziendale incorporato
- Nome utente
- Numero badge
- CNP
- Nota di sicurezza (la password non viene inviata per motivi di sicurezza)

L'email viene formattata in HTML con design professionale e tradotta nella lingua corrente del sistema.

### Controllo Email
Se l'utente trovato NON ha un WorkEmail valido nel database, il sistema mostra un messaggio di errore:
> "Non è possibile recuperare la password perché nel database dei dipendenti NON è stata registrata una WorkEmail valida per questo utente."

## Query Database
Il modulo esegue la seguente query per ricercare l'utente:

```sql
SELECT 
    U.nomeuser, 
    a.WorkEmail, 
    e.EmployeeSurname + ' ' + e.EmployeeName AS EmployeeName, 
    b.NoBadge, 
    e.employeenid AS CNP 
FROM resetservices.dbo.tbuserkey U 
INNER JOIN employee.dbo.employees e ON e.employeeid = u.idanga 
INNER JOIN employee.dbo.EmployeeHireHistory H 
    ON h.employeeid = e.EmployeeId 
    AND h.employeerid = 2 
    AND h.EndWorkDate IS NULL 
INNER JOIN employee.dbo.EmployeeAddress A 
    ON a.EmployeeId = e.EmployeeId 
    AND a.dateout IS NULL
INNER JOIN employee.dbo.EmployeeBadgeHistory BH 
    ON bh.EmployeeHireHistoryId = h.EmployeeHireHistoryId 
    AND bh.dateout IS NULL
INNER JOIN employee.dbo.badges B 
    ON b.BadgeId = BH.BadgeID
WHERE u.nomeuser = IIF(@iduser IS NOT NULL, @iduser, u.nomeuser)
    AND u.nota = IIF(@EmployeeName IS NOT NULL, @EmployeeName, u.nota)
    AND b.NoBadge = IIF(@BadgeNo IS NOT NULL, @BadgeNo, b.NoBadge)
    AND a.workemail = IIF(@WorkEmail IS NOT NULL, @WorkEmail, a.workemail)
    AND e.EmployeeNID = IIF(@CNP IS NOT NULL, @CNP, e.EmployeeNID)
    AND u.nomeuser = IIF(@iduser IS NULL AND @WorkEmail IS NULL AND @EmployeeName IS NULL AND @BadgeNo IS NULL AND @CNP IS NULL, 'x', U.nomeuser)
```

## Installazione Traduzioni
Eseguire lo script SQL:
```
TRADUZIONI_RECUPERO_PASSWORD.sql
```

Questo script installa **140 traduzioni** (28 chiavi × 5 lingue) per:
- Italiano (it)
- Inglese (en)
- Rumeno (ro)
- Tedesco (de)
- Svedese (sv)

## File Coinvolti
- `password_recovery.py`: Modulo principale con la finestra di recupero
- `main.py`: Integrazione nel menu Help
- `TRADUZIONI_RECUPERO_PASSWORD.sql`: Script SQL per le traduzioni
- `logo.png`: Logo aziendale incorporato nell'email

## Note di Sicurezza
- Il modulo NON richiede autenticazione (è accessibile a tutti)
- La password dell'utente NON viene mai inviata via email
- L'email viene inviata solo all'indirizzo WorkEmail registrato nel database
- Per recuperare la password effettiva, l'utente deve contattare l'amministratore di sistema

## Dipendenze
- `utils.send_email()`: Per l'invio delle email
- `email_connector.EmailSender`: Gestore SMTP interno
- `logo.png`: Deve essere presente nella directory dell'applicazione

## Chiavi di Traduzione Principali
- `menu_recover_password`: Voce di menu
- `password_recovery_title`: Titolo finestra
- `password_recovery_instructions`: Istruzioni
- `password_recovery_email_sent`: Messaggio di successo
- `password_recovery_no_email`: Errore email mancante
- `email_*`: Traduzioni per il contenuto dell'email HTML

## Testing
1. Verificare che il logo.png esista nella directory dell'applicazione
2. Testare la ricerca con ciascun criterio singolarmente
3. Testare la ricerca con combinazioni di criteri
4. Verificare la normalizzazione del badge (input con meno di 10 caratteri)
5. Verificare il caso di email mancante (dovrebbe mostrare errore)
6. Verificare il caso di utente non trovato
7. Controllare la formattazione dell'email ricevuta in tutte le lingue
