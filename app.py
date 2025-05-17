import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar

# ===== FORM INPUTS =====
st.title("SaaS Financial Model Generator")

# Date Selection
date_options = pd.date_range(start="2025-01-01", end="2040-12-01", freq="MS")
kick_off_str = st.selectbox("Web/App Kick-off Date", options=date_options.strftime("%Y-%m-%d"))
kick_off_date = datetime.strptime(kick_off_str, "%Y-%m-%d").date()

# Core Parameters
col1, col2 = st.columns(2)
with col1:
    free_trial_days = st.number_input("Free Trial (days)", 0, 28, 7)
    subscription_price = st.number_input("Subscription Price $", 0.0, 1000.0, 39.95, 0.01)
    sem_cost_metric = st.selectbox("SEM Cost Metric", ["CPC", "CPA"], index=1)
    
with col2:
    trial_to_paid = st.number_input("Trial-To-Paid Rate %", 0.0, 100.0, 25.0, 0.1) / 100
    churn_rate = st.number_input("Monthly Churn Rate %", 0.0, 100.0, 5.0, 0.1) / 100
    sem_cpa = st.number_input("SEM CPA Cost", 0.0, 100.0, 26.0, 0.1)

# Traffic Inputs
st.subheader("Traffic Parameters")
traffic_cols = st.columns(3)
with traffic_cols[0]:
    sem_traffic_m1 = st.number_input("Initial SEM Traffic", 0, 10000000, 600000)
    sem_cr_y1 = st.number_input("SEM Conv. Rate Y1%", 0.0, 100.0, 4.0, 0.1) / 100
    
with traffic_cols[1]:
    seo_traffic_m1 = st.number_input("Initial SEO Traffic", 0, 10000000, 400000)
    seo_cr_y1 = st.number_input("SEO Conv. Rate Y1%", 0.0, 100.0, 4.0, 0.1) / 100
    
with traffic_cols[2]:
    subs_affiliate_m1 = st.number_input("Affiliate Subs", 0, 100000, 10000)
    affiliate_cpa = st.number_input("Affiliate CPA", 0.0, 50.0, 11.0, 0.1)

# ===== CALCULATION FUNCTIONS =====
def calculate_growth(base_value, month_idx, annual_growth_rates):
    """Calculate compounded growth"""
    years = month_idx // 12
    if years >= len(annual_growth_rates): years = len(annual_growth_rates) - 1
    return base_value * (1 + annual_growth_rates[years]) ** (month_idx / 12)

def generate_financial_model():
    # Initialize DataFrame
    months = [kick_off_date + relativedelta(months=i) for i in range(60)]  # 5 years
    
    df = pd.DataFrame({
        "Month": months,
        "Days": [calendar.monthrange(m.year, m.month)[1] for m in months]
    })
    
    # Your full financial model calculations here...
    # Add all the logic from your original script
    
    return df

# ===== RUN MODEL =====
if st.button("Generate Projections"):
    with st.spinner("Calculating 5-year projections..."):
        results_df = generate_financial_model()
        
        st.success("Done!")
        st.dataframe(results_df.style.format("{:,.2f}"))
        
        # Add visualizations
        st.line_chart(results_df[["Total Monthly Recurring Revenue MRR"]])
        st.download_button("Download CSV", results_df.to_csv(), "financial_projections.csv")
