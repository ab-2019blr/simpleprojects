# Charting Page of StockMarketApp
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import read_bank_nifty_data, read_bank_nifty_index_data # Importing read_data function from data package
from data.data_processor import compute_rsi, compute_dma  # Importing compute_rsi function from data package

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

# Display RSI below the candlestick chart
st.subheader("Relative Strength Index (RSI)")
@st.cache_data
def get_rsi_data():
    return compute_rsi(df['close'], period=14)
df['date'], df['RSI'] = get_rsi_data()
# Prepare RSI Plotly chart
rsi_fig = go.Figure()
rsi_fig.add_trace(go.Scatter(
    x=df['date'], y=df['RSI'], mode='lines', name='RSI'
))
rsi_fig.update_layout(
    title='Bank Nifty RSI (14-day)',
    xaxis_title='Date',
    yaxis_title='RSI',
    yaxis=dict(range=[0, 100]),  # RSI is always between 0-100
    shapes=[
        # Overbought line at 70
        dict(type='line', yref='y', y0=70, y1=70, xref='paper', x0=0, x1=1,
             line=dict(color='red', dash='dash')),
        # Oversold line at 30
        dict(type='line', yref='y', y0=30, y1=30, xref='paper', x0=0, x1=1,
             line=dict(color='green', dash='dash'))
    ]
)
st.plotly_chart(rsi_fig, use_container_width=True)
st.success("RSI chart displayed successfully!")

st.divider()

# Display DMA below the candlestick chart
st.subheader("Daily Moving Average (DMA)")
@st.cache_data
def get_dma_data():
    return compute_dma(df['close'], short_period=20, long_period=50)
df['date'], df['close'], df['20DMA'], df['50DMA'] = get_dma_data()
# Reformat the date column for better readability 
df['date'] = pd.to_datetime(df['date']).dt.strftime('%d-%b-%Y')
# Just prepare DMA Plotly chart
dma_fig = go.Figure()
dma_fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines', name='Close'))
dma_fig.add_trace(go.Scatter(x=df['date'], y=df['20DMA'], mode='lines', name='20DMA'))
dma_fig.add_trace(go.Scatter(x=df['date'], y=df['50DMA'], mode='lines', name='50DMA'))
dma_fig.update_layout(
    xaxis=dict(autorange='reversed'), # Reverse x-axis to show latest date on right
    title='Bank Nifty: Close, 20DMA, 50DMA',
    xaxis_title='Date',
    yaxis_title='Price')
# Rename the columns for clarity
df = df.rename(columns={'date': 'Date', 'close': 'Closing Price', '20DMA': '20-Day Moving Average', '50DMA': '50-Day Moving Average'})
# Display DMA in Streamlit table format
st.dataframe(df[['Date', 'Closing Price', '20-Day Moving Average', '50-Day Moving Average']].tail(10), hide_index=True)  # Show last 10 rows
# Now render the DMA chart
st.plotly_chart(dma_fig, use_container_width=True)

st.success("DMA data displayed successfully!")
st.divider()
