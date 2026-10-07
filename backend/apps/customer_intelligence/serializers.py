"""
Serializers for Customer Intelligence & Churn Prediction
Enterprise AI Decision Intelligence Platform - Member 1
"""

from rest_framework import serializers
from .models import CustomerPredictionRecord


# Standard domain choices from validated dataset
VALID_SHIP_MODES = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
VALID_SEGMENTS = ['Consumer', 'Corporate', 'Home Office']
VALID_REGIONS = ['Central', 'East', 'South', 'West']
VALID_CATEGORIES = ['Furniture', 'Office Supplies', 'Technology']
VALID_SALES_CATEGORIES = ['Low', 'Medium', 'High', 'Very High']


class CustomerPredictionRequestSerializer(serializers.Serializer):
    """
    Validates incoming customer transaction features for churn scoring.
    Strictly accepts only the verified leakage-safe operational inputs.
    """
    customer_id = serializers.CharField(
        max_length=64, required=False, allow_blank=True, default='',
        help_text="Optional customer identifier for tracking"
    )
    ship_mode = serializers.ChoiceField(
        choices=VALID_SHIP_MODES, default='Standard Class',
        help_text="Fulfillment speed: Standard Class, Second Class, First Class, Same Day"
    )
    segment = serializers.ChoiceField(
        choices=VALID_SEGMENTS, default='Consumer',
        help_text="Customer profile tier: Consumer, Corporate, Home Office"
    )
    state = serializers.CharField(
        max_length=64, default='California',
        help_text="US State of transaction"
    )
    region = serializers.ChoiceField(
        choices=VALID_REGIONS, default='West',
        help_text="Macro-geographic territory: Central, East, South, West"
    )
    category = serializers.ChoiceField(
        choices=VALID_CATEGORIES, default='Office Supplies',
        help_text="Merchandise department: Furniture, Office Supplies, Technology"
    )
    sub_category = serializers.CharField(
        max_length=64, default='Binders',
        help_text="Granular product line (e.g., Binders, Tables, Phones)"
    )
    sales = serializers.FloatField(
        min_value=0.01, default=100.0,
        help_text="Gross invoice amount in USD"
    )
    quantity = serializers.IntegerField(
        min_value=1, default=2,
        help_text="Number of units purchased (>= 1)"
    )
    discount = serializers.FloatField(
        min_value=0.0, max_value=1.0, default=0.0,
        help_text="Promotional markdown rate between 0.00 and 1.00"
    )
    sales_category = serializers.ChoiceField(
        choices=VALID_SALES_CATEGORIES, default='Medium',
        help_text="Transaction magnitude tier: Low, Medium, High, Very High"
    )

    def validate(self, attrs):
        # Auto-compute sales_category if not explicitly provided or defaulted
        sales = attrs.get('sales', 100.0)
        if 'sales_category' not in attrs or not attrs['sales_category']:
            if sales <= 100.0:
                attrs['sales_category'] = 'Low'
            elif sales <= 500.0:
                attrs['sales_category'] = 'Medium'
            elif sales <= 1000.0:
                attrs['sales_category'] = 'High'
            else:
                attrs['sales_category'] = 'Very High'
        return attrs


class BatchPredictionRequestSerializer(serializers.Serializer):
    """
    Validates a batch list of customer transactions.
    """
    records = CustomerPredictionRequestSerializer(many=True)


class CustomerPredictionRecordSerializer(serializers.ModelSerializer):
    """
    Serializes persisted prediction records for history and dashboards.
    """
    class Meta:
        model = CustomerPredictionRecord
        fields = '__all__'


class PredictionResponseSerializer(serializers.Serializer):
    """
    Standard API output format for single prediction.
    """
    record_id = serializers.IntegerField(required=False)
    customer_id = serializers.CharField(allow_blank=True)
    churn_prediction = serializers.IntegerField()
    churn_probability = serializers.FloatField()
    risk_tier = serializers.CharField()
    recommended_action = serializers.CharField()
    model_version = serializers.CharField()
    engineered_features = serializers.DictField()
