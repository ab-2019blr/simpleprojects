# File to configure the  database settings for the StockMarketApp project

from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file in project root

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT', '3306')  # Default MySQL port is 3306
DB_CONFIG = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASS,
    'database': DB_NAME,
    'port': DB_PORT
}
DB_CONNECTION_STRING = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# Optional: Uncomment the line below to print the database configuration for debugging
# print("Database configuration loaded successfully.")