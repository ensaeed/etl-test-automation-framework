# ETL Test Automation Framework


[![ETL CI](https://github.com/ensaeed/etl-test-automation-framework/actions/workflows/etl-ci.yml/badge.svg)](https://github.com/ensaeed/etl-test-automation-framework/actions)
This project demonstrates a **Python-based ETL testing framework using Pytest,Pandas and GitHub Actions**.

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
ETL Test Automation Framework
│
├── config/                # Config-driven testing
├── data/                  # Sample datasets
├── etl/                   # Loader / extractor / transformer
├── fixtures/              # Pytest fixtures
├── tests/                 # Schema, quality, reconciliation tests
│
├── pytest.ini
├── requirements.txt
├── README.md
│
└── .github/workflows/
    └── etl-ci.yml         # CI pipeline
```

## Goal of the Project

To demonstrate best practices for **automated data pipeline testing**, including:

* schema validation
* data quality checks
* transformation testing
* dataset reconciliation
* end-to-end pipeline verification

* ## Example Data
Sample input and expected output datasets are provided in the `data/` folder.


## How to Run the ETL Tests

1. Install dependencies:
   pip install -r requirements.txt

2. Run the test suite:
   pytest

 ## Example Usage

Sample input and expected output datasets are available in the `data/` folder.

To run the ETL tests:

pip install -r requirements.txt
pytest

## Project Structure

etl-test-automation-framework/
│
├── etl/                  # ETL transformation logic
├── validators/           # Schema and data validation
├── tests/                # Automated test suite
├── data/                 # Sample input and expected output datasets
├── config/               # Configuration files
├── paper/                # JOSS paper
├── requirements.txt
├── README.md

## Continuous Integration

The project uses GitHub Actions to automatically run the ETL test suite when changes are pushed to the repository.

## Citation

If you use this software, please cite:

Saeed, E. (2026). Automating ETL Pipeline Testing Using Pytest and Continuous Integration. Journal of Open Source Software.


