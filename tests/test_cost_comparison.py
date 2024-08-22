import unittest
from unittest.mock import patch, MagicMock
from src.models import InvestmentOptionsSchema
from src.modules.cost_comparison import run_cost_comparison_module

class TestCostComparisonModule(unittest.TestCase):

    @patch('src.modules.cost_comparison.fetch_price_list')
    @patch('src.modules.cost_comparison.fetch_rental_income')
    @patch('src.modules.cost_comparison.filter_investment_options')
    def test_run_cost_comparison_module(self, mock_filter_investment_options, mock_fetch_rental_income, mock_fetch_price_list):
        # Mocking the filter_investment_options function to return a list of properties
        mock_filter_investment_options.return_value = [
            {
                'propertyID': 'prop1',
                'projectName': 'Project A',
                'type': 'Apartment',
                'price': 300000,
                'total_area_sqmeter': 100,
                'no_of_rooms': 3,
                'no_of_bathrooms': 2,
                'location': 'Kyrenia',
                'completion_date': '2025-12-31',
                'facilities': ['Pool', 'Gym'],
                'percentage_sold': 80,
                'propertyDeveloper': 'Dovec'
            }
        ]

        # Mocking fetch_rental_income function to return rental income data
        mock_fetch_rental_income.return_value = {
            'realistic': {
                'annual_net_rental_yield': 5.0,
                'ROI': 8.0
            }
        }

        # Mocking fetch_price_list function to return price list data
        mock_fetch_price_list.return_value = [{
            'payment_plan': {
                'total_amount': 310000,
                'additional_fees': {'fee1': 1000, 'fee2': 2000}
            }
        }]

        # Providing test parameters
        test_params = {
            "location": "Kyrenia",
            "budget_min": 250000,
            "budget_max": 400000,
            "purpose": "Residential"
        }

        # Running the cost comparison module
        result = run_cost_comparison_module(**test_params)
        
        # Assertions to check the structure and content of the result
        self.assertIn("properties", result)
        self.assertEqual(len(result["properties"]), 1)

        property_data = result["properties"][0]
        self.assertEqual(property_data["projectName"], "Project A")
        self.assertEqual(property_data["Property"], "Apartment")
        self.assertEqual(property_data["Location"], "Kyrenia")
        self.assertEqual(property_data["Total Price"], "€300,000")
        self.assertEqual(property_data["Gross Rental Yield"], "5.00%")
        self.assertEqual(property_data["Net Rental Yield"], "8.00%")
        self.assertEqual(property_data["Developer Track Record"], "Excellent")
    
    def test_run_cost_comparison_module_invalid_input(self):
        # Test with invalid input to ensure error handling works correctly
        result = run_cost_comparison_module(location="Nicosia", budget_min="invalid", budget_max=500000)
        self.assertIn("error", result)
        self.assertTrue("validation" in result["error"])

if __name__ == '__main__':
    unittest.main()
