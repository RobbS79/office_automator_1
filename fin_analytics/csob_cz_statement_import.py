import pandas as pd
import os

file_path = '/Users/robertsoroka/Downloads/csob-export-pohyby-20241225-00-13.CSV'

# Read the CSV with the correct encoding
raw_csv_entries = pd.read_csv(file_path, header=0, encoding='cp1250',delimiter=";")
raw_csv_entries["datum zaúčtování"] = pd.to_datetime(raw_csv_entries["datum zaúčtování"], dayfirst=True)
# Display the data
print(raw_csv_entries.columns)
output_dir = 'transactions_2024'
os.makedirs(output_dir, exist_ok=True)

# Add a 'Month' column for grouping
raw_csv_entries['Month'] = raw_csv_entries['datum zaúčtování'].dt.strftime('%Y-%m')

# Group by month and save each group to a separate CSV
for month, group in raw_csv_entries.groupby('Month'):
    # Define the output file path
    output_file = os.path.join(output_dir, f"{month}_CZ.csv")

    # Save the group to a CSV file (excluding the 'Month' column if not needed)
    group.drop(columns=['Month'], inplace=True)  # Remove this line if you want to keep the 'Month' column
    group.to_csv(output_file, index=False)

    print(f"Saved {month} data to {output_file}")
