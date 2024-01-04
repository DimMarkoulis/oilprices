import os
import pandas as pd
from PyPDF2 import PdfReader
import re

def extract_data_after_nomos_attikis(text):
    pattern = r"ΝΟΜΟΣ ΑΤΤΙΚΗΣ(.{36})"  # Pattern to capture 24 characters after "ΝΟΜΟΣ ΑΤΤΙΚΗΣ"
    matches = re.findall(pattern, text)
    return matches

def extract_from_multiple_pdfs(folder_path):
    pdf_files = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]

    all_results = []
    for file_name in pdf_files:
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)

            text = ''
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

        result = extract_data_after_nomos_attikis(text)
        all_results.append(result)

    # Create a DataFrame to store the extracted data from all PDFs
    df = pd.DataFrame({'Extracted Data': all_results})

    # Extract only the last element from each list in the DataFrame
    df['Extracted Data'] = df['Extracted Data'].apply(lambda x: x[-1] if x else None)

    return df

# Replace 'folder_path' with the directory path containing your PDF files
folder_path = r"C:\Users\dimma\OneDrive\Υπολογιστής\Πληροφοριακά Συστήματα\Semeter Projects\oil_prices"

# Extract data from multiple PDFs
extracted_data_df = extract_from_multiple_pdfs(folder_path)

# Export the DataFrame to an Excel file
output_excel = "extracted_data.xlsx"
extracted_data_df.to_excel(output_excel, index=False)

# Display the path to the exported Excel file
print(f"Data exported to: {output_excel}")
