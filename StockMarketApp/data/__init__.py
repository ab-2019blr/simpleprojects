# Package for StockMarketApp data handling
# This package contains modules for data collection, processing, and storage
# for the StockMarketApp project.

from .database import read_data, read_specific_data, read_bank_nifty_data, read_bank_nifty_index_data, read_nifty50_stock_quotes_data, read_nifty_indexes_data, read_nifty_stocks_quotes # Import read_data function from database module

from .api_client import fetch_stock_ticker, fetch_stock_ticker_finnhub, fetch_market_news, fetch_global_market_news # Import API client functions from api_client module

from .data_processor import compute_rsi, compute_dma # Import data processing function from data_processor module

from .file_data_processor import read_csv_to_dataframe, read_top_gainers_csv_to_dataframe, read_top_losers_csv_to_dataframe, read_index_valuation_csv_to_dataframe # Import file data processing functions from file_data_processor module

from .portfolio_data_processor import add_transaction, get_all_transactions, get_portfolio_summary, delete_transaction, TransactionType, Transaction, CurrentPrice, initialize_default_prices, update_current_prices, get_last_price_update, test_connection, get_database_stats # Import portfolio data processing functions from portfolio_data_processor module

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
    'compute_dma',
    'read_nifty50_stock_quotes_data',
    'read_nifty_indexes_data',
    'read_csv_to_dataframe',
    'read_nifty_stocks_quotes',
    'read_top_gainers_csv_to_dataframe',
    'read_top_losers_csv_to_dataframe',
    'read_index_valuation_csv_to_dataframe',
    'add_transaction', 
    'get_all_transactions',
    'get_portfolio_summary',
    'delete_transaction',
    'TransactionType',
    'Transaction',
    'CurrentPrice',
    'initialize_default_prices',
    'update_current_prices',
    'get_last_price_update',
    'test_connection',
    'get_database_stats'
]  # Define the public interface of the package

# __all__ = ['etch_stock_ticker_finnhub', 'fetch_market_news', 'fetch_global_market_news', 'read_bank_nifty_data']  # Define the public interface of the package