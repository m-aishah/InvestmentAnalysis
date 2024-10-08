from src.models import InvestmentOptionsSchema
from src.modules.filter_investment_options import filter_investment_options
from src.modules.access_data import fetch_rental_income, fetch_price_list
from datetime import datetime
import numpy as np

class RiskScorer:
    """
    A class for scoring various risk factors associated with property investments.
    """
    def __init__(self):
        pass

    def location_risk(self, location):
        """
        Calculates risk based on the location.

        Args:
            location (str): The location of the property.

        Returns:
            float: Risk score for the given location.
        """
        
        # Change this implementation.
        risk_scores = {
            "All": 1.0,
            "Kyrenia": 0.2,
            "Iskele": 0.3,
            "Guzelyurt": 0.4,
            "Nicosia": 0.5,
            "Famagusta": 0.6,
            "Lefke": 0.7,
            "Karpaz Peninsula": 0.8
        }
        return risk_scores.get(location, 1.0)

    def price_risk(self, min_price, max_price):
        """
        Calculates risk based on the price range of the property.

        Args:
            min_price (float): Minimum price of the property.
            max_price (float): Maximum price of the property.

        Returns:
            float: Risk score based on price volatility.
        """
        price_volatility = max_price - min_price
        return price_volatility / max_price

    def completion_sale_risk(self, percentage_sold, start_date, completion_date):
        """
        Calculates risk associated with the completion and sale of the property.

        Args:
            percentage_sold (float): Percentage of the property sold.
            start_date (str): The start date of the sale.
            completion_date (str): The expected completion date.

        Returns:
            float: Risk score based on completion and sale status.
        """
        
        days_to_completion = (datetime.strptime(completion_date, '%Y-%m-%d') - datetime.now()).days
        sale_risk = 1 - (percentage_sold / 100)
        return sale_risk + (days_to_completion / 365)

    def rental_income_risk(self, rental_income):
        """
        Calculates risk based on rental income variability.

        Args:
            rental_income (dict): Dictionary containing pessimistic and optimistic rental income yields.

        Returns:
            float: Risk score based on the difference between optimistic and pessimistic yields.
        """
        pessimistic_yield = rental_income['pessimistic']['annual_net_rental_yield']
        optimistic_yield = rental_income['optimistic']['annual_net_rental_yield']
        return (optimistic_yield - pessimistic_yield) / optimistic_yield

    def financial_risk(self, payment_plan):
        """
        Calculates financial risk based on the payment plan.

        Args:
            payment_plan (dict): Dictionary containing details of the payment plan.

        Returns:
            float: Risk score based on additional fees in the payment plan.
        """
        total_amount = payment_plan['total_amount']
        additional_fees = sum(payment_plan['additional_fees'].values())
        return additional_fees / total_amount

    def developer_risk(self, property_developer):
        """
        Calculates risk based on the developer's reputation.

        Args:
            property_developer (str): Name of the property developer.

        Returns:
            float: Risk score based on the developer's reputation.
        """
        # Placeholder for developer risk scoring logic, this is the chance to give dovec a priority
        if property_developer == "Dovec Construction":
            return 0.0
        return 1.0

class RiskEvaluator:
    """
    A class for evaluating the risk of a property based on various risk factors.
    """
    def __init__(self, scorer):
        """
        Initializes the RiskEvaluator instance with a RiskScorer.

        Args:
            scorer (RiskScorer): An instance of the RiskScorer class.
        """
        self.scorer = scorer

    def evaluate_property(self, property_data):
        """
        Evaluates the risk of a property based on its data.

        Args:
            property_data (dict): Dictionary containing property details.

        Returns:
            tuple: A tuple containing the composite risk score and a dictionary of individual risk scores.
        """
        location_score = self.scorer.location_risk(property_data['location'])
        price_score = self.scorer.price_risk(property_data['min_price'], property_data['max_price'])
        completion_sale_score = self.scorer.completion_sale_risk(
            property_data['percentage_sold'], property_data['start_date'], property_data['completion_date']
        )
        rental_income_score = self.scorer.rental_income_risk(property_data['rental_income'])
        financial_score = self.scorer.financial_risk(property_data['payment_plan'])
        developer_score = self.scorer.developer_risk(property_data['property_developer'])

        risk_scores = {
            "location": location_score,
            "price": price_score,
            "completion_sale": completion_sale_score,
            "rental_income": rental_income_score,
            "financial": financial_score,
            "developer": developer_score
        }
        composite_score = np.mean(list(risk_scores.values()))
        return composite_score, risk_scores

class RiskReportGenerator:
    """
    A class for generating risk reports based on property data and risk evaluations.
    """
    def generate_report(self, property_data, risk_score, risk_factors):
        """
        Generates a comprehensive risk report for a property.

        Args:
            property_data (dict): Dictionary containing property details.
            risk_score (float): The overall risk score of the property.
            risk_factors (dict): Dictionary containing individual risk factors.

        Returns:
            dict: A dictionary representing the risk report.
        """
        report = {
            "propertyID": property_data['propertyID'],
            "property_name": property_data['projectName'],
            "location": property_data['location'],
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "recommendations": self.generate_recommendations(risk_factors)
        }
        return report

    def generate_recommendations(self, risk_factors):
        """
        Generates recommendations based on risk factors.

        Args:
            risk_factors (dict): Dictionary containing individual risk factors.

        Returns:
            list: A list of recommendations based on the risk factors.
        """
        recommendations = []
        if risk_factors['location'] > 0.5:
            recommendations.append("Consider alternative locations with lower risk.")
        if risk_factors['price'] > 0.5:
            recommendations.append("Evaluate price stability in the area.")
        if risk_factors['completion_sale'] > 0.5:
            recommendations.append("Check project completion and sales status.")
        if risk_factors['rental_income'] > 0.5:
            recommendations.append("Assess rental income stability.")
        if risk_factors['financial'] > 0.5:
            recommendations.append("Review payment plan and additional fees.")
        if risk_factors['developer'] > 0.5:
            recommendations.append("Investigate developer's track record.")
        return recommendations

scorer = RiskScorer()
evaluator = RiskEvaluator(scorer)
report_generator = RiskReportGenerator()


def gather_property_details(property_id):
    """
    Gathers detailed information about a property given its ID.

    Args:
        property_id (str): The ID of the property.

    Returns:
        list: A list of dictionaries containing detailed property information.
    """
    price_list = fetch_price_list(property_id)
    rental_income = fetch_rental_income(property_id)

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

def run_risk_analysis_module(**kwargs):
    """
    Runs the risk analysis module to evaluate and report on property investment risks.

    Args:
        **kwargs: Keyword arguments containing parameters for filtering investment options.

    Returns:
        dict: A dictionary containing risk analysis reports for the filtered projects.
    """
    parameters = InvestmentOptionsSchema(**kwargs)
    filtered_projects = filter_investment_options(parameters)
    risk_analysis_report = []
    
    for item in filtered_projects:
        projectID = item['projectID']
        property_id = item['propertyID']
        rental_income = fetch_rental_income(property_id)
        price_list = fetch_price_list(property_id)
        property_developer = item['propertyDeveloper']
        if price_list: payment_plan = price_list[0]['payment_plan']
        else: payment_plan = None
        if rental_income and payment_plan:
            property_data = {
                "propertyID": property_id,
                "projectName": item['projectName'],
                "propertyDeveloper": item['propertyDeveloper'],
                "location": item['location'],
                "purpose": item['purpose'],
                "completion_date": item['completion_date'],
                "facilities": item['facilities'],
                "min_price": item['price'],
                "max_price": item['price'],  
                "percentage_sold": item['percentage_sold'],
                "start_date": item['start_date'],
                "rental_income": rental_income,
                "payment_plan": payment_plan,
                "property_developer": property_developer,
                "developer_history": {}  # Placeholder for developer history
            }
            risk_score, risk_factors = evaluator.evaluate_property(property_data)
            report = report_generator.generate_report(property_data, risk_score, risk_factors)
            risk_analysis_report.append({
                'Project Name': item['projectName'],
                'Property Developer': item['propertyDeveloper'],
                'Location': item['location'],
                'Purpose': item['purpose'],
                'Completion Date': item['completion_date'],
                'Facilities': ", ".join(item['facilities']),
                'Property Type': item['type'],
                'Risk Report': report
            })

    return {"risk_analysis": risk_analysis_report}


# Testing
if __name__ == "__main__":
    # Example usage:
    kwargs = {
        "location": "Nicosia",
        "budget_min": 200000,
        "budget_max": 600000,
        "purpose": "Residential"
    }

    result = run_risk_analysis_module(**kwargs)
    print(result)