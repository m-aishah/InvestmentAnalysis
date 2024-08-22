from src.models import InvestmentOptionsSchema
from src.modules.filter_investment_options import filter_investment_options
from src.modules.access_data import fetch_rental_income

def run_rental_income_forecast(**kwargs):
    """
    Run a rental income forecast based on the provided investment criteria.

    Args:
        **kwargs: Key-value arguments representing the investment criteria,
        which will be used to filter properties.
        These criteria include location, budget range, property size, number of rooms, etc.

    Returns:
        Dict: A dictionary containing the rental income forecast for properties that match the criteria
        Each entry includes property details and rental income forecasts
        for optimistic, pessimistic, and realistic scenarios.
        If no properties are found, the result will indicate that no properties matched the criteria.
    """
    
    parameters = InvestmentOptionsSchema(**kwargs)
    filtered_projects = filter_investment_options(parameters)
    forecast = []
    
    for project in filtered_projects:
        property_id = project['propertyID']
        try:
            rental_income = fetch_rental_income(property_id)
        except Exception as e:
            rental_income = None
            print(f"Error fetching rental income for property ID {property_id}: {e}")
        
        if rental_income:
            forecast.append({
                "propertyID": property_id,
                "projectName": project['projectName'],
                "propertyDeveloper": project['propertyDeveloper'],
                "location": project['location'],
                "purpose": project['purpose'],
                "description": project['description'],
                "rental_income": {
                    'optimistic': rental_income['optimistic'],
                    'pessimistic': rental_income['pessimistic'],
                    'realistic': rental_income['realistic']
                }
            })

    result = {"rental_income_forecast": forecast if len(forecast) > 0 else 'No property found with the given criteria.'}
    return result
