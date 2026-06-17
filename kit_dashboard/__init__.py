"""
kit_dashboard — Dashboard web intranet per la preparazione dei kit di produzione.

Architettura: il web server (kit_web_server.py) gira come processo AUTONOMO
sul PC 192.168.10.72 (Scheduled Task al boot) e fa da sé il sync ogni 5 min.
Il programma desktop fa solo da watcher (alert se il server è down).

Componenti:
  - server_config : lettura/scrittura kit_server_config.json (dir dell'eseguibile)
  - planning      : lettura ora pianificata prima fase PTHM da T:\\Planning
  - eta           : stima minuti al completamento dei kit
  - sync_service  : ricalcolo dello snapshot in DB (usato dal web server)
  - controller    : watcher — ping /health + alert (popup KIT_PREP + email) se down
  - server_watcher: helper di health-check e alert con dedup atomico

Autostart server: install_kit_dashboard_autostart.py
Spec: docs/KitDashboard_WebServer_Spec_v1.0.md
"""
