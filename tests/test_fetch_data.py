import unittest
from unittest.mock import patch, MagicMock
from api.fetch_data import fetch_auction_results
import requests
import json
from datetime import datetime 

class TestFetchAuctionResults(unittest.TestCase):

    @patch('api.fetch_data.requests.post')
    def test_fetch_auction_results(self, mock_post):
        # Mock response data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "help": "https://api.nationalgrideso.com/api/3/action/help_show?name=datastore_search",
            "success": True,
            "result": {
                "resource_id": "a63ab354-7e68-44c2-ad96-c6f920c30e85",
                "records": [
                    {
                        "_id": 1,
                        "registeredAuctionParticipant": "HABITAT ENERGY LIMITED",
                        "auctionUnit": "HAB6-FFR",
                        "serviceType": "Response",
                        "auctionProduct": "DCH",
                        "executedQuantity": 36.0,
                        "clearingPrice": 1.58,
                        "deliveryStart": "2024-08-06T17:00:00",
                        "deliveryEnd": "2024-08-06T22:00:00",
                        "technologyType": "Batteries",
                        "postCode": "TN17",
                        "unitResultID": "579#||#87#||#DCH#||#24070"
                    }
                ]
            }
        }
        
        # Configure the mock to return a response with the mocked data
        mock_post.return_value = mock_response
        
        # Call the function
        records = fetch_auction_results("HABITAT ENERGY LIMITED")
        
        # Assertions
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['registeredAuctionParticipant'], 'HABITAT ENERGY LIMITED')

    @patch('api.fetch_data.requests.post')
    def test_fetch_auction_results_http_error(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response

        # Call the function
        results = fetch_auction_results("HABITAT ENERGY LIMITED")

        # Assertions
        self.assertEqual(results, [])

    @patch('api.fetch_data.requests.post')
    def test_fetch_auction_results_api_error(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": False,
            "error": {
                "message": "Invalid request"
            }
        }
        mock_post.return_value = mock_response

        # Call the function
        results = fetch_auction_results("HABITAT ENERGY LIMITED")

        # Assertions
        self.assertEqual(results, [])

    @patch('api.fetch_data.requests.post')
    def test_fetch_auction_results_json_decode_error(self, mock_post):
        # Setup mock to raise JSONDecodeError
        mock_post.side_effect = json.JSONDecodeError("Expecting value", "", 0)

        # Call the function
        results = fetch_auction_results("HABITAT ENERGY LIMITED")

        # Assertions
        self.assertEqual(results, [])

    @patch('api.fetch_data.requests.post')
    def test_fetch_auction_results_request_exception(self, mock_post):
        # Setup mock to raise RequestException
        mock_post.side_effect = requests.RequestException("Network error")

        # Call the function
        results = fetch_auction_results("HABITAT ENERGY LIMITED")

        # Assertions
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()