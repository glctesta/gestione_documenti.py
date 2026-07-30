"""
Genera il file deploy_manifest.json nella directory di distribuzione.

Uso: python generate_deploy_manifest.py <dist_dir> [--workers N]
Esempi:
    python generate_deploy_manifest.py dist\\DocumentManagement
    python generate_deploy_manifest.py "T:\\...\\DocumentManagement" --workers 12

Il manifest viene creato nella root di <dist_dir> e contiene, per ogni file,
path, dimensione e hash SHA-256. Serve a due cose:
  1. l'app verifica PRIMA di aggiornare che tutti i file siano presenti con la
     dimensione attesa (previene upgrade da un trasferimento incompleto);
  2. l'updater dei client usa l'hash per copiare SOLO i file cambiati,
     confrontando l'hash del file locale senza rileggere il file dal server.

NB: va rigenerato a ogni deploy, sulla cartella di DESTINAZIONE e come ultimo
passo (dopo firma e copia). Non viene prodotto dalla build PyInstaller. Un
manifest della versione precedente fa fallire la verifica dimensioni e blocca
l'aggiornamento su tutti i client.

Su una share di rete la lettura e' dominata dalla latenza per file: l'hashing
viene fatto con piu' thread e il progresso e' stampato periodicamente, cosi' si
vede che il lavoro procede (in sequenziale sono ~31 ms per file, con 8 thread
~7 ms: su ~6000 file la differenza e' fra circa un minuto e una quindicina di
secondi).
"""
import argparse
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


MANIFEST_FILENAME = 'deploy_manifest.json'
DEFAULT_WORKERS = 8
PROGRESS_EVERY_SECONDS = 2.0


def _fmt_mb(n):
    return f"{n / 1024 / 1024:.1f} MB"


def _file_sha256(path: str) -> str:
    """SHA-256 del contenuto del file (a blocchi, per file grandi)."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def _collect_files(dist_dir):
    """Elenco (rel_path, full_path, size) dei file da registrare, ordinato."""
    out = []
    for root, _dirs, filenames in os.walk(dist_dir):
        for filename in sorted(filenames):
            if filename == MANIFEST_FILENAME:   # esclude il manifest stesso
                continue
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, dist_dir).replace('\\', '/')
            try:
                size = os.path.getsize(full_path)
            except OSError as e:
                print(f"  ATTENZIONE: {rel_path} non leggibile ({e}), ignorato")
                continue
            out.append((rel_path, full_path, size))
    out.sort(key=lambda t: t[0])
    return out


def generate_manifest(dist_dir: str, workers: int = DEFAULT_WORKERS) -> str:
    """Genera il manifest e lo salva nella directory specificata.

    Args:
        dist_dir: percorso della directory di distribuzione
        workers:  thread paralleli per l'hashing (utile su share di rete)

    Returns:
        percorso del file manifest creato
    """
    dist_dir = os.path.normpath(dist_dir)

    if not os.path.isdir(dist_dir):
        print(f"ERRORE: Directory non trovata: {dist_dir}")
        sys.exit(1)

    print(f"Cartella      : {dist_dir}")
    print("Scansione file in corso...", flush=True)
    t_scan = time.monotonic()
    collected = _collect_files(dist_dir)
    total = len(collected)
    total_bytes = sum(c[2] for c in collected)
    print(f"Trovati {total} file ({_fmt_mb(total_bytes)}) "
          f"in {time.monotonic() - t_scan:.1f}s")

    if not total:
        print("ERRORE: nessun file da registrare.")
        sys.exit(1)

    print(f"Calcolo SHA-256 con {workers} thread...", flush=True)
    files = [None] * total
    done = 0
    done_bytes = 0
    errors = []
    t0 = time.monotonic()
    last_print = t0

    def work(idx):
        rel_path, full_path, size = collected[idx]
        try:
            return idx, rel_path, size, _file_sha256(full_path), None
        except Exception as e:                      # file bloccato/illeggibile
            return idx, rel_path, size, None, str(e)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for idx, rel_path, size, sha, err in pool.map(work, range(total)):
            done += 1
            done_bytes += size
            if err:
                errors.append(f"{rel_path}: {err}")
            files[idx] = {'path': rel_path, 'size': size, 'sha256': sha}

            now = time.monotonic()
            if now - last_print >= PROGRESS_EVERY_SECONDS or done == total:
                elapsed = now - t0
                rate = done / elapsed if elapsed > 0 else 0
                eta = (total - done) / rate if rate > 0 else 0
                print(f"  {done}/{total} file  {_fmt_mb(done_bytes)}  "
                      f"{elapsed:.0f}s trascorsi  ETA {eta:.0f}s", flush=True)
                last_print = now

    # I file non hashati resterebbero con sha256=None: l'updater li tratterebbe
    # come "senza hash" e ricadrebbe sul confronto byte-a-byte solo per quelli.
    if errors:
        print(f"ATTENZIONE: {len(errors)} file non hashati (verranno confrontati "
              f"byte-a-byte dall'updater):")
        for e in errors[:10]:
            print(f"  {e}")
        if len(errors) > 10:
            print(f"  ... e altri {len(errors) - 10}")

    manifest = {
        'version': '2.0',
        'generated_at': datetime.now().isoformat(),
        'total_files': len(files),
        'files': files
    }

    manifest_path = os.path.join(dist_dir, MANIFEST_FILENAME)
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Manifest generato: {manifest_path}")
    print(f"File registrati: {len(files)} "
          f"({sum(1 for x in files if x['sha256'])} con hash) "
          f"in {time.monotonic() - t0:.0f}s")
    return manifest_path


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Genera deploy_manifest.json nella directory di distribuzione.')
    parser.add_argument('dist_dir',
                        help=r'Directory di distribuzione (es. dist\DocumentManagement)')
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS,
                        help=f'Thread paralleli per l\'hashing (default {DEFAULT_WORKERS}); '
                             'alzarlo su share di rete lente')
    args = parser.parse_args(argv)
    if args.workers < 1:
        parser.error('--workers deve essere >= 1')
    generate_manifest(args.dist_dir, args.workers)


if __name__ == '__main__':
    main()
