from .utils import AllDataLoader


class NepalFederalInfo:
    def __init__(self):
        self.data_loader = AllDataLoader()
        self.federal_info = self.data_loader.get_all_info()
    
    def get_all_data(self):
        """Returns a list of all data."""
        return self.federal_info
    
    def get_list_of_district(self, province_name):
        """Returns a list of district names for a given province."""
        province = next((p for p in self.federal_info if p['name'].lower() == province_name.lower()), None)
        if province:
            return [district['name'] for district in province.get("districts", [])]  # Extract only district names
        else:
            return {"message": f"Province '{province_name}' not found."}
    

    def get_list_of_municipalities(self, province_name, district_name=None):
        """Returns a list of municipality names for a given province, and optionally a specific district."""
        
        # Find the province
        province = next((p for p in self.federal_info if p['name'].lower() == province_name.lower()), None)
        
        if not province:
            return {"message": f"Province '{province_name}' not found."}

        municipalities = []
        
        # If a district name is provided, find that district
        if district_name:
            district = next((d for d in province.get("districts", []) if d["name"].lower() == district_name.lower()), None)
            if not district:
                return {"message": f"District '{district_name}' not found in {province_name}."}
            
            # Ensure 'municipalities' is a list before accessing it
            district_municipalities = district.get("municipalities", [])
            if isinstance(district_municipalities, list):
                municipalities.extend([municipality["name"] for municipality in district_municipalities if isinstance(municipality, dict) and "name" in municipality])

    
            else:
                return {"message": f"No municipalities data available for district '{district_name}'."}

        # If no district name is provided, get municipalities from all districts in the province
        else:
            for district in province.get("districts", []):
                district_municipalities = district.get("municipalities", [])
                
                # Check if 'municipalities' is a list before iterating
                if isinstance(district_municipalities, list):
                    municipalities.extend([municipality["name"] for municipality in district_municipalities if isinstance(municipality, dict) and "name" in municipality])
        
        return municipalities if municipalities else {"message": f"No municipalities found in {province_name}."}
    

    
# Example Usage
if __name__ == "__main__":
    np = NepalFederalInfo()
    print(np.get_list_of_district)
