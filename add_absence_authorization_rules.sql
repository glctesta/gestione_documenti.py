/*
    add_absence_authorization_rules.sql

    Regole di visibilita' della form Autorizzazione Assenze (absence_authorization.py).

    Sostituiscono la logica cablata nel codice ("stesso CdcId + FunctionCode minore",
    piu' il gate FunctionCode >= 70) e il fallback su Employee.dbo.GetManagerForSingleEmployee,
    che concedeva visibilita' totale alle Risorse Umane tramite un SubCdcId = 24
    scritto dentro la stored procedure.

    Modello
    -------
    Un dipartimento e' un CdcId; il suo capo e' chi ha il FunctionCode piu' alto.
    Le regole si valutano per Priority CRESCENTE: vince la PRIMA che combacia.
    Chi non combacia con nessuna regola non vede alcuna richiesta.

      MatchFunctionCode          FunctionCode dell'autorizzatore (NULL = ininfluente)
      MatchSubCdcId              sotto-reparto dell'autorizzatore (NULL = ininfluente)
                                 almeno uno dei due deve essere valorizzato, altrimenti
                                 la regola varrebbe per chiunque (vedi CK_AAR_Match)
      ScopeAllDepartments        1 = vede tutti i CdC, 0 = solo il proprio
      MaxSubordinateFunctionCode vede i dipendenti con FunctionCode < questo valore;
                                 NULL = nessun limite
      Exclusions                 CdcId esclusi dall'ambito (tabella figlia)

    Idempotente: puo' essere rieseguito.
*/

SET NOCOUNT ON;
GO

-- ─────────────────────────────────────────────────────────────────────────
-- Tabelle
-- ─────────────────────────────────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM Employee.sys.tables t
               INNER JOIN Employee.sys.schemas s ON s.schema_id = t.schema_id
               WHERE t.name = 'AbsenceAuthorizationRules' AND s.name = 'dbo')
BEGIN
    CREATE TABLE Employee.dbo.AbsenceAuthorizationRules (
        RuleId                      INT IDENTITY(1,1) NOT NULL,
        RuleName                    NVARCHAR(80)  NOT NULL,
        MatchFunctionCode           INT           NULL,
        MatchSubCdcId               INT           NULL,
        ScopeAllDepartments         BIT           NOT NULL CONSTRAINT DF_AAR_Scope   DEFAULT (0),
        MaxSubordinateFunctionCode  INT           NULL,
        Priority                    INT           NOT NULL,
        Notes                       NVARCHAR(400) NULL,
        DateIn                      DATETIME      NOT NULL CONSTRAINT DF_AAR_DateIn  DEFAULT (GETDATE()),
        DateOut                     DATETIME      NULL,
        CONSTRAINT PK_AbsenceAuthorizationRules PRIMARY KEY (RuleId),
        -- Una regola senza alcun criterio combacerebbe con qualunque utente:
        -- meglio impedirlo a livello di schema.
        CONSTRAINT CK_AAR_Match CHECK (MatchFunctionCode IS NOT NULL OR MatchSubCdcId IS NOT NULL)
    );
    PRINT 'Creata Employee.dbo.AbsenceAuthorizationRules';
END
ELSE
    PRINT 'Employee.dbo.AbsenceAuthorizationRules gia'' presente';
GO

IF NOT EXISTS (SELECT 1 FROM Employee.sys.tables t
               INNER JOIN Employee.sys.schemas s ON s.schema_id = t.schema_id
               WHERE t.name = 'AbsenceAuthorizationRuleExclusions' AND s.name = 'dbo')
BEGIN
    CREATE TABLE Employee.dbo.AbsenceAuthorizationRuleExclusions (
        RuleId INT NOT NULL,
        CdcId  INT NOT NULL,
        CONSTRAINT PK_AbsenceAuthorizationRuleExclusions PRIMARY KEY (RuleId, CdcId),
        CONSTRAINT FK_AARE_Rule FOREIGN KEY (RuleId)
            REFERENCES Employee.dbo.AbsenceAuthorizationRules (RuleId)
    );
    PRINT 'Creata Employee.dbo.AbsenceAuthorizationRuleExclusions';
END
ELSE
    PRINT 'Employee.dbo.AbsenceAuthorizationRuleExclusions gia'' presente';
GO

-- ─────────────────────────────────────────────────────────────────────────
-- Regole
-- ─────────────────────────────────────────────────────────────────────────
-- 10 — Amministratore (FunctionCode 100): vede tutto, nessun limite.
IF NOT EXISTS (SELECT 1 FROM Employee.dbo.AbsenceAuthorizationRules WHERE RuleName = N'Amministratore')
    INSERT INTO Employee.dbo.AbsenceAuthorizationRules
        (RuleName, MatchFunctionCode, MatchSubCdcId, ScopeAllDepartments,
         MaxSubordinateFunctionCode, Priority, Notes)
    VALUES
        (N'Amministratore', 100, NULL, 1, NULL, 10,
         N'FunctionCode 100: vede le richieste di chiunque, escluse le proprie.');

-- 20 — Risorse Umane (SubCdcId 24): vede tutto a prescindere dal FunctionCode.
--      Deve precedere la regola 40: ORMENISAN e' FC=70 e combacerebbe con entrambe.
IF NOT EXISTS (SELECT 1 FROM Employee.dbo.AbsenceAuthorizationRules WHERE RuleName = N'Risorse Umane')
    INSERT INTO Employee.dbo.AbsenceAuthorizationRules
        (RuleName, MatchFunctionCode, MatchSubCdcId, ScopeAllDepartments,
         MaxSubordinateFunctionCode, Priority, Notes)
    VALUES
        (N'Risorse Umane', NULL, 24, 1, NULL, 20,
         N'Chiunque appartenga al sotto-reparto HUMAN RESOURCES vede tutto, anche con FunctionCode basso. Prima arrivava implicitamente dalla SP GetManagerForSingleEmployee.');

-- 30 — Operation Manager (FunctionCode 90): tutti i dipartimenti tranne gli
--      amministrativi (ADMINISTRATION, PURCHASING, ACCOUNTING).
--      Vede anche i capi dipartimento (FC < 90).
IF NOT EXISTS (SELECT 1 FROM Employee.dbo.AbsenceAuthorizationRules WHERE RuleName = N'Operation Manager')
    INSERT INTO Employee.dbo.AbsenceAuthorizationRules
        (RuleName, MatchFunctionCode, MatchSubCdcId, ScopeAllDepartments,
         MaxSubordinateFunctionCode, Priority, Notes)
    VALUES
        (N'Operation Manager', 90, NULL, 1, 90, 30,
         N'FunctionCode 90: tutti i CdC tranne quelli elencati nelle esclusioni; include i capi dipartimento.');

-- 40 — Capo dipartimento (FunctionCode 70): solo il proprio CdC, sotto di se'.
IF NOT EXISTS (SELECT 1 FROM Employee.dbo.AbsenceAuthorizationRules WHERE RuleName = N'Capo dipartimento')
    INSERT INTO Employee.dbo.AbsenceAuthorizationRules
        (RuleName, MatchFunctionCode, MatchSubCdcId, ScopeAllDepartments,
         MaxSubordinateFunctionCode, Priority, Notes)
    VALUES
        (N'Capo dipartimento', 70, NULL, 0, 70, 40,
         N'FunctionCode 70: solo i dipendenti del proprio CdcId con FunctionCode < 70. Presuppone un solo FC=70 per dipartimento.');
GO

-- Esclusioni per l'Operation Manager: i dipartimenti amministrativi.
--   4  = ADMINISTRATION
--   6  = PURCHASING
--   12 = ACCOUNTING (era un sotto-reparto di ADMINISTRATION ed e' stato promosso
--        a dipartimento autonomo: senza questa riga rientrerebbe nell'ambito)
INSERT INTO Employee.dbo.AbsenceAuthorizationRuleExclusions (RuleId, CdcId)
SELECT r.RuleId, v.CdcId
FROM Employee.dbo.AbsenceAuthorizationRules r
CROSS APPLY (VALUES (4), (6), (12)) AS v(CdcId)
WHERE r.RuleName = N'Operation Manager'
  AND NOT EXISTS (
      SELECT 1 FROM Employee.dbo.AbsenceAuthorizationRuleExclusions e
      WHERE e.RuleId = r.RuleId AND e.CdcId = v.CdcId
  );
GO

-- ─────────────────────────────────────────────────────────────────────────
-- Riepilogo
-- ─────────────────────────────────────────────────────────────────────────
SELECT r.Priority, r.RuleName, r.MatchFunctionCode, r.MatchSubCdcId,
       r.ScopeAllDepartments, r.MaxSubordinateFunctionCode,
       Esclusi = STUFF((
           SELECT ', ' + cc.CdcDescription
           FROM Employee.dbo.AbsenceAuthorizationRuleExclusions e
           INNER JOIN Employee.dbo.CostCenters cc ON cc.CdcId = e.CdcId
           WHERE e.RuleId = r.RuleId
           FOR XML PATH('')), 1, 2, '')
FROM Employee.dbo.AbsenceAuthorizationRules r
WHERE r.DateOut IS NULL
ORDER BY r.Priority;
GO
