import os
from pathlib import Path

# Project root directory.
ROOT_DIR = Path(__file__)
DATA_FOLDER = 'data'

def craft_json_path(file: str="") -> Path:
    """
    Crafts a Path object with file

    Args:
        file (str): file name with type 

    Returns:
        Path: Full Path from ROOT_DIR to file.
    """
    end_pointer = os.path.join(DATA_FOLDER, file)
    return ROOT_DIR.parent.joinpath(end_pointer)

