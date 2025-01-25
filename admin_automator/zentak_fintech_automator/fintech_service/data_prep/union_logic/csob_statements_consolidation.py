import pandas as pd

df2 = pd.read_csv('/Users/robertsoroka/Downloads/csob-export-pohyby-20241225-00-13.CSV',delimiter=";",encoding="cp1250")
df1 = pd.read_csv('/Users/robertsoroka/Downloads/SK6575000000004026922060_202412242335.csv',header=2)


# Define mappings to standardize column names
df1_mapping = {
    'datum zauctovania': 'Date',
    'suma': 'Amount',
    'mena': 'Currency',
    'typ transakcie': 'Transaction Type',
    'nazov protistrany': 'Counterparty Name',
    'informacia pre prijemcu': 'Message',
    'cislo uctu protistrany': "Counterparty bank account"

}

df2_mapping = {
    'datum zaúčtování': 'Date',
    'částka platby': 'Amount',
    'měna platby': 'Currency',
    'zpráva příjemci i plátci': 'Message',
    'protistrana': 'Counterparty Name',
    'popis transakce': 'Transaction Type',
    'účet protistrany': 'Counterparty bank account'
}

# Standardize column names
df1 = df1.rename(columns=df1_mapping)
df2 = df2.rename(columns=df2_mapping)


# Add missing columns with default values if necessary
for col in df1.columns:
    if col not in df2.columns:
        df2[col] = None  # Or set a sensible default value

for col in df2.columns:
    if col not in df1.columns:
        df1[col] = None  # Or set a sensible default value"""


# Ensure consistent column order
df2 = df2[df1.columns]

# Concatenate dataframes
union_df = pd.concat([df1, df2], ignore_index=True)

# Add a 'Category' column (optional)
union_df['Category'] = None
union_df = union_df[["Date","Amount","Currency","Transaction Type","Counterparty Name", "Counterparty bank account", "Message"]]
# View the resulting dataframe
union_df.to_csv("data_prep/sample_transactions/unioned_statements.csv",encoding='utf-16',index=False)
