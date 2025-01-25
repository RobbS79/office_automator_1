import json
import pandas as pd
from collections import defaultdict


class ExpensesMapper:
    def __init__(self, category_1_transaction_sample_path):
        self.category_1_transaction_sample_path = category_1_transaction_sample_path
        # Read the CSV file and replace NaN with "null"
        self.df = pd.read_csv(self.category_1_transaction_sample_path).fillna("null")

    def map_dataframe_to_json(self):
        # Initialize a defaultdict for hierarchical data
        data_dict = defaultdict(list)

        # Iterate through the rows of the DataFrame
        for _, row in self.df.iterrows():
            # Organize data based on transaction type and category
            key = f"{row['category_1']}"
            transaction_data = {
                "currency": row["Currency"],
                "transaction_type": row["Transaction Type"],
                "counterparty_name": row["Counterparty Name"],
                "counterparty_bank_account": row["Counterparty bank account"],
                "category_2": row["category_2"]
            }
            data_dict[key].append(transaction_data)

        # Write the data to a JSON file
        with open('transactions_categorisation/init_transactions_mapper.json', 'w', encoding='utf-8') as json_file:
            json.dump(dict(data_dict), json_file, ensure_ascii=False, indent=4)


# Example usage:
mapper = ExpensesMapper('/Users/robertsoroka/PycharmProjects/office_automator_1/fin_analytics/transactions_categorisation/category_2_init.csv')
mapper.map_dataframe_to_json()

"""
def assign_category_2_using_data_dict(df, data_dict):
    # Define columns to exclude from the matching process
    excluded_columns = {"Date", "Amount", "Message"}

    # Convert relevant columns to string for consistency
    df["Counterparty Name"] = df["Counterparty Name"].astype(str)
    df["Counterparty bank account"] = df["Counterparty bank account"].astype(str)

    # Function to determine category_2 for a row
    def determine_category_2(row):
        for category_key, transactions in data_dict.items():
            for transaction in transactions:
                # Ensure all comparisons are type-safe
                if (transaction.get("currency", "") == row.get("Currency", "") and
                        transaction.get("transaction_type", "") == row.get("Transaction Type", "") and
                        str(transaction.get("counterparty_bank_account", "") or "").strip() ==
                        str(row.get("Counterparty bank account", "") or "").strip()):
                    return transaction.get("category_2", "unknown")  # Return category_2 if found

        return "unknown"  # Default if no match is found

    # Apply the function to each row in the DataFrame
    df["category_2"] = df.apply(determine_category_2, axis=1)

    # Fill NaN values in category_2 with an empty string
    df["category_2"] = df["category_2"].fillna("")

    return df

#df2 = pd.read_csv("")

#instance = assign_category_2_using_data_dict(df, transactions_dict)
#instance.to_csv("categorised.csv", index=False)

"""