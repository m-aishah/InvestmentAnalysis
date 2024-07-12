from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import pandas as pd
from dummy_data import rental_income_data, price_list_data, projects_data
from models import InvestmentOptionsSchema
from modules.filter_investment_options import filter_investment_options

def format_property_data(project, property_data, rental_income_data, price_list_data):
    property_id = property_data['propertyID']
    price_data = price_list_data.get(property_id, [])
    rental_data = rental_income_data.get(property_id, {})
    
    # Extracting price data
    total_price = property_data['price']
    additional_fees = property_data['payment_plan']['additional_fees']
    total_cost_including_fees = total_price + sum(additional_fees.values())
    
    # Extracting rental income data (using 'realistic' scenario)
    rental_data_realistic = rental_data.get('realistic', {})
    gross_rental_yield = rental_data_realistic.get('annual_net_rental_yield', 0)
    net_rental_yield = rental_data_realistic.get('ROI', 0)
    
    # Constructing formatted data
    formatted_data = {
        "Metric": "Cost Comparison",
        f"Project Name - {project['projectName']} - Property {property_data['propertyID']}": f"{project['projectName']} - {property_data['propertyID']}",
        f"Property Type - {project['projectName']} - {property_data['type']}": property_data['type'],
        f"Location - {project['projectName']} - {property_data['location']}": project['location'],
        f"Price per Square Meter - {project['projectName']} - {property_data['type']}": f"€{property_data['price'] / property_data['total_area_sqmeter']:.0f}",
        f"Total Price - {project['projectName']} - {property_data['type']}": f"€{total_price:,}",
        f"Additional Fees - {project['projectName']} - {property_data['type']}": f"€{sum(additional_fees.values()):,}",
        f"Total Cost Including Fees - {project['projectName']} - {property_data['type']}": f"€{total_cost_including_fees:,}",
        f"Price to Income Ratio - {project['projectName']} - {property_data['type']}": f"{gross_rental_yield:.2f}",
        f"Mortgage as Percentage of Income - {project['projectName']} - {property_data['type']}": f"{net_rental_yield:.2f}%",
        f"Loan Affordability Index - {project['projectName']} - {property_data['type']}": f"{total_price / net_rental_yield:.2f}",
        f"Gross Rental Yield - {project['projectName']} - {property_data['type']}": f"{gross_rental_yield:.2f}%",
        f"Net Rental Yield - {project['projectName']} - {property_data['type']}": f"{net_rental_yield:.2f}%",
        f"ROI - {project['projectName']} - {property_data['type']}": f"{rental_data_realistic.get('ROI', 0)}%",
        f"Total Area (sqm) - {project['projectName']} - {property_data['type']}": property_data['total_area_sqmeter'],
        f"Number of Rooms - {project['projectName']} - {property_data['type']}": f"{property_data['no_of_rooms']} bedrooms, {property_data['no_of_bathrooms']} bathrooms",
        f"Facilities and Amenities - {project['projectName']} - {property_data['type']}": ', '.join(project['facilities']),
        f"Estimated Completion Date - {project['projectName']} - {property_data['type']}": project['completion_date'],
        f"Developer Track Record - {project['projectName']} - {property_data['type']}": "Excellent" if project['percentage_sold'] >= 70 else "Good"
    }
    
    return formatted_data

def run_cost_comparison_module(**props):
    try:
        parameters = InvestmentOptionsSchema(**props)
        
    except Exception as e:
        return {"error": str(e)}

    filtered_projects = filter_investment_options(parameters)
    if not filtered_projects:
        return {"message": "No properties found matching the criteria."}
    
    comparison_data = []
    for project in filtered_projects:
        specific_project = [proj for proj in projects_data if project['projectID'] == proj["projectID"]]
        formatted_data = format_property_data(project, specific_project[0], rental_income_data, price_list_data)
        comparison_data.append(formatted_data)
    

    return {"properties": comparison_data}
