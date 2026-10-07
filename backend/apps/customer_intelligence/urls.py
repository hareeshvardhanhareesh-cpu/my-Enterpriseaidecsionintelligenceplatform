"""
URL Routing for Customer Intelligence Module
Enterprise AI Decision Intelligence Platform - Member 1
"""

from django.urls import path
from .views import (
    ChurnPredictionView,
    BatchChurnPredictionView,
    PredictionHistoryView,
    AnalyticsSummaryView,
    HealthCheckView,
)

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='churn_health'),
    path('predict/', ChurnPredictionView.as_view(), name='churn_predict'),
    path('batch-predict/', BatchChurnPredictionView.as_view(), name='churn_batch_predict'),
    path('history/', PredictionHistoryView.as_view(), name='churn_history'),
    path('analytics/', AnalyticsSummaryView.as_view(), name='churn_analytics'),
]
