-- =============================================
-- Label Configuration Table Creation Script
-- =============================================
-- Description: Creates the LabelConfiguration table to store
--              label dimensions and field printing preferences
-- =============================================

USE [Traceability_RS]
GO

-- Create the table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LabelConfiguration]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[LabelConfiguration] (
        ConfigID INT IDENTITY(1,1) PRIMARY KEY,
        LabelWidth DECIMAL(10,2) NOT NULL DEFAULT 10.0,  -- Width in cm
        LabelHeight DECIMAL(10,2) NOT NULL DEFAULT 5.0,  -- Height in cm
        PrintOrderNumber BIT NOT NULL DEFAULT 1,
        PrintMaterialCode BIT NOT NULL DEFAULT 1,
        PrintComponentQuantity BIT NOT NULL DEFAULT 1,
        PrintReferences BIT NOT NULL DEFAULT 1,
        OrderNumberPosition INT NULL,
        MaterialCodePosition INT NULL,
        ComponentQuantityPosition INT NULL,
        ReferencesPosition INT NULL,
        CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
        ModifiedDate DATETIME NOT NULL DEFAULT GETDATE(),
        CreatedBy NVARCHAR(100) NULL,
        ModifiedBy NVARCHAR(100) NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );
    
    PRINT 'Table [dbo].[LabelConfiguration] created successfully.';
END
ELSE
BEGIN
    PRINT 'Table [dbo].[LabelConfiguration] already exists.';
END
GO

-- Insert default configuration if table is empty
IF NOT EXISTS (SELECT 1 FROM [dbo].[LabelConfiguration] WHERE IsActive = 1)
BEGIN
    INSERT INTO [dbo].[LabelConfiguration] 
        (LabelWidth, LabelHeight, PrintOrderNumber, PrintMaterialCode, 
         PrintComponentQuantity, PrintReferences, 
         OrderNumberPosition, MaterialCodePosition, 
         ComponentQuantityPosition, ReferencesPosition,
         CreatedBy, ModifiedBy)
    VALUES 
        (10.0, 5.0, 1, 1, 1, 1, 1, 2, 3, 4, N'SYSTEM', N'SYSTEM');
    
    PRINT 'Default configuration inserted successfully.';
END
ELSE
BEGIN
    PRINT 'Active configuration already exists.';
END
GO

-- Verify the table and data
SELECT * FROM [dbo].[LabelConfiguration];
GO
