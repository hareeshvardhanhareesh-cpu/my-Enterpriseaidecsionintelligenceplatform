"""
Django Admin Registration for Customer Intelligence
"""

from django.contrib import admin
from .models import CustomerPredictionRecord


@admin.register(CustomerPredictionRecord)
class CustomerPredictionRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer_id', 'risk_tier', 'churn_probability', 
        'churn_prediction', 'region', 'category', 'discount_tier', 'created_at'
    )
    list_filter = ('risk_tier', 'churn_prediction', 'region', 'category', 'discount_tier', 'created_at')
    search_fields = ('customer_id', 'state', 'sub_category')
    readonly_fields = (
        'created_at', 'log_sales', 'sales_per_quantity', 
        'discount_tier', 'region_category_interaction'
    )
