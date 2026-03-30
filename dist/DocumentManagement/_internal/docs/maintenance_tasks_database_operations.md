# Database Operations - Maintenance Tasks Management

## Overview

This document describes all database operations (INSERT, UPDATE, DELETE) performed by the **Maintenance Tasks Management** window (`maintenance_gui.open_add_maintenance_tasks`).

**Window Access**: `Manutenzione` → `Task di Manutenzione` → `Gestione Task di Manutenzione`

---

## Database Table Modified

### Primary Table: `[Traceability_RS].[eqp].[CompitiManutenzione]`

This is the **ONLY** table directly modified by this form.

**Table Purpose**: Stores maintenance tasks/activities associated with specific equipment and programmed interventions.

---

## Database Operations

### 1. INSERT - New Maintenance Tasks

**Method**: `DatabaseManager.insert_new_maintenance_task()`

**Location**: [main.py:6584-6602](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6584-L6602)

**SQL Query**:
```sql
INSERT INTO eqp.CompitiManutenzione
(ProgrammedInterventionId, EquipmentId, Categoria, NomeCompito, DescrizioneCompito, Ordine, LinkedDocument)
VALUES (?, ?, ?, ?, ?, ?, ?)
```

**Parameters**:
- `ProgrammedInterventionId` (INT) - ID of the programmed intervention type
- `EquipmentId` (INT) - ID of the equipment/machine
- `Categoria` (NVARCHAR) - Category/general title for the task group
- `NomeCompito` (NVARCHAR) - Task name
- `DescrizioneCompito` (NVARCHAR) - Task description
- `Ordine` (INT) - Display order number
- `LinkedDocument` (VARBINARY) - Optional attached document (binary data)

**When Triggered**:
- User clicks "Salva Modifiche" button
- For each task in the list that has `id = None` (new tasks not yet in database)

**Code Reference**: [maintenance_gui.py:1976-1978](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/maintenance_gui.py#L1976-L1978)

---

### 2. UPDATE - Existing Maintenance Tasks

**Method**: `DatabaseManager.update_maintenance_task()`

**Location**: [main.py:6518-6536](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6518-L6536)

**SQL Query**:
```sql
UPDATE eqp.CompitiManutenzione
SET EquipmentId        = ?, 
    Categoria          = ?, 
    NomeCompito        = ?, 
    DescrizioneCompito = ?, 
    LinkedDocument     = ?
WHERE CompitoId = ?
```

**Parameters**:
- `EquipmentId` (INT) - ID of the equipment/machine
- `Categoria` (NVARCHAR) - Category/general title
- `NomeCompito` (NVARCHAR) - Task name
- `DescrizioneCompito` (NVARCHAR) - Task description
- `LinkedDocument` (VARBINARY) - Optional attached document
- `CompitoId` (INT) - ID of the task to update (WHERE clause)

**When Triggered**:
- User clicks "Salva Modifiche" button
- For each task in the list that has an existing `id` (tasks already in database)

**Code Reference**: [maintenance_gui.py:1972-1974](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/maintenance_gui.py#L1972-L1974)

---

### 3. DELETE - Remove Maintenance Tasks

**Method**: `DatabaseManager.delete_maintenance_tasks()`

**Location**: [main.py:6538-6554](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/main.py#L6538-L6554)

**SQL Query**:
```sql
DELETE FROM eqp.CompitiManutenzione 
WHERE CompitoId IN (?, ?, ?, ...)
```

**Parameters**:
- `task_ids_to_delete` (LIST of INT) - List of CompitoId values to delete

**When Triggered**:
- User clicks "Salva Modifiche" button
- For tasks that were initially loaded but are no longer in the current task list
- Calculated as: `initial_task_ids - current_task_ids`

**Code Reference**: [maintenance_gui.py:1965-1966](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/maintenance_gui.py#L1965-L1966)

---

## Workflow Summary

### User Actions → Database Operations

1. **User selects Equipment and Intervention Type**
   - Loads existing tasks from database (SELECT query)
   - No modifications yet

2. **User adds new tasks**
   - Tasks stored in memory with `id = None`
   - No database changes until save

3. **User edits existing tasks**
   - Tasks updated in memory, keeping their `id`
   - No database changes until save

4. **User removes tasks**
   - Tasks removed from memory list
   - No database changes until save

5. **User clicks "Salva Modifiche"**
   - System calculates differences:
     - `tasks_to_insert`: Tasks with `id = None`
     - `tasks_to_update`: Tasks with existing `id`
     - `ids_to_delete`: IDs in `initial_task_ids` but not in `current_task_ids`
   
   - **Confirmation dialog** shows summary:
     ```
     Stai per:
     - AGGIORNARE X compiti
     - INSERIRE Y nuovi compiti
     - CANCELLARE Z compiti
     
     Procedere?
     ```
   
   - If user confirms:
     1. **DELETE** operations execute first
     2. **UPDATE** operations for existing tasks
     3. **INSERT** operations for new tasks

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  User Interface (AddMaintenanceTasksWindow)                 │
│  - Select Equipment                                          │
│  - Select Intervention Type                                  │
│  - Add/Edit/Remove Tasks                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Click "Salva"       │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Calculate Changes   │
          │  - To Insert         │
          │  - To Update         │
          │  - To Delete         │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Confirmation Dialog │
          └──────────┬───────────┘
                     │
                     ▼
    ┌────────────────┴────────────────┐
    │                                  │
    ▼                                  ▼
┌───────────┐                  ┌──────────────┐
│  DELETE   │                  │   UPDATE     │
│  Tasks    │ ──────────────▶  │   Tasks      │
└───────────┘                  └──────┬───────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │   INSERT     │
                               │   Tasks      │
                               └──────┬───────┘
                                      │
                                      ▼
                        ┌─────────────────────────┐
                        │  eqp.CompitiManutenzione│
                        │  (Database Table)       │
                        └─────────────────────────┘
```

---

## Table Schema Reference

### `[Traceability_RS].[eqp].[CompitiManutenzione]`

**Key Fields**:
- `CompitoId` (INT, PRIMARY KEY) - Auto-generated task ID
- `ProgrammedInterventionId` (INT, FOREIGN KEY) - Links to intervention type
- `EquipmentId` (INT, FOREIGN KEY) - Links to equipment/machine
- `Categoria` (NVARCHAR) - Category/group title
- `NomeCompito` (NVARCHAR) - Task name
- `DescrizioneCompito` (NVARCHAR) - Task description
- `Ordine` (INT) - Display order
- `LinkedDocument` (VARBINARY) - Optional attached document

---

## Error Handling

All database operations include:
- **Transaction management**: `commit()` on success, `rollback()` on error
- **Error logging**: Errors stored in `self.db.last_error_details`
- **User feedback**: Error messages displayed in messagebox if operations fail

**Code Reference**: [maintenance_gui.py:1963-1984](file:///c:/Users/gtesta/PythonProjetcs/Python/PrductionDocumentation/maintenance_gui.py#L1963-L1984)

---

## Related Tables (Read-Only)

While the form only **modifies** `eqp.CompitiManutenzione`, it **reads** from:

1. **`eqp.Equipments`** - To populate equipment dropdown
2. **`eqp.ProgrammedInterventions`** - To populate intervention type dropdown

These tables are **NOT modified** by this form.

---

## Summary

| Operation | Table | Method | When |
|-----------|-------|--------|------|
| **INSERT** | `eqp.CompitiManutenzione` | `insert_new_maintenance_task()` | New tasks added by user |
| **UPDATE** | `eqp.CompitiManutenzione` | `update_maintenance_task()` | Existing tasks modified by user |
| **DELETE** | `eqp.CompitiManutenzione` | `delete_maintenance_tasks()` | Tasks removed by user |

**All operations occur only when user clicks "Salva Modifiche" and confirms the action.**
