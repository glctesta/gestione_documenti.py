-- Add AttachmentDoc column to PeriodicalProductCheckLogs
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'PeriodicalProductCheckLogs'
      AND COLUMN_NAME = 'AttachmentDoc'
)
BEGIN
    ALTER TABLE [Traceability_RS].[dbo].[PeriodicalProductCheckLogs]
    ADD AttachmentDoc VARBINARY(MAX) NULL;
    PRINT 'Column AttachmentDoc added to PeriodicalProductCheckLogs';
END
ELSE
    PRINT 'Column AttachmentDoc already exists';

-- Add PriodicalProductCheckListId column to track which task had the X-Ray check
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'PeriodicalProductCheckLogs'
      AND COLUMN_NAME = 'PriodicalProductCheckListId'
)
BEGIN
    ALTER TABLE [Traceability_RS].[dbo].[PeriodicalProductCheckLogs]
    ADD PriodicalProductCheckListId INT NULL;
    PRINT 'Column PriodicalProductCheckListId added to PeriodicalProductCheckLogs';
END
ELSE
    PRINT 'Column PriodicalProductCheckListId already exists';

-- Insert setting for email recipients
IF NOT EXISTS (SELECT 1 FROM traceability_rs.dbo.settings WHERE atribute = 'sys_email_NoXrayInChekControl')
INSERT INTO traceability_rs.dbo.settings (atribute, [value])
VALUES ('sys_email_NoXrayInChekControl', 'gianluca.testa@vandewiele.com');
