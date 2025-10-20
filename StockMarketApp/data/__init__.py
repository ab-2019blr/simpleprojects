# Package for StockMarketApp data handling
# This package contains modules for data collection, processing, and storage
# for the StockMarketApp project.

from .database import read_data, read_specific_data, read_bank_nifty_data, read_bank_nifty_index_data # Import read_data function from database module

from .api_client import fetch_stock_ticker, fetch_stock_ticker_finnhub, fetch_market_news, fetch_global_market_news # Import API client functions from api_client module

from .data_processor import compute_rsi, compute_dma # Import data processing function from data_processor module
__all__ = [
    'read_data', 
    'read_specific_data', 
    'fetch_stock_ticker', 
    'fetch_stock_ticker_finnhub',
    'fetch_market_news',
    'fetch_global_market_news',
    'read_bank_nifty_data',
    'read_bank_nifty_index_data',
    'compute_rsi',
    'compute_dma'
]  # Define the public interface of the package

# __all__ = ['etch_stock_ticker_finnhub', 'fetch_market_news', 'fetch_global_market_news', 'read_bank_nifty_data']  # Define the public interface of the package