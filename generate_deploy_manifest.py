"""
Genera il file deploy_manifest.json nella directory di distribuzione.

Uso: python generate_deploy_manifest.py <dist_dir>
Esempio: python generate_deploy_manifest.py dist\DocumentManagement

Il manifest viene creato nella root di <dist_dir> e contiene l'elenco
completo dei file con le loro dimensioni. Il sistema di aggiornamento
dell'app usa questo file per verificare che tutti i file siano stati
trasferiti PRIMA di avviare l'update.
"""
import json
import os
import sys
from datetime import datetime


MANIFEST_FILENAME = 'deploy_manifest.json'


def generate_manifest(dist_dir: str) -> str:
    """Genera il manifest e lo salva nella directory specificata.
    
    Args:
        dist_dir: Percorso della directory di distribuzione
        
    Returns:
        Percorso del file manifest creato
    """
    dist_dir = os.path.normpath(dist_dir)
    
    if not os.path.isdir(dist_dir):
        print(f"ERRORE: Directory non trovata: {dist_dir}")
        sys.exit(1)
    
    files = []
    for root, dirs, filenames in os.walk(dist_dir):
        for filename in sorted(filenames):
            # Escludi il manifest stesso dalla lista
            if filename == MANIFEST_FILENAME:
                continue
            
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, dist_dir)
            size = os.path.getsize(full_path)
            files.append({
                'path': rel_path.replace('\\', '/'),  # Normalizza separatori
                'size': size
            })
    
    manifest = {
        'version': '1.0',
        'generated_at': datetime.now().isoformat(),
        'total_files': len(files),
        'files': files
    }
    
    manifest_path = os.path.join(dist_dir, MANIFEST_FILENAME)
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"Manifest generato: {manifest_path}")
    print(f"File registrati: {len(files)}")
    return manifest_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Uso: python {os.path.basename(__file__)} <dist_dir>")
        print(f"Esempio: python {os.path.basename(__file__)} dist\\DocumentManagement")
        sys.exit(1)
    
    generate_manifest(sys.argv[1])
