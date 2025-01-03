import pandas as pd
import os
def get_sk_statement(statement_csv_path='/Users/robertsoroka/Downloads/SK6575000000004026922060_202412242335.csv'):
    # Path to the CSV file
    file_path = statement_csv_path

    # Read the CSV file, skipping the first two rows (header=2)
    raw_csv_entries = pd.read_csv(file_path, header=2)

    # Convert the 'datum zauctovania' column to datetime format
    raw_csv_entries["datum zauctovania"] = pd.to_datetime(raw_csv_entries["datum zauctovania"], dayfirst=True)

    # Print the converted column
    print(raw_csv_entries.columns)

    # Create the output directory if it doesn't exist
    output_dir = 'transactions_2024'
    os.makedirs(output_dir, exist_ok=True)

    # Add a 'Month' column for grouping
    raw_csv_entries['Month'] = raw_csv_entries['datum zauctovania'].dt.strftime('%Y-%m')

    # Group by month and save each group to a separate CSV
    for month, group in raw_csv_entries.groupby('Month'):
        # Define the output file path
        output_file = os.path.join(output_dir, f"{month}_SK.csv")

        # Save the group to a CSV file (excluding the 'Month' column if not needed)
        group.drop(columns=['Month'], inplace=True)  # Remove this line if you want to keep the 'Month' column
        group.to_csv(output_file, index=False)

        print(f"Saved {month} data to {output_file}")

    return group[["datum zauctovania","suma", "mena", "typ transakcie", "nazov protistrany"]]

a = get_sk_statement()
print(a)