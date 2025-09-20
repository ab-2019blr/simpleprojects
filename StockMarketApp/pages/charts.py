# Charting Page of StockMarketApp
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import read_bank_nifty_data
# Set page configuration
st.set_page_config(page_title="Charts", layout="centered", page_icon="📉")

st.subheader("Secondary Page: Charting Page")
st.write("This is the secondary page of the StockMarketApp app.")
st.divider()

@st.cache_data
def get_bank_nifty_data():
    return read_bank_nifty_data() 

df = get_bank_nifty_data()
# print(df.columns) # Debugging line to check column names
# print(df.head()) # Debugging line to check data
# Prepare the data for candlestick chart
df['Date'] = pd.to_datetime(df['trade_date']).dt.strftime('%Y-%m-%d')
df = df.sort_values(by='Date')  
df = df.rename(columns={'open_price': 'open', 'high_price': 'high', 'low_price': 'low', 'close_price': 'close', 'Date': 'date'})
# Prepare the candlestick chart using Plotly
fig = go.Figure(data=[go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
fig.update_layout(
    title='Bank Nifty Candlestick Chart', 
    xaxis_title='Date', 
    yaxis_title='Price'
)
# Add content specific to this page
# Display in Streamlit
st.plotly_chart(fig)
st.success("Chart displayed successfully!")

st.divider()
