import pdfplumber
import re
from datetime import datetime
import json

def parse_invoice(pdf_path):
    """
    Extracts text from a PDF invoice and find key fields using regex.
    This parser is tailored for the simple, clean format of your sample invoices.
    """
    extracted_data = {
        "vendor": None,
        "invoice_number": None,
        "invoice_date": None,
        "due_date": None,
        "total": None
    }
    
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    vendor_match = re.search(r'From:\s*([^\n]+)', text)
    if vendor_match:
        extracted_data['vendor'] = vendor_match.group(1).strip()

    inv_num_match = re.search(r'Invoice\s*Number\s*[:\#]?\s*([A-Z0-9-]+)', text, re.IGNORECASE)
    if inv_num_match:
        extracted_data['invoice_number'] = inv_num_match.group(1)

    inv_date_match = re.search(r'Invoice\s*Date\s*[:\#]?\s*([0-9]{4}-[0-9]{2}-[0-9]{2})', text)
    if inv_date_match:
        extracted_data['invoice_date'] = inv_date_match.group(1)
    elif not extracted_data['invoice_date']:
        inv_date_match_alt = re.search(r'Invoice\s*Date\s*[:\#]?\s*([0-9/]+)', text)
        if inv_date_match_alt:
            extracted_data['invoice_date'] = inv_date_match_alt.group(1)

    due_date_match = re.search(r'Due\s*Date\s*[:\#]?\s*([0-9]{4}-[0-9]{2}-[0-9]{2})', text)
    if due_date_match:
        extracted_data['due_date'] = due_date_match.group(1)
    elif not extracted_data['due_date']:
        due_date_match_alt = re.search(r'Due\s*Date\s*[:\#]?\s*([0-9/]+)', text)
        if due_date_match_alt:
            extracted_data['due_date'] = due_date_match_alt.group(1)

    total_match = re.search(r'\$?\s*([0-9,]+\.\d{2})', text)
    if total_match:
        total_str = total_match.group(1).replace(',', '')
        extracted_data['total'] = float(total_str)
    
    return extracted_data

def main():
    """
    Main function to parse all sample invoices and save the data to a JSON file.
    This is the final goal of this script.
    """
    invoice_files = [
        "invoices/amazon_inv_0012.pdf",
        "invoices/microsoft_inv_0043.pdf",
        "invoices/google_inv_0076.pdf" 
    ]
    
    all_invoices_data = []
    
    for file_path in invoice_files:
        print(f"Parsing: {file_path}")
        try:
            invoice_data = parse_invoice(file_path)
            all_invoices_data.append(invoice_data)
            print(f"Success: {invoice_data}\n")
        except Exception as e:
            print(f"Error parsing {file_path}: {e}\n")
    
    with open('invoices.json', 'w') as json_file:
        json.dump(all_invoices_data, json_file, indent=4)
    
    print("All invoices parsed successfully! Data saved to 'invoices.json'.")
    print("\nFinal extracted data:")
    print(json.dumps(all_invoices_data, indent=4))

if __name__ == '__main__':
    main()