"""
Funzione standalone per generare il report PDF degli ospiti.
Può essere chiamata direttamente dal menu di main.py.
"""

import logging
from datetime import datetime
import os

logger = logging.getLogger("TraceabilityRS")


def generate_guests_pdf_report(db_handler):
    """
    Genera un report PDF dei visitatori presenti in fabbrica oggi.
    Salva il PDF in C:\\Temp, lo apre automaticamente e aggiorna il campo PrintedOn.
    
    Args:
        db_handler: Istanza del gestore database
        
    Returns:
        tuple: (success: bool, message: str, pdf_path: str or None)
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        # Registra font Unicode per supportare caratteri rumeni (ă, â, î, ș, ț)
        try:
            # Prova a usare DejaVuSans (disponibile su Windows)
            pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
            font_name = 'DejaVuSans'
            font_name_bold = 'DejaVuSans-Bold'
            logger.info("Font DejaVuSans registrato con successo")
        except:
            try:
                # Fallback: prova Arial Unicode MS
                pdfmetrics.registerFont(TTFont('ArialUnicode', 'ARIALUNI.TTF'))
                font_name = 'ArialUnicode'
                font_name_bold = 'ArialUnicode'
                logger.info("Font Arial Unicode registrato con successo")
            except:
                # Ultimo fallback: usa font standard (potrebbero non mostrare tutti i caratteri)
                font_name = 'Helvetica'
                font_name_bold = 'Helvetica-Bold'
                logger.warning("Impossibile registrare font Unicode, alcuni caratteri rumeni potrebbero non essere visualizzati correttamente")
        
        # Ottieni la data corrente
        today = datetime.now()
        today_date = today.date()
        
        # Verifica e ripristina la connessione se necessario
        try:
            if not db_handler.conn or db_handler.conn.closed:
                logger.warning("Connessione database chiusa, tentativo di riconnessione...")
                db_handler.connect()
        except Exception as e:
            logger.error(f"Errore verifica connessione: {e}")
            return (False, f"Errore connessione database: {str(e)}", None)
        
        # Query per ottenere i visitatori presenti oggi
        query = """
            SELECT 
                VisitorId,
                GuestName,
                CompanyName,
                ShowFrom as StartVisit,
                ShowUntil as EndVisit,
                SponsorGuy
            FROM [Employee].[dbo].[Visitors]
            WHERE CAST(ShowFrom AS DATETIME) <= ?
              AND CAST(ShowUntil AS DATETIME) >= ?
            ORDER BY GuestName
        """
        
        # logger.info(f"=== DEBUG QUERY VISITATORI ===")
        # logger.info(f"Data oggi (datetime): {today}")
        # logger.info(f"Data oggi (date): {today_date}")
        # logger.info(f"Parametri query: today={today}, today={today}")
        
        try:
            # Crea un nuovo cursore per questa operazione
            cursor = db_handler.conn.cursor()
            
            # Esegui la query con logging
            logger.info(f"Esecuzione query con parametri: ({today}, {today})")
            cursor.execute(query, (today, today))
            visitors = cursor.fetchall()
            
            logger.info(f"Query eseguita. Numero visitatori trovati: {len(visitors) if visitors else 0}")
            
            # Log dettagliato dei visitatori trovati
            if visitors:
                for i, v in enumerate(visitors):
                    logger.info(f"Visitatore {i+1}: ID={v.VisitorId}, Nome={v.GuestName}, Azienda={v.CompanyName}, Start={v.StartVisit}, End={v.EndVisit}")
            else:
                logger.warning("Nessun visitatore trovato dalla query!")
                
                # Esegui query di debug per vedere tutti i visitatori
                debug_query = "SELECT COUNT(*) as Total FROM [Employee].[dbo].[Visitors]"
                cursor.execute(debug_query)
                total = cursor.fetchone()
                logger.info(f"Totale visitatori nella tabella: {total[0] if total else 0}")
            
            cursor.close()
        except Exception as e:
            logger.error(f"Errore esecuzione query visitatori: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return (False, f"Errore recupero visitatori: {str(e)}", None)
        
        if not visitors:
            logger.info("Nessun visitatore trovato per oggi")
            return (False, "Nessun visitatore presente oggi da stampare", None)
        
        # Crea directory C:\\Temp se non esiste
        temp_dir = r'C:\Temp'
        os.makedirs(temp_dir, exist_ok=True)
        
        # Crea nome file con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f'Visitors_Report_{timestamp}.pdf'
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        # Crea PDF
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        
        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
        if os.path.exists(logo_path):
            img = ImageReader(logo_path)
            c.drawImage(img, 2*cm, height - 4*cm, width=4*cm, height=2*cm, preserveAspectRatio=True)
        
        # Titolo
        c.setFont(font_name_bold, 16)
        c.drawCentredString(width/2, height - 5*cm, "LISTĂ VIZITATORI PREZENȚI")
        
        # Data
        c.setFont(font_name, 12)
        data_ro = today.strftime("%d.%m.%Y")
        c.drawCentredString(width/2, height - 6*cm, f"Data: {data_ro}")
        
        # Tabella visitatori
        y = height - 8*cm
        c.setFont(font_name_bold, 10)
        c.drawString(2*cm, y, "Nume Vizitator")
        c.drawString(8*cm, y, "Companie")
        c.drawString(13*cm, y, "Ora Sosire")
        c.drawString(16*cm, y, "Ora Plecare")
        
        # Linea separatrice
        y -= 0.3*cm
        c.line(2*cm, y, width - 2*cm, y)
        y -= 0.5*cm
        
        # Dati visitatori
        c.setFont(font_name, 9)
        visitor_ids = []  # Lista per tracciare gli ID dei visitatori stampati
        
        for visitor in visitors:
            if y < 4*cm:  # Nuova pagina se necessario
                c.showPage()
                y = height - 3*cm
                c.setFont(font_name, 9)
            
            visitor_ids.append(visitor.VisitorId)
            guest_name = visitor.GuestName or ''
            company = visitor.CompanyName or ''
            start_time = visitor.StartVisit.strftime("%H:%M") if visitor.StartVisit else ''
            end_time = visitor.EndVisit.strftime("%H:%M") if visitor.EndVisit else 'În curs'
            
            c.drawString(2*cm, y, guest_name[:35])
            c.drawString(8*cm, y, company[:25])
            c.drawString(13*cm, y, start_time)
            c.drawString(16*cm, y, end_time)
            
            y -= 0.6*cm
        
        # Nota legale in rumeno
        y -= 1*cm
        if y < 6*cm:
            c.showPage()
            y = height - 3*cm
        
        c.setFont(font_name_bold, 10)
        c.drawString(2*cm, y, f"Listă persoane prezente în Vandewiele Romania pentru ziua {data_ro}")
        y -= 0.8*cm
        
        c.setFont(font_name, 9)
        text_lines = [
            "Prezenta listă trebuie păstrată de departamentul de personal și predată",
            "responsabililor în caz de evenimente catastrofale (cum ar fi incendii,",
            "cutremure sau alte tipuri de calamități)."
        ]
        
        for line in text_lines:
            c.drawString(2*cm, y, line)
            y -= 0.5*cm
        
        # Footer
        c.setFont(font_name, 8)  # Usa font_name invece di Helvetica-Oblique
        c.drawCentredString(width/2, 1.5*cm, "Document generat automat - Vandewiele Romania")
        
        c.save()
        
        # Aggiorna PrintedOn per tutti i visitatori stampati
        if visitor_ids:
            try:
                placeholders = ','.join(['?' for _ in visitor_ids])
                update_query = f"""
                    UPDATE [Employee].[dbo].[Visitors]
                    SET PrintedOn = GETDATE()
                    WHERE VisitorId IN ({placeholders})
                """
                cursor = db_handler.conn.cursor()
                cursor.execute(update_query, visitor_ids)
                db_handler.conn.commit()
                cursor.close()
                logger.info(f"PrintedOn aggiornato per {len(visitor_ids)} visitatori")
            except Exception as e:
                logger.error(f"Errore aggiornamento PrintedOn: {e}")
        
        # Apri il PDF
        if os.name == 'nt':  # Windows
            os.startfile(pdf_path)
        else:  # Linux/Mac
            import subprocess
            subprocess.run(['xdg-open', pdf_path])
        
        logger.info(f"Report PDF generato: {pdf_path} ({len(visitors)} visitatori)")
        
        return (True, f"Report PDF generato con successo:\n{pdf_path}\n\nVisitatori: {len(visitors)}", pdf_path)
        
    except ImportError as e:
        error_msg = "Libreria reportlab non installata.\nEseguire: pip install reportlab"
        logger.error(f"ImportError: {e}")
        return (False, error_msg, None)
    except Exception as e:
        error_msg = f"Errore durante la generazione del report: {str(e)}"
        logger.error(f"Errore generazione report PDF: {e}")
        import traceback
        traceback.print_exc()
        return (False, error_msg, None)
