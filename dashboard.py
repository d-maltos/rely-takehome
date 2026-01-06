"""
dashboard.py
Author: Dylan Maltos
Last Updated: 2026-01-05

Rely Health Takehome - Space Missions Interactive Dashboard
A Streamlit-based dashboard for visualizing and analyzing space mission data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from space_missions_functions import (
    getMissionCountByCompany,
    getSuccessRate,
    getMissionsByDateRange,
    getTopCompaniesByMissionCount,
    getMissionStatusCount,
    getMissionsByYear,
    getMostUsedRocket,
    getAverageMissionsPerYear
)

# Page configuration
st.set_page_config(
    page_title="Space Missions Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and preprocess space missions data."""
    df = pd.read_csv('space_missions.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    return df

def main():
    """Main dashboard function."""
    st.markdown('<h1 class="main-header">🚀 Space Missions Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Company filter
    companies = sorted(df['Company'].unique().tolist())
    selected_companies = st.sidebar.multiselect(
        "Companies",
        options=companies,
        default=companies
    )
    
    # Mission status filter
    statuses = sorted(df['MissionStatus'].dropna().unique().tolist())
    selected_statuses = st.sidebar.multiselect(
        "Mission Status",
        options=statuses,
        default=statuses
    )
    
    # Location filter
    locations = sorted(df['Location'].dropna().unique().tolist())
    selected_locations = st.sidebar.multiselect(
        "Launch Locations",
        options=locations,
        default=locations
    )
    
    # Apply filters
    filtered_df = df.copy()
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_date) &
            (filtered_df['Date'].dt.date <= end_date)
        ]
    
    if selected_companies:
        filtered_df = filtered_df[filtered_df['Company'].isin(selected_companies)]
    
    if selected_statuses:
        filtered_df = filtered_df[filtered_df['MissionStatus'].isin(selected_statuses)]
    
    if selected_locations:
        filtered_df = filtered_df[filtered_df['Location'].isin(selected_locations)]
    
    # Summary Statistics Section
    st.header("📊 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_missions = len(filtered_df)
    success_count = len(filtered_df[filtered_df['MissionStatus'] == 'Success'])
    success_rate = (success_count / total_missions * 100) if total_missions > 0 else 0
    unique_companies = filtered_df['Company'].nunique()
    unique_locations = filtered_df['Location'].nunique()
    
    with col1:
        st.metric("Total Missions", f"{total_missions:,}")
    
    with col2:
        st.metric("Success Rate", f"{success_rate:.2f}%")
    
    with col3:
        st.metric("Companies", unique_companies)
    
    with col4:
        st.metric("Launch Locations", unique_locations)
    
    st.markdown("---")
    
    # Visualizations Section
    st.header("📈 Visualizations")
    
    # Visualization 1: Success Rate Over Time
    st.subheader("1. Mission Success Rate Over Time")
    st.markdown("""
    **Why this visualization?** This line chart shows the evolution of mission success rates over time, 
    helping identify trends in space mission reliability. It's useful for understanding how technology 
    and experience have improved mission outcomes.
    
    **Visualization method:** Line chart with a rolling average to smooth out year-to-year variations 
    and highlight long-term trends.
    """)
    
    yearly_stats = filtered_df.groupby('Year').agg({
        'MissionStatus': lambda x: (x == 'Success').sum(),
        'Mission': 'count'
    }).reset_index()
    yearly_stats.columns = ['Year', 'Successes', 'Total']
    # Ensure numeric types to avoid dtype errors
    yearly_stats['Successes'] = pd.to_numeric(yearly_stats['Successes'], errors='coerce').fillna(0)
    yearly_stats['Total'] = pd.to_numeric(yearly_stats['Total'], errors='coerce').fillna(0)
    # Calculate success rate, ensuring it's between 0 and 100
    yearly_stats['SuccessRate'] = (yearly_stats['Successes'] / yearly_stats['Total'] * 100).round(2)
    yearly_stats['SuccessRate'] = yearly_stats['SuccessRate'].clip(0, 100)  # Cap at 100%
    # Filter out invalid rows
    yearly_stats = yearly_stats[(yearly_stats['Total'] > 0) & (yearly_stats['SuccessRate'].notna())]
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=yearly_stats['Year'],
        y=yearly_stats['SuccessRate'],
        mode='lines+markers',
        name='Success Rate',
        line=dict(color='#2ecc71', width=2),
        marker=dict(size=6)
    ))
    fig1.update_layout(
        title="Mission Success Rate by Year (%)",
        xaxis_title="Year",
        yaxis_title="Success Rate (%)",
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Visualization 2: Missions by Company (Top 10)
    st.subheader("2. Missions by Company (Top 10)")
    st.markdown("""
    **Why this visualization?** This horizontal bar chart displays the top 10 companies by mission count, 
    providing insight into which organizations have been most active in space exploration. It helps 
    identify industry leaders and their relative contributions.
    
    **Visualization method:** Horizontal bar chart sorted by mission count, making it easy to compare 
    companies and read their names clearly.
    """)
    
    company_counts = filtered_df['Company'].value_counts().head(10).reset_index()
    company_counts.columns = ['Company', 'MissionCount']
    company_counts = company_counts.sort_values('MissionCount', ascending=True)
    
    fig2 = px.bar(
        company_counts,
        x='MissionCount',
        y='Company',
        orientation='h',
        title="Top 10 Companies by Mission Count",
        labels={'MissionCount': 'Number of Missions', 'Company': 'Company'},
        color='MissionCount',
        color_continuous_scale='Blues'
    )
    fig2.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Visualization 3: Mission Status Distribution
    st.subheader("3. Mission Status Distribution")
    st.markdown("""
    **Why this visualization?** This pie chart shows the overall distribution of mission outcomes, 
    giving a quick overview of success vs. failure rates across all missions. It provides context 
    for understanding the overall reliability of space missions.
    
    **Visualization method:** Pie chart with percentage labels, allowing users to quickly see 
    the proportion of each outcome type.
    """)
    
    status_counts = filtered_df['MissionStatus'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    fig3 = px.pie(
        status_counts,
        values='Count',
        names='Status',
        title="Distribution of Mission Statuses",
        color_discrete_map={
            'Success': '#2ecc71',
            'Failure': '#e74c3c',
            'Partial Failure': '#f39c12',
            'Prelaunch Failure': '#95a5a6'
        }
    )
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Visualization 4: Missions by Year (Timeline)
    st.subheader("4. Mission Launch Timeline")
    st.markdown("""
    **Why this visualization?** This bar chart shows the number of missions launched each year, 
    revealing trends in space activity over time. It helps identify periods of high activity, 
    such as the space race era, and shows the growth of commercial spaceflight.
    
    **Visualization method:** Bar chart with year on x-axis, making it easy to see temporal 
    patterns and compare activity levels across different decades.
    """)
    
    yearly_missions = filtered_df.groupby('Year').size().reset_index()
    yearly_missions.columns = ['Year', 'MissionCount']
    
    fig4 = px.bar(
        yearly_missions,
        x='Year',
        y='MissionCount',
        title="Number of Missions Launched by Year",
        labels={'MissionCount': 'Number of Missions', 'Year': 'Year'},
        color='MissionCount',
        color_continuous_scale='Viridis'
    )
    fig4.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
    
    # Visualization 5: Top Launch Locations
    st.subheader("5. Top Launch Locations")
    st.markdown("""
    **Why this visualization?** This bar chart displays the most active launch sites, showing 
    where space missions are typically launched from. This helps understand geographic distribution 
    of space activity and identify key spaceports.
    
    **Visualization method:** Horizontal bar chart showing top 10 locations, sorted by mission count 
    for easy comparison.
    """)
    
    location_counts = filtered_df['Location'].value_counts().head(10).reset_index()
    location_counts.columns = ['Location', 'MissionCount']
    location_counts = location_counts.sort_values('MissionCount', ascending=True)
    
    fig5 = px.bar(
        location_counts,
        x='MissionCount',
        y='Location',
        orientation='h',
        title="Top 10 Launch Locations by Mission Count",
        labels={'MissionCount': 'Number of Missions', 'Location': 'Location'},
        color='MissionCount',
        color_continuous_scale='Reds'
    )
    fig5.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("---")
    
    # Data Table Section
    st.header("📋 Mission Data Table")
    st.markdown("Interactive table with sorting and filtering capabilities")
    
    # Display options
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search missions, companies, or rockets", "")
    with col2:
        rows_per_page = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
    
    # Apply search filter
    display_df = filtered_df.copy()
    if search_term:
        mask = (
            display_df['Mission'].str.contains(search_term, case=False, na=False) |
            display_df['Company'].str.contains(search_term, case=False, na=False) |
            display_df['Rocket'].str.contains(search_term, case=False, na=False)
        )
        display_df = display_df[mask]
    
    # Select columns to display
    columns_to_show = ['Date', 'Company', 'Mission', 'Rocket', 'Location', 'MissionStatus', 'RocketStatus']
    display_df = display_df[columns_to_show].copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    
    # Display table
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    st.markdown(f"**Showing {len(display_df)} of {len(filtered_df)} missions**")
    
    # Function Testing Section (for development/debugging)
    with st.expander("🧪 Function Testing (Development)"):
        st.markdown("Test the required functions programmatically:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Function 1: getMissionCountByCompany")
            test_company = st.text_input("Company name", "NASA")
            if st.button("Test Function 1"):
                result = getMissionCountByCompany(test_company)
                st.write(f"Result: {result}")
        
        with col2:
            st.subheader("Function 2: getSuccessRate")
            test_company2 = st.text_input("Company name", "NASA", key="company2")
            if st.button("Test Function 2"):
                result = getSuccessRate(test_company2)
                st.write(f"Result: {result}%")
        
        with col1:
            st.subheader("Function 3: getMissionsByDateRange")
            start_date = st.text_input("Start date (YYYY-MM-DD)", "1957-10-01")
            end_date = st.text_input("End date (YYYY-MM-DD)", "1957-12-31")
            if st.button("Test Function 3"):
                result = getMissionsByDateRange(start_date, end_date)
                st.write(f"Result: {result[:10]}..." if len(result) > 10 else f"Result: {result}")
        
        with col2:
            st.subheader("Function 4: getTopCompaniesByMissionCount")
            n_companies = st.number_input("Number of companies", min_value=1, max_value=20, value=5)
            if st.button("Test Function 4"):
                result = getTopCompaniesByMissionCount(n_companies)
                st.write(f"Result: {result}")
        
        with col1:
            st.subheader("Function 5: getMissionStatusCount")
            if st.button("Test Function 5"):
                result = getMissionStatusCount()
                st.write(f"Result: {result}")
        
        with col2:
            st.subheader("Function 6: getMissionsByYear")
            test_year = st.number_input("Year", min_value=1950, max_value=2030, value=2020)
            if st.button("Test Function 6"):
                result = getMissionsByYear(int(test_year))
                st.write(f"Result: {result}")
        
        with col1:
            st.subheader("Function 7: getMostUsedRocket")
            if st.button("Test Function 7"):
                result = getMostUsedRocket()
                st.write(f"Result: {result}")
        
        with col2:
            st.subheader("Function 8: getAverageMissionsPerYear")
            start_year = st.number_input("Start year", min_value=1950, max_value=2030, value=2010)
            end_year = st.number_input("End year", min_value=1950, max_value=2030, value=2020)
            if st.button("Test Function 8"):
                result = getAverageMissionsPerYear(int(start_year), int(end_year))
                st.write(f"Result: {result}")

if __name__ == "__main__":
    main()

