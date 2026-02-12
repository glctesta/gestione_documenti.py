"""
Label Printer Module
Gestisce la generazione e stampa di etichette per componenti.
Supporta stampanti Zebra (ZPL), Brother e ZJIANG (ESC/POS).
"""

import logging
from typing import Dict, Any, Tuple, Optional
from io import BytesIO
from printer_config import PrinterConfigManager
from printer_connection_manager import get_printer_connection, PrinterConnectionError

logger = logging.getLogger("TraceabilityRS")


def load_label_config(db) -> Dict[str, Any]:
    """
    Carica la configurazione etichetta dal database.
    
    Returns:
        dict: Configurazione con dimensioni e campi da stampare
    """
    try:
        cursor = db.conn.cursor()
        query = """
        SELECT TOP 1 
            LabelWidth, LabelHeight,
            PrintOrderNumber, PrintMaterialCode, PrintComponentQuantity, PrintReferences,
            OrderNumberPosition, MaterialCodePosition, ComponentQuantityPosition, ReferencesPosition,
            TSPLXOffset, TSPLYOffset, TSPLLineSpacing, TSPLFontSize, TSPLFontMultiplierX, TSPLFontMultiplierY,
            TSPLQRCodeX, TSPLQRCodeY, TSPLQRCodeCellWidth
        FROM [Traceability_RS].[dbo].[LabelConfiguration]
        WHERE IsActive = 1
        ORDER BY ConfigID DESC
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        
        if row:
            (width, height,
             print_order, print_material, print_qty, print_refs,
             order_pos, material_pos, qty_pos, refs_pos,
             tspl_x, tspl_y, tspl_spacing, tspl_font, tspl_mul_x, tspl_mul_y,
             qr_x, qr_y, qr_cell) = row
            
            config = {
                'width': float(width) if width else 10.0,
                'height': float(height) if height else 5.0,
                'print_order_number': bool(print_order),
                'print_material_code': bool(print_material),
                'print_component_quantity': bool(print_qty),
                'print_references': bool(print_refs),
                'order_number_position': order_pos if order_pos else 1,
                'material_code_position': material_pos if material_pos else 2,
                'component_quantity_position': qty_pos if qty_pos else 3,
                'references_position': refs_pos if refs_pos else 4,
                # TSPL parameters with defaults for backward compatibility
                'tspl_x_offset': tspl_x if tspl_x is not None else 120,
                'tspl_y_offset': tspl_y if tspl_y is not None else 100,
                'tspl_line_spacing': tspl_spacing if tspl_spacing is not None else 60,
                'tspl_font_size': tspl_font if tspl_font else "3",
                'tspl_font_multiplier_x': tspl_mul_x if tspl_mul_x is not None else 1,
                'tspl_font_multiplier_y': tspl_mul_y if tspl_mul_y is not None else 1,
                # QR Code parameters
                'tspl_qr_x': qr_x if qr_x is not None else 450,
                'tspl_qr_y': qr_y if qr_y is not None else 100,
                'tspl_qr_cell_width': qr_cell if qr_cell is not None else 4
            }
            
            logger.info(f"Configurazione etichetta caricata: {width}x{height} cm")
            return config
        else:
            # Configurazione di default
            logger.warning("Nessuna configurazione etichetta trovata, uso default")
            return {
                'width': 10.0,
                'height': 5.0,
                'print_order_number': True,
                'print_material_code': True,
                'print_component_quantity': True,
                'print_references': True,
                'order_number_position': 1,
                'material_code_position': 2,
                'component_quantity_position': 3,
                'references_position': 4,
                'tspl_x_offset': 120,
                'tspl_y_offset': 100,
                'tspl_line_spacing': 60,
                'tspl_font_size': "3",
                'tspl_font_multiplier_x': 1,
                'tspl_font_multiplier_y': 1,
                'tspl_qr_x': 450,
                'tspl_qr_y': 100,
                'tspl_qr_cell_width': 4
            }
    except Exception as e:
        logger.error(f"Errore caricamento configurazione etichetta: {e}")
        # Ritorna configurazione di default in caso di errore
        return {
            'width': 10.0,
            'height': 5.0,
            'print_order_number': True,
            'print_material_code': True,
            'print_component_quantity': True,
            'print_references': True,
            'order_number_position': 1,
            'material_code_position': 2,
            'component_quantity_position': 3,
            'references_position': 4,
            'tspl_x_offset': 120,
            'tspl_y_offset': 100,
            'tspl_line_spacing': 60,
            'tspl_font_size': "3",
            'tspl_font_multiplier_x': 1,
            'tspl_font_multiplier_y': 1,
            'tspl_qr_x': 450,
            'tspl_qr_y': 100,
            'tspl_qr_cell_width': 4
        }


def generate_zpl_label(label_data: Dict[str, Any], label_config: Dict[str, Any]) -> str:
    """
    Genera comandi ZPL per stampanti Zebra.
    
    Args:
        label_data: Dati dell'etichetta (OrderNumber, ComponentCode, etc.)
        label_config: Configurazione dimensioni e campi da stampare
        
    Returns:
        str: Comandi ZPL per la stampa
    """
    # Converti dimensioni da cm a dots (203 DPI per Zebra)
    # 1 cm = 80 dots circa a 203 DPI
    width_dots = int(label_config['width'] * 80)
    height_dots = int(label_config['height'] * 80)
    
    # Inizia comando ZPL
    zpl = "^XA\n"  # Inizio formato
    
    # Imposta dimensioni etichetta
    zpl += f"^PW{width_dots}\n"  # Larghezza
    zpl += f"^LL{height_dots}\n"  # Lunghezza
    
    # Prepara i campi da stampare in ordine di posizione
    fields = []
    
    if label_config['print_order_number']:
        fields.append((
            label_config['order_number_position'],
            f"Order: {label_data['OrderNumber']}"
        ))
    
    if label_config['print_material_code']:
        fields.append((
            label_config['material_code_position'],
            f"Component: {label_data['ComponentCode']}"
        ))
    
    if label_config['print_component_quantity']:
        fields.append((
            label_config['component_quantity_position'],
            f"Qty: {label_data['OrderQuantity']}"
        ))
    
    if label_config['print_references']:
        fields.append((
            label_config['references_position'],
            f"Ref: {label_data['References']}"
        ))
    
    # Ordina i campi per posizione
    fields.sort(key=lambda x: x[0])
    
    # Posiziona i campi sull'etichetta
    y_position = 50  # Posizione Y iniziale
    y_increment = 80  # Incremento tra le righe
    
    for _, field_text in fields:
        zpl += f"^FO50,{y_position}^A0N,40,40^FD{field_text}^FS\n"
        y_position += y_increment
    
    # Aggiungi QR code se disponibile
    if label_data.get('QRCodeImage'):
        qr_x = width_dots - 200  # Posizione X (a destra)
        qr_y = 50  # Posizione Y
        qr_data = label_data['ComponentCode']
        
        # Comando QR code ZPL
        zpl += f"^FO{qr_x},{qr_y}^BQN,2,6^FDQA,{qr_data}^FS\n"
    
    zpl += "^XZ\n"  # Fine formato
    
    logger.info("Comando ZPL generato")
    return zpl


def generate_escpos_label(label_data: Dict[str, Any], label_config: Dict[str, Any], model: str) -> str:
    """
    Genera comandi per stampanti Brother e ZJIANG.
    ZJIANG usa TSPL (TSC Printer Language), Brother usa ESC/POS.
    
    Args:
        label_data: Dati dell'etichetta
        label_config: Configurazione dimensioni e campi
        model: Modello stampante (BROTHER o ZJIANG)
        
    Returns:
        str: Comandi per la stampa
    """
    # Per ZJIANG, usa TSPL (TSC Printer Language)
    if model == 'ZJIANG':
        # Usa millimetri per SIZE e GAP, dots per TEXT
        width_mm = int(label_config['width'] * 10)  # cm -> mm
        height_mm = int(label_config['height'] * 10)  # cm -> mm
        
        # Comandi TSPL
        commands = []
        
        # Imposta dimensioni etichetta in mm (più affidabile per SIZE/GAP)
        commands.append(f"SIZE {width_mm} mm,{height_mm} mm")
        
        # Imposta gap tra etichette in mm
        commands.append("GAP 2 mm,0 mm")
        
        # Modalità tear-off (stacca etichetta dopo stampa)
        commands.append("SET TEAR ON")
        
        # Direzione stampa (0 = normale)
        commands.append("DIRECTION 0")
        
        # Imposta densità di stampa (0-15, default 8)
        commands.append("DENSITY 12")
        
        # Imposta velocità di stampa (2-4, default 4)
        commands.append("SPEED 3")
        
        # Cancella buffer
        commands.append("CLS")
        
        # Prepara i campi da stampare in ordine di posizione
        # Usa etichette corte per risparmiare spazio
        fields = []
        
        if label_config['print_order_number']:
            fields.append((
                label_config['order_number_position'],
                f"Ord:{label_data['OrderNumber']}"  # Abbreviato
            ))
        
        if label_config['print_material_code']:
            fields.append((
                label_config['material_code_position'],
                f"{label_data['ComponentCode']}"  # Solo il codice, senza etichetta
            ))
        
        if label_config['print_component_quantity']:
            fields.append((
                label_config['component_quantity_position'],
                f"Q:{label_data['OrderQuantity']}"  # Abbreviato
            ))
        
        if label_config['print_references']:
            fields.append((
                label_config['references_position'],
                f"Rif:{label_data['References']}"  # Abbreviato
            ))
        
        # Ordina i campi per posizione
        fields.sort(key=lambda x: x[0])\
        
        # Stampa i campi con comando TEXT usando coordinate in dots
        # TEXT x, y, "font", rotation, x-multiplication, y-multiplication, "content"
        # Usa parametri dalla configurazione invece di valori hardcoded
        # 203 DPI = 8 dots/mm
        # Etichetta 50mm = 400 dots, quindi Y max utilizzabile è circa 350
        y_position = label_config['tspl_y_offset']  # Da configurazione
        y_increment = label_config['tspl_line_spacing']  # Da configurazione
        x_position = label_config['tspl_x_offset']  # Da configurazione
        font_size = label_config['tspl_font_size']  # Da configurazione
        font_mul_x = label_config['tspl_font_multiplier_x']  # Da configurazione
        font_mul_y = label_config['tspl_font_multiplier_y']  # Da configurazione
        
        for _, field_text in fields:
            # Usa parametri configurabili per font e posizione
            commands.append(f'TEXT {x_position},{y_position},"{font_size}",0,{font_mul_x},{font_mul_y},"{field_text}"')
            y_position += y_increment
        
        # Aggiungi QR code sul lato destro dell'etichetta
        # QRCODE x, y, error_correction_level, cell_width, mode, rotation, "data"
        # Error correction: L=1, M=2, Q=3, H=4
        # Usa parametri dalla configurazione
        qr_x = label_config['tspl_qr_x']  # Da configurazione
        qr_y = label_config['tspl_qr_y']  # Da configurazione
        qr_cell_width = label_config['tspl_qr_cell_width']  # Da configurazione
        
        # Stampa QR code con il codice componente
        component_code = label_data.get('ComponentCode', '')
        if component_code:
            commands.append(f'QRCODE {qr_x},{qr_y},L,{qr_cell_width},A,0,"{component_code}"')
        
        # Stampa 1 etichetta
        commands.append("PRINT 1")
        
        # Unisci tutti i comandi con \r\n (TSPL richiede CRLF)
        tspl_commands = "\r\n".join(commands) + "\r\n"
        
        logger.info("=" * 80)
        logger.info(f"✅ COMANDI TSPL GENERATI PER {model}")
        logger.info("=" * 80)
        logger.info(f"📦 Contenuto etichetta: {[f[1] for f in fields]}")
        logger.info(f"📏 Dimensioni etichetta: {width_mm}x{height_mm} mm")
        logger.info(f"📝 Numero comandi TSPL: {len(commands)}")
        logger.info("=" * 80)
        logger.info("🔍 COMANDI TSPL COMPLETI:")
        logger.info("-" * 80)
        for i, cmd in enumerate(commands, 1):
            logger.info(f"  {i:2d}. {cmd}")
        logger.info("-" * 80)
        logger.info("=" * 80)
        
        return tspl_commands
    
    # Per BROTHER, usa comandi ESC/POS standard
    else:
        # ESC/POS commands
        ESC = chr(27)
        GS = chr(29)
        
        # Inizializza stampante
        commands = f"{ESC}@"  # Initialize printer
        
        # Imposta dimensioni carattere (se supportato)
        commands += f"{ESC}!{chr(0x10)}"  # Double height
        
        # Prepara i campi da stampare in ordine di posizione
        fields = []
        
        if label_config['print_order_number']:
            fields.append((
                label_config['order_number_position'],
                f"Order: {label_data['OrderNumber']}"
            ))
        
        if label_config['print_material_code']:
            fields.append((
                label_config['material_code_position'],
                f"Component: {label_data['ComponentCode']}"
            ))
        
        if label_config['print_component_quantity']:
            fields.append((
                label_config['component_quantity_position'],
                f"Qty: {label_data['OrderQuantity']}"
            ))
        
        if label_config['print_references']:
            fields.append((
                label_config['references_position'],
                f"Ref: {label_data['References']}"
            ))
        
        # Ordina i campi per posizione
        fields.sort(key=lambda x: x[0])
        
        # Stampa i campi
        for _, field_text in fields:
            commands += f"{field_text}\n"
        
        # Taglia carta (se supportato)
        commands += f"\n\n\n{GS}V{chr(66)}{chr(0)}"  # Cut paper
        
        logger.info(f"Comando ESC/POS generato per {model}")
        return commands


def print_label(label_data: Dict[str, Any], db) -> Tuple[bool, Optional[str]]:
    """
    Stampa un'etichetta usando la configurazione corrente.
    
    Args:
        label_data: Dati dell'etichetta da stampare
        db: Database handler
        
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    try:
        logger.info("=" * 80)
        logger.info("🏁 PRINT_LABEL: INIZIO PROCESSO DI STAMPA ETICHETTA")
        logger.info("=" * 80)
        logger.info(f"📦 PRINT_LABEL: Componente: {label_data.get('ComponentCode', 'N/A')}")
        logger.info(f"📦 PRINT_LABEL: Ordine: {label_data.get('OrderNumber', 'N/A')}")
        logger.info(f"📦 PRINT_LABEL: Fase: {label_data.get('Phase', 'N/A')}")
        
        # Carica configurazione etichetta
        logger.info("⚙️ PRINT_LABEL: Caricamento configurazione etichetta dal database...")
        label_config = load_label_config(db)
        logger.info(f"⚙️ PRINT_LABEL: ✓ Configurazione etichetta caricata: {label_config.get('width')}x{label_config.get('height')} cm")
        
        # Carica configurazione stampante
        logger.info("⚙️ PRINT_LABEL: Caricamento configurazione stampante...")
        printer_config_manager = PrinterConfigManager()
        printer_config = printer_config_manager.get_config()
        
        logger.info(f"⚙️ PRINT_LABEL: ✓ Configurazione stampante: {printer_config_manager.get_config_summary()}")
        
        # Determina il tipo di stampante e genera il comando appropriato
        connection_type = printer_config.get('connection_type', 'DEFAULT')
        printer_model = printer_config.get('printer_model', 'ZEBRA')
        
        logger.info(f"🔧 PRINT_LABEL: Tipo connessione: {connection_type}")
        logger.info(f"🔧 PRINT_LABEL: Modello stampante: {printer_model}")
        
        # Genera comandi stampante
        logger.info("=" * 80)
        logger.info("📝 PRINT_LABEL: GENERAZIONE COMANDI STAMPANTE")
        logger.info("=" * 80)
        logger.info(f"🔧 PRINT_LABEL: MODELLO STAMPANTE CONFIGURATO: '{printer_model}'")
        logger.info(f"🔧 PRINT_LABEL: TIPO CONNESSIONE: '{connection_type}'")
        
        if printer_model == 'ZEBRA':
            logger.info("📝 PRINT_LABEL: ➡️ Generazione comandi ZPL per stampante ZEBRA...")
            label_commands = generate_zpl_label(label_data, label_config)
            logger.info("📝 PRINT_LABEL: ✓ Comandi ZPL generati con successo")
            logger.info("📝 PRINT_LABEL: Tipo comandi: ZPL (Zebra Programming Language)")
        elif printer_model in ['BROTHER', 'ZJIANG']:
            if printer_model == 'ZJIANG':
                logger.info("📝 PRINT_LABEL: ➡️ Generazione comandi TSPL per stampante ZJIANG ZJ-9210...")
                logger.info("📝 PRINT_LABEL: Tipo comandi: TSPL (TSC Printer Language)")
            else:
                logger.info("📝 PRINT_LABEL: ➡️ Generazione comandi ESC/POS per stampante BROTHER...")
                logger.info("📝 PRINT_LABEL: Tipo comandi: ESC/POS")
            
            label_commands = generate_escpos_label(label_data, label_config, printer_model)
            logger.info(f"📝 PRINT_LABEL: ✓ Comandi generati con successo per {printer_model}")
        else:
            # Default a ZPL per stampanti sconosciute
            logger.warning("=" * 80)
            logger.warning(f"⚠️ PRINT_LABEL: ATTENZIONE - MODELLO STAMPANTE SCONOSCIUTO: '{printer_model}'")
            logger.warning("⚠️ PRINT_LABEL: Uso comandi ZPL come default")
            logger.warning("⚠️ PRINT_LABEL: Se la stampante non è Zebra, la stampa potrebbe NON funzionare!")
            logger.warning("=" * 80)
            label_commands = generate_zpl_label(label_data, label_config)
            logger.info("📝 PRINT_LABEL: ✓ Comandi ZPL generati (default)")
        
        logger.info("=" * 80)
        
        logger.info(f"📝 PRINT_LABEL: Lunghezza comandi generati: {len(label_commands)} caratteri")
        
        # Ottieni connessione stampante
        logger.info("🔌 PRINT_LABEL: Ottenimento connessione stampante...")
        printer_connection = get_printer_connection(printer_config)
        logger.info(f"🔌 PRINT_LABEL: ✓ Connessione stampante ottenuta: {type(printer_connection).__name__}")
        
        # Stampa etichetta
        logger.info("🖨️ PRINT_LABEL: Invio etichetta alla stampante...")
        logger.info("-" * 80)
        printer_connection.print_label(label_commands)
        logger.info("-" * 80)
        logger.info("🖨️ PRINT_LABEL: ✓ Etichetta inviata alla stampante")
        
        logger.info("=" * 80)
        logger.info(f"✅ PRINT_LABEL: STAMPA COMPLETATA CON SUCCESSO - Componente: {label_data['ComponentCode']}")
        logger.info("=" * 80)
        return True, None
        
    except PrinterConnectionError as e:
        error_msg = f"Errore connessione stampante: {str(e)}"
        logger.error("=" * 80)
        logger.error(f"❌ PRINT_LABEL: ERRORE CONNESSIONE STAMPANTE")
        logger.error(f"❌ PRINT_LABEL: {error_msg}")
        logger.error("=" * 80)
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Errore durante la stampa: {str(e)}"
        logger.error("=" * 80)
        logger.error(f"❌ PRINT_LABEL: ERRORE GENERICO DURANTE LA STAMPA")
        logger.error(f"❌ PRINT_LABEL: {error_msg}", exc_info=True)
        logger.error("=" * 80)
        return False, error_msg
