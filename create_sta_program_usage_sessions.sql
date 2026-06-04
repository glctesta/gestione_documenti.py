USE [Traceability_RS];
GO

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'sta')
    EXEC('CREATE SCHEMA sta');
GO

IF OBJECT_ID('sta.ProgramUsageSessions', 'U') IS NULL
BEGIN
    CREATE TABLE sta.ProgramUsageSessions (
        ProgramUsageId BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        ProgramName NVARCHAR(260) NOT NULL,
        AppVersion NVARCHAR(50) NULL,
        HostName NVARCHAR(128) NULL,
        IpAddress NVARCHAR(64) NULL,
        StartDate DATE NOT NULL,
        StartDateTime DATETIME2(0) NOT NULL,
        EndDateTime DATETIME2(0) NULL,
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_ProgramUsage_CreatedAt DEFAULT SYSDATETIME()
    );

    CREATE INDEX IX_ProgramUsage_StartDateTime
        ON sta.ProgramUsageSessions (StartDateTime DESC);

    CREATE INDEX IX_ProgramUsage_Host_StartDate
        ON sta.ProgramUsageSessions (HostName, StartDate DESC);
END
GO

PRINT 'Schema sta e tabella sta.ProgramUsageSessions pronti.';
GO
