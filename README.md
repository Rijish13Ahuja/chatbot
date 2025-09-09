# Invoice Chatbot

A small Python chatbot that can read invoices from PDFs and answer basic questions about them using natural language. It leverages OpenAI's GPT model to understand user queries and executes deterministic functions on the parsed invoice data to provide accurate answers.

## Features

- **PDF Invoice Parsing:** Extracts key fields (vendor, invoice number, date, due date, total) from PDF invoices using regex.
- **Natural Language Querying:** Ask questions in plain English about the invoices.
- **Deterministic Answers:** Uses hardcoded logic for calculations, ensuring accuracy for questions about dates, totals, and filters.
- **Sample Data Included:** Works with provided sample invoice PDFs.

## Example Questions & Answers

The chatbot can answer questions like:

*   `How many invoices are due in the next 7 days?`
    > `A: 1 invoice (Amazon (due Sept 5, $2,450.00))`
*   `What is the total value of the invoice from Microsoft?`
    > `A: $3,100.00`
*   `List all vendors with invoices over $2000`
    > `A: Amazon ($2,450.00), Microsoft ($3,100.00)`

## Project Structure
invoice-chatbot/
├── invoices/ # Directory containing sample invoice PDFs
│   ├── amazon_inv_0012.pdf
│   ├── microsoft_inv_0043.pdf
│   └── google_inv_0076.pdf
├── .env # File for storing the OpenAI API key (not in git)
├── .gitignore # Specifies files to be ignored by git
├── invoices.json # Generated file containing parsed invoice data
├── invoice_parser.py # Script to parse PDFs and create invoices.json
├── chatbot.py # Main chatbot application script
├── requirements.txt # Python dependencies
└── README.md # This file



## Prerequisites

Before you begin, ensure you have met the following requirements:

*   **Python 3.7+** installed on your machine.
*   An **OpenAI API key**. You can get one from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).

## Installation & Run Instructions

Follow these steps to set up and run the project:

1.  **Clone or Download the Project**
    ```bash
    git clone <your-repo-url> # Or download and extract the ZIP file
    cd invoice-chatbot
    ```

2.  **Set Up a Virtual Environment and Install Dependencies**
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows (PowerShell):
    .\venv\Scripts\activate
    # On Windows (Command Prompt):
    venv\Scripts\activate.bat

    # Install required packages
    pip install -r requirements.txt
    ```

3.  **Configure Your API Key**
    *   Create a file named `.env` in the project root directory.
    *   Add your OpenAI API key to the file:
        ```ini
        OPENAI_API_KEY=your_actual_api_key_goes_here
        ```
    *   **Replace** `your_actual_api_key_goes_here` with your actual key. **Do not share this key.**

4.  **Parse the Sample Invoices**
    *   This step reads the PDFs in the `invoices/` folder and creates a `invoices.json` data file.
    ```bash
    python invoice_parser.py
    ```
    *   You should see output confirming the invoices were parsed and saved.

5.  **Run the Chatbot**
    *   Start the interactive chatbot application.
    ```bash
    python chatbot.py
    ```
    *   You will see a message: `*** Invoice Chatbot is Ready! ***`
    *   Type your questions at the `You:` prompt.

6.  **To Exit**
    *   Type `quit` or `exit`, or press `Ctrl+C`.

## How It Works

1.  **Data Parsing (`invoice_parser.py`):** Uses `pdfplumber` to extract text from PDF invoices. Regex patterns are then used to find and structure key data fields, which are saved to `invoices.json`.
2.  **Query Logic (`chatbot.py`):** Contains core functions (`get_invoices_due_in_x_days`, `get_total_for_vendor`, etc.) that perform precise calculations on the data.
3.  **LLM Integration (`chatbot.py`):**
    *   The user's natural language question is sent to the OpenAI API.
    *   The LLM (GPT-3.5-turbo) analyzes the question and selects the appropriate function to call, along with its parameters (e.g., `{"days": 7}`).
    *   The script executes the chosen function with the provided parameters.
    *   The result from the function is formatted and displayed as the answer.

This architecture ensures that the LLM handles the natural language understanding, while the precise math and logic are handled by reliable, deterministic code.
