import pandas as pd

def find_duplicate_keys (df,key_columns):
    """   Return rows where column contains duplicate rows"""
    duplicates = df[df.duplicated(subset=key_columns,keep=False)]
    return duplicates

def invalid_postcodes(df,column):
    """Return rows where postcode is not exactly six digits"""
    return ~df[column].astype(str).str.match(r"^[A-Z]{1,2}\d[A-Z\d]?\s\d[A-Z]{2}$", case=False)

def invalid_datetimes(df,column):
    """Return rows where datetime values cannot be parsed"""
    parsed=pd.to_datetime(df[column],errors="coerce")
    return parsed.isna()