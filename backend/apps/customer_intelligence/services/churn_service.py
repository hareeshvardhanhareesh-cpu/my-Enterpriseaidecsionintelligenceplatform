"""
Churn Prediction & Feature Processing Service
Enterprise AI Decision Intelligence Platform - Member 1
"""

import os
import math
import logging
from typing import Dict, Any, Tuple
from django.conf import settings

logger = logging.getLogger(__name__)


class ChurnPredictionService:
    """
    Singleton service managing feature transformation, model inference,
    and business recommendation generation for customer intelligence.
    """
    _instance = None
    _model = None
    _model_loaded = False

    @classmethod
    def get_instance(cls) -> "ChurnPredictionService":
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._load_model_if_available()
        return cls._instance

    def _load_model_if_available(self) -> None:
        """
        Attempts to load a trained model artifact from the central models directory.
        """
        model_paths = [
            os.path.join(settings.BASE_DIR, "..", "models", "member1_churn", "churn_model.joblib"),
            os.path.join(settings.BASE_DIR, "ml_models", "churn_model.joblib"),
        ]

        for p in model_paths:
            if os.path.exists(p):
                try:
                    import joblib
                    self._model = joblib.load(p)
                    self._model_loaded = True
                    logger.info(f"Loaded trained churn model from {p}")
                    return
                except Exception as e:
                    logger.warning(f"Failed to load model from {p}: {e}")

        logger.info("No trained model artifact found yet. Operating in Phase 2 baseline scoring mode.")
        self._model = None
        self._model_loaded = False

    @staticmethod
    def compute_engineered_features(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes the verified Phase 2 engineered features:
        - log_sales = ln(1 + max(sales, 0))
        - sales_per_quantity = sales / quantity
        - discount_tier = Zero (0), Low (0-0.20), Moderate (0.20-0.40), High (>0.40)
        - region_category_interaction = region + "_" + category
        """
        sales = float(data.get("sales", 0.0))
        quantity = int(data.get("quantity", 1))
        discount = float(data.get("discount", 0.0))
        region = str(data.get("region", "")).strip()
        category = str(data.get("category", "")).strip()

        # 1. log_sales
        log_sales = math.log1p(max(sales, 0.0))

        # 2. sales_per_quantity (safe division)
        safe_qty = max(quantity, 1)
        sales_per_quantity = sales / safe_qty if safe_qty > 0 else 0.0

        # 3. discount_tier (fixed business rules, independent of target)
        if discount <= 0.0:
            discount_tier = "Zero"
        elif discount <= 0.20:
            discount_tier = "Low"
        elif discount <= 0.40:
            discount_tier = "Moderate"
        else:
            discount_tier = "High"

        # 4. region_category_interaction
        region_category_interaction = f"{region}_{category}"

        return {
            "log_sales": round(log_sales, 4),
            "sales_per_quantity": round(sales_per_quantity, 4),
            "discount_tier": discount_tier,
            "region_category_interaction": region_category_interaction,
        }

    def predict(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes end-to-end customer churn risk assessment.
        """
        engineered = self.compute_engineered_features(raw_data)
        merged_payload = {**raw_data, **engineered}

        # If a trained model is present, score with it
        if self._model_loaded and self._model is not None:
            try:
                import pandas as pd
                df_input = pd.DataFrame([merged_payload])
                prob = float(self._model.predict_proba(df_input)[0][1])
                prediction = int(prob >= 0.35)
                model_used = "Trained-ML-Artifact"
            except Exception as e:
                logger.error(f"Inference error with trained model: {e}. Falling back to baseline scoring.")
                prob, prediction, model_used = self._baseline_risk_score(merged_payload)
        else:
            prob, prediction, model_used = self._baseline_risk_score(merged_payload)

        # Risk tier classification
        if prob >= 0.50:
            risk_tier = "High"
        elif prob >= 0.25:
            risk_tier = "Medium"
        else:
            risk_tier = "Low"

        # Strategic retention recommendation
        recommendation = self._generate_retention_recommendation(
            risk_tier=risk_tier,
            discount=merged_payload.get("discount", 0.0),
            discount_tier=engineered["discount_tier"],
            region_category=engineered["region_category_interaction"],
            sales_per_qty=engineered["sales_per_quantity"]
        )

        return {
            "input_features": raw_data,
            "engineered_features": engineered,
            "churn_prediction": prediction,
            "churn_probability": round(prob, 4),
            "risk_tier": risk_tier,
            "recommended_action": recommendation,
            "model_version": model_used,
        }

    def _baseline_risk_score(self, features: Dict[str, Any]) -> Tuple[float, int, str]:
        """
        Phase 2 calibrated statistical baseline scoring.
        Calibrated against Phase 1 & 2 verified empirical distributions:
        - Base population churn rate: 11.42%
        - Strong association with high discount tiers (>30%)
        - Regional product category interactions (e.g. Central Furniture: 38.1%)
        - Lower average sales value per purchased unit
        """
        discount = float(features.get("discount", 0.0))
        sales_per_qty = float(features.get("sales_per_quantity", 0.0))
        reg_cat = features.get("region_category_interaction", "")

        # Base log-odds for ~11.4% base rate (logit ≈ -2.05)
        log_odds = -2.05

        # Discount contribution
        if discount > 0.40:
            log_odds += 2.80  # Substantially elevated risk in deep clearance
        elif discount > 0.20:
            log_odds += 1.10  # Moderate elevation
        elif discount > 0.0:
            log_odds += 0.20

        # Region-category interaction contribution (empirical associations)
        if reg_cat == "Central_Furniture":
            log_odds += 1.45  # 38.1% empirical rate
        elif reg_cat in ("Central_Office Supplies", "East_Technology"):
            log_odds += 0.65  # ~21% empirical rate
        elif reg_cat == "West_Technology":
            log_odds -= 1.20  # ~1.3% empirical rate

        # Unit revenue sensitivity
        if sales_per_qty < 20.0:
            log_odds += 0.35  # Commodity transaction risk
        elif sales_per_qty > 100.0:
            log_odds -= 0.40  # High ticket customer commitment

        # Sigmoid transform to probability
        prob = 1.0 / (1.0 + math.exp(-log_odds))
        prob = max(0.01, min(0.99, prob))
        prediction = 1 if prob >= 0.35 else 0

        return prob, prediction, "Phase2-Calibrated-Baseline"

    @staticmethod
    def _generate_retention_recommendation(
        risk_tier: str,
        discount: float,
        discount_tier: str,
        region_category: str,
        sales_per_qty: float
    ) -> str:
        """
        Produces actionable business retention guidance.
        """
        if risk_tier == "High":
            reasons = []
            if discount > 0.30:
                reasons.append(f"aggressive markdown rate ({discount:.0%}) indicates opportunistic purchase pattern")
            if "Central" in region_category:
                reasons.append(f"vulnerable regional category dynamic ({region_category})")
            if sales_per_qty < 25.0:
                reasons.append("low realized unit price")

            detail = "; ".join(reasons) if reasons else "elevated operational churn indicators"
            return (
                f"HIGH ATTRITION RISK. Primary drivers: {detail}. "
                "Action: Trigger proactive outreach, assign dedicated account manager, "
                "and audit post-sale fulfillment experience."
            )
        elif risk_tier == "Medium":
            return (
                f"MODERATE ATTRITION RISK (Discount Tier: {discount_tier}). "
                "Action: Enroll customer into loyalty engagement sequence and offer tailored product warranties."
            )
        else:
            return (
                "LOW ATTRITION RISK. Account health is stable. "
                "Action: Maintain standard communication schedule and explore upsell/cross-sell opportunities."
            )
