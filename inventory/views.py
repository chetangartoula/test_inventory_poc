from collections import defaultdict
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from inventory.models import StockInflow, StockOutflow
from inventory.serializers import StockInSerializer, StockOutSerializer

from django.db.models import Sum

# Create your views here.

class StockInlistView(ListCreateAPIView):
    queryset = StockInflow.objects.all()

    serializer_class = StockInSerializer



    def get_queryset(self):
        artical_code =self.request.query_params.get('artical_code')
        print("artical_code",artical_code)
        queryset = StockInflow.objects.filter(article_code = artical_code)
        return queryset.order_by("-order_delivery_date",'-unique_combined_number')


    def list(self, request, *args, **kwargs):
        data  =  self.get_queryset().values("article_code","registered_quantity","registered_gross_weight","order_delivery_date","unique_combined_number")
        units_before = data.aggregate(total_units= Sum("registered_quantity")).get("total_units",0)
        result_data  =  []
        for d in data:
            d['units_after'] = units_before
            d['units_before']  =  units_before -  d['registered_quantity']
            units_before =  d['units_before']
            
            result_data.append(d)
    
        return Response(data=result_data)




class StockOutlistView(ListCreateAPIView):
    queryset = StockOutflow.objects.all()

    serializer_class = StockOutSerializer



    def get_queryset(self):
        artical_code =self.request.query_params.get('artical_code')
        print("artical_code",artical_code)
        queryset = StockOutflow.objects.filter(article_code = artical_code)
        return queryset.order_by("-order_delivery_date",'-unique_combined_number')


    def list(self, request, *args, **kwargs):
        data  =  self.get_queryset().values("article_code","registered_quantity","registered_gross_weight","order_delivery_date","unique_combined_number")
        units_before = data.aggregate(total_units= Sum("registered_quantity")).get("total_units",0)
        result_data  =  []
        for d in data:
            d['units_after'] = units_before
            d['units_before']  =  units_before -  d['registered_quantity']
            units_before =  d['units_before']
            
            result_data.append(d)
    
        return Response(data=result_data)