from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.scrapper import scrape_website

class CallScrappyAPIView(APIView):
    def get(self, request):
        scrapped_data = scrape_website(website="https://www.jumia.com.ng/")
        response = {
            "message": scrapped_data,
        }
        return Response(data=response, status=status.HTTP_200_OK)

