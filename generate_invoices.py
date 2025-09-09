from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os

os.makedirs("invoices", exist_ok=True)

def create_invoice(filename, vendor, invoice_number, invoice_date, due_date, total):
    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, height - 80, "INVOICE")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 150, f"From: {vendor}")
    c.drawString(50, height - 180, f"Invoice Number: {invoice_number}")
    c.drawString(50, height - 200, f"Invoice Date: {invoice_date}")
    c.drawString(50, height - 220, f"Due Date: {due_date}")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 260, f"Total Amount Due: ${total:,.2f}")
    c.showPage()
    c.save()

create_invoice(
    "invoices/amazon_inv_0012.pdf",
    vendor="Amazon",
    invoice_number="INV-0012",
    invoice_date="2025-08-20",
    due_date="2025-09-05",
    total=2450.00
)

create_invoice(
    "invoices/microsoft_inv_0043.pdf",
    vendor="Microsoft",
    invoice_number="INV-0043",
    invoice_date="2025-08-25",
    due_date="2025-09-10",
    total=3100.00
)

create_invoice(
    "invoices/google_inv_0076.pdf",
    vendor="Google Cloud",
    invoice_number="INV-0076",
    invoice_date="2025-08-28",
    due_date="2025-09-14",
    total=1200.00
)

print("Sample invoices created in ./invoices/")
