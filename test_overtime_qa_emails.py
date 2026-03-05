"""
Test script per inviare email di test per il modulo Overtime Q&A.
Invia a gianluca.testa@vandewiele.com:
  1. Email domanda (question)
  2. Email risposta (answer)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import send_email

TARGET = "gianluca.testa@vandewiele.com"

# ── EMAIL 1: Question ─────────────────────────────────────
print("Invio email 1: Question...")
question_body = """
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: #2E5090;">Overtime Request - Question</h2>
    <p>Dear Gianluca Testa,</p>
    <p>A question has been raised regarding your overtime request before a decision can be made.</p>
    <table style="border-collapse: collapse; margin: 20px 0;">
        <tr>
            <td style="padding: 8px; font-weight: bold; width: 180px;">Request Number:</td>
            <td style="padding: 8px;">OT-2026/TEST-001</td>
        </tr>
        <tr>
            <td style="padding: 8px; font-weight: bold;">Asked by:</td>
            <td style="padding: 8px;">Test Approver</td>
        </tr>
    </table>
    <div style="background-color: #E8F4FD; border-left: 4px solid #2E5090; padding: 14px; margin: 20px 0;">
        <strong>Question:</strong><br>
        <p style="white-space: pre-wrap;">This is a test question about the overtime request.
Could you please clarify the reason for requesting 4 extra hours on Saturday?
Is this related to the urgent production order PO-12345?</p>
    </div>
    <p style="background-color: #FFF3CD; border-left: 4px solid #FFC107; padding: 12px; margin: 20px 0;">
        <strong>&#9888; Action Required:</strong> Please reply to this question via:<br>
        <strong>ERP &rarr; Operations &rarr; Personnel &rarr; Overtime &rarr; Responses</strong>
    </p>
    <p style="margin-top: 30px;">
        Best regards,<br>
        <strong>TraceabilityRS System</strong>
    </p>
</body>
</html>
"""

send_email(
    recipients=[TARGET],
    subject="Question about Overtime Request OT-2026/TEST-001",
    body=question_body,
    is_html=True
)
print("Email 1 (Question) inviata!")

# ── EMAIL 2: Answer ───────────────────────────────────────
print("Invio email 2: Answer...")
answer_body = """
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: #28A745;">Overtime Request - Answer Received</h2>
    <p>Dear Test Approver,</p>
    <p>Your question regarding overtime request <strong>OT-2026/TEST-001</strong> has been answered.</p>
    <div style="background-color: #F0F0F0; border-left: 4px solid #6C757D; padding: 14px; margin: 20px 0;">
        <strong>Your Question:</strong><br>
        <p style="white-space: pre-wrap;">This is a test question about the overtime request.
Could you please clarify the reason for requesting 4 extra hours on Saturday?
Is this related to the urgent production order PO-12345?</p>
    </div>
    <div style="background-color: #D4EDDA; border-left: 4px solid #28A745; padding: 14px; margin: 20px 0;">
        <strong>Answer from Gianluca Testa:</strong><br>
        <p style="white-space: pre-wrap;">Yes, the 4 extra hours on Saturday are needed to complete the urgent production order PO-12345.
The customer deadline is Monday morning and we need to finish the last batch.
The supervisor on site will be Mr. Popescu.</p>
    </div>
    <p style="background-color: #FFF3CD; border-left: 4px solid #FFC107; padding: 12px; margin: 20px 0;">
        <strong>&#9888; Next Steps:</strong> You can now proceed to approve or reject this request, or ask another question via:<br>
        <strong>ERP &rarr; Operations &rarr; Personnel &rarr; Overtime &rarr; Authorization</strong>
    </p>
    <p style="margin-top: 30px;">
        Best regards,<br>
        <strong>TraceabilityRS System</strong>
    </p>
</body>
</html>
"""

send_email(
    recipients=[TARGET],
    subject="Answer to Overtime Question - Request OT-2026/TEST-001",
    body=answer_body,
    is_html=True
)
print("Email 2 (Answer) inviata!")

print("\n=== Test completato! Controllare la casella email. ===")
