"""
Test Minimo - Solo Invio Email
Testa solo l'invio email senza connessione database
"""

import sys
from pathlib import Path

# Aggiungi directory root al path
sys.path.insert(0, str(Path(__file__).parent))

from email_connector import EmailSender

def test_email_only():
    """Test solo invio email"""
    
    print("=" * 80)
    print("🧪 TEST MINIMO - INVIO EMAIL")
    print("=" * 80)
    print()
    
    # 1. Setup email sender
    print("📧 1. Configurazione EmailSender...")
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
            return
    
    # 2. Verifica logo
    print("\n🖼️  2. Verifica logo...")
    logo_path = Path(__file__).parent / "Logo.png"
    if not logo_path.exists():
        print(f"   ⚠️  Logo non trovato: {logo_path}")
        logo_exists = False
    else:
        print(f"   ✅ Logo trovato: {logo_path}")
        logo_exists = True
    
    # 3. Test invio email
    print("\n✉️  3. Test invio email...")
    print("   Destinatario: gianluca.testa@vandewiele.com")
    print("   CC: gianluca.testa@vandewiele.com")
    
    try:
        # Crea email di test
        subject = "🧪 TEST - Sistema Notifiche NPI"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            {'<div style="text-align: center; margin-bottom: 20px;"><img src="cid:logo" alt="Company Logo" style="max-width: 200px; height: auto;"></div>' if logo_exists else ''}
            
            <div style="background-color: #fff3cd; padding: 15px; border-left: 5px solid #ffc107; margin-bottom: 20px;">
                <h2 style="color: #856404; margin: 0;">🧪 TEST - Sistema Notifiche NPI</h2>
            </div>

            <p>Gentile Utente,</p>
            
            <p>Questo è un <strong>test</strong> del sistema di notifiche NPI.</p>
            
            <h3>Funzionalità Testate:</h3>
            <ul>
                <li>✅ Invio email HTML</li>
                <li>{'✅' if logo_exists else '⚠️'} Logo aziendale embedded</li>
                <li>✅ CC recipients</li>
                <li>✅ Formattazione professionale</li>
            </ul>
            
            <div style="background-color: #d1ecf1; padding: 15px; border-left: 5px solid #0c5460; margin: 20px 0;">
                <p style="margin: 0;"><strong>📋 Prossimi Passi:</strong></p>
                <ul style="margin: 10px 0;">
                    <li>Verificare ricezione email</li>
                    <li>Controllare visualizzazione logo</li>
                    <li>Confermare CC funzionante</li>
                </ul>
            </div>

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
            print("\n" + "=" * 80)
            print("✅ EMAIL INVIATA CON SUCCESSO!")
            print("=" * 80)
            print()
            print("📬 Controlla la casella: gianluca.testa@vandewiele.com")
            print()
            print("Dovresti ricevere:")
            if logo_exists:
                print("  ✅ Logo aziendale in alto")
            print("  ✅ Email HTML formattata")
            print("  ✅ CC a gianluca.testa@vandewiele.com")
            print()
        else:
            print("\n❌ INVIO EMAIL FALLITO")
        
    except Exception as e:
        print(f"\n❌ Errore invio email: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("🏁 TEST COMPLETATO")
    print("=" * 80)

if __name__ == "__main__":
    test_email_only()
