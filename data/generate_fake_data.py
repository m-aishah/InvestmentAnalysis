from faker import Faker
import random

fake = Faker()

# Define options
purposes = ["All", "For Relocation", "For Max Rental ROI", "For Buy-Sell Investment"]
prices = [80000, 100000, 120000, 140000, 160000, 180000, 200000, 220000, 240000, 260000, 
          280000, 300000, 350000, 400000, 450000, 500000, 1000000]
locations = ["All", "Kyrenia", "Iskele", "Guzelyurt", "Nicosia", "Famagusta", "Lefke", "Karpaz Peninsula"]

# Function to generate property types
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

# Function to generate projects
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

# Generate dummy data for projects
projects_data = [generate_project() for _ in range(20)]

# Function to generate price list
def generate_price_list(property_id):
    return [
        {
            "No": i,
            "apratment_type": fake.word(),
            "block": fake.random_letter().upper(),
            "floor": random.randint(1, 20),
            "interior_sqmeter": random.randint(50, 150),
            "balcony_terrace_sqmeter": random.randint(10, 50),
            "rooftop_sqmeter": random.randint(0, 100),
            "total_living_space_sqmeter": random.randint(60, 250),
            "payment_plan": {
                "start_date": fake.date_between(start_date='now', end_date='+1y'),
                "delivery_date": fake.date_between(start_date='+1y', end_date='+2y'),
                "price": random.choice(prices),
                "percentage_payment_amount": random.randint(10, 50),
                "payment_amount": random.randint(10000, 50000),
                "installment_payment_plan": [
                    {
                        "percentage": random.randint(1, 20),
                        "plan": [(str(i), fake.date_between(start_date='now', end_date='+1y'), random.randint(1000, 5000)) for i in range(1, random.randint(2, 6))]
                    } for _ in range(random.randint(1, 3))
                ],
                "additional_fees": {
                    "property_price": random.randint(10000, 50000),
                    "VAT": random.randint(1000, 5000),
                    "stamp_duty": random.randint(500, 2000),
                    "title_deed_transfer": random.randint(1000, 5000),
                    "lawyer_fees": random.randint(1000, 5000)
                },
                "total_amount": random.randint(100000, 500000)
            }
        } for i in range(random.randint(1, 5))
    ]

# Generate dummy data for price lists
price_list_data = {property['propertyID']: generate_price_list(property['propertyID']) for project in projects_data for property in project['property_types']}

# Function to generate rental income
def generate_rental_income(property_id):
    scenarios = ["pessimistic", "realistic", "optimistic"]
    return {
        "propertyID": property_id,
        "property": fake.address(),
        "pessimistic": {
            "scenario": "pessimistic",
            "no_of_rental_days": random.randint(50, 365),
            "average_daily_rate": random.randint(50, 200),
            "gross_rental_income": random.randint(10000, 50000),
            "net_income": random.randint(5000, 25000),
            "unit_price": random.randint(100000, 500000),
            "annual_net_rental_yield": round(random.uniform(1, 10), 2),
            "ROI": round(random.uniform(1, 15), 2)
        },
        "realistic": {
            "scenario": "realistic",
            "no_of_rental_days": random.randint(50, 365),
            "average_daily_rate": random.randint(50, 200),
            "gross_rental_income": random.randint(10000, 50000),
            "net_income": random.randint(5000, 25000),
            "unit_price": random.randint(100000, 500000),
            "annual_net_rental_yield": round(random.uniform(1, 10), 2),
            "ROI": round(random.uniform(1, 15), 2)
        },
        "optimistic": {
            "scenario": "optimistic",
            "no_of_rental_days": random.randint(50, 365),
            "average_daily_rate": random.randint(50, 200),
            "gross_rental_income": random.randint(10000, 50000),
            "net_income": random.randint(5000, 25000),
            "unit_price": random.randint(100000, 500000),
            "annual_net_rental_yield": round(random.uniform(1, 10), 2),
            "ROI": round(random.uniform(1, 15), 2)
        }
    }

# Generate dummy data for rental incomes
rental_incomes = {property['propertyID']: generate_rental_income(property['propertyID']) for project in projects_data for property in project['property_types']}

# Example usage
if __name__ == "__main__":
    print("Projects Data:")
    print(projects_data)
    
    print("\nPrice List Data:")
    for property_id, price_list in price_list_data.items():
        print(f"Property ID {property_id}:")
        print(price_list)
        
    print("\nRental Income Data:")
    for property_id, rental_income in rental_incomes.items():
        print(f"Property ID {property_id}:")
        print(rental_income)
