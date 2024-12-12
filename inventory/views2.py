from rest_framework.views import APIView
from inventory.serializers import StockInSerializer, StockOutSerializer, StockFlowSerializer
from datetime import datetime
from inventory.models import StockInflow, StockOutflow, StockFlowTransitionLog
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
    
    # def stock_in_map_batches(self, product_code):
    #     in_map_list = []
    #     distinct_dates = StockInflow.objects.filter(article_code=product_code).values("order_delivery_date").distinct()
    #     for date in distinct_dates:
    #         in_map = {}
    #         date = date.get("order_delivery_date")
    #         date_str = str(date)
    #         in_map.update({"date": date_str, "batches": [], "total_quantity": 0})
    #         stocks_in_date = StockInflow.objects.filter(order_delivery_date=date).all()
    #         for stock in stocks_in_date:
    #             in_map["batches"].extend([{
    #                 "sequence_number": stock.sequence_number,
    #                 "quantity": stock.registered_quantity,
    #                 "batch_number": stock.batch_number,
    #                 "object": stock
    #             }])
    #             in_map["total_quantity"] = in_map["total_quantity"] + stock.registered_quantity
    #         in_map_list.extend([in_map])
    #     return in_map_list
    
    def stock_in_map(self, product_code):
        in_map_list = []
        stocks_in_date = StockInflow.objects.filter(article_code=product_code).order_by("order_delivery_date").all()
        for stock in stocks_in_date:
            date = stock.order_delivery_date
            date_str = str(date)
            in_map_list.extend([{
                "date": date_str,
                "sequence_number": stock.sequence_number,
                "quantity": stock.registered_quantity,
                "batch_number": stock.batch_number,
                "object": stock
            }])
            
        return in_map_list
    
    def stock_out_map(self, product_code):
        out_map_list = []
        stock_outs = StockOutflow.objects.filter(article_code=product_code).order_by("order_delivery_date").all()
        for stock in stock_outs:
            out_map = {}
            date_str = str(stock.order_delivery_date)
            out_map["date"] = date_str
            out_map["quantity"] = stock.registered_quantity
            out_map["object"] = stock
            out_map_list.extend([out_map])
        return out_map_list
    
    def _check_existing_stock_flow(self, product_code):
        count = StockFlowTransitionLog.objects.filter(article_code=product_code).all().count()
        if count > 0:
            StockFlowTransitionLog.objects.filter(article_code=product_code).delete()
    
    def create_stock_in_log(self, units_before, units_after, in_quantity, stock_obj):
        StockFlowTransitionLog.objects.create(
            article_code=stock_obj.article_code,
            units_before=units_before,
            units_after=units_after,
            registered_units=in_quantity,
            entry_date=stock_obj.order_delivery_date,
            type="Stock In"
        )
        
    def create_stock_out_log(self, units_before, units_after, out_quantity, stock_obj):
        StockFlowTransitionLog.objects.create(
            article_code=stock_obj.article_code,
            units_before=units_before,
            units_after=units_after,
            registered_units=out_quantity,
            entry_date=stock_obj.order_delivery_date,            
            type="Stock Out"
        )
    
    def manipulate_stock_v2(self, product_code):
        """
            To mitigate processing time, over looping
        """
        # self._check_existing_stock_flow(product_code=product_code)        
        stock_out_map = self.stock_out_map(product_code=product_code)
        stock_in_map = self.stock_in_map(product_code=product_code)
        print(stock_in_map)
        print(stock_out_map)
        units_before = 0
        units_after = 0
        index = 0
        previous_out_date = None
        # previous_in_date = None
        
        for stock_out in stock_out_map:
            out_date = stock_out['date']
            out_quantity = stock_out['quantity']
            for _ in range(len(stock_in_map)):
                if index > len(stock_in_map):
                    break
                stock_in = stock_in_map[index]
                in_date = stock_in['date']
                in_quantity = stock_in['quantity']
                
                if previous_out_date:
                    if in_date > previous_out_date and in_date < out_date:
                        index += 1                        
                        ...
                    else:
                        continue
                else:
                    # on first loop
                    # true condition: eg: 2024-12-01 < 2024-12-02
                    if in_date < out_date:
                        index += 1
                        units_before = units_after
                        units_after = units_before + in_quantity
                        self.create_stock_in_log(
                            units_before = units_before,
                            units_after = units_after,
                            in_quantity = in_quantity,
                            stock_obj = stock_in['object']
                        )
                    else:
                        # manipulate stock
                        units_after = units_after - out_quantity #EG: (10-20)
                        self.create_stock_out_log(
                            units_before = units_before,
                            units_after = units_after,
                            out_quantity = out_quantity,
                            stock_obj = stock_out['object']
                        )
                    
            previous_out_date = out_date


    def manipulate_stock_v1(self, product_code):
        self._check_existing_stock_flow(product_code=product_code)        
        stock_out_map = self.stock_out_map(product_code=product_code)
        stock_in_map = self.stock_in_map(product_code=product_code)
        print(stock_in_map)
        print(stock_out_map)
        units_before = 0
        units_after = 0
        index = 0
        
        for stock_out in stock_out_map:
            # breakpoint()
            out_date = stock_out['date']
            out_quantity = stock_out['quantity']
            for _ in range(len(stock_in_map)+1):
                if index > len(stock_in_map) - 1 :
                    break
                stock_in = stock_in_map[index]
                in_date = stock_in['date']
                in_quantity = stock_in['quantity']
                
                # true condition: eg: 2024-12-01 < 2024-12-02
                if in_date <= out_date:
                    index += 1
                    units_before = units_after
                    units_after = units_before + in_quantity
                    self.create_stock_in_log(
                        units_before = units_before,
                        units_after = units_after,
                        in_quantity = in_quantity,
                        stock_obj = stock_in['object']
                    )
                # else:
                #     units_after = units_after - out_quantity #EG: (10-20)
                #     self.create_stock_out_log(
                #         units_before = units_before,
                #         units_after = units_after,
                #         out_quantity = out_quantity,
                #         stock_obj = stock_out['object']
                #     )

            # manipulate stock
            units_before = units_after
            units_after = units_after - out_quantity #EG: (10-20)
            self.create_stock_out_log(
                units_before = units_before,
                units_after = units_after,
                out_quantity = out_quantity,
                stock_obj = stock_out['object']
            )



class StockInApi(APIView, StockManager):
    serializer_class = StockInSerializer
    stock_type = "Stock In"
    
    def get_queryset(self):
        return StockInflow.objects.all()
    
    def get(self, request, *args, **kwargs):
        query = self.get_queryset()
        serializer = self.serializer_class(query, many=True)
        self.manipulate_stock_v1(product_code="ab12")
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
    
    def get(self, request, *args, **kwargs):
        query = self.get_queryset()
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            StockOutflow.objects.create(**validated_data)
        return Response({"data": {"message": "Success"}})
        

class StockOverallFlowApi(APIView):
    serializer_class = StockFlowSerializer
    
    def get_queryset(self):
        return StockFlowTransitionLog.objects.all()
    
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)