import requests
import json

def get_response_for_seller(sellingInCountry, product=""):
    #Construct the endpoint
    endpoint = "http://searchUrl.com"

    #Call 1 - call for postive priceDiff
    params = "?sellingInCountry=" + sellingInCountry
    if (product != ""):
        params = params + "&product=" + product

    params = params + "&priceDiff>0&orderBy=desc"

    response = requests.get(endpoint + params)
    positivePriceDiffResponse = json.loads(response.json_data)

    #Call 2 - call for negative price diff
    params= "?buyingInCountry=" + sellingInCountry
    if (product != ""):
        params = params + "&product=" + product

    params = params + "&priceDiff<0&orderBy=asc"

    response = requests.get(endpoint + params)
    negativePriceDiffResponse = json.loads(response.json_data)

    negativePriceDiffResponseFlipped = flip_signs_and_buyer_seller(negativePriceDiffResponse)
    mergedResponseForSeller = merge_sort(positivePriceDiffResponse, negativePriceDiffResponseFlipped)

    return mergedResponseForSeller

def flip_signs_and_buyer_seller(items):
    for item in items:
        item['priceDiff'] = item['priceDiff'].replace("$","")
        pricediffFlipped = int(item['priceDiff']) * -1
        item['priceDiff'] = "$" + str(pricediffFlipped)

        # swap buyer and selle
        temp = item['buyingInCountry']
        item['buyingInCountry'] = item['sellingInCountry']
        item['sellingInCountry'] = temp

    return items

def merge_sort(items1, items2):
    allItems = items1 + items2
    return sorted(allItems, key=lambda item: item['priceDiff'], reverse=True)

