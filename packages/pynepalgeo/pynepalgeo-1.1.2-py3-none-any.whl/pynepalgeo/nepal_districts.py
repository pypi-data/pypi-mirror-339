from .utils import DistrictDataLoader


class NepalDistrict:
    def __init__(self):
        self.data_loader = DistrictDataLoader()
        self.districts = self.data_loader.get_districts()
    
    def get_all_districts(self):
        """Returns a list of all Districts."""
        return self.districts
    
    def get_district_detail(self, name):
        """Returns districts details by name."""
        district = next((p for p in self.districts if p['name'].lower() == name.lower()), None)
        if district:
            return district
        else:
            return {"message": f"district '{name}' not found."}
    
    def get_district_area(self, name):
        """Returns the area (sq km) of a district by name."""
        district = self.get_district_detail(name)
        if isinstance(district, dict) and "message" in district:
            return district  # Return the error message
        return district['area_sq_km'] if district else None
    
    def get_district_website(self, name):
        """Returns the official website of a district by name."""
        district = self.get_district_detail(name)
        if isinstance(district, dict) and "message" in district:
            return district  # Return the error message
        return district['website'] if district else None
    
    def get_district_headquarter(self, name):
        """Returns the headquarter of a municipality by name."""
        district = self.get_district_detail(name)
        if isinstance(district, dict) and "message" in district:
            return district  # Return the error message
        return district['headquarter'] if district else None
    
    
# Example Usage
if __name__ == "__main__":
    np = NepalDistrict()
