

from django.urls import path

from inventory.views import StockInlistView, StockOutlistView



urlpatterns = [
    path("stock-in/",StockInlistView.as_view()),
    path("stock-out/",StockOutlistView.as_view())
]