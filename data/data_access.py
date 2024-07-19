from flask import Flask, jsonify, request
from faker import Faker
import random

app = Flask(__name__)
fake = Faker()

# Simulated data (replace with actual data retrieval)
from faker import Faker
fake = Faker()

projects_data = [
    {
        "projectID": i,
        "projectName": f"Project {chr(65 + i)}",
        "propertyDeveloper": fake.company(),
        "location": fake.random_element(["Kyrenia", "Iskele", "Guzelyurt", "Nicosia", "Famagusta", "Lefke", "Karpaz Peninsula"]),
        "purpose": fake.random_element(["For Relocation", "For Max Rental ROI", "For Buy-Sell Investment"]),
        "description": fake.text(),
        "start_date": fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d'),
        "completion_date": fake.date_between(start_date='today', end_date='+2y').strftime('%Y-%m-%d'),
        "facilities": [fake.word().title(), fake.word().title(), fake.word().title()],
        "image_url": [fake.image_url(), fake.image_url()],
        "no_of_installments": fake.random_int(min=6, max=36),
        "no_of_properties": fake.random_int(min=10, max=100),
        "property_types": [
            {
                "propertyID": f"{chr(65 + i)}{j:03}",
                "no_of_rooms": fake.random_int(min=1, max=5),
                "type": fake.random_element(["Apartment", "Villa", "Office Space", "Penthouse"]),
                "total_area_sqmeter": fake.random_int(min=50, max=500),
                "no_of_bathrooms": fake.random_int(min=1, max=5),
                "price": fake.random_element([80000, 100000, 120000, 140000, 160000, 180000, 200000, 220000, 240000, 260000, 280000, 300000, 350000, 400000, 450000, 500000, 1000000])
            } for j in range(fake.random_int(min=1, max=10))
        ],
        "percentage_sold": fake.random_int(min=0, max=100)
    } for i in range(20)
]

price_list_data = {
    property_type['propertyID']: [
        {
            "No": 1,
            "apratment_type": property_type['type'],
            "block": fake.random_element(["A", "B", "C"]),
            "floor": fake.random_int(min=1, max=10),
            "interior_sqmeter": property_type['total_area_sqmeter'],
            "balcony_terrace_sqmeter": fake.random_int(min=0, max=50),
            "rooftop_sqmeter": fake.random_int(min=0, max=50),
            "total_living_space_sqmeter": property_type['total_area_sqmeter'] + fake.random_int(min=0, max=100),
            "payment_plan": {
                "start_date": fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
                "delivery_date": fake.date_between(start_date='today', end_date='+1y').strftime('%Y-%m-%d'),
                "price": property_type['price'],
                "percentage_payment_amount": fake.random_element([10, 20, 30, 40]),
                "payment_amount": property_type['price'] * 0.3,
                "installment_payment_plan": [
                    {
                        "percentage": f"{fake.random_element([10, 20, 30, 40])}%",
                        "plan": [
                            (str(i), fake.date_this_year().strftime('%B %Y'), fake.random_int(min=1000, max=5000)) for i in range(1, fake.random_int(min=6, max=24))
                        ]
                    }
                ],
                "additional_fees": {
                    "property_price": property_type['price'],
                    "VAT": property_type['price'] * 0.04,
                    "stamp_duty": property_type['price'] * 0.02,
                    "title_deed_transfer": property_type['price'] * 0.008,
                    "lawyer_fees": property_type['price'] * 0.012
                },
                "total_amount": property_type['price'] * 1.06  # Including all fees
            }
        }
    ] for project in projects_data for property_type in project['property_types']
}

rental_income_data = {
    property_type['propertyID']: {
        "propertyID": property_type['propertyID'],
        "property": f"{property_type['type']} {property_type['propertyID']}",
        "pessimistic": {
            "scenario": "Pessimistic",
            "no_of_rental_days": fake.random_int(min=200, max=300),
            "average_daily_rate": fake.random_int(min=50, max=200),
            "gross_rental_income": fake.random_int(min=10000, max=50000),
            "net_income": fake.random_int(min=8000, max=45000),
            "unit_price": property_type['price'],
            "annual_net_rental_yield": fake.random_int(min=5, max=15),
            "ROI": fake.random_int(min=3, max=10)
        },
        "realistic": {
            "scenario": "Realistic",
            "no_of_rental_days": fake.random_int(min=250, max=330),
            "average_daily_rate": fake.random_int(min=70, max=250),
            "gross_rental_income": fake.random_int(min=20000, max=60000),
            "net_income": fake.random_int(min=16000, max=55000),
            "unit_price": property_type['price'],
            "annual_net_rental_yield": fake.random_int(min=7, max=18),
            "ROI": fake.random_int(min=4, max=12)
        },
        "optimistic": {
            "scenario": "Optimistic",
            "no_of_rental_days": fake.random_int(min=300, max=360),
            "average_daily_rate": fake.random_int(min=100, max=300),
            "gross_rental_income": fake.random_int(min=30000, max=80000),
            "net_income": fake.random_int(min=24000, max=75000),
            "unit_price": property_type['price'],
            "annual_net_rental_yield": fake.random_int(min=10, max=20),
            "ROI": fake.random_int(min=5, max=15)
        }
    } for project in projects_data for property_type in project['property_types']
}

# Endpoint to get available projects
@app.route('/projects/available_projects', methods=['GET'])
def get_available_projects():
    location = request.args.get('location')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    purpose = request.args.get('purpose')
    
    # Filter projects based on query parameters
    filtered_projects = [
        project for project in projects_data
        if (location is None or project['location'] == location) and
           (min_price is None or any(pt['price'] >= min_price for pt in project['property_types'])) and
           (max_price is None or any(pt['price'] <= max_price for pt in project['property_types'])) and
           (purpose is None or project['purpose'] == purpose)
    ]
    
    return jsonify(filtered_projects)

# Endpoint to get price list of a specific property
@app.route('/projects/available_projects/<propertyID>/price_list', methods=['GET'])
def get_price_list(propertyID):
    price_list = price_list_data.get(propertyID, [])
    return jsonify(price_list)

# Endpoint to get rental income of a specific property
@app.route('/projects/available_projects/<propertyID>/rental_income', methods=['GET'])
def get_rental_income(propertyID):
    rental_income = rental_income_data.get(propertyID, {})
    return jsonify(rental_income)

if __name__ == '__main__':
    app.run(debug=True)