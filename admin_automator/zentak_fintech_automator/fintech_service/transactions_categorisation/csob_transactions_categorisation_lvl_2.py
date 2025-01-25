import numpy as np
import pandas as pd
import json


class ExpenseCategorisationLvl2:
    def __init__(self, sample_transactions: str, data_dict_path: str):
        # Load data_dict from JSON file
        try:
            with open(data_dict_path, "r") as f:
                self.data_dict = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise ValueError("The 'data_dict_path' parameter must be a valid path to a JSON file.") from e

        # Load transactions
        try:
            self.sample_transactions = pd.read_csv(sample_transactions)
        except Exception as e:
            raise ValueError("The 'sample_transactions' parameter must be a valid path to a CSV file.") from e

        # Validate that sample_transactions is a DataFrame
        if not isinstance(self.sample_transactions, pd.DataFrame):
            raise TypeError("The 'sample_transactions' parameter must be a pandas DataFrame.")

        self.transactions = self.sample_transactions.copy()

    def assign_category_2_using_data_dict(self):
        # Replace NaN values with "null" in the dataframe
        self.transactions = self.transactions.fillna("null")

        # Ensure all relevant columns are strings and standardized
        columns_to_cast = [
            "Currency", "Transaction Type", "category_1",
            "Counterparty bank account", "Counterparty Name"
        ]
        for col in columns_to_cast:
            if col in self.transactions.columns:
                self.transactions[col] = self.transactions[col].astype(str).str.strip()

        # Standardize data_dict formatting
        standardized_data_dict = {
            category_key: [
                {k: (v.strip() if isinstance(v, str) else v) for k, v in transaction.items()}
                for transaction in transactions
            ]
            for category_key, transactions in self.data_dict.items()
        }

        def determine_category_2(row):
            for category_key, mapping_transactions in standardized_data_dict.items():
                for transaction in mapping_transactions:
                    # Match row values with transaction dictionary
                    #print(row)
                    if (
                            category_key == row["category_1"] and
                            transaction.get("currency") == row["Currency"] and
                            transaction.get("transaction_type") == row["Transaction Type"] and
                            transaction.get("counterparty_bank_account") == row["Counterparty bank account"]
                    ):
                        print("Match")
                        return transaction.get("category_2")
            return "unknown"

        # Apply function row-wise to assign category_2
        self.transactions["category_2"] = self.transactions.apply(determine_category_2, axis=1)
        self.transactions["amount_in_eur"] = 0  # Initialize the column
        self.transactions["amount_in_eur"] = np.where(
            self.transactions["Currency"] == "CZK",
            self.transactions["Amount"] / 25,
            self.transactions["Amount"]
        )
        self.transactions["Date"] = pd.to_datetime(self.transactions["Date"], format="%d.%m.%Y", errors="coerce")
        return self.transactions


'''instance = ExpenseCategorisationLvl2("/Users/robertsoroka/PycharmProjects/office_automator_1/fin_analytics/transactions_categorisation/category_1.csv",
                                    )
print(instance.assign_category_2_using_data_dict())
instance.assign_category_2_using_data_dict().to_csv("category_2.csv")
'''