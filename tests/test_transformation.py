import pandas as pd
from etl.transformer import transform_customers


def test_transform_customers_keeps_latest_record_per_customer(source_df):


    out = transform_customers(source_df)

    # One row per customer

    assert out ["customer_id"].is_unique

    # check latest record is retained
    expected_df=source_df.copy()
    expected_df["created_at"]=pd.to_datetime(expected_df["created_at"],errors="coerce")
    out["created_at"]=pd.to_datetime(out["created_at"],errors='coerce')

    for cust_id in source_df["customer_id"].unique():
        expected_max = expected_df[expected_df["customer_id"] == cust_id]["created_at"].max()
        actual = out.loc[out["customer_id"] == cust_id, "created_at"].iloc[0]
        assert actual == expected_max


#Postcode standardisation test
def test_postcode_is_uppercase(source_df):
    out=transform_customers(source_df)
    assert out["postcode"].str.isupper().all()


#Full name creation test
def test_full_name_created(source_df):
    out=transform_customers(source_df)
    assert "full_name" in out.columns


#Datetime conversion test
def test_created_at_is_datetime(source_df):
    out=transform_customers(source_df)

    assert pd.api.types.is_datetime64_any_dtype(out["created_at"])