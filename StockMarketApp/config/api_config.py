# File to configure the API settings for the StockMarketApp project
from dotenv import load_dotenv
import os   
load_dotenv()  # Loads .env file in project root

finnhub_api_key = os.getenv('API_KEY_FINNHUB')
alpha_vantage_api_key = os.getenv('API_KEY_ALPHAVANTAGE')
india_api_key = os.getenv('API_KEY_INDIAPI')
news_api_key = os.getenv('API_KEY_NEWSAPI')
marketaux_api_key = os.getenv('API_KEY_MARKETAUX')