import pandas as pd
from icecream import ic
import re

df = pd.read_excel('./1.xls')
print(df)
batch_pattern = ["batch", "btch", "batchno", "batchnumber", "bno"]
qty_pattern = ["qty", "quantity", "qnty", "qtv", "onty"]
medicine_name_pattern = ['productdescription', 'productname', 'description', 'medicinename', 'itemname', 'product', 'particulars']

# Combine all patterns into a single list
all_list = batch_pattern + qty_pattern + medicine_name_pattern

# Function to check if any value in a row matches any pattern
def any_pattern_match(row):
    for value in row:
        if any(pattern in str(value).lower() for pattern in all_list):
            return True
    return False

def find_index(column_list):

    matching_dict = {}

    for i, col_name in enumerate(column_list):
        col_name = "".join(col_name) if isinstance(col_name, tuple) else str(col_name)
        cleaned_col_name = re.sub("[^A-Za-z0-9]+", "", col_name.lower())

        if any(pattern in cleaned_col_name for pattern in batch_pattern):
            matching_dict["Batch Number OCR"] = i
        elif any(
            pattern in cleaned_col_name 
                and "l" not in cleaned_col_name
                and "sch" not in cleaned_col_name
                and "disc" not in cleaned_col_name
                and "f" not in cleaned_col_name
            for pattern in qty_pattern
        ):
            matching_dict["Quantity"] = i
        elif any(pattern in cleaned_col_name for pattern in medicine_name_pattern):
            matching_dict["Product Description"] = i
    
    return matching_dict

# Apply the function to each row and get the index of the matching row
matching_row_index = df[df.apply(any_pattern_match, axis=1)].index
ic(matching_row_index)
order = df.iloc[22]
df.columns = order
df = df.drop([x for x in range(23)])
ic(df)
col_index = find_index(df.columns)
ic(col_index, df.columns)
new_col_name = ["description", "batch_number", "quantity", "page_no"]
old_col__name = ["Product Description", "Batch Number OCR", "Quantity", "page_no"]
new_col_names = {df.columns[value]: key for key, value in col_index.items()}
df.rename(columns=new_col_names, inplace=True)
df.rename(columns=dict(zip(old_col__name, new_col_name)), inplace=True)
df['page_no'] = 1
df = df.iloc[:, list(col_index.values())+[-1]]
df_cleaned = df.dropna(subset=new_col_name)
ic(df_cleaned)