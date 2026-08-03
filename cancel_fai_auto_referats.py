# -*- coding: utf-8 -*-
"""
cancel_fai_auto_referats.py — annulla i REFERAT automatici FAI emessi per errore.

Motivo: fino al 30/07/2026 l'enforcement confrontava l'operatore per NOME
("Cognome Nome" dall'anagrafica contro "Nome Cognome" scritto dal login in
fai.FaiLogs.Operator): il confronto non era MAI vero, quindi il FAI compilato
non veniva riconosciuto e l'escalation arrivava sempre fino al referat
disciplinare. Le sanzioni cosi' generate non sono valide.

Cosa fa:
  1. Esporta un backup JSON di TUTTO cio' che tocca (righe disciplinari + PDF).
  2. Cancella da Employee.dbo.EmployeeDisciplinaryHistory i referat generati
     automaticamente dall'enforcement FAI (testo 'verificarea FAI obligatorie').
  3. Marca gli eventi in fai.FaiEnforcementLog: ReferatGenerated = 0 e nota di
     annullamento (il log resta, come traccia di audit).
  4. Sposta i PDF Referat_FAI_*.pdf da C:\\Temp in una sottocartella 'annullati'.

I numeri di documento gia' emessi in Employee.dbo.Registry NON vengono toccati
(sono un registro progressivo: si lascia il numero, senza il provvedimento).

Run:  python cancel_fai_auto_referats.py          (mostra cosa farebbe)
      python cancel_fai_auto_referats.py --apply  (esegue)
"""
import glob
import json
import os
import shutil
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from database_config import DatabaseConfig

REFERAT_MARKER = '%verificarea FAI obligatorie%'
PDF_DIR = r"C:\Temp"
PDF_PATTERN = "Referat_FAI_*.pdf"
BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backup_referat')


def _fetch_targets(cur):
    cur.execute("""
        SELECT EmployeeDisciplinaryHistoryId, EmployeeHireHistoryId, RegistroId,
               DocSavedOn, ExplicationNote, ArticoloLegaleId, SefID,
               DataAvvenimento, OraAvvenimento, DateSys
        FROM Employee.dbo.EmployeeDisciplinaryHistory
        WHERE ExplicationNote LIKE ?
        ORDER BY EmployeeDisciplinaryHistoryId
    """, REFERAT_MARKER)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def _fetch_log_events(cur):
    cur.execute("""
        SELECT EnforcementLogId, EventType, EmployeeName, EscalationLevel,
               OrderNumber, ShiftTime, DateIn
        FROM Traceability_RS.fai.FaiEnforcementLog
        WHERE ReferatGenerated = 1
        ORDER BY EnforcementLogId
    """)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def main(apply_changes: bool):
    conn = pyodbc.connect(DatabaseConfig().get_connection_string(), timeout=30)
    cur = conn.cursor()

    referats = _fetch_targets(cur)
    events = _fetch_log_events(cur)
    pdfs = glob.glob(os.path.join(PDF_DIR, PDF_PATTERN))

    print(f"Referat disciplinari da annullare : {len(referats)}")
    for r in referats:
        print(f"   #{r['EmployeeDisciplinaryHistoryId']} hhid={r['EmployeeHireHistoryId']} "
              f"registro={r['RegistroId']} del {r['DateSys']}")
    print(f"Eventi enforcement da smarcare    : {len(events)}")
    print(f"PDF referat da archiviare         : {len(pdfs)}")

    if not apply_changes:
        print("\n[DRY-RUN] Nessuna modifica eseguita. Rilanciare con --apply per applicare.")
        conn.close()
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(BACKUP_DIR, f'referat_fai_backup_{stamp}.json')
    with open(backup_path, 'w', encoding='utf-8') as fh:
        json.dump({'referats': referats, 'enforcement_events': events, 'pdfs': pdfs},
                  fh, ensure_ascii=False, indent=2, default=str)
    print(f"\nBackup salvato in: {backup_path}")

    ids = [r['EmployeeDisciplinaryHistoryId'] for r in referats]
    if ids:
        cur.execute(
            "DELETE FROM Employee.dbo.EmployeeDisciplinaryHistory "
            "WHERE EmployeeDisciplinaryHistoryId IN ({})".format(
                ",".join("?" * len(ids))), *ids)
        print(f"Referat disciplinari cancellati: {cur.rowcount}")

    annul_note = (' [ANNULLATO 30/07/2026: referat non valido - il FAI compilato '
                  'non veniva riconosciuto (confronto per nome)]')
    cur.execute("""
        UPDATE Traceability_RS.fai.FaiEnforcementLog
        SET ReferatGenerated = 0,
            Notes = LEFT(ISNULL(Notes, '') + ?, 500)
        WHERE ReferatGenerated = 1
    """, annul_note)
    print(f"Eventi enforcement smarcati: {cur.rowcount}")

    conn.commit()
    conn.close()

    if pdfs:
        dest = os.path.join(PDF_DIR, 'referat_annullati')
        os.makedirs(dest, exist_ok=True)
        moved = 0
        for p in pdfs:
            try:
                shutil.move(p, os.path.join(dest, os.path.basename(p)))
                moved += 1
            except Exception as e:
                print(f"   PDF non spostato {p}: {e}")
        print(f"PDF archiviati in {dest}: {moved}")

    print("\n[OK] Annullamento completato.")


if __name__ == '__main__':
    main(apply_changes='--apply' in sys.argv)
