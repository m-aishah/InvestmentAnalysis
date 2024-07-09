from faker import Faker
import random

fake = Faker()

# Define options
purposes = ["All", "For Relocation", "For Max Rental ROI", "For Buy-Sell Investment"]
prices = [80000, 100000, 120000, 140000, 160000, 180000, 200000, 220000, 240000, 260000, 
          280000, 300000, 350000, 400000, 450000, 500000, 1000000]
locations = ["All", "Kyrenia", "Iskele", "Guzelyurt", "Nicosia", "Famagusta", "Lefke", "Karpaz Peninsula"]

# Function to generate a price list for a property
def generate_price_list(property_id):
    num_entries = random.randint(1, 5)
    price_list = []
    for i in range(num_entries):
        start_date = fake.date_between(start_date='-1y', end_date='now')
        delivery_date = fake.date_between(start_date='now', end_date='+2y')
        price = random.choice(prices)
        installment_payment_plan = [
            {
                "percentage": random.uniform(1, 100),
                "plan": [(f"{i+1}", fake.date_between(start_date='now', end_date='+2y').strftime("%B %Y"), random.randint(1000, 5000))]
            }
            for i in range(random.randint(1, 5))
        ]
        additional_fees = {
            "property_price": price,
            "VAT": price * 0.18,
            "stamp_duty": price * 0.01,
            "title_deed_transfer": price * 0.03,
            "lawyer_fees": random.randint(1000, 5000)
        }
        total_amount = price + sum(additional_fees.values())
        
        price_list.append({
            "No": i + 1,
            "apratment_type": random.choice(["1+1", "2+1", "3+1"]),
            "block": random.choice(["A", "B", "C"]),
            "floor": random.randint(1, 10),
            "interior_sqmeter": random.uniform(50, 150),
            "balcony_terrace_sqmeter": random.uniform(5, 50),
            "rooftop_sqmeter": random.uniform(10, 100),
            "total_living_space_sqmeter": random.uniform(60, 200),
            "payment_plan": {
                "start_date": start_date,
                "delivery_date": delivery_date,
                "price": price,
                "percentage_payment_amount": random.uniform(1, 100),
                "payment_amount": random.randint(1000, 5000),
                "installment_payment_plan": installment_payment_plan,
                "additional_fees": additional_fees,
                "total_amount": total_amount
            }
        })
    return price_list

# Function to generate property types with associated price list
def generate_property_types():
    property_types = []
    price_lists = {}
    for _ in range(random.randint(1, 3)):
        property_id = random.randint(100, 999)
        no_of_rooms = random.randint(1, 5)
        property_type = random.choice(["apartment", "house", "villa"])
        total_area_sqmeter = random.randint(100, 300)
        no_of_bathrooms = random.randint(1, 3)
        price = random.choice(prices)
        
        property = {
            "propertyID": property_id,
            "no_of_rooms": no_of_rooms,
            "type": property_type,
            "total_area_sqmeter": total_area_sqmeter,
            "no_of_bathrooms": no_of_bathrooms,
            "price": price
        }
        
        property_types.append(property)
        price_lists[property_id] = generate_price_list(property_id)
    
    return property_types, price_lists

# Function to generate a project
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
    property_types, price_lists = generate_property_types()
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
    }, price_lists

# Generate dummy data for 20 projects
projects_data = []
price_list_data = {}

for _ in range(20):
    project, price_lists = generate_project()
    projects_data.append(project)
    price_list_data.update(price_lists)

# Example usage
if __name__ == "__main__":
    for project in projects_data:
        print(project)
    
    for property_id, price_list in price_list_data.items():
        print(f"Property ID: {property_id}")
        for price in price_list:
            print(price)
