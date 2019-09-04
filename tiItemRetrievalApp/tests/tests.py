from django.test import TestCase
from unittest.mock import Mock, patch
import tiItemRetrievalApp.searchclient as search_client

# Create your tests here
class search_test_cases(TestCase):

    # TODO - Complete after elastic search functionality is complete, refer: https://realpython.com/testing-third-party-apis-with-mocks/ - def test_integration_contract():
    #def test_search_contract(TestCase):

    def mocked_requests_get(*args):
        print ("mock called with arg", args[0])
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json_data(self):
                print ("from test: ", self.json_data)
                return self.json_data

        #print ("mocks equal check for positive reponse", args[0] == 'http://searchUrl.com?sellingInCountry=India&priceDiff>0&orderBy=desc')
        #print ("mocks equal check for negative reponse", args[0] == 'http://searchUrl.com?buyingInCountry=India&priceDiff<0&orderBy=asc')
        if args[0] == 'http://searchUrl.com?sellingInCountry=India&priceDiff>0&orderBy=desc&attempt=1':
            #print ("Returning positive price mock object")
            return MockResponse('[ {"buyingInCountry": "USA", "sellingInCountry":"India", "priceDiff":"$200", "product":"samsung s9", "provider":"amazon", "productImage":"https://image"} ]', 200)
        elif args[0] == 'http://searchUrl.com?buyingInCountry=India&priceDiff<0&orderBy=asc&attempt=1':
            #print ("Returning negative price mock object")
            return MockResponse('[ {"buyingInCountry": "India", "sellingInCountry":"China", "priceDiff":"-$300", "product":"samsung s9", "provider":"alibaba", "productImage":"https://imageFromAlibaba"} ]', 200)
        elif args[0] == 'http://searchUrl.com?buyingInCountry=NoResult&priceDiff<0&orderBy=asc&attempt=4':
            #print ("Returning negative price mock object")
            return MockResponse('[ {"buyingInCountry": "NoResultResponseOn4thAttempt", "sellingInCountry":"NoResultResponseOn4thAttempt", "priceDiff":"-$300", "product":"NoResultResponseOn4thAttempt", "provider":"NoResultResponseOn4thAttempt", "productImage":"NoResultResponseOn4thAttempt"} ]', 200)


        return MockResponse(None, 404)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_search_response_for_seller(self, mock_get):
        response = search_client.get_response_for_seller("India")
        self.assertEqual(response, [{"buyingInCountry": "China", "sellingInCountry":"India", "priceDiff":"$300", "product":"samsung s9", "provider":"alibaba", "productImage":"https://imageFromAlibaba"},
                                    {"buyingInCountry": "USA", "sellingInCountry":"India", "priceDiff":"$200", "product":"samsung s9", "provider":"amazon", "productImage":"https://image"}])

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_search_response_no_results_returned(self, mock_get):
        response = search_client.get_response_for_seller("NoResult")
        self.assertEqual(response, [{"buyingInCountry": "NoResultResponseOn4thAttempt", "sellingInCountry":"NoResultResponseOn4thAttempt", "priceDiff":"$300", "product":"NoResultResponseOn4thAttempt", "provider":"NoResultResponseOn4thAttempt", "productImage":"NoResultResponseOn4thAttempt"} ] )