import os
import json
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_invoices_data(json_file_path='invoices.json'):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        print(f"Successfully loaded {len(data)} invoices.")
        return data
    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found. Please run invoice_parser.py first.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {json_file_path}.")
        return []

invoice_data = load_invoices_data()

def get_invoices_due_in_x_days(days=7):
    today = datetime.now().date()
    future_date = today + timedelta(days=days)
    due_soon = []

    for invoice in invoice_data:
        try:
            due_date = datetime.strptime(invoice['due_date'], '%Y-%m-%d').date()
        except ValueError:
            print(f"Warning: Could not parse date {invoice['due_date']} for invoice {invoice['invoice_number']}")
            continue

        if today <= due_date <= future_date:
            due_soon.append(invoice)

    return due_soon

def get_total_for_vendor(vendor_name):
    total = 0.0
    vendor_name_lower = vendor_name.lower()

    for invoice in invoice_data:
        if invoice['vendor'].lower() == vendor_name_lower:
            total += invoice['total']
    return total

def get_vendors_above_amount(threshold=2000):
    vendors_above = []
    vendor_totals = {}

    for invoice in invoice_data:
        vendor = invoice['vendor']
        total = invoice['total']

        if vendor not in vendor_totals:
            vendor_totals[vendor] = 0
        vendor_totals[vendor] += total

    for vendor, total in vendor_totals.items():
        if total > threshold:
            vendors_above.append({"vendor": vendor, "total": total})

    return vendors_above

def format_due_invoices(invoices_list):
    if not invoices_list:
        return "0 invoices are due in the specified period."

    formatted_list = []
    for inv in invoices_list:
        due_date_obj = datetime.strptime(inv['due_date'], '%Y-%m-%d')
        formatted_date = due_date_obj.strftime('%b %d')
        formatted_date = formatted_date.replace(' 0', ' ')
        formatted_list.append(f"{inv['vendor']} (due {formatted_date}, ${inv['total']:,.2f})")

    count = len(invoices_list)
    invoice_word = "invoice" if count == 1 else "invoices"
    return f"{count} {invoice_word} ({', '.join(formatted_list)})"

def format_vendors_above_list(vendors_list):
    if not vendors_list:
        return "No vendors found with total invoice value above the threshold."

    formatted_list = []
    for vendor_info in vendors_list:
        formatted_list.append(f"{vendor_info['vendor']} (${vendor_info['total']:,.2f})")

    return ", ".join(formatted_list)

available_functions = {
    "get_invoices_due_in_x_days": get_invoices_due_in_x_days,
    "get_total_for_vendor": get_total_for_vendor,
    "get_vendors_above_amount": get_vendors_above_amount
}

tools_for_llm = [
    {
        "type": "function",
        "function": {
            "name": "get_invoices_due_in_x_days",
            "description": "Get a list of invoices that are due within a specified number of days from today.",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "The number of days to look ahead for due invoices, e.g. 7 for the next week.",
                    }
                },
                "required": ["days"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_total_for_vendor",
            "description": "Get the total monetary value of all invoices from a specific vendor or company.",
            "parameters": {
                "type": "object",
                "properties": {
                    "vendor_name": {
                        "type": "string",
                        "description": "The name of the vendor or company, e.g. Amazon or Microsoft.",
                    }
                },
                "required": ["vendor_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_vendors_above_amount",
            "description": "Get all vendors whose total invoice value exceeds a specified amount.",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold": {
                        "type": "number",
                        "description": "The monetary threshold to filter vendors by, e.g. 2000 for $2000.",
                    }
                },
                "required": ["threshold"],
            },
        },
    },
]

def ask_question(user_query):
    print(f"\nQ: {user_query}")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_query}],
        tools=tools_for_llm,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        function_name = tool_calls[0].function.name
        function_args = json.loads(tool_calls[0].function.arguments)

        print(f"LLM decided to call function: {function_name} with args: {function_args}")

        function_to_call = available_functions[function_name]
        function_response = function_to_call(**function_args)

        if function_name == "get_invoices_due_in_x_days":
            final_answer = format_due_invoices(function_response)
        elif function_name == "get_total_for_vendor":
            final_answer = f"${function_response:,.2f}"
        elif function_name == "get_vendors_above_amount":
            final_answer = format_vendors_above_list(function_response)
        else:
            final_answer = str(function_response)

        print(f"A: {final_answer}")
        return final_answer

    else:
        final_answer = response_message.content
        print(f"A: {final_answer}")
        return final_answer

if __name__ == '__main__':
    print("*** Invoice Chatbot is Ready! ***")
    print("Type your questions about the invoices (e.g., 'How many are due next week?')")
    print("Type 'quit', 'exit', or press Ctrl+C to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            if user_input:
                ask_question(user_input)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")