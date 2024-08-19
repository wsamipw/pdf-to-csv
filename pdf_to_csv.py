import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
import argparse
import os

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

def convert_to_csv(table):
    output_dir = './export'
    output_file_name = 'all_data.csv'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    full_file_path = os.path.join(output_dir, output_file_name)
    df = pd.DataFrame(table[1:], columns=table[0])
    df.to_csv(full_file_path, index=False)
    print('Done!')

def main():
    parser = argparse.ArgumentParser(description='Convert PDF to CSV')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    args = parser.parse_args()

    print(f'Converting {args.pdf_path} to CSV...')

    # Extract tables from PDF
    table = extract_table_from_pdf(args.pdf_path)

    # Convert tables to CSV
    convert_to_csv(table)

if __name__ == '__main__':
    main()
