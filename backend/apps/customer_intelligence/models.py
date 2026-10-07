"""
Customer Intelligence Models
Enterprise AI Decision Intelligence Platform - Member 1
"""

from django.db import models


class CustomerPredictionRecord(models.Model):
    """
    Stores historical customer churn predictions, input features,
    and recommended retention interventions for auditing and executive dashboards.
    """
    RISK_TIER_CHOICES = [
        ('Low', 'Low Risk (< 25%)'),
        ('Medium', 'Medium Risk (25% - 50%)'),
        ('High', 'High Risk (> 50%)'),
    ]

    # Optional business identifier
    customer_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)

    # Raw Operational Features (Verified Pre-Sale Set)
    ship_mode = models.CharField(max_length=32)
    segment = models.CharField(max_length=32)
    state = models.CharField(max_length=64)
    region = models.CharField(max_length=32)
    category = models.CharField(max_length=64)
    sub_category = models.CharField(max_length=64)
    sales_category = models.CharField(max_length=32)
    sales = models.FloatField()
    quantity = models.IntegerField()
    discount = models.FloatField()

    # Engineered Features (Phase 2 Pipeline)
    log_sales = models.FloatField()
    sales_per_quantity = models.FloatField()
    discount_tier = models.CharField(max_length=32)
    region_category_interaction = models.CharField(max_length=128)

    # Prediction Outputs
    churn_prediction = models.IntegerField(help_text="0 for Retained, 1 for Churned")
    churn_probability = models.FloatField(help_text="Predicted probability between 0.0 and 1.0")
    risk_tier = models.CharField(max_length=16, choices=RISK_TIER_CHOICES, default='Low')
    recommended_action = models.TextField(blank=True, default='')

    # Metadata
    model_version = models.CharField(max_length=32, default='v1.0-pre-release')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer Prediction Record'
        verbose_name_plural = 'Customer Prediction Records'

    def __str__(self):
        cid = self.customer_id or f"ID-{self.pk}"
        return f"{cid} | Prob: {self.churn_probability:.2%} | Tier: {self.risk_tier}"
