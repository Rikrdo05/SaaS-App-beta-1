import streamlit as st
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

# ===== 1. INPUT FORM =====
st.title("📊 SaaS Financial Model")

with st.form("parameters"):
    # Core Parameters
    kick_off_date = st.date_input("Launch Date", date(2025,1,1))
    subscription_price = st.number_input("Monthly Price ($)", 39.95, format="%.2f")
    free_trial_days = st.slider("Free Trial (Days)", 0, 28, 7)
    
    # Conversion Rates
    trial_to_paid = st.slider("Trial Conversion %", 0.0, 100.0, 25.0) / 100
    churn_rate = st.slider("Monthly Churn %", 0.0, 30.0, 5.0) / 100
    
    # Traffic Inputs
    sem_traffic_m1 = st.number_input("Initial SEM Traffic", 600000)
    seo_traffic_m1 = st.number_input("Initial SEO Traffic", 400000)
    
    if st.form_submit_button("Calculate Projections"):
        st.session_state.calculate = True

# ===== 2. CALCULATIONS =====
if getattr(st.session_state, 'calculate', False):
    months = [kick_off_date + relativedelta(months=i) for i in range(60)]  # 5 years
    
    df = pd.DataFrame({
        "Month": months,
        "SEM Traffic": [sem_traffic_m1 * (1.02 ** (i//12)) for i in range(60)],
        "SEO Traffic": [seo_traffic_m1 * (1.02 ** (i//12)) for i in range(60)],
        "MRR": [subscription_price * 1000 * (1 - churn_rate) ** i for i in range(60)]
    })
    
    # ===== 3. RESULTS =====
    st.success("✅ 5-Year Projections Generated")
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df.head(10).style.format("{:,.0f}"))
    with col2:
        st.line_chart(df, x="Month", y="MRR")
    
    st.download_button("📥 Download CSV", df.to_csv(), "projections.csv")
