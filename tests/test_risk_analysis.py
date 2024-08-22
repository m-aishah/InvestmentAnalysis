import unittest
from unittest.mock import patch, MagicMock
from src.models import InvestmentOptionsSchema
from src.modules.risk_analysis import run_risk_analysis_module

class TestRunRiskAnalysisModule(unittest.TestCase):

    @patch('src.modules.risk_analysis.filter_investment_options')
    @patch('src.modules.risk_analysis.fetch_rental_income')
    @patch('src.modules.risk_analysis.fetch_price_list')
    def test_run_risk_analysis_module(self, mock_fetch_price_list, mock_fetch_rental_income, mock_filter_investment_options):
        # Mocking the responses for external API calls
        mock_filter_investment_options.return_value = [{
            'projectID': 'proj1',
            'propertyID': 'prop1',
            'propertyDeveloper': 'Dev1',
            'projectName': 'Project A',
            'location': 'Nicosia',
            'purpose': 'Residential',
            'completion_date': '2025-01-01',
            'facilities': ['Pool', 'Gym'],
            'percentage_sold': 50,
            'price': 500000,
            'start_date': '2023-01-01',
            'type': 'Apartment'
        }]
        
        mock_fetch_rental_income.return_value = {
            'pessimistic': {'annual_net_rental_yield': 4.0},
            'optimistic': {'annual_net_rental_yield': 6.0}
        }
        
        mock_fetch_price_list.return_value = [{
            'payment_plan': {
                'price': 500000,
                'start_date': '2023-01-01',
                'delivery_date': '2025-01-01',
                'installment_payment_plan': 'Plan A',
                'additional_fees': {'fee1': 1000},
                'total_amount': 520000
            }
        }]

        # Input parameters for the test
        kwargs = {
            "location": "Nicosia",
            "budget_min": 200000,
            "budget_max": 600000,
            "purpose": "Residential"
        }
        
        # Running the function
        result = run_risk_analysis_module(**kwargs)
        
        # Asserting the output structure and contents
        self.assertIn('risk_analysis', result)
        self.assertEqual(len(result['risk_analysis']), 1)
        risk_report = result['risk_analysis'][0]
        self.assertEqual(risk_report['Project Name'], 'Project A')
        self.assertEqual(risk_report['Property Developer'], 'Dev1')
        self.assertEqual(risk_report['Location'], 'Nicosia')
        self.assertIn('Risk Report', risk_report)

if __name__ == '__main__':
    unittest.main()
