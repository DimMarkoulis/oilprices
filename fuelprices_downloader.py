import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime

url = 'http://www.fuelprices.gr/deltia_dn.view'

folder_loc = r'C:\Users\dimma\OneDrive\Υπολογιστής\Πληροφοριακά Συστήματα\Semeter Projects\oil_prices\oil_pdfs'
if not os.path.exists(folder_loc):
    os.mkdir(folder_loc)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Prompt the user for start and end dates in the dd/mm/yyyy format
start_date_str = input("Enter the start date (dd/mm/yyyy): ")
end_date_str = input("Enter the end date (dd/mm/yyyy): ")

# Convert the input date format to datetime objects
start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
end_date = datetime.strptime(end_date_str, '%d/%m/%Y')

for link in soup.select("a[href$='.pdf']"):
    filename = link['href'].split('/')[-1]
    # Extract date from filename assuming the format "IMERISIO_DELTIO_ANA_NOMO_DD_MM_YYYY.pdf"
    try:
        date_str = filename.split('_')[-1].replace('.pdf', '')  # Extracting the date part from the filename
        file_date = datetime.strptime(date_str, '%d_%m_%Y')
        
        # Filter based on the date range
        if start_date <= file_date <= end_date:
            with open(os.path.join(folder_loc, filename), 'wb') as f:
                f.write(requests.get(urljoin(url, link['href'])).content)
    except ValueError:
        try:
            # Try an alternative date format if the first one fails
            parts = filename.split('_')
            if len(parts) >= 4:
                date_str_alt = parts[-3] + '_' + parts[-2] + '_' + parts[-1].replace('.pdf', '')
                file_date_alt = datetime.strptime(date_str_alt, '%d_%m_%Y')
                
                # Filter based on the date range
                if start_date <= file_date_alt <= end_date:
                    with open(os.path.join(folder_loc, filename), 'wb') as f:
                        f.write(requests.get(urljoin(url, link['href'])).content)
        except (ValueError, IndexError) as e:
            print(f"Error processing {filename}: {e}")
            continue  # Skip the file if both date formats fail
