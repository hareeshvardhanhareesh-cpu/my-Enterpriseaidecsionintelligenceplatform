# Enterprise AI Decision Intelligence Platform

An end-to-end, multi-tier decision intelligence platform engineered for enterprise retail and supply chain analytics. The platform combines predictive customer attrition modeling, financial optimization, inventory risk management, and explainable AI into a unified executive decision system.

---

## Team Structure & Module Responsibilities

The platform is engineered collaboratively by a team of 4 specialists, each owning an autonomous, microservice-ready subsystem:

| Module / Member | Domain | Core Responsibilities | Status |
| :--- | :--- | :--- | :--- |
| **Member 1** | **Customer Intelligence & Churn Prediction** | Customer behavior analysis, churn risk modeling, XAI (SHAP), FastAPI scoring service | **Phase 1 Completed** |
| **Member 2** | **Financial Intelligence & Margin Optimization** | Profitability analysis, dynamic pricing recommendations, discount threshold optimization | Pending Integration |
| **Member 3** | **Supply Chain & Inventory Intelligence** | Demand forecasting, stockout risk prediction, inventory holding cost minimization | Pending Integration |
| **Member 4** | **Unified Executive Dashboard & Decision Engine** | Multi-agent decision synthesis, holistic executive dashboard, centralized API gateway | Pending Integration |

---

## Member 1: Customer Intelligence & Churn Prediction

Member 1's codebase, notebooks, and technical reports are organized under the [`member1_customer_intelligence/`](member1_customer_intelligence/) directory:

- **Interactive Jupyter Notebook:** [`member1_customer_intelligence/notebooks/01_customer_data_analysis.ipynb`](member1_customer_intelligence/notebooks/01_customer_data_analysis.ipynb)
- **Production EDA Script:** [`member1_customer_intelligence/src/data_analysis.py`](member1_customer_intelligence/src/data_analysis.py)
- **Technical EDA Report:** [`member1_customer_intelligence/reports/customer_eda_report.md`](member1_customer_intelligence/reports/customer_eda_report.md)
- **High-Resolution Figures:** [`member1_customer_intelligence/reports/figures/`](member1_customer_intelligence/reports/figures/)
- **Module Documentation:** [`member1_customer_intelligence/README.md`](member1_customer_intelligence/README.md)

---

## Quickstart & Installation

```bash
# 1. Clone repository
git clone https://github.com/hareeshvardhanhareesh-cpu/my-Enterpriseaidecsionintelligenceplatform.git
cd my-Enterpriseaidecsionintelligenceplatform

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Member 1 EDA Pipeline
python member1_customer_intelligence/src/data_analysis.py
```
