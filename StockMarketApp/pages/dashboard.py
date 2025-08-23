# Main dashboard page for stock market analysis and monitoring

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import read_data  # Importing read_data function from data package

st.title("Stock Market Dashboard")
st.subheader("Monitor and Analyze Stock Market Data")

# Cache the data reading function to optimize performance
@st.cache_data
def get_data():
    return read_data()

# Add content specific to this page
if st.button("Read Data"):
    df = get_data()
    st.dataframe(df, hide_index=True)  # Display the data in a table format
    st.success("Data displayed successfully!")