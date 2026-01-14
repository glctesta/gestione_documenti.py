# ============================================================================
# CODICE DA AGGIUNGERE A paste_manager.py
# Per collegamento Paste-Prodotti
# ============================================================================

# ----- PARTE 1: Aggiungere in __init__ dopo le altre variabili -----
# Linea ~35-38, dopo self._doc_data = None

self.selected_products = {}  # {IdProduct: {'code': ..., 'name': ..., 'no_reuse': bool}}
self.products_dict = {}      # {display_name: {'id': ..., 'code': ..., 'name': ...}}


# ----- PARTE 2: Aggiungere frame prodotti in _build_ui -----
# Inserire dopo la sezione "Documento allegato" (dopo row=5)
# PRIMA dei pulsanti azione (row=6)

# --- SEZIONE PRODOTTI ASSOCIATI ---
# (Nuovo row=6, spostare pulsanti a row=7)

product_main_frame = ttk.LabelFrame(left_frame, text="Prodotti Associati (opzionale)")
product_main_frame.grid(row=6, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

# Combo aggiunta prodotto
add_frame = ttk.Frame(product_main_frame)
add_frame.pack(fill='x', padx=5, pady=5)

ttk.Label(add_frame, text="Aggiungi:").pack(side='left', padx=5)

self.product_var = tk.StringVar()
self.product_combo = ttk.Combobox(add_frame, textvariable=self.product_var,
                                 state='readonly', width=30)
self.product_combo.pack(side='left', padx=5)

ttk.Button(add_frame, text="➕", command=self._add_product, width=3).pack(side='left', padx=2)
ttk.Button(add_frame, text="Toggle ☐/☑", command=self._toggle_no_reuse).pack(side='left', padx=2)
ttk.Button(add_frame, text="❌", command=self._remove_product, width=3).pack(side='left', padx=2)

# TreeView prodotti
tree_frame = ttk.Frame(product_main_frame)
tree_frame.pack(fill='both', expand=True, padx=5, pady=5)

prod_columns = ('id', 'code', 'name', 'no_reuse')
self.products_tree = ttk.Treeview(tree_frame, columns=prod_columns, 
                                 show='headings', height=4)

self.products_tree.heading('id', text='ID')
self.products_tree.heading('code', text='Codice')
self.products_tree.heading('name', text='Nome Prodotto')
self.products_tree.heading('no_reuse', text='Cannot Reuse')

self.products_tree.column('id', width=40)
self.products_tree.column('code', width=80)
self.products_tree.column('name', width=150)
self.products_tree.column('no_reuse', width=80)

prod_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', 
                              command=self.products_tree.yview)
self.products_tree.configure(yscrollcommand=prod_scrollbar.set)

self.products_tree.pack(side='left', fill='both', expand=True)
prod_scrollbar.pack(side='right', fill='y')

# Pulsanti azione (ora row=7 invece di row=6)
btn_frame = ttk.Frame(left_frame)
btn_frame.grid(row=7, column=0, columnspan=2, pady=20)  # ← CAMBIATO DA row=6


# ----- PARTE 3: Nuovo metodo per caricare prodotti -----
# Aggiungere DOPO _load_producers

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
        
        logger.info(f"[PASTE] Caricati {len(self.products_dict)} prodotti")
        
    except Exception as e:
        logger.error(f"Errore caricamento prodotti: {e}")
        messagebox.showerror('Errore', f"Errore caricamento prodotti: {str(e)}")


# ----- PARTE 4: Metodi gestione prodotti -----
# Aggiungere DOPO _load_products

def _add_product(self):
    """Aggiunge prodotto alla selezione"""
    selected = self.product_var.get()
    if not selected:
        messagebox.showwarning('Attenzione', 'Selezionare un prodotto')
        return
    
    product_info = self.products_dict[selected]
    product_id = product_info['id']
    
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
        '☐'
    ))
    
    self.product_var.set('')
    logger.info(f"[PASTE] Aggiunto prodotto ID={product_id}")

def _toggle_no_reuse(self):
    """Toggle flag Cannot Reuse"""
    selection = self.products_tree.selection()
    if not selection:
        messagebox.showwarning('Attenzione', 'Selezionare un prodotto dalla lista')
        return
    
    product_id = int(selection[0])
    
    # Toggle
    current = self.selected_products[product_id]['no_reuse']
    self.selected_products[product_id]['no_reuse'] = not current
    
    # Aggiorna TreeView
    values = list(self.products_tree.item(selection[0])['values'])
    values[3] = '☑' if not current else '☐'
    self.products_tree.item(selection[0], values=values)
    
    logger.info(f"[PASTE] Toggle NotRecicle per Product={product_id}: {not current}")

def _remove_product(self):
    """Rimuove prodotto dalla selezione"""
    selection = self.products_tree.selection()
    if not selection:
        messagebox.showwarning('Attenzione', 'Selezionare un prodotto da rimuovere')
        return
    
    product_id = int(selection[0])
    del self.selected_products[product_id]
    self.products_tree.delete(selection[0])
    
    logger.info(f"[PASTE] Rimosso prodotto ID={product_id}")


# ----- PARTE 5: Modificare __init__ per chiamare _load_products -----
# Trovare la linea dove c'è self._load_producers() (linea ~36-38)
# Aggiungere subito dopo:

self._load_products()


# ----- PARTE 6: Modificare _on_save per salvare prodotti -----
# SOSTITUIRE il metodo _on_save esistente (linee 303-421) con questa versione:

def _on_save(self):
    """Salva o aggiorna una pasta"""
    
    # Validazioni esistenti
    pasta_code = self.pasta_code_var.get().strip()
    producer_name = self.producer_var.get().strip()
    
    if not pasta_code:
        messagebox.showwarning(
            self.lang.get('warning', 'Attenzione'),
            self.lang.get('enter_pasta_code', 'Inserire il codice pasta')
        )
        return
    
    if not producer_name:
        messagebox.showwarning(
            self.lang.get('warning', 'Attenzione'),
            self.lang.get('select_producer', 'Selezionare un produttore')
        )
        return
    
    # Verifica produttore
    if producer_name not in self.producers_dict:
        response = messagebox.askyesno(
            self.lang.get('warning', 'Attenzione'),
            f"Il produttore '{producer_name}' non esiste.\n\nVuoi aprire la gestione produttori?"
        )
        if response:
            self._open_producers_management()
        return
    
    producer_id = self.producers_dict[producer_name]
    
    # Validità
    try:
        valability = int(self.valability_var.get())
    except:
        messagebox.showwarning('Attenzione', 'Inserire validità in mesi (numero)')
        return
    
    # Temperature
    try:
        low_temp = float(self.low_temp_var.get())
        high_temp = float(self.high_temp_var.get())
    except:
        messagebox.showwarning('Attenzione', 'Inserire temperature valide')
        return
    
    try:
        cursor = self.db.conn.cursor()
        
        # GESTIONE PRODOTTI ASSOCIATI
        # Per ogni prodotto selezionato, crea record in PastaProducts
        pasta_product_ids = []
        
        if self.selected_products:
            for product_id, product_info in self.selected_products.items():
                not_recicle = 1 if product_info['no_reuse'] else 0
                
                # INSERT in PastaProducts
                cursor.execute("""
                    INSERT INTO [Traceability_RS].[pst].[PastaProducts]
                    (IdProduct, DateIN, DateOut, NotRecicle)
                    VALUES (?, GETDATE(), NULL, ?)
                """, (product_id, not_recicle))
                
                # Ottieni ID creato
                cursor.execute("SELECT @@IDENTITY")
                pasta_product_id = int(cursor.fetchone()[0])
                pasta_product_ids.append(pasta_product_id)
                
                logger.info(f"[PASTE] Creato PastaProductId={pasta_product_id}, "
                           f"Product={product_id}, NotRecicle={not_recicle}")
        
        # Usa il primo PastaProductId (o NULL se nessun prodotto)
        main_pasta_product_id = pasta_product_ids[0] if pasta_product_ids else None
        
        if self._editing:
            # UPDATE
            cursor.execute("""
                UPDATE [Traceability_RS].[pst].[Pastas]
                SET ProducerId = ?, PastaCode = ?, PastaDataSheet = ?
                WHERE Pastaid = ?
            """, (producer_id, pasta_code, self._doc_data, self._current_pasta_id))
            
            # UPDATE configurazione
            cursor.execute("""
                UPDATE [Traceability_RS].[pst].[PastaConfigs]
                SET Valability = ?, LowTemperature = ?, HighTemperature = ?
                WHERE PastaId = ?
            """, (valability, low_temp, high_temp, self._current_pasta_id))
            
            message = f"Pasta {pasta_code} aggiornata con successo"
            pasta_id = self._current_pasta_id
            
        else:
            # INSERT nuova pasta
            cursor.execute("""
                INSERT INTO [Traceability_RS].[pst].[Pastas]
                (ProducerId, PastaCode, CreatedAt, CreatedBy, PastaDataSheet)
                VALUES (?, ?, GETDATE(), ?, ?)
            """, (producer_id, pasta_code, self.user_id, self._doc_data))
            
            cursor.execute("SELECT @@IDENTITY")
            pasta_id = int(cursor.fetchone()[0])
            
            # INSERT configurazione
            cursor.execute("""
                INSERT INTO [Traceability_RS].[pst].[PastaConfigs]
                (PastaId, Valability, LowTemperature, HighTemperature)
                VALUES (?, ?, ?, ?)
            """, (pasta_id, valability, low_temp, high_temp))
            
            message = f"Pasta {pasta_code} creata con successo"
        
        self.db.conn.commit()
        cursor.close()
        
        logger.info(f"[PASTE] Salvata Pasta ID={pasta_id}, Code={pasta_code}, "
                   f"Prodotti={len(self.selected_products)}")
        
        messagebox.showinfo('Successo', message)
        
        self._load_pastas()
        self._on_new()
        
    except Exception as e:
        self.db.conn.rollback()
        logger.error(f"Errore salvataggio pasta: {e}")
        messagebox.showerror('Errore', f"Errore durante il salvataggio: {str(e)}")


# ----- PARTE 7: Modificare _on_new per pulire prodotti -----
# Aggiungere in _on_new (linea ~291-301) PRIMA dell'ultimo return:

self.selected_products = {}
self.product_var.set('')
# Pulisci TreeView prodotti
for item in self.products_tree.get_children():
    self.products_tree.delete(item)


# ----- PARTE 8: Caricare prodotti in modifica -----
# Aggiungere NUOVO metodo dopo _on_select:

def _load_associated_products(self, pasta_id):
    """Carica prodotti associati alla pasta"""
    try:
        cursor = self.db.conn.cursor()
        
        # Carica tutti i prodotti con DateOut NULL
        cursor.execute("""
            SELECT pp.PastaProductId, pp.IdProduct, pp.NotRecicle,
                   p.ProductCode, p.ProductName
            FROM [Traceability_RS].[pst].[PastaProducts] pp
            INNER JOIN [Traceability_RS].[dbo].[Products] p 
                ON pp.IdProduct = p.IdProduct
            INNER JOIN [Traceability_RS].[pst].[Pastas] pa
                ON pa.Pastaid = ?
            WHERE pp.DateOut IS NULL
        """, (pasta_id,))
        
        # Pulisci selezione corrente
        self.selected_products = {}
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Aggiungi prodotti trovati
        for row in cursor.fetchall():
            product_id = row.IdProduct
            not_recicle = row.NotRecicle if row.NotRecicle is not None else 0
            
            self.selected_products[product_id] = {
                'code': row.ProductCode,
                'name': row.ProductName,
                'no_reuse': bool(not_recicle)
            }
            
            self.products_tree.insert('', 'end', iid=str(product_id), values=(
                product_id,
                row.ProductCode,
                row.ProductName,
                '☑' if not_recicle else '☐'
            ))
        
        cursor.close()
        logger.info(f"[PASTE] Caricati {len(self.selected_products)} prodotti per Pasta={pasta_id}")
        
    except Exception as e:
        logger.error(f"Errore caricamento prodotti associati: {e}")


# ----- PARTE 9: Chiamare _load_associated_products in _on_select -----
# In _on_select (linea ~237-276), ALLA FINE prima del return, aggiungere:

# Carica prodotti associati
self._load_associated_products(pasta_id)


# ============================================================================
# FINE MODIFICHE
# ============================================================================

# NOTE:
# 1. Assicurati che la tabella PastaProducts esista con i campi corretti
# 2. NON serve più il campo PastaProductId in Pastas (ignoralo)
# 3. La relazione è: Pasta N → N Products tramite PastaProducts
# 4. DateOut rimane sempre NULL per ora (gestione futura)
