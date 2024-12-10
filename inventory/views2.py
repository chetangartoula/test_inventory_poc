from rest_framework.views import APIView
from inventory.serializers import StockInSerializer, StockOutSerializer
from datetime import datetime
from inventory.models import StockInflow, StockOutflow
from rest_framework.response import Response


class StockManager(object):    
    # def get_cdt(self) -> datetime:
    #     return datetime.now()
    
    @staticmethod
    def unique_combined_number(procuct_code, od):
        cd = str(od).split("-")[::-1]
        return "".join(cd) + f"-{procuct_code}"
    
    @staticmethod
    def sequence_number():
        entry_number = StockInflow.objects.all().count()
        return entry_number + 1
    
    @staticmethod
    def identify_batch(data):
        batch_count = (StockInflow.objects
                   .filter(unique_combined_number=data['unique_combined_number'])
                   .count())
        data['batch_number'] = batch_count + 1
        
    # def _distince_stock_in_dates(self):
    #     return StockInflow.objects.values("order_delivery_date").distinct()
    
    def stock_in_map(self, product_code):
        in_map_list = []
        distinct_dates = StockInflow.objects.filter(article_code=product_code).values("order_delivery_date").distinct()
        for date in distinct_dates:
            in_map = {}
            date = date.get("order_delivery_date")
            date_str = str(date)
            in_map.update({"date": date_str, "batches": [], "total_quantity": 0})
            stocks_in_date = StockInflow.objects.filter(order_delivery_date=date).all()
            for stock in stocks_in_date:
                in_map["batches"].extend([{
                    "sequence_number": stock.sequence_number,
                    "quantity": stock.registered_quantity,
                    "batch_number": stock.batch_number
                }])
                in_map["total_quantity"] = in_map["total_quantity"] + stock.registered_quantity
            in_map_list.extend([in_map])
        return in_map_list
    
    def stock_out_map(self, product_code):
        out_map_list = []
        stock_outs = StockOutflow.objects.filter(article_code=product_code).all()
        for stock in stock_outs:
            out_map = {}
            date_str = str(stock.order_delivery_date)
            out_map[date_str] = stock.registered_quantity
            out_map_list.extend([out_map])
        return out_map_list
    
    def manipulate_stock(self, product_code, registered_unit=10):
        stock_out_map = self.stock_out_map(product_code=product_code)
        stock_in_map = self.stock_in_map(product_code=product_code)
        print(stock_in_map)
        print(stock_out_map)
        units_before = 0
        units_after = 0
        for stock_out in stock_out_map:
            ...


class StockInApi(APIView, StockManager):
    serializer_class = StockInSerializer
    stock_type = "Stock In"
    
    def get_queryset(self):
        return StockInflow.objects.all()
    
    def get(self, request, *args, **kwargs):
        query = self.get_queryset()
        serializer = self.serializer_class(query, many=True)
        self.manipulate_stock(product_code="01ab")
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serialzer = self.serializer_class(data=request.data)
        if serialzer.is_valid(raise_exception=True):
            validated_data = serialzer.validated_data
            unique_combined_number = self.unique_combined_number(procuct_code=validated_data['article_code'], od=validated_data['order_delivery_date'])
            sequence_number = self.sequence_number()
            validated_data['unique_combined_number'] = unique_combined_number
            validated_data['sequence_number'] = sequence_number
            self.identify_batch(validated_data)
            stock_in = StockInflow(**validated_data)
            stock_in.save()
        return Response({"data": {"message": "Success"}})
        

class StockOutApi(APIView):
    serializer_class = StockOutSerializer
    stock_type = "Stock Out"
    
    def get_queryset(self):
        return StockOutflow.objects.all()
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            StockOutflow.objects.create(**validated_data)
        return Response({"data": {"message": "Success"}})
        

class StockOverallFlowApi(APIView):
    
    def get(self, requets, *args, **kwargs):
        ...