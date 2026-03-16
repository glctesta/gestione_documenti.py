# Regole Progetto TraceabilityRS

## Regole di Sviluppo

Quando aggiungiamo una nuova funzione, la modifichiamo o la cancelliamo  NON devono essere alterate le altre funzionalita' del programma che NON hanno legami con la funzione in questione.
- Per le GUI tkinter: usa sempre ttk widgets, pattern LabelFrame con Treeview+Scrollbar
- I nomi delle colonne dal database vw_Soggetti sono: SoggettoId, NomeSoggetto, Email, Tipo, MSTeamsUserID
- Le email si inviano tramite `email_connector.EmailSender`, gli indirizzi multipli sono separati da `;`
- Le impostazioni si leggono da `traceability_rs.dbo.Settings` con colonna `atribute` e `value`
