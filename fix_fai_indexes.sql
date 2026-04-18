-- ============================================================
-- FIX: Aggiunge indice covering per deduplicazione cross-pipeline
-- su FaiEnforcementLog (OrderNumber, CheckDate, EscalationLevel)
--
-- Questo indice elimina i table scan sulle query di
-- check_cross_pipeline_escalated() e check_already_escalated()
-- che usano OrderNumber come chiave di ricerca.
-- ============================================================

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes 
    WHERE name = 'IX_FaiEnforcementLog_OrderNumber' 
      AND object_id = OBJECT_ID('[fai].[FaiEnforcementLog]')
)
BEGIN
    CREATE INDEX IX_FaiEnforcementLog_OrderNumber
        ON [Traceability_RS].[fai].[FaiEnforcementLog] (OrderNumber, CheckDate, EscalationLevel)
        INCLUDE (EventType, DateIn, EmployeeHireHistoryId);
    PRINT 'Indice IX_FaiEnforcementLog_OrderNumber creato';
END
ELSE
    PRINT 'Indice IX_FaiEnforcementLog_OrderNumber esiste già';
GO
