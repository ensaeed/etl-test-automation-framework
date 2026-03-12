import pandas as pd

from validators.data_validators import find_duplicate_keys
from validators.data_validators import invalid_datetimes
from validators.data_validators import invalid_postcodes

def test_no_duplicate_customer_ids(source_df):
    duplicates=find_duplicate_keys(source_df,["customer_id"])
    assert duplicates.empty,f"Duplicate customer_id found:{duplicates}"


def test_postcode_format_valid(source_df):
    bad_mask=invalid_postcodes(source_df,"postcode")
    bad_rows=source_df[bad_mask]
    assert bad_rows.empty,f"Invalid Postcode values:{bad_rows}"


def test_created_at_valid_datetime(source_df):
    bad_mask=invalid_datetimes(source_df,"created_at")
    bad_rows=source_df[bad_mask]
    assert bad_rows.empty,f"Invalid datetime values:{bad_rows}"