from models import InvestmentOptionsSchema
from modules.filter_investment_options import filter_investment_options
import pandas as pd


def print_comparison_table(properties):
    if not properties:
        print("No properties found matching the criteria.")
        return
    
    df = pd.DataFrame(properties)
    print("Property Comparison Table:")
    print(df.to_string(index=False))

def run_cost_comparison_module(**props):
    try:
        parameters = InvestmentOptionsSchema(**props)
    except Exception as e:
        return {"error": str(e)}

    filtered_properties = filter_investment_options(parameters)
    if not filtered_properties:
        return {"message": "No properties found matching the criteria."}
    
    # Print for testing
    # print_comparison_table(filtered_properties)
    return {"properties": filtered_properties}
