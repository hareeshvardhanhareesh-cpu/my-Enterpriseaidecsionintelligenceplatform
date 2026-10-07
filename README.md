# Enterprise AI Decision Intelligence Platform

An end-to-end, multi-tier decision intelligence platform engineered for enterprise retail and supply chain analytics. The platform combines predictive customer attrition modeling, financial optimization, inventory risk management, and explainable AI into a unified executive decision system.

---

## Team Structure & Module Responsibilities

The platform is engineered collaboratively by a team of 4 specialists, each owning an autonomous, microservice-ready subsystem:

| Module / Member | Domain | Core Responsibilities | Status |
| :--- | :--- | :--- | :--- |
| **Member 1** | **Customer Intelligence & Churn Prediction** | Customer behavior analysis, churn risk modeling, XAI (SHAP), Django REST API scoring service | **Phase 2 Completed** |
| **Member 2** | **Financial Intelligence & Margin Optimization** | Profitability analysis, dynamic pricing recommendations, discount threshold optimization | Pending Integration |
| **Member 3** | **Supply Chain & Inventory Intelligence** | Demand forecasting, stockout risk prediction, inventory holding cost minimization | Pending Integration |
| **Member 4** | **Unified Executive Dashboard & Decision Engine** | Multi-agent decision synthesis, holistic executive dashboard, centralized API gateway | Pending Integration |

---

## Project Structure

```
my-Enterpriseaidecsionintelligenceplatform-1/
├── backend/                          # Django REST API Backend
│   ├── core_platform/                # Django project settings, URLs, WSGI/ASGI
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/                         # Django application modules
│   │   ├── __init__.py
│   │   └── customer_intelligence/    # Member 1: Churn Prediction API
│   │       ├── models.py             # CustomerPredictionRecord model
│   │       ├── views.py              # API views (predict, batch, history, analytics)
│   │       ├── serializers.py        # DRF input/output serializers
│   │       ├── urls.py               # App-level URL routing
│   │       ├── admin.py              # Django admin configuration
│   │       └── services/
│   │           └── churn_service.py  # Feature engineering & scoring engine
│   ├── manage.py
│   └── db.sqlite3
├── frontend/                         # React UI (future integration)
├── dataset/                          # Raw source datasets
│   └── Cleaned_Superstore.csv
├── data/                             # Processed data artifacts
│   └── processed/
├── models/                           # Trained ML model artifacts (Phase 3+)
│   └── member1_churn/
│       └── churn_model.joblib        # (auto-detected by backend when available)
├── member1_customer_intelligence/    # Member 1: EDA, notebooks, reports
│   ├── notebooks/
│   ├── reports/
│   ├── src/
│   └── data/
├── reports/                          # Cross-module platform reports
├── requirements.txt
└── README.md
```

---

## Prerequisites

- **Python 3.11+** — Verify with `py --version` or `python --version`
- **pip** — Included with Python

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hareeshvardhanhareesh-cpu/my-Enterpriseaidecsionintelligenceplatform.git
cd my-Enterpriseaidecsionintelligenceplatform
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Windows
py -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Start the Django Backend Server

```bash
# Navigate to the backend directory
cd backend

# Run database migrations (first time or after model changes)
py manage.py migrate

# Start the development server on port 8000
py manage.py runserver 8000
```

The server starts at **http://127.0.0.1:8000/**

### Verify the Server is Running

Open your browser or use `curl`:

```bash
curl http://127.0.0.1:8000/api/v1/customer-intelligence/health/
```

Expected response:
```json
{
  "status": "healthy",
  "subsystem": "Member 1 — Customer Intelligence & Churn Prediction",
  "model_mode": "Phase 2 Calibrated Baseline",
  "database_connected": true
}
```

---

## API Endpoints (Customer Intelligence — Member 1)

Base URL: `http://127.0.0.1:8000/api/v1/customer-intelligence/`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health/` | Service health status and model mode |
| `POST` | `/predict/` | Score a single customer transaction for churn risk |
| `POST` | `/batch-predict/` | High-throughput batch scoring for multiple records |
| `GET` | `/history/` | Audit log of past predictions (filterable: `?risk_tier=High`) |
| `GET` | `/analytics/` | Aggregated executive KPIs, risk distribution, regional averages |

### Example: Single Prediction

```bash
curl -X POST http://127.0.0.1:8000/api/v1/customer-intelligence/predict/ ^
  -H "Content-Type: application/json" ^
  -d "{\"customer_id\": \"CUST1042\", \"ship_mode\": \"Standard Class\", \"segment\": \"Consumer\", \"state\": \"Texas\", \"region\": \"Central\", \"category\": \"Furniture\", \"sub_category\": \"Tables\", \"sales\": 450.0, \"quantity\": 3, \"discount\": 0.45, \"sales_category\": \"Medium\"}"
```

**Sample Response (201 Created):**
```json
{
  "status": "success",
  "record_id": 1,
  "customer_id": "CUST1042",
  "churn_prediction": 1,
  "churn_probability": 0.8581,
  "risk_tier": "High",
  "recommended_action": "HIGH ATTRITION RISK. Primary drivers: aggressive markdown rate (45%) ...",
  "model_version": "Phase2-Calibrated-Baseline",
  "engineered_features": {
    "log_sales": 6.1115,
    "sales_per_quantity": 150.0,
    "discount_tier": "High",
    "region_category_interaction": "Central_Furniture"
  }
}
```

### Example: View Prediction History

```bash
curl http://127.0.0.1:8000/api/v1/customer-intelligence/history/?risk_tier=High&limit=10
```

### Example: Analytics Dashboard

```bash
curl http://127.0.0.1:8000/api/v1/customer-intelligence/analytics/
```

### Browsable API (Development)

Navigate to any endpoint URL in your browser (e.g., `http://127.0.0.1:8000/api/v1/customer-intelligence/predict/`) to access DRF's interactive **Browsable API** — a built-in web form for testing requests without `curl`.

---

## Django Admin Panel

### Create a Superuser (First Time)

```bash
cd backend
py manage.py createsuperuser
```

Access the admin panel at: **http://127.0.0.1:8000/admin/**

The admin interface provides a full CRUD dashboard for `CustomerPredictionRecord` with filters by risk tier, region, category, and discount tier.

---

## Running the EDA Pipeline (Member 1)

```bash
# From the project root
py member1_customer_intelligence/src/data_analysis.py
```

Reports are generated in `member1_customer_intelligence/reports/`.

---

## Member 1: Customer Intelligence & Churn Prediction

Member 1's codebase, notebooks, and technical reports are organized under the [`member1_customer_intelligence/`](member1_customer_intelligence/) directory:

- **Interactive Jupyter Notebook:** [`member1_customer_intelligence/notebooks/01_customer_data_analysis.ipynb`](member1_customer_intelligence/notebooks/01_customer_data_analysis.ipynb)
- **Production EDA Script:** [`member1_customer_intelligence/src/data_analysis.py`](member1_customer_intelligence/src/data_analysis.py)
- **Technical EDA Report:** [`member1_customer_intelligence/reports/customer_eda_report.md`](member1_customer_intelligence/reports/customer_eda_report.md)
- **High-Resolution Figures:** [`member1_customer_intelligence/reports/figures/`](member1_customer_intelligence/reports/figures/)
- **Module Documentation:** [`member1_customer_intelligence/README.md`](member1_customer_intelligence/README.md)

---

## Architecture & Future Integration

- **Backend:** Django + Django REST Framework (Python)
- **Frontend (Planned):** React (Vite) communicating via REST JSON contracts
- **CORS:** Pre-configured with `django-cors-headers` for `localhost:5173` (Vite default)
- **Database:** SQLite (development) — swap to PostgreSQL for production
- **Model Upgrades:** When Phase 3 trained models are saved to `models/member1_churn/churn_model.joblib`, the service auto-detects and loads the trained artifact

---

## Troubleshooting

| Issue | Solution |
| :--- | :--- |
| `py` command not found | Use `python` or `python3` instead |
| `ModuleNotFoundError: No module named 'django'` | Run `pip install -r requirements.txt` |
| Migration errors | Run `py manage.py migrate` from the `backend/` directory |
| Port 8000 in use | Use a different port: `py manage.py runserver 8080` |
| CORS errors from React frontend | Verify `CORS_ALLOW_ALL_ORIGINS = True` in `settings.py` |
