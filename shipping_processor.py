# shipping_processor.py
import pandas as pd
from datetime import datetime


def process_shipping_file(file_path, shipping_settings, db_data, user_name, xls_config):
    """
    Analizza il file Excel, lo confronta con i dati del DB e assegna uno stato a ogni riga.
    """
    try:
        sheet_name = xls_config.get('sheet_name')
        if not sheet_name:
            return None, None, "Nome del foglio di lavoro non configurato nelle Impostazioni XLS."

        df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)

        if not shipping_settings:
            return None, None, "Nessuna impostazione di spedizione trovata."
        shipping_days = [s.DayOfWeek for s in shipping_settings if
                         s.ShippingType and s.ShippingType.strip().lower() == 'normal']
        if not shipping_days:
            return None, None, "Nessun giorno di spedizione di tipo 'Normale' è stato configurato."

        today = datetime.now().date()
        target_date_col_name = None
        shipping_date = None

        for col_name in df.columns:
            try:
                col_date = None
                if isinstance(col_name, datetime):
                    col_date = col_name.date()
                else:
                    col_date_obj = pd.to_datetime(str(col_name), errors='coerce')
                    if not pd.isna(col_date_obj):
                        col_date = col_date_obj.date()

                if not col_date:
                    continue

                col_weekday = col_date.weekday() + 1

                if col_date >= today and col_weekday in shipping_days:
                    target_date_col_name = col_name
                    shipping_date = col_date
                    break
            except (ValueError, TypeError, AttributeError):
                continue

        if not target_date_col_name:
            return None, None, "Nessuna data di spedizione valida trovata nel file Excel."

        df_shipping = df[pd.to_numeric(df[target_date_col_name], errors='coerce').fillna(0) > 0].copy()

        processed_data = []
        db_items_map = {(str(item.OrderNumber), str(item.ProductCode)): item for item in db_data}
        file_keys_processed = set()

        for index, row in df_shipping.iterrows():
            order = str(row.iloc[4])
            product = str(row.iloc[3])
            key = (order, product)
            file_keys_processed.add(key)

            original_qty = int(row[target_date_col_name])
            db_item = db_items_map.get(key)

            item_data = {
                'id': None, 'shipping_date': shipping_date, 'order': order, 'product': product,
                'original_qty': original_qty, 'modified_qty': None, 'note': "",
                'status': 'status_new', 'user': user_name
            }

            if db_item:
                item_data.update({
                    'id': db_item.ItemId, 'note': db_item.Note or "",
                    'modified_qty': db_item.ModifiedQty, 'status': 'status_confirmed'
                })
                db_qty = db_item.ModifiedQty if db_item.ModifiedQty is not None else db_item.OriginalQty
                if db_qty != original_qty:
                    item_data['status'] = 'status_modified_by_plan'

            processed_data.append(item_data)

        for db_item in db_data:
            key = (str(db_item.OrderNumber), str(db_item.ProductCode))
            if key not in file_keys_processed:
                processed_data.append({
                    'id': db_item.ItemId, 'shipping_date': shipping_date, 'order': db_item.OrderNumber,
                    'product': db_item.ProductCode, 'original_qty': db_item.OriginalQty,
                    'modified_qty': db_item.ModifiedQty, 'note': db_item.Note,
                    'status': 'status_removed_by_plan', 'user': user_name
                })

        summary = {
            'next_ship_date': shipping_date.strftime('%d/%m/%Y'),
            'total_orders': df_shipping.iloc[:, 4].nunique(),
            'total_quantity': df_shipping[target_date_col_name].sum()
        }

        return processed_data, summary, None

    except Exception as e:
        return None, None, f"Errore durante l'elaborazione del file Excel: {e}"