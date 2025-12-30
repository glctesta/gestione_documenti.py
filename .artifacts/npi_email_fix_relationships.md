# Fix: Notifiche Email Task NPI - Errore Relationships

## ❌ Problema

```
AttributeError: type object 'TaskProdotto' has no attribute 'predecessors'
```

## 🔍 Causa

Il model `TaskProdotto` non aveva le relationships `predecessors` e `successors` definite, necessarie per caricare le dipendenze del task nell'email di notifica.

## ✅ Soluzione

### 1. Aggiornato Model `TaskProdotto` (`data_models.py`)

```python
class TaskProdotto(Base):
    # ... campi esistenti ...
    
    # Relationships esistenti
    dependencies = relationship("TaskDependency", ...)
    
    # NUOVE relationships aggiunte
    predecessors = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.TaskProdottoID",
        back_populates="task",
        overlaps="dependencies"
    )
    successors = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.DependsOnTaskProdottoID",
        overlaps="depends_on_task"
    )
```

### 2. Corretto Nomi Campi in `_format_task_dependencies`

**Prima** ❌:
```python
dep_task_id = dep.SuccessorTaskID if is_successor else dep.PredecessorTaskID
```

**Dopo** ✅:
```python
dep_task_id = dep.TaskProdottoID if is_successor else dep.DependsOnTaskProdottoID
```

## 📊 Schema Dipendenze

### Tabella `TaskDependencies`

```
DependencyID (PK)
TaskProdottoID (FK) ────→ Task che dipende
DependsOnTaskProdottoID (FK) ────→ Task da cui dipende
```

### Esempio

```
Task A dipende da Task B:
- TaskProdottoID = A
- DependsOnTaskProdottoID = B

Quindi:
- A.predecessors → contiene la dipendenza (A dipende da B)
- B.successors → contiene la dipendenza (B è richiesto da A)
```

## 🔄 Logica Corretta

```python
# Per un task X:

# Predecessori (task da cui X dipende)
for dep in X.predecessors:
    task_da_cui_dipendo = dep.DependsOnTaskProdottoID
    # X deve aspettare che questo task sia completato

# Successori (task che dipendono da X)
for dep in X.successors:
    task_che_dipende_da_me = dep.TaskProdottoID
    # Questo task deve aspettare che X sia completato
```

## ✅ Risultato

Ora le notifiche email includono correttamente:

- **Predecessori**: Task che devono essere completati prima
- **Successori**: Task che aspettano il completamento di questo

---

**Data**: 23 Dicembre 2024  
**Versione**: 2.2.8.1  
**Stato**: ✅ Corretto - Pronto per Test
