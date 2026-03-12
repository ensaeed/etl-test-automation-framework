# ETL Test Automation Framework

This project demonstrates a **Python-based ETL testing framework using Pytest and Pandas**.

The framework validates the entire data pipeline using multiple layers of tests, from basic extraction checks to full end-to-end dataset validation.

## Test Layers Implemented

1. **Extraction Tests**

   * Verify source file exists
   * Ensure input data can be loaded correctly

2. **Schema Validation**

   * Required columns present
   * No unexpected columns
   * No nulls in key fields

3. **Data Quality Checks**

   * Detect duplicate keys
   * Validate postcode format
   * Validate datetime values

4. **Transformation Tests**

   * Verify business logic transformations
   * Ensure `full_name` is created correctly

5. **Reconciliation Tests**

   * Ensure row counts match expected values
   * Confirm no records are lost during transformation

6. **End-to-End Tests**

   * Validate the final transformed dataset
   * Compare actual output against expected dataset

## Technologies Used

* Python
* Pytest
* Pandas

## Running the Tests

Run all tests:

```bash
pytest -v
```

Run only end-to-end tests:

```bash
pytest -v -m e2e
```

## Project Structure

```
ETL/
│
├── data/              # Sample input data
├── etl/               # ETL transformation logic
├── fixtures/          # Test fixtures
├── tests/             # Test suite
├── pytest.ini         # Pytest configuration
└── README.md
```

## Goal of the Project

To demonstrate best practices for **automated data pipeline testing**, including:

* schema validation
* data quality checks
* transformation testing
* dataset reconciliation
* end-to-end pipeline verification
