# Nepal Geo Information

A simple Python package to retrieve detail information about geography information of Nepal.

## Installation

 Install it using `pip` (if converted to a package):

```bash
pip install pynepalgeo

```

## Features for NepalDistricts Class

- Get a list of all districts.
- Retrieve specific details about a district by name.
- Access district area, official website, and headquarter. 


```python
from pynepalgeo import NepalDistrict

np = NepalDistrict() #create class
```
#### Get all districts
```python
all_districts = np.get_all_districts()
```

#### Get details of a specific district
```python
detail = np.get_district_detail("Kathmandu")
```

#### Get area of a district in sqkm
```python
area = np.get_district_area("Kathmandu")
```

#### Get official website of a district
```python
website = np.get_district_website("Kathmandu")
```

#### Get district headquarter
```python
headquarter = np.get_district_headquarter("Kathmandu")
```

## Features for Nepal Municipality Class

- Get a list of all municipalities.
- Retrieve specific details about a municipality by name.
- Access district area, official website, type, and total wards.

```python
from pynepalgeo import NepalMunicipalities

np = NepalMunicipalities() #create class
```
#### Get all municipality
```python
all_municipalities = np.get_all_municipalities()
```

#### Get details of a specific municipality
```python
detail = np.get_municipality_detail("Jaljala")
```

#### Get area of a municipality in sqkm
```python
area = np.get_municipality_area("Jaljala")
```

#### Get official website of a municipality
```python
website = np.get_municipality_website("Jaljala")
```

#### Get official website of a municipality
```python
type = np.get_municipality_type("Jaljala")
```
## Features for Nepal Province Class

- Get a list of all provinces.
- Retrieve specific details about a province by name.
- Access province area, official website, and headquarter.

```python
from pynepalgeo import NepalProvinces

np = NepalProvinces() #create class
```
#### Get all province
```python
all_province = np.get_all_provinces()
```

#### Get details of a specific province
```python
detail = np.get_province_detail("Gandaki")
```

#### Get area of a province in sqkm
```python
area = np.get_province_area("Gandaki")
```

#### Get official website of a province
```python
website = np.get_province_website("Gandaki")
```

#### Get official headquarter of a province
```python
type = np.get_province_headquarter("Gandaki")
```

## Features for Nepal NepalFederalInfo Class

- Get a list of all district.
- Get a list of all municipalities.


```python
from pynepalgeo import NepalFederalInfo

np = NepalFederalInfo() #create class
```
#### Get all federal data
```python
all_data = np.get_all_data()
```

#### Get all province
```python
all_district_province_wise = np.get_list_of_district()
```

#### Get all municipality province wise
```python
detail = np.get_list_of_municipalities("Gandaki")
```

#### Get all municipality district wise
```python
detail = np.get_list_of_municipalities("Gandaki","Parbat")
```
