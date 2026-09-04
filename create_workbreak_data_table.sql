-- ============================================================================
-- Schema tabella figlia WorkBreakData
-- Ogni pausa (WorkBreaks) può essere associata a più CDC / Sub CDC / Funzioni.
-- I dati multipli sono salvati come prodotto delle selezioni nelle rispettive listbox.
-- ============================================================================

-- Se la tabella esiste già con una struttura vecchia, la ricrea da zero.
-- ATTENZIONE: se contiene già dati, verranno persi.
IF OBJECT_ID(N'[Employee].[dbo].[WorkBreakData]', N'U') IS NOT NULL
BEGIN
    DROP TABLE [Employee].[dbo].[WorkBreakData];
    PRINT 'Tabella Employee.dbo.WorkBreakData esistente droppata per ricreazione.';
END
GO

CREATE TABLE [Employee].[dbo].[WorkBreakData] (
    [WorkBreakDataId]  INT IDENTITY(1,1) NOT NULL,
    [WorkBreakId]      SMALLINT NOT NULL,
    [CdcId]            INT NULL,
    [SubCdcId]         INT NULL,
    [FunctionId]       INT NULL,
    [DateIn]           DATETIME NOT NULL DEFAULT GETDATE(),
    [DateOut]          DATETIME NULL,
    CONSTRAINT [PK_WorkBreakData] PRIMARY KEY CLUSTERED ([WorkBreakDataId] ASC),
    CONSTRAINT [FK_WorkBreakData_WorkBreaks]
        FOREIGN KEY ([WorkBreakId])
        REFERENCES [Employee].[dbo].[WorkBreaks] ([WorkBreakId]),
    CONSTRAINT [FK_WorkBreakData_CostCenters]
        FOREIGN KEY ([CdcId])
        REFERENCES [Employee].[dbo].[CostCenters] ([CdcId]),
    CONSTRAINT [FK_WorkBreakData_CdcSub]
        FOREIGN KEY ([SubCdcId])
        REFERENCES [Employee].[dbo].[CdcSub] ([SubCdcId]),
    CONSTRAINT [FK_WorkBreakData_Functions]
        FOREIGN KEY ([FunctionId])
        REFERENCES [Employee].[dbo].[Functions] ([FunctionId]),
    CONSTRAINT [CK_WorkBreakData_AtLeastOne]
        CHECK ([CdcId] IS NOT NULL OR [SubCdcId] IS NOT NULL OR [FunctionId] IS NOT NULL)
);

CREATE NONCLUSTERED INDEX [IX_WorkBreakData_WorkBreakId]
    ON [Employee].[dbo].[WorkBreakData] ([WorkBreakId])
    INCLUDE ([CdcId], [SubCdcId], [FunctionId], [DateOut]);

CREATE NONCLUSTERED INDEX [IX_WorkBreakData_CdcId]
    ON [Employee].[dbo].[WorkBreakData] ([CdcId])
    WHERE [CdcId] IS NOT NULL;

CREATE NONCLUSTERED INDEX [IX_WorkBreakData_SubCdcId]
    ON [Employee].[dbo].[WorkBreakData] ([SubCdcId])
    WHERE [SubCdcId] IS NOT NULL;

CREATE NONCLUSTERED INDEX [IX_WorkBreakData_FunctionId]
    ON [Employee].[dbo].[WorkBreakData] ([FunctionId])
    WHERE [FunctionId] IS NOT NULL;

PRINT 'Tabella Employee.dbo.WorkBreakData creata.';
GO
