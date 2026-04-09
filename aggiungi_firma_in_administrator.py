import pyodbc

# Connetti al database
connection = pyodbc.connect(
    r"DRIVER={SQL Server Native Client 11.0};"
    r"SERVER=roghipsql01.vandewiele.local\emsreset;"
    r"DATABASE=employee;"
    r"UID=emsreset;"
    r"PWD=E6QhqKUxHFXTbkB7eA8c9ya;"
)

cursor = connection.cursor()

# Leggi il file JPG (usa r"..." per i percorsi Windows)
with open(r"C:\Users\gtesta\OneDrive - Vandewiele\Documents GT\firmapersonale.jpg", "rb") as file:
    binary_data = file.read()

# Aggiorna la firma nella tabella
sql = "UPDATE employee.dbo.Administrators SET Firma = ? WHERE AdminId = ?"
administrator_id = 7  # <-- Cambia con l'ID corretto
cursor.execute(sql, (binary_data, administrator_id))

# Conferma l'inserimento
connection.commit()

print("Immagine caricata con successo!")

# Chiudi la connessione
cursor.close()
connection.close()