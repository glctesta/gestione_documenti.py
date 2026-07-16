# -*- coding: utf-8 -*-
"""
insert_password_recovery_other_translations.py
Traduzioni per il recupero password a favore di operatori SENZA email aziendale
(checkbox + pannello in password_recovery). 5 lingue. Idempotente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('recovery_for_other_checkbox',
     'Recupero per un operatore SENZA email aziendale (richiede autorizzazione)',
     'Recovery for an operator WITHOUT company email (requires authorization)',
     'Recuperare pentru un operator FĂRĂ email de companie (necesită autorizare)',
     'Wiederherstellung für einen Bediener OHNE Firmen-E-Mail (Autorisierung erforderlich)',
     'Återställning för en operatör UTAN företagsmejl (kräver behörighet)'),
    ('recovery_other_title',
     'Operatore senza email aziendale (mostra credenziali a schermo)',
     'Operator without company email (shows credentials on screen)',
     'Operator fără email de companie (afișează credențialele pe ecran)',
     'Bediener ohne Firmen-E-Mail (zeigt Zugangsdaten am Bildschirm)',
     'Operatör utan företagsmejl (visar inloggning på skärmen)'),
    ('recovery_other_userid', 'UserID:', 'UserID:', 'UserID:', 'UserID:', 'UserID:'),
    ('recovery_other_name', 'oppure Cognome e Nome:', 'or Surname and Name:',
     'sau Nume și Prenume:', 'oder Nachname und Vorname:', 'eller Efternamn och Namn:'),
    ('recovery_other_search', '🔍 Cerca credenziali', '🔍 Search credentials',
     '🔍 Caută credențiale', '🔍 Zugangsdaten suchen', '🔍 Sök inloggning'),
    ('recovery_other_col_employee', 'Dipendente', 'Employee', 'Angajat', 'Mitarbeiter', 'Anställd'),
    ('recovery_other_col_cdc', 'Reparto', 'Department', 'Departament', 'Abteilung', 'Avdelning'),
    ('recovery_other_col_subcdc', 'Sotto-reparto', 'Sub-department', 'Sub-departament',
     'Unterabteilung', 'Underavdelning'),
    ('recovery_other_col_function', 'Funzione', 'Function', 'Funcție', 'Funktion', 'Funktion'),
    ('recovery_other_col_user', 'UserID', 'UserID', 'UserID', 'UserID', 'UserID'),
    ('recovery_other_col_pass', 'Password', 'Password', 'Parolă', 'Passwort', 'Lösenord'),
    ('recovery_no_auth', 'Autorizzazione non disponibile.', 'Authorization not available.',
     'Autorizare indisponibilă.', 'Autorisierung nicht verfügbar.', 'Behörighet ej tillgänglig.'),
    ('recovery_not_authorized', 'Autorizzazione richiesta.', 'Authorization required.',
     'Autorizare necesară.', 'Autorisierung erforderlich.', 'Behörighet krävs.'),
    ('recovery_other_need_input', 'Inserire UserID oppure Cognome e Nome.',
     'Enter UserID or Surname and Name.', 'Introduceți UserID sau Nume și Prenume.',
     'UserID oder Nachname und Vorname eingeben.', 'Ange UserID eller Efternamn och Namn.'),
]

LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    ins = skip = 0
    for row in TRANSLATIONS:
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
    conn.commit()
    conn.close()
    print(f"[OK] Password recovery (other) translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
