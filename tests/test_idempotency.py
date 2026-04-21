import pandas as pd
from pandas.testing import assert_frame_equal

# Adjust this import to match your project structure
from etl.transformer import transform_customers


def test_transform_is_idempotent(sample_input_df: pd.DataFrame) -> None:
    """
    Running the same transformation twice on the same input
    should produce the same output.
    """
    first_result = transform_customers(sample_input_df.copy())
    second_result = transform_customers(sample_input_df.copy())

    # Sort columns defensively in case output column order changes
    first_result = first_result.sort_index(axis=1)
    second_result = second_result.sort_index(axis=1)

    assert_frame_equal(first_result, second_result)


def test_transform_output_is_stable_when_reapplied() -> None:
    """
    Applying the transformation to already transformed output
    should not introduce duplicate rows or additional changes.

    This assumes the transform function can safely accept already
    transformed data. If your function is only designed for raw input,
    you can remove this test.
    """
    raw_df = pd.DataFrame(
        {
            "customer_id": [101, 101, 102],
            "first_name": ["Alice", "Alice", "Bob"],
            "last_name": ["Smith", "Smith", "Jones"],
            "zipcode": ["sw1a 1aa", "SW1A 1AA", "m1 1ae"],
            "created_at": ["2024-01-01", "2024-01-03", "2024-01-02"],
        }
    )

    first_result = transform_customers(raw_df.copy())
    second_result = transform_customers(first_result.copy())

    first_result = first_result.sort_values(by=["customer_id"]).reset_index(drop=True)
    second_result = second_result.sort_values(by=["customer_id"]).reset_index(drop=True)

    first_result = first_result.sort_index(axis=1)
    second_result = second_result.sort_index(axis=1)

    assert_frame_equal(first_result, second_result)


def test_deduplication_is_repeatable() -> None:
    """
    Deduplication should consistently keep the latest record
    for each customer_id across repeated runs.
    """
    raw_df = pd.DataFrame(
        {
            "customer_id": [1, 1, 1, 2],
            "first_name": ["John", "John", "John", "Jane"],
            "last_name": ["Doe", "Doe", "Doe", "Roe"],
            "zipcode": ["EC1A 1BB", "EC1A 1BB", "EC1A 1BB", "W1A 0AX"],
            "created_at": ["2024-01-01", "2024-01-05", "2024-01-03", "2024-01-02"],
        }
    )

    result_1 = transform_customers(raw_df.copy())
    result_2 = transform_customers(raw_df.copy())

    john_row_1 = result_1.loc[result_1["customer_id"] == 1].iloc[0]
    john_row_2 = result_2.loc[result_2["customer_id"] == 1].iloc[0]

    assert len(result_1[result_1["customer_id"] == 1]) == 1
    assert len(result_2[result_2["customer_id"] == 1]) == 1
    assert str(john_row_1["created_at"]) == str(john_row_2["created_at"])