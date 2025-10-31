# Read operation from local .csv files for dashboard and other pages
import pandas as pd
import base64
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
local_csv_path = os.path.join(os.path.dirname(__file__), "nifty_advance_decline_data.csv")
top_gainers_csv_path = os.path.join(os.path.dirname(__file__), "nifty_top_gainers_data.csv")
top_losers_csv_path = os.path.join(os.path.dirname(__file__), "nifty_top_losers_data.csv")
index_valuation_csv_path = os.path.join(os.path.dirname(__file__), "nifty_index_valuation_data.csv")
DEFAULT_FILE_NAME = local_csv_path
DEFAULT_FILE_NAME_TOP_GAINERS = top_gainers_csv_path
DEFAULT_FILE_NAME_TOP_LOSERS = top_losers_csv_path
DEFAULT_FILE_NAME_INDEX_VALUATION = index_valuation_csv_path

def read_csv_to_dataframe(file_path=None) -> pd.DataFrame:
    # Check if a file_path was provided. If not, use the default.
    if file_path is None:
        file_path = DEFAULT_FILE_NAME
    # Check if the file exists 
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return pd.DataFrame()  # Return empty DataFrame if file not found
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully read CSV file: {file_path}")
        return df
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

def read_top_gainers_csv_to_dataframe(file_path=None) -> pd.DataFrame:
    # Check if a file_path was provided. If not, use the default.
    if file_path is None:
        file_path = DEFAULT_FILE_NAME_TOP_GAINERS
    # Check if the file exists 
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return pd.DataFrame()  # Return empty DataFrame if file not found
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully read CSV file: {file_path}")
        return df
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

def read_top_losers_csv_to_dataframe(file_path=None) -> pd.DataFrame:
    # Check if a file_path was provided. If not, use the default.
    if file_path is None:
        file_path = DEFAULT_FILE_NAME_TOP_LOSERS
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return pd.DataFrame()  # Return empty DataFrame if file not found
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully read CSV file: {file_path}")
        return df
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error 
    
def read_index_valuation_csv_to_dataframe(file_path=None) -> pd.DataFrame:
    # Check if a file_path was provided. If not, use the default.
    if file_path is None:
        file_path = DEFAULT_FILE_NAME_INDEX_VALUATION
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return pd.DataFrame()  # Return empty DataFrame if file not found
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully read CSV file: {file_path}")
        return df
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error 