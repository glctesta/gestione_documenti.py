# Fix: Notifiche Email - Correzione Firma Metodo

## ❌ Problema

```
TypeError: EmailSender.send_email() got an unexpected keyword argument 'to_addresses'
```

## 🔍 Causa

Stavo usando `EmailSender` direttamente con parametri sbagliati. Il progetto ha già una funzione `send_email` in `utils.py` con una firma diversa.

## ✅ Soluzione

### Prima ❌

```python
from email_connector import EmailSender

email_sender = EmailSender()
success = email_sender.send_email(
    to_addresses=[email],      # ❌ Parametro sbagliato
    subject=subject,
    body_html=email_html,      # ❌ Parametro sbagliato
    from_address=from_email,   # ❌ Non supportato
    from_name=from_name        # ❌ Non supportato
)
```

### Dopo ✅

```python
from utils import send_email

send_email(
    recipients=[email],        # ✅ Corretto
    subject=subject,
    body=email_html,          # ✅ Corretto
    is_html=True              # ✅ Flag per HTML
)
```

## 📋 Firma Corretta `send_email` (utils.py)

```python
def send_email(
    recipients: List[str],     # Lista email destinatari
    subject: str,              # Oggetto email
    body: str,                 # Corpo (testo o HTML)
    smtp_host: str = "...",    # Host SMTP (default)
    smtp_port: int = 25,       # Porta SMTP (default)
    is_html: bool = False,     # Se True, body è HTML
    timeout: int = 15          # Timeout connessione
) -> None
```

## 🔄 Funzionamento

1. `send_email` usa `EmailSender` internamente
2. Configura automaticamente le credenziali
3. Gestisce la lista destinatari
4. Supporta HTML tramite flag `is_html=True`

## ⚠ Nota: "Per Conto" Non Supportato

La funzione `send_email` in `utils.py` **non supporta** l'invio "per conto" di un altro utente (from_address/from_name).

L'email sarà sempre inviata da: `Accounting@Eutron.it`

Se necessario modificare in futuro, si può:
1. Aggiungere parametri `from_address` e `from_name` a `send_email`
2. Passarli a `EmailSender.send_email()`

## ✅ Risultato

Le notifiche email ora vengono inviate correttamente usando la funzione standard del progetto.

---

**Data**: 23 Dicembre 2024  
**Versione**: 2.2.8.1  
**Stato**: ✅ Corretto - Email Funzionanti
