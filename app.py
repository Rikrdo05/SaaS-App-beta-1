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
if getattr(st.session_state, 'calculate', False):
    # Assign all variables from form data
    for key, value in st.session_state.form_data.items():
        globals()[key] = value
    
    # Calculate derived variables
    renewal_rate = 1 - churn_rate
    LTV = (subscription_price * trial_to_paid) / (1 - renewal_rate)
    
    # Define growth rate functions
    def get_sem_growth_rate(month_idx):
        if month_idx <= 12: return 1 + sem_gr_y1
        elif month_idx <= 24: return 1 + sem_gr_y2
        elif month_idx <= 36: return 1 + sem_gr_y3
        elif month_idx <= 48: return 1 + sem_gr_y4
        else: return 1 + sem_gr_y5

    def get_sem_cr(month_idx):
        if month_idx <= 12: return sem_cr_y1
        elif month_idx <= 24: return sem_cr_y2
        elif month_idx <= 36: return sem_cr_y3
        elif month_idx <= 48: return sem_cr_y4
        else: return sem_cr_y5  

    def get_seo_growth_rate(month_idx):
        if month_idx <= 12: return 1 + seo_gr_y1
        elif month_idx <= 24: return 1 + seo_gr_y2
        elif month_idx <= 36: return 1 + seo_gr_y3
        elif month_idx <= 48: return 1 + seo_gr_y4
        else: return 1 + seo_gr_y5

    def get_seo_cr(month_idx):
        if month_idx <= 12: return seo_cr_y1
        elif month_idx <= 24: return seo_cr_y2
        elif month_idx <= 36: return seo_cr_y3
        elif month_idx <= 48: return seo_cr_y4
        else: return seo_cr_y5      
    
    def get_afmar_growth_rate(month_idx):
        if month_idx <= 12: return 1 + aff_gr_y1
        elif month_idx <= 24: return 1 + aff_gr_y2
        elif month_idx <= 36: return 1 + aff_gr_y3
        elif month_idx <= 48: return 1 + aff_gr_y4
        else: return 1 + aff_gr_y5
            
# Create DataFrame with calculations
months = [kick_off_date + relativedelta(months=i) for i in range(60)]
df = pd.DataFrame({
    "Month": months,
    "Year": [month.year for month in months],
    "Days Count": [calendar.monthrange(month.year, month.month)[1] for month in months]
})

# Calculate trial days allocation (fixed version)
df["Cross-Over Month Trial-To-Paid"] = df["Days Count"].apply(
    lambda days: min(free_trial_days / days, 1.0)  # Ensure never > 100%
)
df["Trial-To-Paid Within Month"] = 1 - df["Cross-Over Month Trial-To-Paid"]

# Traffic calculations
df["SEM - Paid Traffic"] = 0.0
df.at[0, "SEM - Paid Traffic"] = sem_traffic_m1
for i in range(1, 60):
    df.at[i, "SEM - Paid Traffic"] = df.at[i-1, "SEM - Paid Traffic"] * get_sem_growth_rate(i)

df["SEO - Organic Traffic"] = 0.0
df.at[0, "SEO - Organic Traffic"] = seo_traffic_m1
for i in range(1, 60):
    df.at[i, "SEO - Organic Traffic"] = df.at[i-1, "SEO - Organic Traffic"] * get_seo_growth_rate(i)

df["Affiliate Marketing Subscriptions"] = 0.0
df.at[0, "Affiliate Marketing Subscriptions"] = subs_affiliate_m1
for i in range(1, 60):
    df.at[i, "Affiliate Marketing Subscriptions"] = df.at[i-1, "Affiliate Marketing Subscriptions"] * get_afmar_growth_rate(i)
    
    # Subscription calculations
    df["SEM Subscriptions"] = df["SEM - Paid Traffic"] * df.index.map(get_sem_cr)
    df["SEO Subscriptions"] = df["SEO - Organic Traffic"] * df.index.map(get_seo_cr)
    df["Total Monthly Subscriptions"] = df["SEM Subscriptions"] + df["SEO Subscriptions"] + df["Affiliate Marketing Subscriptions"]

    # Trial to paid calculations
    df["Trial To Paid Transactions Count"] = 0.0
    df.at[0, "Trial To Paid Transactions Count"] = (
        df.at[0, "Total Monthly Subscriptions"] * 
        df.at[0, "Trial-To-Paid Within Month"] * 
        trial_to_paid
    )
    for i in range(1, len(df)):
        df.at[i, "Trial To Paid Transactions Count"] = (
            (df.at[i, "Total Monthly Subscriptions"] * df.at[i, "Trial-To-Paid Within Month"] * trial_to_paid) +
            (df.at[i-1, "Total Monthly Subscriptions"] * df.at[i-1, "Cross-Over Month Trial-To-Paid"] * trial_to_paid)
        )

    # Renewal calculations
    df["Monthly Renewal Transactions Count"] = 0.0
    for i in range(1, len(df)):
        prev_ttp = df.loc[i - 1, "Trial To Paid Transactions Count"]
        renewal_prev = df.loc[i - 1, "Monthly Renewal Transactions Count"]
        df.loc[i, "Monthly Renewal Transactions Count"] = (prev_ttp + renewal_prev) * (1 - churn_rate)  

    # Financial calculations
    df['New Monthly Recurring Revenue MRR'] = df["Trial To Paid Transactions Count"] * subscription_price
    df['Renewal Recurring Revenue MRR'] = df["Monthly Renewal Transactions Count"] * subscription_price
    df['Total Monthly Recurring Revenue MRR'] = df['Renewal Recurring Revenue MRR'] + df['New Monthly Recurring Revenue MRR']
    df['Chargebacks'] = df['Total Monthly Recurring Revenue MRR'] * chb_rate
    df['Refunds'] = df['Total Monthly Recurring Revenue MRR'] * refund_rate
    df['Income'] = df['Total Monthly Recurring Revenue MRR'] - df['Refunds'] - df['Chargebacks']
    df['Credit Card Processing'] = df['Total Monthly Recurring Revenue MRR'] * ccp_rate
    df['Web Hosting'] = monthly_web_hosting_cost
    df['Cost of Goods/Services Sold'] = df['Credit Card Processing'] + df['Web Hosting']
    df['Gross Income'] = df['Income'] - df['Cost of Goods/Services Sold']
    df['Labor Cost'] = monthly_labor_cost
    df['SEM Marketing'] = df["SEM Subscriptions"] * sem_cpa
    df['Affiliate Marketing'] = df["Affiliate Marketing Subscriptions"] * affiliate_cpa
    df['Internet Marketing Cost'] = df['Affiliate Marketing'] + df['SEM Marketing']
    df['Technology & Software'] = monthly_techsoft_cost
    df['Earnings Before Taxes'] = df['Gross Income'] - df['Labor Cost'] - df['Internet Marketing Cost'] - df['Technology & Software']
    
    # Cash flow calculations
    df['Cash Flow Accumulation'] = df['Earnings Before Taxes']
    for i in range(1, len(df)):
        prev_cf = df.loc[i - 1, 'Cash Flow Accumulation']
        current_earnings = df.loc[i, 'Earnings Before Taxes']
        df.loc[i, 'Cash Flow Accumulation'] = prev_cf + current_earnings

    # LTV and CAC calculations
    df["Internet Marketing CAC Weighted average"] = ((df["SEM Subscriptions"] * sem_cpa) + 
                                                   (df["Affiliate Marketing Subscriptions"] * affiliate_cpa)) / \
                                                  (df["SEM Subscriptions"] + df["Affiliate Marketing Subscriptions"])
    
    # Prepare financial data for visualization
    df_financials = df[[
        'Month', 'Year', 'Total Monthly Recurring Revenue MRR', 'Chargebacks', 
        'Refunds', 'Income', 'Credit Card Processing', 'Web Hosting',
        'Cost of Goods/Services Sold', 'Gross Income', 'Labor Cost',
        'SEM Marketing', 'Affiliate Marketing', 'Internet Marketing Cost',
        'Technology & Software', 'Earnings Before Taxes', 'Cash Flow Accumulation'
    ]].rename(columns={'Total Monthly Recurring Revenue MRR': 'Revenue'})
    
    df_financials_by_year = df_financials.groupby("Year", as_index=False).sum(numeric_only=True)
    
    # Create and display charts
    st.title("📈 Financial Projections")
    
    # Chart 1: Financial Performance by Year
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_financials_by_year["Year"], y=df_financials_by_year["Revenue"],
                             mode='lines+markers', name='Revenue'))
    fig1.add_trace(go.Scatter(x=df_financials_by_year["Year"], y=df_financials_by_year["Income"],
                             mode='lines+markers', name='Income'))
    fig1.add_trace(go.Scatter(x=df_financials_by_year["Year"], y=df_financials_by_year["Gross Income"],
                             mode='lines+markers', name='Gross Income'))
    fig1.add_trace(go.Scatter(x=df_financials_by_year["Year"], y=df_financials_by_year["Earnings Before Taxes"],
                             mode='lines+markers', name='Earnings Before Taxes'))
    fig1.update_layout(
        title="Financial Performance by Year",
        xaxis_title="Year",
        yaxis_title="Amount ($)",
        plot_bgcolor="white",
        hovermode="x unified",
        legend=dict(title=""),
        yaxis=dict(gridcolor="lightgray")
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Chart 2: Cash Flow Accumulation by Year
    fig2 = px.bar(
        df_financials_by_year,
        x="Year",
        y="Cash Flow Accumulation",
        title="Cash Flow Accumulation by Year",
        labels={"Cash Flow Accumulation": "Cash Flow Accumulation"},
        text_auto=True,
        color_discrete_sequence=["skyblue"]
    )
    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="Cash Flow Accumulation",
        bargap=0.3,
        plot_bgcolor="white",
        yaxis_gridcolor="lightgray"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Chart 3: New vs Renewal MRR
    df_rev_split = df[['Month', 'New Monthly Recurring Revenue MRR', 'Renewal Recurring Revenue MRR']]
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_rev_split["Month"],
        y=df_rev_split["New Monthly Recurring Revenue MRR"],
        mode='lines',
        name='New MRR',
        stackgroup='one'
    ))
    fig3.add_trace(go.Scatter(
        x=df_rev_split["Month"],
        y=df_rev_split["Renewal Recurring Revenue MRR"],
        mode='lines',
        name='Renewal MRR',
        stackgroup='one'
    ))
    fig3.update_layout(
        title="Stacked Line Chart of New vs Renewal MRR",
        xaxis_title="Month",
        yaxis_title="MRR",
        xaxis=dict(type='category')
    )
    st.plotly_chart(fig3, use_container_width=True)
