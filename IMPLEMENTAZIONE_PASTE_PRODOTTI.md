# IMPLEMENTAZIONE COLLEGAMENTO PASTE-PRODOTTI
# ============================================

## OBIETTIVO
Modificare la form di configurazione paste per permettere di associare 
una pasta a uno o più prodotti, con possibilità di marcare ogni prodotto 
come "Cannot Reuse" (NotRecicle).

## STRUTTURA DATABASE

### Tabella Products (source)
```sql
SELECT IdProduct, ProductCode, ProductName 
FROM Traceability_RS.dbo.Products 
ORDER BY ProductCode
```

### Tabella PastaProducts (collegamento)
```sql
CREATE TABLE PastaProducts (
    PastaProductId INT IDENTITY PRIMARY KEY,
    IdProduct INT,
    DateIN DATETIME,
    DateOut DATETIME,
    NotRecicle BIT
)
```

### Tabella Pastas (aggiornamento)
```sql
-- Aggiungere campo PastaProductId
ALTER TABLE Pastas ADD PastaProductId INT NULL
```

## MODIFICHE UI IN paste_manager.py

### 1. Aggiungere TreeView Prodotti nella Form

```python
def _build_product_selection_frame(self, parent):
    """Costruisce frame selezione prodotti"""
    product_frame = ttk.LabelFrame(parent, text="Prodotti Associati", padding="10")
    product_frame.pack(fill='both', expand=True, padx=5, pady=5)
    
    # Combo per aggiungere prodotti
    add_frame = ttk.Frame(product_frame)
    add_frame.pack(fill='x', padx=5, pady=5)
    
    ttk.Label(add_frame, text="Aggiungi Prodotto:").pack(side='left', padx=5)
    
    self.product_var = tk.StringVar()
    self.product_combo = ttk.Combobox(add_frame, textvariable=self.product_var,
                                     state='readonly', width=40)
    self.product_combo.pack(side='left', padx=5)
    
    ttk.Button(add_frame, text="Aggiungi", 
              command=self._add_product).pack(side='left', padx=5)
    
    # TreeView prodotti selezionati
    columns = ('id', 'code', 'name', 'no_reuse')
    self.products_tree = ttk.Treeview(product_frame, columns=columns, 
                                     show='headings', height=6)
    
    self.products_tree.heading('id', text='ID')
    self.products_tree.heading('code', text='Codice')
    self.products_tree.heading('name', text='Nome Prodotto')
    self.products_tree.heading('no_reuse', text='Cannot Reuse')
    
    self.products_tree.column('id', width=50)
    self.products_tree.column('code', width=100)
    self.products_tree.column('name', width=200)
    self.products_tree.column('no_reuse', width=100)
    
    scrollbar = ttk.Scrollbar(product_frame, orient='vertical', 
                             command=self.products_tree.yview)
    self.products_tree.configure(yscrollcommand=scrollbar.set)
    
    self.products_tree.pack(side='left', fill='both', expand=True, padx=(5,0), pady=5)
    scrollbar.pack(side='right', fill='y', pady=5)
    
    # Pulsanti azione
    btn_frame = ttk.Frame(product_frame)
    btn_frame.pack(fill='x', padx=5, pady=5)
    
    ttk.Button(btn_frame, text="Toggle Cannot Reuse",
              command=self._toggle_no_reuse).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Rimuovi Prodotto",
              command=self._remove_product).pack(side='left', padx=5)
    
    # Lista prodotti selezionati {IdProduct: {'code': ..., 'name': ..., 'no_reuse': bool}}
    self.selected_products = {}
```

### 2. Caricare Prodotti Disponibili

```python
def _load_products(self):
    """Carica prodotti disponibili"""
    try:
        query = """
            SELECT IdProduct, ProductCode, ProductName 
            FROM [Traceability_RS].[dbo].[Products] 
            ORDER BY ProductCode
        """
        cursor = self.db.conn.cursor()
        cursor.execute(query)
        
        self.products_dict = {}
        for row in cursor.fetchall():
            display = f"{row.ProductCode} - {row.ProductName}"
            self.products_dict[display] = {
                'id': row.IdProduct,
                'code': row.ProductCode,
                'name': row.ProductName
            }
        
        self.product_combo['values'] = list(self.products_dict.keys())
        cursor.close()
        
    except Exception as e:
        logger.error(f"Errore caricamento prodotti: {e}")
```

### 3. Gestione Selezione Prodotti

```python
def _add_product(self):
    """Aggiunge prodotto alla lista"""
    selected = self.product_var.get()
    if not selected:
        return
    
    product_info = self.products_dict[selected]
    product_id = product_info['id']
    
    # Verifica se già presente
    if product_id in self.selected_products:
        messagebox.showwarning('Attenzione', 'Prodotto già aggiunto')
        return
    
    # Aggiungi alla lista
    self.selected_products[product_id] = {
        'code': product_info['code'],
        'name': product_info['name'],
        'no_reuse': False
    }
    
    # Aggiungi alla TreeView
    self.products_tree.insert('', 'end', iid=str(product_id), values=(
        product_id,
        product_info['code'],
        product_info['name'],
        '☐'  # Checkbox non selezionato
    ))
    
    self.product_var.set('')

def _toggle_no_reuse(self):
    """Toggle del flag Cannot Reuse per prodotto selezionato"""
    selection = self.products_tree.selection()
    if not selection:
        messagebox.showwarning('Attenzione', 'Selezionare un prodotto')
        return
    
    product_id = int(selection[0])
    
    # Toggle flag
    current = self.selected_products[product_id]['no_reuse']
    self.selected_products[product_id]['no_reuse'] = not current
    
    # Aggiorna TreeView
    values = self.products_tree.item(selection[0])['values']
    new_values = list(values)
    new_values[3] = '☑' if not current else '☐'
    self.products_tree.item(selection[0], values=new_values)

def _remove_product(self):
    """Rimuove prodotto dalla lista"""
    selection = self.products_tree.selection()
    if not selection:
        return
    
    product_id = int(selection[0])
    del self.selected_products[product_id]
    self.products_tree.delete(selection[0])
```

### 4. Modifica Logica Salvataggio

```python
def _on_save(self):
    """Salva pasta con prodotti associati"""
    
    # ... validazioni esistenti ...
    
    try:
        cursor = self.db.conn.cursor()
        
        # Se ci sono prodotti selezionati
        pasta_product_id = None
        if self.selected_products:
            # Per ogni prodotto selezionato
            for product_id, product_info in self.selected_products.items():
                # INSERT in PastaProducts
                cursor.execute("""
                    INSERT INTO [Traceability_RS].[pst].[PastaProducts]
                    (IdProduct, DateIN, DateOut, NotRecicle)
                    VALUES (?, GETDATE(), NULL, ?)
                """, (product_id, 1 if product_info['no_reuse'] else 0))
                
                # Ottieni PastaProductId appena creato
                cursor.execute("SELECT @@IDENTITY")
                current_pasta_product_id = int(cursor.fetchone()[0])
                
                # Usa il primo come PastaProductId principale
                # (o logica diversa se necessario)
                if pasta_product_id is None:
                    pasta_product_id = current_pasta_product_id
                
                logger.info(f"Creato PastaProductId={current_pasta_product_id} "
                           f"per Product={product_id}, NotRecicle={product_info['no_reuse']}")
        
        if self._editing:
            # UPDATE pasta esistente
            cursor.execute("""
                UPDATE [Traceability_RS].[pst].[Pastas]
                SET ProducerId = ?, PastaCode = ?, PastaProductId = ?
                WHERE Pastaid = ?
            """, (producer_id, pasta_code, pasta_product_id, self._current_pasta_id))
        else:
            # INSERT nuova pasta
            cursor.execute("""
                INSERT INTO [Traceability_RS].[pst].[Pastas]
                (ProducerId, PastaCode, CreatedAt, CreatedBy, PastaProductId)
                VALUES (?, ?, GETDATE(), ?, ?)
            """, (producer_id, pasta_code, self.user_name, pasta_product_id))
        
        self.db.conn.commit()
        cursor.close()
        
        messagebox.showinfo('Successo', 'Pasta salvata con successo')
        
    except Exception as e:
        self.db.conn.rollback()
        logger.error(f"Errore salvataggio: {e}")
        messagebox.showerror('Errore', f"Errore: {str(e)}")
```

### 5. Caricamento Prodotti in Modifica

```python
def _on_select(self, event):
    """Carica pasta selezionata per modifica"""
    
    # ... codice esistente ...
    
    # Carica prodotti associati
    self._load_associated_products(pasta_id)

def _load_associated_products(self, pasta_id):
    """Carica prodotti già associati alla pasta"""
    try:
        # Prima ottieni PastaProductId dalla pasta
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT PastaProductId 
            FROM [Traceability_RS].[pst].[Pastas]
            WHERE Pastaid = ?
        """, (pasta_id,))
        
        result = cursor.fetchone()
        if not result or not result.PastaProductId:
            cursor.close()
            return
        
        # Carica tutti i prodotti associati
        cursor.execute("""
            SELECT pp.PastaProductId, pp.IdProduct, pp.NotRecicle,
                   p.ProductCode, p.ProductName
            FROM [Traceability_RS].[pst].[PastaProducts] pp
            INNER JOIN [Traceability_RS].[dbo].[Products] p 
                ON pp.IdProduct = p.IdProduct
            WHERE pp.DateOut IS NULL
              AND pp.PastaProductId = ?
        """, (result.PastaProductId,))
        
        # Popola TreeView e selected_products
        self.selected_products = {}
        for row in cursor.fetchall():
            product_id = row.IdProduct
            self.selected_products[product_id] = {
                'code': row.ProductCode,
                'name': row.ProductName,
                'no_reuse': bool(row.NotRecicle)
            }
            
            self.products_tree.insert('', 'end', iid=str(product_id), values=(
                product_id,
                row.ProductCode,
                row.ProductName,
                '☑' if row.NotRecicle else '☐'
            ))
        
        cursor.close()
        
    except Exception as e:
        logger.error(f"Errore caricamento prodotti associati: {e}")
```

## TRADUZIONI SQL NECESSARIE

```sql
-- Italiano
INSERT INTO AppTranslations VALUES 
('IT', 'associated_products', 'Prodotti Associati', NULL),
('IT', 'add_product', 'Aggiungi Prodotto', NULL),
('IT', 'cannot_reuse', 'Cannot Reuse', NULL),
('IT', 'toggle_cannot_reuse', 'Toggle Cannot Reuse', NULL),
('IT', 'remove_product', 'Rimuovi Prodotto', NULL),
('IT', 'product_already_added', 'Prodotto già aggiunto', NULL);

-- Altre lingue (RO, EN, DE, SV)...
```

## NOTE IMPLEMENTAZIONE

1. **Gestione Multiple PastaProductId**: 
   - Se una pasta ha più prodotti, vengono creati più record in PastaProducts
   - Solo il primo PastaProductId viene salvato in Pastas.PastaProductId
   - Alternativamente, si potrebbe salvare una lista o usare una junction table

2. **DateOut**: 
   - Impostato a NULL alla creazione
   - Verrà valorizzato quando il prodotto viene "chiuso" o rimosso

3. **NotRecicle**: 
   - BIT (0/1)
   - Determina se il prodotto può essere riutilizzato

4. **UI/UX**:
   - TreeView per visualizzare prodotti selezionati
   - Checkbox visivo con simboli ☐/☑
   - Possibilità di aggiungere/rimuovere prodotti
   - Toggle rapido del flag Cannot Reuse

## FILE DA MODIFICARE

1. `paste_manager.py` - Form configurazione paste
2. `main.py` - Se serve aggiungere query helper
3. SQL - Script traduzioni

## TESTING

1. Creare una pasta senza prodotti
2. Creare una pasta con 1 prodotto
3. Creare una pasta con multipli prodotti
4. Modificare prodotti di pasta esistente
5. Toggle Cannot Reuse
6. Verificare salvataggio in DB
