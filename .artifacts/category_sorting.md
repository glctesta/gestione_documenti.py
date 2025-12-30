# Ordinamento Alfabetico delle Categorie

## Modifica Implementata

Le categorie nel combobox del tab "Catalogo Task" sono ora ordinate **alfabeticamente** per facilitare la ricerca.

## File Modificato

**`npi/windows/config_window.py`** - Metodo `_load_categories_for_combobox()`

## Comportamento

### Prima
```
Combobox Categorie:
├─ Tutte le categorie
├─ 
├─ Design
├─ Pilot run preparation
├─ Materials procurement
├─ Testing
└─ Quality assurance
```
*(Ordine casuale basato su NrOrdin)*

### Dopo
```
Combobox Categorie:
├─ Tutte le categorie
├─ 
├─ Design
├─ Materials procurement
├─ Pilot run preparation
├─ Quality assurance
└─ Testing
```
*(Ordine alfabetico)*

## Implementazione

```python
# Ordina alfabeticamente le categorie
sorted_categories = sorted(self.category_map.keys())

# Costruisci la lista con "Tutte" all'inizio, poi le categorie ordinate
category_values = [all_categories_label, ""] + sorted_categories
```

## Dove si Applica

Questa modifica si applica a **due combobox**:

1. **Filtro Categoria** (in alto nella finestra)
   - Usato per filtrare i task visualizzati nella lista

2. **Categoria del Task** (nel form di dettaglio)
   - Usato quando si crea o modifica un task

Entrambi usano lo stesso metodo `_load_categories_for_combobox()`, quindi l'ordinamento alfabetico è applicato automaticamente a entrambi.

## Note

- L'opzione **"Tutte le categorie"** rimane sempre **prima** nell'elenco
- L'ordinamento è **case-sensitive** (maiuscole prima delle minuscole)
- Se tutte le categorie iniziano con la maiuscola, l'ordine sarà puramente alfabetico
