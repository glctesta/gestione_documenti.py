-- ============================================================
-- ALTER TABLE NpiDocuments: aggiunta BudgetItemId
-- Permette di associare un documento a una riga di budget NPI
-- ============================================================
USE Traceability_RS
GO

IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'NpiDocuments' AND COLUMN_NAME = 'BudgetItemId'
)
BEGIN
    ALTER TABLE dbo.NpiDocuments
    ADD BudgetItemId INT NULL;

    ALTER TABLE dbo.NpiDocuments
    ADD CONSTRAINT FK_NpiDocuments_BudgetItem
        FOREIGN KEY (BudgetItemId)
        REFERENCES dbo.NpiBudgetItems(BudgetItemId);

    PRINT '✅ Colonna BudgetItemId aggiunta a NpiDocuments'
END
ELSE
    PRINT '⚠️ Colonna BudgetItemId già esistente in NpiDocuments'
GO
