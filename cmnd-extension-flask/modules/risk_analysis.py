from models import InvestmentOptionsSchema
# from modules.filter_investment_options import filter_investment_options
from datetime import datetime
import numpy as np
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
# from data import rental_incomes, price_list_data

# Simulated data (replace with actual data retrieval)
available_projects_data = [
    {
        "projectID": 1,
        "projectName": "Project A",
        "propertyDeveloper": "Developer X",
        "location": "Nicosia",
        "purpose": "Residential",
        "description": "Lorem ipsum dolor sit amet.",
        "start_date": "2023-01-01",
        "completion_date": "2024-12-31",
        "facilities": ["Swimming Pool", "Gym"],
        "image_url": ["image1.jpg", "image2.jpg"],
        "no_of_installments": 12,
        "no_of_properties": 50,
        "property_types": [
            {
                "propertyID": "A001",
                "no_of_rooms": 3,
                "type": "Apartment",
                "total_area_sqmeter": 120,
                "no_of_bathrooms": 2,
                "price": 250000
            },
            {
                "propertyID": "A002",
                "no_of_rooms": 4,
                "type": "Villa",
                "total_area_sqmeter": 300,
                "no_of_bathrooms": 3,
                "price": 500000
            }
        ],
        "percentage_sold": 70
    },
    {
        "projectID": 2,
        "projectName": "Project B",
        "propertyDeveloper": "Developer Y",
        "location": "Kyrenia",
        "purpose": "Commercial",
        "description": "Lorem ipsum dolor sit amet.",
        "start_date": "2023-06-01",
        "completion_date": "2025-05-31",
        "facilities": ["Parking Area", "Conference Rooms"],
        "image_url": ["image3.jpg", "image4.jpg"],
        "no_of_installments": 24,
        "no_of_properties": 30,
        "property_types": [
            {
                "propertyID": "B001",
                "no_of_rooms": 10,
                "type": "Office Space",
                "total_area_sqmeter": 500,
                "no_of_bathrooms": 4,
                "price": 800000
            }
        ],
        "percentage_sold": 50
    }
]

price_list_data = {
    "A001": [
        {
            "No": 1,
            "apratment_type": "Apartment",
            "block": "A",
            "floor": 1,
            "interior_sqmeter": 100,
            "balcony_terrace_sqmeter": 20,
            "rooftop_sqmeter": 0,
            "total_living_space_sqmeter": 120,
            "payment_plan": {
                "start_date": "2023-08-01",
                "delivery_date": "2024-08-01",
                "price": 250000,
                "percentage_payment_amount": 30,
                "payment_amount": 75000,
                "installment_payment_plan": [
                    {
                        "percentage": "30%",
                        "plan": [
                            ("1", "August 2024", 1510)
                        ]
                    }
                ],
                "additional_fees": {
                    "property_price": 250000,
                    "VAT": 10000,
                    "stamp_duty": 5000,
                    "title_deed_transfer": 2000,
                    "lawyer_fees": 3000
                },
                "total_amount": 300000
            }
        }
    ],
    "A002": [
        {
            "No": 1,
            "apratment_type": "Villa",
            "block": "B",
            "floor": 2,
            "interior_sqmeter": 250,
            "balcony_terrace_sqmeter": 50,
            "rooftop_sqmeter": 20,
            "total_living_space_sqmeter": 320,
            "payment_plan": {
                "start_date": "2023-09-01",
                "delivery_date": "2024-09-01",
                "price": 500000,
                "percentage_payment_amount": 30,
                "payment_amount": 150000,
                "installment_payment_plan": [
                    {
                        "percentage": "30%",
                        "plan": [
                            ("1", "September 2024", 2510)
                        ]
                    }
                ],
                "additional_fees": {
                    "property_price": 500000,
                    "VAT": 20000,
                    "stamp_duty": 10000,
                    "title_deed_transfer": 4000,
                    "lawyer_fees": 6000
                },
                "total_amount": 600000
            }
        }
    ]
}

rental_income_data = {
    "A001": {
        "propertyID": "A001",
        "property": "Apartment A001",
        "pessimistic": {
            "scenario": "Pessimistic",
            "no_of_rental_days": 300,
            "average_daily_rate": 100,
            "gross_rental_income": 30000,
            "net_income": 25000,
            "unit_price": 250000,
            "annual_net_rental_yield": 10,
            "ROI": 5
        },
        "realistic": {
            "scenario": "Realistic",
            "no_of_rental_days": 330,
            "average_daily_rate": 120,
            "gross_rental_income": 39600,
            "net_income": 33600,
            "unit_price": 250000,
            "annual_net_rental_yield": 13.44,
            "ROI": 6.72
        },
        "optimistic": {
            "scenario": "Optimistic",
            "no_of_rental_days": 360,
            "average_daily_rate": 150,
            "gross_rental_income": 54000,
            "net_income": 46800,
            "unit_price": 250000,
            "annual_net_rental_yield": 18.72,
            "ROI": 9.36
        }
    },
    "A002": {
        "propertyID": "A002",
        "property": "Villa A002",
        "pessimistic": {
            "scenario": "Pessimistic",
            "no_of_rental_days": 280,
            "average_daily_rate": 200,
            "gross_rental_income": 56000,
            "net_income": 48000,
            "unit_price": 500000,
            "annual_net_rental_yield": 9.6,
            "ROI": 4.8
        },
        "realistic": {
            "scenario": "Realistic",
            "no_of_rental_days": 300,
            "average_daily_rate": 250,
            "gross_rental_income": 75000,
            "net_income": 65000,
            "unit_price": 500000,
            "annual_net_rental_yield": 13,
            "ROI": 6.5
        },
        "optimistic": {
            "scenario": "Optimistic",
            "no_of_rental_days": 330,
            "average_daily_rate": 300,
            "gross_rental_income": 99000,
            "net_income": 88000,
            "unit_price": 500000,
            "annual_net_rental_yield": 17.6,
            "ROI": 8.8
        }
    }
}

def filter_investment_options(parameters: InvestmentOptionsSchema):
    # try:
      #  projects_data = fetch_available_projects()
    # except Exception as e:
      #  raise Exception(f"Failed to fetch projects data: {e}")

    filtered_projects = []

    for project in available_projects_data:
        if parameters.location and project['location'] != parameters.location:
            continue
        for property in project['property_types']:
            if (property['price'] >= parameters.budget_min and
                property['price'] <= parameters.budget_max and
                (property['total_area_sqmeter'] >= parameters.size_min if parameters.size_min else True) and
                (property['total_area_sqmeter'] <= parameters.size_max if parameters.size_max else True) and
                (property['no_of_rooms'] >= parameters.bedrooms_min if parameters.bedrooms_min else True) and
                (property['no_of_rooms'] <= parameters.bedrooms_max if parameters.bedrooms_max else True) and
                (property['no_of_bathrooms'] >= parameters.bathrooms_min if parameters.bathrooms_min else True) and
                (property['no_of_bathrooms'] <= parameters.bathrooms_max if parameters.bathrooms_max else True) and
                (project['purpose'] == 'Residential' if parameters.family_size else True) and
                (property['type'] == parameters.property_type if parameters.property_type else True)):
                filtered_projects.append({
                    'projectID': project['projectID'],
                    'projectName': project['projectName'],
                    'propertyDeveloper': project['propertyDeveloper'],
                    'location': project['location'],
                    'purpose': project['purpose'],
                    'start_date': project['start_date'],
                    'completion_date': project['completion_date'],
                    'facilities': project['facilities'],
                    'no_of_installments': project['no_of_installments'],
                    'no_of_properties': project['no_of_properties'],
                    'percentage_sold': project['percentage_sold'],
                    'propertyID': property['propertyID'],
                    'no_of_rooms': property['no_of_rooms'],
                    'type': property['type'],
                    'total_area_sqmeter': property['total_area_sqmeter'],
                    'no_of_bathrooms': property['no_of_bathrooms'],
                    'price': property['price']
                })

    if not filtered_projects:
        return []

    if parameters.sort_by and parameters.sort_by in filtered_projects[0]:
        filtered_projects = sorted(filtered_projects, key=lambda x: x[parameters.sort_by])

    return filtered_projects

class RiskScorer:
    def __init__(self):
        pass

    def location_risk(self, location):
        risk_scores = {
            "All": 1.0,
            "Kyrenia": 0.2,
            "Iskele": 0.3,
            "Guzelyurt": 0.4,
            "Nicosia": 0.5,
            "Famagusta": 0.6,
            "Lefke": 0.7,
            "Karpaz Peninsula": 0.8
        }
        return risk_scores.get(location, 1.0)

    def price_risk(self, min_price, max_price):
        price_volatility = max_price - min_price
        return price_volatility / max_price

    def completion_sale_risk(self, percentage_sold, start_date, completion_date):
        days_to_completion = (datetime.strptime(completion_date, '%Y-%m-%d') - datetime.now()).days
        sale_risk = 1 - (percentage_sold / 100)
        return sale_risk + (days_to_completion / 365)

    def rental_income_risk(self, rental_income):
        pessimistic_yield = rental_income['pessimistic']['annual_net_rental_yield']
        optimistic_yield = rental_income['optimistic']['annual_net_rental_yield']
        return (optimistic_yield - pessimistic_yield) / optimistic_yield

    def financial_risk(self, payment_plan):
        total_amount = payment_plan['total_amount']
        additional_fees = sum(payment_plan['additional_fees'].values())
        return additional_fees / total_amount

    def developer_risk(self, developer_history):
        # Placeholder for developer risk scoring logic
        return 1.0

class RiskEvaluator:
    def __init__(self, scorer):
        self.scorer = scorer

    def evaluate_property(self, property_data):
        location_score = self.scorer.location_risk(property_data['location'])
        price_score = self.scorer.price_risk(property_data['min_price'], property_data['max_price'])
        completion_sale_score = self.scorer.completion_sale_risk(
            property_data['percentage_sold'], property_data['start_date'], property_data['completion_date']
        )
        rental_income_score = self.scorer.rental_income_risk(property_data['rental_income'])
        financial_score = self.scorer.financial_risk(property_data['payment_plan'])
        developer_score = self.scorer.developer_risk(property_data['developer_history'])

        risk_scores = {
            "location": location_score,
            "price": price_score,
            "completion_sale": completion_sale_score,
            "rental_income": rental_income_score,
            "financial": financial_score,
            "developer": developer_score
        }
        composite_score = np.mean(list(risk_scores.values()))
        return composite_score, risk_scores

class RiskReportGenerator:
    def generate_report(self, property_data, risk_score, risk_factors):
        report = {
            "property_id": property_data['propertyID'],
            "property_name": property_data['projectName'],
            "location": property_data['location'],
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "recommendations": self.generate_recommendations(risk_factors)
        }
        return report

    def generate_recommendations(self, risk_factors):
        recommendations = []
        if risk_factors['location'] > 0.5:
            recommendations.append("Consider alternative locations with lower risk.")
        if risk_factors['price'] > 0.5:
            recommendations.append("Evaluate price stability in the area.")
        if risk_factors['completion_sale'] > 0.5:
            recommendations.append("Check project completion and sales status.")
        if risk_factors['rental_income'] > 0.5:
            recommendations.append("Assess rental income stability.")
        if risk_factors['financial'] > 0.5:
            recommendations.append("Review payment plan and additional fees.")
        if risk_factors['developer'] > 0.5:
            recommendations.append("Investigate developer's track record.")
        return recommendations

scorer = RiskScorer()
evaluator = RiskEvaluator(scorer)
report_generator = RiskReportGenerator()

def fetch_price_list(property_id):
    # Simulated function to fetch price list data
    return price_list_data.get(property_id, [])

def fetch_rental_income(property_id):
    # Simulated function to fetch rental income data
    return rental_income_data.get(property_id, {})

def gather_property_details(property_id):
    price_list = fetch_price_list(property_id)
    rental_income = fetch_rental_income(property_id)

    details = []
    for price_info in price_list:
        payment_plan = price_info['payment_plan']
        details.append({
            'Apartment Type': price_info['apratment_type'],
            'Block': price_info['block'],
            'Floor': price_info['floor'],
            'Interior Area (sqm)': price_info['interior_sqmeter'],
            'Balcony/Terrace Area (sqm)': price_info['balcony_terrace_sqmeter'],
            'Rooftop Area (sqm)': price_info['rooftop_sqmeter'],
            'Total Living Space (sqm)': price_info['total_living_space_sqmeter'],
            'Price': payment_plan['price'],
            'Payment Plan Start Date': payment_plan['start_date'],
            'Payment Plan Delivery Date': payment_plan['delivery_date'],
            'Installment Payment Plan': payment_plan['installment_payment_plan'],
            'Additional Fees': payment_plan['additional_fees'],
            'Total Amount': payment_plan['total_amount']
        })

    return details

def run_risk_analysis_module(**kwargs):
    parameters = InvestmentOptionsSchema(**kwargs)
    filtered_projects = filter_investment_options(parameters)
    property_details = []
    
    for item in filtered_projects:
        projectID = item['projectID']
        property_id = item['propertyID']
        property_data = {
            "propertyID": property_id,
            "projectName": item['projectName'],
            "propertyDeveloper": item['propertyDeveloper'],
            "location": item['location'],
            "purpose": item['purpose'],
            "completion_date": item['completion_date'],
            "facilities": item['facilities'],
            "min_price": item['price'],
            "max_price": item['price'],  
            "percentage_sold": item['percentage_sold'],
            "start_date": item['start_date'],
            "rental_income": rental_income_data.get(property_id, {}),
            "payment_plan": price_list_data.get(property_id, [{}])[0]['payment_plan'],
            "developer_history": {}  # Placeholder for developer history
        }
        risk_score, risk_factors = evaluator.evaluate_property(property_data)
        report = report_generator.generate_report(property_data, risk_score, risk_factors)
        property_details.append({
            'Project Name': item['projectName'],
            'Property Developer': item['propertyDeveloper'],
            'Location': item['location'],
            'Purpose': item['purpose'],
            'Completion Date': item['completion_date'],
            'Facilities': ", ".join(item['facilities']),
            'Property Type': item['type'],
            'Risk Report': report
        })

    return {"risk_analysis": property_details}

# Example usage:
kwargs = {
    "location": "Nicosia",
    "budget_min": 200000,
    "budget_max": 600000,
    "purpose": "Residential"
}

result = run_risk_analysis_module(**kwargs)
# print(result)