-- =============================================
-- Add QR Code Position Configuration Columns
-- =============================================
-- Adds QR code positioning parameters to TSPL configuration
-- =============================================

USE [Traceability_RS]
GO

-- Add TSPLQRCodeX
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[LabelConfiguration]') AND name = 'TSPLQRCodeX')
BEGIN
    ALTER TABLE [dbo].[LabelConfiguration] ADD TSPLQRCodeX INT NULL;
    PRINT 'Column TSPLQRCodeX added.';
END
ELSE
    PRINT 'Column TSPLQRCodeX already exists.';
GO

-- Add TSPLQRCodeY
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[LabelConfiguration]') AND name = 'TSPLQRCodeY')
BEGIN
    ALTER TABLE [dbo].[LabelConfiguration] ADD TSPLQRCodeY INT NULL;
    PRINT 'Column TSPLQRCodeY added.';
END
ELSE
    PRINT 'Column TSPLQRCodeY already exists.';
GO

-- Add TSPLQRCodeCellWidth
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[LabelConfiguration]') AND name = 'TSPLQRCodeCellWidth')
BEGIN
    ALTER TABLE [dbo].[LabelConfiguration] ADD TSPLQRCodeCellWidth INT NULL;
    PRINT 'Column TSPLQRCodeCellWidth added.';
END
ELSE
    PRINT 'Column TSPLQRCodeCellWidth already exists.';
GO

-- Update existing records with default values
PRINT 'Updating existing records with default QR code values...';
UPDATE [dbo].[LabelConfiguration]
SET 
    TSPLQRCodeX = ISNULL(TSPLQRCodeX, 450),
    TSPLQRCodeY = ISNULL(TSPLQRCodeY, 100),
    TSPLQRCodeCellWidth = ISNULL(TSPLQRCodeCellWidth, 4);

PRINT 'Update complete.';
GO

-- Verify columns
PRINT '';
PRINT '=== QR CODE CONFIGURATION COLUMNS ===';
SELECT 
    COLUMN_NAME, 
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'LabelConfiguration'
AND COLUMN_NAME LIKE 'TSPLQR%'
ORDER BY ORDINAL_POSITION;
GO

-- Show current configuration
PRINT '';
PRINT '=== CURRENT CONFIGURATION ===';
SELECT 
    ConfigID,
    TSPLQRCodeX,
    TSPLQRCodeY,
    TSPLQRCodeCellWidth,
    IsActive
FROM [dbo].[LabelConfiguration]
WHERE IsActive = 1;
GO
