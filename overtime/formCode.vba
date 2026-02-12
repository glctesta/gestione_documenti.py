Option Compare Database
Dim DataInizioMese, DataFineMese As Date
Dim Justify As String

Private Sub Badge_AfterUpdate()
On Error GoTo Errori

If VerificaEssenziali = 0 Then
    Me.Badge.Value = ""
    Exit Sub
End If

Select Case CLng(Me.cboMotivo.Column(0))
    Case Is = 1 Or 7 Or 8
    
        If Len(Nz(Me.ListaOrdiniScelti.ListCount - 1, "")) = 0 Then
            MsgBox "You must add at least one order", vbExclamation + vbOKOnly, Intestazione()
            Exit Sub
        End If
    Case Else
    
End Select


CboMotivo_AfterUpdate

If IsNumber(Me.Badge.Value) = False Then
    MsgBox "This is not a valid Badge.", vbCritical + vbOKOnly, Intestazione()
    Me.Badge.Value = ""
    Me.cboOrdini.SetFocus
    Me.Badge.SetFocus
    GoTo Fine
End If


Me.IdSuperUser.Value = VerificaBadge2(Me.Badge.Value, 0, -1, , , -1, -1)

If Len(Nz(Me.IdSuperUser.Value, "")) = 0 Then
    MsgBox "Badge not valid.", vbCritical + vbOKOnly, Intestazione()
    Me.Badge.Value = ""
    Me.cboOrdini.SetFocus
    Me.Badge.SetFocus
    GoTo Fine
End If

DatiCapo = Split(Me.IdSuperUser.Value, ",")
Me.IdSuperUser.Value = DatiCapo(0)
Me.sesso.Value = DatiCapo(8)
Me.Dipartimento.Value = DatiCapo(3)
Me.NomeCapo.Value = DatiCapo(1)

Dim cnn As adodb.Connection
Dim RegistroId, RichiestaId As Long
Dim i As Byte

Dim Rcs As adodb.Recordset
Set Rcs = New adodb.Recordset
Set cnn = New adodb.Connection
Dim Sender As String: Sender = DLookup("[AccountingEmail]", "tbsys", "[Dataout] is null")

cnn.ConnectionString = GetCnnString(CBool(DLookup("[lWork]", "TbSys", "[dataout] Is Null")))
cnn.ConnectionTimeout = 60
cnn.Open
    Dim RichiestaOveertime As String
    
    Set Rcs = cnn.Execute("exec Registro @tipo=190, @anno=" & Year(Date) & _
             ",@data='" & Format(Date, "yyyy-mm-dd") & "',@operatore=" & CLng(DLookup("[iduid]", "TmpUser")) & ", @obj=" & IIf(Me.cboOrdini.Column(0) > 0, Me.cboOrdini.Column(0), 0) & ", @chichiama=0")
    RegistroId = Rcs.Fields(0)
    RichiestaOveertime = Rcs.Fields(1)
    
    cnn.Execute ("insert into [dbo].[ExtraTimeApproval] (IdChief,IdRegistro) VALUES (" & Me.IdUser.Value & "," & Rcs.Fields(0) & ");")
    Set Rcs = cnn.Execute("Select top 1 ExtraHourApprovalId from ExtraTimeApproval order by ExtraHourApprovalId desc;")
    
    RichiestaId = Rcs.Fields(0)
    
    
    With Me.OvertimeList
        For i = 1 To .ListCount - 1
         cnn.Execute ("INSERT INTO dbo.ExtraTimeApprovalStory (ExtraHourApprovalId,IdEmployee,Descriptionreasons,DateStart,DateEnd,SuperVisorId,Justify,IdOrder, QtyTarget) VALUES( " & _
            RichiestaId & "," & .Column(0, i) & ",N'" & Trim(.Column(2, i)) & "','" & Format(.Column(3, i), "YYYY-MM-DD HH:NN:00") & _
            "','" & Format(.Column(4, i), "YYYY-MM-DD HH:NN:00") & "'," & Me.IdSuperUser.Value & ",N'" & Replace(Nz(.Column(8, i), "N/A"), "'", " ") & "'," & IIf(.Column(5, i) = "0", "NULL", .Column(5, i)) & "," & Nz(Me.Targhet.Value, "NULL") & ");")
        Next i
    End With
    
    If Me.ListaOrdiniScelti.ListCount - 1 > 0 And MustHaveOrder = -1 Then
    With Me.ListaOrdiniScelti
        For i = 1 To .ListCount - 1
            cnn.Execute ("INSERT INTO ExtratimeOrders (IdOrder,NoQuantityToAchieve,ExtraHourApprovalId) VALUES (" & .Column(0, i) & "," & .Column(2, i) & "," & RichiestaId & ");")
        Next i
    End With
    End If
    
    'manda la richiesta via email e setta il flag ad attivo
    Me.Label31.Caption = "Over time Request: " & RichiestaOveertime
    cnn.Close

    'prepara dati per il Report di accettazione delle ore straordinarie
    
    Call CaricaDartiPerReport
    'DoCmd.OpenReport "RP_AccordoDipendentiOverTime", acViewPreview
    Dim NomeFile As String
    NomeFile = "c:\Temp\OverTimeRequest_" & Format(Now(), "ddmmyyhhnnss")
    DoCmd.OutputTo acOutputReport, "RP_AccordoDipendentiOverTime", acFormatPDF, NomeFile & ".pdf", -1

    Dim cTo, ccc, Body, Obj, Attach As String
    cTo = ReachEmailAddress(199, 1, "TO")
    ccc = ReachEmailAddress(199, 1, "cc")
    Obj = "Pending overtime request"
    Body = Greatings("English") & ",<P>there is an overtime request to approve. </br>Please access ERP and approve it (by menu: HUMAN RESIURCE->Operative on job->OverTime->Overtime approval.</P>" & CloseEmail
    Attach = NomeFile
    
    If EmailCDO(Sender, Pwd(Sender), (cTo), (Obj), (Body), (ccc), Attach, "", True) Then
        MsgBox "Management has been announced by email. Request sent.", vbOKOnly + vbInformation, Intestazione()
    Else
        MsgBox "Due to an internal error email to inform management about overtime request has not sent. Please announce management.", vbExclamation + vbOKOnly, Intestazione()
        If MsgBox("Do you want to sen d manually?", vbQuestion + vbYesNo, Intestazione()) = vbNo Then GoTo Fine
        Call ManualEmail("", "", (cTo), (Obj), (Body), (ccc), (Attach), , 0)
    End If
    
GoTo Fine

Errori:
MsgBox Err.Number & " OvertimeRequest Badge_AfterUpdate " & Err.Description, vbCritical + vbOKOnly, Intestazione()
'Resume


Fine:

Set cnn = Nothing
Set Rcs = Nothing
Me.Badge.Value = ""

End Sub

Private Sub Badge_GotFocus()
If Len(Nz(Me.Badge.Value, "")) = 0 Then Exit Sub

If VerificaEssenziali = 0 Then Exit Sub
Me.Badge.Value = ""

End Sub

Private Sub cboEmployee_AfterUpdate()
If Len(Nz(Me.CboEmployee.Column(0), "")) = 0 Then Exit Sub
If VerificaEssenziali = 0 Then
    Me.Badge.Value = ""
    Exit Sub
End If

    If Len(Nz(Me.cboMotivo.Column(0), 0)) = 0 Then Exit Sub
    If CBool(Nz(Me.cboMotivo.Column(4), 0)) = True Then
        Dim volte As Byte: volte = 0
                
Reintroduci:
        Justify = InputBox("Add more informazion about this request, please", "Add justification")
            If Len(Nz(Justify, Empty)) = 0 Then
                If volte < 3 Then
                    MsgBox "The justification box cannot be empty", vbExclamation + vbOKOnly, Intestazione()
                    volte = volte + 1
                    GoTo Reintroduci
                Else
                    MsgBox "The justification box cannot be empty, this routine has been terminated", vbCritical + vbOKOnly, Intestazione()
                    DoCmd.Close acForm, "SK_OverTimeRequest", acSaveNo
                    Exit Sub
                End If
            End If
    Else
        Justify = Empty
    End If

Me.Label18.Caption = "for " & Me.cboMotivo.Column(1)
Me.IdUser.Value = Me.CboEmployee.Column(0)

'Verifica che non abbia gia' avuto per il giorno precedente ore supplimenteare


'verifico che non sia stata gia' introdotta
Dim i As Long

'aggiungi alla lista
With Me.OvertimeList
    For i = 1 To .ListCount - 1
        If .Column(0, i) = Me.CboEmployee.Column(0) Then
            If .Column(3, i) = Format(Me.DateStart.Value, "YYYY-mm-dd") + " " & Left(Me.StartTime.Value, 2) & ":" & Right(Me.StartTime.Value, 2) Then 'Me.CboMotivo.Column(1) Then
                .RemoveItem (i)
                'Exit For
            End If
        End If
    Next i
    .AddItem Me.CboEmployee.Column(0) & ";" & Me.CboEmployee.Column(1) & " " & Me.CboEmployee.Column(2) & ";" & Me.cboMotivo.Column(1) & ";" & Format(Me.DateStart.Value, "YYYY-MM-DD") + " " & Left(Me.StartTime.Value, 2) & ":" & Right(Me.StartTime.Value, 2) & ";" & Format(Me.DateStop.Value, "YYYY-MM-DD") + " " & Left(Me.EndTime.Value, 2) & ":" & Right(Me.EndTime.Value, 2) & ";" & Nz(Me.cboOrdini.Column(0), 0) & ";" & Me.Targhet.Value & ";" & Me.IdUser.Value & ";" & Nz(Justify, Empty) & ";"
End With

Me.cboMotivo.SetFocus
Me.CboEmployee.SetFocus

Me.Badge.Enabled = True

End Sub

Private Sub cboEmployee_GotFocus()
Call CheckIntegrita
End Sub

Private Sub cboEmployee_LostFocus()

    If Len(Nz(Me.CboEmployee.Column(0), "")) > 0 Then Me.CboEmployee.BackColor = vbWhite

End Sub

Private Sub cboEmployee_NotInList(NewData As String, Response As Integer)
Dim i As Long
Dim Trovato As String
    
    For i = 0 To Me.NonPermessi.ListCount - 1
        If Trim(Me.NonPermessi.Column(2, i)) Like "*" & Trim(NewData) & "*" Then
            Trovato = Me.NonPermessi.Column(2, i) & " has " & Me.NonPermessi.Column(3, i) & " hours of overtime already!"
            Exit For
        End If
    Next i
    
    If Len(Nz(Trovato, Empty)) = 0 Then
        MsgBox "Your entry doesn't exist in data base", vbExclamation + vbOKOnly, Intestazione()
    Else
        MsgBox Trovato, vbExclamation + vbOKOnly, Intestazione()
    End If
    
    Response = 0
        Me.CboEmployee.Value = Empty
        Me.NonPermessi.SetFocus
        Me.CboEmployee.SetFocus
End Sub

Private Sub CboMotivo_AfterUpdate()
If Len(Nz(Me.cboMotivo.Column(0), "")) = 0 Then Exit Sub
End Sub

Private Sub cboOrdini_AfterUpdate()

    If Me.cboMotivo.Column(3) = -1 And VerificaIntegritaOrdine = 5 Then
        MsgBox "Cannot select 'Working on NO order' if you have to complete orders which are on late!", vbExclamation + vbOKOnly, Intestazione()
        Me.cboOrdini.Value = ""
    Else
        Me.IdOrder.Value = Nz(Me.cboOrdini.Column(0), "")
    End If
    
End Sub


Private Sub cboOrdini_LostFocus()
    cboOrdini_AfterUpdate
End Sub

Private Sub cmdAddOrder_Click()
    If Len(Nz(Me.cboOrdini.Column(0), "")) = 0 Then Exit Sub
    If VerificaSeGiaEsiste(Me.cboOrdini.Column(0)) = True Then Exit Sub
    Call InserisciNuovoOrdine
End Sub



Private Sub DateStop_AfterUpdate()
If Len(Nz(Me.DateStop, "")) = 0 Then Exit Sub
If Me.DateStop.Value < Me.DateStart.Value Then
    MsgBox "Finish overtime date cannot be lower than start overtime date.", vbExclamation + vbOKOnly, Intestazione()
    Me.DateStop.Value = ""
End If
End Sub

Private Sub EndTime_AfterUpdate()
If Len(Nz(Me.EndTime.Value, "")) < 2 Then Exit Sub

    If Len(Nz(Me.DateStop.Value, "")) = 0 Then Exit Sub

    Me.GiornoEnd.Value = GiornoDellaSettimana(Me.DateStop.Value, "EN")
    Me.GiornoEnd.ForeColor = ColoraFestivi(Me.DateStop.Value)
    Me.GiornoEnd.Value = Me.GiornoStart.Value & " " & IsNight(Left(Me.EndTime.Value, 2))
    Me.EndTime.BackColor = vbWhite

    'If Me.GiornoEnd.value <> "Saturday" Or Me.GiornoEnd.value <> "Sunday" Then
        
End Sub

Private Sub Form_Load()
Dim Icon As String
Icon = CurrentDb.Containers("Databases").Documents("Userdefined").Properties("LocalPath") & "\" & CurrentDb.Containers("Databases").Documents("Userdefined").Properties("Pics") & "\" & Trim(DLookup("[IconForm]", "Tbsys", "[dataout] is null"))
SetFormIcon Me.hwnd, Icon
Me.Image0.SizeMode = acOLESizeStretch
Me.Image0.PictureType = 1
Me.Image0.Picture = Trim(DLookup("[LogoPath]", "TbSys", "[dataout] is null"))
Me.RecordSelectors = False
Me.NavigationButtons = False
Me.FormHeader.BackColor = vbWhite
Me.Image0.Width = 2081
Me.Image0.Height = 800
StartTime = Format(DateAdd("H", 8, Now()), "HH:00")
Me.EndTime.SetFocus
Me.Label18.Caption = Empty
Dim volte As Byte



If VerificaSeHaEmail(DLookup("[UID]", "TmpUser")) = 0 Then
    MsgBox "Your Email is stored into DB. You must add your email address before move on.", vbExclamation + vbOKOnly, Intestazione()
    If volte > 2 Then
    DoCmd.Close acForm, "SK_OverTimeRequest", acSaveNo
        Exit Sub
    End If
    
    
Ripeti:
    volte = volte + 1

    If AddEmail(DLookup("[UID]", "TmpUser")) = 0 Then
       GoTo Ripeti
    End If
    
End If

With Me.OvertimeList
    .RowSource = Empty
    .AddItem "IDEMPLOY;Employee;Reason;From;To;IdOrdine;Target;RequestId;Justify;"
End With

Me.ListaOrdiniScelti.RowSource = Empty
Me.ListaOrdiniScelti.AddItem "IdPO;Order number;"
Me.Targhet.Value = 0
Me.CboEmployee.Value = Empty
Me.Label31.Caption = Empty
Me.cboMotivo.Value = Empty
Me.EndTime.Value = Empty
Me.Badge.Enabled = False
Me.cboOrdini.Value = Empty
Me.DateStart.Value = Empty
Me.DateStop.Value = Empty
Me.StartTime.Value = Empty
Me.EndTime.Value = Empty
Me.DateStart.SetFocus
Me.NonPermessi.RowSource = Empty



Call CaricaOrdini
Call NotAllowedEmployees
Call CaricaEmployee

End Sub

Private Sub CaricaEmployee()
'Dim Cnn As ADODB.Connection
'Dim Rcs, RCslcl As ADODB.Recordset
'Set RCslcl = New ADODB.Recordset
'Set Rcs = New ADODB.Recordset
'Set Cnn = New ADODB.Connection
'Cnn.ConnectionString = GetCnnString(CBool(DLookup("[lWork]", "TbSys", "[dataout] Is Null")))
'Cnn.ConnectionTimeout = 60
'Cnn.Open
DataInizioMese = Date - Day(Date) + 1: DataFineMese = Date
Me.CboEmployee.RowSource = Empty
    'pulisco la tabella locale
'    CurrentDb.Execute "Delete * from TmpEmployee;"
'    Set Rcs = Cnn.Execute("select h.EmployeeHireHistoryId,EmployeeName,EmployeeSurname,EmployeeNID from Employee.dbo.Employees E inner join employee.dbo.EmployeeHireHistory H on e.employeeId=h.EmployeeId inner join employee.dbo.Employeers r on h.employeerId=r.EmployeerId  where r.EmployeerFiscalCode COLLATE DATABASE_DEFAULT=(select Cui from tbsocieta where Idsoc=" & DLookup("[workingComp]", "TbSys", "[Dataout] is null") & ") and h.EndWorkDate is null AND NOT h.EmployeeHireHistoryId IN ( " & _
'        "SELECT IdEmployeeHireHistoryId FROM(SELECT IdEmployeeHireHistoryId,SUM(oremese) AS TotOre FROM(SELECT CAST(datestart AS DATE) AS Giorno,OS.IdEmployee AS IdEmployeeHireHistoryId,SUM(DATEDIFF(Hour,datestart,dateend)) AS Oremese FROM ExtraTimeApprovalStory OS WHERE datestart BETWEEN '" & Format(DataInizioMese, "yyyy-mm-dd") & "' AND '" & Format(DataFineMese, "yyyy-mm-dd") & "' GROUP BY IdEmployee,CAST(datestart AS DATE)) AS T GROUP BY T.IdEmployeeHireHistoryId) AS G INNER JOIN " & _
'        "Employee.dbo.EmployeeHireHistory H ON g.IdEmployeeHireHistoryId=h.EmployeeHireHistoryId INNER JOIN employee.dbo.employees E ON h.employeeid=e.EmployeeId WHERE totore>" & Me.MaxOre.Value & "); ")
'
'    RCslcl.Open "select * from TmpEmployee;", CurrentProject.Connection, adOpenDynamic, adLockOptimistic
'
'    With RCslcl
'    Do Until Rcs.EOF
'        .AddNew
'        !EmployeeId = Rcs.Fields(0)
'        !Cnp = Rcs.Fields(3)
'        !Name = Rcs.Fields(1)
'        !SurName = Rcs.Fields(2)
'        .Update
'        Rcs.MoveNext
'    Loop
'    End With
Call CaricaEmployeesGeneral

Me.CboEmployee.RowSource = "SELECT TmpEmployee.IdEmployeeHire as EmployeeId, TmpEmployee.Surname, TmpEmployee.Name FROM TmpEmployee ORDER BY TmpEmployee.Surname; "

'    Me.cboEmployee.Requery
    
GoTo Fine
Fine:
'Cnn.Close
'Set Cnn = Nothing
'Set Rcs = Nothing
'Set RCslcl = Nothing

End Sub
Private Sub CaricaOrdini()
Dim cnn As adodb.Connection
Dim Rcs, RcsLcl As adodb.Recordset
Set RcsLcl = New adodb.Recordset
Set Rcs = New adodb.Recordset
Set cnn = New adodb.Connection
cnn.ConnectionString = GetCnnString(CBool(DLookup("[lWork]", "TbSys", "[dataout] Is Null")))
cnn.ConnectionTimeout = 60
cnn.Open

    'pulisco la tabella locale
    CurrentDb.Execute "Delete * from TmpPoFatti;"
    'Set Rcs = cnn.Execute("select o.idordine,po,qtastory from tbordini o inner join tbsubordine so on o.idordine=so.idordine inner join tbprodfin pf on so.idpf=pf.idpf inner join Tbregistro r on o.idregistro = r.contatore where pf.belongto is null and dataord > '" & Format(Date - 100, "yyyy-mm-dd") & "' and r.IdRegistro IN( 21,36) and right(o.po,1) <>'e';")
    If Trim(DLookup("[SQLDataBaseNome]", "TbSys", "[Dataout] is null ")) = "Mooz" Then
        Set Rcs = cnn.Execute("USE [ResetServices] select o.idordine,po,qtastory from tbordini o inner join tbsubordine so on o.idordine=so.idordine inner join tbprodfin pf on so.idpf=pf.idpf inner join Tbregistro r on o.idregistro = r.contatore where pf.belongto is null and dataord > '" & Format(Date - 100, "yyyy-mm-dd") & "' and r.IdRegistro IN( 21,36) and right(o.po,1) <>'e';")
    Else
        Set Rcs = cnn.Execute("select o.idordine,po,qtastory from tbordini o inner join tbsubordine so on o.idordine=so.idordine inner join tbprodfin pf on so.idpf=pf.idpf inner join Tbregistro r on o.idregistro = r.contatore where pf.belongto is null and dataord > '" & Format(Date - 100, "yyyy-mm-dd") & "' and r.IdRegistro IN( 21,36) and right(o.po,1) <>'e';")
    End If
    RcsLcl.Open "select * from TmpPoFatti;", CurrentProject.Connection, adOpenDynamic, adLockOptimistic

    With RcsLcl
    Do Until Rcs.EOF
        .AddNew
        !IdPO = Rcs.Fields(0)
        !qtypoorigine = Rcs.Fields(2)
        !PO = Rcs.Fields(1)
        .Update
        Rcs.MoveNext
    Loop
        .AddNew
        !IdPO = 0
        !qtypoorigine = 0
        !PO = "Working on No ORDER"
        !Cliente = "A"
        .Update
    End With
    
    Me.cboOrdini.Requery
    
GoTo Fine
Fine:
cnn.Close
Set cnn = Nothing
Set Rcs = Nothing
Set RcsLcl = Nothing
End Sub

Private Function VerificaEssenziali() As Boolean
Dim Crt As control
VerificaEssenziali = -1
    
    For Each Crt In Me.Controls
        If Crt.Tag = "Essenziali" Then
            If Len(Nz(Crt.Value, "")) = 0 Then
                Crt.BackColor = vbRed
                VerificaEssenziali = 0
            Else
                Crt.BackColor = vbWhite
            End If
        End If
    Next
    
    If MustHaveOrder Then
        If Me.cboOrdini.Column(0) > 0 Then
            If Len(Nz(Me.Targhet.Value, "")) = 0 Then
                Me.Targhet.BackColor = vbRed
                VerificaEssenziali = 0
            Else
                Me.Targhet.BackColor = vbWhite
            End If
        End If
    End If
End Function

Private Sub ListaOrdiniScelti_DblClick(Cancel As Integer)
Dim i As Byte
    If MsgBox("Do you want to delete the selected order from overtime list request?", vbQuestion + vbYesNo + vbDefaultButton2, Intestazione()) = vbNo Then Exit Sub
    
    With Me.ListaOrdiniScelti
    For i = 0 To .ListCount - 1
        If .selected(i) = True Then
            .RemoveItem (i)
        End If
    Next i
       
    End With
End Sub

Private Sub OvertimeList_DblClick(Cancel As Integer)
With Me.OvertimeList
    If .ListCount - 1 = 0 Then Exit Sub
    .RemoveItem (.ItemsSelected(0))
End With

End Sub

Private Sub StartTime_AfterUpdate()
If Len(Nz(Me.StartTime.Value, "")) = 0 Then
    Me.StartTime.BackColor = vbRed
Else
    Me.StartTime.BackColor = vbWhite
End If
End Sub

Private Sub Targhet_AfterUpdate()
If Me.cboOrdini.Column(0) > 0 And MustHaveOrder = -1 Then
    If IsNumber(IIf(Len(Nz(Me.Targhet.Value, "")) = 0, "A", Me.Targhet.Value)) = False Then
        MsgBox "The target must be a number as a quantity to achieve during the overtime requested.", vbExclamation + vbOKOnly, Intestazione()
        Me.Targhet.Value = Empty
    End If
Else
    Me.Targhet.BackColor = vbWhite
End If
    cmdAddOrder_Click
End Sub

Private Sub Targhet_LostFocus()
If Len(Nz(Me.Targhet.Value, Empty)) > 0 Then Me.Targhet.BackColor = vbWhite
Targhet_AfterUpdate
    If CheckIntegrita Then
        cmdAddOrder_Click
    End If
End Sub

Private Function VerificaSeGiaEsiste(IdOrdne As Long) As Boolean
    Dim i As Integer
    
    VerificaSeGiaEsiste = 0
    
    With Me.ListaOrdiniScelti
    For i = 1 To .ListCount
        If CLng(Nz(.Column(0, i), 0)) = 0 Then Exit For
        If CLng(.Column(0, i)) = CLng(Me.cboOrdini.Column(0)) Then
            VerificaSeGiaEsiste = -1
            Exit For
        End If
    Next i
    
    End With
    
End Function

Private Sub InserisciNuovoOrdine()
    If CheckIntegrita = 0 Then Exit Sub
    
    Dim i As Byte
    Dim Aggiungo As Boolean: Aggiungo = -1
    
    For i = 1 To Me.ListaOrdiniScelti.ListCount - 1
        If Me.ListaOrdiniScelti.Column(0, i) = Me.cboOrdini.Column(0) Then
            Aggiungo = 0
        End If
    Next i
    
    If Aggiungo = -1 Then
        Me.ListaOrdiniScelti.AddItem Me.cboOrdini.Column(0) & ";" & Me.cboOrdini.Column(1) & ";" & Me.Targhet.Value & ";"
    End If
    
End Sub

Private Sub CaricaDartiPerReport()
CurrentDb.Execute "Delete * from TmpAccordoDipendentiOre;"
Dim DataOra As Date: DataOra = Date
Dim NumeroOreStraordiniarie As Byte

Dim i As Integer
    With Me.OvertimeList
        For i = 1 To .ListCount - 1
            NumeroOreStraordiniarie = DateDiff("H", DataOra & " " & Left(Me.StartTime.Value, 2) & ":" & Right(Me.StartTime.Value, 2), DataOra & " " & Left(Me.EndTime.Value, 2) & ":" & Right(Me.EndTime.Value, 2))
            CurrentDb.Execute "Insert into TmpAccordoDipendentiOre (Dipendente,Da_Ora_A_Ora,Motivo) VALUES ('" & _
                .Column(1, i) & "','" & Str(NumeroOreStraordiniarie) & " ore" & "','" & .Column(2, i) & "');"
        Next i
    End With
End Sub

Private Function VerificaIntegritaOrdine() As Byte
' se 0 = ordine si - quantita' si;
' se 1 = ordine no - quantita' no;
' se 2 = ordine si - quantita' no;
' se 3 = ordine no - quantita' si;
' se 4 = ordine si non importa quantita'
' se 5 = ordine no non importa quantita'

    If CLng(Nz(Me.cboOrdini.Column(0), 0)) > 0 And CLng(Nz(Me.Targhet.Value, 0)) > 0 Then
        VerificaIntegritaOrdine = 0
        Exit Function
    ElseIf CLng(Nz(Me.cboOrdini.Column(0), 0)) = 0 And CLng(Nz(Me.Targhet.Value, 0)) = 0 Then
        VerificaIntegritaOrdine = 1
        Exit Function
    ElseIf CLng(Nz(Me.cboOrdini.Column(0), 0)) > 0 And CLng(Nz(Me.Targhet.Value, 0)) = 0 Then
        VerificaIntegritaOrdine = 2
        Exit Function
    ElseIf CLng(Nz(Me.cboOrdini.Column(0), 0)) = 0 And CLng(Nz(Me.Targhet.Value, 0)) > 0 Then
        VerificaIntegritaOrdine = 3
        Exit Function
    ElseIf CLng(Nz(Me.cboOrdini.Column(0), 0)) > 0 Then
        VerificaIntegritaOrdine = 4
        Exit Function
    ElseIf CLng(Nz(Me.cboOrdini.Column(0), 0)) = 0 Then
        VerificaIntegritaOrdine = 5
    End If

End Function

Private Sub FocusSu(CosaFocalizzo As String)
Select Case CosaFocalizzo
    Case Is = "Quantita'"
        Me.cboMotivo.SetFocus
        Me.Targhet.SetFocus
    Case Is = "Ordine"
        Me.cboMotivo.SetFocus
        Me.cboOrdini.SetFocus
End Select

End Sub

Public Function CheckIntegrita() As Boolean
Dim Risultato As Byte: Risultato = VerificaIntegritaOrdine
If Me.cboMotivo.Column(3) = -1 Then
    If Risultato = 1 Then
        MsgBox "You have to add order number and quantity.", vbExclamation + vbOKOnly, Intestazione()
        Call FocusSu("Ordine")
        CheckIntegrita = 0
        Exit Function
    ElseIf Risultato = 3 Then
        MsgBox "You have to add one order at least.", vbExclamation + vbOKOnly, Intestazione()
        Call FocusSu("Ordine")
        CheckIntegrita = 0
        Exit Function
    ElseIf Risultato = 2 Then
        MsgBox "You have to add quantity.", vbExclamation + vbOKOnly, Intestazione()
        Call FocusSu("Quantita'")
        CheckIntegrita = 0
        Exit Function
    Else
        CheckIntegrita = -1
    End If
End If
End Function

Private Sub NotAllowedEmployees()
    Dim cnn As adodb.Connection
    Dim Rcs As adodb.Recordset
    DataInizioMese = (Date - Day(Date) + 1): DataFineMese = Date
    
    Set Rcs = New adodb.Recordset
    Set cnn = New adodb.Connection
    cnn.ConnectionString = GetCnnString(CBool(DLookup("[lWork]", "TbSys", "[dataout] Is Null")))
    cnn.ConnectionTimeout = 60
    cnn.Open
    DataInizioMese = Date - Day(Date) + 1: DataFineMese = Date
        Set Rcs = cnn.Execute("select maxhourspermonth  from overtimerules where dateout is null;")
        If Not Rcs.EOF Then
            Me.MaxOre.Value = Rcs.Fields(0)
        Else
            Me.MaxOre.Value = 32
        End If
        
        Set Rcs = cnn.Execute("SELECT  IdEmployeeHireHistoryId, row_number() OVER (Order by  upper(e.employeename+' '+e.employeesurname)) as NoRow, upper(e.employeename+' '+e.employeesurname) As EmployeeName, TotOre FROM(SELECT IdEmployeeHireHistoryId,SUM(oremese) AS TotOre FROM(SELECT CAST(datestart AS DATE) AS Giorno,OS.IdEmployee as IdEmployeeHireHistoryId,SUM(DATEDIFF(Hour,datestart,dateend)) AS Oremese FROM ExtraTimeApprovalStory OS WHERE datestart BETWEEN '" & Format(DataInizioMese, "yyyy-mm-dd") & "' AND '" & Format(DataFineMese, "yyyy-mm-dd") & "' GROUP BY IdEmployee,CAST(datestart AS DATE)) AS T GROUP BY T.IdEmployeeHireHistoryId) AS G inner join Employee.dbo.EmployeeHireHistory H on g.IdEmployeeHireHistoryId=h.EmployeeHireHistoryId inner join employee.dbo.employees E on h.employeeid=e.EmployeeId where totore>" & Me.MaxOre.Value & " order by e.employeename+' '+e.employeesurname;")
        
        
        With Me.NonPermessi
        .RowSource = ""
        .ColumnCount = 4
        .AddItem "EmployeeHireHistoryId;No;Employee Name;Hours"
        .ColumnHeads = True
    
        Do Until Rcs.EOF
            .AddItem Rcs.Fields(0) & ";" & Rcs.Fields(1) & ";" & Rcs.Fields(2) & ";" & Rcs.Fields(3) & ";"
            Rcs.MoveNext
        Loop
    
        End With
        
    GoTo Fine
Fine:
    cnn.Close
    Set cnn = Nothing
    Set Rcs = Nothing
    

End Sub

Private Function AddEmail(uid As String) As Byte
    Dim cnn As adodb.Connection
    Dim Rcs As adodb.Recordset
    DataInizioMese = (Date - Day(Date) + 1): DataFineMese = Date
    Dim Email As String
    
    Email = InputBox("Add the request email address, please", "Add email")
    
    If InStr(1, Email, "@") = 0 Then
        MsgBox "Email not valid!", vbExclamation + vbOKOnly, Intestazione()
        AddEmail = 0
        Exit Function
    End If
    
    
    Set Rcs = New adodb.Recordset
    Set cnn = New adodb.Connection
    cnn.ConnectionString = GetCnnString(CBool(DLookup("[lWork]", "TbSys", "[dataout] Is Null")))
    cnn.ConnectionTimeout = 60
    cnn.Open
     Set Rcs = cnn.Execute("Select IdAnga from dbo.TbUserKey where NomeUser='" & Trim(uid) & "';")
        If Rcs.EOF Or Len(Nz(Rcs.Fields(0), Empty)) = 0 Then
                MsgBox "I cannot step forward because this user '" & uid & "' isn't reaceable into Empoyee's records.", vbCritical + vbOKOnly, Intestazione()
                AddEmail = 0
        Else
    
            cnn.Execute ("update employee.dbo.EmployeeAddress set Email ='" & Email & "' Where EmployeeId = " & Rcs.Fields(0) & " and Dateout is null ;")
            AddEmail = 1
        End If
  GoTo Fine
Fine:
    cnn.Close
    Set cnn = Nothing
    Set Rcs = Nothing
    
   
    
End Function
