# Package for StockMarketApp data handling
# This package contains modules for data collection, processing, and storage
# for the StockMarketApp project.

from .database import read_data, read_specific_data # Import read_data function from database module

from .api_client import fetch_stock_ticker, fetch_stock_ticker_finnhub, fetch_market_news # Import API client functions from api_client module

__all__ = ['read_data', 'read_specific_data', 'fetch_stock_ticker', 'fetch_stock_ticker_finnhub', 'fetch_market_news']  # Define the public interface of the package