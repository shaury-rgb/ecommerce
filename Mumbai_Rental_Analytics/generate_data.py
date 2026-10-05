import csv
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)

def generate_normal(mean, std):
    # Box-Muller transform for normal distribution
    import math
    u1 = random.random()
    u2 = random.random()
    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return mean + z0 * std

localities = [
    {"name": "Bandra West", "base_rent": 80000, "base_sqft": 600, "lat": 19.0596, "lon": 72.8295},
    {"name": "Andheri West", "base_rent": 50000, "base_sqft": 550, "lat": 19.1363, "lon": 72.8277},
    {"name": "Powai", "base_rent": 60000, "base_sqft": 700, "lat": 19.1176, "lon": 72.9060},
    {"name": "Worli", "base_rent": 100000, "base_sqft": 800, "lat": 19.0169, "lon": 72.8166},
    {"name": "Lower Parel", "base_rent": 90000, "base_sqft": 750, "lat": 18.9953, "lon": 72.8282},
    {"name": "Borivali West", "base_rent": 35000, "base_sqft": 500, "lat": 19.2288, "lon": 72.8441},
    {"name": "Goregaon East", "base_rent": 40000, "base_sqft": 550, "lat": 19.1646, "lon": 72.8665},
    {"name": "Juhu", "base_rent": 120000, "base_sqft": 900, "lat": 19.1075, "lon": 72.8263},
    {"name": "Malabar Hill", "base_rent": 150000, "base_sqft": 1000, "lat": 18.9500, "lon": 72.7950},
    {"name": "Chembur", "base_rent": 45000, "base_sqft": 600, "lat": 19.0522, "lon": 72.8995},
]

property_types = ["Apartment", "Independent House", "Villa", "Studio"]
furnishing_statuses = ["Fully Furnished", "Semi-Furnished", "Unfurnished"]

num_records = 5000
data = []
start_date = datetime(2023, 1, 1)

for i in range(num_records):
    loc = random.choice(localities)
    bhk = random.choices([1, 2, 3, 4, 5], weights=[0.3, 0.4, 0.2, 0.08, 0.02])[0]
    
    # Base area based on BHK and locality
    area = loc["base_sqft"] + (bhk - 1) * 300 + generate_normal(0, 50)
    
    # Calculate rent based on area, locality, bhk
    rent = (area / loc["base_sqft"]) * loc["base_rent"] + (bhk * 10000)
    
    prop_type = random.choices(property_types, weights=[0.9, 0.05, 0.01, 0.04])[0]
    if prop_type == "Studio":
        bhk = 1
        area = area * 0.6
        rent = rent * 0.7
        
    furnishing = random.choices(furnishing_statuses, weights=[0.4, 0.4, 0.2])[0]
    if furnishing == "Fully Furnished":
        rent *= 1.2
    elif furnishing == "Unfurnished":
        rent *= 0.85
        
    bathrooms = bhk if bhk <= 3 else bhk - 1
    if random.random() > 0.8: bathrooms += 1
    
    parking = random.choices([0, 1, 2], weights=[0.3, 0.6, 0.1])[0]
    floor = random.randint(1, 40)
    building_age = random.choices([random.randint(0, 5), random.randint(6, 15), random.randint(16, 30)], weights=[0.3, 0.5, 0.2])[0]
    
    # Add noise for realism
    rent = rent * random.uniform(0.9, 1.1)
    
    # Listing date
    listing_date = start_date + timedelta(days=random.randint(0, 365))
    
    # Add coordinates with slight jitter
    lat = loc["lat"] + random.uniform(-0.01, 0.01)
    lon = loc["lon"] + random.uniform(-0.01, 0.01)
    
    data.append({
        "id": i + 1,
        "locality": loc["name"],
        "monthly_rent": round(rent, -2),
        "property_type": prop_type,
        "bhk": bhk,
        "area_sqft": round(area, 2),
        "furnishing": furnishing,
        "bathrooms": bathrooms,
        "parking": parking,
        "floor": floor,
        "building_age": building_age,
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
        "listing_date": listing_date.strftime("%Y-%m-%d")
    })

# Inject dirty data
# 1. Missing values
for i in random.sample(range(num_records), 100):
    data[i]['monthly_rent'] = ""
for i in random.sample(range(num_records), 200):
    data[i]['building_age'] = ""
for i in random.sample(range(num_records), 150):
    data[i]['furnishing'] = ""

# 2. Inconsistent strings
for i in random.sample(range(num_records), 50):
    data[i]['locality'] = 'bandra west'
for i in random.sample(range(num_records), 50):
    data[i]['locality'] = 'Andheri W'
for i in random.sample(range(num_records), 50):
    data[i]['locality'] = 'S. Mumbai - Worli'

# 3. Incorrect numeric values
for i in random.sample(range(num_records), 10):
    data[i]['monthly_rent'] = -50000
for i in random.sample(range(num_records), 10):
    data[i]['area_sqft'] = -500

# 4. Outliers
for i in random.sample(range(num_records), 5):
    data[i]['monthly_rent'] = 5000000
for i in random.sample(range(num_records), 5):
    data[i]['area_sqft'] = 50000

# 5. Duplicates
duplicates = [data[i].copy() for i in random.sample(range(num_records), 100)]
data.extend(duplicates)

# Re-assign IDs to duplicates might make it too obvious, but let's keep original ID to show it's a true duplicate
# actually leaving same ID is fine for duplicate detection

keys = data[0].keys()
with open("mumbai_rentals_raw.csv", "w", newline="", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)

print(f"mumbai_rentals_raw.csv created successfully with {len(data)} records.")
