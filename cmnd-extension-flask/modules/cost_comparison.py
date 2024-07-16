from typing import List, Dict
from dummy_data import rental_income_data, price_list_data, projects_data
from models import InvestmentOptionsSchema
from modules.filter_investment_options import filter_investment_options

def format_property_data(property, rental_income, price_list):
        
    
    # Extracting price data
    project_name = property['projectName']
    property_type = property['type']
    total_price = property['price']
    additional_fees = price_list['payment_plan']['additional_fees']
    total_cost_including_fees = total_price + sum(additional_fees.values())
    
    # Extracting rental income data (using 'realistic' scenario)
    rental_data_realistic = rental_income.get('realistic', {})
    gross_rental_yield = rental_data_realistic.get('annual_net_rental_yield', 0)
    net_rental_yield = rental_data_realistic.get('ROI', 0)
    
    # Constructing formatted data
    
    formatted_data = {
        "Metric": "Cost Comparison",
        f"Project Name - {project_name} - Property {property['propertyID']}": f"{project_name} - {property['propertyID']}",
        f"Property Type - {project_name} - {property_type}": property_type,
        f"Location - {project_name} - {property['location']}": property['location'],
        f"Price per Square Meter - {project_name} - {property_type}": f"€{property['price'] / property['total_area_sqmeter']:.0f}",
        f"Total Price - {project_name} - {property_type}": f"€{total_price:,}",
        f"Additional Fees - {project_name} - {property_type}": f"€{sum(additional_fees.values()):,}",
        f"Total Cost Including Fees - {project_name} - {property_type}": f"€{total_cost_including_fees:,}",
        f"Price to Income Ratio - {project_name} - {property_type}": f"{gross_rental_yield:.2f}",
        f"Mortgage as Percentage of Income - {project_name} - {property_type}": f"{net_rental_yield:.2f}%",
        f"Loan Affordability Index - {project_name} - {property_type}": f"{total_price / net_rental_yield:.2f}",
        f"Gross Rental Yield - {project_name} - {property_type}": f"{gross_rental_yield:.2f}%",
        f"Net Rental Yield - {project_name} - {property_type}": f"{net_rental_yield:.2f}%",
        f"ROI - {project_name} - {property_type}": f"{rental_data_realistic.get('ROI', 0)}%",
        f"Total Area (sqm) - {project_name} - {property_type}": property['total_area_sqmeter'],
        f"Number of Rooms - {project_name} - {property_type}": f"{property['no_of_rooms']} bedrooms, {property['no_of_bathrooms']} bathrooms",
        f"Facilities and Amenities - {project_name} - {property_type}": ', '.join(property['facilities']),
        f"Estimated Completion Date - {project_name} - {property_type}": property['completion_date'],
        f"Developer Track Record - {project_name} - {property_type}": "Excellent" if property['percentage_sold'] >= 70 else "Good"
    }
    
    return formatted_data

def run_cost_comparison_module(**props):
    try:
        parameters = InvestmentOptionsSchema(**props)
        
    except Exception as e:
        return {"error": str(e)}

    properties = filter_investment_options(parameters)
    if not properties:
        return {"message": "No properties found matching the criteria."}
    
    comparison_data = []
    for property in properties:
        property_id = property['propertyID']
        price_list = price_list_data.get(property_id, None)[0] if price_list_data.get(property_id, None) else None
        rental_income = rental_income_data.get(property_id, None)
        if price_list and rental_income:
            formatted_data = format_property_data(property, rental_income, price_list)
        comparison_data.append(formatted_data)
    return {"properties": comparison_data}
