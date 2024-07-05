import pandas as pd
from pydantic import BaseModel, Field
from flask import Flask, request, jsonify, abort
from typing import Optional, List, Dict
from data import projects_data

class InvestmentOptionsSchema(BaseModel):
    budget_min: int = Field(0, title="Minimum Budget", description="Minimum budget for property investment")
    budget_max: int = Field(..., title="Maximum Budget", description="Maximum budget for property investment")
    location: Optional[str] = Field(None, title="Location", description="Location preference for property investment")
    size_min: Optional[int] = Field(0, title="Minimum Size", description="Minimum property size in square meters", ge=0)
    size_max: Optional[int] = Field(None, title="Maximum Size", description="Maximum property size in square meters")
    bedrooms_min: Optional[int] = Field(0, title="Minimum Bedrooms", description="Minimum number of bedrooms", ge=0)
    bedrooms_max: Optional[int] = Field(None, title="Maximum Bedrooms", description="Maximum number of bedrooms")
    bathrooms_min: Optional[float] = Field(0, title="Minimum Bathrooms", description="Minimum number of bathrooms", ge=0)
    bathrooms_max: Optional[float] = Field(None, title="Maximum Bathrooms", description="Maximum number of bathrooms")
    family_size: Optional[int] = Field(None, title="Family Size", description="Number of family members")
    property_type: Optional[str] = Field(None, title="Property Type", description="Type of property (e.g., house, apartment)")
    sort_by: Optional[str] = Field(None, title="Sort By", description="Sort the results by a specific field (e.g., price, size)")

def filter_investment_options(parameters):
    filtered_projects = []
    
    for project in projects_data:
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

def print_comparison_table(properties):
    if len(properties) == 0:
        print("No properties found matching the criteria.")
        return
    
    comparison_table = "Property Comparison Table:\n"
    comparison_table += "{:<5} {:<20} {:<20} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<15} {:<20}\n".format(
        "ID", "Project Name", "Developer", "Location", "Price", "Size", "Beds", "Baths", "Type", "Facilities", "Completion Date")
    comparison_table += "-" * 150 + "\n"
    
    for property in properties:
        facilities = ", ".join(property['facilities'])
        comparison_table += "{:<5} {:<20} {:<20} {:<10} ${:<10,.2f} {:<10} {:<10} {:<10} {:<10} {:<15} {:<20}\n".format(
            property['propertyID'], property['projectName'], property['propertyDeveloper'], property['location'],
            property['price'], property['total_area_sqmeter'], property['no_of_rooms'], property['no_of_bathrooms'], 
            property['type'], facilities, property['completion_date'])
    
    print(comparison_table)

# Cost Comparison:
def run_cost_comparison_module(**props):
    parameters = InvestmentOptionsSchema(**props)
    filtered_properties = filter_investment_options(parameters)
    if not filtered_properties:
        return {"message": "No properties found matching the criteria."}
    
    # Print the comparison table for debugging
    print_comparison_table(filtered_properties)
    
    # Return structured data
    return {"properties": filtered_properties}



# FUTURE PROJECTIONS
def calculate_expected_return_per_sqm():
    # Placeholder function for calculating expected return per square meter
    return 100  # Placeholder value

def estimate_potential_revenue():
    # Placeholder function for estimating potential revenue over 3-5 years
    return 500000  # Placeholder value

# Example usage:
def run_future_projections_module():
    expected_return_per_sqm = calculate_expected_return_per_sqm()
    potential_revenue = estimate_potential_revenue()
    return {
        "expected_return_per_sqm": expected_return_per_sqm,
        "potential_revenue": potential_revenue
    }

# INVESTMENT RECOMMENDATIONS
def analyze_investment_opportunities(properties):
    # Placeholder function for analyzing investment opportunities
    recommendations = []
    for property in properties:
        recommendation = {
            "property_id": property['id'],
            "recommendation": "Good investment opportunity",
            "pros": ["High ROI", "Low risk"],
            "cons": ["High initial cost"]
        }
        recommendations.append(recommendation)
    return recommendations

# Example usage:
def run_investment_recommendations_module(properties):
    recommendations = analyze_investment_opportunities(properties)
    return recommendations


def custom_json_schema(model):
    schema = model.schema()
    properties_formatted = {
        k: {
            "title": v.get("title"),
            "type": v.get("type")
        } for k, v in schema["properties"].items()
    }

    return {
        "type": "object",
        "default": {},
        "properties": properties_formatted,
        "required": schema.get("required", [])
    }

# Define the tool configuration and metadata for CMND.ai
tools = [
    {
        "name": "cost_comparison_module",
        "description": "Filters and compares investment options based on user-defined criteria & Costs",
        "parameters": custom_json_schema(InvestmentOptionsSchema),
        "runCmd": run_cost_comparison_module,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },

    {
        "name": "future_projections_module",
        "description": "Calculates expected return and potential revenue for investment options",
        "parameters": None,
        "runCmd": run_future_projections_module,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": False
    },

    {
        "name": "investment_recommendations_module",
        "description": "Provides investment recommendations based on predefined criteria",
        "parameters": None,  # No parameters needed for this module
        "runCmd": run_investment_recommendations_module,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": False
    }    
]