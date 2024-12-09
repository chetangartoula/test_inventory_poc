from django.db import models

# Create your models here.
class StockInflow(models.Model):
    article_code = models.CharField(max_length=200)
    article_name = models.CharField(max_length=500)
    registered_quantity = models.FloatField(
        null=True, blank=True, default=0
    )  # Default to 0
    registered_gross_weight = models.FloatField(
        null=True, blank=True, default=0
    )  # Default to 0
    price_amount = models.FloatField(default=0)  # Default to 0 for price amount
    amount_amount = models.FloatField(default=0)  # Default to 0 for amount
    order_code = models.CharField(max_length=255, null=True, blank=True)
    order_relation_code = models.CharField(max_length=200, null=True, blank=True)
    order_relation_name = models.CharField(max_length=255, null=True, blank=True)
    order_delivery_date = models.DateField()
    orderline_code = models.CharField(
        max_length=255, null=True, blank=True
    )  # This will store the code from OrderLines
    packed_per_type = models.CharField(
        max_length=50, null=True, blank=True
    )  # New field for packed per type
    article_quality_name = models.CharField(
        max_length=255, null=True, blank=True
    )  # New field for packed per type
    is_manual_entry = models.BooleanField(
        default=False
    )  # New field to indicate manual entry
    unique_combined_number = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
    type = models.CharField(max_length=50)  # New field for stock type
    sub_type = models.CharField(max_length=100, blank=True, null=True)
    factor = models.FloatField(default=1.0)
    # New field for batch use by date
    batch_use_by_date = models.DateField(null=True, blank=True, default=None)
    # Adding the manual entry type field
    manual_entry_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=[("last", "Last"), ("specific", "Specific")],
    )

class StockOutflow(models.Model):
    article_code = models.CharField(max_length=200)
    article_name = models.CharField(max_length=500)
    registered_quantity = models.FloatField(
        null=True, blank=True, default=0
    )  # Default to 0
    registered_gross_weight = models.FloatField(
        null=True, blank=True, default=0
    )  # Default to 0
    price_amount = models.FloatField(default=0)  # Default to 0 for price amount
    amount_amount = models.FloatField(default=0)  # Default to 0 for amount
    order_code = models.CharField(max_length=255, null=True, blank=True)
    order_delivery_date = models.DateField()
    orderline_code = models.CharField(
        max_length=255, null=True, blank=True
    )  # This will store the code from OrderLines
    packed_per_type = models.CharField(max_length=50, null=True, blank=True)
    article_quality_name = models.CharField(
        max_length=255, null=True, blank=True
    )  # New field for packed per type
    factor = models.FloatField(default=1.0)
    type = models.CharField(max_length=50, default="Sales")
    sub_type = models.CharField(max_length=100, blank=True, null=True)
    unique_combined_number = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
    order_relation_code = models.CharField(max_length=200)
    order_relation_name = models.CharField(max_length=255, null=True, blank=True)
    # New fields for manual entry
    is_manual_entry = models.BooleanField(
        default=False
    )  # Field to indicate if it's a manual entry
    # Constraints for manual_entry_reason
    MANUAL_ENTRY_REASONS = [
        ("damaged", "Damaged"),
        ("lost", "Lost"),
        ("counting", "Counting"),
        ("normal_sale_order", "Normal Sale Order"),
    ]
    manual_entry_reason = models.CharField(
        max_length=500,
        choices=MANUAL_ENTRY_REASONS,
        default="normal_sale_order",
        null=True,
        blank=True,
    )


class StockFlowTransitionLog(models.Model):
    article_code = models.CharField(max_length=200)
    article_name = models.CharField(max_length=500)
    units_before = models.FloatField(null=True, blank=True)
    units_after = models.FloatField(
        null=True, blank=True
    )  # Represents combined quantity/weight value
    registered_units = models.FloatField(null=True, default=0)
    type = models.CharField(max_length=50)
    batch_number_stock_in = models.CharField(
        max_length=255, null=True, blank=True
    )  # Allow NULL for batch number
    entry_date = models.DateField(
        null=True, blank=True
    )  # New field for entry date (order_delivery_date)
    unique_combined_number = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )  # New field for unique_combined_number
    sequence_number = models.PositiveIntegerField(default=0)
    packed_per_type = models.CharField(
        max_length=50, null=True, blank=True
    )  # New field to track packaging type
    order_relation_code = models.CharField(
        max_length=200, null=True
    )  # Track the order relation code
    order_relation_name = models.CharField(
        max_length=255, null=True, blank=True
    )  # Track the order relation name
    is_manual_entry = models.BooleanField(
        default=False
    )  # Track if this is a manual entry

    manual_entry_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=[("last", "Last"), ("specific", "Specific")],
    )  # Type of manual entry (last or specific)
    # New field to track the reason for manual entry
    # New field to track the reason for manual entry
    manual_entry_reason = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=[
            ("normal_sale_order", "Normal Sale Order"),
            ("normal_purchase_order", "Normal Purchase Order"),
            ("damaged", "Damaged"),
            ("lost", "Lost"),
            ("counting", "Counting"),
        ],
    )
