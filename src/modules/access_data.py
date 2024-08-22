import requests

def fetch_available_projects(location=None, min_price=None, max_price=None, purpose=None):
    """
    Fetch available projects based on optional query parameters.

    Args:
        location (str, optional): The location to filter projects by. Defaults to None.
        min_price (int, optional): The minimum price to filter projects by. Defaults to None.
        max_price (int, optional): The maximum price to filter projects by. Defaults to None.
        purpose (str, optional): The purpose to filter projects by. Defaults to None.

    Returns:
        dict: The JSON response containing the list of available projects.

    Raises:
        Exception: If the request fails or returns an error status code.
    """
    
    url = "http://127.0.0.1:5000/projects/available_projects"
    params = {
        "location": location,
        "min_price": min_price,
        "max_price": max_price,
        "purpose": purpose
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch projects data: {response.status_code} - {response.text}")
    

def fetch_rental_income(property_id):
    """
    Fetch rental income data for a specific property ID.

    Args:
        property_id (str): The ID of the property to fetch rental income data for.

    Returns:
        dict: The JSON response containing the rental income data for the specified property.

    Raises:
        Exception: If the request fails or returns an error status code.
    """
    
    url = f"http://127.0.0.1:5000/projects/available_projects/{property_id}/rental_income"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch rental income data: {response.status_code} - {response.text}")

def fetch_price_list(property_id):
    """
    Fetch the price list for a specific property ID.

    Args:
        property_id (str): The ID of the property to fetch the price list for.

    Returns:
        dict: The JSON response containing the price list for the specified property.

    Raises:
        Exception: If the request fails or returns an error status code.
    """
    
    url = f"http://127.0.0.1:5000/projects/available_projects/{property_id}/price_list"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch price list data: {response.status_code} - {response.text}")