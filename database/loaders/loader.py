import os
import json
from pathlib import Path

# Project root directory.
# move to path.py
ROOT_DIR = Path(__file__)
DATA_FOLDER = 'data'

def craft_json_path(file: str="") -> Path:
    """
    Function to join the ROOT_DIR path with all the .json files from ./data
    Will create paths to (tcp, mtu, http).json

    Args:
        file (str): file name with type 

    Returns:
        Path: Full Path from ROOT_DIR to file.
    """
    end_pointer = os.path.join(DATA_FOLDER, file)
    return ROOT_DIR.parent.parent.joinpath(end_pointer)

class Loader:
    
    def __init__(self, json: str) -> None:
        """
        Loader object.

        Args:
            json (str): .json file name.
        """
        self._json_file = json

    def load(self) -> dict:
        """
        Loads the data of a json file.

        Returns:
            dict: JSON data.
        """
        try:
            with open(self._json_file) as json_file:
                return json.loads(json_file.read())
            
        except FileNotFoundError:
            print(f'[!] {self._json_file} doesnt exist!')
            return {}
        