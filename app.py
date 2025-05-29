import streamlit as st
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import calendar
import plotly.graph_objects as go
import plotly.express as px
import textwrap

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Assumptions"

if "form_data" not in st.session_state:
    st.session_state.form_data = {}

if "calculate" not in st.session_state:
    st.session_state.calculate = False

st.title("📊 SaaS Financial Model")

with st.form("single_page_form", clear_on_submit=False):
    # Core Parameters - Column 1
    st.subheader("Core Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        # Year selection only
        current_year = date.today().year
        years = list(range(current_year, current_year + 6))  # Next 5 years
        selected_year = st.selectbox("Launch Year", years, index=1)  # Default to next year
        
        # Create and store the date object (always January 1st of selected year)
        kick_off_date = date(int(selected_year), 1, 1)  # Fixed to January (month=1)
        
        # Store in session state
        st.session_state.form_data['kick_off_date'] = kick_off_date
        st.session_state.form_data['subscription_price'] = st.number_input("Monthly Subscription Price ($)",min_value=0.0,value=25.5,step=0.5, format="%.2f")


    
    with col2:
        st.session_state.form_data['free_trial_days'] = st.number_input("Subscription Free Trial (Days)", min_value=0, max_value=28,value=7,step=1)
        st.session_state.form_data['trial_to_paid'] = st.number_input("Monthly Trial To Paid Rate %", min_value=0, max_value=100,value=25,step=5) / 100
        st.session_state.form_data['churn_rate'] = st.number_input("Monthly Churn Rate%", min_value=0.1, max_value=100,value=25,step=5) / 100      
        
    
    # Traffic Inputs
    st.subheader("Web/App Traffic Parameters")
    traffic_col1, traffic_col2, traffic_col3 = st.columns(3)
    
    with traffic_col1:
        st.session_state.form_data['sem_traffic_m1'] = st.number_input(
            "Paid Traffic (SEM Traffic) - First Month", min_value=0, 
            value=100000, step=1000, format="%d")
    with traffic_col2:
        st.session_state.form_data['seo_traffic_m1'] = st.number_input(
            "Organic Traffic (SEO Traffic) - First Month", min_value=0, 
            value=100000, step=1000, format="%d")
    with traffic_col3:
        st.session_state.form_data['am_traffic_m1'] = st.number_input(
            "Affiliate Marketing Traffic - First Month (Traffic coming from another website)", min_value=0, 
            value=10000, step=1000, format="%d")    
    
    # Growth Rates Section
    st.subheader("Web/App Traffic Monthly Growth Rates by Year")
    st.write("Note: A 1% monthly growth rate is approximately equivalent to 12% annual growth rate")
    # SEM Growth Rates
    st.markdown("**Web/App Paid Traffic (SEM Traffic) Monthly Growth Rate by Year**")
    _cols = st.columns(5)
    with _cols[0]:
        st.session_state.form_data['sem_traffic_gr_y1'] = st.number_input("Monthly Growth Rate - Year 1 (%)", 0.0, 100.0, 2.0, 0.5, key="_y1") / 100
    with _cols[1]:
        st.session_state.form_data['sem_traffic_gr_y2'] = st.number_input("Monthly Growth Rate - Year 2 (%)", 0.0, 100.0, 2.0, 0.5, key="_y2") / 100
    with _cols[2]:
        st.session_state.form_data['sem_traffic_gr_y3'] = st.number_input("Monthly Growth Rate - Year 3 (%)", 0.0, 100.0, 2.0, 0.5, key="sem_y3") / 100
    with _cols[3]:
        st.session_state.form_data['sem_traffic_gr_y4'] = st.number_input("Monthly Growth Rate - Year 4 (%)", 0.0, 100.0, 2.0, 0.5, key="sem_y4") / 100
    with _cols[4]:
        st.session_state.form_data['sem_traffic_gr_y5'] = st.number_input("Monthly Growth Rate - Year 5 (%)", 0.0, 100.0, 2.0, 0.5, key="sem_y5") / 100
    
    # SEO Growth Rates
    st.markdown("**Web/App Organic Traffic (SEO Traffic) Monthly Growth Rate by Year**")
    seo_cols = st.columns(5)
    with seo_cols[0]:
        st.session_state.form_data['seo_traffic_gr_y1'] = st.number_input("Monthly Growth Rate - Year 1 (%)", 0.0, 100.0, 2.0, 0.5, key="seo_y1") / 100
    with seo_cols[1]:
        st.session_state.form_data['seo_traffic_gr_y2'] = st.number_input("Monthly Growth Rate - Year 2 (%)", 0.0, 100.0, 2.0, 0.5, key="seo_y2") / 100
    with seo_cols[2]:
        st.session_state.form_data['seo_traffic_gr_y3'] = st.number_input("Monthly Growth Rate - Year 3 (%)", 0.0, 100.0, 2.0, 0.5, key="seo_y3") / 100
    with seo_cols[3]:
        st.session_state.form_data['seo_traffic_gr_y4'] = st.number_input("Monthly Growth Rate - Year 4 (%)", 0.0, 100.0, 2.0, 0.5, key="seo_y4") / 100
    with seo_cols[4]:
        st.session_state.form_data['seo_traffic_gr_y5'] = st.number_input("Monthly Growth Rate - Year 5 (%)", 0.0, 100.0, 2.0, 0.5, key="seo_y5") / 100
    
    # Affiliate Marketing Growth Rates
    st.markdown("**Web/App Affiliate Marketing Traffic Monthly Growth Rate by Year**")
    am_cols = st.columns(5)
    with am_cols[0]:
        st.session_state.form_data['am_traffic_gr_y1'] = st.number_input("Monthly Growth Rate - Year 1 (%)", 0.0, 100.0, 2.0, 0.5, key="am_y1") / 100
    with am_cols[1]:
        st.session_state.form_data['am_traffic_gr_y2'] = st.number_input("Monthly Growth Rate - Year 2 (%)", 0.0, 100.0, 2.0, 0.5, key="am_y2") / 100
    with am_cols[2]:
        st.session_state.form_data['am_traffic_gr_y3'] = st.number_input("Monthly Growth Rate - Year 3 (%)", 0.0, 100.0, 2.0, 0.5, key="am_y3") / 100
    with am_cols[3]:
        st.session_state.form_data['am_traffic_gr_y4'] = st.number_input("Monthly Growth Rate - Year 4 (%)", 0.0, 100.0, 2.0, 0.5, key="am_y4") / 100
    with am_cols[4]:
        st.session_state.form_data['am_traffic_gr_y5'] = st.number_input("Monthly Growth Rate - Year 5 (%)", 0.0, 100.0, 2.0, 0.5, key="am_y5") / 100
    
    # Conversion Rates Section
    st.subheader("Conversion Rate Assumptions (Traffic-to-Trial Rate %)")
    
    # SEM Conversion Rates
    st.markdown("**Paid Traffic (SEM Traffic) Conversion Rates**")
    sem_cr_cols = st.columns(5)
    with sem_cr_cols[0]:
        st.session_state.form_data['sem_cr_y1'] = st.number_input("Year 1 (%)", 0.0, 100.0, 4.0, 0.5, key="sem_cr_y1") / 100
    with sem_cr_cols[1]:
        st.session_state.form_data['sem_cr_y2'] = st.number_input("Year 2 (%)", 0.0, 100.0, 4.5, 0.5, key="sem_cr_y2") / 100
    with sem_cr_cols[2]:
        st.session_state.form_data['sem_cr_y3'] = st.number_input("Year 3 (%)", 0.0, 100.0, 5.0, 0.5, key="sem_cr_y3") / 100
    with sem_cr_cols[3]:
        st.session_state.form_data['sem_cr_y4'] = st.number_input("Year 4 (%)", 0.0, 100.0, 5.5, 0.5, key="sem_cr_y4") / 100
    with sem_cr_cols[4]:
        st.session_state.form_data['sem_cr_y5'] = st.number_input("Year 5 (%)", 0.0, 100.0, 6.0, 0.5, key="sem_cr_y5") / 100
    
    # SEO Conversion Rates
    st.markdown("**Organic Tradffic (SEO Traffic) Conversion Rates**")
    seo_cr_cols = st.columns(5)
    with seo_cr_cols[0]:
        st.session_state.form_data['seo_cr_y1'] = st.number_input("Year 1 (%)", 0.0, 100.0, 4.0, 0.5, key="seo_cr_y1") / 100
    with seo_cr_cols[1]:
        st.session_state.form_data['seo_cr_y2'] = st.number_input("Year 2 (%)", 0.0, 100.0, 4.5, 0.5, key="seo_cr_y2") / 100
    with seo_cr_cols[2]:
        st.session_state.form_data['seo_cr_y3'] = st.number_input("Year 3 (%)", 0.0, 100.0, 5.0, 0.5, key="seo_cr_y3") / 100
    with seo_cr_cols[3]:
        st.session_state.form_data['seo_cr_y4'] = st.number_input("Year 4 (%)", 0.0, 100.0, 5.5, 0.5, key="seo_cr_y4") / 100
    with seo_cr_cols[4]:
        st.session_state.form_data['seo_cr_y5'] = st.number_input("Year 5 (%)", 0.0, 100.0, 6.0, 0.5, key="seo_cr_y5") / 100

    # Affiliate Marketing Conversion Rates
    st.markdown("**Affiliate Marketing Traffic Conversion Rates**")
    am_cr_cols = st.columns(5)
    with am_cr_cols[0]:
        st.session_state.form_data['am_cr_y1'] = st.number_input("Year 1 (%)", 0.0, 100.0, 4.0, 0.5, key="am_cr_y1") / 100
    with am_cr_cols[1]:
        st.session_state.form_data['am_cr_y2'] = st.number_input("Year 2 (%)", 0.0, 100.0, 4.5, 0.5, key="am_cr_y2") / 100
    with am_cr_cols[2]:
        st.session_state.form_data['am_cr_y3'] = st.number_input("Year 3 (%)", 0.0, 100.0, 5.0, 0.5, key="am_cr_y3") / 100
    with am_cr_cols[3]:
        st.session_state.form_data['am_cr_y4'] = st.number_input("Year 4 (%)", 0.0, 100.0, 5.5, 0.5, key="am_cr_y4") / 100
    with am_cr_cols[4]:
        st.session_state.form_data['am_cr_y5'] = st.number_input("Year 5 (%)", 0.0, 100.0, 6.0, 0.5, key="am_cr_y5") / 100

    

    # Cost Assumptions Section
    st.subheader("Cost Assumptions")
    cost_col1, cost_col2 = st.columns(2)
    
    with cost_col1:
        st.session_state.form_data['sem_cpa'] = st.number_input("SEM Customer Acquisition Cost - CAC ($)", min_value=0.0, value=20.0, step=0.5, format="%.2f")
        st.session_state.form_data['affiliate_cpa'] = st.number_input("Affiliate Marketing Customer Acquisition Cost - CAC ($)", min_value=0.0, value=11.0, step=0.5, format="%.2f")
        st.session_state.form_data['ccp_rate'] = st.number_input("Credit Card Processing Cost (% of Revenue)", min_value=0.0, value=10.0, step=0.5, format="%.2f") / 100
        st.session_state.form_data['refund_rate'] = st.number_input("Refund Rate (% of Revenue)", min_value=0.0, value=5.0, step=0.5, format="%.2f") / 100
        
    with cost_col2:
        st.session_state.form_data['chb_rate'] = st.number_input("Chargeback Rate (% of Revenue)", min_value=0.0, value=0.5, step=0.5, format="%.2f") / 100
        st.session_state.form_data['monthly_web_hosting_cost'] = st.number_input("Monthly Web Hosting Cost ($)", min_value=0, value=300, step=50)
        st.session_state.form_data['monthly_techsoft_cost'] = st.number_input("Monthly Technology & Software Cost ($)", min_value=0, value=300, step=50)
        st.session_state.form_data['monthly_labor_cost'] = st.number_input("Monthly Labor Cost ($)", min_value=0, value=10000, step=1000)

    # Other Revenue Sources
    st.subheader("Other Revenue - Ad Network (e.g, Google AdSense)")
    st.write("Set the below values to 0.00 if Ad Network is not part of your revenue model")
    AdNet_col1, AdNet_col2 = st.columns(2)
    
    with AdNet_col1:
        st.session_state.form_data['views per visit'] = st.number_input("Page Views Per Visit", min_value=0.0, value=0.0, step=0.5, format="%.2f")
        
    with AdNet_col2:
        st.session_state.form_data['cpm'] = st.number_input("Revenue Per Mile/1,000 Impressions - RPM Revenue ($)", min_value=0.0, value=5.0, step=0.5, format="%.2f")
        

    # Other Revenue Sources
    st.subheader("Other Revenue - Affiliate Marketing (Promoting an specific merchant/Website/App)")
    st.write("Set the below values to 0.00 if you are not promoting any third party merchant/website/App")
    AdAF_col1, AdAF_col2 = st.columns(2)
    
    with AdAF_col1:
        st.session_state.form_data['am_ctr'] = st.number_input("Affiliate Ad Click-Trough Rate CTR %", min_value=0.0, value=0.0, step=0.5, format="%.2f") / 100
        st.session_state.form_data['am_cpa'] = st.number_input("Affiliate Comission Per Action CPA Revenue ($)", min_value=0.0, value=0.0, step=0.5, format="%.2f")
 
    with AdAF_col2:
        st.session_state.form_data['am_ocr'] = st.number_input("Affiliate Offer Conversion Rate %", min_value=0.0, value=0.0, step=0.5, format="%.2f") / 100
     
           
    # Calculate button - FIXED VERSION
    if st.form_submit_button("Calculate Projections"):
        st.session_state.calculate = True
        st.rerun()



# Calculations and Results
if st.session_state.calculate:
    # Extract all variables from session state
    form_data = st.session_state.form_data
    kick_off_date = form_data['kick_off_date']
    subscription_price = form_data['subscription_price']
    free_trial_days = form_data['free_trial_days']
    trial_to_paid = form_data['trial_to_paid']
    churn_rate = form_data['churn_rate']
    sem_traffic_m1 = form_data['sem_traffic_m1']
    seo_traffic_m1 = form_data['seo_traffic_m1']
    am_traffic_m1 = form_data['am_traffic_m1']
    sem_traffic_gr_y1 = form_data['sem_traffic_gr_y1']
    sem_traffic_gr_y2 = form_data['sem_traffic_gr_y2']
    sem_traffic_gr_y3 = form_data['sem_traffic_gr_y3']
    sem_traffic_gr_y4 = form_data['sem_traffic_gr_y4']
    sem_traffic_gr_y5 = form_data['sem_traffic_gr_y5']
    seo_traffic_gr_y1 = form_data['seo_traffic_gr_y1']
    seo_traffic_gr_y2 = form_data['seo_traffic_gr_y2']
    seo_traffic_gr_y3 = form_data['seo_traffic_gr_y3']
    seo_traffic_gr_y4 = form_data['seo_traffic_gr_y4']
    seo_traffic_gr_y5 = form_data['seo_traffic_gr_y5']
    am_traffic_gr_y1 = form_data['am_traffic_gr_y1']
    am_traffic_gr_y2 = form_data['am_traffic_gr_y2']
    am_traffic_gr_y3 = form_data['am_traffic_gr_y3']
    am_traffic_gr_y4 = form_data['am_traffic_gr_y4']
    am_traffic_gr_y5 = form_data['am_traffic_gr_y5']
    sem_cr_y1 = form_data['sem_cr_y1']
    sem_cr_y2 = form_data['sem_cr_y2']
    sem_cr_y3 = form_data['sem_cr_y3']
    sem_cr_y4 = form_data['sem_cr_y4']
    sem_cr_y5 = form_data['sem_cr_y5']
    seo_cr_y1 = form_data['seo_cr_y1']
    seo_cr_y2 = form_data['seo_cr_y2']
    seo_cr_y3 = form_data['seo_cr_y3']
    seo_cr_y4 = form_data['seo_cr_y4']
    seo_cr_y5 = form_data['seo_cr_y5']
    am_cr_y1 = form_data['am_cr_y1']
    am_cr_y2 = form_data['am_cr_y2']
    am_cr_y3 = form_data['am_cr_y3']
    am_cr_y4 = form_data['am_cr_y4']
    am_cr_y5 = form_data['am_cr_y5']
    sem_cpa = form_data['sem_cpa']
    affiliate_cpa = form_data['affiliate_cpa']
    ccp_rate = form_data['ccp_rate']
    refund_rate = form_data['refund_rate']
    chb_rate = form_data['chb_rate']
    monthly_web_hosting_cost = form_data['monthly_web_hosting_cost']
    monthly_techsoft_cost = form_data['monthly_techsoft_cost']
    monthly_labor_cost = form_data['monthly_labor_cost']
    views_per_visit=0.000000001 if form_data['views per visit'] == 0 else form_data['views per visit']
    cpm=0 if form_data['views per visit'] == 0 else form_data['cpm']
    
    
    am_ctr=form_data['am_ctr']
    am_cpa=form_data['am_cpa']
    am_ocr=form_data['am_ocr']
    renewal_rate = 1 - churn_rate
    LTV = (subscription_price * trial_to_paid) / (1 - renewal_rate)
    sem_roi=LTV-sem_cpa 
    if sem_cpa == 0:
        sem_roi_percent = None 
    else: 
        sem_roi_percent = sem_roi / sem_cpa
    affiliate_marketing_roi=LTV-affiliate_cpa
    
    if affiliate_cpa == 0:
        affiliate_marketing_roi_percent = None 
    else: 
        affiliate_marketing_roi_percent = affiliate_marketing_roi/affiliate_cpa

    # First, let's create a function to determine the growth rate based on the month index
    def get_sem_growth_rate(month_idx):
        if month_idx <= 11:  # Year 1
            return 1 + sem_traffic_gr_y1 if sem_traffic_gr_y1 != 0 else 1
        elif month_idx <= 23:  # Year 2
            return 1 + sem_traffic_gr_y2 if sem_traffic_gr_y2 != 0 else 1
        elif month_idx <= 35:  # Year 3
            return 1 + sem_traffic_gr_y3 if sem_traffic_gr_y3 != 0 else 1
        elif month_idx <= 47:  # Year 4
            return 1 + sem_traffic_gr_y4 if sem_traffic_gr_y4 != 0 else 1
        else:  # Year 5
            return 1 + sem_traffic_gr_y5 if sem_traffic_gr_y5 != 0 else 1

    def get_sem_cr(month_idx):
        if month_idx <= 11:    # Year 1
            return sem_cr_y1 
        elif month_idx <= 23:  # Year 2
            return sem_cr_y2
        elif month_idx <= 35:  # Year 3
            return sem_cr_y3
        elif month_idx <= 47:  # Year 4
            return sem_cr_y4
        else:                  # Year 5
            return sem_cr_y5  

    def get_seo_growth_rate(month_idx):
        if month_idx <= 11:  # Year 1
            return 1 + seo_traffic_gr_y1
        elif month_idx <= 23:  # Year 2
            return 1 + seo_traffic_gr_y2
        elif month_idx <= 35:  # Year 3
            return 1 + seo_traffic_gr_y3
        elif month_idx <= 47:  # Year 4
            return 1 + seo_traffic_gr_y4
        else:  # Year 5
            return 1 + seo_traffic_gr_y5

    def get_seo_cr(month_idx):
        if month_idx <= 11:    # Year 1
            return seo_cr_y1
        elif month_idx <= 23:  # Year 2
            return seo_cr_y2
        elif month_idx <= 35:  # Year 3
            return seo_cr_y3
        elif month_idx <= 47:  # Year 4
            return seo_cr_y4
        else:                  # Year 5
            return seo_cr_y5      

    def get_am_growth_rate(month_idx):
        if month_idx <= 11:  # Year 1
            return 1 + am_traffic_gr_y1
        elif month_idx <= 23:  # Year 2
            return 1 + am_traffic_gr_y2
        elif month_idx <= 35:  # Year 3
            return 1 + am_traffic_gr_y3
        elif month_idx <= 47:  # Year 4
            return 1 + am_traffic_gr_y4
        else:  # Year 5
            return 1 + am_traffic_gr_y5

    def get_am_cr(month_idx):
        if month_idx <= 11:    # Year 1
            return am_cr_y1
        elif month_idx <= 23:  # Year 2
            return am_cr_y2
        elif month_idx <= 35:  # Year 3
            return am_cr_y3
        elif month_idx <= 47:  # Year 4
            return am_cr_y4
        else:                  # Year 5
            return am_cr_y5
            


    # Recurring revenue and financials dataframe
    months = [kick_off_date + relativedelta(months=i) for i in range(60)]
    # Create DataFrame
    df = pd.DataFrame({
        "Month": [kick_off_date + relativedelta(months=i) for i in range(60)],
        "Year": [month.year for month in months],  # Extract year from each date
        "Days Count": [calendar.monthrange(month.year, month.month)[1] for month in months],
    })
    df["Cross-Over Month Trial-To-Paid"] = free_trial_days / df["Days Count"]
    df["Trial-To-Paid Within Month"] = 1 - df["Cross-Over Month Trial-To-Paid"]
    
    df["SEM - Paid Traffic"] = 0.0
    df.at[0, "SEM - Paid Traffic"] = sem_traffic_m1  # Set first month value

    # Calculate subsequent months
    for i in range(1, 60):
        sem_growth_rate = get_sem_growth_rate(i)
        df.at[i, "SEM - Paid Traffic"] = df.at[i-1, "SEM - Paid Traffic"] * sem_growth_rate

    df["SEO - Organic Traffic"] = 0.0
    df.at[0, "SEO - Organic Traffic"] = seo_traffic_m1  # Set first month value

    # Calculate subsequent months
    for i in range(1, 60):
        seo_growth_rate = get_seo_growth_rate(i)
        df.at[i, "SEO - Organic Traffic"] = df.at[i-1, "SEO - Organic Traffic"] * seo_growth_rate

    df["AM - Paid Traffic"] = 0.0
    df.at[0, "AM - Paid Traffic"] = am_traffic_m1  # Set first month value

    # Calculate subsequent months
    for i in range(1, 60):
        am_growth_rate = get_am_growth_rate(i)
        df.at[i, "AM - Paid Traffic"] = df.at[i-1, "AM - Paid Traffic"] * am_growth_rate
        
    df["SEM Subscriptions"] = df["SEM - Paid Traffic"] * df.index.map(get_sem_cr)
    df["SEO Subscriptions"] = df["SEO - Organic Traffic"] * df.index.map(get_seo_cr)
    df["AM Subscriptions"] = df["AM - Paid Traffic"] * df.index.map(get_am_cr)
    df["Total Monthly Subscriptions"] = df["SEM Subscriptions"] + df["SEO Subscriptions"] + df["AM Subscriptions"]
    df["Website Views"]= (df["SEM - Paid Traffic"]+df["SEO - Organic Traffic"]+df["AM - Paid Traffic"])*views_per_visit

    # Initialize the new column
    df["Trial To Paid Transactions Count"] = 0.0

    # First row calculation
    df.at[0, "Trial To Paid Transactions Count"] = (
        df.at[0, "Total Monthly Subscriptions"] * 
        df.at[0, "Trial-To-Paid Within Month"] * 
        trial_to_paid
    )

    # Subsequent rows calculation
    for i in range(1, len(df)):
        df.at[i, "Trial To Paid Transactions Count"] = (
            (df.at[i, "Total Monthly Subscriptions"] * df.at[i, "Trial-To-Paid Within Month"] * trial_to_paid) +
            (df.at[i-1, "Total Monthly Subscriptions"] * df.at[i-1, "Cross-Over Month Trial-To-Paid"] * trial_to_paid)
        )

    df["Monthly Renewal Transactions Count"] = 0.0
    for i in range(1, len(df)):
        prev_ttp = df.loc[i - 1, "Trial To Paid Transactions Count"]
        renewal_prev = df.loc[i - 1, "Monthly Renewal Transactions Count"]
        df.loc[i, "Monthly Renewal Transactions Count"] = (prev_ttp + renewal_prev) * (1 - churn_rate)  

    df['New Monthly Recurring Revenue MRR'] = df["Trial To Paid Transactions Count"] * subscription_price
    df['Renewal Recurring Revenue MRR'] = df["Monthly Renewal Transactions Count"] * subscription_price
    df["Ad Network Revenue"]=(df["Website Views"]*(cpm/1000)) if views_per_visit > 0 else 0
    df['Ad Affiliate Revenue']=df["Website Views"]*am_ctr*am_ocr*am_cpa/views_per_visit
    df['Revenue'] = df['Renewal Recurring Revenue MRR'] + df['New Monthly Recurring Revenue MRR'] +df["Ad Network Revenue"]+df['Ad Affiliate Revenue']
    df['Chargebacks'] = df['Revenue'] * chb_rate
    df['Refunds'] = df['Revenue'] * refund_rate
    df['Income'] = df['Revenue'] - df['Refunds'] - df['Chargebacks']
    df['Credit Card Processing'] = df['Revenue'] * ccp_rate
    df['Web Hosting'] = monthly_web_hosting_cost
    df['Cost of Goods/Services Sold'] = df['Credit Card Processing'] + df['Web Hosting']
    df['Gross Income'] = df['Income'] - df['Cost of Goods/Services Sold']
    df['Labor Cost'] = monthly_labor_cost
    df['SEM Marketing'] = df["SEM Subscriptions"] * sem_cpa
    df['Affiliate Marketing'] = df["AM Subscriptions"] * affiliate_cpa
    df['Internet Marketing Cost'] = df['Affiliate Marketing'] + df['SEM Marketing']
    df['Technology & Software'] = monthly_techsoft_cost
    df['Earnings Before Taxes'] = df['Gross Income'] - df['Labor Cost'] - df['Internet Marketing Cost'] - df['Technology & Software']
    df['Cash Flow Accumulation'] = df['Earnings Before Taxes']  # Initialize with first month's value

    for i in range(1, len(df)):
        prev_cf = df.loc[i - 1, 'Cash Flow Accumulation']
        current_earnings = df.loc[i, 'Earnings Before Taxes']
        df.loc[i, 'Cash Flow Accumulation'] = prev_cf + current_earnings

    df["Internet Marketing CAC Weighted average"] = ((df["SEM Subscriptions"] * sem_cpa) + (df["AM Subscriptions"] * affiliate_cpa)) / (df["SEM Subscriptions"] + df["AM Subscriptions"])

    # dataframe for cac payback period
    first_value = subscription_price * trial_to_paid
    ltv_threshold = LTV * 0.999  # 99% of LTV

    # Initialize list with the first period value
    period_values = [first_value]

    # Generate values until the cumulative sum reaches 99% of LTV
    while sum(period_values) < ltv_threshold:
        next_value = period_values[-1] * renewal_rate
        period_values.append(next_value)

    cumulative_ltv = pd.DataFrame({"Period Value": period_values})
    cumulative_ltv["Accumulated Value"] = cumulative_ltv["Period Value"].cumsum()
    start_month = free_trial_days / 30
    months = [start_month + i for i in range(len(cumulative_ltv))]
    cumulative_ltv["Months"] = months
    
    if LTV < sem_cpa: 
        time_to_recover_sem_cac = 100000
    else: 
        match_row = cumulative_ltv[cumulative_ltv["Accumulated Value"] >= sem_cpa].head(1)
        if not match_row.empty:
            time_to_recover_sem_cac = match_row["Months"].values[0]
        else:
            time_to_recover_sem_cac = "No Pay Back"
        
    if LTV < affiliate_cpa:
        time_to_recover_affiliate_cac = 100000
    else:
        match_row = cumulative_ltv[cumulative_ltv["Accumulated Value"] >= affiliate_cpa].head(1)
        if not match_row.empty:
            time_to_recover_affiliate_cac = match_row["Months"].values[0]
        else:
            time_to_recover_affiliate_cac = "No Pay Back"
    
    def lookup_payback_period(cac_value):
        if LTV < cac_value:
            return "No Pay Back"
        match_row = cumulative_ltv[cumulative_ltv["Accumulated Value"] >= cac_value].head(1)
        if not match_row.empty:
            return match_row["Months"].values[0]
        else:
            return "No Pay Back"



    df["time_to_recover_Internet_marketing_cac"] = df["Internet Marketing CAC Weighted average"].apply(lookup_payback_period)

    # Financials dataframe consolidation
    df_financials = df[[
        'Month',
        'Year',
        'Revenue',
        'Chargebacks',
        'Refunds',
        'Income',
        'Credit Card Processing',
        'Web Hosting',
        'Cost of Goods/Services Sold',
        'Gross Income',
        'Labor Cost',
        'SEM Marketing',
        'Affiliate Marketing',
        'Internet Marketing Cost',
        'Technology & Software',
        'Earnings Before Taxes',
        'Cash Flow Accumulation'
    ]]
    df_financials_by_year = df_financials.groupby("Year", as_index=False).sum(numeric_only=True)

    # Show charts
    st.title("📈 Financial Projections Results")

    # Traffic Sources Chart
    st.subheader("Web/App Monthly Traffic")
    df_traffic = df[[
        'Month',
        'SEM - Paid Traffic',
        'SEO - Organic Traffic',
        'AM - Paid Traffic'
    ]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_traffic["Month"],
        y=df_traffic["SEM - Paid Traffic"],
        mode='lines',
        name='Paid(SEM)<br>Traffic',
        line=dict(color='#1f77b4', width=2),
        hovertemplate='SEM: %{y:,.0f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df_traffic["Month"],
        y=df_traffic["SEO - Organic Traffic"],
        mode='lines',
        name='Organic(SEO)<br>Traffic',
        line=dict(color='#ff7f0e', width=2),
        hovertemplate='SEO: %{y:,.0f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df_traffic["Month"],
        y=df_traffic["AM - Paid Traffic"],
        mode='lines',
        name='Affiliate<br>Marketing',
        line=dict(color='#2ca02c', width=2),
        hovertemplate='Affiliate: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Traffic Volume",
        xaxis=dict(
            type='date',
            tickformat='%b-%Y', 
            tickmode='auto',
            nticks=30,
            tickangle=-45  # Optional: rotates labels for better readability
        ),
        yaxis=dict(tickformat=","),
        hovermode="x unified",
        legend=dict(title="Traffic Source"),
        plot_bgcolor="white",
        yaxis_gridcolor="lightgray",
        margin=dict(t=25)
    )
    
    st.plotly_chart(fig, use_container_width=True)    

    # Monthly Subscriptions
    st.subheader("Monthly Subscriptions")
    df_subscriptions = df[[
        'Month',
        'Total Monthly Subscriptions',
        'Trial To Paid Transactions Count'
    ]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_subscriptions["Month"],
        y=df_subscriptions["Total Monthly Subscriptions"],
        mode='lines',
        name='New Monthly<br>Subscriptions',
        line=dict(color='#4E79A7', width=2),
        hovertemplate='Total Subs: %{y:,.0f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df_subscriptions["Month"],
        y=df_subscriptions["Trial To Paid Transactions Count"],
        mode='lines',
        name='Trial To Paid<br>New Users',
        line=dict(color='#F28E2B', width=2),
        hovertemplate='Trial To Paid: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Count",
        xaxis=dict(
            type='date',
            tickformat='%b-%Y',
            tickmode='auto',
            nticks=30,
            tickangle=-45
        ),
        yaxis=dict(tickformat=","),
        hovermode="x unified",
        legend=dict(title="Subscription Type"),
        plot_bgcolor="white",
        yaxis_gridcolor="lightgray",
        margin=dict(t=25)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Revenue split chart
    st.subheader("Monthly Recurring Revenue MRR Split")
    df_rev_split = df[[
        'Month',
        'New Monthly Recurring Revenue MRR',
        'Renewal Recurring Revenue MRR' ,
        'Ad Network Revenue',
        'Ad Affiliate Revenue'
    ]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_rev_split["Month"],
        y=df_rev_split["New Monthly Recurring Revenue MRR"],
        mode='lines',
        name='Trial To Paid<br>(New Users)',
        stackgroup='one',
        hovertemplate='Trial To Paid: $%{y:,.2f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df_rev_split["Month"],
        y=df_rev_split["Renewal Recurring Revenue MRR"],
        mode='lines',
        name='Recurring<br>Renewals',
        stackgroup='one',
        hovertemplate='Recurring Renewal: $%{y:,.2f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df_rev_split["Month"],
        y=df_rev_split["Ad Network Revenue"],
        mode='lines',
        name='Ad Network',
        stackgroup='one',
        hovertemplate='Ad Network: $%{y:,.2f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df_rev_split["Month"],
        y=df_rev_split["Ad Affiliate Revenue"],
        mode='lines',
        name='Ad Affiliate<br>Marketing',
        stackgroup='one',
        hovertemplate='Ad Affiliate: $%{y:,.2f}<extra></extra>'
    ))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="MRR",
        xaxis=dict(
            type='date',
            tickformat='%b-%Y',
            tickmode='auto',
            nticks=30,
            tickangle=-45,
            dtick='M2'# Optional: rotates labels for better readability
        ),
        yaxis=dict(tickformat="$,.2f"),
        margin=dict(t=25)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Financial performance by year chart
    st.subheader("Financial Performance by Year")
    
    fig = go.Figure()
    colors = ['#006400','#2E8B57','#3CB371','#90EE90']
    fig.add_trace(go.Scatter(x=df_financials_by_year["Year"], y=df_financials_by_year["Revenue"],
                             mode='lines+markers', name='Revenue',line=dict(color=colors[0], width=3),hovertemplate='$%{y:,.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=df_financials_by_year["Year"], y=df_financials_by_year["Income"],
                             mode='lines+markers', name='Income',line=dict(color=colors[1], width=3),hovertemplate='$%{y:,.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=df_financials_by_year["Year"], y=df_financials_by_year["Gross Income"],
                             mode='lines+markers', name='Gross<br>Income',line=dict(color=colors[2], width=3),hovertemplate='$%{y:,.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=df_financials_by_year["Year"], y=df_financials_by_year["Earnings Before Taxes"],
                             mode='lines+markers', name='Earnings<br>EBITDA',line=dict(color=colors[3], width=3),hovertemplate='$%{y:,.2f}<extra></extra>'))
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Amount ($)",
        plot_bgcolor="white",
        hovermode="x unified",
        legend=dict(title=""),
        yaxis=dict(gridcolor="lightgray"),
        margin=dict(t=25)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Cashflow accumulation chart
    st.subheader("Cash Flow Accumulation by Year")
    df_cashflow = df_financials.groupby("Year", as_index=False)["Earnings Before Taxes"].sum()
    df_cashflow["Cash Flow Accumulation"] = df_cashflow["Earnings Before Taxes"].cumsum()
    fig = px.bar(
        df_cashflow,
        x="Year",
        y="Cash Flow Accumulation",
        labels={"Cash Flow Accumulation": "Cash Flow Accumulation ($)"},
        text_auto='.2f',
        color_discrete_sequence=["skyblue"]
    )
    fig.update_traces(
        hovertemplate='$%{y:,.2f}<extra></extra>',
        texttemplate='$%{y:,.2f}',
        textposition='outside',
        textfont_color='darkgray'
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Cash Flow Accumulation",
        bargap=0.3,
        plot_bgcolor="white",
        yaxis_gridcolor="lightgray",
        margin=dict(t=30)
    )
    st.plotly_chart(fig, use_container_width=True)



    # Key Metrics Summary Table - ADDED AT THE END
    st.subheader("Key Metrics Summary")
    metrics_data = {
        "Metric": [
            "Average Monthly Renewal Rate (%)",
            "User Subscription Life Time Value - LTV ($)",
            "SEM Paid Customer Acquisition Cost Return of Investment - ROI ($)",
            "SEM Paid Customer Acquisition Cost Return of Investment - ROI (%)",
            "Affiliate Marketing Customer Acquisition Cost ROI ($)",
            "Affiliate Marketing Customer Acquisition Cost ROI (%)",
            "Time to Recover SEM Customer Acquisition Cost - CAC (months)",
            "Time to Recover Affiliate Marketing Cust Acq Cost - CAC (months)"
        ],
        "Value": [
            f"{renewal_rate:.1%}",
            f"${LTV:,.2f}",
            f"${sem_roi:,.2f}" if sem_roi_percent is not None else "N/A. You input SEM CAC = 0.00",
            f"{sem_roi_percent:.2%}" if sem_roi_percent is not None else "N/A. You input SEM CAC = 0.00",
            f"${affiliate_marketing_roi:,.2f}" if affiliate_marketing_roi_percent is not None else "N/A. You input Affiliate Marketing CAC = 0.00",
            f"{affiliate_marketing_roi_percent:.2%}" if affiliate_marketing_roi_percent is not None else "N/A. You input Affiliate Marketing CAC = 0.00",
            "N/A. You input SEM CAC = 0.00" if sem_roi_percent is None else "Immediately" if time_to_recover_sem_cac == 0.0 else "Not Profitable" if time_to_recover_sem_cac>1200 else f"{time_to_recover_sem_cac:,.2f}",
            "N/A. You input Affiliate Marketing CAC = 0.00" if affiliate_marketing_roi_percent is None else "Immediately" if time_to_recover_affiliate_cac == 0.0 else "Not Profitable" if time_to_recover_affiliate_cac>1200 else f"{time_to_recover_affiliate_cac:,.2f}"
        ]
    }
    metrics_df = pd.DataFrame(metrics_data)
    st.dataframe(
        metrics_df,
        column_config={
            "Metric": st.column_config.TextColumn("Metric", width="medium"),
            "Value": st.column_config.TextColumn("Value", width="small")
        },
        hide_index=True,
        use_container_width=True
    )

