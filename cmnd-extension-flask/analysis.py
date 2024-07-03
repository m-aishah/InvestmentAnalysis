# Placeholder data (replace with actual data source later)
property_listings = [
    {"id": 1, "price": 250000, "location": "City A", "size": 1500, "features": ["3 bedrooms", "2 bathrooms"]},
    {"id": 2, "price": 300000, "location": "City B", "size": 1800, "features": ["4 bedrooms", "2.5 bathrooms"]},
    {"id": 3, "price": 200000, "location": "City A", "size": 1200, "features": ["2 bedrooms", "1 bathroom"]},
    # Add more properties as needed
]

def filter_properties(budget_min, budget_max, location):
    filtered_properties = []
    for property in property_listings:
        if budget_min <= property['price'] <= budget_max and property['location'] == location:
            filtered_properties.append(property)
    return filtered_properties

def display_comparison_table(properties):
    print("Property Comparison Table:")
    print("{:<5} {:<10} {:<15} {:<10}".format("ID", "Price", "Location", "Size"))
    print("-" * 40)
    for property in properties:
        print("{:<5} ${:<10,.2f} {:<15} {:<10} sqft".format(property['id'], property['price'], property['location'], property['size']))

# Example usage
budget_min = 200000
budget_max = 300000
location = "City A"
filtered_properties = filter_properties(budget_min, budget_max, location)
display_comparison_table(filtered_properties)