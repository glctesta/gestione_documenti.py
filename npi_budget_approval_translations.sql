-- ============================================================
-- NPI Budget Approval Translations
-- Languages: IT, RO (N''), EN, SV, DE
-- ============================================================
USE Traceability_RS
GO

-- budget_btn_approve_rows
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_approve_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_approve_rows','🔔 Approva Righe');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_approve_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_approve_rows',N'🔔 Aprobă Rânduri');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_approve_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_approve_rows','🔔 Approve Rows');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_approve_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_approve_rows','🔔 Godkänn Rader');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_approve_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_approve_rows','🔔 Zeilen genehmigen');
GO

-- budget_btn_approve_all
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_btn_approve_all')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_btn_approve_all','📋 Approva Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_btn_approve_all')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_btn_approve_all',N'📋 Aprobă Buget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_btn_approve_all')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_btn_approve_all','📋 Approve Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_btn_approve_all')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_btn_approve_all','📋 Godkänn Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_btn_approve_all')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_btn_approve_all','📋 Budget genehmigen');
GO

-- budget_approve_select_rows
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approve_select_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approve_select_rows','Selezionare una o più righe da approvare.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approve_select_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approve_select_rows',N'Selectați unul sau mai multe rânduri de aprobat.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approve_select_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approve_select_rows','Select one or more rows to approve.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approve_select_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approve_select_rows','Välj en eller fler rader att godkänna.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approve_select_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approve_select_rows','Wählen Sie eine oder mehrere Zeilen zur Genehmigung.');
GO

-- budget_approve_rows_confirm
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approve_rows_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approve_rows_confirm','Inviare richiesta di approvazione per {count} riga/e?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approve_rows_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approve_rows_confirm',N'Trimiteți cerere de aprobare pentru {count} rând(uri)?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approve_rows_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approve_rows_confirm','Send approval request for {count} row(s)?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approve_rows_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approve_rows_confirm','Skicka godkännandebegäran för {count} rad(er)?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approve_rows_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approve_rows_confirm','Genehmigungsanfrage für {count} Zeile(n) senden?');
GO

-- budget_approve_all_confirm
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approve_all_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approve_all_confirm','Inviare richiesta di approvazione per l''intero budget?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approve_all_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approve_all_confirm',N'Trimiteți cerere de aprobare pentru întregul buget?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approve_all_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approve_all_confirm','Send approval request for the entire budget?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approve_all_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approve_all_confirm','Skicka godkännandebegäran för hela budgeten?');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approve_all_confirm')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approve_all_confirm','Genehmigungsanfrage für das gesamte Budget senden?');
GO

-- budget_approve_sent
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approve_sent')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approve_sent','Richiesta di approvazione inviata con successo.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approve_sent')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approve_sent',N'Cererea de aprobare a fost trimisă cu succes.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approve_sent')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approve_sent','Approval request sent successfully.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approve_sent')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approve_sent','Godkännandebegäran skickad.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approve_sent')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approve_sent','Genehmigungsanfrage erfolgreich gesendet.');
GO

-- npi_budget_approver_enable / disable
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='npi_budget_approver_enable')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','npi_budget_approver_enable','✅ Abilita PC Approvazione Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='npi_budget_approver_enable')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','npi_budget_approver_enable',N'✅ Activează PC Aprobare Buget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='npi_budget_approver_enable')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','npi_budget_approver_enable','✅ Enable Budget Approval PC');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='npi_budget_approver_enable')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','npi_budget_approver_enable','✅ Aktivera Budgetgodkännande-PC');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='npi_budget_approver_enable')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','npi_budget_approver_enable','✅ Budget-Genehmigungs-PC aktivieren');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='npi_budget_approver_disable')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','npi_budget_approver_disable','❌ Disabilita PC Approvazione Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='npi_budget_approver_disable')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','npi_budget_approver_disable',N'❌ Dezactivează PC Aprobare Buget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='npi_budget_approver_disable')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','npi_budget_approver_disable','❌ Disable Budget Approval PC');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='npi_budget_approver_disable')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','npi_budget_approver_disable','❌ Avaktivera Budgetgodkännande-PC');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='npi_budget_approver_disable')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','npi_budget_approver_disable','❌ Budget-Genehmigungs-PC deaktivieren');
GO

-- npi_budget_approver_enabled_msg / disabled_msg
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='npi_budget_approver_enabled_msg')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','npi_budget_approver_enabled_msg','Questo PC è ora configurato come approvatore budget NPI.
Il monitor è attivo.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='npi_budget_approver_enabled_msg')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','npi_budget_approver_enabled_msg',N'Acest PC este acum configurat ca aprobator buget NPI.
Monitorul este activ.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='npi_budget_approver_enabled_msg')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','npi_budget_approver_enabled_msg','This PC is now configured as NPI budget approver.
The monitor is active.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='npi_budget_approver_enabled_msg')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','npi_budget_approver_enabled_msg','Denna dator är nu konfigurerad som NPI-budgetgodkännare.
Monitorn är aktiv.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='npi_budget_approver_enabled_msg')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','npi_budget_approver_enabled_msg','Dieser PC ist jetzt als NPI-Budgetgenehmiger konfiguriert.
Der Monitor ist aktiv.');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='npi_budget_approver_disabled_msg')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','npi_budget_approver_disabled_msg','Questo PC non è più configurato come approvatore budget NPI.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='npi_budget_approver_disabled_msg')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','npi_budget_approver_disabled_msg',N'Acest PC nu mai este configurat ca aprobator buget NPI.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='npi_budget_approver_disabled_msg')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','npi_budget_approver_disabled_msg','This PC is no longer configured as NPI budget approver.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='npi_budget_approver_disabled_msg')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','npi_budget_approver_disabled_msg','Denna dator är inte längre konfigurerad som NPI-budgetgodkännare.');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='npi_budget_approver_disabled_msg')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','npi_budget_approver_disabled_msg','Dieser PC ist nicht mehr als NPI-Budgetgenehmiger konfiguriert.');
GO

-- Approval monitor popup labels
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approval_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approval_title','💰 Nuova Richiesta Approvazione Budget!');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approval_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approval_title',N'💰 Nouă Cerere Aprobare Buget!');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approval_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approval_title','💰 New Budget Approval Request!');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approval_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approval_title','💰 Ny Begäran om Budgetgodkännande!');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approval_title')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approval_title','💰 Neue Budgetgenehmigungsanfrage!');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approval_rejection_note')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approval_rejection_note','Nota rifiuto (opzionale)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approval_rejection_note')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approval_rejection_note',N'Notă respingere (opțional)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approval_rejection_note')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approval_rejection_note','Rejection note (optional)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approval_rejection_note')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approval_rejection_note','Avvisningsnotering (valfritt)');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approval_rejection_note')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approval_rejection_note','Ablehnungshinweis (optional)');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approval_btn_approve')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approval_btn_approve','✅ Approva');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approval_btn_approve')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approval_btn_approve',N'✅ Aprobă');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approval_btn_approve')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approval_btn_approve','✅ Approve');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approval_btn_approve')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approval_btn_approve','✅ Godkänn');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approval_btn_approve')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approval_btn_approve','✅ Genehmigen');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approval_btn_reject')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approval_btn_reject','❌ Rifiuta');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approval_btn_reject')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approval_btn_reject',N'❌ Respinge');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approval_btn_reject')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approval_btn_reject','❌ Reject');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approval_btn_reject')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approval_btn_reject','❌ Avvisa');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approval_btn_reject')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approval_btn_reject','❌ Ablehnen');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approval_btn_later')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approval_btn_later','⏳ Dopo');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approval_btn_later')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approval_btn_later',N'⏳ Mai târziu');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approval_btn_later')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approval_btn_later','⏳ Later');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approval_btn_later')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approval_btn_later','⏳ Senare');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approval_btn_later')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approval_btn_later','⏳ Später');
GO

-- budget_approval_type_rows / type_budget
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approval_type_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approval_type_rows','Righe selezionate');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approval_type_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approval_type_rows',N'Rânduri selectate');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approval_type_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approval_type_rows','Selected rows');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approval_type_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approval_type_rows','Valda rader');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approval_type_rows')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approval_type_rows','Ausgewählte Zeilen');
GO

IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='it' AND TranslationKey='budget_approval_type_budget')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('it','budget_approval_type_budget','Intero Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='ro' AND TranslationKey='budget_approval_type_budget')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('ro','budget_approval_type_budget',N'Întregul Buget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='en' AND TranslationKey='budget_approval_type_budget')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('en','budget_approval_type_budget','Entire Budget');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='sv' AND TranslationKey='budget_approval_type_budget')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('sv','budget_approval_type_budget','Hela Budgeten');
IF NOT EXISTS (SELECT 1 FROM dbo.AppTranslations WHERE LanguageCode='de' AND TranslationKey='budget_approval_type_budget')
INSERT INTO dbo.AppTranslations (LanguageCode, TranslationKey, TranslationValue) VALUES ('de','budget_approval_type_budget','Gesamtes Budget');
GO

PRINT '✅ Traduzioni Approvazione Budget NPI completate'
GO
