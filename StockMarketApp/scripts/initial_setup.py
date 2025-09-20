# File contains initial data setup for the database and environment variables for the project setup and configuration   
# This script is executed when the project is initialized
# to ensure that the database is ready and environment variables are set correctly.
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database_config import DB_CONFIG
from sqlalchemy import create_engine

# Read CSV into DataFrame
local_data_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'nifty_bank_bulk_data.csv')
df = pd.read_csv(local_data_file_path, parse_dates=['Date'], dayfirst=True)

# Create SQLAlchemy engine
engine = create_engine(DB_CONFIG)

# Insert data into MySQL table (append to existing)
df.to_sql('your_table_name', con=engine, if_exists='append', index=False)
print("Initial data setup completed successfully.")
# Note: Replace 'your_table_name' with the actual table name where data needs to be inserted.
# Optional: Uncomment the line below to print the DataFrame for debugging
print(df.head())  # Print first few rows of the DataFrame to verify data is loaded correctly