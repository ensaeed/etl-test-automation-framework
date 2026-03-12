import pandas as pd
import pytest
from etl.transformer import transform_customers

@pytest.mark.e2e
def test_end_to_end_pipeline_runs_successfully(source_df):
    out=transform_customers(source_df)

    assert out is not None
    assert not out.empty

@pytest.mark.e2e
def test_end_to_end_output_has_expected_columns(source_df):
    out=transform_customers(source_df)

    expected_columns={
        "customer_id",
        "first_name",
        "last_name",
        "postcode",
        "created_at",
        "full_name",
    }
    assert expected_columns.issubset(set(out.columns))

@pytest.mark.e2e
def test_end_to_end_customer_ids_are_unique(source_df):
    out=transform_customers(source_df)

    assert out["customer_id"].is_unique

@pytest.mark.e2e
def test_end_to_end_full_name_is_created(source_df):
    out=transform_customers(source_df)

    expected=(
        out["first_name"].astype(str).str.strip()
        +" "
        + out["last_name"].astype(str).str.strip()
            )
    assert (out["full_name"]==expected).all()

@pytest.mark.e2e
def test_transformed_output_matches_expected_dataset(source_df,expected_df):
    actual_df=transform_customers(source_df)
    expected_df=expected_df.copy()

    actual_df=actual_df.sort_values(by="customer_id").reset_index(drop=True)
    expected_df=expected_df.sort_values(by="customer_id").reset_index(drop=True)

    actual_df["created_at"]=pd.to_datetime(actual_df["created_at"],errors="coerce")
    expected_df["created_at"]=pd.to_datetime(expected_df["created_at"],errors="coerce")


    pd.testing.assert_frame_equal(actual_df,expected_df,check_dtype=False)