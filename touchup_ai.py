# -*- coding: utf-8 -*-
"""
touchup_ai.py — analisi AI (Ollama locale) della validità delle soluzioni touch-up.

Architettura credibile: i numeri (ricorrenze, riaperture, soluzioni distinte) sono
calcolati in modo DETERMINISTICO in touchup_report_gui; qui l'LLM SOLO interpreta
quei dati esatti — spiega quali soluzioni sembrano inefficaci e propone priorità.
Il modello gira in locale (nessun dato esce dalla rete aziendale).

Config da traceability_rs.dbo.settings (con default):
  ollama_server         -> server Ollama nel formato ip:port (default 192.168.10.72:11434)
  ollama_model_touchup  -> modello chat (default qwen2.5:14b-instruct)
"""
import json
import logging
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

DEFAULT_SERVER = '192.168.10.72:11434'   # ip:port
DEFAULT_MODEL = 'qwen2.5:14b-instruct'


def _setting(conn, attribute, default):
    try:
        cur = conn.cursor()
        cur.execute("SELECT [value] FROM traceability_rs.dbo.settings WHERE atribute = ?", (attribute,))
        row = cur.fetchone()
        cur.close()
        if row and row[0] and str(row[0]).strip():
            return str(row[0]).strip()
    except Exception as e:
        logger.warning(f"touchup_ai _setting({attribute}): {e}")
    return default


def _server_to_url(server):
    """Da 'ip:port' (o URL già completo) a URL base http://ip:port."""
    server = (server or DEFAULT_SERVER).strip().rstrip('/')
    if not server.startswith(('http://', 'https://')):
        server = 'http://' + server
    return server


def get_config(conn):
    """Ritorna (url_base, model). L'IP:porta viene da settings 'ollama_server'."""
    server = _setting(conn, 'ollama_server', DEFAULT_SERVER)
    model = _setting(conn, 'ollama_model_touchup', DEFAULT_MODEL)
    return _server_to_url(server), model


def _build_prompt(data, meta):
    """Costruisce (system, user) dal report. Dati già aggregati e deterministici."""
    k = data.get('kpi', {})
    pp = data.get('by_product_problem', [])
    period = f"{meta.get('date_from')} → {meta.get('date_to')}"

    lines = []
    for d in pp:
        lines.append(
            f"- Product: {d['product']} | Error: {d['problem']} | occurrences: {d['count']} | "
            f"reopenings: {d['reopened']} | distinct declared solutions: {d['n_solutions']} | "
            f"flag: {d['flag'] or 'none'}\n"
            f"    declared solutions: {d['solutions'] or '(none recorded)'}")
    table = "\n".join(lines) if lines else "(no product/error pairs in the period)"

    system = (
        "You are a senior quality engineer in an electronics (PCB) manufacturing plant, "
        "analyzing touch-up (rework) defect reports and the corrective actions declared by "
        "technicians. Your goal is to judge whether those declared solutions are actually "
        "EFFECTIVE, using ONLY the data provided. The key signal: if the same product+error "
        "keeps recurring despite solutions being declared, the corrective actions were likely "
        "ineffective or only declared, not truly implemented. The declared-solutions text may be "
        "in Romanian; interpret it. Do NOT invent numbers — the counts are exact. Be concise, "
        "factual and actionable.")
    user = (
        f"Period: {period}\n"
        f"KPIs: total reports {k.get('total')}, open {k.get('open')}, closed {k.get('closed')}, "
        f"reopened {k.get('reopened')}, avg first response {k.get('avg_resp_min')} min.\n\n"
        f"Recurrence by product x error (exact counts):\n{table}\n\n"
        "Provide, in English:\n"
        "1. The most critical product+error pairs (recurring despite solutions) and WHY.\n"
        "2. For those, judge whether the declared solutions look like genuine root-cause fixes "
        "or superficial/reworded/repeated non-fixes.\n"
        "3. Whether any solution text keeps repeating unchanged while the problem persists.\n"
        "4. A short prioritized action list (max 5) to actually stop the recurrence.\n"
        "Keep it under ~350 words. Base everything strictly on the data above.")
    return system, user


def analyze_recurrence(data, meta, url=None, model=None, timeout=180):
    """Chiama Ollama /api/chat e restituisce il testo dell'analisi. Solleva
    RuntimeError con messaggio chiaro in caso di problemi (server irraggiungibile,
    modello non caricato)."""
    url = _server_to_url(url or DEFAULT_SERVER)
    model = model or DEFAULT_MODEL
    system, user = _build_prompt(data, meta)
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "stream": False,
        "options": {"temperature": 0.2, "top_p": 0.9},
    }
    req = urllib.request.Request(
        f"{url}/api/chat",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode('utf-8'))
        msg = (body.get('message') or {}).get('content', '').strip()
        if not msg:
            raise RuntimeError("Risposta vuota dal modello.")
        return msg
    except urllib.error.HTTPError as e:
        detail = ''
        try:
            detail = e.read().decode('utf-8')[:300]
        except Exception:
            pass
        if e.code == 404:
            raise RuntimeError(
                f"Modello '{model}' non trovato su Ollama. Caricarlo con "
                f"'ollama pull {model}' sul server {url}. {detail}")
        raise RuntimeError(f"Errore Ollama HTTP {e.code}: {detail}")
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Server Ollama non raggiungibile ({url}): {e.reason}. "
            f"Verificare che Ollama sia in esecuzione e raggiungibile in rete.")
    except Exception as e:
        raise RuntimeError(f"Errore analisi AI: {e}")
