# File contains the database connection and models for the StockMarketApp project

import mysql.connector
from mysql.connector import Error
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from config.database_config import DB_CONFIG  
from config.database_config import DB_CONNECTION_STRING
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
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

    # Read data from the database table
    def read_data():
        try:
            users = session.query(User).all()  # Query all records from the User table
            for user in users:
                print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")
        except Exception as e:
            print("Error while reading data:", e)
        finally:
            return users
    
    # Function call to read data
    read_data()
    
except Exception as e:
    print("Error while connecting to MySQL:", e)    

finally:
    session.close()  # Close the session
    print("SQLAlchemy session closed.") 
    if 'engine' in locals() and engine is not None:
        engine.dispose()
        print("MySQL connection closed.") 