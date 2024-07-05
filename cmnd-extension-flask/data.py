from faker import Faker
import random

fake = Faker()

# Define options
purposes = ["All", "For Relocation", "For Max Rental ROI", "For Buy-Sell Investment"]
prices = [80000, 100000, 120000, 140000, 160000, 180000, 200000, 220000, 240000, 260000, 
          280000, 300000, 350000, 400000, 450000, 500000, 1000000]
locations = ["All", "Kyrenia", "Iskele", "Guzelyurt", "Nicosia", "Famagusta", "Lefke", "Karpaz Peninsula"]

def generate_project():
    project_id = random.randint(1, 100)
    project_name = fake.company()
    property_developer = fake.company()
    location = random.choice(locations)
    purpose = random.choice(purposes)
    description = fake.text()
    start_date = fake.date_between(start_date='-2y', end_date='-1y')
    completion_date = fake.date_between(start_date='now', end_date='+2y')
    facilities = [fake.word() for _ in range(random.randint(1, 5))]
    image_urls = [fake.image_url() for _ in range(random.randint(1, 3))]
    no_of_installments = random.randint(6, 24)
    no_of_properties = random.randint(10, 100)
    property_types = generate_property_types()
    percentage_sold = random.randint(0, 100)
    
    return {
        "projectID": project_id,
        "projectName": project_name,
        "propertyDeveloper": property_developer,
        "location": location,
        "purpose": purpose,
        "description": description,
        "start_date": start_date,
        "completion_date": completion_date,
        "facilities": facilities,
        "image_url": image_urls,
        "no_of_installments": no_of_installments,
        "no_of_properties": no_of_properties,
        "property_types": property_types,
        "percentage_sold": percentage_sold
    }

def generate_property_types():
    property_types = []
    for _ in range(random.randint(1, 3)):
        property_id = random.randint(100, 999)
        no_of_rooms = random.randint(1, 5)
        property_type = random.choice(["apartment", "house", "villa"])
        total_area_sqmeter = random.randint(100, 300)
        no_of_bathrooms = random.randint(1, 3)
        price = random.choice(prices)
        
        property_types.append({
            "propertyID": property_id,
            "no_of_rooms": no_of_rooms,
            "type": property_type,
            "total_area_sqmeter": total_area_sqmeter,
            "no_of_bathrooms": no_of_bathrooms,
            "price": price
        })
    
    return property_types

# Generate dummy data for 20 projects
projects_data = [generate_project() for _ in range(20)]

# print(projects_data)
