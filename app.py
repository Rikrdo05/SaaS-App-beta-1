import streamlit as st
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import calendar
import plotly.graph_objects as go
import plotly.express as px

# Initialize session state for multi-page form
if 'page' not in st.session_state:
    st.session_state.page = 1
    st.session_state.form_data = {}

# Page 1: Core Parameters and Traffic Inputs
if st.session_state.page == 1:
    st.title("📊 SaaS Financial Model - Part 1/2")
    
    with st.form("part1"):
        # Core Parameters - Column 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.form_data['kick_off_date'] = st.date_input("Web/App Kick-off Date", date(2025,1,1))
            st.session_state.form_data['subscription_price'] = st.number_input("Subscription Price ($)", 39.95, format="%.2f")
            st.session_state.form_data['sem_cost_metric'] = st.selectbox("SEM Cost Metric", ["CPC", "CPA"], index=1)
        
        with col2:
            st.session_state.form_data['free_trial_days'] = st.slider("Free Trial (Days)", 0, 28, 7)
            st.session_state.form_data['trial_to_paid'] = st.slider("Trial Conversion %", 0.0, 100.0, 25.0) / 100
            st.session_state.form_data['churn_rate'] = st.slider("Monthly Churn %", 0.0, 30.0, 5.0) / 100
        
        # Traffic Inputs
        st.subheader("Traffic Parameters")
        traffic_col1, traffic_col2, traffic_col3 = st.columns(3)
        
        with traffic_col1:
            st.session_state.form_data['sem_traffic_m1'] = st.number_input("Initial SEM Traffic", 600000)
        with traffic_col2:
            st.session_state.form_data['seo_traffic_m1'] = st.number_input("Initial SEO Traffic", 400000)
        with traffic_col3:
            st.session_state.form_data['subs_affiliate_m1'] = st.number_input("Subscriptions from Affiliate Marketing", 10000)
        
        # Growth Rates Section
        st.subheader("Monthly Growth Rates")
        
        # SEM Growth Rates
        st.markdown("**SEM/Web Traffic Growth**")
        sem_cols = st.columns(5)
        with sem_cols[0]:
            st.session_state.form_data['sem_gr_y1'] = st.number_input("Year 1", 0.0, 100.0, 2.0, key="sem_y1") / 100
        with sem_cols[1]:
            st.session_state.form_data['sem_gr_y2'] = st.number_input("Year 2", 0.0, 100.0, 2.0, key="sem_y2") / 100
        with sem_cols[2]:
            st.session_state.form_data['sem_gr_y3'] = st.number_input("Year 3", 0.0, 100.0, 2.0, key="sem_y3") / 100
        with sem_cols[3]:
            st.session_state.form_data['sem_gr_y4'] = st.number_input("Year 4", 0.0, 100.0, 2.0, key="sem_y4") / 100
        with sem_cols[4]:
            st.session_state.form_data['sem_gr_y5'] = st.number_input("Year 5", 0.0, 100.0, 2.0, key="sem_y5") / 100
        
        # SEO Growth Rates
        st.markdown("**SEO/Web Traffic Growth**")
        seo_cols = st.columns(5)
        with seo_cols[0]:
            st.session_state.form_data['seo_gr_y1'] = st.number_input("Year 1", 0.0, 100.0, 2.0, key="seo_y1") / 100
        with seo_cols[1]:
            st.session_state.form_data['seo_gr_y2'] = st.number_input("Year 2", 0.0, 100.0, 2.0, key="seo_y2") / 100
        with seo_cols[2]:
            st.session_state.form_data['seo_gr_y3'] = st.number_input("Year 3", 0.0, 100.0, 2.0, key="seo_y3") / 100
        with seo_cols[3]:
            st.session_state.form_data['seo_gr_y4'] = st.number_input("Year 4", 0.0, 100.0, 2.0, key="seo_y4") / 100
        with seo_cols[4]:
            st.session_state.form_data['seo_gr_y5'] = st.number_input("Year 5", 0.0, 100.0, 2.0, key="seo_y5") / 100
        
        # Affiliate Growth Rates
        st.markdown("**Affiliate Subscriptions Growth**")
        aff_cols = st.columns(5)
        with aff_cols[0]:
            st.session_state.form_data['aff_gr_y1'] = st.number_input("Year 1", 0.0, 100.0, 2.0, key="aff_y1") / 100
        with aff_cols[1]:
            st.session_state.form_data['aff_gr_y2'] = st.number_input("Year 2", 0.0, 100.0, 2.0, key="aff_y2") / 100
        with aff_cols[2]:
            st.session_state.form_data['aff_gr_y3'] = st.number_input("Year 3", 0.0, 100.0, 2.0, key="aff_y3") / 100
        with aff_cols[3]:
            st.session_state.form_data['aff_gr_y4'] = st.number_input("Year 4", 0.0, 100.0, 2.0, key="aff_y4") / 100
        with aff_cols[4]:
            st.session_state.form_data['aff_gr_y5'] = st.number_input("Year 5", 0.0, 100.0, 2.0, key="aff_y5") / 100

        if st.form_submit_button("Next →"):
            st.session_state.page = 2
            st.rerun()

# Page 2: Conversion Rates and Cost Assumptions
elif st.session_state.page == 2:
    st.title("📊 SaaS Financial Model - Part 2/2")
    
    with st.form("part2"):
        # Conversion Rates Section
        st.subheader("Conversion Rate Assumptions")
        
        # SEM Conversion Rates
        st.markdown("**SEM Conversion Rates**")
        sem_cr_cols = st.columns(5)
        with sem_cr_cols[0]:
            st.session_state.form_data['sem_cr_y1'] = st.number_input("Year 1", 0.0, 100.0, 4.0, key="sem_cr_y1") / 100
        with sem_cr_cols[1]:
            st.session_state.form_data['sem_cr_y2'] = st.number_input("Year 2", 0.0, 100.0, 4.5, key="sem_cr_y2") / 100
        with sem_cr_cols[2]:
            st.session_state.form_data['sem_cr_y3'] = st.number_input("Year 3", 0.0, 100.0, 5.0, key="sem_cr_y3") / 100
        with sem_cr_cols[3]:
            st.session_state.form_data['sem_cr_y4'] = st.number_input("Year 4", 0.0, 100.0, 5.5, key="sem_cr_y4") / 100
        with sem_cr_cols[4]:
            st.session_state.form_data['sem_cr_y5'] = st.number_input("Year 5", 0.0, 100.0, 6.0, key="sem_cr_y5") / 100
        
        # SEO Conversion Rates
        st.markdown("**SEO Conversion Rates**")
        seo_cr_cols = st.columns(5)
        with seo_cr_cols[0]:
            st.session_state.form_data['seo_cr_y1'] = st.number_input("Year 1", 0.0, 100.0, 4.0, key="seo_cr_y1") / 100
        with seo_cr_cols[1]:
            st.session_state.form_data['seo_cr_y2'] = st.number_input("Year 2", 0.0, 100.0, 4.5, key="seo_cr_y2") / 100
        with seo_cr_cols[2]:
            st.session_state.form_data['seo_cr_y3'] = st.number_input("Year 3", 0.0, 100.0, 5.0, key="seo_cr_y3") / 100
        with seo_cr_cols[3]:
            st.session_state.form_data['seo_cr_y4'] = st.number_input("Year 4", 0.0, 100.0, 5.5, key="seo_cr_y4") / 100
        with seo_cr_cols[4]:
            st.session_state.form_data['seo_cr_y5'] = st.number_input("Year 5", 0.0, 100.0, 6.0, key="seo_cr_y5") / 100
        
        # Cost Assumptions Section
        st.subheader("Cost Assumptions")
        cost_col1, cost_col2 = st.columns(2)
        
        with cost_col1:
            st.session_state.form_data['sem_cpa'] = st.number_input("SEM CPA ($)", 26.0, format="%.2f")
            st.session_state.form_data['affiliate_cpa'] = st.number_input("Affiliate Marketing Pay-per-Subscription ($)", 11.0, format="%.2f")
            st.session_state.form_data['ccp_rate'] = st.number_input("Credit Card Processing Cost (%)", 6.0, format="%.2f") / 100
            st.session_state.form_data['refund_rate'] = st.number_input("Refund Rate (%)", 1.0, format="%.2f") / 100
            
        with cost_col2:
            st.session_state.form_data['chb_rate'] = st.number_input("Chargeback Rate (%)", 0.5, format="%.2f") / 100
            st.session_state.form_data['monthly_web_hosting_cost'] = st.number_input("Monthly Web Hosting Cost ($)", 300)
            st.session_state.form_data['monthly_techsoft_cost'] = st.number_input("Monthly Technology & Software Cost ($)", 1000)
            st.session_state.form_data['monthly_labor_cost'] = st.number_input("Monthly Labor Cost ($)", 10000)
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("← Back"):
                st.session_state.page = 1
                st.rerun()
        with col2:
            if st.form_submit_button("Calculate Projections"):
                st.session_state.calculate = True

# Calculations and Results
