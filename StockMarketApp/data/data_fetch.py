# File contains all data fetching functions for the StockMarketApp project
# This file is responsible for fetching stock market data from various sources,
# including APIs, databases, and external files. It handles data retrieval,
# ensuring that the data is up-to-date and formatted correctly for further processing.
# It also includes functions for handling errors during data fetching and logging the results.


# Documentation: of niftystocks can be found at https://pypi.org/project/niftystocks/ 
# Documentation: of nsetools can be found at https://pypi.org/project/nsetools/
# Documentation: of nsepython can be found at https://pypi.org/project/nsepython/
# Documentation: of nselib can be found at https://pypi.org/project/nselib/ 
from niftystocks import ns 
from nsetools import Nse 
nse = Nse() 
from nsepython import * 
from nselib import capital_market
import pandas as pd

# Fist section of this file is for fetching NSE 50 or NSE 500 stock symbols using niftystocks library
# try: 
#     # Get a list of NSE 50 or NSE 500 stock symbols
#     symbols = ns.get_nifty50() #  or ns.get_nifty500() for NSE 500
#     # Convert the list of symbols to a pandas Series and save it to a CSV file
#     # The 'Symbol' column will be created in the CSV file 
#     print(symbols)
#     pd.Series(symbols, name='Symbol').to_csv('nse50_symbols.csv', index=False)
#     print("Successfully fetched NSE 50 symbols.")  # Log success message
# except FileNotFoundError as e:
#     print(f"File not found error: {e}")
# except pd.errors.EmptyDataError as e:
#     print(f"Empty data error: {e}")
# except pd.errors.ParserError as e:
#     print(f"Parser error: {e}")
# except ConnectionError as e:
#     print(f"Connection error: {e}")
# except TimeoutError as e:
#     print(f"Timeout error: {e}")
# except Exception as e:
#     print(f"Error fetching NSE 50 symbols: {e}")  # Log the error message
#     symbols = []  # Set symbols to an empty list in case of an error to avoid further errors

# Fetch NIFTY BANK index data as a sample
# try: 
#     # Get a list of NIFTY BANK stock symbols
#     bank_nifty_symbols = nse.get_stocks_in_index(index="NIFTY BANK")
#     print(bank_nifty_symbols)
#     # Convert the list of symbols to a pandas Series and save it to a CSV file
#     # The 'Symbol' column will be created in the CSV file 
#     pd.Series(bank_nifty_symbols, name='Symbol').to_csv('nifty_bank_symbols.csv', index=False)
#     print("Successfully fetched NIFTY BANK symbols.")  # Log success message
# except FileNotFoundError as e:
#     print(f"File not found error: {e}")
# except pd.errors.EmptyDataError as e:
#     print(f"Empty data error: {e}")
# except pd.errors.ParserError as e:
#     print(f"Parser error: {e}")
# except ConnectionError as e:
#     print(f"Connection error: {e}")
# except TimeoutError as e:
#     print(f"Timeout error: {e}")
# except Exception as e:
#     print(f"Error fetching NIFTY BANK symbols: {e}")  # Log the error message
#     bank_nifty_symbols = []  # Set symbols to an empty list in case of an error to avoid further errors

# Fetch NIFTY index data with chart url as a sample
index_ticker = "NIFTY BANK"
start_date = "01-Sep-2025"
end_date = "19-Sep-2025"
try:
    # print(nse_get_index_quote("NIFTY 50"))  # Uses nsepython to fetch and print NIFTY index quote
    # print(nse.get_index_quote("NIFTY 50"))  # Uses nsetools to fetch NIFTY index quote with chart url 
    bank_nifty_df = index_history(index_ticker, start_date, end_date)
    bank_nifty_df.to_csv('nifty_bank_index_data.csv', index=False)
    print("Successfully fetched NIFTY BANK data.")  # Log success message
    #  # Uses nsepython to fetch and print NIFTY index historical data 
except Exception as e:
    print(f"Error fetching NIFTY index data: {e}")  # Log the error message 

# This section of the file is for fetching bulk data for NSE 50, NIFTY BANK or NSE 500 stocks using nselib library
# Loads the list of NSE 50, NIFTY BANK or NSE 500 symbols; assume 'Symbol' column is present in the CSV
# try:
#     # nse50_df = pd.read_csv("nse50_symbols.csv")
#     nifty_bank_df = pd.read_csv("nifty_bank_symbols.csv")
#     symbols = nifty_bank_df['Symbol'].tolist()
# except FileNotFoundError as e:
#     print(f"File not found error: {e}")
#     symbols = []
# print(symbols)  # Debug line... Print the list of symbols to verify they are loaded correctly

# Fetching bulk data for each NSE 50/NIFTY BANK/NSE 500 stock symbol
# This section retrieves price, volume, and deliverable position data for each stock
# It handles exceptions for each symbol to ensure that the process continues even if one symbol fails
# all_data = []

# for symbol in symbols:
#     try:
#         df = capital_market.price_volume_and_deliverable_position_data(
#                 symbol=symbol, 
#                 # from_date='01-07-2025', 
#                 # to_date='14-08-2025', 
#                 period='1W'
#             )
#         df['Symbol'] = symbol
#         all_data.append(df)
#     except Exception as e:
#         print(f"Failed for {symbol}: {e}")

# try:
#     # If an error occurs, it logs the error and continues with the next symbol
#     if not all_data:
#         print("No data fetched. Please check the symbols or the connection.")   
#     # Concatenate all fetched data into a single DataFrame and save it to a CSV file
#     if all_data:  # Check if all_data is not empty
#         bulk_df = pd.concat(all_data, ignore_index=True)
#         # bulk_df.to_csv('nse50_bulk_data.csv', index=False)
#         bulk_df.to_csv('nifty_bank_bulk_data.csv', index=False)
#         print("Successfully fetched NSE bulk data.")  # Log success message
#     else:
#         print("No data fetched. Please check the symbols or the connection.") 
# except Exception as e:
#     print(f"Error fetching NSE 50, NIFTY BANK or NSE 500 bulk data: {e}")  # Log the error message
#     all_data = []  # Set all_data to an empty list in case of an error to avoid further errors 
