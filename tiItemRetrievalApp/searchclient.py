import requests
import json

def get_response_for_seller(sellingInCountry, product=""):
    #Construct the endpoint
    endpoint = "http://searchUrl.com"

    #Call 1 - call for postive priceDiff
    params = "?sellingInCountry=" + sellingInCountry
    if (product != ""):
        params = params + "&product=" + product

    params = params + "&pricediff>0&orderby=asc"

    response = requests.get(endpoint + params)
    positivePriceDiffResponse = json.loads(response.json_data())

    #Call 2 - call for negative price diff
    params= "buyingInCountry=" + sellingInCountry
    if (product != ""):
        params = params + "&product=" + product

    params = params + "&pricediff<0&orderby=desc"

    response = requests.get(endpoint + params)
    negativePriceDiffResponse = json.loads(response.json_data)

    negativePriceDiffResponseFlipped = flip_signs_and_buyer_seller(negativePriceDiffResponse)
    mergedResponseForSeller = merge_sort(positivePriceDiffResponse, negativePriceDiffResponseFlipped)

    return mergedResponseForSeller

def flip_signs_and_buyer_seller(items):
    pass

def merge_sort(items1, items2):
    pass

