from django.test import TestCase
from unittest.mock import Mock, patch
import tiItemRetrievalApp.searchclient as search_client

# Create your tests here
class search_test_cases(unittest.TestCase):

    # TODO - Complete after elastic search functionality is complete, refer: https://realpython.com/testing-third-party-apis-with-mocks/ - def test_integration_contract():
    #def test_search_contract(TestCase):

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data
    
        if args[0] == 'http://searchUrl.com/sellingInCountry=India&priceDiff>0&orderBy=desc':
            return MockResponse( [ {"buyingInCountry": "USA", "sellingInCountry":"India", "priceDiff":"$200", "product":"samsung s9", "provider":"amazon"} ], 200)
        elif args[0] == 'http://searchUrl.com/buyingInCountry=India&priceDiff<0&orderBy=asc':
            return MockResponse([ {"buyingInCountry": "India", "sellingInCountry":"China", "priceDiff":"-$300", "product":"samsung s9", "provider":"alibaba"} ], 200)

        return MockResponse(None, 404)

    def test_search_response_for_seller(self):
        with patch('tiItemRetrievalApp.searchresultprovider.requests.get', side_effect=mocked_requests_get) as mock_getsearchresult:
            response = search_client.get_response_for_seller("India")
            self.assertEqual(response.json(), [{"buyingInCountry": "China", "sellingInCountry":"India", "priceDiff":"$300", "product":"samsung s9", "provider":"alibaba"},
                                               {"buyingInCountry": "USA", "sellingInCountry":"India", "priceDiff":"$200", "product":"samsung s9", "provider":"amazon"}])
