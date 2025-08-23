# File contains the database connection and models for the StockMarketApp project

import mysql.connector
from mysql.connector import Error
import sys
import os
import pandas as pd
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