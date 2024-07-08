from models import InvestmentOptionsSchema
from data import projects_data

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