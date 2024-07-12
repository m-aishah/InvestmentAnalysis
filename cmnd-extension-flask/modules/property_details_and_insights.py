from models import InvestmentOptionsSchema
from modules.filter_investment_options import filter_investment_options
# from data_access import fetch_price_lists
from dummy_data import price_list_data

def gather_property_details(property_id):
    # try:
      #  price_list = fetch_price_list(property_id)
    # except Exception as e:
      #  raise Exception(f"Failed to fetch price list: {e}")

    details = []
    property_price_list = price_list_data.get(property_id, None)
    if property_price_list:
        for price_info in property_price_list:
            payment_plan = price_info['payment_plan']
            details.append({
                'Apartment Type': price_info['apratment_type'],
                'Block': price_info['block'],
                'Floor': price_info['floor'],
                'Interior Area (sqm)': price_info['interior_sqmeter'],
                'Balcony/Terrace Area (sqm)': price_info['balcony_terrace_sqmeter'],
                'Rooftop Area (sqm)': price_info['rooftop_sqmeter'],
                'Total Living Space (sqm)': price_info['total_living_space_sqmeter'],
                'Price': payment_plan['price'],
                'Price Per Square Meter': payment_plan['price'] / price_info['total_living_space_sqmeter'],
                'Payment Plan Start Date': payment_plan['start_date'],
                'Payment Plan Delivery Date': payment_plan['delivery_date'],
                'Installment Payment Plan': payment_plan['installment_payment_plan'],
                'Additional Fees': payment_plan['additional_fees'],
                'Total Amount': payment_plan['total_amount']
            })
    return details

def run_property_details_and_insights(**kwargs):
    parameters = InvestmentOptionsSchema(**kwargs)
    filtered_projects = filter_investment_options(parameters)
    # print(len(filtered_projects))
    
    property_details = []
    # print(filtered_projects)
    for item in filtered_projects:
        property_id = item['propertyID']
        details = gather_property_details(property_id)
        if len(details) > 0:
            property_details.append({
                'propertyID': item['propertyID'],
                'Project Name': item['projectName'],
                'Property Developer': item['propertyDeveloper'],
                'Location': item['location'],
                'Purpose': item['purpose'],
                'Completion Date': item['completion_date'],
                'Facilities': ", ".join(item['facilities']),
                'Property Details': details
            })

    return {"property_details": property_details}
