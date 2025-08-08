import pyodbc
import os

# --- CONFIGURAZIONE ---
# Usa la stessa stringa di connessione della tua applicazione principale
DB_CONN_STR = (
    "DRIVER={SQL Server Native Client 11.0};"
    "SERVER=roghipsql01.vandewiele.local\\emsreset;"
    "DATABASE=Traceability_rs;"
    "UID=emsreset;"
    "PWD=E6QhqKUxHFXTbkB7eA8c9ya;"
)

# Nome della tabella e delle colonne
TABLE_NAME = "Traceability_RS.dbo.ProductDocuments"
ID_COLUMN = "DocumentProductionId"  # Assumendo che tu abbia una chiave primaria chiamata ID
PATH_COLUMN = "DocumentPath"  # La tua vecchia colonna con i percorsi
BINARY_COLUMN = "DocumentData"  # La nuova colonna VARBINARY(MAX)


def migrare_pdf_a_db():
    """
    Legge i percorsi dei file dal DB, carica i file e aggiorna
    il record con i dati binari.
    """
    conn = None
    migrati = 0
    errori = 0

    try:
        conn = pyodbc.connect(DB_CONN_STR)
        cursor = conn.cursor()

        # 1. Seleziona tutti i record che hanno un percorso ma non ancora i dati binari
        query_select = f"""
            SELECT {ID_COLUMN}, {PATH_COLUMN} 
            FROM {TABLE_NAME} 
            WHERE {PATH_COLUMN} IS NOT NULL 
              AND LTRIM(RTRIM({PATH_COLUMN})) <> ''
              AND {BINARY_COLUMN} IS NULL
        """
        print("Recupero dei percorsi dei documenti dal database...")
        cursor.execute(query_select)
        rows = cursor.fetchall()

        if not rows:
            print("Nessun documento da migrare trovato.")
            return

        print(f"Trovati {len(rows)} documenti da migrare. Inizio del processo...")

        # 2. Itera su ogni riga
        for row in rows:
            doc_id = row[0]
            file_path = row[1]

            print(f"\nElaborazione ID: {doc_id} -> Percorso: {file_path}")

            try:
                # 3. Controlla se il file esiste prima di provare a leggerlo
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Il file non esiste al percorso specificato.")

                # 4. Leggi il contenuto del file in modalità binaria
                with open(file_path, 'rb') as f:
                    binary_data = f.read()

                # 5. Aggiorna il record nel database con i dati binari
                query_update = f"UPDATE {TABLE_NAME} SET {BINARY_COLUMN} = ? WHERE {ID_COLUMN} = ?"
                cursor.execute(query_update, binary_data, doc_id)
                conn.commit()  # Salva la modifica per questo file

                print(f"✅ Successo: Documento ID {doc_id} migrato.")
                migrati += 1

            except FileNotFoundError as e:
                print(f"❌ ERRORE (File non trovato): {e}. Salto questo record.")
                errori += 1
            except Exception as e:
                print(f"❌ ERRORE (Generico): Impossibile elaborare l'ID {doc_id}. Dettagli: {e}. Salto questo record.")
                errori += 1

    except pyodbc.Error as e:
        print(f"Errore di connessione al database: {e}")
    finally:
        if conn:
            conn.close()
        print("\n--- Migrazione Completata ---")
        print(f"Documenti migrati con successo: {migrati}")
        print(f"Documenti saltati per errori: {errori}")


# Esegui la funzione di migrazione
if __name__ == "__main__":
    migrare_pdf_a_db()