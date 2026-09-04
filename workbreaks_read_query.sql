-- ============================================================================
-- Query di lettura per la nuova struttura WorkBreaks + WorkBreakData
-- ============================================================================

-- ---------------------------------------------------------------------------
-- 1. VISTA DETTAGLIO: una riga per ogni combinazione CDC / Sub CDC / Funzione
-- ---------------------------------------------------------------------------
IF OBJECT_ID(N'[Employee].[dbo].[vw_WorkBreaks_Detail]', N'V') IS NOT NULL
    DROP VIEW [Employee].[dbo].[vw_WorkBreaks_Detail];
GO

CREATE VIEW [Employee].[dbo].[vw_WorkBreaks_Detail]
AS
SELECT 
    wb.WorkBreakId,
    wb.IsForChangeShift,
    wd.WorkBreakDataId,
    wd.CdcId,
    cc.CdcDescription,
    wd.SubCdcId,
    sc.SubCdcDescription,
    wd.FunctionId,
    f.FunctionDescription,
    wb.Shift,
    wb.FromTime,
    wb.ToTime,
    CASE WHEN wb.Sound IS NOT NULL AND DATALENGTH(wb.Sound) > 0 THEN 1 ELSE 0 END AS HasSound,
    CASE WHEN wb.TextToshow IS NOT NULL AND DATALENGTH(wb.TextToshow) > 0 THEN 1 ELSE 0 END AS HasDocument,
    wb.EmployeerId,
    er.EmployeerName,
    wb.WorkBreakReasonId,
    wbr.ReasonDescription,
    wb.DateIn,
    wb.DateOut
FROM [Employee].[dbo].[WorkBreaks] wb
LEFT JOIN [Employee].[dbo].[WorkBreakData] wd 
       ON wd.WorkBreakId = wb.WorkBreakId 
      AND wd.DateOut IS NULL
LEFT JOIN [Employee].[dbo].[CostCenters] cc ON cc.CdcId = wd.CdcId
LEFT JOIN [Employee].[dbo].[CdcSub] sc ON sc.SubCdcId = wd.SubCdcId
LEFT JOIN [Employee].[dbo].[Functions] f ON f.FunctionId = wd.FunctionId
LEFT JOIN [Employee].[dbo].[Employeers] er ON er.EmployeerId = wb.EmployeerId
LEFT JOIN [Employee].[dbo].[WorkBreakReasons] wbr ON wbr.WorkBreakReasonId = wb.WorkBreakReasonId
WHERE wb.DateOut IS NULL;
GO

-- Esempio di utilizzo della vista dettaglio
-- SELECT * FROM [Employee].[dbo].[vw_WorkBreaks_Detail]
-- ORDER BY FromTime, Shift, CdcDescription, SubCdcDescription, FunctionDescription;

-- ---------------------------------------------------------------------------
-- 2. QUERY RIEPILOGO: una riga per regola con CDC / Sub CDC / Funzioni concatenati
-- ---------------------------------------------------------------------------
SELECT 
    wb.WorkBreakId,
    wb.IsForChangeShift,
    wb.Shift,
    wb.FromTime,
    wb.ToTime,
    STUFF((
        SELECT DISTINCT ', ' + cc.CdcDescription
        FROM [Employee].[dbo].[WorkBreakData] wd2
        LEFT JOIN [Employee].[dbo].[CostCenters] cc ON cc.CdcId = wd2.CdcId
        WHERE wd2.WorkBreakId = wb.WorkBreakId 
          AND wd2.DateOut IS NULL 
          AND wd2.CdcId IS NOT NULL
        FOR XML PATH(''), TYPE
    ).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS CDCs,
    STUFF((
        SELECT DISTINCT ', ' + sc.SubCdcDescription
        FROM [Employee].[dbo].[WorkBreakData] wd2
        LEFT JOIN [Employee].[dbo].[CdcSub] sc ON sc.SubCdcId = wd2.SubCdcId
        WHERE wd2.WorkBreakId = wb.WorkBreakId 
          AND wd2.DateOut IS NULL 
          AND wd2.SubCdcId IS NOT NULL
        FOR XML PATH(''), TYPE
    ).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS SubCDCs,
    STUFF((
        SELECT DISTINCT ', ' + f.FunctionDescription
        FROM [Employee].[dbo].[WorkBreakData] wd2
        LEFT JOIN [Employee].[dbo].[Functions] f ON f.FunctionId = wd2.FunctionId
        WHERE wd2.WorkBreakId = wb.WorkBreakId 
          AND wd2.DateOut IS NULL 
          AND wd2.FunctionId IS NOT NULL
        FOR XML PATH(''), TYPE
    ).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS Functions,
    CASE WHEN wb.Sound IS NOT NULL AND DATALENGTH(wb.Sound) > 0 THEN 1 ELSE 0 END AS HasSound,
    CASE WHEN wb.TextToshow IS NOT NULL AND DATALENGTH(wb.TextToshow) > 0 THEN 1 ELSE 0 END AS HasDocument,
    wb.EmployeerId,
    er.EmployeerName,
    wb.WorkBreakReasonId,
    wbr.ReasonDescription,
    wb.DateIn
FROM [Employee].[dbo].[WorkBreaks] wb
LEFT JOIN [Employee].[dbo].[Employeers] er ON er.EmployeerId = wb.EmployeerId
LEFT JOIN [Employee].[dbo].[WorkBreakReasons] wbr ON wbr.WorkBreakReasonId = wb.WorkBreakReasonId
WHERE wb.DateOut IS NULL
ORDER BY wb.FromTime, wb.Shift, wb.WorkBreakId;
GO
