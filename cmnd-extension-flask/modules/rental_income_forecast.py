from models import InvestmentOptionsSchema
from filter_investment_options import filter_investment_options
import requests

def fetch_rental_income(property_id: int):
    if property_id:
        # Construct the URL based on the project_id
        url = f"http://example.com/projects/available_projects/{property_id}/rental_income"
        
        try:
            # Make GET request to the API endpoint
            response = requests.get(url)
           
            # Check if request was successful (status code 200)
            if response.status_code == 200:
                rental_income_data = response.json()
                return rental_income_data
            
            elif response.status_code == 404:
                print("Error: Project not found")
                return None
                        
            else:
                print(f"Error: Failed to fetch data from API. Status code: {response.status_code}")
                 # Return None if request failed to fetch data from API
                
        except requests.exceptions.RequestException as e:
            print(f"Error: Request to Kibris Sunum API failed - {str(e)}")
            return None 

def run_rental_income_forecast(**kwargs):
    parameters = InvestmentOptionsSchema(**kwargs)
    filtered_projects = filter_investment_options(parameters)
    rental_income_data = []
    
    for project in filtered_projects:
        #Fetch rental income forecast data for specified property
        rental_income = fetch_rental_income(int(project['propertyID']))
            
        if rental_income:
            rental_income_data.append(rental_income)
    
          