from django.urls import path
from views import SearchResultProvider

urlpatterns = [
    path('', SearchResultProvider.as_view(), name='searchresults'),
]