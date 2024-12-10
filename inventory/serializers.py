from rest_framework import serializers

from inventory.models import StockInflow,StockFlowTransitionLog, StockOutflow



class StockInSerializer(serializers.Serializer):
    ENTRY_CHOICES = (
        ("damage", "Damaged"),
        ("lost", "Lost"),
        ("counting", "Counting"),
        ("normal sale order", "Normal Sale Order"),
    )

    article_code = serializers.CharField(
        label="Product Code"
    )

    registered_quantity = serializers.CharField(label="Registered Quantity")
    registered_gross_weight = serializers.CharField(
        label="Registered Gross Weight",
    )
    order_relation_code = serializers.CharField(
        label="Order Relation Code",
        
    )
    order_delivery_date = serializers.DateField(
        label="Order Delivery Date",
        # input_formats=["%d-%m-%Y"],
       
    )
    # stock_in_out = serializers.ChoiceField(
    #     choices=[("in", "IN"), ("out", "OUT")],
    # )
    batch_use_by_date = serializers.DateField(
        label="Batch Use By Date",
        # input_formats=["%d-%m-%Y"],
       
        required=False,
    )



    def create(self, validated_data):
        # validated_data.pop("stock_in_out")
       
        formatted_date = validated_data.get("order_delivery_date")
        article_code = validated_data.get("article_code")
        unique_combined_number = f"{article_code}-{formatted_date.strftime('%Y%m%d')}"
        existing_entry = StockInflow.objects.filter(
                article_code=article_code,
                order_delivery_date=formatted_date,
            ).count()
        if existing_entry > 0:
            sequence_number = existing_entry + 1
            unique_combined_number += (
                f"-{str(sequence_number)}"
            )
        validated_data['packed_per_type']= "Quantity"
        validated_data["manual_entry_type"]= True
        validated_data['unique_combined_number'] = unique_combined_number
        obj = StockInflow.objects.create(**validated_data)

        return obj
    


    


class StockOutSerializer(serializers.Serializer):
    ENTRY_CHOICES = (
        ("damage", "Damaged"),
        ("lost", "Lost"),
        ("counting", "Counting"),
        ("normal sale order", "Normal Sale Order"),
    )

    article_code = serializers.CharField(
        label="Product Code"
    )

    registered_quantity = serializers.CharField(label="Registered Quantity")
    registered_gross_weight = serializers.CharField(
        label="Registered Gross Weight",
    )
    order_relation_code = serializers.CharField(
        label="Order Relation Code",
        
    )
    # stock_in_out = serializers.ChoiceField(
    #     choices=[("in", "IN"), ("out", "OUT")],
    #     initial="out",
    # )
    order_delivery_date = serializers.DateField(
        label="Order Delivery Date",
        # input_formats=["%d-%m-%Y"],
        
    )
    manual_entry_reason = serializers.ChoiceField(
        choices=ENTRY_CHOICES,
        
    )


    def create(self, validated_data):
        formatted_date = validated_data.get("order_delivery_date")
        article_code = validated_data.get("article_code")
        unique_combined_number = f"{article_code}-{formatted_date.strftime('%Y%m%d')}"
        existing_entry = StockInflow.objects.filter(
                article_code=article_code,
                order_delivery_date=formatted_date,
            ).count()
        if existing_entry > 0:
            sequence_number = existing_entry + 1
            unique_combined_number += (
                f"-{str(sequence_number)}"
            )
        validated_data['packed_per_type']= "Quantity"
        # validated_data["manual_entry_type"]= True
        
        validated_data['unique_combined_number'] = unique_combined_number
        obj = StockOutflow.objects.create(**validated_data)

        return obj