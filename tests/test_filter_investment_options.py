import unittest
from unittest.mock import patch, MagicMock
from src.models import InvestmentOptionsSchema
from src.modules.filter_investment_options import filter_investment_options

class TestFilterInvestmentOptions(unittest.TestCase):

    @patch('src.modules.filter_investment_options.fetch_available_projects')
    def test_filter_by_location(self, mock_fetch_available_projects):
        # Mocking fetch_available_projects to return sample project data
        mock_fetch_available_projects.return_value = [
            {
                'projectID': 'proj1',
                'projectName': 'Project 1',
                'propertyDeveloper': 'Developer A',
                'location': 'Kyrenia',
                'description': 'A beautiful project',
                'purpose': 'Residential',
                'start_date': '2023-01-01',
                'completion_date': '2025-01-01',
                'facilities': ['Pool', 'Gym'],
                'no_of_installments': 12,
                'no_of_properties': 10,
                'percentage_sold': 50,
                'property_types': [
                    {
                        'propertyID': 'prop1',
                        'no_of_rooms': 3,
                        'type': 'Apartment',
                        'total_area_sqmeter': 100,
                        'no_of_bathrooms': 2,
                        'price': 250000
                    }
                ],
                'image_url': ['http://example.com/image.jpg']
            }
        ]

        parameters = InvestmentOptionsSchema(location='Kyrenia', budget_min=200000, budget_max=300000)
        filtered_projects = filter_investment_options(parameters)
        
        expected_result = [
            {
                'projectID': 'proj1',
                'projectName': 'Project 1',
                'propertyDeveloper': 'Developer A',
                'location': 'Kyrenia',
                'description': 'A beautiful project',
                'purpose': 'Residential',
                'start_date': '2023-01-01',
                'completion_date': '2025-01-01',
                'facilities': ['Pool', 'Gym'],
                'no_of_installments': 12,
                'no_of_properties': 10,
                'percentage_sold': 50,
                'propertyID': 'prop1',
                'no_of_rooms': 3,
                'type': 'Apartment',
                'total_area_sqmeter': 100,
                'no_of_bathrooms': 2,
                'price': 250000,
                'ImageURL': 'http://example.com/image.jpg'
            }
        ]
        
        self.assertEqual(filtered_projects, expected_result)

    @patch('src.modules.filter_investment_options.fetch_available_projects')
    def test_filter_by_price_range(self, mock_fetch_available_projects):
        # Mocking fetch_available_projects to return sample project data
        mock_fetch_available_projects.return_value = [
            {
                'projectID': 'proj2',
                'projectName': 'Project 2',
                'propertyDeveloper': 'Developer B',
                'location': 'Nicosia',
                'description': 'Another great project',
                'purpose': 'Commercial',
                'start_date': '2024-01-01',
                'completion_date': '2026-01-01',
                'facilities': ['Parking'],
                'no_of_installments': 10,
                'no_of_properties': 5,
                'percentage_sold': 70,
                'property_types': [
                    {
                        'propertyID': 'prop2',
                        'no_of_rooms': 2,
                        'type': 'Office',
                        'total_area_sqmeter': 80,
                        'no_of_bathrooms': 1,
                        'price': 180000
                    },
                    {
                        'propertyID': 'prop3',
                        'no_of_rooms': 4,
                        'type': 'Retail',
                        'total_area_sqmeter': 150,
                        'no_of_bathrooms': 3,
                        'price': 350000
                    }
                ],
                'image_url': ['http://example.com/image2.jpg']
            }
        ]

        parameters = InvestmentOptionsSchema(location='Nicosia', budget_min=100000, budget_max=200000)
        filtered_projects = filter_investment_options(parameters)
        
        expected_result = [
            {
                'projectID': 'proj2',
                'projectName': 'Project 2',
                'propertyDeveloper': 'Developer B',
                'location': 'Nicosia',
                'description': 'Another great project',
                'purpose': 'Commercial',
                'start_date': '2024-01-01',
                'completion_date': '2026-01-01',
                'facilities': ['Parking'],
                'no_of_installments': 10,
                'no_of_properties': 5,
                'percentage_sold': 70,
                'propertyID': 'prop2',
                'no_of_rooms': 2,
                'type': 'Office',
                'total_area_sqmeter': 80,
                'no_of_bathrooms': 1,
                'price': 180000,
                'ImageURL': 'http://example.com/image2.jpg'
            }
        ]
        
        self.assertEqual(filtered_projects, expected_result)

    @patch('src.modules.filter_investment_options.fetch_available_projects')
    def test_no_properties_found(self, mock_fetch_available_projects):
        # Mocking fetch_available_projects to return no data
        mock_fetch_available_projects.return_value = []

        parameters = InvestmentOptionsSchema(location='Kyrenia', budget_min=200000, budget_max=300000)
        filtered_projects = filter_investment_options(parameters)
        
        self.assertEqual(filtered_projects, [])

    @patch('src.modules.filter_investment_options.fetch_available_projects')
    def test_invalid_parameters(self, mock_fetch_available_projects):
        # Mocking fetch_available_projects to return some data
        mock_fetch_available_projects.return_value = [
            {
                'projectID': 'proj1',
                'projectName': 'Project 1',
                'propertyDeveloper': 'Developer A',
                'location': 'Kyrenia',
                'description': 'A beautiful project',
                'purpose': 'Residential',
                'start_date': '2023-01-01',
                'completion_date': '2025-01-01',
                'facilities': ['Pool', 'Gym'],
                'no_of_installments': 12,
                'no_of_properties': 10,
                'percentage_sold': 50,
                'property_types': [
                    {
                        'propertyID': 'prop1',
                        'no_of_rooms': 3,
                        'type': 'Apartment',
                        'total_area_sqmeter': 100,
                        'no_of_bathrooms': 2,
                        'price': 250000
                    }
                ],
                'image_url': ['http://example.com/image.jpg']
            }
        ]

        # Parameters that don't match any properties
        parameters = InvestmentOptionsSchema(location='Unknown', budget_min=500000, budget_max=600000)
        filtered_projects = filter_investment_options(parameters)
        
        self.assertEqual(filtered_projects, [])

    @patch('src.modules.filter_investment_options.fetch_available_projects')
    def test_sorting(self, mock_fetch_available_projects):
        # Mocking fetch_available_projects to return sample project data
        mock_fetch_available_projects.return_value = [
            {
                'projectID': 'proj3',
                'projectName': 'Project 3',
                'propertyDeveloper': 'Developer C',
                'location': 'Kyrenia',
                'description': 'Third project',
                'purpose': 'Residential',
                'start_date': '2022-01-01',
                'completion_date': '2024-01-01',
                'facilities': ['Gym'],
                'no_of_installments': 15,
                'no_of_properties': 20,
                'percentage_sold': 60,
                'property_types': [
                    {
                        'propertyID': 'prop4',
                        'no_of_rooms': 4,
                        'type': 'House',
                        'total_area_sqmeter': 120,
                        'no_of_bathrooms': 3,
                        'price': 300000
                    }
                ],
                'image_url': ['http://example.com/image3.jpg']
            },
            {
                'projectID': 'proj4',
                'projectName': 'Project 4',
                'propertyDeveloper': 'Developer D',
                'location': 'Kyrenia',
                'description': 'Fourth project',
                'purpose': 'Residential',
                'start_date': '2023-01-01',
                'completion_date': '2025-01-01',
                'facilities': ['Pool'],
                'no_of_installments': 10,
                'no_of_properties': 15,
                'percentage_sold': 75,
                'property_types': [
                    {
                        'propertyID': 'prop5',
                        'no_of_rooms': 3,
                        'type': 'Apartment',
                        'total_area_sqmeter': 100,
                        'no_of_bathrooms': 2,
                        'price': 250000
                    }
                ],
                'image_url': ['http://example.com/image4.jpg']
            }
        ]

        parameters = InvestmentOptionsSchema(location='Kyrenia', budget_min=200000, budget_max=350000, sort_by='price')

    @patch('src.modules.filter_investment_options.fetch_available_projects')
    def test_sorting(self, mock_fetch_available_projects):
        # Mocking fetch_available_projects to return sample project data
        mock_fetch_available_projects.return_value = [
            {
                'projectID': 'proj3',
                'projectName': 'Project 3',
                'propertyDeveloper': 'Developer C',
                'location': 'Kyrenia',
                'description': 'Third project',
                'purpose': 'Residential',
                'start_date': '2022-01-01',
                'completion_date': '2024-01-01',
                'facilities': ['Gym'],
                'no_of_installments': 15,
                'no_of_properties': 20,
                'percentage_sold': 60,
                'property_types': [
                    {
                        'propertyID': 'prop4',
                        'no_of_rooms': 4,
                        'type': 'House',
                        'total_area_sqmeter': 120,
                        'no_of_bathrooms': 3,
                        'price': 300000
                    }
                ],
                'image_url': ['http://example.com/image3.jpg']
            },
            {
                'projectID': 'proj4',
                'projectName': 'Project 4',
                'propertyDeveloper': 'Developer D',
                'location': 'Kyrenia',
                'description': 'Fourth project',
                'purpose': 'Residential',
                'start_date': '2023-01-01',
                'completion_date': '2025-01-01',
                'facilities': ['Pool'],
                'no_of_installments': 10,
                'no_of_properties': 15,
                'percentage_sold': 75,
                'property_types': [
                    {
                        'propertyID': 'prop5',
                        'no_of_rooms': 3,
                        'type': 'Apartment',
                        'total_area_sqmeter': 100,
                        'no_of_bathrooms': 2,
                        'price': 250000
                    }
                ],
                'image_url': ['http://example.com/image4.jpg']
            }
        ]

        parameters = InvestmentOptionsSchema(location='Kyrenia', budget_min=200000, budget_max=350000, sort_by='price')
        filtered_projects = filter_investment_options(parameters)
        
        expected_result = [
            {
                'projectID': 'proj4',
                'projectName': 'Project 4',
                'propertyDeveloper': 'Developer D',
                'location': 'Kyrenia',
                'description': 'Fourth project',
                'purpose': 'Residential',
                'start_date': '2023-01-01',
                'completion_date': '2025-01-01',
                'facilities': ['Pool'],
                'no_of_installments': 10,
                'no_of_properties': 15,
                'percentage_sold': 75,
                'propertyID': 'prop5',
                'no_of_rooms': 3,
                'type': 'Apartment',
                'total_area_sqmeter': 100,
                'no_of_bathrooms': 2,
                'price': 250000,
                'ImageURL': 'http://example.com/image4.jpg'
            },
            {
                'projectID': 'proj3',
                'projectName': 'Project 3',
                'propertyDeveloper': 'Developer C',
                'location': 'Kyrenia',
                'description': 'Third project',
                'purpose': 'Residential',
                'start_date': '2022-01-01',
                'completion_date': '2024-01-01',
                'facilities': ['Gym'],
                'no_of_installments': 15,
                'no_of_properties': 20,
                'percentage_sold': 60,
                'propertyID': 'prop4',
                'no_of_rooms': 4,
                'type': 'House',
                'total_area_sqmeter': 120,
                'no_of_bathrooms': 3,
                'price': 300000,
                'ImageURL': 'http://example.com/image3.jpg'
            }
        ]
        
        self.assertEqual(filtered_projects, expected_result)
if __name__ == '__main__':
    unittest.main()
