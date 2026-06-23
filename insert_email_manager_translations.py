# -*- coding: utf-8 -*-
"""Traduzioni per il gestore avanzato indirizzi email (settings_gui)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyodbc
from database_config import DatabaseConfig

TRANSLATIONS = [
    ('manage_email_addresses_button', '📧 Gestione Indirizzi Email', '📧 Manage Email Addresses',
     '📧 Gestionare Adrese Email', '📧 E-Mail-Adressen verwalten', '📧 Hantera e-postadresser'),
    ('email_addr_mgr_title', 'Gestione Indirizzi Email', 'Email Address Management',
     'Gestionare Adrese Email', 'E-Mail-Adressverwaltung', 'Hantering av e-postadresser'),
    ('email_addr_mgr_filter', 'Filtro chiave (atribute)', 'Key filter (attribute)',
     'Filtru cheie (atribute)', 'Schluesselfilter (Attribut)', 'Nyckelfilter (attribut)'),
    ('email_addr_mgr_key', 'Chiave contiene:', 'Key contains:', 'Cheia conține:',
     'Schluessel enthaelt:', 'Nyckel innehaaller:'),
    ('email_addr_mgr_load', 'Carica', 'Load', 'Incarca', 'Laden', 'Ladda'),
    ('email_addr_mgr_addresses', 'Indirizzi trovati', 'Addresses found', 'Adrese gasite',
     'Gefundene Adressen', 'Hittade adresser'),
    ('email_addr_mgr_col_email', 'Indirizzo email', 'Email address', 'Adresa email',
     'E-Mail-Adresse', 'E-postadress'),
    ('email_addr_mgr_col_count', 'N. righe', 'Rows', 'Nr. randuri', 'Zeilen', 'Rader'),
    ('email_addr_mgr_col_keys', 'Chiavi (atribute)', 'Keys (attribute)', 'Chei (atribute)',
     'Schluessel (Attribut)', 'Nycklar (attribut)'),
    ('email_addr_mgr_actions', "Azioni sull'indirizzo selezionato", 'Actions on selected address',
     'Actiuni pe adresa selectata', 'Aktionen fuer ausgewaehlte Adresse', 'Atgaerder paa vald adress'),
    ('email_addr_mgr_new', 'Nuovo indirizzo:', 'New address:', 'Adresa noua:', 'Neue Adresse:', 'Ny adress:'),
    ('email_addr_mgr_correct', '✏ Correggi su tutte', '✏ Correct in all', '✏ Corecteaza in toate',
     '✏ In allen korrigieren', '✏ Korrigera i alla'),
    ('email_addr_mgr_delete', '🗑 Elimina da tutte', '🗑 Delete from all', '🗑 Sterge din toate',
     '🗑 Aus allen loeschen', '🗑 Ta bort fraan alla'),
    ('email_addr_mgr_loaded', '{0} righe, {1} indirizzi distinti', '{0} rows, {1} distinct addresses',
     '{0} randuri, {1} adrese distincte', '{0} Zeilen, {1} eindeutige Adressen',
     '{0} rader, {1} unika adresser'),
    ('email_addr_mgr_select', 'Seleziona un indirizzo dalla lista.', 'Select an address from the list.',
     'Selectati o adresa din lista.', 'Waehlen Sie eine Adresse aus der Liste.', 'Vaelj en adress i listan.'),
    ('email_addr_mgr_invalid', 'Inserire un indirizzo email valido.', 'Enter a valid email address.',
     'Introduceti o adresa email valida.', 'Geben Sie eine gueltige E-Mail-Adresse ein.',
     'Ange en giltig e-postadress.'),
    ('email_addr_mgr_confirm_correct', 'Sostituire "{0}" con "{1}" in {2} righe?',
     'Replace "{0}" with "{1}" in {2} rows?', 'Inlocuiti "{0}" cu "{1}" in {2} randuri?',
     '"{0}" durch "{1}" in {2} Zeilen ersetzen?', 'Ersaett "{0}" med "{1}" i {2} rader?'),
    ('email_addr_mgr_corrected', 'Indirizzo aggiornato in {0} righe.', 'Address updated in {0} rows.',
     'Adresa actualizata in {0} randuri.', 'Adresse in {0} Zeilen aktualisiert.',
     'Adress uppdaterad i {0} rader.'),
    ('email_addr_mgr_confirm_delete', 'Eliminare "{0}" da {1} righe?', 'Delete "{0}" from {1} rows?',
     'Stergeti "{0}" din {1} randuri?', '"{0}" aus {1} Zeilen loeschen?', 'Ta bort "{0}" fraan {1} rader?'),
    ('email_addr_mgr_deleted', 'Indirizzo eliminato da {0} righe.', 'Address deleted from {0} rows.',
     'Adresa stearsa din {0} randuri.', 'Adresse aus {0} Zeilen geloescht.',
     'Adress borttagen fraan {0} rader.'),
    ('info_title', 'Info', 'Info', 'Info', 'Info', 'Info'),
    ('email_addr_mgr_addr_filter', 'Indirizzo contiene:', 'Address contains:', 'Adresa conține:',
     'Adresse enthaelt:', 'Adress innehaaller:'),
    ('email_addr_mgr_cooccur', 'Altri indirizzi nelle stesse chiavi', 'Other addresses in the same keys',
     'Alte adrese in aceleasi chei', 'Andere Adressen in denselben Schluesseln',
     'Andra adresser i samma nycklar'),
    ('email_addr_mgr_col_shared', 'Chiavi in comune', 'Shared keys', 'Chei comune',
     'Gemeinsame Schluessel', 'Gemensamma nycklar'),
    ('email_addr_mgr_shown', 'mostrati', 'shown', 'afisate', 'angezeigt', 'visade'),
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
    conn.commit(); conn.close()
    print(f"[OK] Email manager translations - Inserite: {ins}, Saltate: {skip}")


if __name__ == '__main__':
    main()
