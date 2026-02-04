"""
Test Script Semplificato per Sistema Notifiche NPI
Invia tutte le email solo a gianluca.testa@vandewiele.com
"""

import sys
import os
from pathlib import Path

# Aggiungi directory root al path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from email_connector import EmailSender
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurazione database
DB_CONN_STR = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=192.168.10.110;"
    "DATABASE=Traceability_RS;"
    "Trusted_Connection=yes;"
)

def test_notification_simple():
    """Test semplificato del sistema di notifiche"""
    
    print("=" * 80)
    print("🧪 TEST SEMPLIFICATO SISTEMA NOTIFICHE NPI")
    print("=" * 80)
    print()
    
    # 1. Setup database connection
    print("📊 1. Connessione al database...")
    try:
        engine = create_engine(DB_CONN_STR, echo=False)
        session = Session(engine)
        print("   ✅ Connessione stabilita")
    except Exception as e:
        print(f"   ❌ Errore connessione: {e}")
        return
    
    # 2. Verifica task in ritardo
    print("\n🔍 2. Verifica task in ritardo...")
    try:
        query = text("""
            SELECT TOP 5
                tp.TaskId,
                tp.OwnerID,
                e.EmployeeName + ' ' + e.EmployeeSurname AS FullName,
                a.WorkEmail AS Email,
                DATEDIFF(DAY, tp.DataFine, GETDATE()) AS GiorniRitardo
            FROM Traceability_rs.dbo.TaskProdotto tp
            LEFT JOIN Employee.dbo.EmployeeHireHistory s ON tp.OwnerID = s.EmployeeHireHistoryId
            LEFT JOIN Employee.dbo.Employees e ON e.EmployeeId = s.EmployeeId
            LEFT JOIN Employee.dbo.EmployeeAddress a ON a.EmployeeId = e.EmployeeId
            WHERE tp.DataFine < GETDATE()
              AND tp.Stato NOT IN ('Completato', 'Cancellato')
              AND tp.PercentualeCompletamento < 100
              AND tp.OwnerID IS NOT NULL
              AND a.WorkEmail IS NOT NULL
        """)
        
        results = session.execute(query).fetchall()
        
        if not results:
            print("   ℹ️  Nessun task in ritardo trovato")
            session.close()
            return
        
        print(f"   ✅ Trovati {len(results)} task in ritardo")
        print()
        print("   Task in ritardo:")
        for row in results:
            task_id, owner_id, full_name, email, giorni = row
            print(f"   - Task {task_id}: {full_name} - {giorni} giorni")
        
    except Exception as e:
        print(f"   ❌ Errore query: {e}")
        session.close()
        return
    
    # 3. Setup email sender
    print("\n📧 3. Configurazione EmailSender...")
    try:
        email_sender = EmailSender()
        from_email = email_sender.load_credentials()
        print(f"   ✅ Email mittente: {from_email}")
    except Exception as e:
        print(f"   ⚠️  Credenziali non configurate: {e}")
        print("   Configurazione credenziali...")
        try:
            email_sender.save_credentials("noreply@vandewiele.com", "")
            print("   ✅ Credenziali salvate")
        except Exception as e2:
            print(f"   ❌ Errore salvataggio credenziali: {e2}")
            session.close()
            return
    
    # 4. Test invio email semplice
    print("\n✉️  4. Test invio email...")
    print("   Destinatario: gianluca.testa@vandewiele.com")
    print("   CC: gianluca.testa@vandewiele.com")
    
    try:
        # Verifica logo
        logo_path = Path(__file__).parent / "Logo.png"
        if not logo_path.exists():
            print(f"   ⚠️  Logo non trovato: {logo_path}")
            logo_exists = False
        else:
            print(f"   ✅ Logo trovato: {logo_path}")
            logo_exists = True
        
        # Crea email di test
        subject = "🧪 TEST - Notifica Task in Ritardo NPI"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            {'<div style="text-align: center; margin-bottom: 20px;"><img src="cid:logo" alt="Company Logo" style="max-width: 200px; height: auto;"></div>' if logo_exists else ''}
            
            <div style="background-color: #fff3cd; padding: 15px; border-left: 5px solid #ffc107; margin-bottom: 20px;">
                <h2 style="color: #856404; margin: 0;">🧪 TEST - Task in Ritardo</h2>
            </div>

            <p>Questo è un <strong>test</strong> del sistema di notifiche NPI.</p>
            
            <p>Trovati <strong>{len(results)}</strong> task in ritardo:</p>
            
            <ul>
                {''.join([f'<li>Task {row[0]}: {row[2]} - {row[4]} giorni</li>' for row in results[:3]])}
            </ul>

            <hr style="margin-top: 40px;">
            <p style="font-size: 0.9em; color: #666;">
                Test automatico - Sistema NPI<br>
                {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M')}
            </p>
        </body>
        </html>
        """
        
        # Prepara allegati
        attachments = []
        if logo_exists:
            attachments.append(('inline', str(logo_path), 'logo'))
        
        # Invia email
        print("   📤 Invio email in corso...")
        success = email_sender.send_email(
            to_email="gianluca.testa@vandewiele.com",
            subject=subject,
            body=body,
            is_html=True,
            cc_emails=["gianluca.testa@vandewiele.com"],
            attachments=attachments if attachments else None
        )
        
        if success:
            print("   ✅ Email inviata con successo!")
            print()
            print("   📬 Controlla la casella: gianluca.testa@vandewiele.com")
            print("   Dovresti ricevere:")
            if logo_exists:
                print("   - ✅ Logo aziendale in alto")
            print("   - ✅ Lista task in ritardo")
            print("   - ✅ CC a gianluca.testa@vandewiele.com")
        else:
            print("   ❌ Invio email fallito")
        
    except Exception as e:
        print(f"   ❌ Errore invio email: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()
        print("\n🔒 Sessione database chiusa")
    
    print("\n" + "=" * 80)
    print("🏁 TEST COMPLETATO")
    print("=" * 80)

if __name__ == "__main__":
    test_notification_simple()
