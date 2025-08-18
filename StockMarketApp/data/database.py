# File contains the database connection and models for the StockMarketApp project

import mysql.connector
from mysql.connector import Error
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database_config import DB_CONFIG

try:
    connection = mysql.connector.connect(**DB_CONFIG)
    if connection.is_connected():
        print("Connection to MySQL was successful!")
    else:
        print("Connection failed.")

except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()  # Close the connection
        print("MySQL connection closed.") 