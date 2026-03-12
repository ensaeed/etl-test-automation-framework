import  pytest
import pandas as pd
from pathlib import Path

import yaml


@pytest.fixture()
def config():
    config_path=Path.cwd()/"config"/"config.yaml"
    with open(config_path,"r") as f:
        return yaml.safe_load(f)

@pytest.fixture()
def source_file_path(config):
    return Path.cwd() / config["paths"]["input_file"]


@pytest.fixture()
def source_df(source_file_path):
    return pd.read_csv(source_file_path)

@pytest.fixture()
def expected_df():
    return pd.read_csv("data/expected_output.csv")