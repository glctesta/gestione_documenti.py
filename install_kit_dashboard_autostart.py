# -*- coding: utf-8 -*-
"""
install_kit_dashboard_autostart.py — Registra il web server Kit Dashboard come
attività pianificata (Windows Task Scheduler) sul PC server (es. 192.168.10.72).

L'attività (modalità SYSTEM, SENZA login):
  - parte all'AVVIO del PC (BootTrigger, ritardo 1 min per rete/DB);
  - gira come account SYSTEM (nessun utente loggato necessario);
  - si RIAVVIA automaticamente in caso di crash (ogni 1 min, fino a 999 volte);
  - non ha limite di durata.

IMPORTANTE (SYSTEM non ha drive mappati come T:):
  - la lettura della pianificazione usa il percorso UNC in kit_server_config.json
    (`planning_path`, default \\\\192.168.10.110\\InternalApplications\\Planning);
  - l'account MACCHINA (es. PC72$) deve avere accesso in LETTURA a quella share
    (verificare con IT) e al DB.

Eseguire SUL PC SERVER, da un prompt **come Amministratore**:

    .venv\\Scripts\\python.exe install_kit_dashboard_autostart.py            # installa (SYSTEM/boot)
    .venv\\Scripts\\python.exe install_kit_dashboard_autostart.py --logon    # variante: al logon utente
    .venv\\Scripts\\python.exe install_kit_dashboard_autostart.py --remove   # rimuove
    .venv\\Scripts\\python.exe install_kit_dashboard_autostart.py --print    # stampa solo l'XML

Il web server poi è raggiungibile su http://<ip>:<porta>/produzione e /magazzino.
"""
import sys, io, os, getpass, tempfile, subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kit_dashboard import server_config

TASK_NAME = "KitDashboardServer"


def _command_and_args():
    """Comando da eseguire: exe --kit-web-server (frozen) o pythonw script (dev)."""
    base = server_config.app_base_dir()
    if getattr(sys, "frozen", False):
        return sys.executable, "--kit-web-server", base
    # dev: usa pythonw.exe (niente console) accanto a python.exe
    pyw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    if not os.path.isfile(pyw):
        pyw = sys.executable
    script = os.path.join(base, "kit_web_server.py")
    return pyw, f'"{script}"', base


def _build_xml(logon: bool = False):
    cmd, args, workdir = _command_and_args()
    if logon:
        # Variante: al logon dell'utente corrente (drive T: mappato disponibile)
        user = f"{os.environ.get('USERDOMAIN', '')}\\{getpass.getuser()}".strip("\\")
        trigger = f"<LogonTrigger><Enabled>true</Enabled><UserId>{user}</UserId></LogonTrigger>"
        principal = (f"<Principal id=\"Author\"><UserId>{user}</UserId>"
                     f"<LogonType>InteractiveToken</LogonType>"
                     f"<RunLevel>LeastPrivilege</RunLevel></Principal>")
    else:
        # Default: all'avvio del PC, come SYSTEM (nessun login necessario)
        trigger = "<BootTrigger><Enabled>true</Enabled><Delay>PT1M</Delay></BootTrigger>"
        principal = ("<Principal id=\"Author\"><UserId>S-1-5-18</UserId>"
                     "<RunLevel>HighestAvailable</RunLevel></Principal>")
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Kit Dashboard web server (auto-sync ogni 5 min)</Description>
  </RegistrationInfo>
  <Triggers>
    {trigger}
  </Triggers>
  <Principals>
    {principal}
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>999</Count>
    </RestartOnFailure>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Enabled>true</Enabled>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{cmd}</Command>
      <Arguments>{args}</Arguments>
      <WorkingDirectory>{workdir}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""


def install(logon: bool = False) -> str:
    """Crea (o sostituisce) la task. Ritorna un messaggio riepilogativo."""
    xml = _build_xml(logon=logon)
    mode = "LOGON utente" if logon else "SYSTEM / avvio PC"
    fd, path = tempfile.mkstemp(suffix=".xml")
    os.close(fd)
    with open(path, "w", encoding="utf-16") as f:
        f.write(xml)
    try:
        r = subprocess.run(["schtasks", "/Create", "/TN", TASK_NAME, "/XML", path, "/F"],
                           capture_output=True, text=True)
        out = (r.stdout or "").strip() or (r.stderr or "").strip()
        if r.returncode == 0:
            cfg = server_config.load_config()
            subprocess.run(["schtasks", "/Run", "/TN", TASK_NAME], capture_output=True, text=True)
            msg = (f"Task '{TASK_NAME}' creato e avviato ({mode}).\n"
                   f"Dashboard: http://{cfg['server_host_ip']}:{cfg['server_port']}/produzione\n\n"
                   f"Ricorda di aprire la porta nel firewall:\n"
                   f"netsh advfirewall firewall add rule name=\"KitDashboard {cfg['server_port']}\" "
                   f"dir=in action=allow protocol=TCP localport={cfg['server_port']}")
        else:
            msg = (f"ERRORE creazione task ({mode}).\n{out}\n\n"
                   f"Eseguire come AMMINISTRATORE.")
        print(msg)
        return msg
    finally:
        os.remove(path)


def remove() -> str:
    r = subprocess.run(["schtasks", "/Delete", "/TN", TASK_NAME, "/F"],
                       capture_output=True, text=True)
    msg = (r.stdout or "").strip() or (r.stderr or "").strip() or "Task rimosso."
    print(msg)
    return msg


if __name__ == "__main__":
    _logon = "--logon" in sys.argv
    if "--print" in sys.argv:
        print(_build_xml(logon=_logon))
    elif "--remove" in sys.argv:
        remove()
    else:
        install(logon=_logon)
