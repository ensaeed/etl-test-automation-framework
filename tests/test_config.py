from pathlib import Path
import tempfile
import yaml
import pytest

from etl.config import load_config


def test_load_config_reads_valid_yaml() -> None:
    """
    A valid YAML config should load successfully.
    """
    config_data = {
        "paths": {
            "input_file": "data/sample_input.csv",
            "expected_output": "data/expected_output.csv",
        },
        "schema": {
            "required_columns": [
                "customer_id",
                "first_name",
                "last_name",
                "zipcode",
                "created_at",
            ]
        },
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        config_file = Path(tmp_dir) / "config.yaml"
        config_file.write_text(yaml.safe_dump(config_data), encoding="utf-8")

        config = load_config(config_file)

        assert "paths" in config
        assert "schema" in config
        assert config["paths"]["input_file"] == "data/sample_input.csv"
        assert "required_columns" in config["schema"]


def test_load_config_raises_for_missing_file() -> None:
    """
    Missing config file should raise FileNotFoundError.
    """
    missing_path = Path("does_not_exist.yaml")

    with pytest.raises(FileNotFoundError):
        load_config(missing_path)


def test_load_config_raises_for_invalid_yaml() -> None:
    """
    Invalid YAML syntax should fail clearly.
    """
    invalid_yaml = """
    paths:
      input_file: data/sample_input.csv
      expected_output: [unclosed_list
    """

    with tempfile.TemporaryDirectory() as tmp_dir:
        config_file = Path(tmp_dir) / "bad_config.yaml"
        config_file.write_text(invalid_yaml, encoding="utf-8")

        with pytest.raises(Exception):
            load_config(config_file)


def test_load_config_contains_required_top_level_keys() -> None:
    """
    Config should include expected top-level sections.
    """
    config_data = {
        "paths": {"input_file": "data/sample_input.csv"},
        "schema": {"required_columns": ["customer_id"]},
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        config_file = Path(tmp_dir) / "config.yaml"
        config_file.write_text(yaml.safe_dump(config_data), encoding="utf-8")

        config = load_config(config_file)

        assert "paths" in config
        assert "schema" in config


def test_load_config_raises_when_required_section_missing() -> None:
    """
    If your config loader validates required sections,
    missing schema should raise an error.
    """
    config_data = {
        "paths": {"input_file": "data/sample_input.csv"},
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        config_file = Path(tmp_dir) / "config.yaml"
        config_file.write_text(yaml.safe_dump(config_data), encoding="utf-8")

        with pytest.raises((KeyError, ValueError)):
            load_config(config_file)