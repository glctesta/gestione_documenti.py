# -*- coding: utf-8 -*-
"""
install_scrap_reminder_task.py — Registra il sollecito validazione scorie/rientri
(scrap_validation_reminder.py) come attività pianificata del Windows Task Scheduler,
in esecuzione RIPETUTA ogni 30 minuti.

L'attività (default: SYSTEM, senza login):
  - parte ogni giorno e si RIPETE ogni 30 min per 24h (quindi di fatto sempre);
  - gira come SYSTEM (nessun utente loggato necessario) — la connessione DB usa
    UID/PWD da db_config.enc (SQL auth) e l'SMTP è un host diretto, quindi non
    servono drive mappati; la WorkingDirectory è impostata per leggere
    encryption_key.key / db_config.enc;
  - limite di durata per run PT10M (lo script termina in pochi secondi);
  - se un'istanza è ancora attiva, la nuova viene ignorata (IgnoreNew).

Lo script è idempotente e ha claim atomico anti-duplicato: eseguirlo spesso è sicuro.

Eseguire da un prompt **come Amministratore**, con il python del progetto:

    .venv\\Scripts\\python.exe install_scrap_reminder_task.py            # installa (SYSTEM)
    .venv\\Scripts\\python.exe install_scrap_reminder_task.py --logon    # variante: al logon utente
    .venv\\Scripts\\python.exe install_scrap_reminder_task.py --minutes 60  # intervallo custom
    .venv\\Scripts\\python.exe install_scrap_reminder_task.py --remove   # rimuove
    .venv\\Scripts\\python.exe install_scrap_reminder_task.py --print    # stampa solo l'XML
"""
import sys, io, os, getpass, tempfile, subprocess, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TASK_NAME = "ScrapValidationReminder"
SCRIPT_NAME = "scrap_validation_reminder.py"


def _command_and_args():
    """pythonw.exe (niente console) + percorso dello script; WorkingDirectory = app dir."""
    base = os.path.dirname(os.path.abspath(__file__))
    pyw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    if not os.path.isfile(pyw):
        pyw = sys.executable
    script = os.path.join(base, SCRIPT_NAME)
    return pyw, f'"{script}"', base


def _build_xml(logon: bool = False, minutes: int = 30):
    cmd, args, workdir = _command_and_args()
    interval = f"PT{max(1, int(minutes))}M"
    if logon:
        user = f"{os.environ.get('USERDOMAIN', '')}\\{getpass.getuser()}".strip("\\")
        principal = (f"<Principal id=\"Author\"><UserId>{user}</UserId>"
                     f"<LogonType>InteractiveToken</LogonType>"
                     f"<RunLevel>LeastPrivilege</RunLevel></Principal>")
    else:
        principal = ("<Principal id=\"Author\"><UserId>S-1-5-18</UserId>"
                     "<RunLevel>HighestAvailable</RunLevel></Principal>")
    # CalendarTrigger giornaliero + Repetition ogni N min per 24h (StartBoundary in
    # passato: la task si arma comunque e ripete per tutta la giornata, ogni giorno).
    trigger = (
        "<CalendarTrigger>"
        "<StartBoundary>2024-01-01T06:00:00</StartBoundary>"
        "<Enabled>true</Enabled>"
        f"<Repetition><Interval>{interval}</Interval><Duration>P1D</Duration>"
        "<StopAtDurationEnd>false</StopAtDurationEnd></Repetition>"
        "<ScheduleByDay><DaysInterval>1</DaysInterval></ScheduleByDay>"
        "</CalendarTrigger>"
    )
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Sollecito validazione scorie/rientri pendenti (ogni {minutes} min)</Description>
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
    <ExecutionTimeLimit>PT10M</ExecutionTimeLimit>
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


def install(logon: bool = False, minutes: int = 30) -> str:
    xml = _build_xml(logon=logon, minutes=minutes)
    mode = "LOGON utente" if logon else "SYSTEM"
    fd, path = tempfile.mkstemp(suffix=".xml")
    os.close(fd)
    with open(path, "w", encoding="utf-16") as f:
        f.write(xml)
    try:
        r = subprocess.run(["schtasks", "/Create", "/TN", TASK_NAME, "/XML", path, "/F"],
                           capture_output=True, text=True)
        out = (r.stdout or "").strip() or (r.stderr or "").strip()
        if r.returncode == 0:
            subprocess.run(["schtasks", "/Run", "/TN", TASK_NAME], capture_output=True, text=True)
            msg = (f"Task '{TASK_NAME}' creato e avviato ({mode}, ogni {minutes} min).\n"
                   f"Prerequisiti: eseguire add_returnmaterials_reminder_columns.sql e "
                   f"popolare la setting 'Sys_email_valida_restituzioni'.")
        else:
            msg = f"ERRORE creazione task ({mode}).\n{out}\n\nEseguire come AMMINISTRATORE."
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
    parser = argparse.ArgumentParser(description="Installer task sollecito validazione scorie")
    parser.add_argument("--logon", action="store_true", help="Esegui al logon utente invece che come SYSTEM")
    parser.add_argument("--minutes", type=int, default=30, help="Intervallo di ripetizione in minuti (default 30)")
    parser.add_argument("--remove", action="store_true", help="Rimuove la task")
    parser.add_argument("--print", action="store_true", dest="print_xml", help="Stampa solo l'XML")
    a = parser.parse_args()
    if a.print_xml:
        print(_build_xml(logon=a.logon, minutes=a.minutes))
    elif a.remove:
        remove()
    else:
        install(logon=a.logon, minutes=a.minutes)
