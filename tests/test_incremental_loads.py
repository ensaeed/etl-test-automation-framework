import pandas as pd

# Adjust this import to match your project
from etl.transformer import transform_customers


def test_incremental_load_keeps_only_latest_record_per_customer() -> None:
    """
    For duplicate customer IDs, the latest record by created_at should be retained.
    """
    df = pd.DataFrame(
        {
            "customer_id": [1001, 1001, 1002],
            "first_name": ["Alice", "Alice", "Bob"],
            "last_name": ["Smith", "Smith", "Jones"],
            "zipcode": ["SW1A 1AA", "EC1A 1BB", "M1 1AE"],
            "created_at": ["2024-01-01", "2024-02-01", "2024-01-15"],
        }
    )

    result = transform_customers(df)

    assert len(result[result["customer_id"] == 1001]) == 1
    latest_row = result[result["customer_id"] == 1001].iloc[0]
    assert latest_row["postcode"] == "EC1A 1BB"


def test_incremental_load_adds_new_customer_records() -> None:
    """
    New customer IDs should be preserved in the output.
    """
    df = pd.DataFrame(
        {
            "customer_id": [2001, 2002],
            "first_name": ["John", "Sara"],
            "last_name": ["Doe", "Khan"],
            "zipcode": ["SW1A 1AA", "B1 1AA"],
            "created_at": ["2024-01-01", "2024-01-02"],
        }
    )

    result = transform_customers(df)

    assert set(result["customer_id"]) == {2001, 2002}


def test_incremental_load_replaces_older_record_with_newer_one() -> None:
    """
    A newer version of an existing customer record should replace the older one.
    """
    df = pd.DataFrame(
        {
            "customer_id": [3001, 3001],
            "first_name": ["Amina", "Amina"],
            "last_name": ["Yusuf", "Yusuf"],
            "zipcode": ["M1 1AE", "LS1 1UR"],
            "created_at": ["2024-01-10", "2024-03-05"],
        }
    )

    result = transform_customers(df)

    customer_row = result[result["customer_id"] == 3001].iloc[0]
    assert customer_row["postcode"] == "LS1 1UR"


def test_incremental_load_with_same_timestamp_is_deterministic() -> None:
    """
    If duplicate records have the same timestamp, the framework should still
    behave deterministically. This test mainly checks that only one record remains.
    """
    df = pd.DataFrame(
        {
            "customer_id": [4001, 4001],
            "first_name": ["Noor", "Noor"],
            "last_name": ["Ahmed", "Ahmed"],
            "zipcode": ["SW1A 1AA", "SW1A 1AA"],
            "created_at": ["2024-01-01", "2024-01-01"],
        }
    )

    result = transform_customers(df)

    assert len(result[result["customer_id"] == 4001]) == 1


def test_incremental_load_handles_late_arriving_record() -> None:
    """
    Simulates a late-arriving record with an older timestamp.
    The newer record should still remain as the final version.
    """
    df = pd.DataFrame(
        {
            "customer_id": [5001, 5001],
            "first_name": ["Omar", "Omar"],
            "last_name": ["Ali", "Ali"],
            "zipcode": ["B2 2BB", "B1 1AA"],
            "created_at": ["2024-03-01", "2024-01-01"],
        }
    )

    result = transform_customers(df)

    customer_row = result[result["customer_id"] == 5001].iloc[0]
    assert customer_row["postcode"] == "B2 2BB"