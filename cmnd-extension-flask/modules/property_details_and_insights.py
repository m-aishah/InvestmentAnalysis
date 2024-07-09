from models import InvestmentOptionsSchema
# from data_access import fetch_price_list
from modules.filter_investment_options import filter_investment_options
from data import price_list

def gather_property_details(property_id):
    # try:
      #  price_list = fetch_price_list(property_id)
    # except Exception as e:
      #  raise Exception(f"Failed to fetch price list: {e}")

    details = []
    for price_info in price_list:
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
    property_details = []

    for item in filtered_projects:
        property_id = item['property']['propertyID']
        details = gather_property_details(property_id)
        property_details.append({
            'Project Name': item['project']['projectName'],
            'Property Developer': item['project']['propertyDeveloper'],
            'Location': item['project']['location'],
            'Purpose': item['project']['purpose'],
            'Completion Date': item['project']['completion_date'],
            'Facilities': ", ".join(item['project']['facilities']),
            'Details': details
        })

    return {"property_details": property_details}
