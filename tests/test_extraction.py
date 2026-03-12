from etl.extractor import source_file_exists

def test_source_file_exists(source_file_path):
    assert source_file_exists(source_file_path), f"Missing file:{source_file_path}"