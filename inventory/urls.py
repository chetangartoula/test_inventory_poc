

from django.urls import path

from inventory.views import StockInlistView



urlpatterns = [
    path("stock-in/",StockInlistView.as_view())
]