# -*- coding: utf-8 -*-
"""
insert_password_recovery_dest_translations.py
Traduzioni per l'invio via email (all'indirizzo fornito) delle credenziali degli
operatori senza email aziendale. Aggiorna anche il testo del pulsante di ricerca.
5 lingue. Idempotente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

# Chiavi nuove (insert se mancanti)
NEW = [
    ('recovery_other_dest_email', 'Invia a (email):', 'Send to (email):', 'Trimite la (email):',
     'Senden an (E-Mail):', 'Skicka till (e-post):'),
    ('recovery_other_dest_required',
     'Inserire un indirizzo email valido a cui inviare le credenziali.',
     'Enter a valid email address to send the credentials to.',
     'Introduceți o adresă de email validă pentru trimiterea datelor de autentificare.',
     'Geben Sie eine gültige E-Mail-Adresse für den Versand der Zugangsdaten ein.',
     'Ange en giltig e-postadress att skicka inloggningsuppgifterna till.'),
    ('recovery_other_email_sent', 'Credenziali inviate a: {0}', 'Credentials sent to: {0}',
     'Datele de autentificare au fost trimise la: {0}', 'Zugangsdaten gesendet an: {0}',
     'Inloggningsuppgifter skickade till: {0}'),
    ('recovery_other_email_error', 'Invio email non riuscito', 'Email sending failed',
     'Trimiterea emailului a eșuat', 'E-Mail-Versand fehlgeschlagen', 'E-postutskick misslyckades'),
]

# Chiavi da AGGIORNARE al nuovo testo (il pulsante ora cerca e invia)
UPDATE = [
    ('recovery_other_search', '🔍 Cerca e invia credenziali', '🔍 Search and send credentials',
     '🔍 Caută și trimite datele', '🔍 Suchen und Zugangsdaten senden', '🔍 Sök och skicka inloggning'),
]

LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    ins = skip = upd = 0
    for row in NEW:
        key = row[0]
        for i, lang in enumerate(LANGS):
            cur.execute("SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                        "WHERE LanguageCode = ? AND TranslationKey = ?", (lang, key))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO Traceability_rs.dbo.AppTranslations "
                            "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                            (lang, key, row[i + 1]))
                ins += 1
            else:
                skip += 1
    for row in UPDATE:
        key = row[0]
        for i, lang in enumerate(LANGS):
            cur.execute("UPDATE Traceability_rs.dbo.AppTranslations SET TranslationValue = ? "
                        "WHERE LanguageCode = ? AND TranslationKey = ?", (row[i + 1], lang, key))
            if cur.rowcount == 0:
                cur.execute("INSERT INTO Traceability_rs.dbo.AppTranslations "
                            "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                            (lang, key, row[i + 1]))
                ins += 1
            else:
                upd += 1
    conn.commit()
    conn.close()
    print(f"[OK] Password recovery (dest email) - Inserite: {ins}, Aggiornate: {upd}, Saltate: {skip}")


if __name__ == '__main__':
    main()
