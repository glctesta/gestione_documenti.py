-- ============================================================================
-- Tabella lookup motivazioni pausa (WorkBreakReasons)
-- Ogni pausa puo' essere associata a una motivazione (es. Pausa sigaretta,
-- Pausa pranzo). I valori predefiniti sono in rumeno come richiesto.
-- ============================================================================

IF OBJECT_ID(N'[Employee].[dbo].[WorkBreakReasons]', N'U') IS NULL
BEGIN
    CREATE TABLE [Employee].[dbo].[WorkBreakReasons] (
        [WorkBreakReasonId]  INT IDENTITY(1,1) NOT NULL,
        [ReasonDescription]  NVARCHAR(100) NOT NULL,
        [DateIn]             DATETIME NOT NULL DEFAULT GETDATE(),
        [DateOut]            DATETIME NULL,
        CONSTRAINT [PK_WorkBreakReasons] PRIMARY KEY CLUSTERED ([WorkBreakReasonId] ASC)
    );
    PRINT 'Tabella Employee.dbo.WorkBreakReasons creata.';
END
ELSE
BEGIN
    PRINT 'Tabella Employee.dbo.WorkBreakReasons gia esistente.';
END
GO

-- Valori predefiniti in rumeno
IF NOT EXISTS (SELECT 1 FROM [Employee].[dbo].[WorkBreakReasons] WHERE [ReasonDescription] = N'Pauza țigară' AND [DateOut] IS NULL)
    INSERT INTO [Employee].[dbo].[WorkBreakReasons] ([ReasonDescription]) VALUES (N'Pauza țigară');

IF NOT EXISTS (SELECT 1 FROM [Employee].[dbo].[WorkBreakReasons] WHERE [ReasonDescription] = N'Pauză de masă' AND [DateOut] IS NULL)
    INSERT INTO [Employee].[dbo].[WorkBreakReasons] ([ReasonDescription]) VALUES (N'Pauză de masă');

PRINT 'Motivazioni pausa predefinite inserite.';
GO

-- Colonna di riferimento su WorkBreaks
IF NOT EXISTS (
    SELECT 1
    FROM Employee.INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'WorkBreaks'
      AND COLUMN_NAME = 'WorkBreakReasonId'
)
BEGIN
    ALTER TABLE [Employee].[dbo].[WorkBreaks]
        ADD [WorkBreakReasonId] INT NULL
            CONSTRAINT [FK_WorkBreaks_WorkBreakReasons]
            FOREIGN KEY ([WorkBreakReasonId])
            REFERENCES [Employee].[dbo].[WorkBreakReasons] ([WorkBreakReasonId]);
    PRINT 'Colonna WorkBreakReasonId aggiunta a WorkBreaks.';
END
ELSE
BEGIN
    PRINT 'Colonna WorkBreakReasonId gia esistente.';
END
GO
