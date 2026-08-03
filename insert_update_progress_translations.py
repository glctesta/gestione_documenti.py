# -*- coding: utf-8 -*-
"""
insert_update_progress_translations.py
Chiavi di traduzione per:
  - i messaggi di avanzamento mostrati durante la preparazione di un
    aggiornamento all'avvio (splash + finestra "preparazione aggiornamento"),
  - il blocco dell'eliminazione di un'associazione ordine vendita/produzione
    gia' spedita (orders/match_production_orders_window.py).

Idempotente: salta le chiavi gia' presenti. Run: python insert_update_progress_translations.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from database_config import DatabaseConfig

# (key, it, en, ro, de, sv)
TRANSLATIONS = [
    # ── Avanzamento preparazione aggiornamento ───────────────────────────────
    ('update_prep_step_start',
     'Avvio della preparazione...', 'Starting preparation...',
     'Se începe pregătirea...', 'Vorbereitung wird gestartet...',
     'Förberedelsen startar...'),
    ('update_prep_step_updater',
     'Copia del programma di aggiornamento dal server...',
     'Copying the update program from the server...',
     'Se copiază programul de actualizare de pe server...',
     'Updater wird vom Server kopiert...',
     'Uppdateringsprogrammet kopieras från servern...'),
    ('update_prep_step_verify',
     'Verifica dei file della nuova versione sul server...',
     'Checking the new version files on the server...',
     'Se verifică fișierele noii versiuni de pe server...',
     'Dateien der neuen Version auf dem Server werden geprüft...',
     'Filerna för den nya versionen kontrolleras på servern...'),
    ('update_prep_step_done',
     'Preparazione completata.', 'Preparation completed.',
     'Pregătire finalizată.', 'Vorbereitung abgeschlossen.',
     'Förberedelsen klar.'),
    ('splash_update_verify',
     'Nuova versione {0} disponibile: verifica dei file ({1}s)...',
     'New version {0} available: checking files ({1}s)...',
     'Versiune nouă {0} disponibilă: se verifică fișierele ({1}s)...',
     'Neue Version {0} verfügbar: Dateien werden geprüft ({1}s)...',
     'Ny version {0} tillgänglig: filerna kontrolleras ({1}s)...'),
    ('splash_update_prepare',
     'Preparazione aggiornamento alla versione {0}...',
     'Preparing the update to version {0}...',
     'Se pregătește actualizarea la versiunea {0}...',
     'Update auf Version {0} wird vorbereitet...',
     'Uppdatering till version {0} förbereds...'),
    ('splash_resume_startup',
     'Ripresa del caricamento...', 'Resuming startup...',
     'Se reia încărcarea...', 'Startvorgang wird fortgesetzt...',
     'Uppstarten återupptas...'),

    # ── Eliminazione associazione bloccata ───────────────────────────────────
    ('cannot_delete',
     'Eliminazione non possibile', 'Deletion not possible',
     'Ștergere imposibilă', 'Löschen nicht möglich', 'Borttagning inte möjlig'),
    ('shipment', 'Spedizione', 'Shipment', 'Expediere', 'Sendung', 'Leverans'),
    ('assoc_delete_blocked_generic',
     "Impossibile eliminare l'associazione: è già utilizzata da spedizioni "
     "o regole di spedizione.",
     'The association cannot be deleted: it is already used by shipments '
     'or shipping rules.',
     'Asocierea nu poate fi ștearsă: este deja folosită de expedieri '
     'sau reguli de expediere.',
     'Die Zuordnung kann nicht gelöscht werden: Sie wird bereits von Sendungen '
     'oder Versandregeln verwendet.',
     'Kopplingen kan inte tas bort: den används redan av leveranser '
     'eller leveransregler.'),
    ('assoc_delete_blocked_shipped',
     "L'associazione è già stata spedita e non può essere eliminata.",
     'The association has already been shipped and cannot be deleted.',
     'Asocierea a fost deja expediată și nu poate fi ștearsă.',
     'Die Zuordnung wurde bereits versendet und kann nicht gelöscht werden.',
     'Kopplingen har redan skickats och kan inte tas bort.'),
    ('assoc_delete_blocked_pallets',
     'Pallet confermati: {0} (quantità totale {1})',
     'Confirmed pallets: {0} (total quantity {1})',
     'Paleți confirmați: {0} (cantitate totală {1})',
     'Bestätigte Paletten: {0} (Gesamtmenge {1})',
     'Bekräftade pallar: {0} (total kvantitet {1})'),
    ('assoc_delete_blocked_rules',
     'Regole di spedizione collegate: {0}. Eliminarle prima dalla finestra '
     'dei report ordini.',
     'Linked shipping rules: {0}. Delete them first from the orders report window.',
     'Reguli de expediere legate: {0}. Ștergeți-le mai întâi din fereastra '
     'de rapoarte comenzi.',
     'Verknüpfte Versandregeln: {0}. Löschen Sie sie zuerst im Fenster '
     'der Auftragsberichte.',
     'Kopplade leveransregler: {0}. Ta bort dem först i orderrapportfönstret.'),
]

LANGS = ('it', 'en', 'ro', 'de', 'sv')


def main():
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    cur = conn.cursor()
    inserted = skipped = 0
    for row in TRANSLATIONS:
        key = row[0]
        for i, lang in enumerate(LANGS):
            val = row[i + 1]
            cur.execute(
                "SELECT COUNT(*) FROM Traceability_rs.dbo.AppTranslations "
                "WHERE LanguageCode = ? AND TranslationKey = ?",
                (lang, key),
            )
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "INSERT INTO Traceability_rs.dbo.AppTranslations "
                    "(LanguageCode, TranslationKey, TranslationValue) VALUES (?, ?, ?)",
                    (lang, key, val),
                )
                inserted += 1
            else:
                skipped += 1
    conn.commit()
    conn.close()
    print(f"[OK] Update progress / assoc delete translations - Inserite: {inserted}, "
          f"Saltate (gia' presenti): {skipped}")


if __name__ == '__main__':
    main()
