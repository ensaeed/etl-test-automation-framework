from pathlib import Path

def source_file_exists(file_path):
    return Path(file_path).exists()