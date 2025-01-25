import pandas as pd
from collections import defaultdict
import json


#statements = pd.read_csv("/../data_prep/sample_transactions/unioned_statements.csv", encoding="utf-16")
class ExpenseCategorisationLvl1:
    def __init__(self, sample_transactions: str):
        self.transactions = sample_transactions

    def categorise_lvl_1(self):
        # Replace commas with dots and convert the 'Amount' column to float
        counterparties = pd.read_csv(self.transactions, header=0, encoding='cp1250',delimiter=";",
                                     usecols=["datum zaúčtování", "popis transakce", "částka platby", "zpráva příjemci i plátci",
                                              "měna platby", "účet protistrany"])
        df2_mapping = {
            'datum zaúčtování': 'Date',
            'částka platby': 'Amount',
            'měna platby': 'Currency',
            'zpráva příjemci i plátci': 'Message',
            'protistrana': 'Counterparty Name',
            'popis transakce': 'Transaction Type',
            'účet protistrany': 'Counterparty bank account'
        }
        counterparties = counterparties.rename(columns=df2_mapping)
        counterparties_init_len = counterparties
        print(counterparties.columns)
        #counterparties['Amount'] = counterparties['Amount'].astype("float")
        counterparties['Amount'] = counterparties['Amount'].str.replace(",", ".").astype(float)

        # Create the 'category_1' column based on the value of 'Amount'
        counterparties['category_1'] = counterparties['Amount'].apply(lambda x: 'income' if x > 0 else 'expense')
        counterparties_post_len = counterparties
        # Ensure lengths match
        assert len(counterparties_post_len) == len(counterparties_init_len), (
            "Length mismatch after processing: "
            f"{len(counterparties_post_len)} vs {len(counterparties_init_len)}"
        )
        return counterparties


category_1 = ExpenseCategorisationLvl1("/Users/robertsoroka/Downloads/csob-export-pohyby-20250118-13-15.CSV")
category_1.categorise_lvl_1().to_csv("transactions_categorisation/category_1.csv")
