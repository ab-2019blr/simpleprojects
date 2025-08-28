# File contains External API client for the StockMarketApp project
# This file is responsible for interacting with external APIs to fetch stock market data 
# and other relevant information needed for the application. 

# Documentation: For NIFTY top gainers and losers, we are using the API from NSETOOLS : https://vsjha18.github.io/nsetools/index.html
# Alternatively, similar functionality can be achieved using Alpha Vantage API: https://www.alphavantage.co/documentation/
# For more information on the APIs, refer to the documentation provided in the project.

import requests
import sys 
import os
import json
# import pandas as pd
# from nsetools import Nse
# nse = Nse() 

# Looking for specific symbols or tickers from Alpha Vantage API
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.api_config import alpha_vantage_api_key, finnhub_api_key, marketaux_api_key
def fetch_stock_ticker(keyword: str) -> dict:
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={alpha_vantage_api_key}"
    response = requests.get(url)
    data = response.json()
    # Retrieves the value for the 'bestMatches' key from dictionary 'data'
    matches = data.get('bestMatches', []) 
    # Filter results to include only those from India/Bombay region
    filtered = [match for match in matches if match.get('4. region') == 'India/Bombay']
    return (filtered) 

def fetch_stock_ticker_finnhub(symbol: str) -> dict:
    url = f"https://finnhub.io/api/v1/search?q={symbol}&exchange=NS&token={finnhub_api_key}"
    response = requests.get(url)
    data = response.json()
    if isinstance(data, list) and len(data) > 0:
        result_data = data[0].get('result', [])
    elif isinstance(data, dict):
        result_data = data.get('result', [])
    else:
        result_data = []

    return (result_data)
# Example usage: with Alpha Vantage API 
# result = fetch_stock_ticker("Infosys")
# print(json.dumps(result, indent=2))

# Example usage: with Finnhub API
# result = fetch_stock_ticker_finnhub("tcs")
# print(json.dumps(result, indent=2)) # print the json response (result) 

# Fetching NIFTY top gainers and losers using NSETOOLS API

# Market news from MarketAux API
def fetch_market_news(number: int) -> dict:
    url = f"https://api.marketaux.com/v1/news/all?countries=in&filter_entities=true&limit={number}&published_after=2025-08-27T11:06&api_token={marketaux_api_key}"
    response = requests.get(url)
    data = response.json()
    if isinstance(data, list) and len(data) > 0:
        result_data = data[0].get('data', [])
    elif isinstance(data, dict):
        result_data = data.get('data', [])
    else:
        result_data = []

    return (result_data)

news_feed = fetch_market_news(3)# Fetch 3 latest market news articles
print(json.dumps(news_feed, indent=2))# Example usage: Fetching market news
