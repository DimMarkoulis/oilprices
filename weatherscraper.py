import requests
import pandas as pd
import sys

response = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Athens/last300days/today?unitGroup=metric&include=days&elements=temp&key=TAQCS9WRY93G4AP9368CVBQ93&contentType=xlsx")

if response.status_code != 200:
    print('Unexpected Status code: ', response.status_code)
    sys.exit()

# Save the XLSX data to a file
with open('weather_data.xlsx', 'wb') as f:
    f.write(response.content)

# Load the XLSX data into a DataFrame using pandas
df = pd.read_excel('weather_data.xlsx')

# Set 'Datetime' column as index
df.set_index(df.columns[1], inplace=True)

# Save DataFrame as CSV
df.to_csv('weather_data.csv')

# Accessing specific columns
print(df)