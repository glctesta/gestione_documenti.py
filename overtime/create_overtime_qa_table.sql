-- =============================================
-- Script per creare tabella ExtraTimeApprovalQA
-- Database: ResetServices
-- Domande e risposte sulle richieste straordinario
-- =============================================

USE [ResetServices]
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ExtraTimeApprovalQA]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ExtraTimeApprovalQA](
        [QAId]                      [int] IDENTITY(1,1) NOT NULL,
        [ExtraHourApprovalId]       [int] NOT NULL,
        [StoryExtraHourApprovalId]  [int] NULL,
        [QuestionBy]                [int] NOT NULL,
        [QuestionDate]              [datetime] NOT NULL DEFAULT GETDATE(),
        [QuestionText]              [nvarchar](2000) NOT NULL,
        [AnswerBy]                  [int] NULL,
        [AnswerDate]                [datetime] NULL,
        [AnswerText]                [nvarchar](2000) NULL,
        CONSTRAINT [PK_ExtraTimeApprovalQA] PRIMARY KEY CLUSTERED ([QAId] ASC),
        CONSTRAINT [FK_QA_Approval] FOREIGN KEY ([ExtraHourApprovalId])
            REFERENCES [dbo].[ExtraTimeApproval] ([ExtraHourApprovalId]),
        CONSTRAINT [FK_QA_Story] FOREIGN KEY ([StoryExtraHourApprovalId])
            REFERENCES [dbo].[ExtraTimeApprovalStory] ([StoryExtraHourApprovalId])
    ) ON [PRIMARY]

    PRINT N'Tabella ExtraTimeApprovalQA creata con successo'
END
ELSE
BEGIN
    PRINT N'Tabella ExtraTimeApprovalQA già esistente'
END
GO

-- Verifica
SELECT 
    'ExtraTimeApprovalQA' AS TableName,
    COUNT(*) AS RecordCount
FROM [dbo].[ExtraTimeApprovalQA]
GO

PRINT N'Script completato con successo!'
