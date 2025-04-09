from .utils import MunicipalityDataLoader


class NepalMunicipalities:
    def __init__(self):
        self.data_loader = MunicipalityDataLoader()
        self.municipalaties = self.data_loader.get_municipalities()
    
    def get_all_municipalities(self):
        """Returns a list of all Municipalities."""
        return self.municipalaties
    
    def get_municipality_detail(self, name):
        """Returns Municipality details by name."""
        municipality = next((p for p in self.municipalaties if p['name'].lower() == name.lower()), None)
        if municipality:
            return municipality
        else:
            return {"message": f"municipality '{name}' not found."}
    
    def get_municipality_area(self, name):
        """Returns the area (sq km) of a municipality by name."""
        municipality = self.get_municipality_detail(name)
        if isinstance(municipality, dict) and "message" in municipality:
            return municipality  # Return the error message
        return municipality['area_sq_km'] if municipality else None
    
    def get_municipality_website(self, name):
        """Returns the official website of a municipality by name."""
        municipality = self.get_municipality_detail(name)
        if isinstance(municipality, dict) and "message" in municipality:
            return municipality  # Return the error message
        return municipality['website'] if municipality else None
    
    def get_municipality_type(self, name):
        """Returns the type of a municipality by name."""
        municipality = self.get_municipality_detail(name)
        if isinstance(municipality, dict) and "message" in municipality:
            return municipality  # Return the error message
        return municipality['type'] if municipality else None
    
    def get_total_wards(self, name):
        """Returns the no of wards of a municipality by name."""
        municipality = self.get_municipality_detail(name)
        if isinstance(municipality, dict) and "message" in municipality:
            return municipality  # Return the error message
        return municipality['wards'] if municipality else None
# Example Usage
if __name__ == "__main__":
    np = NepalMunicipalities()
