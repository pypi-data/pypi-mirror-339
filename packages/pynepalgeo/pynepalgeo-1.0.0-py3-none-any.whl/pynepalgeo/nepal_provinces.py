"""load data from utils.py using relative path"""
from .utils import ProvinceDataLoader


class NepalProvinces:
    def __init__(self):
        self.data_loader = ProvinceDataLoader()
        self.provinces = self.data_loader.get_provinces()
    
    def get_all_provinces(self):
        """Returns a list of all provinces."""
        return self.provinces
    
    def get_province_detail(self, name):
        """Returns province details by name."""
        province = next((p for p in self.provinces if p['name'].lower() == name.lower()), None)
        if province:
            return province
        else:
            return {"Message": f"Province '{name}' not found."}
    
    def get_province_area(self, name):
        """Returns the area (sq km) of a province by name."""
        province = self.get_province_detail(name)
        if isinstance(province, dict) and "message" in province:
            return province  # Return the error message
        return province['area_sq_km'] if province else None
    
    def get_province_website(self, name):
        """Returns the official website of a province by name."""
        province = self.get_province_detail(name)
        if isinstance(province, dict) and "message" in province:
            return province  # Return the error message
        return province['website'] if province else None
    
    def get_province_headquarter(self, name):
        """Returns the headquarter of a province by name."""
        province = self.get_province_detail(name)
        if isinstance(province, dict) and "message" in province:
            return province  # Return the error message
        return province['headquarter'] if province else None
    
# Example Usage
if __name__ == "__main__":
    np = NepalProvinces()
