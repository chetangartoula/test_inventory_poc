from django.urls import path

from inventory.views2 import StockInApi, StockOutApi, StockOverallFlowApi



urlpatterns = [
    path("stock-in/",StockInApi.as_view()),
    path("stock-out/",StockOutApi.as_view()),
    path("stock-logs/", StockOverallFlowApi.as_view())
]