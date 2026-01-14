# Risoluzione Problema: EXE non parte (processo in background senza GUI)

## 🔍 Problema Identificato

L'applicazione compilata con PyInstaller:
- **Parte come processo** (visibile nel Task Manager)
- **Non mostra l'interfaccia grafica** (finestra Tkinter)
- **Nessun errore visibile** all'utente

## ⚠️ Cause Principali

### 1. **File Mancanti nel Bundle PyInstaller**
Il file `.spec` originale includeva solo `logo.png`, ma l'applicazione richiede:
- **Font TrueType**: `DejaVuSans.ttf`, `DejaVuSans-Bold.ttf`
- **Immagini**: `Logo.png`, `Frigo_acclimate.jpg`
- **File di configurazione**: `config.ini`, `lang.conf`, ecc.
- **Chiavi di encryption**: `email_credentials.enc`, `email_key.key`

### 2. **Console Disabilitata**
Il parametro `console=False` nel file `.spec` nasconde tutti gli errori di avvio, rendendo impossibile il debug.

### 3. **Hidden Imports Mancanti**
Moduli importati dinamicamente non vengono inclusi automaticamente:
- `PIL` e suoi sottomoduli
- `sqlalchemy.pool`
- `packaging.version`
- `reportlab` e suoi sottomoduli
- `pandas`, `matplotlib`

## ✅ Soluzione Implementata

### Modifica al file `main.spec`:

```python
# 1. INCLUSIONE FILE DATI
datas_list = []
files_to_include = [
    'Logo.png', 'logo.png', 'Logo.ico',
    'DejaVuSans.ttf', 'DejaVuSans-Bold.ttf',
    'Frigo_acclimate.jpg',
    'config.ini', 'lang.conf',
    'email_credentials.enc', 'email_key.key',
    'zebra_printer_config.json'
]

for file in files_to_include:
    if os.path.exists(file):
        datas_list.append((file, '.'))

# 2. INCLUSIONE DIRECTORY NPI
if os.path.exists('npi'):
    datas_list.append(('npi', 'npi'))

# 3. HIDDEN IMPORTS COMPLETI
hiddenimports=[
    'pyodbc', 'PIL', 'PIL.Image', 'PIL.ImageTk',
    'sqlalchemy', 'sqlalchemy.pool',
    'packaging', 'packaging.version',
    'tkcalendar', 'pandas', 'matplotlib',
    'reportlab', 'reportlab.pdfgen', 'reportlab.lib',
    'reportlab.platypus', 'reportlab.pdfbase.ttfonts',
]

# 4. CONSOLE ABILITATA (TEMPORANEAMENTE PER DEBUG)
console=True  # Cambiare a False dopo il debug
```

### Ricompilazione:
```powershell
pyinstaller --clean main.spec
```

## 🐛 Come Debuggare in Futuro

### 1. **Abilitare la Console Temporaneamente**
Nel file `.spec`, impostare `console=True` per vedere gli errori di avvio.

### 2. **Verificare i Log**
L'applicazione scrive log in:
- `%LOCALAPPDATA%\TraceabilityRS\logs\traceability_rs.log`
- `%LOCALAPPDATA%\TraceabilityRS\logs\stdout.log`
- `%LOCALAPPDATA%\TraceabilityRS\logs\stderr.log`

### 3. **Eseguire l'EXE da PowerShell**
```powershell
# Esegui da terminale per catturare output
.\dist\main\main.exe
```

### 4. **Verificare File Inclusi**
Dopo la compilazione, controllare la cartella `dist\main\` per verificare che tutti i file siano presenti.

## 📋 Checklist Pre-Compilazione

Prima di compilare con PyInstaller:

- [ ] Tutti i file di risorse (immagini, font, config) esistono nella directory principale
- [ ] Il file `.spec` include tutti i file nelle `datas`
- [ ] Tutti i `hiddenimports` sono specificati
- [ ] `console=True` per la prima compilazione (debug)
- [ ] Testare l'exe in un ambiente pulito
- [ ] Dopo conferma funzionamento, impostare `console=False`

## 🔧 Comando di Build Finale

```powershell
# 1. Clean build precedente
pyinstaller --clean main.spec

# 2. Testare con console=True
.\dist\main\main.exe

# 3. Se tutto funziona, rimuovere console
#    Modificare main.spec: console=False
#    Ricompilare: pyinstaller main.spec
```

## 📝 Note Importanti

- **Percorsi relativi**: Il codice usa `os.path.exists("logo.png")` che funziona solo se i file sono nella directory corrente dell'exe
- **Icona**: Aggiunta `icon='Logo.ico'` all'exe
- **UPX**: Compressione abilitata per ridurre dimensioni
- **Directory NPI**: Inclusa interamente per il modulo NPI Manager

## 🎯 Risultato Atteso

Dopo la ricompilazione:
- L'exe mostra una **finestra console** (temporaneamente)
- Eventuali **errori sono visibili** nella console
- L'interfaccia Tkinter **si apre correttamente**
- Tutti i **file di risorse sono accessibili**
