import unittest
from unittest.mock import patch
from src.modules.access_data import fetch_available_projects, fetch_rental_income, fetch_price_list

class TestAccessData(unittest.TestCase):

    @patch('src.modules.access_data.requests.get')
    def test_fetch_available_projects_success(self, mock_get):
        # Mock the JSON response
        mock_response = {
            "projects": [
                {"id": 1, "name": "Project A", "location": "Nicosia"},
                {"id": 2, "name": "Project B", "location": "Kyrenia"}
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        # Call the function
        result = fetch_available_projects(location="Nicosia")
        
        # Assertions
        self.assertEqual(result, mock_response)
        mock_get.assert_called_once_with(
            "http://127.0.0.1:5000/projects/available_projects",
            params={"location": "Nicosia", "min_price": None, "max_price": None, "purpose": None}
        )

    @patch('src.modules.access_data.requests.get')
    def test_fetch_available_projects_failure(self, mock_get):
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Internal Server Error"

        with self.assertRaises(Exception) as context:
            fetch_available_projects(location="Nicosia")
        
        self.assertIn("Failed to fetch projects data", str(context.exception))

    @patch('src.modules.access_data.requests.get')
    def test_fetch_rental_income_success(self, mock_get):
        # Mock the JSON response
        mock_response = {
            "realistic": {
                "annual_net_rental_yield": 5.2,
                "ROI": 6.5
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        # Call the function
        result = fetch_rental_income(property_id="123")
        
        # Assertions
        self.assertEqual(result, mock_response)
        mock_get.assert_called_once_with("http://127.0.0.1:5000/projects/available_projects/123/rental_income")

    @patch('src.modules.access_data.requests.get')
    def test_fetch_rental_income_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Not Found"

        with self.assertRaises(Exception) as context:
            fetch_rental_income(property_id="123")
        
        self.assertIn("Failed to fetch rental income data", str(context.exception))

    @patch('src.modules.access_data.requests.get')
    def test_fetch_price_list_success(self, mock_get):
        # Mock the JSON response
        mock_response = [
            {
                "propertyID": "123",
                "price": 200000,
                "payment_plan": {
                    "total_amount": 210000,
                    "additional_fees": {
                        "tax": 10000,
                        "other_fees": 5000
                    }
                }
            }
        ]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        # Call the function
        result = fetch_price_list(property_id="123")
        
        # Assertions
        self.assertEqual(result, mock_response)
        mock_get.assert_called_once_with("http://127.0.0.1:5000/projects/available_projects/123/price_list")

    @patch('src.modules.access_data.requests.get')
    def test_fetch_price_list_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Not Found"

        with self.assertRaises(Exception) as context:
            fetch_price_list(property_id="123")
        
        self.assertIn("Failed to fetch price list data", str(context.exception))

if __name__ == '__main__':
    unittest.main()
