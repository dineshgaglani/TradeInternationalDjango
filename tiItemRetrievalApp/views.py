from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import logging

from tiItemRetrievalApp import searchclient

logging.basicConfig()
logger = logging.getLogger("logger")

# Create your views here.
class SearchResultProvider(View):
    def get(self, request):
        usertype = searchclient.get_response_for_seller(request.GET.get("usertype"))

        if usertype == "seller":
            response = searchclient.get_response_for_seller(request.GET.get("country"))
        elif usertype == "buyer":
            pass
        else:
            pass

        return HttpResponse(response.json(), content_type='text/plain')
        