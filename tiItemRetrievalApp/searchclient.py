import requests
import json

def query_search_engine(searchParams):
    endpoint = "http://searchUrl.com"
    response_json_data_str = '[]'

    for attempt in range(4):
        params = searchParams + "&attempt=" + str(attempt + 1)
        response = requests.get(endpoint + params)
        if response.json_data:
            response_json_data_str = response.json_data
            break

    return json.loads(response_json_data_str)


def get_response_for_seller(sellingInCountry, product=""):
    #Construct the endpoint
    endpoint = "http://searchUrl.com"

    #Call 1 - call for postive priceDiff
    params = "?sellingInCountry=" + sellingInCountry
    if (product != ""):
        params = params + "&product=" + product
    params = params + "&priceDiff>0&orderBy=desc"

    positivePriceDiffResponse = query_search_engine(params)

    #Call 2 - call for negative price diff
    params= "?buyingInCountry=" + sellingInCountry
    if (product != ""):
        params = params + "&product=" + product
    params = params + "&priceDiff<0&orderBy=asc"

    negativePriceDiffResponse = query_search_engine(params)
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

