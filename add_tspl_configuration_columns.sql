-- =============================================
-- Add TSPL Configuration Columns - SAFE VERSION
-- =============================================
-- This script safely adds columns one by one
-- =============================================

USE [Traceability_RS]
GO

-- Add TSPLXOffset
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[LabelConfiguration]') AND name = 'TSPLXOffset')
BEGIN
    ALTER TABLE [dbo].[LabelConfiguration] ADD TSPLXOffset INT NULL;
    PRINT 'Column TSPLXOffset added.';
END
ELSE
    PRINT 'Column TSPLXOffset already exists.';
GO

-- Add TSPLYOffset
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[LabelConfiguration]') AND name = 'TSPLYOffset')
BEGIN
    ALTER TABLE [dbo].[LabelConfiguration] ADD TSPLYOffset INT NULL;
    PRINT 'Column TSPLYOffset added.';
END
ELSE
    PRINT 'Column TSPLYOffset already exists.';
GO

-- Add TSPLLineSpacing
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[LabelConfiguration]') AND name = 'TSPLLineSpacing')
BEGIN
    ALTER TABLE [dbo].[LabelConfiguration] ADD TSPLLineSpacing INT NULL;
    PRINT 'Column TSPLLineSpacing added.';
END
ELSE
    PRINT 'Column TSPLLineSpacing already exists.';
GO

-- Add TSPLFontSize
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[LabelConfiguration]') AND name = 'TSPLFontSize')
BEGIN
    ALTER TABLE [dbo].[LabelConfiguration] ADD TSPLFontSize VARCHAR(10) NULL;
    PRINT 'Column TSPLFontSize added.';
END
ELSE
    PRINT 'Column TSPLFontSize already exists.';
GO

-- Add TSPLFontMultiplierX
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[LabelConfiguration]') AND name = 'TSPLFontMultiplierX')
BEGIN
    ALTER TABLE [dbo].[LabelConfiguration] ADD TSPLFontMultiplierX INT NULL;
    PRINT 'Column TSPLFontMultiplierX added.';
END
ELSE
    PRINT 'Column TSPLFontMultiplierX already exists.';
GO

-- Add TSPLFontMultiplierY
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[LabelConfiguration]') AND name = 'TSPLFontMultiplierY')
BEGIN
    ALTER TABLE [dbo].[LabelConfiguration] ADD TSPLFontMultiplierY INT NULL;
    PRINT 'Column TSPLFontMultiplierY added.';
END
ELSE
    PRINT 'Column TSPLFontMultiplierY already exists.';
GO

-- Update existing records with default values
PRINT 'Updating existing records with default values...';
UPDATE [dbo].[LabelConfiguration]
SET 
    TSPLXOffset = ISNULL(TSPLXOffset, 120),
    TSPLYOffset = ISNULL(TSPLYOffset, 100),
    TSPLLineSpacing = ISNULL(TSPLLineSpacing, 60),
    TSPLFontSize = ISNULL(TSPLFontSize, '3'),
    TSPLFontMultiplierX = ISNULL(TSPLFontMultiplierX, 1),
    TSPLFontMultiplierY = ISNULL(TSPLFontMultiplierY, 1);

PRINT 'Update complete.';
GO

-- Verify all columns exist
PRINT '';
PRINT '=== VERIFICATION ===';
SELECT 
    COLUMN_NAME, 
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'LabelConfiguration'
AND COLUMN_NAME LIKE 'TSPL%'
ORDER BY ORDINAL_POSITION;
GO

-- Show current configuration
PRINT '';
PRINT '=== CURRENT ACTIVE CONFIGURATION ===';
SELECT 
    ConfigID,
    LabelWidth,
    LabelHeight,
    TSPLXOffset,
    TSPLYOffset,
    TSPLLineSpacing,
    TSPLFontSize,
    TSPLFontMultiplierX,
    TSPLFontMultiplierY,
    IsActive
FROM [dbo].[LabelConfiguration]
WHERE IsActive = 1;
GO
