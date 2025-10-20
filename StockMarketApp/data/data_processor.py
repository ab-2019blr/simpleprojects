# File contains data processing functions for the StockMarketApp project
# This file is responsible for processing and transforming stock market data
# to be used in the application, including data cleaning, normalization, and feature extraction.
# It also contains functions for calculating technical indicators, market statistics, and performance metrics.
import mysql.connector
from mysql.connector import Error
import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from config.database_config import DB_CONFIG  
from config.database_config import DB_CONNECTION_STRING
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Double, Date, BigInteger, UniqueConstraint
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base

# RSI claculation function using pandas 
def compute_rsi(series, period=14): 
    engine = None
    df = None
    try:
        # Create SQLAlchemy engine
        engine = create_engine(DB_CONNECTION_STRING)
        # Read data from the table into a pandas DataFrame
        query = 'SELECT historical_date, close FROM bank_nifty_index_data ORDER BY historical_date'
        df = pd.read_sql(query, con=engine)
        df['date'] = pd.to_datetime(df['historical_date'])
        delta = series.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period, min_periods=period).mean()
        avg_loss = loss.rolling(window=period, min_periods=period).mean()
        rs = avg_gain / avg_loss
        rsi_value = 100 - (100 / (1 + rs))
        df_rsi = pd.DataFrame({'RSI': rsi_value})
        return df['date'], df_rsi
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        if engine:
            engine.dispose()  # Dispose the engine and close all connections


# DMA calculation function using pandas
def compute_dma(series, short_period=20, long_period=50):
    engine = None
    df = None
    try:
        # Create SQLAlchemy engine
        engine = create_engine(DB_CONNECTION_STRING)
        # Read data from the table into a pandas DataFrame
        query = 'SELECT historical_date, close FROM bank_nifty_index_data ORDER BY historical_date'
        df = pd.read_sql(query, con=engine)
        df['date'] = pd.to_datetime(df['historical_date']) 
        df['20DMA'] = series.rolling(window=short_period).mean()
        df['50DMA'] = series.rolling(window=long_period).mean()
        return df['date'], df['close'], df['20DMA'], df['50DMA']  
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        if engine:
            engine.dispose()  # Dispose the engine and close all connections

