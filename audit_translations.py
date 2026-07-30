# -*- coding: utf-8 -*-
"""Audit delle traduzioni: trova i testi che escono nella lingua sbagliata.

Confronta le chiavi usate nel codice (lang.get / _t_fmt / get_raw) con il
contenuto di dbo.AppTranslations e segnala tre problemi distinti:

  [A] chiave con testo di default ASSENTE in tutte le lingue
      -> a video compare sempre il default hardcoded (di norma italiano),
         qualunque sia la lingua impostata sul PC. E' il caso piu' comune.

  [B] chiave con SEGNAPOSTO POSIZIONALE ({0}, {}) chiamata come
      lang.get(chiave, 'default con {0}')
      -> LanguageManager.get(key, *args) usa il 2o argomento come fallback solo
         se la chiave MANCA; se la chiave esiste lo passa invece a .format(), e
         il segnaposto viene sostituito dal testo di default. Esempio reale:
         "Se pornește actualizarea la versiunea Avvio aggiornamento alla
         versione 2.4.2.7.9......". Va usato App._t_fmt().
      NB: i segnaposto NOMINALI ({qty}, {n}) non sono un problema: get() solleva
         KeyError e restituisce il template intatto, cosi' il .format(qty=...)
         del chiamante funziona. Non vengono segnalati.

  [C] chiave presente solo in ALCUNE lingue
      -> nelle lingue mancanti si ricade sul default o sulla chiave stessa.

Uso:
    python audit_translations.py                 # tutti i .py del progetto
    python audit_translations.py main.py         # solo un file
    python audit_translations.py --quiet         # solo il riepilogo

Exit code 1 se esistono problemi di tipo A o B (utile come gate pre-deploy).
"""
import argparse
import ast
import io
import os
import re
import sys

import pyodbc

from database_config import DatabaseConfig

# I testi tradotti contengono emoji e diacritiche (romeno, svedese): su console
# Windows cp1252 la stampa alzerebbe UnicodeEncodeError a metà report.
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8',
                                 errors='replace', line_buffering=True)

LANGS = ('it', 'en', 'ro', 'de', 'sv')
SKIP_DIRS = {'.venv', '.venv_old', 'venv', 'env', 'dist', 'build',
             '__pycache__', '.git', '.agent', '.claude', 'node_modules'}

# Segnaposto POSIZIONALE: {} oppure {0}, {1:02d}, ... (non {qty}, non {{)
_POSITIONAL_RE = re.compile(r'(?<!\{)\{(\d*)(?:![rsa])?(?::[^{}]*)?\}')


def has_positional_placeholder(text):
    """True se il testo contiene almeno un segnaposto posizionale."""
    return bool(text) and bool(_POSITIONAL_RE.search(text))


def iter_python_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, names in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for n in sorted(names):
                if n.endswith('.py'):
                    yield os.path.join(root, n)


def extract_calls(path):
    """Estrae (key, default, via, lineno) dalle chiamate di traduzione del file."""
    try:
        src = open(path, encoding='utf-8-sig', errors='surrogateescape').read()
        tree = ast.parse(src)
    except (SyntaxError, OSError) as e:
        print(f"  ATTENZIONE: {path} non analizzabile ({e})")
        return []

    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        attr = node.func.attr
        if attr not in ('get', '_t_fmt', 'get_raw'):
            continue
        if attr == 'get':
            # solo le get() sul language manager (self.lang, lang, self.lang_manager)
            try:
                owner = ast.unparse(node.func.value)
            except Exception:
                continue
            if 'lang' not in owner.lower():
                continue
        if not node.args or not isinstance(node.args[0], ast.Constant) \
                or not isinstance(node.args[0].value, str):
            continue
        key = node.args[0].value
        default = None
        if len(node.args) > 1 and isinstance(node.args[1], ast.Constant) \
                and isinstance(node.args[1].value, str):
            default = node.args[1].value
        out.append((key, default, attr, node.lineno))
    return out


def load_db_keys():
    """{chiave: set(lingue)} da dbo.AppTranslations."""
    conn = pyodbc.connect(DatabaseConfig().get_connection_string())
    try:
        cur = conn.cursor()
        cur.execute("SELECT LanguageCode, TranslationKey "
                    "FROM Traceability_rs.dbo.AppTranslations")
        have = {}
        for lc, key in cur.fetchall():
            if key:
                have.setdefault(key, set()).add((lc or '').lower())
        return have
    finally:
        conn.close()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Audit delle chiavi di traduzione rispetto a dbo.AppTranslations.')
    parser.add_argument('paths', nargs='*', default=None,
                        help='File o cartelle da analizzare (default: cartella del progetto)')
    parser.add_argument('--quiet', action='store_true',
                        help='Stampa solo il riepilogo finale')
    args = parser.parse_args(argv)

    base = os.path.dirname(os.path.abspath(__file__))
    paths = args.paths or [base]

    have = load_db_keys()
    print(f"Chiavi in AppTranslations: {len(have)}")

    calls = []
    files = 0
    for path in iter_python_files(paths):
        found = extract_calls(path)
        if found:
            files += 1
        rel = os.path.relpath(path, base)
        calls.extend((rel, *c) for c in found)
    print(f"File analizzati con traduzioni: {files} — chiamate: {len(calls)} — "
          f"chiavi distinte: {len(set(c[1] for c in calls))}")

    langs = set(LANGS)
    missing_all, risky, partial = {}, {}, {}
    for rel, key, default, via, line in calls:
        present = have.get(key, set()) & langs
        if default is not None and not present:
            missing_all.setdefault(key, (rel, line, default))
        if via == 'get' and present and has_positional_placeholder(default):
            risky.setdefault((key, rel, line), default)
        if present and present != langs:
            partial.setdefault(key, sorted(langs - present))

    def section(title, note, items):
        print()
        print(f"=== {title}: {len(items)} ===")
        print(f"    {note}")

    section('[A] chiavi con default assenti in TUTTE le lingue',
            'a video compare sempre il default hardcoded', missing_all)
    if not args.quiet:
        for key, (rel, line, default) in sorted(missing_all.items()):
            flag = '  [SEGNAPOSTO POSIZIONALE -> usare _t_fmt]' \
                if has_positional_placeholder(default) else ''
            print(f"  {key:<40} {rel}:{line}{flag}")
            print(f"      default: {default[:100]!r}")

    section('[B] segnaposto posizionale con lang.get(key, default)',
            'il default viene inserito al posto del valore: usare _t_fmt()', risky)
    if not args.quiet:
        for (key, rel, line), default in sorted(risky.items()):
            print(f"  {key:<40} {rel}:{line}")
            print(f"      default: {default[:100]!r}")

    section('[C] chiavi tradotte solo in alcune lingue',
            'nelle lingue mancanti si ricade sul default', partial)
    if not args.quiet:
        for key, miss in sorted(partial.items()):
            print(f"  {key:<40} mancano: {', '.join(miss)}")

    print()
    problems = len(missing_all) + len(risky)
    print(f"RIEPILOGO: A={len(missing_all)}  B={len(risky)}  C={len(partial)}")
    if problems:
        print("Esito: PROBLEMI DA CORREGGERE (A/B)")
        return 1
    print("Esito: OK (nessun problema di tipo A o B)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
