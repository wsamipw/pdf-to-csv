import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
import argparse

def extract_table_from_pdf(pdf_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        for page in pdf.pages:
            print(f'Extracting table from page {page.page_number}')
            # Extract tables from each page
            tables = page.extract_tables()
            for table in tables:
                all_tables.extend(table)
    return all_tables

def filter_rows_by_polling_center(table, polling_center):
    # Convert table to DataFrame
    df = pd.DataFrame(table[1:], columns=table[0])
    # Filter rows where Polling Center is the specified value
    filtered_df = df[df['Polling Center'] == polling_center]
    return filtered_df

def main():
    parser = argparse.ArgumentParser(description='Filter PDF table rows by Polling Center.')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    parser.add_argument('polling_center', type=str, help='Polling Center to filter by')
    args = parser.parse_args()

    # Extract tables from PDF
    table = extract_table_from_pdf(args.pdf_path)

    # Filter rows where Polling Center is specified value
    filtered_data = filter_rows_by_polling_center(table, args.polling_center)

    # Save the filtered data to a new CSV file
    filtered_data.to_csv(f'filtered_data_{args.polling_center}.csv', index=False)

if __name__ == '__main__':
    main()
