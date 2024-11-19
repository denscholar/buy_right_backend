from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.scrapper import scrape_websites

# from products.scrapper import scrape_website


websites = [
    {
        "name": "jumia",
        "search_terms": ["Electronics"],
    },
    # Add more website dictionaries here as needed
]
class CallScrappyAPIView(APIView):
    def get(self, request):
        scrapped_data = scrape_websites(websites)
        response = {
            "message": scrapped_data,
        }
        return Response(data=response, status=status.HTTP_200_OK)

