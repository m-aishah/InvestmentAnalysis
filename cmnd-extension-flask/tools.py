import os
import pandas as pd
from pydantic import BaseModel, Field

# Placeholder data (replace with actual data source later)
property_data = {
    "id": [1, 2, 3],
    "price": [250000, 300000, 200000],
    "location": ["City A", "City B", "City A"],
    "size": [1500, 1800, 1200],
    "features": [["3 bedrooms", "2 bathrooms"], ["4 bedrooms", "2.5 bathrooms"], ["2 bedrooms", "1 bathroom"]]
}
# Create a pandas DataFrame
df_properties = pd.DataFrame(property_data)

class InvestmentOptionsSchema(BaseModel):
    budget_min: int = Field(..., title="Minimum Budget", description="Minimum budget for property investment")
    budget_max: int = Field(..., title="Maximum Budget", description="Maximum budget for property investment")
    location: str = Field(..., title="Location", description="Location preference for property investment")

def filter_investment_options(parameters):
    budget_min = parameters.budget_min
    budget_max = parameters.budget_max
    location = parameters.location
    filtered_properties = df_properties[(df_properties['price'] >= budget_min) & 
                                         (df_properties['price'] <= budget_max) & 
                                         (df_properties['location'] == location)]
    return filtered_properties.to_dict(orient='records')

def display_comparison_table(properties):
    if len(properties) == 0:
        return "No properties found matching the criteria."
    
    comparison_table = "Property Comparison Table:\n"
    comparison_table += "{:<5} {:<10} {:<15} {:<10}\n".format("ID", "Price", "Location", "Size")
    comparison_table += "-" * 40 + "\n"
    
    for property in properties:
        comparison_table += "{:<5} ${:<10,.2f} {:<15} {:<10} sqft\n".format(property['id'], property['price'], property['location'], property['size'])
    
    return comparison_table

# Cost Comparison:
def run_cost_comparison_module(parameters):
    filtered_properties = filter_investment_options(parameters)
    comparison_table = display_comparison_table(filtered_properties)
    return comparison_table

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