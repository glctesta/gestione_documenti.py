"""
Generatore di report PDF per validazione FAI
Crea un PDF che assomiglia al form cartaceo FAI
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os
import logging

logger = logging.getLogger("TraceabilityRS")

DEFAULT_DECLARATION_LABELS = {
    'NPI': 'NPI (PRESERIE)',
    'Test': 'TEST',
    'PRODUCTION': 'PRODUCȚIE',
    'StandardProcessDeviation': 'VARIAȚIA STANDARD A PROCESULUI',
    'Others': 'ALTELE'
}

# Registra font per caratteri speciali rumeni
try:
    # Cerca font DejaVu nella directory corrente
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Registra DejaVu Sans per testo normale
    dejavu_path = os.path.join(base_dir, 'DejaVuSans.ttf')
    if os.path.exists(dejavu_path):
        pdfmetrics.registerFont(TTFont('DejaVu', dejavu_path))
        logger.info("Font DejaVu registrato con successo")
        USE_DEJAVU = True
    else:
        logger.warning(f"Font DejaVu non trovato in {dejavu_path}, uso Helvetica")
        USE_DEJAVU = False
        
    # Registra DejaVu Sans Bold
    dejavu_bold_path = os.path.join(base_dir, 'DejaVuSans-Bold.ttf')
    if os.path.exists(dejavu_bold_path):
        pdfmetrics.registerFont(TTFont('DejaVu-Bold', dejavu_bold_path))
except Exception as e:
    logger.warning(f"Impossibile registrare font DejaVu: {e}")
    USE_DEJAVU = False


class FAIReportGenerator:
    """Genera report PDF per validazione FAI"""
    
    def __init__(self, output_path):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=12*mm,
            rightMargin=12*mm,
            topMargin=10*mm,
            bottomMargin=10*mm
        )
        self.styles = getSampleStyleSheet()
        self.elements = []
        
        # Usa DejaVu se disponibile, altrimenti Helvetica
        base_font = 'DejaVu' if USE_DEJAVU else 'Helvetica'
        bold_font = 'DejaVu-Bold' if USE_DEJAVU else 'Helvetica-Bold'
        
        # Crea stili custom
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=14,
            textColor=colors.HexColor('#000080'),
            alignment=TA_CENTER,
            spaceAfter=6
        )
        
        self.section_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=10,
            bold=True,
            spaceBefore=3,
            spaceAfter=3
        )
    
    def add_header(self, template_data, validation_data):
        """Aggiunge l'intestazione del report con logo"""
        
        # Font da usare
        base_font = 'DejaVu' if USE_DEJAVU else 'Helvetica'
        bold_font = 'DejaVu-Bold' if USE_DEJAVU else 'Helvetica-Bold'
        
        # Logo Vandewiele (ridotto)
        logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=25*mm, height=8*mm)
        else:
            logo = Paragraph("<b>VANDEWIELE</b>", self.title_style)
        
        # Intestazione tabella
        header_data = [
            [logo, 'FORMULAR', 'FAI (Inspecția primei plăci) PTH', ''],
            ['', 'Nr. document', 'Revizia', 'Data ultim. rev.', 'Nr. pagini'],
            ['', template_data.get('NrDocument', ''), 
             template_data.get('Revision', ''), 
             template_data.get('RevisionDate', datetime.now().strftime('%d/%m/%Y')),
             '1']
        ]
        
        header_table = Table(header_data, colWidths=[25*mm, 32*mm, 64*mm, 39*mm])
        header_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), base_font),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (1, 0), (1, 0), bold_font),
            ('FONTNAME', (2, 0), (2, 0), bold_font),
            ('FONTSIZE', (2, 0), (2, 0), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (0, 0), (0, 2)),
            ('SPAN', (2, 0), (3, 0)),
            ('LEFTPADDING', (0, 0), (-1, -1), 1),
            ('RIGHTPADDING', (0, 0), (-1, -1), 1),
        ]))
        
        self.elements.append(header_table)
        self.elements.append(Spacer(1, 5*mm))
    
    def add_validation_types(self, validation_data, declaration_labels=None, product_code='', order_number='', quantity=''):
        """Aggiunge la sezione dei tipi di validazione."""

        base_font = 'DejaVu' if USE_DEJAVU else 'Helvetica'
        bold_font = 'DejaVu-Bold' if USE_DEJAVU else 'Helvetica-Bold'

        text_style = ParagraphStyle(
            'ValidationText',
            fontName=base_font,
            fontSize=8,
            leading=10,
            alignment=0
        )

        labels = dict(DEFAULT_DECLARATION_LABELS)
        if declaration_labels:
            labels.update(declaration_labels)

        def mark(value, label):
            return Paragraph(f"{'[x]' if value else '[ ]'} {label}", text_style)

        types_data = [
            [Paragraph(f'Cod: {product_code}', text_style),
             Paragraph('', text_style),
             Paragraph('Comanda SL:', text_style),
             Paragraph(order_number, text_style),
             Paragraph('Interval SN per panel:', text_style),
             Paragraph('', text_style)],
            [Paragraph(f'Cantitate: {quantity}', text_style),
             mark(validation_data.get('NPI'), labels['NPI']),
             mark(validation_data.get('PRODUCTION'), labels['PRODUCTION']),
             mark(validation_data.get('StandardProcessDeviation'), labels['StandardProcessDeviation']),
             Paragraph('', text_style),
             Paragraph('', text_style)],
            [mark(validation_data.get('Test'), labels['Test']),
             mark(validation_data.get('Others'), labels['Others']),
             Paragraph('', text_style),
             Paragraph('', text_style),
             Paragraph('', text_style),
             Paragraph('', text_style)]
        ]

        types_table = Table(types_data, colWidths=[26*mm, 26*mm, 20*mm, 28*mm, 33*mm, 27*mm])
        types_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), base_font),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (1, 1), (3, 1), bold_font),
            ('FONTSIZE', (1, 1), (3, 1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 1),
            ('RIGHTPADDING', (0, 0), (-1, -1), 1),
        ]))

        self.elements.append(types_table)
        self.elements.append(Spacer(1, 3*mm))
    
    def add_steps_table(self, steps_data):
        """Aggiunge la tabella con gli step di validazione"""
        # Font da usare
        base_font = 'DejaVu' if USE_DEJAVU else 'Helvetica'
        bold_font = 'DejaVu-Bold' if USE_DEJAVU else 'Helvetica-Bold'
        
        # Stile per testo con wrap
        text_style = ParagraphStyle(
            'CellText',
            parent=self.styles['Normal'],
            fontName=base_font,
            fontSize=8,  # Aumentato da 7 a 8
            leading=10,
            wordWrap='CJK'
        )
        
        # Header della tabella step  
        table_data = [
            [
                Paragraph('<b>Step</b>', text_style),
                Paragraph('<b>Descriere verificare/instrucțiune de lucru</b>', text_style),
                Paragraph('<b>Verificarea conform</b>', text_style),
                Paragraph('<b>OK</b>', text_style),
                Paragraph('<b>Not OK</b>', text_style)
            ],
        ]
        
        # Aggiungi ogni step
        for step in steps_data:
            step_name = step.get('Step', '')
            description = step.get('Description', '')
            equipment = step.get('Equipment', '')
            is_ok = step.get('IsOk')
            
            # Usa caratteri Unicode affidabili
            ok_mark = '✓' if is_ok == 1 or is_ok == True else '☐'
            not_ok_mark = '✓' if is_ok == 0 or is_ok == False else '☐'
            
            # Usa Paragraph per word wrap automatico
            table_data.append([
                Paragraph(step_name, text_style),
                Paragraph(description, text_style),
                Paragraph(equipment, text_style),
                Paragraph(f'<para align="center">{ok_mark}</para>', text_style),
                Paragraph(f'<para align="center">{not_ok_mark}</para>', text_style)
            ])
            
            # Se NOT OK, aggiungi i 3 campi problema
            if (is_ok == 0 or is_ok == False) and (step.get('Problem') or step.get('RootCause') or step.get('CorrectiveAction')):
                problem_desc = step.get('Problem', '')
                root_cause = step.get('RootCause', '')
                corrective = step.get('CorrectiveAction', '')
                
                if problem_desc:
                    table_data.append([
                        Paragraph('', text_style),
                        Paragraph(f'<b>Problemă:</b> {problem_desc}', text_style),
                        Paragraph('', text_style),
                        Paragraph('', text_style),
                        Paragraph('', text_style)
                    ])
                if root_cause:
                    table_data.append([
                        Paragraph('', text_style),
                        Paragraph(f'<b>Cauză:</b> {root_cause}', text_style),
                        Paragraph('', text_style),
                        Paragraph('', text_style),
                        Paragraph('', text_style)
                    ])
                if corrective:
                    table_data.append([
                        Paragraph('', text_style),
                        Paragraph(f'<b>Acțiuni corective:</b> {corrective}', text_style),
                        Paragraph('', text_style),
                        Paragraph('', text_style),
                        Paragraph('', text_style)
                    ])
            
            # 🆕 Aggiungi riga note/codice stencil se esistono
            notes = step.get('Notes', '')
            if notes:
                table_data.append([
                    Paragraph('', text_style),
                    Paragraph(f'<b>Note/Codice Stencil:</b> {notes}', text_style),
                    Paragraph('', text_style),
                    Paragraph('', text_style),
                    Paragraph('', text_style)
                ])
        
        steps_table = Table(table_data, colWidths=[25*mm, 68*mm, 34*mm, 16*mm, 17*mm])
        steps_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), base_font),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CCCCCC')),
            ('ALIGN', (3, 0), (4, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 1),
            ('RIGHTPADDING', (0, 0), (-1, -1), 1),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        
        self.elements.append(steps_table)
    
    def add_footer(self, operator_name):
        """Aggiunge il footer con firma e data"""
        
        # Font da usare
        base_font = 'DejaVu' if USE_DEJAVU else 'Helvetica'
        bold_font = 'DejaVu-Bold' if USE_DEJAVU else 'Helvetica-Bold'
        
        footer_data = [
            ['Decizia finală', '', 'Acceptat condițional ☐'],
            [f'Data / ora: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 
             f'Operator: {operator_name}', 
             'Pag. 1 din 1']
        ]
        
        footer_table = Table(footer_data, colWidths=[60*mm, 70*mm, 60*mm])
        footer_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), base_font),  # ✅ DejaVu
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (0, 0), bold_font),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        self.elements.append(Spacer(1, 5*mm))
        self.elements.append(footer_table)
        
        # Nota proprietà intellettuale con DejaVu
        proprieta_style = ParagraphStyle(
            'Proprieta',
            parent=self.styles['Normal'],
            fontName=base_font,  # ✅ DejaVu
            fontSize=6,
            alignment=TA_CENTER
        )
        
        proprieta = Paragraph(
            'Proprietatea intelectuală a acestui document aparține EUTRON ELECTRONIC SERVICES S.r.l., '
            'toate drepturile rezervate.',
            proprieta_style
        )
        self.elements.append(Spacer(1, 3*mm))
        self.elements.append(proprieta)
    
    def generate(self, template_data, validation_data, steps_data, operator_name, declaration_labels=None,
                product_code='', order_number='', quantity=''):
        """Genera il PDF completo"""
        try:
            self.add_header(template_data, validation_data)
            self.add_validation_types(validation_data, declaration_labels, product_code, order_number, quantity)
            self.add_steps_table(steps_data)
            self.add_footer(operator_name)
            
            # Build PDF
            self.doc.build(self.elements)
            logger.info(f"Report FAI generato: {self.output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Errore generazione report FAI: {e}", exc_info=True)
            return False


def generate_fai_report(fai_log_id, db, output_path):
    """
    Funzione helper per generare un report FAI dal database
    
    Args:
        fai_log_id: ID del log FAI da stampare
        db: Connessione database
        output_path: Percorso file PDF output
    """
    def _load_validation_labels_for_template(template_id):
        labels = dict(DEFAULT_DECLARATION_LABELS)
        if not template_id:
            return labels

        try:
            labels_query = """
            SELECT FaiTemplateId, DeclarationKey, DeclarationLabel
            FROM [Traceability_RS].[fai].[FaiTemplateDeclarations]
            WHERE DateOut IS NULL
              AND (FaiTemplateId = ? OR FaiTemplateId IS NULL)
            ORDER BY CASE WHEN FaiTemplateId = ? THEN 0 ELSE 1 END, DisplayOrder, FaiTemplateDeclarationId
            """
            db.cursor.execute(labels_query, (template_id, template_id))
            rows = db.cursor.fetchall()
            loaded_keys = set()

            for row in rows:
                key = (row.DeclarationKey or '').strip()
                value = (row.DeclarationLabel or '').strip()
                if key in labels and value and key not in loaded_keys:
                    labels[key] = value
                    loaded_keys.add(key)
        except Exception as e:
            logger.warning(f"Impossibile leggere fai.FaiTemplateDeclarations per template {template_id}: {e}")

        return labels

    try:
        # Recupera dati template
        template_query = """
        SELECT t.FaiTemplateId, t.NrDocument, t.Revision, t.RevisionDate, t.FaiTitle
        FROM Traceability_RS.fai.FaiLogHeathers h
        INNER JOIN Traceability_RS.fai.FaiLogs l ON h.FaiLogId = l.FaiLogId
        INNER JOIN Traceability_RS.fai.FaiStepDetails d ON l.FaiStepDetailId = d.FaiStepDetailId
        INNER JOIN Traceability_RS.fai.FaiSteps s ON d.FatStepId = s.FatStepId
        INNER JOIN Traceability_RS.fai.FaiTemplates t ON s.FaiTemplateId = t.FaiTemplateId
        WHERE h.FaiLogId = ?
        """
        
        db.cursor.execute(template_query, (fai_log_id,))
        template_row = db.cursor.fetchone()
        
        if not template_row:
            logger.error(f"Template non trovato per FaiLogId {fai_log_id}")
            return False
        
        template_data = {
            'NrDocument': template_row.NrDocument,
            'Revision': template_row.Revision,
            'RevisionDate': template_row.RevisionDate.strftime('%d/%m/%Y') if template_row.RevisionDate else '',
            'FaiTitle': template_row.FaiTitle
        }
        declaration_labels = _load_validation_labels_for_template(template_row.FaiTemplateId)
        
        # Recupera dati ordine (OrderNumber, ProductCode, Quantity)
        order_query = """
        SELECT o.OrderNumber, o.orderquantity, p.productcode
        FROM Traceability_RS.fai.FaiLogHeathers h
        INNER JOIN Traceability_RS.fai.FaiLogs l ON h.FaiLogId = l.FaiLogId
        INNER JOIN Traceability_RS.dbo.orders o ON l.OrderId = o.IDOrder
        INNER JOIN Traceability_RS.dbo.products p ON o.IDProduct = p.IDProduct
        WHERE h.FaiLogId = ?
        """
        
        db.cursor.execute(order_query, (fai_log_id,))
        order_row = db.cursor.fetchone()
        
        order_number = order_row.OrderNumber if order_row else ''
        product_code = order_row.ProductCode if order_row else ''
        quantity = order_row.orderquantity if order_row else ''
        
        # Recupera dati validazione
        validation_query = """
        SELECT NPI, Test, PRODUCTION, StandardProcessDeviation, Others
        FROM Traceability_RS.fai.FaiLogHeathers
        WHERE FaiLogId = ?
        """
        
        db.cursor.execute(validation_query, (fai_log_id,))
        validation_row = db.cursor.fetchone()
        
        validation_data = {
            'NPI': validation_row.NPI if validation_row else 0,
            'Test': validation_row.Test if validation_row else 0,
            'PRODUCTION': validation_row.PRODUCTION if validation_row else 0,
            'StandardProcessDeviation': validation_row.StandardProcessDeviation if validation_row else 0,
            'Others': validation_row.Others if validation_row else 0
        }
        
        # Recupera step - TUTTI quelli della stessa validazione (OrderId + DateIn) ma NON annullati
        steps_query = """
        SELECT 
            s.StepName,
            d.StepDetail,
            ISNULL(e.Description, '') + ' ' + ISNULL(e.SerialNumber, '') as Equipment,
            l.IsOk,
            l.ProblemDescription,
            l.RoutCauseProblem,
            l.CorrectiveAction,
            l.Operator,
            l.Dati
        FROM Traceability_RS.fai.FaiLogs l
        INNER JOIN Traceability_RS.fai.FaiStepDetails d ON l.FaiStepDetailId = d.FaiStepDetailId
        INNER JOIN Traceability_RS.fai.FaiSteps s ON d.FatStepId = s.FatStepId
        LEFT JOIN Traceability_RS.fai.FaiEquipments e ON d.FaiEquipmentId = e.FaiEquipmentid
        WHERE l.OrderId = (SELECT TOP 1 l2.OrderId FROM Traceability_RS.fai.FaiLogs l2 WHERE l2.FaiLogId = ?)
          AND CAST(l.DateIn AS DATE) = CAST((SELECT TOP 1 l2.DateIn FROM Traceability_RS.fai.FaiLogs l2 WHERE l2.FaiLogId = ?) AS DATE)
          AND l.DateOut IS NULL
        ORDER BY s.OrderinList, d.OrdineList
        """
        
        db.cursor.execute(steps_query, (fai_log_id, fai_log_id))
        steps_rows = db.cursor.fetchall()
        
        logger.info(f"Recuperati {len(steps_rows)} step per report FAI")
        
        steps_data = []
        operator_name = ''
        
        for row in steps_rows:
            steps_data.append({
                'Step': row.StepName,
                'Description': row.StepDetail,
                'Equipment': row.Equipment,
                'IsOk': row.IsOk,
                'Problem': row.ProblemDescription if row.ProblemDescription else '',
                'RootCause': row.RoutCauseProblem if hasattr(row, 'RoutCauseProblem') and row.RoutCauseProblem else '',
                'CorrectiveAction': row.CorrectiveAction if hasattr(row, 'CorrectiveAction') and row.CorrectiveAction else '',
                'Notes': row.Dati if hasattr(row, 'Dati') and row.Dati else ''  # 🆕 Note/Codice Stencil
            })
            if row.Operator:
                operator_name = row.Operator
        
        # Genera PDF
        generator = FAIReportGenerator(output_path)
        return generator.generate(template_data, validation_data, steps_data, operator_name, declaration_labels,
                                 product_code, order_number, quantity)
        
    except Exception as e:
        logger.error(f"Errore generazione report FAI: {e}", exc_info=True)
        return False

