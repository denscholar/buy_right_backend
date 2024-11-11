from django.urls import path

from products.views import CallScrappyAPIView

urlpatterns = [path("", CallScrappyAPIView.as_view(), name="scrap-data")]
