import unittest
from unittest.mock import patch, MagicMock
from src.models import InvestmentOptionsSchema
from src.modules.property_details_and_insights import gather_property_details, run_property_details_and_insights
from src.modules.access_data import fetch_price_list

class TestPropertyDetailsAndInsights(unittest.TestCase):

    @patch('src.modules.property_details_and_insights.fetch_price_list')
    def test_gather_property_details(self, mock_fetch_price_list):
        # Mocking fetch_price_list to return sample price list data
        mock_fetch_price_list.return_value = [
            {
                'apratment_type': '2BHK',
                'block': 'A',
                'floor': '5',
                'interior_sqmeter': 80,
                'balcony_terrace_sqmeter': 20,
                'rooftop_sqmeter': 0,
                'total_living_space_sqmeter': 100,
                'payment_plan': {
                    'price': 250000,
                    'start_date': '2024-01-01',
                    'delivery_date': '2025-01-01',
                    'installment_payment_plan': 'Monthly',
                    'additional_fees': {'fee1': 1000},
                    'total_amount': 260000
                }
            }
        ]

        property_id = 'prop1'
        details = gather_property_details(property_id)

        expected_details = [
            {
                'Apartment Type': '2BHK',
                'Block': 'A',
                'Floor': '5',
                'Interior Area (sqm)': 80,
                'Balcony/Terrace Area (sqm)': 20,
                'Rooftop Area (sqm)': 0,
                'Total Living Space (sqm)': 100,
                'Price': 250000,
                'Price Per Square Meter': 2500,
                'Payment Plan Start Date': '2024-01-01',
                'Payment Plan Delivery Date': '2025-01-01',
                'Installment Payment Plan': 'Monthly',
                'Additional Fees': {'fee1': 1000},
                'Total Amount': 260000
            }
        ]

        self.assertEqual(details, expected_details)

    @patch('src.modules.property_details_and_insights.filter_investment_options')
    @patch('src.modules.property_details_and_insights.gather_property_details')
    def test_run_property_details_and_insights(self, mock_gather_property_details, mock_filter_investment_options):
        # Mocking filter_investment_options to return sample filtered projects
        mock_filter_investment_options.return_value = [
            {
                'propertyID': 'prop1',
                'projectName': 'Project A',
                'propertyDeveloper': 'Dovec Construction',
                'location': 'Kyrenia',
                'purpose': 'Residential',
                'completion_date': '2025-12-31',
                'facilities': ['Pool', 'Gym'],
                'no_of_rooms': 3,
                'no_of_bathrooms': 2
            }
        ]

        # Mocking gather_property_details to return sample property details
        mock_gather_property_details.return_value = [
            {
                'Apartment Type': '2BHK',
                'Block': 'A',
                'Floor': '5',
                'Interior Area (sqm)': 80,
                'Balcony/Terrace Area (sqm)': 20,
                'Rooftop Area (sqm)': 0,
                'Total Living Space (sqm)': 100,
                'Price': 250000,
                'Price Per Square Meter': 2500,
                'Payment Plan Start Date': '2024-01-01',
                'Payment Plan Delivery Date': '2025-01-01',
                'Installment Payment Plan': 'Monthly',
                'Additional Fees': {'fee1': 1000},
                'Total Amount': 260000
            }
        ]

        parameters = {
            'location': 'Kyrenia',
            'budget_min': 200000,
            'budget_max': 300000
        }

        result = run_property_details_and_insights(**parameters)

        expected_result = {
            "property_details": [
                {
                    'propertyID': 'prop1',
                    'Project Name': 'Project A',
                    'Property Developer': 'Dovec Construction',
                    'Location': 'Kyrenia',
                    'Purpose': 'Residential',
                    'Completion Date': '2025-12-31',
                    'Facilities': 'Pool, Gym',
                    'ImageURL': [
                        "https://static.tildacdn.com/stor3335-6430-4635-a664-303033613461/19958823.jpg",
                        "https://optim.tildacdn.one/tild3831-3338-4936-b035-626534353538/-/format/webp/90156560.jpeg",
                        "https://optim.tildacdn.com/stor3830-3761-4335-b033-396166663233/-/format/webp/93188055.jpg",
                        "https://optim.tildacdn.com/stor3465-3132-4464-b562-636266383936/-/format/webp/44491027.jpg"
                    ],
                    'Property Details': [
                        {
                            'Apartment Type': '2BHK',
                            'Block': 'A',
                            'Floor': '5',
                            'Interior Area (sqm)': 80,
                            'Balcony/Terrace Area (sqm)': 20,
                            'Rooftop Area (sqm)': 0,
                            'Total Living Space (sqm)': 100,
                            'Price': 250000,
                            'Price Per Square Meter': 2500,
                            'Payment Plan Start Date': '2024-01-01',
                            'Payment Plan Delivery Date': '2025-01-01',
                            'Installment Payment Plan': 'Monthly',
                            'Additional Fees': {'fee1': 1000},
                            'Total Amount': 260000
                        }
                    ],
                    '360 view': 'https://360.dovecconstruction.com/',
                    'Number of Rooms': 3,
                    'Number of Bathrooms': 2
                }
            ]
        }

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
