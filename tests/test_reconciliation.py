import pandas as pd
from etl.transformer import transform_customers


def test_row_count_reconciliation(source_df):
    out= transform_customers(source_df)
    assert len(out)==source_df["customer_id"].nunique()


def test_all_customers_present(source_df):
    out=transform_customers(source_df)
    assert set(out["customer_id"])==set(source_df["customer_id"])

def test_names_reconciled(source_df):
    out=transform_customers(source_df)
    expected=(
        out["first_name"].str.strip()+
        " "+
        out["last_name"].str.strip()
    )
    assert (out["full_name"]==expected).all()


def test_no_customers_lost(source_df):
    out = transform_customers(source_df)
    assert set(out["customer_id"])==set(source_df["customer_id"])



