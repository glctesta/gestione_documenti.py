import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TraceabilityManager:
    def __init__(self, parent, db, lang):
        self.parent = parent
        self.db = db
        self.lang = lang

    def _format_product_name_with_version(self, product_name, version):
        """Formatta il nome del prodotto con la versione se presente."""
        if version and version.strip():
            return f"{product_name} [{version}]"
        return product_name

    def _row_get_value(self, row, *field_names, default=None, index=None):
        """Recupera un valore da pyodbc.Row in modo robusto (case-insensitive + fallback indice)."""
        for field in field_names:
            if hasattr(row, field):
                value = getattr(row, field)
                if value is not None:
                    return value
            lower_field = field.lower()
            if hasattr(row, lower_field):
                value = getattr(row, lower_field)
                if value is not None:
                    return value
            upper_field = field.upper()
            if hasattr(row, upper_field):
                value = getattr(row, upper_field)
                if value is not None:
                    return value

        if index is not None:
            try:
                value = row[index]
                return default if value is None else value
            except Exception:
                pass

        return default

    def _product_row_to_tree_values(self, product):
        """Converte una riga prodotto in tuple pronta per la Treeview."""
        product_id = self._row_get_value(product, 'idproduct', 'IDProduct', index=0)
        product_code = self._row_get_value(product, 'ProductCode', 'productcode', default='', index=1)
        product_name = self._row_get_value(product, 'ProductName', 'productname', default='', index=2)
        is_final_flag = self._row_get_value(product, 'IsFinalProduct', 'isfinalproduct', default=False)
        product_customer_code = self._row_get_value(product, 'ProductCodClienteFinal', 'productcodclientefinal', default='')
        final_client_name = self._row_get_value(product, 'FinalClientName', 'finalclientname', default='')
        acronim = self._row_get_value(product, 'AcronimForCode', 'acronimforcode', default='')
        version = self._row_get_value(product, 'Version', 'version', default='')

        is_final = "Sì" if bool(is_final_flag) else "No"
        customer_code = product_customer_code if product_customer_code and product_customer_code != '#ND' else ""
        return (
            product_id,
            product_code,
            product_name,
            is_final,
            customer_code,
            final_client_name or "",
            acronim or "",
            version or ""
        )

    def open_manage_customers(self, user_name=None):
        """Apre la finestra per gestire i clienti finali"""
        window = tk.Toplevel(self.parent)
        window.title(self.lang.get('manage_customers_title', "Gestione Clienti Finali"))
        window.geometry("800x600")

        # Frame principale
        main_frame = ttk.Frame(window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Etichetta utente
        if user_name:
            status_frame = ttk.Frame(main_frame)
            status_frame.pack(fill=tk.X, pady=(0, 10))
            ttk.Label(status_frame, text=f"Utente: {user_name}").pack(side=tk.LEFT)

        # Titolo
        title_label = ttk.Label(main_frame,
                                text=self.lang.get('manage_customers_label', "Gestione Clienti Finali"),
                                font=("Helvetica", 14, "bold"))
        title_label.pack(pady=(0, 20))

        # Frame per i pulsanti
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # Pulsanti
        ttk.Button(button_frame, text=self.lang.get('button_add', "Aggiungi"),
                   command=lambda: self._open_customer_form(window)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text=self.lang.get('button_edit', "Modifica"),
                   command=self._edit_customer).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text=self.lang.get('button_delete', "Elimina"),
                   command=self._delete_customer).pack(side=tk.LEFT)

        # Tabella clienti
        columns = ('id', 'name', 'full_name', 'acronim', 'city', 'country', 'vat')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)

        # Intestazioni colonne
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text=self.lang.get('customer_name', "Nome"))
        self.tree.heading('full_name', text=self.lang.get('customer_full_name', "Nome Completo"))
        self.tree.heading('acronim', text=self.lang.get('customer_acronim', "Acronimo"))
        self.tree.heading('city', text=self.lang.get('customer_city', "Città"))
        self.tree.heading('country', text=self.lang.get('customer_country', "Paese"))
        self.tree.heading('vat', text=self.lang.get('customer_vat', "P.IVA"))

        # Dimensioni colonne
        self.tree.column('id', width=50)
        self.tree.column('name', width=120)
        self.tree.column('full_name', width=180)
        self.tree.column('acronim', width=80)
        self.tree.column('city', width=100)
        self.tree.column('country', width=100)
        self.tree.column('vat', width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Carica i dati
        self._load_customers()

        # Bind doppio click per modifica
        self.tree.bind('<Double-1>', lambda e: self._edit_customer())

    def _load_customers(self):
        """Carica i clienti nella tabella"""
        # Pulisci la tabella
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Recupera i clienti dal database
        customers = self.db.fetch_final_customers()

        # Popola la tabella
        for customer in customers:
            self.tree.insert('', tk.END, values=(
                customer.IDFinalClient,
                customer.FinalClientName,
                customer.FinalClientFullName,
                customer.AcronimForCode,
                customer.ClientCity,
                customer.ClientCountry,
                customer.VatCode
            ))

    def _open_customer_form(self, parent, customer_data=None):
        """Apre il form per aggiungere/modificare un cliente"""
        form_window = tk.Toplevel(parent)
        form_window.title(self.lang.get('customer_form_title', "Dettaglio Cliente"))
        form_window.geometry("500x500")
        form_window.grab_set()

        # Frame principale
        form_frame = ttk.Frame(form_window, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Variabili per i campi
        name_var = tk.StringVar(value=customer_data[1] if customer_data else "")
        full_name_var = tk.StringVar(value=customer_data[2] if customer_data else "")
        acronim_var = tk.StringVar(value=customer_data[3] if customer_data else "")
        address_var = tk.StringVar(value=customer_data[4] if customer_data else "")
        city_var = tk.StringVar(value=customer_data[5] if customer_data else "")
        zip_var = tk.StringVar(value=customer_data[6] if customer_data else "")
        country_var = tk.StringVar(value=customer_data[7] if customer_data else "")
        vat_var = tk.StringVar(value=customer_data[8] if customer_data else "")

        # Campi del form
        ttk.Label(form_frame, text=self.lang.get('customer_name', "Nome *")).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=name_var, width=40).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        ttk.Label(form_frame, text=self.lang.get('customer_full_name', "Nome Completo")).grid(row=1, column=0,
                                                                                              sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=full_name_var, width=40).grid(row=1, column=1, sticky=tk.W, pady=5,
                                                                         padx=(10, 0))

        ttk.Label(form_frame, text=self.lang.get('customer_acronim', "Acronimo")).grid(row=2, column=0, sticky=tk.W,
                                                                                       pady=5)
        ttk.Entry(form_frame, textvariable=acronim_var, width=40).grid(row=2, column=1, sticky=tk.W, pady=5,
                                                                       padx=(10, 0))

        ttk.Label(form_frame, text=self.lang.get('customer_address', "Indirizzo")).grid(row=3, column=0, sticky=tk.W,
                                                                                        pady=5)
        ttk.Entry(form_frame, textvariable=address_var, width=40).grid(row=3, column=1, sticky=tk.W, pady=5,
                                                                       padx=(10, 0))

        ttk.Label(form_frame, text=self.lang.get('customer_city', "Città")).grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=city_var, width=40).grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        ttk.Label(form_frame, text=self.lang.get('customer_zip', "CAP")).grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=zip_var, width=40).grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        ttk.Label(form_frame, text=self.lang.get('customer_country', "Paese")).grid(row=6, column=0, sticky=tk.W,
                                                                                    pady=5)
        ttk.Entry(form_frame, textvariable=country_var, width=40).grid(row=6, column=1, sticky=tk.W, pady=5,
                                                                       padx=(10, 0))

        ttk.Label(form_frame, text=self.lang.get('customer_vat', "P.IVA")).grid(row=7, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=vat_var, width=40).grid(row=7, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Pulsanti
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)

        def save_customer():
            # Validazione
            if not name_var.get().strip():
                messagebox.showerror("Errore", "Il campo Nome è obbligatorio", parent=form_window)
                return

            if customer_data:  # Modifica
                success, message = self.db.update_final_customer(
                    customer_data[0], name_var.get(), full_name_var.get(), acronim_var.get(),
                    address_var.get(), city_var.get(), zip_var.get(), country_var.get(), vat_var.get()
                )
            else:  # Nuovo cliente
                success, message = self.db.add_final_customer(
                    name_var.get(), full_name_var.get(), acronim_var.get(),
                    address_var.get(), city_var.get(), zip_var.get(), country_var.get(), vat_var.get()
                )

            if success:
                messagebox.showinfo("Successo", message, parent=form_window)
                self._load_customers()
                form_window.destroy()
            else:
                messagebox.showerror("Errore", message, parent=form_window)

        ttk.Button(button_frame, text=self.lang.get('button_save', "Salva"),
                   command=save_customer).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text=self.lang.get('button_cancel', "Annulla"),
                   command=form_window.destroy).pack(side=tk.LEFT)

    def _edit_customer(self):
        """Modifica il cliente selezionato"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un cliente da modificare",
                                   parent=self.tree.winfo_toplevel())
            return

        item = self.tree.item(selection[0])
        customer_data = item['values']

        # Recupera tutti i dati del cliente (la tabella mostra solo alcuni campi)
        customers = self.db.fetch_final_customers()
        full_customer_data = next((c for c in customers if c.IDFinalClient == customer_data[0]), None)

        if full_customer_data:
            self._open_customer_form(self.tree.winfo_toplevel(), [
                full_customer_data.IDFinalClient,
                full_customer_data.FinalClientName,
                full_customer_data.FinalClientFullName,
                full_customer_data.AcronimForCode,
                full_customer_data.ClientAddress,
                full_customer_data.ClientCity,
                full_customer_data.ClientZIP,
                full_customer_data.ClientCountry,
                full_customer_data.VatCode
            ])

    def _delete_customer(self):
        """Elimina il cliente selezionato"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un cliente da eliminare", parent=self.tree.winfo_toplevel())
            return

        item = self.tree.item(selection[0])
        customer_name = item['values'][1]

        if messagebox.askyesno("Conferma",
                               f"Sei sicuro di voler eliminare il cliente '{customer_name}'?",
                               parent=self.tree.winfo_toplevel()):
            success, message = self.db.delete_final_customer(item['values'][0])
            if success:
                messagebox.showinfo("Successo", message, parent=self.tree.winfo_toplevel())
                self._load_customers()
            else:
                messagebox.showerror("Errore", message, parent=self.tree.winfo_toplevel())

    def open_define_products(self, user_name=None):
        """Apre la finestra per definire i prodotti finali"""
        window = tk.Toplevel(self.parent)
        window.title(self.lang.get('define_products_title', "Definizione Prodotti Finali"))
        window.geometry("1000x700")

        # Frame principale
        main_frame = ttk.Frame(window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Etichetta utente
        if user_name:
            status_frame = ttk.Frame(main_frame)
            status_frame.pack(fill=tk.X, pady=(0, 10))
            ttk.Label(status_frame, text=f"Utente: {user_name}").pack(side=tk.LEFT)

        # Titolo
        title_label = ttk.Label(main_frame,
                                text=self.lang.get('define_products_label', "Definizione Prodotti Finali"),
                                font=("Helvetica", 14, "bold"))
        title_label.pack(pady=(0, 20))

        # Frame per i filtri
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filter_frame, text="Filtra per codice:").pack(side=tk.LEFT, padx=(0, 5))
        filter_var = tk.StringVar()
        filter_entry = ttk.Entry(filter_frame, textvariable=filter_var, width=30)
        filter_entry.pack(side=tk.LEFT, padx=(0, 10))
        filter_entry.bind('<KeyRelease>', lambda e: self._filter_products(filter_var.get()))

        # Tabella prodotti
        columns = ('id', 'code', 'name', 'is_final', 'customer_code', 'client_name', 'acronim', 'version')
        self.products_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)

        # Intestazioni colonne
        self.products_tree.heading('id', text='ID')
        self.products_tree.heading('code', text='Codice Prodotto')
        self.products_tree.heading('name', text='Nome Prodotto')
        self.products_tree.heading('is_final', text='Prodotto Finale')
        self.products_tree.heading('customer_code', text='Codice Cliente')
        self.products_tree.heading('client_name', text='Cliente Finale')
        self.products_tree.heading('acronim', text='Acronimo')
        self.products_tree.heading('version', text='Versione')

        # Dimensioni colonne
        self.products_tree.column('id', width=50)
        self.products_tree.column('code', width=120)
        self.products_tree.column('name', width=180)
        self.products_tree.column('is_final', width=100)
        self.products_tree.column('customer_code', width=120)
        self.products_tree.column('client_name', width=150)
        self.products_tree.column('acronim', width=80)
        self.products_tree.column('version', width=80)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)

        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Pulsante modifica
        ttk.Button(main_frame, text=self.lang.get('button_edit', "Modifica"),
                   command=self._edit_product_final_info).pack(pady=10)

        # Bind doppio click per modifica
        self.products_tree.bind('<Double-1>', lambda e: self._edit_product_final_info())

        # Carica i dati
        self.all_products = self.db.fetch_final_products()
        self._load_products()

    def _load_products(self):
        """Carica i prodotti nella tabella"""
        # Pulisci la tabella
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        # Popola la tabella
        for product in self.all_products:
            self.products_tree.insert('', tk.END, values=self._product_row_to_tree_values(product))

    def _filter_products(self, filter_text):
        """Filtra i prodotti in base al testo inserito"""
        if not filter_text:
            self._load_products()
            return

        filter_text = filter_text.lower()
        filtered_products = []
        for p in self.all_products:
            product_code = str(self._row_get_value(p, 'ProductCode', 'productcode', default=''))
            product_name = str(self._row_get_value(p, 'ProductName', 'productname', default=''))
            if filter_text in product_code.lower() or filter_text in product_name.lower():
                filtered_products.append(p)

        # Pulisci la tabella
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        # Popola con i prodotti filtrati
        for product in filtered_products:
            self.products_tree.insert('', tk.END, values=self._product_row_to_tree_values(product))

    def _edit_product_final_info(self):
        """Modifica le informazioni di prodotto finale"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un prodotto da modificare",
                                   parent=self.products_tree.winfo_toplevel())
            return

        item = self.products_tree.item(selection[0])
        product_values = item['values']

        # Trova il prodotto completo nella lista
        product = next(
            (p for p in self.all_products if self._row_get_value(p, 'idproduct', 'IDProduct', index=0) == product_values[0]),
            None
        )

        if product:
            self._open_product_final_form(self.products_tree.winfo_toplevel(), product)

    def _open_product_final_form(self, parent, product):
        """Apre il form per modificare le informazioni di prodotto finale"""
        form_window = tk.Toplevel(parent)
        form_window.title("Modifica Prodotto Finale")
        form_window.geometry("500x450")
        form_window.grab_set()

        # Frame principale
        form_frame = ttk.Frame(form_window, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Informazioni prodotto
        product_id = self._row_get_value(product, 'idproduct', 'IDProduct', index=0)
        product_code = self._row_get_value(product, 'ProductCode', 'productcode', default='')
        product_name = self._row_get_value(product, 'ProductName', 'productname', default='')
        is_final_flag = self._row_get_value(product, 'IsFinalProduct', 'isfinalproduct', default=False)
        final_client_name = self._row_get_value(product, 'FinalClientName', 'finalclientname', default='')
        product_acronim = self._row_get_value(product, 'AcronimForCode', 'acronimforcode', default='')
        product_customer_code = self._row_get_value(product, 'ProductCodClienteFinal', 'productcodclientefinal', default='')
        product_version = self._row_get_value(product, 'Version', 'version', default='')

        ttk.Label(form_frame, text=f"Codice: {product_code}", font=("Helvetica", 10, "bold")).grid(row=0,
                                                                                                          column=0,
                                                                                                          columnspan=2,
                                                                                                          sticky=tk.W,
                                                                                                          pady=(0, 10))
        ttk.Label(form_frame, text=f"Nome: {product_name}").grid(row=1, column=0, columnspan=2, sticky=tk.W,
                                                                        pady=(0, 20))

        # Checkbox prodotto finale
        is_final_var = tk.BooleanVar(value=bool(is_final_flag))
        ttk.Checkbutton(form_frame, text="Prodotto Finale", variable=is_final_var).grid(row=2, column=0, columnspan=2,
                                                                                        sticky=tk.W, pady=5)

        # Cliente finale
        ttk.Label(form_frame, text="Cliente Finale:").grid(row=3, column=0, sticky=tk.W, pady=5)

        # Recupera i clienti finali
        clients = self.db.fetch_final_clients_for_products()
        client_names = [f"{c.FinalClientName} ({c.AcronimForCode})" for c in clients]
        client_dict = {f"{c.FinalClientName} ({c.AcronimForCode})": c.IDFinalClient for c in clients}

        client_var = tk.StringVar()
        client_combo = ttk.Combobox(form_frame, textvariable=client_var, values=client_names, state="readonly")
        client_combo.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Seleziona il cliente corrente se presente
        if final_client_name and product_acronim:
            current_client = f"{final_client_name} ({product_acronim})"
            if current_client in client_names:
                client_var.set(current_client)

        # Codice cliente
        ttk.Label(form_frame, text="Codice Cliente:").grid(row=4, column=0, sticky=tk.W, pady=5)
        customer_code_var = tk.StringVar(
            value=product_customer_code if product_customer_code != '#ND' else "")
        ttk.Entry(form_frame, textvariable=customer_code_var, width=30).grid(row=4, column=1, sticky=tk.W, pady=5,
                                                                             padx=(10, 0))

        # Versione
        ttk.Label(form_frame, text="Versione:").grid(row=5, column=0, sticky=tk.W, pady=5)
        version_var = tk.StringVar(value=product_version if product_version else "")
        ttk.Entry(form_frame, textvariable=version_var, width=30).grid(row=5, column=1, sticky=tk.W, pady=5,
                                                                       padx=(10, 0))

        # Pulsanti
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        def save_product_info():
            selected_client_name = client_var.get()
            final_client_id = client_dict.get(selected_client_name) if selected_client_name else None
            customer_code = customer_code_var.get().strip() or None
            version = version_var.get().strip() or None

            success, message = self.db.update_product_final_info(
                product_id, is_final_var.get(), final_client_id, customer_code, version
            )

            if success:
                messagebox.showinfo("Successo", message, parent=form_window)
                # Ricarica i dati
                self.all_products = self.db.fetch_final_products()
                self._load_products()
                form_window.destroy()
            else:
                messagebox.showerror("Errore", message, parent=form_window)

        ttk.Button(button_frame, text=self.lang.get('button_save', "Salva"),
                   command=save_product_info).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text=self.lang.get('button_cancel', "Annulla"),
                   command=form_window.destroy).pack(side=tk.LEFT)

    def open_manage_links(self, user_name=None):
        """Apre la finestra per gestire i collegamenti tra prodotti"""
        window = tk.Toplevel(self.parent)
        window.title(self.lang.get('manage_links_title', "Gestione Collegamenti"))
        window.geometry("1200x800")

        # Frame principale
        main_frame = ttk.Frame(window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Etichetta utente
        if user_name:
            status_frame = ttk.Frame(main_frame)
            status_frame.pack(fill=tk.X, pady=(0, 10))
            ttk.Label(status_frame, text=f"{self.lang.get('user', 'Utente')}: {user_name}").pack(side=tk.LEFT)

        # Titolo
        title_label = ttk.Label(main_frame,
                                text=self.lang.get('manage_links_label', "Gestione Collegamenti Prodotti"),
                                font=("Helvetica", 14, "bold"))
        title_label.pack(pady=(0, 20))

        # Frame per i filtri
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 20))

        # Filtro per cliente
        ttk.Label(filter_frame, text=self.lang.get('select_client', "Seleziona Cliente:")).pack(side=tk.LEFT, padx=(0, 5))

        self.client_var = tk.StringVar()
        self.client_combo = ttk.Combobox(filter_frame, textvariable=self.client_var, width=30, state="readonly")
        self.client_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.client_combo.bind('<<ComboboxSelected>>', self._on_client_selected)

        # Pulsante per caricare tutti i collegamenti
        ttk.Button(filter_frame, text=self.lang.get('show_all', "Mostra Tutti"),
                   command=self._load_all_links).pack(side=tk.LEFT)

        # Frame per l'aggiunta di nuovi collegamenti
        add_frame = ttk.LabelFrame(main_frame, text=self.lang.get('add_new_link', "Aggiungi Nuovo Collegamento"),
                                   padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 20))

        # Prodotti finali
        ttk.Label(add_frame, text=self.lang.get('final_product', "Prodotto Finale:")).grid(row=0, column=0, sticky=tk.W,
                                                                                           pady=5)
        self.final_product_var = tk.StringVar()
        self.final_product_combo = ttk.Combobox(add_frame, textvariable=self.final_product_var,
                                                width=30, state="readonly")
        self.final_product_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Semilavorati
        ttk.Label(add_frame, text=self.lang.get('semi_product', "Semilavorato:")).grid(row=0, column=2, sticky=tk.W,
                                                                                       pady=5, padx=(20, 0))
        self.semi_product_var = tk.StringVar()
        self.semi_product_combo = ttk.Combobox(add_frame, textvariable=self.semi_product_var,
                                               width=30, state="readonly")
        self.semi_product_combo.grid(row=0, column=3, sticky=tk.W, pady=5, padx=(10, 0))

        # Pulsante aggiungi
        ttk.Button(add_frame, text=self.lang.get('add_link', "Aggiungi Collegamento"),
                   command=self._add_new_link).grid(row=0, column=4, padx=(20, 0))

        # Tabella collegamenti
        columns = ('id', 'client', 'final_code', 'final_name', 'semi_code', 'semi_name', 'actions')
        self.links_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)

        # Intestazioni colonne con traduzioni
        self.links_tree.heading('id', text='ID')
        self.links_tree.heading('client', text=self.lang.get('client_name_col', 'Cliente'))
        self.links_tree.heading('final_code', text=self.lang.get('product_code', 'Codice Finale'))
        self.links_tree.heading('final_name', text=self.lang.get('product_name', 'Nome Finale'))
        self.links_tree.heading('semi_code', text=self.lang.get('product_code', 'Codice Semilavorato'))
        self.links_tree.heading('semi_name', text=self.lang.get('product_name', 'Nome Semilavorato'))
        self.links_tree.heading('actions', text=self.lang.get('actions', 'Azioni'))

        self.links_tree.bind('<Button-1>', self._on_tree_click)

        # Dimensioni colonne
        self.links_tree.column('id', width=50)
        self.links_tree.column('client', width=120)
        self.links_tree.column('final_code', width=120)
        self.links_tree.column('final_name', width=180)
        self.links_tree.column('semi_code', width=120)
        self.links_tree.column('semi_name', width=180)
        self.links_tree.column('actions', width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.links_tree.yview)
        self.links_tree.configure(yscrollcommand=scrollbar.set)

        self.links_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Carica i clienti per il filtro
        self._load_clients()

        # Carica tutti i collegamenti iniziali
        self._load_all_links()

    def _load_clients(self):
        """Carica i clienti nel combobox"""
        clients = self.db.fetch_final_clients_for_linking()
        client_options = [f"{c.FinalClientName} ({c.AcronimForCode})" for c in clients]
        self.client_combo['values'] = client_options

        # Dizionario per mapping clienti
        self.client_dict = {}
        for c in clients:
            self.client_dict[f"{c.FinalClientName} ({c.AcronimForCode})"] = c.IDFinalClient

    def _on_client_selected(self, event):
        """Quando viene selezionato un cliente"""
        selected_client = self.client_var.get()
        if selected_client:
            client_id = self.client_dict[selected_client]

            # Carica prodotti finali per questo cliente
            final_products = self.db.fetch_final_products_by_client(client_id)
            final_options = []
            self.final_product_dict = {}
            for p in final_products:
                product_id = self._row_get_value(p, 'idproduct', 'IDProduct', index=0)
                product_code = self._row_get_value(p, 'ProductCode', 'productcode', default='N/A', index=1)
                product_name = self._row_get_value(p, 'ProductName', 'productname', default='', index=2)
                product_version = self._row_get_value(p, 'Version', 'version', default='', index=3)
                display_name = f"{product_code} - {self._format_product_name_with_version(product_name, product_version)}"
                final_options.append(display_name)
                if product_id is not None:
                    self.final_product_dict[display_name] = product_id

            self.final_product_combo['values'] = final_options

            # Carica semilavorati per questo cliente
            semi_products = self.db.fetch_semi_products_by_client(client_id)
            semi_options = []
            self.semi_product_dict = {}
            for p in semi_products:
                product_id = self._row_get_value(p, 'idproduct', 'IDProduct', index=0)
                product_code = self._row_get_value(p, 'ProductCode', 'productcode', default='N/A', index=1)
                product_name = self._row_get_value(p, 'ProductName', 'productname', default='', index=2)
                product_version = self._row_get_value(p, 'Version', 'version', default='', index=3)
                display_name = f"{product_code} - {self._format_product_name_with_version(product_name, product_version)}"
                semi_options.append(display_name)
                if product_id is not None:
                    self.semi_product_dict[display_name] = product_id

            self.semi_product_combo['values'] = semi_options

            # Carica i collegamenti per questo cliente
            self._load_links_for_client(client_id)

    def _load_all_links(self):
        """Carica tutti i collegamenti"""
        links = self.db.fetch_existing_links()
        self._populate_links_tree(links)

    def _load_links_for_client(self, client_id):
        """Carica i collegamenti per un cliente specifico"""
        links = self.db.fetch_existing_links(client_id=client_id)
        self._populate_links_tree(links)

    def _populate_links_tree(self, links):
        """Popola la tabella con i collegamenti"""
        # Pulisci la tabella
        for item in self.links_tree.get_children():
            self.links_tree.delete(item)

        # Popola la tabella
        for link in links:
            # Format product names with versions
            final_name = self._format_product_name_with_version(
                self._row_get_value(link, 'FinalName', 'finalname', default=''),
                self._row_get_value(link, 'FinalVersion', 'finalversion', default='')
            )
            semi_name = self._format_product_name_with_version(
                self._row_get_value(link, 'SemiName', 'seminame', default=''),
                self._row_get_value(link, 'SemiVersion', 'semiversion', default='')
            )
            
            self.links_tree.insert('', tk.END, values=(
                self._row_get_value(link, 'ProductLInkedTableId', 'productlinkedtableid', index=0),
                self._row_get_value(link, 'FinalClientName', 'finalclientname', default=''),
                self._row_get_value(link, 'FinalCode', 'finalcode', default=''),
                final_name,
                self._row_get_value(link, 'SemiCode', 'semicode', default=''),
                semi_name,
                "Elimina"
            ))

    def _add_new_link(self):
        """Aggiunge un nuovo collegamento"""
        final_product_text = self.final_product_var.get()
        semi_product_text = self.semi_product_var.get()

        if not final_product_text or not semi_product_text:
            messagebox.showwarning(self.lang.get('warning', "Attenzione"),
                                   self.lang.get('select_both_products',
                                                 "Seleziona sia il prodotto finale che il semilavorato"))
            return

        final_product_id = self.final_product_dict.get(final_product_text)
        semi_product_id = self.semi_product_dict.get(semi_product_text)

        if not final_product_id or not semi_product_id:
            messagebox.showerror("Errore", "Selezione prodotti non valida")
            return

        success, message = self.db.add_product_link(final_product_id, semi_product_id)

        if success:
            messagebox.showinfo("Successo", message)
            # Aggiorna la lista
            selected_client = self.client_var.get()
            if selected_client:
                client_id = self.client_dict[selected_client]
                self._load_links_for_client(client_id)
            else:
                self._load_all_links()

            # Pulisci i combobox
            self.final_product_var.set("")
            self.semi_product_var.set("")
        else:
            messagebox.showerror("Errore", message)

    def _delete_link(self, link_id):
        """Elimina un collegamento"""
        if messagebox.askyesno(self.lang.get('confirmation', "Conferma"),
                               self.lang.get('confirm_delete_link',
                                             "Sei sicuro di voler eliminare questo collegamento?")):
            success, message = self.db.delete_product_link(link_id)

            if success:
                messagebox.showinfo(self.lang.get('success', "Successo"), message)
                # Aggiorna la lista
                selected_client = self.client_var.get()
                if selected_client:
                    client_id = self.client_dict[selected_client]
                    self._load_links_for_client(client_id)
                else:
                    self._load_all_links()
            else:
                messagebox.showerror("Errore", message)

    def _on_tree_click(self, event):
        """Gestisce i click sulla tabella"""
        region = self.links_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.links_tree.identify_column(event.x)
            item = self.links_tree.identify_row(event.y)

            if column == "#7":  # Colonna Azioni
                values = self.links_tree.item(item, "values")
                link_id = values[0]
                self._delete_link(link_id)

    def open_verification_association(self, user_name=None):
        """Apre la finestra per la verifica associazione"""
        window = tk.Toplevel(self.parent)
        window.title(self.lang.get('verification_title', "Verifica Associazione"))
        window.geometry("600x500")

        # Frame principale
        main_frame = ttk.Frame(window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Etichetta utente
        if user_name:
            status_frame = ttk.Frame(main_frame)
            status_frame.pack(fill=tk.X, pady=(0, 10))
            ttk.Label(status_frame, text=f"{self.lang.get('user', 'Utente')}: {user_name}").pack(side=tk.LEFT)

        # Titolo
        title_label = ttk.Label(main_frame,
                                text=self.lang.get('verification_title', "Verifica Associazione"),
                                font=("Helvetica", 14, "bold"))
        title_label.pack(pady=(0, 20))

        # Filtro Cliente
        ttk.Label(main_frame, text=self.lang.get('select_client', "Seleziona Cliente:")).pack(anchor=tk.W, pady=(0, 5))

        self.client_var = tk.StringVar()
        self.client_combo = ttk.Combobox(main_frame, textvariable=self.client_var, width=40, state="readonly")
        self.client_combo.pack(fill=tk.X, pady=(0, 15))
        self.client_combo.bind('<<ComboboxSelected>>', self._on_client_selected_verification)

        # Anno
        year_frame = ttk.Frame(main_frame)
        year_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(year_frame, text=self.lang.get('year', "Anno:")).pack(side=tk.LEFT, padx=(0, 5))

        self.year_var = tk.StringVar(value=str(datetime.now().year))
        year_entry = ttk.Entry(year_frame, textvariable=self.year_var, width=10)
        year_entry.pack(side=tk.LEFT, padx=(0, 10))
        year_entry.bind('<KeyRelease>', self._on_year_changed)

        ttk.Button(year_frame, text=self.lang.get('refresh', "Aggiorna"),
                   command=self._load_orders).pack(side=tk.LEFT)

        # Filtro Ordine
        ttk.Label(main_frame, text=self.lang.get('select_order', "Seleziona Ordine:")).pack(anchor=tk.W, pady=(0, 5))

        self.order_var = tk.StringVar()
        self.order_combo = ttk.Combobox(main_frame, textvariable=self.order_var, width=40, state="readonly")
        self.order_combo.pack(fill=tk.X, pady=(0, 15))

        # Etichetta
        ttk.Label(main_frame, text=self.lang.get('label_code', "Codice Etichetta:")).pack(anchor=tk.W, pady=(0, 5))

        self.label_var = tk.StringVar()
        self.label_entry = ttk.Entry(main_frame, textvariable=self.label_var, width=40)
        self.label_entry.pack(fill=tk.X, pady=(0, 15))
        self.label_entry.bind('<Return>', self._verify_label)

        # Pulsante verifica
        ttk.Button(main_frame, text=self.lang.get('verify', "Verifica"),
                   command=self._verify_label).pack(pady=10)

        # Risultato
        self.result_text = tk.Text(main_frame, height=8, width=50, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Carica i clienti
        self._load_clients_verification()

        # Carica gli ordini per l'anno corrente
        self._load_orders()

    def _load_clients_verification(self):
        """Carica i clienti per la verifica"""
        clients = self.db.fetch_clients_for_verification()
        client_options = [f"{c.FinalClientName} (ID: {c.idclient})" for c in clients]
        self.client_combo['values'] = client_options

        # Dizionario per mapping clienti
        self.client_dict = {}
        for c in clients:
            self.client_dict[f"{c.FinalClientName} (ID: {c.idclient})"] = c.idclient

    def _on_client_selected_verification(self, event):
        """Quando viene selezionato un cliente"""
        self._load_orders()

    def _on_year_changed(self, event):
        """Quando cambia l'anno"""
        # Potremmo aggiungere un debounce qui se necessario
        pass

    def _load_orders(self):
        """Carica gli ordini in base a cliente e anno"""
        try:
            year = int(self.year_var.get())
        except ValueError:
            messagebox.showerror("Errore", "Anno non valido")
            return

        client_id = None
        selected_client = self.client_var.get()
        if selected_client:
            client_id = self.client_dict.get(selected_client)

        orders = self.db.fetch_orders_by_year_and_client(year, client_id)
        order_options = [
            f"{self._row_get_value(o, 'OrderNumber', 'ordernumber', default='')} - "
            f"{self._row_get_value(o, 'productcode', 'ProductCode', default='')} - "
            f"{self._row_get_value(o, 'FinalClientName', 'finalclientname', default='')}"
            for o in orders
        ]
        self.order_combo['values'] = order_options

        # Dizionario per mapping ordini
        self.order_dict = {}
        for o in orders:
            key = (
                f"{self._row_get_value(o, 'OrderNumber', 'ordernumber', default='')} - "
                f"{self._row_get_value(o, 'productcode', 'ProductCode', default='')} - "
                f"{self._row_get_value(o, 'FinalClientName', 'finalclientname', default='')}"
            )
            self.order_dict[key] = self._row_get_value(o, 'idorder', 'IDOrder', default=None)

    def _verify_label(self, event=None):
        """Verifica l'associazione dell'etichetta"""
        label_code = self.label_var.get().strip()
        selected_order = self.order_var.get()

        if not label_code:
            messagebox.showwarning("Attenzione", "Inserire il codice etichetta")
            self.label_entry.focus()
            return

        if not selected_order:
            messagebox.showwarning("Attenzione", "Selezionare un ordine")
            return

        # Verifica l'etichetta
        results = self.db.verify_label_association(label_code)

        if not results:
            messagebox.showerror("Errore", "Etichetta non trovata")
            self.label_var.set("")
            self.label_entry.focus()
            return

        # Controlla se l'ordine corrisponde
        selected_order_id = self.order_dict.get(selected_order)
        order_numbers = [str(self._row_get_value(r, 'OrderNumber', 'ordernumber', default='')) for r in results]

        if selected_order_id and str(selected_order_id) not in order_numbers:
            messagebox.showerror("Errore", "Ordine relativo alla scheda NON corrisponde con l'ordine in lavoro")
            self.label_var.set("")
            self.label_entry.focus()
            return

        # Mostra i risultati
        self._display_results(results)

    def _display_results(self, results):
        """Mostra i risultati della verifica"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        if results:
            result = results[0]  # Prendi il primo risultato
            text = f"✓ VERIFICA COMPLETATA CON SUCCESSO\n\n"
            text += f"Codice Etichetta: {self._row_get_value(result, 'LabelCod', 'labelcod', default='N/D')}\n"
            text += f"Numero Ordine: {self._row_get_value(result, 'OrderNumber', 'ordernumber', default='N/D')}\n"
            text += f"Codice Prodotto: {self._row_get_value(result, 'ProductCode', 'productcode', default='N/D')}\n"
            text += f"ID Scheda: {self._row_get_value(result, 'IDBoard', 'idboard', default='N/D')}\n\n"
            text += f"L'etichetta è correttamente associata all'ordine selezionato."
        else:
            text = "Nessun risultato trovato."

        self.result_text.insert(1.0, text)
        self.result_text.config(state=tk.DISABLED)
