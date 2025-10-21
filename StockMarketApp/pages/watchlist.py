# Watchlist management page implementation goes here
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import read_nifty50_stock_quotes_data # Importing read_data function from data package

# Set page configuration
st.set_page_config(page_title="Watchlist", layout="centered", page_icon="👀")

st.subheader("Watchlist Management Page")

# Dropdown for stock selection
stock_list = [
    "RELIANCE", 
    "BHARTIARTL", 
    "TCS", 
    "TITAN", 
    "INFY", 
    "BEL", 
    "TATAMOTORS", 
    "ONGC", 
    "NTPC", 
    "WIPRO", 
    "ITC", 
    "HDFCBANK", 
    "MARUTI", 
    "HINDUNILVR", 
    "ICICIBANK"
    # Add more stocks as needed
] 
selected_stock = st.selectbox("Select a stock to add to your watchlist:", stock_list)
columns = ["Symbol", "Last Price", "Previous Close", "Change", "Total Traded Volume", "Total Traded Value", "Year High", "Year Low"]
# columns = ["symbol", "last_price", "previous_close", "change", "p_change", "total_traded_volume", "total_traded_value", "year_high", "year_low"] 
# Mapping dictionary to rename columns from database to user-friendly names in DataFrame
column_mapping = {
    "symbol": "Symbol",
    "last_price": "Last Price",
    "previous_close": "Previous Close",
    "change": "Change",
    "p_change": "Percentage Change",
    "total_traded_volume": "Total Traded Volume",
    "total_traded_value": "Total Traded Value",
    "year_high": "Year High",
    "year_low": "Year Low"
}

# Initialize session state for watchlist
if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = pd.DataFrame(columns=columns)
@st.cache_data
def get_watchlist_data(selected_stock):
    raw_data = read_nifty50_stock_quotes_data(selected_stock)
    # Convert to DataFrame (if dict, wrap in list)
    df = pd.DataFrame([raw_data]) if isinstance(raw_data, dict) else pd.DataFrame(raw_data)
    # Rename columns using mapping dictionary
    df = df.rename(columns=column_mapping)
    # Ensure consistent DataFrame column order
    expected_columns = [
        "Symbol",
        "Last Price",
        "Previous Close",
        "Change",
        "Total Traded Volume",
        "Total Traded Value",
        "Year High",
        "Year Low"
    ]
    df = df[[col for col in expected_columns if col in df.columns]]
    return df.to_dict(orient='records')[0]  # Return as dictionary

# Add stock button
if st.button("Add"):
    # Check for duplicates
    if selected_stock in st.session_state['watchlist']['Symbol'].values:
        st.error(f"The stock symbol '{selected_stock}' is already in the watchlist.")
    else:
        data = get_watchlist_data(selected_stock)
        st.session_state['watchlist'] = pd.concat([st.session_state['watchlist'], pd.DataFrame([data])], ignore_index=True)

# Editable and Deletable Table
edited_watchlist = st.data_editor(
    st.session_state['watchlist'],
    num_rows="dynamic",  # allows adding/deleting rows interactively
    use_container_width=True, 
    hide_index=True
)

# Update session state if rows are deleted
st.session_state['watchlist'] = edited_watchlist

st.success("Watchlist updated successfully!")
st.divider()
