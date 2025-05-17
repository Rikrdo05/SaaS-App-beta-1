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
        sem_cost_metric = st.selectbox("SEM Cost Metric", ["CPC", "CPA"], index=1)
    
    with col2:
        free_trial_days = st.slider("Free Trial (Days)", 0, 28, 7)
        trial_to_paid = st.slider("Trial Conversion %", 0.0, 100.0, 25.0) / 100
        churn_rate = st.slider("Monthly Churn %", 0.0, 30.0, 5.0) / 100
    
    # Traffic Inputs - New Section
    st.subheader("Traffic Parameters")
    traffic_col1, traffic_col2, traffic_col3 = st.columns(3)
    
    with traffic_col1:
        sem_traffic_m1 = st.number_input("Initial SEM Traffic", 600000)
    with traffic_col2:
        seo_traffic_m1 = st.number_input("Initial SEO Traffic", 400000)
    with traffic_col3:
        subs_affiliate_m1 = st.number_input("Subscriptions from Affiliate Marketing", 10000)
    
    # Growth Rates Section
    st.subheader("Monthly Growth Rates")
    
    # SEM Growth Rates
    st.markdown("**SEM/Web Traffic Growth**")
    sem_cols = st.columns(5)
    with sem_cols[0]:
        sem_gr_y1 = st.number_input("Year 1", 0.0, 100.0, 2.0, key="sem_y1") / 100
    with sem_cols[1]:
        sem_gr_y2 = st.number_input("Year 2", 0.0, 100.0, 2.0, key="sem_y2") / 100
    with sem_cols[2]:
        sem_gr_y3 = st.number_input("Year 3", 0.0, 100.0, 2.0, key="sem_y3") / 100
    with sem_cols[3]:
        sem_gr_y4 = st.number_input("Year 4", 0.0, 100.0, 2.0, key="sem_y4") / 100
    with sem_cols[4]:
        sem_gr_y5 = st.number_input("Year 5", 0.0, 100.0, 2.0, key="sem_y5") / 100
    
    # SEO Growth Rates
    st.markdown("**SEO/Web Traffic Growth**")
    seo_cols = st.columns(5)
    with seo_cols[0]:
        seo_gr_y1 = st.number_input("Year 1", 0.0, 100.0, 2.0, key="seo_y1") / 100
    with seo_cols[1]:
        seo_gr_y2 = st.number_input("Year 2", 0.0, 100.0, 2.0, key="seo_y2") / 100
    with seo_cols[2]:
        seo_gr_y3 = st.number_input("Year 3", 0.0, 100.0, 2.0, key="seo_y3") / 100
    with seo_cols[3]:
        seo_gr_y4 = st.number_input("Year 4", 0.0, 100.0, 2.0, key="seo_y4") / 100
    with seo_cols[4]:
        seo_gr_y5 = st.number_input("Year 5", 0.0, 100.0, 2.0, key="seo_y5") / 100
    
    # Affiliate Growth Rates
    st.markdown("**Affiliate Subscriptions Growth**")
    aff_cols = st.columns(5)
    with aff_cols[0]:
        aff_gr_y1 = st.number_input("Year 1", 0.0, 100.0, 2.0, key="aff_y1") / 100
    with aff_cols[1]:
        aff_gr_y2 = st.number_input("Year 2", 0.0, 100.0, 2.0, key="aff_y2") / 100
    with aff_cols[2]:
        aff_gr_y3 = st.number_input("Year 3", 0.0, 100.0, 2.0, key="aff_y3") / 100
    with aff_cols[3]:
        aff_gr_y4 = st.number_input("Year 4", 0.0, 100.0, 2.0, key="aff_y4") / 100
    with aff_cols[4]:
        aff_gr_y5 = st.number_input("Year 5", 0.0, 100.0, 2.0, key="aff_y5") / 100

    if st.form_submit_button("Calculate Projections"):
        st.session_state.calculate = True

# ===== 2. CALCULATIONS =====
if getattr(st.session_state, 'calculate', False):
    # Your existing calculations here...
    months = [kick_off_date + relativedelta(months=i) for i in range(60)]
    
    df = pd.DataFrame({
        "Month": months,
        "SEM Traffic": [sem_traffic_m1 * (1 + sem_gr_y1) ** i if i < 12 else 
                       sem_traffic_m1 * (1 + sem_gr_y2) ** (i-12) if i < 24 else
                       sem_traffic_m1 * (1 + sem_gr_y3) ** (i-24) if i < 36 else
                       sem_traffic_m1 * (1 + sem_gr_y4) ** (i-36) if i < 48 else
                       sem_traffic_m1 * (1 + sem_gr_y5) ** (i-48) for i in range(60)],
        
        "SEO Traffic": [seo_traffic_m1 * (1 + seo_gr_y1) ** i if i < 12 else 
                       seo_traffic_m1 * (1 + seo_gr_y2) ** (i-12) if i < 24 else
                       seo_traffic_m1 * (1 + seo_gr_y3) ** (i-24) if i < 36 else
                       seo_traffic_m1 * (1 + seo_gr_y4) ** (i-36) if i < 48 else
                       seo_traffic_m1 * (1 + seo_gr_y5) ** (i-48) for i in range(60)],
        
        "Affiliate Subs": [subs_affiliate_m1 * (1 + aff_gr_y1) ** i if i < 12 else 
                          subs_affiliate_m1 * (1 + aff_gr_y2) ** (i-12) if i < 24 else
                          subs_affiliate_m1 * (1 + aff_gr_y3) ** (i-24) if i < 36 else
                          subs_affiliate_m1 * (1 + aff_gr_y4) ** (i-36) if i < 48 else
                          subs_affiliate_m1 * (1 + aff_gr_y5) ** (i-48) for i in range(60)],
        
        "MRR": [subscription_price * 1000 * (1 - churn_rate) ** i for i in range(60)]
    })
    
    # ===== 3. RESULTS =====
    st.success("✅ Projections Generated")
    
    st.write("### Growth Rates Summary")
    growth_df = pd.DataFrame({
        "Year": [1, 2, 3, 4, 5],
        "SEM Growth": [sem_gr_y1, sem_gr_y2, sem_gr_y3, sem_gr_y4, sem_gr_y5],
        "SEO Growth": [seo_gr_y1, seo_gr_y2, seo_gr_y3, seo_gr_y4, seo_gr_y5],
        "Affiliate Growth": [aff_gr_y1, aff_gr_y2, aff_gr_y3, aff_gr_y4, aff_gr_y5]
    })
    st.dataframe(growth_df.style.format("{:.2%}"))
    
    st.write("### First Year Projections")
    st.dataframe(df.head(12).style.format("{:,.0f}"))
    
    st.line_chart(df, x="Month", y=["SEM Traffic", "SEO Traffic", "Affiliate Subs"])
