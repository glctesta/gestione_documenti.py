import os

radice = r"C:\Users\gtesta\PythonProjetcs"  # Correggi il percorso se necessario
cerca = "[ESCALARE MANAGEMENT]"

# Contatore per le iterazioni
contatore_iterazioni = 0

if not os.path.exists(radice):
    print(f"La directory specificata '{radice}' non esiste.")
else:
    print(f"Sto cercando nella directory: {radice}")

for root, dirs, files in os.walk(radice):
    print(f"Sto analizzando la directory: {root}")
    for name in files:
        contatore_iterazioni += 1  # Incrementa il contatore
        print(f"Iterazione {contatore_iterazioni}: Sto controllando il file {name}...")  # Stampa il progresso

        if name.endswith(".py"):
            percorso = os.path.join(root, name)
            try:
                with open(percorso, "r", encoding="utf-8", errors="ignore") as f:
                    for i, riga in enumerate(f, start=1):
                        print(f"Riga {i} del file {percorso}: {riga.strip()}")
                        if cerca in riga:
                            print(f"{percorso}:{i}: {riga.strip()}")
            except Exception as e:
                print("Errore su", percorso, e)

print(f"Ricerca completata. Numero totale di file controllati: {contatore_iterazioni}")
