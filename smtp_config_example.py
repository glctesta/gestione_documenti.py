# Configurazione SMTP per invio email FAI
# Rinomina questo file in smtp_config.py e inserisci le tue credenziali

SMTP_CONFIG = {
    'server': 'smtp.office365.com',  # o smtp.gmail.com per Gmail
    'port': 587,
    'user': 'noreply@tuodominio.com',  # Email mittente
    'password': 'tua_password_smtp',  # Password o App Password
    'use_tls': True
}

# Per Gmail:
# 1. Attiva "App meno sicure" o usa "App Password"
# 2. server: 'smtp.gmail.com'
# 3. port: 587

# Per Office 365:
# 1. Usa le credenziali Office 365
# 2. server: 'smtp.office365.com'
# 3. port: 587
