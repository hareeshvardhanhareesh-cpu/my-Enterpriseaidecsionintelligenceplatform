"""
API Views for Customer Intelligence & Churn Prediction
Enterprise AI Decision Intelligence Platform - Member 1
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg

from .models import CustomerPredictionRecord
from .serializers import (
    CustomerPredictionRequestSerializer,
    BatchPredictionRequestSerializer,
    CustomerPredictionRecordSerializer,
)
from .services.churn_service import ChurnPredictionService


class ChurnPredictionView(APIView):
    """
    POST /api/v1/customer-intelligence/predict/
    
    Accepts operational customer and order parameters, computes Phase 2
    engineered features, evaluates churn probability and risk tier,
    persists the audit log, and returns actionable retention guidance.
    """
    def post(self, request):
        serializer = CustomerPredictionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": "error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        service = ChurnPredictionService.get_instance()
        result = service.predict(validated_data)

        # Persist prediction in the database for auditing and dashboard analytics
        eng = result["engineered_features"]
        record = CustomerPredictionRecord.objects.create(
            customer_id=validated_data.get("customer_id", ""),
            ship_mode=validated_data.get("ship_mode", ""),
            segment=validated_data.get("segment", ""),
            state=validated_data.get("state", ""),
            region=validated_data.get("region", ""),
            category=validated_data.get("category", ""),
            sub_category=validated_data.get("sub_category", ""),
            sales_category=validated_data.get("sales_category", ""),
            sales=validated_data.get("sales", 0.0),
            quantity=validated_data.get("quantity", 1),
            discount=validated_data.get("discount", 0.0),
            log_sales=eng.get("log_sales", 0.0),
            sales_per_quantity=eng.get("sales_per_quantity", 0.0),
            discount_tier=eng.get("discount_tier", "Zero"),
            region_category_interaction=eng.get("region_category_interaction", ""),
            churn_prediction=result["churn_prediction"],
            churn_probability=result["churn_probability"],
            risk_tier=result["risk_tier"],
            recommended_action=result["recommended_action"],
            model_version=result["model_version"],
        )

        response_payload = {
            "status": "success",
            "record_id": record.id,
            "customer_id": record.customer_id,
            "churn_prediction": result["churn_prediction"],
            "churn_probability": result["churn_probability"],
            "risk_tier": result["risk_tier"],
            "recommended_action": result["recommended_action"],
            "model_version": result["model_version"],
            "engineered_features": eng,
            "created_at": record.created_at,
        }

        return Response(response_payload, status=status.HTTP_201_CREATED)


class BatchChurnPredictionView(APIView):
    """
    POST /api/v1/customer-intelligence/batch-predict/
    
    Accepts an array of customer records for high-throughput batch scoring.
    """
    def post(self, request):
        serializer = BatchPredictionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": "error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        records_data = serializer.validated_data["records"]
        service = ChurnPredictionService.get_instance()
        results = []
        high_risk_count = 0

        for item in records_data:
            res = service.predict(item)
            eng = res["engineered_features"]
            rec = CustomerPredictionRecord.objects.create(
                customer_id=item.get("customer_id", ""),
                ship_mode=item.get("ship_mode", ""),
                segment=item.get("segment", ""),
                state=item.get("state", ""),
                region=item.get("region", ""),
                category=item.get("category", ""),
                sub_category=item.get("sub_category", ""),
                sales_category=item.get("sales_category", ""),
                sales=item.get("sales", 0.0),
                quantity=item.get("quantity", 1),
                discount=item.get("discount", 0.0),
                log_sales=eng.get("log_sales", 0.0),
                sales_per_quantity=eng.get("sales_per_quantity", 0.0),
                discount_tier=eng.get("discount_tier", "Zero"),
                region_category_interaction=eng.get("region_category_interaction", ""),
                churn_prediction=res["churn_prediction"],
                churn_probability=res["churn_probability"],
                risk_tier=res["risk_tier"],
                recommended_action=res["recommended_action"],
                model_version=res["model_version"],
            )
            if res["risk_tier"] == "High":
                high_risk_count += 1

            results.append({
                "record_id": rec.id,
                "customer_id": rec.customer_id,
                "churn_prediction": res["churn_prediction"],
                "churn_probability": res["churn_probability"],
                "risk_tier": res["risk_tier"],
            })

        return Response({
            "status": "success",
            "total_processed": len(results),
            "high_risk_count": high_risk_count,
            "predictions": results,
        }, status=status.HTTP_200_OK)


class PredictionHistoryView(APIView):
    """
    GET /api/v1/customer-intelligence/history/
    
    Returns recent customer risk evaluations, filterable by risk tier.
    """
    def get(self, request):
        risk_filter = request.query_params.get("risk_tier", None)
        limit = int(request.query_params.get("limit", 50))

        queryset = CustomerPredictionRecord.objects.all()
        if risk_filter:
            queryset = queryset.filter(risk_tier=risk_filter.capitalize())

        queryset = queryset[:limit]
        serializer = CustomerPredictionRecordSerializer(queryset, many=True)
        return Response({
            "status": "success",
            "count": len(serializer.data),
            "records": serializer.data
        }, status=status.HTTP_200_OK)


class AnalyticsSummaryView(APIView):
    """
    GET /api/v1/customer-intelligence/analytics/
    
    Provides executive dashboard metrics: risk distribution,
    average churn probability, and regional risk hotspots.
    """
    def get(self, request):
        total = CustomerPredictionRecord.objects.count()
        if total == 0:
            return Response({
                "status": "success",
                "total_records": 0,
                "message": "No customer assessments recorded yet. Run predictions to populate analytics."
            })

        tier_counts = (
            CustomerPredictionRecord.objects
            .values("risk_tier")
            .annotate(count=Count("id"))
        )
        avg_prob = CustomerPredictionRecord.objects.aggregate(avg=Avg("churn_probability"))["avg"] or 0.0

        regional_breakdown = (
            CustomerPredictionRecord.objects
            .values("region")
            .annotate(
                total=Count("id"),
                avg_prob=Avg("churn_probability")
            )
        )

        return Response({
            "status": "success",
            "total_assessments": total,
            "overall_avg_churn_probability": round(avg_prob, 4),
            "risk_tier_distribution": {item["risk_tier"]: item["count"] for item in tier_counts},
            "regional_breakdown": list(regional_breakdown),
        }, status=status.HTTP_200_OK)


class HealthCheckView(APIView):
    """
    GET /api/v1/customer-intelligence/health/
    
    Microservice heartbeat check.
    """
    def get(self, request):
        service = ChurnPredictionService.get_instance()
        return Response({
            "status": "healthy",
            "subsystem": "Member 1 — Customer Intelligence & Churn Prediction",
            "model_mode": "Trained ML Model" if service._model_loaded else "Phase 2 Calibrated Baseline",
            "database_connected": True,
        }, status=status.HTTP_200_OK)
