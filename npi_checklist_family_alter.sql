-- ============================================================
-- ALTER FamilyNpis — Add Checklist Configuration
-- Per ogni famiglia, definisce quale sezione checklist rappresenta
-- e quali tipi di dati raccogliere
-- ============================================================
USE Traceability_RS
GO

-- ChecklistSection: nome della sezione checklist (es. 'SMT_TOP', 'PTH', 'ICT', etc.)
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id=OBJECT_ID('dbo.FamilyNpis') AND name='ChecklistSection')
BEGIN
    ALTER TABLE dbo.FamilyNpis ADD ChecklistSection NVARCHAR(100) NULL;
    PRINT '✅ Colonna ChecklistSection aggiunta'
END
GO

-- Flag per i tipi di dati da raccogliere nella checklist per questa famiglia
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id=OBJECT_ID('dbo.FamilyNpis') AND name='CL_HasPrograms')
BEGIN
    ALTER TABLE dbo.FamilyNpis ADD CL_HasPrograms BIT NOT NULL DEFAULT 0;
    PRINT '✅ Colonna CL_HasPrograms aggiunta'
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id=OBJECT_ID('dbo.FamilyNpis') AND name='CL_HasMaterials')
BEGIN
    ALTER TABLE dbo.FamilyNpis ADD CL_HasMaterials BIT NOT NULL DEFAULT 0;
    PRINT '✅ Colonna CL_HasMaterials aggiunta'
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id=OBJECT_ID('dbo.FamilyNpis') AND name='CL_HasProductionData')
BEGIN
    ALTER TABLE dbo.FamilyNpis ADD CL_HasProductionData BIT NOT NULL DEFAULT 0;
    PRINT '✅ Colonna CL_HasProductionData aggiunta'
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id=OBJECT_ID('dbo.FamilyNpis') AND name='CL_HasVerification')
BEGIN
    ALTER TABLE dbo.FamilyNpis ADD CL_HasVerification BIT NOT NULL DEFAULT 0;
    PRINT '✅ Colonna CL_HasVerification aggiunta'
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id=OBJECT_ID('dbo.FamilyNpis') AND name='CL_HasPreformingChecks')
BEGIN
    ALTER TABLE dbo.FamilyNpis ADD CL_HasPreformingChecks BIT NOT NULL DEFAULT 0;
    PRINT '✅ Colonna CL_HasPreformingChecks aggiunta'
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id=OBJECT_ID('dbo.FamilyNpis') AND name='CL_HasCoating')
BEGIN
    ALTER TABLE dbo.FamilyNpis ADD CL_HasCoating BIT NOT NULL DEFAULT 0;
    PRINT '✅ Colonna CL_HasCoating aggiunta'
END
GO

-- Ordine di visualizzazione nel Notebook della checklist
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id=OBJECT_ID('dbo.FamilyNpis') AND name='CL_SortOrder')
BEGIN
    ALTER TABLE dbo.FamilyNpis ADD CL_SortOrder INT NOT NULL DEFAULT 0;
    PRINT '✅ Colonna CL_SortOrder aggiunta'
END
GO

PRINT '✅ FamilyNpis aggiornata con colonne checklist'
GO
