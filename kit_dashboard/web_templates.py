# -*- coding: utf-8 -*-
"""
web_templates.py — Template Jinja2 (in rumeno) per la Kit Dashboard web.

Esposti come dict TEMPLATES per un jinja2.DictLoader (no file su disco →
nessun problema di bundling PyInstaller). Etichette in rumeno per i monitor
di reparto.
"""

STATUS_LABELS = {
    'WH_OPEN': 'Depozit – în pregătire',
    'WH_PARTIAL': 'Depozit – parțial (derogare)',
    'WH_CLOSED': 'Depozit – închis',
    'REOPENED': 'Redeschis (verificare eșuată)',
    'IN_PREFORMING': 'Gata pentru producție',
    'BLOCKED_MISSING_MATERIAL': 'Blocat – material lipsă',
    'RECEIVED_IN_PRODUCTION': 'Primit în producție',
    'COMPLETED': 'Finalizat',
}

_BASE = """
<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{% block head %}{% endblock %}
<title>{% block title %}Kit Dashboard{% endblock %}</title>
<style>
  :root{--accent:#1F497D;--ok:#27ae60;--warn:#e67e22;--err:#c0392b;--bg:#0f1622;--card:#16202e;}
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:'Segoe UI',Arial,sans-serif;background:var(--bg);color:#e8eef6;font-size:16px;}
  header{background:var(--accent);color:#fff;padding:12px 24px;display:flex;align-items:center;
         justify-content:space-between;gap:18px;flex-wrap:wrap;}
  header .title{font-size:1.5rem;font-weight:700;}
  nav a{color:#cfe0f5;text-decoration:none;margin-right:16px;font-weight:600;}
  nav a.active,nav a:hover{color:#fff;text-decoration:underline;}
  .meta{font-size:.85rem;opacity:.9;}
  .btn{background:#fff;color:var(--accent);border:none;border-radius:18px;padding:6px 16px;
       font-weight:700;cursor:pointer;font-size:.85rem;}
  .btn:hover{background:#e8f0fb;}
  main{padding:18px 24px 60px;}
  h2{color:#9cc1ee;margin:22px 0 10px;font-size:1.15rem;}
  table{width:100%;border-collapse:collapse;margin-bottom:18px;background:var(--card);
        border-radius:8px;overflow:hidden;}
  th{background:#1d2c40;color:#cfe0f5;text-align:left;padding:9px 12px;font-size:.85rem;
     text-transform:uppercase;letter-spacing:.4px;}
  td{padding:9px 12px;border-bottom:1px solid #243246;}
  tr:last-child td{border-bottom:none;}
  .prog{background:#243246;border-radius:6px;height:18px;width:160px;overflow:hidden;display:inline-block;vertical-align:middle;}
  .prog > span{display:block;height:100%;background:var(--ok);}
  .pct{font-size:.8rem;margin-left:6px;opacity:.85;}
  .badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.8rem;font-weight:700;}
  .b-ok{background:#143d2a;color:#5fe0a0;}
  .b-warn{background:#3d2f12;color:#f0b86b;}
  .b-err{background:#3d1717;color:#ff8080;}
  .b-p0{background:#5a1f1f;color:#ffb0b0;}
  .miss-badge{background:#3d1717;color:#ff9a9a;border-radius:12px;padding:2px 10px;font-weight:700;
              text-decoration:none;display:inline-block;}
  .miss-badge:hover{background:#551f1f;}
  a.order{color:#9cc1ee;font-weight:700;text-decoration:none;}
  a.order:hover{text-decoration:underline;}
  tr.late{background:#2a1414;}
  tr.late.blink{animation:blink 1.1s steps(2,start) infinite;}
  @keyframes blink{50%{background:#5a1f1f;}}
  .filters{margin:8px 0 14px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;}
  .filters input,.filters select{background:#16202e;color:#e8eef6;border:1px solid #2c3e57;
      border-radius:6px;padding:7px 10px;font-size:.9rem;}
  .empty{opacity:.6;font-style:italic;padding:10px 2px;}
  .ico{font-weight:700;}
  .ico.yes{color:var(--ok);} .ico.no{color:var(--err);}
  footer{opacity:.5;font-size:.75rem;padding:14px 24px;}
</style>
</head>
<body>
<header>
  <div class="title">📦 {% block htitle %}Kit Dashboard{% endblock %}</div>
  <nav>
    <a href="/magazzino" class="{{ 'active' if page=='mag' else '' }}">Depozit</a>
    <a href="/produzione" class="{{ 'active' if page=='prod' else '' }}">Producție</a>
  </nav>
  <div style="display:flex;align-items:center;gap:14px;">
    <span class="meta">Actualizat la {{ snapshot_time or '—' }}</span>
    <form method="post" action="/refresh" style="margin:0;">
      <input type="hidden" name="next" value="{{ request_path }}">
      <button class="btn" type="submit">↻ Reîmprospătează acum</button>
    </form>
  </div>
</header>
<main>{% block content %}{% endblock %}</main>
<footer>Kit Production Dashboard · TraceabilityRS · date sincronizate la fiecare 5 minute</footer>
{% block scripts %}{% endblock %}
</body>
</html>
"""

_MAGAZZINO = """
{% extends "base" %}
{% block title %}Depozit – Pregătire Kit{% endblock %}
{% block htitle %}Depozit – Pregătire Kit{% endblock %}
{% block head %}<meta http-equiv="refresh" content="60">{% endblock %}
{% block content %}
<h2>Comenzi în pregătire ({{ rows|length }})</h2>
{% if not rows %}<div class="empty">Nicio comandă în pregătire.</div>{% endif %}
{% if rows %}
<table>
  <tr><th>Comandă</th><th>Produs</th><th>Cant.</th><th>Stare</th><th>Avansare</th>
      <th>Coduri lipsă</th><th>ETA</th><th>Gata la</th><th>Ultima activitate</th></tr>
  {% for r in rows %}
  <tr class="{{ 'late blink' if r.is_late else '' }}">
    <td>{% if r.priority and r.priority>0 %}<span class="badge b-p0">P{{ r.priority }}</span> {% endif %}
        <a class="order" href="/ordine/{{ r.order_number }}">{{ r.order_number }}</a></td>
    <td>{{ r.product_code or '—' }}</td>
    <td>{{ r.order_qty|qty }}</td>
    <td>{{ r.kit_status|status }}</td>
    <td><span class="prog"><span style="width:{{ r.pct_complete }}%"></span></span>
        <span class="pct">{{ r.items_done }}/{{ r.items_total }} ({{ r.pct_complete }}%)</span></td>
    <td>{% if r.missing_codes>0 %}<a class="miss-badge" href="/ordine/{{ r.order_number }}">{{ r.missing_codes }}</a>{% else %}—{% endif %}</td>
    <td>{{ ('~%d min'|format(r.eta_minutes)) if r.eta_minutes else '—' }}</td>
    <td>{{ r.eta_ready_at|hm }}</td>
    <td>{{ r.last_activity_date|dt }}</td>
  </tr>
  {% endfor %}
</table>
{% endif %}
{% endblock %}
"""

_PRODUZIONE = """
{% extends "base" %}
{% block title %}Producție – Recepție Kit{% endblock %}
{% block htitle %}Producție – Recepție Kit{% endblock %}
{% block head %}<meta http-equiv="refresh" content="60">{% endblock %}
{% block content %}

<h2>✅ Kituri gata de preluare ({{ ready|length }})</h2>
{% if not ready %}<div class="empty">Niciun kit gata în acest moment.</div>{% endif %}
{% if ready %}
<table id="tbl-ready">
  <tr><th>Comandă</th><th>Produs</th><th>Cant.</th><th>Pregătit (depozit)</th></tr>
  {% for r in ready %}
  <tr data-search="{{ (r.order_number ~ ' ' ~ (r.product_code or ''))|lower }}">
    <td><a class="order" href="/ordine/{{ r.order_number }}">{{ r.order_number }}</a></td>
    <td>{{ r.product_code or '—' }}</td>
    <td>{{ r.order_qty|qty }}</td>
    <td>{{ r.last_activity_date|dt }}</td>
  </tr>
  {% endfor %}
</table>
{% endif %}

<h2>⏳ Următoarele kituri ({{ next_rows|length }})</h2>
<div class="filters">
  <input id="flt" type="text" placeholder="Caută comandă / produs…" oninput="filterRows()">
  <select id="mode" onchange="filterRows()">
    <option value="all">Toate</option>
    <option value="late">Doar întârziate</option>
    <option value="incomplete">Doar incomplete</option>
  </select>
</div>
{% if not next_rows %}<div class="empty">Niciun kit în pregătire.</div>{% endif %}
{% if next_rows %}
<table id="tbl-next">
  <tr><th>Comandă</th><th>Produs</th><th>Stare</th><th>Avansare</th>
      <th>Coduri lipsă</th><th>ETA</th><th>Planificat PTHM</th></tr>
  {% for r in next_rows %}
  <tr class="{{ 'late blink' if r.is_late else '' }}"
      data-search="{{ (r.order_number ~ ' ' ~ (r.product_code or ''))|lower }}"
      data-late="{{ 1 if r.is_late else 0 }}" data-incomplete="{{ 1 if r.is_incomplete else 0 }}">
    <td>{% if r.priority and r.priority>0 %}<span class="badge b-p0">P{{ r.priority }}</span> {% endif %}
        <a class="order" href="/ordine/{{ r.order_number }}">{{ r.order_number }}</a></td>
    <td>{{ r.product_code or '—' }}</td>
    <td>{{ r.kit_status|status }}</td>
    <td><span class="prog"><span style="width:{{ r.pct_complete }}%"></span></span>
        <span class="pct">{{ r.pct_complete }}%</span></td>
    <td>{% if r.missing_codes>0 %}<a class="miss-badge" href="/ordine/{{ r.order_number }}">{{ r.missing_codes }}</a>{% else %}—{% endif %}</td>
    <td>{{ ('~%d min'|format(r.eta_minutes)) if r.eta_minutes else '—' }}</td>
    <td>{{ r.planned_start|dt }}</td>
  </tr>
  {% endfor %}
</table>
{% endif %}

<h2>🗂 Istoric {% if search %}(căutare: "{{ search }}"){% else %}(ultimele {{ days }} zile){% endif %}</h2>
<form class="filters" method="get" action="/produzione">
  <input type="text" name="q" value="{{ search }}" placeholder="Caută în istoric (comandă / produs)…">
  <button class="btn" type="submit">Caută</button>
  {% if search %}<a class="btn" href="/produzione" style="text-decoration:none;">✕ Resetează</a>{% endif %}
</form>
{% if not history %}<div class="empty">Niciun rezultat.</div>{% endif %}
{% if history %}
<table>
  <tr><th>Comandă</th><th>Produs</th><th>Planificat PTHM</th><th>Gata la</th>
      <th>Finalizat</th><th>În termen</th><th>Complet</th><th>Stare</th></tr>
  {% for h in history %}
  <tr>
    <td><a class="order" href="/ordine/{{ h.order_number }}">{{ h.order_number }}</a></td>
    <td>{{ h.product_code or '—' }}</td>
    <td>{{ h.planned_start|dt }}</td>
    <td>{{ h.ready_date|dt }}</td>
    <td>{{ h.completed_date|dt }}</td>
    <td>{{ h.was_on_time|yesno }}</td>
    <td>{{ h.was_complete|yesno }}</td>
    <td>{{ h.final_status|status }}</td>
  </tr>
  {% endfor %}
</table>
{% endif %}
{% endblock %}
{% block scripts %}
<script>
function filterRows(){
  var q=(document.getElementById('flt').value||'').toLowerCase();
  var mode=document.getElementById('mode').value;
  document.querySelectorAll('#tbl-next tr[data-search]').forEach(function(tr){
    var ok = tr.getAttribute('data-search').indexOf(q)>=0;
    if(mode==='late' && tr.getAttribute('data-late')!=='1') ok=false;
    if(mode==='incomplete' && tr.getAttribute('data-incomplete')!=='1') ok=false;
    tr.style.display = ok ? '' : 'none';
  });
}
</script>
{% endblock %}
"""

_ORDINE = """
{% extends "base" %}
{% block title %}Comandă {{ order_number }}{% endblock %}
{% block htitle %}Comandă {{ order_number }}{% endblock %}
{% block content %}
<p style="margin-bottom:14px;"><a class="order" href="/produzione">&larr; Înapoi la Producție</a></p>
{% if d.snap %}
  <h2>{{ order_number }} · {{ d.snap.product_code or '—' }} ·
      {{ d.snap.kit_status|status }}
      {% if d.snap.is_late %}<span class="badge b-err">ÎNTÂRZIAT</span>{% endif %}</h2>
  <p class="meta">Avansare {{ d.snap.items_done }}/{{ d.snap.items_total }}
     ({{ d.snap.pct_complete }}%) · Coduri lipsă: {{ d.snap.missing_codes }}
     {% if d.snap.planned_start %}· Planificat PTHM: {{ d.snap.planned_start|dt }}{% endif %}</p>
{% elif d.history %}
  <h2>{{ order_number }} · {{ d.history.product_code or '—' }} · {{ d.history.final_status|status }}
      (istoric)</h2>
{% else %}
  <div class="empty">Comanda nu a fost găsită în dashboard.</div>
{% endif %}

<h2>Materiale lipsă ({{ d.missing|length }})</h2>
{% if not d.missing %}<div class="empty">Niciun material lipsă.</div>{% endif %}
{% if d.missing %}
<table>
  <tr><th>Cod material</th><th>Necesar</th><th>Prelevat</th><th>Lipsă</th><th>Stare</th></tr>
  {% for m in d.missing %}
  <tr><td>{{ m.material_code }}</td><td>{{ m.qty_required|qty }}</td>
      <td>{{ m.qty_picked|qty }}</td>
      <td><span class="badge b-err">{{ m.qty_missing|qty }}</span></td>
      <td>{{ m.pick_status }}</td></tr>
  {% endfor %}
</table>
{% endif %}

{% if d.requests %}
<h2>Cereri material deschise ({{ d.requests|length }})</h2>
<table>
  <tr><th>Material</th><th>Cant.</th><th>Fază</th><th>Stare</th><th>Data</th><th>Motivație</th></tr>
  {% for r in d.requests %}
  <tr><td>{{ r.material_code }}</td><td>{{ r.qty_requested|qty }}</td>
      <td>{{ r.requesting_phase }}</td><td>{{ r.wh_status }}</td>
      <td>{{ r.request_date|dt }}</td><td>{{ r.note or '—' }}</td></tr>
  {% endfor %}
</table>
{% endif %}
{% endblock %}
"""

TEMPLATES = {
    'base': _BASE,
    'magazzino': _MAGAZZINO,
    'produzione': _PRODUZIONE,
    'ordine': _ORDINE,
}
