# -*- coding: utf-8 -*-
"""
npi_commerciali_weekly_email.py — Email settimanale ai commerciali NPI.

Per ogni Commerciale (Soggetti IsCommercial=1) con AutoEmail=1 e una Email valida,
invia un riepilogo dei progetti NPI dei suoi clienti, suddivisi in:
  - Da chiudere  (Attivo, non in ritardo)
  - In ritardo   (Attivo, ScadenzaProgetto < oggi)
  - Chiusi
In copia (CC) gli indirizzi della setting 'Sys_email_npi_global_view'.

Pensato per essere schedulato dal Task Scheduler di Windows il VENERDÌ alle 17:00.

Uso:
  .venv\\Scripts\\python.exe npi_commerciali_weekly_email.py [--dry-run]

Spec: docs/NPI_Commerciali_Spec_v1.0.md
"""
import sys, io, os, argparse
from datetime import date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyodbc
from config_manager import ConfigManager
import utils

CC_SETTING = "Sys_email_npi_global_view"


def get_conn():
    cfg = ConfigManager(key_file="encryption_key.key", config_file="db_config.enc").load_config()
    return pyodbc.connect(
        f"DRIVER={cfg['driver']};SERVER={cfg['server']};DATABASE={cfg['database']};"
        f"UID={cfg['username']};PWD={cfg['password']};TrustServerCertificate=Yes"
    )


def get_commerciali_auto(cur):
    cur.execute("""
        SELECT SoggettoId, NomeSoggetto, Email
        FROM dbo.Soggetti
        WHERE IsCommercial = 1 AND AutoEmail = 1
          AND Email IS NOT NULL AND LTRIM(RTRIM(Email)) <> ''
        ORDER BY NomeSoggetto
    """)
    return [(r[0], r[1], r[2]) for r in cur.fetchall()]


def get_progetti_commerciale(cur, soggetto_id):
    """Progetti NPI dei clienti associati al commerciale, categorizzati."""
    cur.execute("""
        SELECT p.Cliente, p.CodiceProdotto, p.NomeProdotto, n.[Version],
               n.ScadenzaProgetto, n.StatoProgetto
        FROM dbo.CommercialeCliente cc
        INNER JOIN dbo.Prodotti p ON LTRIM(RTRIM(p.Cliente)) = cc.ClienteNome
        INNER JOIN dbo.ProgettiNPI n ON n.ProdottoID = p.ProdottoID AND n.DateOut IS NULL
        WHERE cc.SoggettoID = ?
        ORDER BY p.Cliente, n.ScadenzaProgetto
    """, (soggetto_id,))
    today = date.today()
    da_chiudere, in_ritardo, chiusi = [], [], []
    for r in cur.fetchall():
        cliente, cod, nome, ver, scad, stato = r
        row = {
            'cliente': cliente, 'codice': cod, 'nome': nome,
            'version': ver, 'scadenza': scad, 'stato': stato,
        }
        if (stato or '').strip().lower() == 'chiuso':
            chiusi.append(row)
        elif scad is not None and scad < today:
            in_ritardo.append(row)
        else:
            da_chiudere.append(row)
    return da_chiudere, in_ritardo, chiusi


def _fmt_date(d):
    return d.strftime('%d/%m/%Y') if d else '—'


def _section(title, rows, color):
    if not rows:
        return ""
    trs = []
    for r in rows:
        trs.append(
            f"<tr><td>{r['cliente'] or ''}</td><td>{r['codice'] or ''}</td>"
            f"<td>{r['nome'] or ''}</td><td>{r['version'] or ''}</td>"
            f"<td style='text-align:center'>{_fmt_date(r['scadenza'])}</td></tr>"
        )
    return f"""
    <h3 style="color:{color};margin:18px 0 6px;">{title} ({len(rows)})</h3>
    <table style="border-collapse:collapse;width:100%;font-size:13px;">
      <tr style="background:#1a5276;color:#fff;">
        <th style="padding:6px 8px;text-align:left;">Cliente</th>
        <th style="padding:6px 8px;text-align:left;">Codice</th>
        <th style="padding:6px 8px;text-align:left;">Prodotto</th>
        <th style="padding:6px 8px;text-align:left;">Ver.</th>
        <th style="padding:6px 8px;">Scadenza</th>
      </tr>
      {''.join(trs)}
    </table>"""


def build_html(nome_comm, da_chiudere, in_ritardo, chiusi):
    body = (f"<div style='font-family:Segoe UI,Arial,sans-serif;color:#333;max-width:760px;'>"
            f"<h2 style='color:#1a5276;'>Riepilogo settimanale progetti NPI</h2>"
            f"<p>Gentile <strong>{nome_comm}</strong>, di seguito la sintesi dei progetti NPI "
            f"dei tuoi clienti.</p>")
    body += _section("⛔ In ritardo", in_ritardo, "#c0392b")
    body += _section("🟠 Da chiudere", da_chiudere, "#e67e22")
    body += _section("✅ Chiusi", chiusi, "#27ae60")
    body += ("<p style='font-size:11px;color:#888;margin-top:24px;'>"
             "Email automatica settimanale — non rispondere a questo messaggio.</p></div>")
    return body


def run(dry_run: bool = False):
    """Esegue l'invio (o la simulazione con dry_run=True). Richiamabile anche
    dall'eseguibile frozen via flag --npi-weekly-email."""
    args = argparse.Namespace(dry_run=dry_run)
    conn = get_conn()
    cur = conn.cursor()

    try:
        cc = utils.get_email_recipients(conn, CC_SETTING)
    except Exception as e:
        print(f"ATTENZIONE: lettura CC {CC_SETTING} fallita: {e}")
        cc = []
    print(f"CC ({CC_SETTING}): {cc or '(nessuno)'}{' [DRY-RUN]' if args.dry_run else ''}")

    commerciali = get_commerciali_auto(cur)
    print(f"Commerciali con AutoEmail=1 ed email: {len(commerciali)}")

    inviate = 0
    for sid, nome, email in commerciali:
        da_chiudere, in_ritardo, chiusi = get_progetti_commerciale(cur, sid)
        tot = len(da_chiudere) + len(in_ritardo) + len(chiusi)
        if tot == 0:
            print(f"  - {nome}: nessun progetto, salto.")
            continue
        print(f"  - {nome} <{email}>: da_chiudere={len(da_chiudere)} "
              f"in_ritardo={len(in_ritardo)} chiusi={len(chiusi)}")
        if args.dry_run:
            continue
        try:
            html = build_html(nome, da_chiudere, in_ritardo, chiusi)
            utils.send_email(
                recipients=[email],
                subject=f"Riepilogo settimanale progetti NPI — {nome}",
                body=html,
                is_html=True,
                cc_emails=cc or None,
            )
            inviate += 1
        except Exception as e:
            print(f"    ERRORE invio a {email}: {e}")

    conn.close()
    print(f"Completato. Email inviate: {inviate}{' (DRY-RUN)' if args.dry_run else ''}")


def main():
    parser = argparse.ArgumentParser(description="Email settimanale commerciali NPI")
    parser.add_argument('--dry-run', action='store_true', help="Non invia, stampa solo il riepilogo")
    args = parser.parse_args()
    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
