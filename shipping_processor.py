# shipping_processor.py
import pandas as pd
from datetime import datetime


def process_shipping_file(file_path, shipping_settings, xls_config):
    """
    Analizza il file Excel con una logica di parsing avanzata che gestisce
    sia le date come testo sia come oggetti datetime nativi di Excel,
    scansionando tutte le colonne per la massima compatibilità.
    """
    try:
        # 1. Estrae la configurazione (nome del foglio)
        sheet_name = xls_config.get('sheet_name')
        if not sheet_name:
            return None, None, "Nome del foglio di lavoro non configurato nelle Impostazioni XLS."

        # 2. Carica il file Excel
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)

        # 3. Ottieni i giorni di spedizione "Normale" configurati
        if not shipping_settings:
            return None, None, "Nessuna impostazione di spedizione trovata."
        shipping_days = [s.DayOfWeek for s in shipping_settings if
                         s.ShippingType and s.ShippingType.strip().lower() == 'normal']
        if not shipping_days:
            return None, None, "Nessun giorno di spedizione di tipo 'Normale' è stato configurato."

        # 4. Trova la colonna con la data di spedizione corretta
        today = datetime.now().date()
        target_date_col_name = None
        shipping_date = None

        # Itera su TUTTE le colonne del file
        for col_name in df.columns:
            try:
                col_date = None
                # --- LOGICA DI CONVERSIONE ROBUSTA ---
                # Tentativo 1: L'intestazione è già un oggetto data/ora?
                if isinstance(col_name, datetime):
                    col_date = col_name.date()
                # Tentativo 2: Prova a interpretarlo come stringa
                else:
                    # errors='coerce' trasforma in 'NaT' (Not a Time) tutto ciò che non capisce
                    col_date_obj = pd.to_datetime(str(col_name), errors='coerce')
                    if not pd.isna(col_date_obj):
                        col_date = col_date_obj.date()

                # Se la conversione non ha prodotto una data, salta alla colonna successiva
                if not col_date:
                    continue
                # --- FINE LOGICA ROBUSTA ---

                col_weekday = col_date.weekday() + 1  # 1=Lunedì

                # Cerca la prima data che soddisfa entrambe le condizioni
                if col_date >= today and col_weekday in shipping_days:
                    target_date_col_name = col_name
                    shipping_date = col_date
                    break  # Trovata la colonna, esci dal ciclo
            except (ValueError, TypeError, AttributeError):
                continue  # Ignora le colonne che non sono date in nessun formato

        if not target_date_col_name:
            return None, None, "Nessuna data di spedizione valida (uguale o successiva a oggi e configurata) trovata nelle colonne del file Excel."

        # 5. Elabora i dati per la colonna trovata
        df_shipping = df[pd.to_numeric(df[target_date_col_name], errors='coerce').fillna(0) > 0].copy()

        if df_shipping.empty:
            summary = {'next_ship_date': shipping_date.strftime('%d/%m/%Y'), 'total_orders': 0, 'total_quantity': 0}
            return [], summary, None

        processed_data = []
        for index, row in df_shipping.iterrows():
            processed_data.append({
                'id': None, 'shipping_date': shipping_date, 'order': str(row.iloc[4]),
                'product': str(row.iloc[3]), 'original_qty': int(row[target_date_col_name]),
                'modified_qty': None, 'note': "", 'status': 'status_new', 'user': "System"
            })

        summary = {
            'next_ship_date': shipping_date.strftime('%d/%m/%Y'),
            'total_orders': df_shipping.iloc[:, 4].nunique(),
            'total_quantity': df_shipping[target_date_col_name].sum()
        }

        return processed_data, summary, None

    except Exception as e:
        return None, None, f"Errore GRAVE durante l'elaborazione del file Excel: {e}"