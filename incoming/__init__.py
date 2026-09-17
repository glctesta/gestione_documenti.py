# File: incoming/__init__.py
"""
incoming — Modulo "Ricezione": richieste incoming tra PC (WH incoming -> Ricezione).

Richieste di tipo MPN mancante/errato o P.O. mancante/quantita', con:
  - popup tra PC (tabella condivisa Traceability_RS.dbo.kit_popup_queue)
  - email e reminder ripetuti (configurabili per tipo richiesta)
  - escalation automatica per richieste rimaste pending
  - report mensile (claim cross-PC via email_job_coordinator)

Componenti:
  - incoming_db.py                : accesso dati (DDL, CRUD, statistiche)
  - incoming_setup.sql            : DDL idempotente + seed settings (da eseguire una volta)
  - add_incoming_translations.sql : traduzioni AppTranslations (it/en/ro/de/sv)
  - incoming_request_gui.py       : finestra invio richiesta (agente GUI)
  - incoming_solutions_gui.py     : finestra risposta (agente GUI)
  - incoming_confirm_gui.py       : finestra conferma (agente GUI)
  - incoming_workstation_config.py: ruoli receiver/sender per PC (agente Setup)
  - incoming_setup_gui.py         : finestra configurazione email/reminder (agente Setup)
  - incoming_monitor.py           : monitor popup/escalation/reminder (agente Monitor)
  - incoming_email.py             : report mensile + email (agente Monitor)
"""
