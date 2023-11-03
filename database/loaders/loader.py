import json

class Loader:
    
    def __init__(self, json: str) -> None:
        """
        Loader object.

        Args:
            sig_json (str): loads the data from a given json file. 
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
        