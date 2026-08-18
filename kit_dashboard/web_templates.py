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
  tr.postponed{background:#3d2f12;}
  .alert{border-radius:6px;padding:10px 14px;margin:12px 0;font-size:.9rem;}
  .alert.ok{background:#143d2a;color:#5fe0a0;}
  .alert.err{background:#3d1717;color:#ff8080;}
  .postpone-bar{background:#1d2c40;border:1px solid #2c3e57;border-radius:8px;padding:12px 16px;margin:14px 0;display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end;}
  .postpone-bar label{display:flex;flex-direction:row;align-items:center;font-size:.8rem;color:#cfe0f5;gap:6px;white-space:nowrap;}
  .postpone-bar input,.postpone-bar select,.postpone-bar textarea{background:#16202e;color:#e8eef6;border:1px solid #2c3e57;border-radius:6px;padding:5px 8px;font-size:.9rem;}
  .postpone-bar textarea{min-width:180px;min-height:32px;height:32px;resize:vertical;}
  .postpone-bar button{align-self:flex-end;}
  .postpone-bar-hidden{display:none;}
  .postpone-bar-visible{display:block;}
  .order-check{transform:scale(1.2);}
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

{% if error %}
<div class="alert err">
  {% if error == 'missing' %}Completați toate câmpurile și selectați cel puțin o comandă.{% endif %}
  {% if error == 'reason' %}Motiv amânare invalid.{% endif %}
  {% if error == 'auth' %}Autentificare eșuată sau permisiune insuficientă.{% endif %}
</div>
{% endif %}
{% if saved %}
<div class="alert ok">{{ saved }} comandă/comenzi amânată/e cu succes.</div>
{% endif %}

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
  <a class="btn" href="/posticipi" style="margin-left:auto;">Kituri amânate</a>
</div>
<form method="post" action="/posponi" id="postpone-form" class="postpone-bar-hidden" onsubmit="return collectOrders()">
  <input type="hidden" name="orders" id="orders-hidden">
  <div class="postpone-bar">
    <label>Motiv amânare
      <select name="reason_code" required>
        <option value="">— alege —</option>
        <option value="MISSING_COMPONENTS">Lipsă componente</option>
        <option value="DOCUMENTATION_PROBLEMS">Probleme documentație</option>
        <option value="TECHNICAL_PROBLEMS">Probleme tehnice</option>
        <option value="OTHER_URGENT">Amânat pentru alte urgențe</option>
      </select>
    </label>
    <label>Explicație extinsă
      <textarea name="reason_text" required placeholder="Descriere detaliată…"></textarea>
    </label>
    <label>Zile
      <input type="number" name="days" min="1" required>
    </label>
    <label>Utilizator
      <input type="text" name="user_id" required placeholder="User">
    </label>
    <label>Parolă
      <input type="password" name="password" required placeholder="Parolă">
    </label>
    <button class="btn" type="submit">OK</button>
  </div>
</form>
{% if not next_rows %}<div class="empty">Niciun kit în pregătire.</div>{% endif %}
{% if next_rows %}
<table id="tbl-next">
  <tr><th><input type="checkbox" id="check-all" title="Selectează toate"></th><th>Comandă</th><th>Produs</th><th>Stare</th><th>Avansare</th>
      <th>Coduri lipsă</th><th>ETA</th><th>Planificat PTHM</th></tr>
  {% for r in next_rows %}
  <tr class="{% if r.postponed_days %}postponed{% elif r.is_late %}late blink{% endif %}"
      data-search="{{ (r.order_number ~ ' ' ~ (r.product_code or ''))|lower }}"
      data-late="{{ 1 if r.is_late else 0 }}" data-incomplete="{{ 1 if r.is_incomplete else 0 }}">
    <td><input type="checkbox" value="{{ r.order_number }}" class="order-check"></td>
    <td>{% if r.priority and r.priority>0 %}<span class="badge b-p0">P{{ r.priority }}</span> {% endif %}
        <a class="order" href="/ordine/{{ r.order_number }}">{{ r.order_number }}</a></td>
    <td>{{ r.product_code or '—' }}</td>
    <td>{% if r.postponed_days %}Amânat {{ r.postponed_days }} zile{% else %}{{ r.kit_status|status }}{% endif %}</td>
    <td><span class="prog"><span style="width:{{ r.pct_complete }}%"></span></span>
        <span class="pct">{{ r.pct_complete }}%</span></td>
    <td>{% if r.missing_codes>0 %}<a class="miss-badge" href="/ordine/{{ r.order_number }}">{{ r.missing_codes }}</a>{% else %}—{% endif %}</td>
    <td>{{ ('~%d min'|format(r.eta_minutes)) if r.eta_minutes else '—' }}</td>
    <td>{{ r.planned_start|dt }}</td>
  </tr>
  {% endfor %}
</table>
{% endif %}

<h2>✅ Kituri primite în producție ({{ received|length }})</h2>
{% if not received %}<div class="empty">Niciun kit încă recepționat.</div>{% endif %}
{% if received %}
<table>
  <tr><th>Comandă</th><th>Primit la</th><th>Recepționat de</th></tr>
  {% for r in received %}
  <tr>
    <td><a class="order" href="/ordine/{{ r.order_number }}">{{ r.order_number }}</a></td>
    <td>{{ r.received_date|dt }}</td>
    <td>Recepționat de {{ r.user_name or '—' }}</td>
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
function updatePostponeBar(){
  var any=document.querySelectorAll('.order-check:checked').length>0;
  var bar=document.getElementById('postpone-form');
  if(bar){
    bar.classList.remove('postpone-bar-hidden','postpone-bar-visible');
    bar.classList.add(any?'postpone-bar-visible':'postpone-bar-hidden');
  }
}
var checkAll=document.getElementById('check-all');
if(checkAll){
  checkAll.addEventListener('change',function(){
    document.querySelectorAll('.order-check').forEach(function(cb){cb.checked=checkAll.checked;});
    updatePostponeBar();
  });
}
document.querySelectorAll('.order-check').forEach(function(cb){
  cb.addEventListener('change',updatePostponeBar);
});
function collectOrders(){
  var checked=document.querySelectorAll('.order-check:checked');
  if(checked.length===0){
    alert('Selectați cel puțin o comandă.');
    return false;
  }
  document.getElementById('orders-hidden').value=Array.from(checked).map(function(cb){return cb.value;}).join(',');
  return true;
}
</script>
{% endblock %}
"""

_POSTICIPATI = """
{% extends "base" %}
{% block title %}Kituri amânate{% endblock %}
{% block htitle %}Kituri amânate{% endblock %}
{% block content %}
<p style="margin-bottom:14px;"><a class="order" href="/produzione">&larr; Înapoi la Producție</a></p>

{% if error %}
<div class="alert err">
  {% if error == 'missing' %}Completați toate câmpurile și selectați cel puțin o comandă.{% endif %}
  {% if error == 'auth' %}Autentificare eșuată sau permisiune insuficientă.{% endif %}
  {% if error == 'notfound' %}Comanda nu a fost găsită.{% endif %}
</div>
{% endif %}
{% if saved %}
<div class="alert ok">{{ saved }} comandă/comenzi actualizată/e.</div>
{% endif %}

<h2>⏸ Kituri amânate ({{ rows|length }})</h2>
{% if not rows %}<div class="empty">Niciun kit amânat în acest moment.</div>{% endif %}
{% if rows %}
<form method="post" action="/gestione_posticipi" id="posticipi-form" onsubmit="return collectPosticipi()">
  <input type="hidden" name="orders" id="orders-hidden">
  <input type="hidden" name="azione" id="azione-hidden">
  <div class="postpone-bar">
    <label>Zile noi
      <input type="number" name="days" id="days-input" min="1">
    </label>
    <label>Utilizator
      <input type="text" name="user_id" required placeholder="User">
    </label>
    <label>Parolă
      <input type="password" name="password" required placeholder="Parolă">
    </label>
    <button class="btn" type="button" onclick="setAzione('riattiva')">Riattiva</button>
    <button class="btn" type="button" onclick="setAzione('modifica')">Modifică zile</button>
  </div>

  <table id="tbl-posticipi">
    <tr><th><input type="checkbox" id="check-all" title="Selectează toate"></th><th>Comandă</th><th>Produs</th>
        <th>Motiv</th><th>Zile</th><th>Amânat de</th><th>Amânat la</th><th>Expiră la</th></tr>
    {% for r in rows %}
    <tr>
      <td><input type="checkbox" value="{{ r.order_number }}" class="order-check"></td>
      <td><a class="order" href="/ordine/{{ r.order_number }}">{{ r.order_number }}</a></td>
      <td>{{ r.product_code or '—' }}</td>
      <td>{{ r.reason_label }}</td>
      <td>{{ r.days }}</td>
      <td>{{ r.postponed_by or '—' }}</td>
      <td>{{ r.postponed_at|dt }}</td>
      <td>{{ r.expires_at|dt }}</td>
    </tr>
    {% endfor %}
  </table>
</form>
{% endif %}
{% endblock %}
{% block scripts %}
<script>
var checkAll=document.getElementById('check-all');
if(checkAll){
  checkAll.addEventListener('change',function(){
    document.querySelectorAll('.order-check').forEach(function(cb){cb.checked=checkAll.checked;});
  });
}
function collectPosticipi(){
  var checked=document.querySelectorAll('.order-check:checked');
  if(checked.length===0){
    alert('Selectați cel puțin o comandă.');
    return false;
  }
  document.getElementById('orders-hidden').value=Array.from(checked).map(function(cb){return cb.value;}).join(',');
  return true;
}
function setAzione(azione){
  document.getElementById('azione-hidden').value=azione;
  var days=document.getElementById('days-input').value;
  if(azione==='modifica' && (!days || parseInt(days)<1)){
    alert('Introduceți un număr valid de zile.');
    return;
  }
  document.getElementById('posticipi-form').submit();
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

<h2>Materiale kit PTH ({{ d.materials|length }})</h2>
{% if not d.materials %}<div class="empty">Niciun material.</div>{% endif %}
{% if d.materials %}
<table>
  <tr><th>HU</th><th>Cod</th><th>Descriere</th><th>Prelevat</th><th>Verificat</th></tr>
  {% for m in d.materials %}
  <tr><td>{{ m.hu }}</td><td>{{ m.material_code }}</td><td>{{ m.descr }}</td>
      <td>{{ m.qty_picked|qty }}</td>
      <td>{% if m.qty_verified %}<span style="color:#0a7d28;font-weight:bold;">{{ m.qty_verified|qty }}</span>{% else %}{{ m.qty_verified|qty }}{% endif %}</td></tr>
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
    'posticipi': _POSTICIPATI,
    'ordine': _ORDINE,
}
