import unittest
from unittest.mock import patch
from api.fetch_data import fetch_auction_results
from datetime import datetime 

class TestFetchAuctionResults(unittest.TestCase):

    @patch('api.fetch_data.requests.post')
    def test_fetch_auction_results(self, mock_post):
        # Mock response data
        mock_response_data = {
            "help": "https://api.nationalgrideso.com/api/3/action/help_show?name=datastore_search",
            "success": True,
            "result": {
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
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response_data
        
        # Call the function
        records = fetch_auction_results("HABITAT ENERGY LIMITED")

        # Debugging: Print results and resource_id
        print("Results:", records)
        
        # Assertions
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["_id"], 1)
        self.assertEqual(records[0]["executedQuantity"], 36.0)
        self.assertEqual(records[0]["clearingPrice"], 1.58)
        self.assertEqual(records[0]['registeredAuctionParticipant'], 'HABITAT ENERGY LIMITED')
        # Convert the deliveryEnd to a date object for comparison
        delivery_end_date = datetime.fromisoformat(records[0]['deliveryEnd']).date()
        self.assertEqual(delivery_end_date, datetime(2024, 8, 6).date())

        # Check if executedQuantity and clearingPrice are float
        self.assertIsInstance(records[0]['executedQuantity'], float)
        self.assertIsInstance(records[0]['clearingPrice'], float)

if __name__ == '__main__':
    unittest.main()