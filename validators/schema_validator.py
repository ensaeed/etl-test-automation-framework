import  pandas as pd

def missing_required_columns (df,required_columns):
    """Return a list of required columns that are missing from the DataFrame."""
    df_cols=set(df.columns) # Turns list into set for faster lookup
    return [col for col in required_columns if col not in df_cols]
    "Loop through the required for columns and keep the missing ones"


def extra_columns(df,expected_columns):
    """
        Return a list of columns that exist in the DataFrame
        but are NOT defined in the expected schema.
        """
    df_cols=set(df.columns)
    expected=set(expected_columns)
    return [col for col in df_cols if col not in expected]


def columns_with_nulls(df,required_columns):
    """"
    Return a list of required columns that contain null values
    """
    return [col for col in required_columns if df[col].isnull().any()]

