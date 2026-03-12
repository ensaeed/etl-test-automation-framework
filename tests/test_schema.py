import  pandas as pd

from validators.schema_validator import missing_required_columns
from  validators.schema_validator import extra_columns
from  validators.schema_validator import columns_with_nulls


def test_required_colmuns_prsent (source_df,config):

    required = config["schema"]["required_columns"]

    missing = missing_required_columns(source_df,required)

    assert not missing, f"Missing required columns: {missing}"



def test_no_extra_columns_present(source_df,config):


    expected = config["schema"]["required_columns"]

    extras=extra_columns(source_df, expected)

    assert not extras,f" Unexpected column found: {extras}"


def test_no_nulls_in_required_columns(source_df,config):
    required = config["schema"]["required_columns"]

    null_columns=columns_with_nulls(source_df,required)

    assert not null_columns,f"Null values found in required columns:{null_columns}"
