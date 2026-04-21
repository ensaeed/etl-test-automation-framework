import pandas as pd
import pytest

# Adjust these imports to match your project
from etl.transformer import transform_customers


def test_transform_raises_key_error_when_required_column_missing() -> None:
    """
    If a required column is missing, the transform should fail clearly.
    """
    df = pd.DataFrame(
        {
            "customer_id": [1],
            "first_name": ["John"],
            # "last_name" is missing
            "zipcode": ["SW1A 1AA"],
            "created_at": ["2024-01-01"],
        }
    )

    with pytest.raises(KeyError):
        transform_customers(df)


def test_transform_handles_invalid_created_at_without_crashing() -> None:
    """
    Invalid dates should not crash the pipeline if the framework
    is designed to flag them as invalid records instead.
    """
    df = pd.DataFrame(
        {
            "customer_id": [1],
            "first_name": ["John"],
            "last_name": ["Doe"],
            "zipcode": ["SW1A 1AA"],
            "created_at": ["not-a-date"],
        }
    )

    result = transform_customers(df)

    assert len(result) == 1
    assert "is_valid_record" in result.columns
    assert result.loc[0, "is_valid_record"] in [False, 0]


def test_transform_handles_invalid_postcode_without_crashing() -> None:
    """
    Invalid postcode should be flagged, not necessarily crash the job.
    """
    df = pd.DataFrame(
        {
            "customer_id": [2],
            "first_name": ["Sara"],
            "last_name": ["Khan"],
            "zipcode": ["BAD_POSTCODE"],
            "created_at": ["2024-01-01"],
        }
    )

    result = transform_customers(df)

    assert len(result) == 1
    assert result.loc[0, "is_valid_record"] in [False, 0]


def test_transform_handles_none_input_defensively() -> None:
    """
    Passing None should fail fast with a clear exception.
    """
    with pytest.raises((TypeError, AttributeError, ValueError)):
        transform_customers(None)  # type: ignore[arg-type]


def test_transform_handles_empty_dataframe() -> None:
    """
    Empty DataFrame should return empty result rather than crash.
    """
    df = pd.DataFrame(
        columns=["customer_id", "first_name", "last_name", "zipcode", "created_at"]
    )

    result = transform_customers(df)

    assert isinstance(result, pd.DataFrame)
    assert result.empty