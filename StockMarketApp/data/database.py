# File contains the database connection and models for the StockMarketApp project

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

####----Code to read CSV and upload to MySQL using SQLAlchemy----####
engine = None
try:
#     # Read CSV file using pandas - Code block for uploading NIFTY BANK bulk data
#     df = pd.read_csv('nifty_bank_bulk_data.csv', parse_dates=['Date'], dayfirst=True)
#     # Read CSV file using pandas - Code block for uploading BANK NIFTY index data
    df = pd.read_csv('nifty_bank_index_data.csv', parse_dates=['HistoricalDate'], dayfirst=True)
    # Drop columns not needed
    df = df.drop(['RequestNumber', 'Index Name'], axis=1)
#     # Rename columns to snake_case and compatible with SQL naming conventions
#     df.rename(columns={
#         'Symbol': 'symbol',
#         'Series': 'series',
#         'Date': 'trade_date',
#         'PrevClose': 'prev_close',
#         'OpenPrice': 'open_price',
#         'HighPrice': 'high_price',
#         'LowPrice': 'low_price',
#         'LastPrice': 'last_price',
#         'ClosePrice': 'close_price',
#         'AveragePrice': 'average_price',
#         'TotalTradedQuantity': 'total_traded_quantity',
#         'TurnoverInRs': 'turnover_in_rs',
#         'No.ofTrades': 'number_of_trades',
#         'DeliverableQty': 'deliverable_qty',
#         '%DlyQttoTradedQty': 'percent_dly_qty_to_traded'
#     }, inplace=True)

    # Rename columns for SQL compatibility
    df.rename(columns={
        'INDEX_NAME': 'index_name',
        'HistoricalDate': 'historical_date',
        'OPEN': 'open',
        'HIGH': 'high',
        'LOW': 'low',
        'CLOSE': 'close'
    }, inplace=True)

    # Parse historical_date to datetime
    df['historical_date'] = pd.to_datetime(df['historical_date'], format="%d %b %Y")

#     # Clean and convert data types
#     for col in ['total_traded_quantity', 'number_of_trades', 'deliverable_qty']:
#         df[col] = pd.to_numeric(df[col], errors='coerce')

#     for col in ['prev_close', 'open_price', 'high_price', 'low_price', 'last_price', 'close_price', 'average_price', 'turnover_in_rs', 'percent_dly_qty_to_traded']:
#         df[col] = pd.to_numeric(df[col], errors='coerce')

    # Clean and convert data types for BANK INFTY index data
    for col in ['open', 'high', 'low', 'close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Create SQLAlchemy engine
    engine = create_engine(DB_CONNECTION_STRING)

    # Define metadata and table
    metadata = MetaData()
#     bank_nifty_table = Table(
#         'bank_nifty_data', metadata,
#         Column('id', Integer, primary_key=True, autoincrement=True),
#         Column('symbol', String(20), nullable=False),
#         Column('series', String(10), nullable=False),
#         Column('trade_date', Date, nullable=False),
#         Column('prev_close', Float),
#         Column('open_price', Float),
#         Column('high_price', Float),
#         Column('low_price', Float),
#         Column('last_price', Float),
#         Column('close_price', Float),
#         Column('average_price', Float),
#         Column('total_traded_quantity', BigInteger),
#         Column('turnover_in_rs', DOUBLE),
#         Column('number_of_trades', Integer),
#         Column('deliverable_qty', BigInteger),
#         Column('percent_dly_qty_to_traded', Float),
#         # UniqueConstraint('symbol', 'trade_date', name='uix_symbol_date')
#     )
    bank_nifty_index_table = Table(
        'bank_nifty_index_data', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('index_name', String(30)),
        Column('historical_date', Date),
        Column('open', Double),
        Column('high', Double),
        Column('low', Double),
        Column('close', Double)
    )
    # Create table if not exists
    metadata.create_all(engine)

#     # Insert or replace data using pandas to_sql (replace with 'append' if you want to add without deleting)
#     df.to_sql('bank_nifty_data', con=engine, if_exists='append', index=False, method='multi')
    df.to_sql('bank_nifty_index_data', con=engine, if_exists='append', index=False, method='multi')

    print("Data uploaded successfully.")
except FileNotFoundError:
    print(f"Error: The .csv file was not found.")
except SQLAlchemyError as e:
    print(f"Database error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    if engine:
        engine.dispose()  # Dispose the engine and close all connections

####----Code to read all Bank Nifty bulk data from MySQL using SQLAlchemy----####
def read_bank_nifty_data() -> pd.DataFrame:
    engine = None
    df = None
    try:
        # Create SQLAlchemy engine
        engine = create_engine(DB_CONNECTION_STRING)
        # Read data from the table into a pandas DataFrame
        query = 'SELECT * FROM bank_nifty_data'
        df = pd.read_sql(query, con=engine)
        return df
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        if engine:
            engine.dispose()  # Dispose the engine and close all connections

####----Code to read all Bank Nifty index data from MySQL using SQLAlchemy----####
def read_bank_nifty_index_data() -> pd.DataFrame:
    engine = None
    df = None
    try:
        # Create SQLAlchemy engine
        engine = create_engine(DB_CONNECTION_STRING)
        # Read data from the table into a pandas DataFrame
        query = 'SELECT * FROM bank_nifty_index_data'
        df = pd.read_sql(query, con=engine)
        return df
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        if engine:
            engine.dispose()  # Dispose the engine and close all connections

####----Sample code to connect to MySQL using mysql-connector-python----#### 
# try:
#     connection = mysql.connector.connect(**DB_CONFIG)
#     if connection.is_connected():
#         print("Connection to MySQL was successful!")
#     else:
#         print("Connection failed.")

# except Error as e:
#     print("Error while connecting to MySQL:", e)

# finally:
#     if 'connection' in locals() and connection.is_connected():
#         connection.close()  # Close the connection
#         print("MySQL connection closed.") 
####----Using SQLAlchemy for database operations----####
# Create SQLAlchemy engine for database operations  
engine = create_engine(DB_CONNECTION_STRING)
Base = declarative_base()  # Base class for SQLAlchemy models
# Define a sample model for demonstration purposes
class User(Base):
    __tablename__ = 'test_table'  # Change this to your actual table name
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)

try:    
    engine.connect()
    print("Connection to MySQL was successful!")
    Session = sessionmaker(bind=engine)
    session = Session()  # Create a new session

    # Read all data from the database table
    def read_data():
        try:
            users = session.query(User).all()  # Query all records from the User table
            data = [{'id': user.id, 'name': user.name, 'age': user.age} for user in users]
            return pd.DataFrame(data)
        except Exception as e:
            print("Error while reading data:", e)
            return pd.DataFrame()
    
    # Read specific data from the database table
    def read_specific_data(name: str) -> pd.DataFrame:
        try:
            user = session.query(User).filter(User.name == name).first()
            if user:
                data = [ojb.__dict__ for ojb in [user]]
                for d in data:
                    d.pop('_sa_instance_state', None)
                return pd.DataFrame(data)
                # return pd.DataFrame(user.__dict__, index=[0])
            else:
                message = f"No user found with name: {name}"
                return pd.DataFrame({'message': [message]})
        except Exception as e:
            print("Error while reading specific data:", e)
            return None
        
    # Function call to read data
    # read_data()
    
    # Function call to read specific data
    # df = read_specific_data("Alice")
    # print(df.to_string(index=False))
    
except Exception as e:
    print("Error while connecting to MySQL:", e)    

finally:
    session.close()  # Close the session
    print("SQLAlchemy session closed.") 
    if 'engine' in locals() and engine is not None:
        engine.dispose()
        print("MySQL connection closed.") 