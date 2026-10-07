"""
URL configuration for core_platform project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response


class APIRootView(APIView):
    """
    GET /
    Platform API index — lists all available services and endpoints.
    """
    def get(self, request):
        base = request.build_absolute_uri('/').rstrip('/')
        return Response({
            "platform": "Enterprise AI Decision Intelligence Platform",
            "version": "v1",
            "services": {
                "customer_intelligence": {
                    "base_url": f"{base}/api/v1/customer-intelligence/",
                    "endpoints": {
                        "health": f"{base}/api/v1/customer-intelligence/health/",
                        "predict": f"{base}/api/v1/customer-intelligence/predict/",
                        "batch_predict": f"{base}/api/v1/customer-intelligence/batch-predict/",
                        "history": f"{base}/api/v1/customer-intelligence/history/",
                        "analytics": f"{base}/api/v1/customer-intelligence/analytics/",
                    }
                }
            },
            "admin": f"{base}/admin/",
        })


urlpatterns = [
    path('', APIRootView.as_view(), name='api_root'),
    path('admin/', admin.site.urls),
    path('api/v1/customer-intelligence/', include('apps.customer_intelligence.urls')),
]
