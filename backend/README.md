# Enterprise AI Decision Intelligence Platform — Backend Service

## Overview
This is the core Django REST Framework (DRF) backend for the **Enterprise AI Decision Intelligence Platform**. It provides modular, decoupled microservices for customer intelligence, risk assessment, and executive analytics.

---

## Quickstart

### 1. Run Migrations
```bash
py manage.py migrate
```

### 2. Start the Development Server
```bash
py manage.py runserver 8000
```
Server runs at `http://127.0.0.1:8000/`.

---

## API Endpoints (Customer Intelligence & Churn — Member 1)

Base URL: `http://127.0.0.1:8000/api/v1/customer-intelligence/`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health/` | Service health status and model mode |
| `POST` | `/predict/` | Score a single customer transaction and receive risk & action guidance |
| `POST` | `/batch-predict/` | High-throughput batch scoring for multiple records |
| `GET` | `/history/` | Audit log of past predictions (filterable by `?risk_tier=High`) |
| `GET` | `/analytics/` | Aggregated executive KPIs, risk tier counts, and regional averages |

---

## Sample Request: Single Prediction (`POST /api/v1/customer-intelligence/predict/`)

```json
{
  "customer_id": "CUST1042",
  "ship_mode": "Standard Class",
  "segment": "Consumer",
  "state": "Texas",
  "region": "Central",
  "category": "Furniture",
  "sub_category": "Tables",
  "sales": 450.0,
  "quantity": 3,
  "discount": 0.45,
  "sales_category": "Medium"
}
```

### Sample Response (`201 Created`):
```json
{
  "status": "success",
  "record_id": 1,
  "customer_id": "CUST1042",
  "churn_prediction": 1,
  "churn_probability": 0.8581,
  "risk_tier": "High",
  "recommended_action": "HIGH ATTRITION RISK. Primary drivers: aggressive markdown rate (45%) indicates opportunistic purchase pattern; vulnerable regional category dynamic (Central_Furniture). Action: Trigger proactive outreach, assign dedicated account manager, and audit post-sale fulfillment experience.",
  "model_version": "Phase2-Calibrated-Baseline",
  "engineered_features": {
    "log_sales": 6.1115,
    "sales_per_quantity": 150.0,
    "discount_tier": "High",
    "region_category_interaction": "Central_Furniture"
  },
  "created_at": "2026-10-07T17:28:47.563426Z"
}
```

---

## Architecture & Integration with Future React UI
- **CORS Support:** Pre-configured with `django-cors-headers` for `localhost:5173` (Vite / React default).
- **Decoupled:** React frontend communicates via standard REST JSON contracts.
- **Model Upgrades:** Model logic lives in `apps/customer_intelligence/services/churn_service.py`. When Phase 3 final models are trained and saved to `models/member1_churn/churn_model.joblib`, the service automatically detects and loads the trained artifact.
