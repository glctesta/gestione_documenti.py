# Aggiornamento Progetto NPI Esistente

## ✅ Problema Risolto

**Prima** ❌:
- Progetto esiste → Messaggio "Il progetto esiste già" → Nessuna azione possibile

**Dopo** ✅:
- Progetto esiste → Domanda "Vuoi aggiornare?" → Aggiorna owner, descrizione e aggiungi documenti

## 🔧 Modifiche Implementate

### 1. Logica Aggiornamento (`config_window.py`)

```python
def _create_npi_project(self):
    # ... ottieni dati dal form ...
    
    progetto = self.npi_manager.create_progetto_npi_for_prodotto(...)
    
    if progetto:
        # Nuovo progetto creato
        messagebox.showinfo('Successo', 'Progetto creato!')
    else:
        # Progetto già esistente - CHIEDI SE AGGIORNARE
        if messagebox.askyesno(
            'Informazione',
            'Il progetto esiste già. Vuoi aggiornare i dati e aggiungere documenti?'
        ):
            existing_project = self.npi_manager.get_progetto_by_prodotto(prodotto_id)
            
            # Aggiorna dati
            update_data = {}
            if version:
                update_data['Version'] = version
            if owner_id:
                update_data['OwnerID'] = owner_id
            if descrizione:
                update_data['Descrizione'] = descrizione
            
            self.npi_manager.update_progetto_npi(existing_project.ProgettoId, update_data)
            
            # Aggiungi documenti
            for doc in self.project_documents:
                self.npi_manager.add_progetto_documento(...)
            
            messagebox.showinfo('Successo', 'Progetto aggiornato!')
```

### 2. Nuovi Metodi Manager (`npi_manager.py`)

```python
def get_progetto_by_prodotto(self, prodotto_id):
    """Recupera il progetto NPI associato a un prodotto."""
    # Ritorna il progetto esistente per quel prodotto

def update_progetto_npi(self, progetto_id, data):
    """Aggiorna i dati di un progetto NPI."""
    # Aggiorna Version, OwnerID, Descrizione, etc.
```

## 📝 Workflow Utente

### Scenario 1: Nuovo Progetto

```
1. Seleziona prodotto "Carpet Loom XYZ"
   ↓
2. Compila: Versione "1.0", Owner "Mario", Descrizione "..."
   ↓
3. Aggiungi documenti: design.png, spec.pdf
   ↓
4. Click "Crea Progetto NPI"
   ↓
5. Sistema: Progetto non esiste → CREA NUOVO
   ↓
6. Messaggio: "Progetto creato con successo" ✅
```

### Scenario 2: Progetto Esistente - Aggiornamento

```
1. Seleziona prodotto "Carpet Loom XYZ" (già ha progetto)
   ↓
2. Compila: Versione "2.0", Owner "Luigi", Descrizione "Nuova versione..."
   ↓
3. Aggiungi documenti: update_notes.pdf, new_design.png
   ↓
4. Click "Crea Progetto NPI"
   ↓
5. Sistema: Progetto esiste → CHIEDE CONFERMA
   ↓
6. Domanda: "Il progetto esiste già. Vuoi aggiornare i dati e aggiungere documenti?"
   ├─ [Sì] → Aggiorna Version, Owner, Descrizione
   │         Aggiunge 2 nuovi documenti
   │         Messaggio: "Progetto aggiornato con successo" ✅
   │
   └─ [No] → Nessuna azione
```

### Scenario 3: Progetto Esistente - Solo Documenti

```
1. Seleziona prodotto "Carpet Loom XYZ" (già ha progetto)
   ↓
2. NON compila versione, owner, descrizione
   ↓
3. Aggiungi documenti: photo1.jpg, photo2.jpg
   ↓
4. Click "Crea Progetto NPI"
   ↓
5. Sistema: Progetto esiste → CHIEDE CONFERMA
   ↓
6. Domanda: "Vuoi aggiornare..."
   ├─ [Sì] → NON aggiorna dati (campi vuoti)
   │         Aggiunge solo 2 documenti
   │         Messaggio: "Progetto aggiornato con successo" ✅
   │
   └─ [No] → Nessuna azione
```

## 🔑 Traduzioni Aggiunte

File: `.artifacts/sql_translations_project_update.sql`

| Chiave | IT | EN |
|--------|----|----|
| `msg_project_exists_update` | Il progetto esiste già. Vuoi aggiornare i dati (owner, descrizione) e aggiungere documenti? | Project already exists. Do you want to update data (owner, description) and add documents? |
| `msg_project_updated` | Progetto aggiornato con successo | Project updated successfully |

## ✅ Vantaggi

1. **Flessibilità**: Puoi aggiornare progetti esistenti senza ricrearli
2. **Documenti Incrementali**: Aggiungi documenti a progetti già creati
3. **Sicurezza**: Chiede sempre conferma prima di modificare
4. **Dati Opzionali**: Aggiorna solo i campi compilati

## 📋 Checklist

- [x] Modificato `_create_npi_project` in `config_window.py`
- [x] Aggiunto `get_progetto_by_prodotto` in `npi_manager.py`
- [x] Aggiunto `update_progetto_npi` in `npi_manager.py`
- [x] Creato script traduzioni `sql_translations_project_update.sql`
- [ ] Eseguire script traduzioni nel database
- [ ] Testare aggiornamento progetto esistente

---

**Data**: 23 Dicembre 2024  
**Versione**: 2.2.8.1  
**Stato**: ✅ Implementato - Richiede Test
