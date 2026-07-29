-- ============================================================
-- FAI Enforcement - Rete di sicurezza contro le email duplicate
--
-- Il fix applicativo (claim atomico in fai_enforcement.py) funziona
-- anche SENZA questo script. Questi indici sono la garanzia a livello
-- DB: se un giorno qualcuno reintroduce una INSERT non protetta, il
-- database rifiuta il duplicato invece di far partire l'email.
--
-- ESEGUIRE I PASSI IN ORDINE. PASSO 1, 2, 3 e 5 non cancellano nulla.
-- Il PASSO 4 e' distruttivo, e' un'ALTERNATIVA al PASSO 3 e normalmente
-- non serve: e' disattivato per default.
--
-- Prima di eseguire: impostare la DATA DI TAGLIO del PASSO 3 (quattro
-- occorrenze, cercare "DATA DI TAGLIO") al giorno in cui si esegue.
-- ============================================================

USE [Traceability_RS];
GO

-- ============================================================
-- PASSO 1 (sola lettura) - Backup della tabella
-- Sempre, prima di toccare qualsiasi cosa.
-- ============================================================
IF OBJECT_ID('fai.FaiEnforcementLog_BackupPreIndex') IS NULL
BEGIN
    SELECT * INTO [fai].[FaiEnforcementLog_BackupPreIndex]
    FROM [fai].[FaiEnforcementLog];
    PRINT 'Backup creato: fai.FaiEnforcementLog_BackupPreIndex';
END
ELSE
    PRINT 'Backup gia'' esistente, non lo sovrascrivo.';
GO


-- ============================================================
-- PASSO 2 (sola lettura) - Quali duplicati ci sono gia' in tabella?
--
-- Queste righe sono, con ogni probabilita', esattamente le email
-- doppie che sono state ricevute: la colonna Copie dice quante ne sono
-- partite e PrimoInvio/UltimoInvio a che distanza.
--
-- Sono la prova del bug e restano dove sono: il PASSO 3 le esclude dal
-- vincolo invece di cancellarle. Utile guardarle per capire quanto era
-- diffuso il problema e da quando.
-- ============================================================

PRINT '--- Duplicati su escalation legate a un ORDINE ---';
SELECT
    EventType,
    EscalationLevel,
    OrderNumber,
    COUNT(*)                  AS Copie,
    MIN(EnforcementLogId)     AS DaTenere,
    MIN(DateIn)               AS PrimoInvio,
    MAX(DateIn)               AS UltimoInvio
FROM [fai].[FaiEnforcementLog]
WHERE OrderNumber IS NOT NULL
GROUP BY EventType, EscalationLevel, OrderNumber
HAVING COUNT(*) > 1
ORDER BY Copie DESC, UltimoInvio DESC;

PRINT '--- Duplicati su escalation legate a un TURNO ---';
SELECT
    EventType,
    EscalationLevel,
    EmployeeHireHistoryId,
    ShiftTime,
    CheckDate,
    COUNT(*)                  AS Copie,
    MIN(EnforcementLogId)     AS DaTenere,
    MIN(DateIn)               AS PrimoInvio,
    MAX(DateIn)               AS UltimoInvio
FROM [fai].[FaiEnforcementLog]
WHERE OrderNumber IS NULL
  AND EmployeeHireHistoryId IS NOT NULL
GROUP BY EventType, EscalationLevel, EmployeeHireHistoryId, ShiftTime, CheckDate
HAVING COUNT(*) > 1
ORDER BY Copie DESC, UltimoInvio DESC;
GO


-- ============================================================
-- PASSO 3 - Indici UNIQUE sulle sole righe NUOVE
--
-- I duplicati gia' presenti in tabella sono il registro di email
-- REALMENTE INVIATE: sono la prova del bug, non spazzatura. Cancellarli
-- farebbe risultare "mai inviate" delle email che sono arrivate.
-- Quindi la storia si lascia dov'e' e si protegge solo il futuro.
--
-- La data di taglio esclude dal vincolo tutto cio' che esiste oggi.
-- Le righe scritte da qui in avanti sono comunque gia' protette dal
-- claim atomico applicativo: questi indici sono la seconda rete.
--
-- >>> IMPOSTARE LA DATA DI TAGLIO AL GIORNO IN CUI SI ESEGUE <<<
--     (deve essere >= oggi, altrimenti si ricade nei duplicati storici)
-- ============================================================

-- Controllo preliminare: dalla data di taglio in poi non devono
-- esserci duplicati, altrimenti la CREATE INDEX fallisce di nuovo.
PRINT '--- Duplicati DALLA DATA DI TAGLIO in poi (deve essere vuoto) ---';
SELECT 'ORDINE' AS Tipo, EventType, EscalationLevel,
       CAST(OrderNumber AS NVARCHAR(50)) AS Chiave, COUNT(*) AS Copie
FROM [fai].[FaiEnforcementLog]
WHERE OrderNumber IS NOT NULL
  AND DateIn >= '20260721'          -- <<< DATA DI TAGLIO
GROUP BY EventType, EscalationLevel, OrderNumber
HAVING COUNT(*) > 1
UNION ALL
SELECT 'TURNO', EventType, EscalationLevel,
       CAST(EmployeeHireHistoryId AS NVARCHAR(50)) + '/' + ISNULL(ShiftTime, ''),
       COUNT(*)
FROM [fai].[FaiEnforcementLog]
WHERE OrderNumber IS NULL
  AND EmployeeHireHistoryId IS NOT NULL
  AND DateIn >= '20260721'          -- <<< DATA DI TAGLIO
GROUP BY EventType, EscalationLevel, EmployeeHireHistoryId, ShiftTime, CheckDate
HAVING COUNT(*) > 1;
GO

-- Escalation legate a un ordine: una sola per (tipo, livello, ordine).
-- Volutamente senza CheckDate: un ordine non conforme non deve
-- ri-scalare ogni mezzanotte.
IF NOT EXISTS (SELECT 1 FROM sys.indexes
               WHERE name = 'UX_FaiEnforcementLog_Order_Level'
                 AND object_id = OBJECT_ID('fai.FaiEnforcementLog'))
BEGIN
    CREATE UNIQUE INDEX UX_FaiEnforcementLog_Order_Level
        ON [fai].[FaiEnforcementLog] (EventType, EscalationLevel, OrderNumber)
        WHERE OrderNumber IS NOT NULL
          AND DateIn >= '20260721';  -- <<< DATA DI TAGLIO
    PRINT 'Creato UX_FaiEnforcementLog_Order_Level';
END
ELSE
    PRINT 'UX_FaiEnforcementLog_Order_Level gia'' presente';
GO

-- Escalation legate a un turno: una per (tipo, livello, dipendente,
-- turno, giorno). Qui CheckDate ci va: la violazione di turno si
-- ripresenta legittimamente ogni giorno.
IF NOT EXISTS (SELECT 1 FROM sys.indexes
               WHERE name = 'UX_FaiEnforcementLog_Shift_Level'
                 AND object_id = OBJECT_ID('fai.FaiEnforcementLog'))
BEGIN
    CREATE UNIQUE INDEX UX_FaiEnforcementLog_Shift_Level
        ON [fai].[FaiEnforcementLog]
           (EventType, EscalationLevel, EmployeeHireHistoryId, ShiftTime, CheckDate)
        WHERE OrderNumber IS NULL
          AND EmployeeHireHistoryId IS NOT NULL
          AND DateIn >= '20260721';  -- <<< DATA DI TAGLIO
    PRINT 'Creato UX_FaiEnforcementLog_Shift_Level';
END
ELSE
    PRINT 'UX_FaiEnforcementLog_Shift_Level gia'' presente';
GO


-- ============================================================
-- PASSO 3-bis - Riparazione dell'artefatto EscalationLevel
--
-- NON cancella righe: RIPRISTINA un valore che era stato corrotto.
--
-- Fino al fix in fai_enforcement.py, ad ogni escalation la riga del
-- livello precedente veniva riscritta al livello nuovo:
--     update_kwargs = {'EscalationLevel': target_level}
-- Cosi' la riga L1 delle 08:28 finiva marcata L3, identica a un vero
-- invio L3 delle 09:28. Sono i finti duplicati a ~3600 secondi.
--
-- Le Notes non venivano toccate, quindi conservano il livello vero:
--     L1 turno      -> 'FAI non compilato entro 60 min dal turno ...'
--     L2/L3 turno   -> 'Escalation L2 ...' / 'Escalation L3 ...'
--     planning      -> 'Planning-based enforcement L2 ...'
--
-- Riparando queste righe gli indici possono coprire anche lo storico e
-- restano bloccanti solo i duplicati VERI.
--
-- Eseguire PRIMA la SELECT di anteprima, poi il blocco di UPDATE.
-- ============================================================

-- Anteprima: righe il cui EscalationLevel non concorda con le Notes
PRINT '--- Righe con EscalationLevel corrotto dalla riscrittura ---';
SELECT EnforcementLogId, EventType, EmployeeHireHistoryId, ShiftTime, CheckDate,
       EscalationLevel AS LivelloAttuale,
       CASE
           WHEN Notes LIKE 'FAI non compilato%' THEN 1
           WHEN Notes LIKE 'Escalation L1%' OR Notes LIKE 'Planning-based enforcement L1%' THEN 1
           WHEN Notes LIKE 'Escalation L2%' OR Notes LIKE 'Planning-based enforcement L2%' THEN 2
           WHEN Notes LIKE 'Escalation L3%' OR Notes LIKE 'Planning-based enforcement L3%' THEN 3
       END        AS LivelloVero,
       DateIn, Notes
FROM [fai].[FaiEnforcementLog]
WHERE Notes IS NOT NULL
  AND EscalationLevel <> CASE
           WHEN Notes LIKE 'FAI non compilato%' THEN 1
           WHEN Notes LIKE 'Escalation L1%' OR Notes LIKE 'Planning-based enforcement L1%' THEN 1
           WHEN Notes LIKE 'Escalation L2%' OR Notes LIKE 'Planning-based enforcement L2%' THEN 2
           WHEN Notes LIKE 'Escalation L3%' OR Notes LIKE 'Planning-based enforcement L3%' THEN 3
           ELSE EscalationLevel
      END
ORDER BY DateIn DESC;
GO

-- Riparazione. Anche questo blocco fa ROLLBACK per default: la prima
-- esecuzione dice quante righe verrebbero corrette. Quando il numero
-- coincide con l'anteprima, cambiare ROLLBACK in COMMIT e rieseguire.
-- Per attivarlo: togliere /* e */ qui sotto.
/*
BEGIN TRANSACTION;

    UPDATE [fai].[FaiEnforcementLog]
    SET EscalationLevel = CASE
            WHEN Notes LIKE 'FAI non compilato%' THEN 1
            WHEN Notes LIKE 'Escalation L1%' OR Notes LIKE 'Planning-based enforcement L1%' THEN 1
            WHEN Notes LIKE 'Escalation L2%' OR Notes LIKE 'Planning-based enforcement L2%' THEN 2
            WHEN Notes LIKE 'Escalation L3%' OR Notes LIKE 'Planning-based enforcement L3%' THEN 3
        END,
        DateOut = ISNULL(DateOut, GETDATE())   -- l'evento e' comunque concluso
    WHERE Notes IS NOT NULL
      AND EscalationLevel <> CASE
            WHEN Notes LIKE 'FAI non compilato%' THEN 1
            WHEN Notes LIKE 'Escalation L1%' OR Notes LIKE 'Planning-based enforcement L1%' THEN 1
            WHEN Notes LIKE 'Escalation L2%' OR Notes LIKE 'Planning-based enforcement L2%' THEN 2
            WHEN Notes LIKE 'Escalation L3%' OR Notes LIKE 'Planning-based enforcement L3%' THEN 3
            ELSE EscalationLevel
        END;
    PRINT 'Righe riparate: ' + CAST(@@ROWCOUNT AS VARCHAR(10));

-- Sostituire con COMMIT TRANSACTION quando il numero coincide con l'anteprima.
ROLLBACK TRANSACTION;
GO
*/


-- ============================================================
-- PASSO 4 (ALTERNATIVA DISTRUTTIVA - normalmente NON serve)
--
-- Solo se si vuole davvero un indice su TUTTA la tabella e si accetta
-- di perdere le righe duplicate storiche. Tiene la copia piu' vecchia
-- di ogni gruppo e cancella le successive.
--
-- Se si sceglie questa strada: prima eseguire questo blocco, poi
-- togliere la clausola "AND DateIn >= ..." dai due indici del PASSO 3.
--
-- Il blocco fa ROLLBACK per default: la prima esecuzione mostra QUANTE
-- righe verrebbero cancellate senza cancellarle. Quando il numero
-- convince, cambiare ROLLBACK in COMMIT e rieseguire.
--
-- Per attivarlo: togliere /* e */ qui sotto.
-- ============================================================
/*
BEGIN TRANSACTION;

    -- Duplicati per ordine
    WITH Dup AS (
        SELECT EnforcementLogId,
               ROW_NUMBER() OVER (
                   PARTITION BY EventType, EscalationLevel, OrderNumber
                   ORDER BY EnforcementLogId
               ) AS rn
        FROM [fai].[FaiEnforcementLog]
        WHERE OrderNumber IS NOT NULL
    )
    DELETE FROM Dup WHERE rn > 1;
    PRINT 'Righe cancellate (ordine): ' + CAST(@@ROWCOUNT AS VARCHAR(10));

    -- Duplicati per turno
    WITH Dup AS (
        SELECT EnforcementLogId,
               ROW_NUMBER() OVER (
                   PARTITION BY EventType, EscalationLevel,
                                EmployeeHireHistoryId, ShiftTime, CheckDate
                   ORDER BY EnforcementLogId
               ) AS rn
        FROM [fai].[FaiEnforcementLog]
        WHERE OrderNumber IS NULL
          AND EmployeeHireHistoryId IS NOT NULL
    )
    DELETE FROM Dup WHERE rn > 1;
    PRINT 'Righe cancellate (turno): ' + CAST(@@ROWCOUNT AS VARCHAR(10));

-- Sostituire con COMMIT TRANSACTION quando i numeri sopra convincono.
ROLLBACK TRANSACTION;
GO
*/


-- ============================================================
-- PASSO 5 (sola lettura) - Verifica
-- ============================================================
SELECT name AS Indice, is_unique AS [Unico], has_filter AS [Filtrato],
       filter_definition AS Filtro
FROM sys.indexes
WHERE object_id = OBJECT_ID('fai.FaiEnforcementLog')
  AND name IS NOT NULL
ORDER BY is_unique DESC, name;
GO

-- Per tornare indietro:
--   DROP INDEX UX_FaiEnforcementLog_Order_Level ON [fai].[FaiEnforcementLog];
--   DROP INDEX UX_FaiEnforcementLog_Shift_Level ON [fai].[FaiEnforcementLog];
-- e, se serve ripristinare i dati:
--   il backup e' in fai.FaiEnforcementLog_BackupPreIndex
