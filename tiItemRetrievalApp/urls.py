from django.urls import path
from tiItemRetrievalApp.views import SearchResultProvider

urlpatterns = [
    path('', SearchResultProvider.as_view(), name='searchresults'),
]