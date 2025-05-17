import streamlit as st
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

# ===== 1. INPUT FORM =====
st.title("📊 SaaS Financial Model")

with st.form("parameters"):
    # Core Parameters - Column 1
    col1, col2 = st.columns(2)
    
    with col1:
        kick_off_date = st.date_input("Web/App Kick-off Date", date(2025,1,1))
        subscription_price = st.number_input("Subscription Price ($)", 39.95, format="%.2f")
        sem_cost_metric = st.selectbox("SEM Cost Metric", ["CPC", "CPA"], index=1)  # <-- ADDED HERE
    
    with col2:
        free_trial_days = st.slider("Free Trial (Days)", 0, 28, 7)
        trial_to_paid = st.slider("Trial Conversion %", 0.0, 100.0, 25.0) / 100
        churn_rate = st.slider("Monthly Churn %", 0.0, 30.0, 5.0) / 100
    
    # Traffic Inputs - New Section
    st.subheader("Traffic Parameters")
    traffic_col1, traffic_col2 = st.columns(2)
    
    with traffic_col1:
        sem_traffic_m1 = st.number_input("Initial SEM Traffic", 600000)
        sem_cpa = st.number_input("SEM CPA Cost", 26.0) if sem_cost_metric == "CPA" else None
    
    with traffic_col2:
        seo_traffic_m1 = st.number_input("Initial SEO Traffic", 400000)
        affiliate_cpa = st.number_input("Affiliate CPA", 11.0)

    if st.form_submit_button("Calculate Projections"):
        st.session_state.calculate = True

# ===== 2. CALCULATIONS =====
if getattr(st.session_state, 'calculate', False):
    # Your existing calculations here...
    months = [kick_off_date + relativedelta(months=i) for i in range(60)]
    
    df = pd.DataFrame({
        "Month": months,
        "SEM Traffic": [sem_traffic_m1 * (1.02 ** (i//12)) for i in range(60)],
        "SEO Traffic": [seo_traffic_m1 * (1.02 ** (i//12)) for i in range(60)],
        "MRR": [subscription_price * 1000 * (1 - churn_rate) ** i for i in range(60)],
        "SEM Cost Metric": sem_cost_metric  # <-- Included in output
    })
    
    # ===== 3. RESULTS =====
    st.success("✅ Projections Generated")
    
    st.write("### Key Inputs")
    st.json({
        "SEM Cost Metric": sem_cost_metric,
        "Subscription Price": f"${subscription_price:.2f}",
        "Free Trial Days": free_trial_days
    })
    
    st.dataframe(df.head(12))  # Show first year
    st.line_chart(df, x="Month", y="MRR")
