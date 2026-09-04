# -*- coding: utf-8 -*-
"""
email_job_coordinator.py
Coordinatore centralizzato per gli invii email/report automatici.

Fornisce lock cross-PC, abilitazione/disabilitazione e log dei job automatici
usando la tabella Traceability_RS.dbo.AutomaticEmailJobs.
"""
import logging

logger = logging.getLogger(__name__)


CREATE_JOBS_TABLE_SQL = """
IF OBJECT_ID('Traceability_RS.dbo.AutomaticEmailJobs', 'U') IS NULL
CREATE TABLE Traceability_RS.dbo.AutomaticEmailJobs (
    JobName              VARCHAR(100)  NOT NULL PRIMARY KEY,
    DisplayName          NVARCHAR(255) NOT NULL,
    FunctionName         VARCHAR(200)  NULL,
    ModulePath           VARCHAR(255)  NULL,
    Description          NVARCHAR(MAX) NULL,
    Timing               NVARCHAR(500) NULL,
    RecipientsSettingKey VARCHAR(100)  NULL,
    IsEnabled            BIT           NOT NULL DEFAULT 1,
    LastRunAt            DATETIME      NULL,
    LastRunStatus        VARCHAR(50)   NULL,
    LastRunMessage       NVARCHAR(500) NULL,
    NextRunAt            DATETIME      NULL,
    LockUntil            DATETIME      NULL,
    CreatedAt            DATETIME      NOT NULL DEFAULT GETDATE(),
    UpdatedAt            DATETIME      NOT NULL DEFAULT GETDATE()
)
"""


# Job predefiniti inseriti automaticamente alla prima apertura della form.
# Stessi valori di create_automatic_email_jobs.sql. I record esistenti non vengono toccati.
# Tuple: (JobName, DisplayName, FunctionName, ModulePath, Description, Timing, RecipientsSettingKey)
DEFAULT_JOBS = [
    ('purchasing_reminder',
     'Reminder acquisti materiali indiretti',
     'check_and_send_purchasing_reminder',
     'indirect_materials_stock_data.py',
     'Invia reminder agli acquisti per le richieste di riordino non confermate.',
     'Lun-Sab 10:00',
     'sys_email_acquista_indiretti'),
    ('indirect_reorder',
     'Riordino materiali indiretti sotto scorta',
     'check_and_send_reorder',
     'indirect_materials_stock_data.py',
     "Invia un'unica email giornaliera con i materiali indiretti sotto la scorta minima.",
     'Lun-Sab 07:30',
     'Sys_email_reorder_indirect_materials'),
    ('fqc_shift_1530_2330',
     'Report FQC fine turno',
     'run_fqc_shift_1530 / run_fqc_shift_2330',
     'fqc_email.py',
     'Invia riepilogo verifiche FQC fine turno alle 15:30 e 23:30.',
     'Lun-Sab 15:30 e 23:30',
     'Sys_check_final_product'),
    ('fails_daily_email',
     'Report giornaliero FAIL boards',
     'run_fails_daily_email',
     'fails_daily_email.py',
     'Report Excel e PDF sui FAIL boards del giorno/mese/anno.',
     'Tutti i giorni lavorativi 07:00',
     'Sys_Fail_report'),
    ('missing_alloy_check',
     'Avviso codici PTHM senza dato alloy',
     'run_missing_alloy_check',
     'material_consumption_report.py',
     'Avviso sui codici PTHM senza dato alloy.',
     'Lun-Sab 08:05',
     'Sys_missing_data_alloy'),
    ('plan_alert_escalation',
     'Escalation alert piano produzione',
     'check_and_escalate',
     'plan_alert_escalation.py',
     'Escalation per alert piano produzione non giustificati entro i tempi previsti.',
     'Ogni ~60 min 07:00-18:00 e 22:00-23:59',
     'Sys_email_control_plan'),
    ('plan_responsibles_daily',
     'Email giornaliera responsabili piano',
     'send_daily_responsibles_email',
     'plan_responsibles.py',
     'Email ai responsabili con discrepanze e urgenze del piano.',
     'Giorni lavorativi RO 08:00',
     'Sys_email_responsabili_piano'),
    ('stale_clients_report',
     'Report client con versione obsoleta',
     'send_stale_clients_email',
     'stale_clients_report.py',
     "Email con l'elenco dei PC che non hanno aggiornato l'applicazione.",
     'Giorni lavorativi 08:00',
     'Sys_stale_clients_email'),
    ('fai_enforcement',
     'FAI enforcement / escalation',
     'run_shift_check / process_pending_escalations / run_planning_based_enforcement',
     'fai_enforcement.py',
     'Invio referat PDF e email per FAI enforcement/escalation.',
     'Ogni 60 sec (continuo)',
     'Sys_email_fai_enforcement'),
    ('fai_autocheck',
     'Notifiche preventive FAI da PlanningMachine',
     'run_autocheck_cycle',
     'fai_autocheck.py',
     'Notifiche preventive FAI generate dalla pianificazione macchine.',
     'Ogni 30 min',
     'Sys_email_fai_autocheck'),
    ('weekly_npi_overview',
     'NPI Overview settimanale',
     '_send_weekly_npi_overview',
     'main.py',
     'Report Excel + grafico con overview settimanale progetti NPI.',
     'Lunedi 09:00',
     'Sys_email_general_napi'),
    ('weekly_overtime_unauthorized',
     'Report straordinari non autorizzati',
     'send_weekly_unauthorized_overtime_email',
     'overtime/overtime_manager.py',
     'Report settimanale degli straordinari non ancora autorizzati.',
     'Lunedi 09:00',
     'Sys_email_overtimeNotAuth'),
    ('monthly_overtime_report',
     'Report mensile straordinari approvati',
     'generate_and_send_monthly_overtime_report',
     'overtime/overtime_manager.py',
     'Report mensile degli straordinari approvati.',
     'Primo giorno lavorativo del mese 09:00',
     'Sys_email_overtimeMonthlyReport'),
    ('monthly_report_generic',
     'Report mensile generic verification',
     '_monthly_report_worker',
     'main.py',
     'Report Excel mensile generic verification.',
     'Primo giorno lavorativo del mese 09:00',
     'Sys_Verify_check_fail'),
    ('kanban_refill_check',
     'Richiesta refill KanBan',
     '_kanban_refill_check_worker',
     'main.py',
     'Email di richiesta refill KanBan con allegato Excel.',
     'Ogni 8 ore',
     'Sys_email_KanBanRefill'),
    ('weekly_visitor_email',
     'Lista visitatori programmata settimana',
     '_check_weekly_visitor_email',
     'main.py',
     'Email settimanale con la lista dei visitatori programmata da lunedi a domenica.',
     'Lunedi (orario variabile)',
     'Sys_email_management'),
    ('label_scrap_shift_end',
     'Scarti etichette fine turno',
     '_process_shift_end',
     'label_scrap_monitor.py',
     'Email con PDF/Excel degli scarti etichette 15 min prima della fine turno.',
     '07:15 / 15:15 / 23:15',
     'sys_email_labelScrap'),
    ('shift_handover_unconfirmed',
     'Alert cambio turno non confermato',
     'ShiftHandoverMonitor',
     'shift_handover_monitor.py',
     'Alert se un cambio turno non viene confermato entro 60 min.',
     'Continuo (postazione specifica)',
     'sys_email_Allert_Shift'),
    ('npi_auto_notifications',
     'Notifiche consolidate task NPI',
     '_check_and_send_notifications',
     'npi/npi_auto_notifications.py',
     'Notifiche consolidate per task NPI in scadenza/scaduti.',
     'Ogni giorno lavorativo ~08:00',
     None),
    ('npi_commerciali_weekly',
     'Riepilogo settimanale progetti NPI per commerciali',
     'run',
     'npi_commerciali_weekly_email.py',
     'Riepilogo settimanale dei progetti NPI destinato ai commerciali.',
     'Venerdi 17:00',
     'Sys_email_npi_global_view'),
    ('touchup_no_response',
     'Escalation Touch-Up senza risposta',
     'escalate_unanswered_reports',
     'touchup_logic.py',
     'Escalation per segnalazioni Touch-Up senza risposta.',
     'Ogni 5 min',
     'Sys_email_TouchUp_warning'),
    ('kit_dashboard_alert',
     'Alert web server Kit Dashboard down',
     'send_alert',
     'kit_dashboard/server_watcher.py',
     'Email se il web server della Kit Dashboard non risponde.',
     'Continuo',
     'Sys_email_Kit_materiali'),
    ('scrap_validation_reminder',
     'Sollecito validazione scorie/rientri pendenti',
     'main',
     'scrap_validation_reminder.py',
     'Sollecito per scorie/rientri pendenti da validare.',
     'Ogni ~30 min (Task Scheduler)',
     'Sys_email_valida_restituzioni'),
    ('kit_requests_reminder',
     'Reminder richieste materiale kit PENDING',
     'main',
     'kit_requests_reminder.py',
     'Reminder per richieste materiale kit ancora in stato PENDING.',
     'Ogni 5 min (Task Scheduler)',
     'Sys_email_Kit_materiali'),
    ('shipment_info_emails',
     'Info spedizioni da file Excel (D365)',
     'run_shipment_info_check',
     'shipment_info_service.py',
     'Scansiona le directory di spedizione configurate, invia email con i dati del file Excel e rinomina il file con prefisso Executed_.',
     'Ogni 60 sec (polling)',
     None),
]


def seed_default_jobs(db):
    """
    Inserisce i job predefiniti se mancanti (idempotente).
    I record esistenti non vengono modificati, cosi' le note editate dall'utente restano intatte.
    """
    try:
        _ensure_jobs_table(db)
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            for job in DEFAULT_JOBS:
                cur.execute(
                    """
                    INSERT INTO Traceability_RS.dbo.AutomaticEmailJobs
                        (JobName, DisplayName, FunctionName, ModulePath,
                         Description, Timing, RecipientsSettingKey, IsEnabled)
                    SELECT ?, ?, ?, ?, ?, ?, ?, 1
                    WHERE NOT EXISTS (
                        SELECT 1 FROM Traceability_RS.dbo.AutomaticEmailJobs
                        WHERE JobName = ?
                    )
                    """,
                    (job[0], job[1], job[2], job[3], job[4], job[5], job[6], job[0])
                )
            db.conn.commit()
            logger.info("Seed job automatici completato")
    except Exception as e:
        logger.warning("Impossibile popolare i job predefiniti: %s", e)


def _ensure_default_job(db, job_name):
    """Inserisce il job predefinito se manca nella tabella. Ritorna True se ora esiste."""
    spec = next((j for j in DEFAULT_JOBS if j[0] == job_name), None)
    if spec is None:
        return False
    try:
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                """
                INSERT INTO Traceability_RS.dbo.AutomaticEmailJobs
                    (JobName, DisplayName, FunctionName, ModulePath,
                     Description, Timing, RecipientsSettingKey, IsEnabled)
                SELECT ?, ?, ?, ?, ?, ?, ?, 1
                WHERE NOT EXISTS (
                    SELECT 1 FROM Traceability_RS.dbo.AutomaticEmailJobs
                    WHERE JobName = ?
                )
                """,
                (spec[0], spec[1], spec[2], spec[3], spec[4], spec[5], spec[6], spec[0])
            )
            db.conn.commit()
            return True
    except Exception as e:
        logger.warning("Impossibile creare job predefinito %s: %s", job_name, e)
        return False


def _job_row_exists(db, job_name):
    try:
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                "SELECT COUNT(*) FROM Traceability_RS.dbo.AutomaticEmailJobs WHERE JobName = ?",
                (job_name,)
            )
            return cur.fetchone()[0] > 0
    except Exception:
        return True  # in caso di errore non tentare l'auto-heal


def _ensure_jobs_table(db):
    """Crea la tabella AutomaticEmailJobs se non esiste."""
    try:
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(CREATE_JOBS_TABLE_SQL)
            db.conn.commit()
    except Exception as e:
        logger.warning("Impossibile assicurare AutomaticEmailJobs: %s", e)


def is_job_enabled(db, job_name):
    """Ritorna True se il job esiste ed e' abilitato. Se la tabella non esiste, True."""
    try:
        _ensure_jobs_table(db)
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                "SELECT IsEnabled FROM Traceability_RS.dbo.AutomaticEmailJobs WHERE JobName = ?",
                (job_name,)
            )
            row = cur.fetchone()
            if row is None:
                return True
            return bool(row[0])
    except Exception as e:
        logger.warning("Errore lettura abilitazione job %s: %s", job_name, e)
        return True


def claim_job_run(db, job_name, lock_minutes=60):
    """
    Prenota l'esecuzione del job se abilitato e non bloccato da un altro PC.
    Ritorna True solo se questo processo vince il lock.
    """
    if not is_job_enabled(db, job_name):
        logger.info("Job %s disabilitato: esecuzione saltata", job_name)
        return False

    try:
        _ensure_jobs_table(db)
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                """
                UPDATE Traceability_RS.dbo.AutomaticEmailJobs
                SET LockUntil = DATEADD(MINUTE, ?, GETDATE()),
                    UpdatedAt = GETDATE()
                WHERE JobName = ?
                  AND IsEnabled = 1
                  AND ISNULL(LockUntil, '1900-01-01') <= GETDATE()
                """,
                (lock_minutes, job_name)
            )
            db.conn.commit()
            claimed = cur.rowcount > 0
            if not claimed and not _job_row_exists(db, job_name):
                # Riga mancante (es. job aggiunto a DEFAULT_JOBS dopo il seed
                # iniziale): la crea e riprova il claim una volta sola.
                if _ensure_default_job(db, job_name):
                    cur.execute(
                        """
                        UPDATE Traceability_RS.dbo.AutomaticEmailJobs
                        SET LockUntil = DATEADD(MINUTE, ?, GETDATE()),
                            UpdatedAt = GETDATE()
                        WHERE JobName = ?
                          AND IsEnabled = 1
                          AND ISNULL(LockUntil, '1900-01-01') <= GETDATE()
                        """,
                        (lock_minutes, job_name)
                    )
                    db.conn.commit()
                    claimed = cur.rowcount > 0
            if claimed:
                logger.info("Job %s lock acquisito per %d minuti", job_name, lock_minutes)
            else:
                logger.info("Job %s non claimato (lockato da altro PC o disabilitato)", job_name)
            return claimed
    except Exception as e:
        logger.error("Errore claim job %s: %s", job_name, e, exc_info=True)
        return False


def force_claim_job(db, job_name, lock_minutes=60):
    """
    Forza il lock per un job (bypassa lock esistente). Utile per esecuzione manuale.
    Ritorna True se il job e' abilitato.
    """
    if not is_job_enabled(db, job_name):
        logger.info("Job %s disabilitato: force run saltata", job_name)
        return False

    try:
        _ensure_jobs_table(db)
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                """
                UPDATE Traceability_RS.dbo.AutomaticEmailJobs
                SET LockUntil = DATEADD(MINUTE, ?, GETDATE()),
                    UpdatedAt = GETDATE()
                WHERE JobName = ? AND IsEnabled = 1
                """,
                (lock_minutes, job_name)
            )
            db.conn.commit()
            claimed = cur.rowcount > 0
            if not claimed and not _job_row_exists(db, job_name):
                if _ensure_default_job(db, job_name):
                    cur.execute(
                        """
                        UPDATE Traceability_RS.dbo.AutomaticEmailJobs
                        SET LockUntil = DATEADD(MINUTE, ?, GETDATE()),
                            UpdatedAt = GETDATE()
                        WHERE JobName = ? AND IsEnabled = 1
                        """,
                        (lock_minutes, job_name)
                    )
                    db.conn.commit()
                    claimed = cur.rowcount > 0
            return claimed
    except Exception as e:
        logger.error("Errore force claim job %s: %s", job_name, e, exc_info=True)
        return False


def release_job_lock(db, job_name):
    """Rilascia il lock del job (es. se l'invio fallisce prima della consegna)."""
    try:
        _ensure_jobs_table(db)
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                """
                UPDATE Traceability_RS.dbo.AutomaticEmailJobs
                SET LockUntil = NULL, UpdatedAt = GETDATE()
                WHERE JobName = ?
                """,
                (job_name,)
            )
            db.conn.commit()
    except Exception as e:
        logger.error("Errore rilascio lock job %s: %s", job_name, e, exc_info=True)


def log_job_run(db, job_name, status, message, next_run_at=None):
    """
    Registra l'esito di un'esecuzione.
    status: 'OK', 'ERROR', 'SKIPPED', 'LOCKED', ecc.
    """
    try:
        _ensure_jobs_table(db)
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                """
                UPDATE Traceability_RS.dbo.AutomaticEmailJobs
                SET LastRunAt = GETDATE(),
                    LastRunStatus = ?,
                    LastRunMessage = ?,
                    NextRunAt = ?,
                    UpdatedAt = GETDATE()
                WHERE JobName = ?
                """,
                (status, message, next_run_at, job_name)
            )
            db.conn.commit()
    except Exception as e:
        logger.error("Errore log job %s: %s", job_name, e, exc_info=True)


def load_jobs(db):
    """Carica tutti i job dalla tabella. Ritorna lista di dict.
    Alla prima apertura inserisce anche i job predefiniti mancanti."""
    try:
        _ensure_jobs_table(db)
        seed_default_jobs(db)
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            cur.execute(
                """
                SELECT JobName, DisplayName, FunctionName, ModulePath,
                       Description, Timing, RecipientsSettingKey, IsEnabled,
                       LastRunAt, LastRunStatus, LastRunMessage, NextRunAt,
                       LockUntil, CreatedAt, UpdatedAt
                FROM Traceability_RS.dbo.AutomaticEmailJobs
                ORDER BY DisplayName
                """
            )
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            return [dict(zip(cols, r)) for r in rows]
    except Exception as e:
        logger.error("Errore caricamento job: %s", e, exc_info=True)
        return []


def update_job(db, job_name, fields):
    """
    Aggiorna i campi modificabili di un job.
    fields: dict con chiavi tra DisplayName, Description, Timing, RecipientsSettingKey, IsEnabled.
    """
    allowed = {'DisplayName', 'Description', 'Timing', 'RecipientsSettingKey', 'IsEnabled'}
    to_update = {k: v for k, v in fields.items() if k in allowed}
    if not to_update:
        return False

    try:
        _ensure_jobs_table(db)
        db._ensure_connection()
        with db._lock:
            cur = db.cursor
            set_clause = ', '.join(f"{k} = ?" for k in to_update)
            params = list(to_update.values()) + [job_name]
            cur.execute(
                f"""
                UPDATE Traceability_RS.dbo.AutomaticEmailJobs
                SET {set_clause}, UpdatedAt = GETDATE()
                WHERE JobName = ?
                """,
                tuple(params)
            )
            db.conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        logger.error("Errore aggiornamento job %s: %s", job_name, e, exc_info=True)
        return False
