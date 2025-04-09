import json
import os


class ProvinceDataLoader:
    """Loads province data from the external dataset file."""
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "dataset", "provinces", "en.json")
        self.provinces = self._load_data()
    
    def _load_data(self):
        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def get_provinces(self):
        return self.provinces

class MunicipalityDataLoader:
    """Loads municipality data from the external dataset file."""
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "dataset", "municipalities", "en.json")
        self.municipalities = self._load_data()
    
    def _load_data(self):
        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def get_municipalities(self):
        return self.municipalities


class DistrictDataLoader:
    """Loads district data from the external dataset file."""
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__),  "dataset", "districts", "en.json")
        self.districts = self._load_data()
    
    def _load_data(self):
        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def get_districts(self):
        return self.districts
    
class AllDataLoader:
    """Loads district data from the external dataset file."""
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__),  "dataset", "alldataset", "en.json")
        self.all_info = self._load_data()
    
    def _load_data(self):
        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def get_all_info(self):
        return self.all_info