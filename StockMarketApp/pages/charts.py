# Charting Page of StockMarketApp
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import read_bank_nifty_data, read_bank_nifty_index_data # Importing read_data function from data package

# Set page configuration
# st.set_page_config(page_title="Charts", layout="centered", page_icon="📉")

# st.subheader("Secondary Page: Charting Page")
# st.write("This is the secondary page of the StockMarketApp app.")
# st.divider()

@st.cache_data
def get_bank_nifty_data():
    return read_bank_nifty_data() 

@st.cache_data
def get_bank_nifty_index_data():
    return read_bank_nifty_index_data()

# df = get_bank_nifty_data()
df = get_bank_nifty_index_data() 
# print(df.columns) # Debugging line to check column names
# print(df.head()) # Debugging line to check data
# Prepare the data for candlestick chart
# df['Date'] = pd.to_datetime(df['trade_date']).dt.strftime('%Y-%m-%d')
df['Date'] = pd.to_datetime(df['historical_date']).dt.strftime('%Y-%m-%d')
df = df.sort_values(by='Date')  
# df = df.rename(columns={'open_price': 'open', 'high_price': 'high', 'low_price': 'low', 'close_price': 'close', 'Date': 'date'})
df = df.rename(columns={'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close', 'Date': 'date'}) 
df = df[['date', 'open', 'high', 'low', 'close']]
# Prepare the candlestick chart using Plotly
fig = go.Figure(data=[go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
fig.update_layout(
    title='Bank Nifty Index Candlestick Chart', 
    xaxis_type='category', # 'xaxis_type' can be 'category' to skip weekend gaps
    xaxis_tickmode='auto', # 'xaxis_tickmode' can be 'auto' or 'linear' to avoid label cluttering
    # xaxis_nticks=5, # Number of ticks on x-axis to show about 5 ticks, adjust as needed
    xaxis_title='Date', 
    yaxis_title='Price',
    xaxis_rangeslider_visible=False
)
# Add content specific to this page
# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
st.success("Chart displayed successfully!")

st.divider()
