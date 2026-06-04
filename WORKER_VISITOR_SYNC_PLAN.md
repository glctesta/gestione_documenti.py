# Piano Implementazione Worker in Tab Dati Ospite

## Obiettivo
Introdurre nella form aperta da open_guest_management_with_login, tab Dati Ospiti, un checkbox Worker (default disabilitato = 0).

Quando Worker = 1 e si salva l'ospite:
- aggiornare i dati ospite in Employee.dbo.VisitorData (come oggi)
- mantenere la logica badge (come oggi)
- sincronizzare il nominativo anche in Timeclocking.dbo.Employee secondo le regole richieste.

## Ambito Modifiche
File principale:
- guest_management_gui.py

Punti previsti:
- UI tab Dati Ospiti (_build_guests_tab)
- caricamento selezione ospite (_on_guest_selected)
- salvataggio ospite (_save_guest_data)
- nuovi helper privati per sync Timeclocking

## Regole Funzionali Richieste
1. Nuovo checkbox Worker in tab Dati Ospiti.
1. Stato default: 0 (non selezionato).
1. Se Worker non selezionato: nessuna operazione su Timeclocking.dbo.Employee.
1. Se Worker selezionato:
- chiedere conferma all'operatore che e' situro che l'ospite abia accesso al sistema di tracciabilita'. Se si allora si prosegue. se non il checkbox sara' settato nuovamente =0.
- ricavare la visita attiva/futura da Employee.dbo.Visitors per VisitorDataId selezionato
- verificare/creare Company in Timeclocking.dbo.Company usando CompanyName = Visitors.CompanyName
- verificare presenza in Timeclocking.dbo.Employee con CompanyID = Visitors.VisitorId
- se presente e DataStop IS NOT NULL:
  - impostare DataStop = NULL
- se non presente: inserire nuovo record Timeclocking.dbo.Employee con campi mappati.

## Mapping Dati verso Timeclocking.dbo.Employee
Origine visita: Employee.dbo.Visitors (record selezionato per VisitorDataId).

- IDEmployee: auto (identity)
- EmployeeName: prima parola di GuestName
- EmployeeSurname: resto della stringa dopo il primo spazio
- UniqueID: valore univoco con prefisso FK + 12 cifre numeriche
- CompanyID: Visitors.VisitorId
- Department: Production
- Profession: TRAINER
- DataStart: Visitors.StartVisit
- DataStop: NULL
- CodeBadge: NoBadge (numero badge assegnato al visitatore, non BadgeId)
- DataLastImport: NULL
- EmployeeSalary: NULL
- IDCompany: Timeclocking.dbo.Company.IDCompany (risolto per CompanyName)
- IDTeam: 135
- IDProfession: 2
- IDRuleCalculationMode: NULL
- IsDirect: 0

## Mapping Dati verso Timeclocking.dbo.Company
Chiave di ricerca: CompanyName uguale a Visitors.CompanyName.

Se non esiste:
- inserire nuovo record Company con:
  - CompanyName = Visitors.CompanyName
  - CompanyCUI = progressivo 8 cifre con prefisso FK (es. FK00000001)
  - CompanyAddress = NULL (o stringa vuota, in base ai vincoli reali)
  - CompanyLogo = NULL
  - CompanyDestMail = NULL
  - IsPrimary = 0
  - IsActive = 1

## Strategia Tecnica
1. UI:
- aggiungere self.edit_worker_var = tk.BooleanVar(value=False)
- aggiungere checkbox Worker nella sezione edit del tab Dati Ospiti.

1. Caricamento ospite:
- inizialmente impostare checkbox a False
- leggere eventuale presenza attiva su Timeclocking.dbo.Employee (CompanyID = VisitorId e DataStop IS NULL) per precompilare Worker=True (opzionale consigliato)

1. Salvataggio:
- mantenere update VisitorData + save badge
- se Worker=True chiamare helper _sync_guest_worker_to_timeclocking(visitor_data_id)
- commit unico transazionale su self.db.conn; rollback totale su errore

1. Helper da introdurre:
- _get_active_or_future_visit_for_worker(visitor_data_id)
- _split_guest_name(full_name) -> (name, surname)
- _get_or_create_timeclocking_company(company_name)
- _generate_next_fk_code(table, column, digits)
- _get_assigned_badge_code(visitor_data_id, reference_date)
- _upsert_timeclocking_employee_from_visitor(visit_row, badge_code)

## Gestione Codici Progressivi FK
CompanyCUI (FK + 8 cifre) e UniqueID (FK + 12 cifre):
- leggere codici esistenti con prefisso FK
- estrarre parte numerica valida
- prendere max + 1
- formattare con zeri a sinistra

Esempi:
- FK00000001 (8 cifre)
- FK000000000001 (12 cifre)

## Validazioni e Casi Limite
1. GuestName vuoto o senza cognome:
- nome = prima parola disponibile
- cognome = stringa uguale al nome (non puo' essere NULL)

1. Nessuna visita attiva/futura per VisitorDataId:
- bloccare sync worker con errore esplicito

1. Badge non assegnato:
- CodeBadge = NULL (salvataggio consentito) solo se il checkbox Worker e' =0

1. CompanyName nullo:
- bloccare sync worker con errore esplicito

1. Record Employee già esistente e attivo (DataStop NULL):
- nessun insert, eventuale update campi tecnici se necessario

## Query Chiave (da implementare)
1. Visita attiva/futura per VisitorDataId.
1. Lookup/insert in Timeclocking.dbo.Company.
1. Lookup Employee per CompanyID = VisitorId.
1. Insert/Update Timeclocking.dbo.Employee.
1. Update DataStop in Timeclocking.dbo.Employee con EndVisit di Employee.dbo.Visitors nella logica background.

## Piano Test
1. Worker=0: salva ospite, nessuna modifica su Timeclocking.
1. Worker=1 con Company esistente e Employee non esistente: insert Employee.
1. Worker=1 con Company non esistente: insert Company + insert Employee.
1. Worker=1 con Employee esistente DataStop non NULL: DataStop->NULL.
1. Verifica parsing nome/cognome da GuestName con 1 parola e con piu parole.
1. Verifica badge CodeBadge valorizzato con NoBadge.

## Rischi
1. Ambiguita semantica di CompanyID in Timeclocking.dbo.Employee (usato come VisitorId su richiesta).
1. Possibili vincoli NOT NULL aggiuntivi su Timeclocking.dbo.Company/Employee non documentati.
1. Concorrenza sui progressivi FK in accessi simultanei.

## background
1. il sistema gia' verifica la data endvisit per i visitatori e , in determinate condizioni esegue altre operazioni, dobbiamo aggiungere anche l'update del campo DataStop della tabella Timeclocking.dbo.Employee con data EndVisit della tabella Visitors.

## Conferma Richiesta Prima di Procedere
Implementazione in codice in attesa di tua conferma.
