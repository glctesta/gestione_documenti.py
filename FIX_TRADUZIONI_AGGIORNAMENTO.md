# Fix Traduzioni Messaggi Aggiornamento Versione

## Problema Identificato

I messaggi di notifica dell'aggiornamento mostravano i placeholder `{0}`, `{1}`, `{2}` non sostituiti correttamente con i valori effettivi (versione nuova, versione attuale, numero di rinvii).

**Esempio del problema:**
```
È disponibile una nuova versione {0}.
La versione attuale è {(1)}.  ← Placeholder malformato
Puoi ancora rinviare l'aggiornamento {2} volte.
```

## Causa del Problema

Il metodo `LanguageManager.get(key, *args)` in `main.py` è definito per ricevere:
- `key`: La chiave di traduzione
- `*args`: Gli argomenti da passare a `.format()` per sostituire i placeholder

Tuttavia, il codice lo stava chiamando in modo errato:

```python
# ERRATO ❌
message = self.lang.get(
    "optional_upgrade_message",
    "È disponibile una nuova versione ({0})...",  # ← Questo era trattato come args[0]!
    version_info.Version,                          # ← args[1]
    APP_VERSION,                                   # ← args[2]
    remaining_skips                                # ← args[3]
)
```

Il secondo parametro (il testo di default) veniva erroneamente incluso in `*args`, causando uno shift degli argomenti:
- La stringa con i placeholder corretti veniva usata come valore per `{0}`
- `version_info.Version` veniva usato per `{1}`
- `APP_VERSION` veniva usato per `{2}`
- `remaining_skips` veniva ignorato

## Soluzione Implementata

### 1. Correzione del codice in `main.py`

Rimosso il secondo parametro (testo di default) dalle chiamate a `lang.get()`:

```python
# CORRETTO ✅
message = self.lang.get(
    "optional_upgrade_message",
    version_info.Version,      # {0}
    APP_VERSION,               # {1}
    remaining_skips            # {2}
)
```

**Modifiche effettuate:**
- Riga 12044: `upgrade_required_title` - rimosso testo di default
- Righe 12047-12050: `force_upgrade_message_mandatory` - rimosso testo di default
- Righe 12055-12059: `force_upgrade_message_max_skips` - rimosso testo di default
- Righe 12088-12092: `upgrade_available_title` e `optional_upgrade_message` - rimossi testi di default

### 2. Aggiornamento traduzioni nel database

Creato e eseguito lo script `correggi_traduzioni_update.py` che ha:
- Verificato tutte le traduzioni esistenti
- Aggiornato 20 traduzioni con i placeholder corretti `{0}`, `{1}`, `{2}`
- Creato le traduzioni mancanti per tutte le lingue (IT, EN, RO, DE, SV)

**Chiavi di traduzione aggiornate:**
1. `upgrade_required_title`
2. `upgrade_available_title`
3. `force_upgrade_message_mandatory`
4. `force_upgrade_message_max_skips`
5. `optional_upgrade_message`

### 3. File SQL di riferimento

Creato il file `TRADUZIONI_AGGIORNAMENTO_VERSIONE.sql` che contiene tutti gli INSERT con le traduzioni corrette, utilizzabile per installazioni future o ripristini.

## Verifica della Soluzione

Eseguito lo script `test_simple.py` che ha confermato:
- ✅ I placeholder vengono sostituiti correttamente
- ✅ Le versioni appaiono nei posti giusti
- ✅ Il numero di rinvii rimanenti è corretto
- ✅ Nessun placeholder resta visibile nel messaggio finale

**Esempio di output corretto dopo il fix:**
```
È disponibile una nuova versione (2.3.0.0).
La versione attuale è (2.2.9.8).

Vuoi aggiornare ora?

Puoi ancora rinviare l'aggiornamento 2 volte.
```

## File Coinvolti

### Modificati:
- `main.py` - Corrette le chiamate a `lang.get()` per i messaggi di aggiornamento

### Creati:
- `TRADUZIONI_AGGIORNAMENTO_VERSIONE.sql` - Script SQL con le traduzioni corrette
- `correggi_traduzioni_update.py` - Script per aggiornare le traduzioni nel database
- `test_simple.py` - Test di verifica del fix

### Di supporto:
- `inserisci_traduzioni_update.py` - Script per inserire traduzioni iniziali
- `ispeziona_traduzioni.py` - Script per ispezionare i valori nel database
- `verifica_traduzioni_update.py` - Script di verifica completa

## Note Importanti

⚠️ **ATTENZIONE:** Il metodo `LanguageManager.get()` NON accetta un parametro "default_text". Il fallback viene gestito internamente usando la chiave stessa. Qualsiasi parametro dopo `key` viene considerato un argomento per `.format()`.

✅ **BEST PRACTICE:** Assicurarsi sempre che le traduzioni siano presenti nel database per evitare di vedere le chiavi invece dei testi formattati.

## Impatto sulla Funzionalità

Questo fix NON modifica nessun'altra funzionalità dell'applicazione:
- ✅ Il sistema di aggiornamento continua a funzionare normalmente
- ✅ `updater.py` non è stato modificato
- ✅ La logica di rinvio e aggiornamenti obbligatori rimane invariata
- ✅ Solo i messaggi mostrati all'utente sono stati corretti

## Data della Correzione

20 Gennaio 2026

---
**Sviluppatore:** Gianluca Testa
