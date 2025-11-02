# This modlue handles processing of portfolio data including transaction records and performance metrics.
# It also fetches and processes data from the database related to user portfolios.

import mysql.connector
from mysql.connector import Error
import sys
import os
import json
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from config.database_config import DB_CONFIG  
from config.database_config import DB_CONNECTION_STRING
from sqlalchemy import create_engine, func, MetaData, Table, Column, Integer, String, Float, Double, Date, BigInteger, UniqueConstraint, JSON, DECIMAL, DateTime, Enum, text
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import enum

Base = declarative_base()  # Base class for SQLAlchemy models
# ================================================
# DATABASE MODELS
# ================================================
class TransactionType(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_symbol = Column(String(20), nullable=False, index=True)
    stock_name = Column(String(100), nullable=False)
    transaction_date = Column(Date, nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    transaction_type = Column(Enum(TransactionType), default=TransactionType.BUY)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class CurrentPrice(Base):
    __tablename__ = 'current_prices'
    
    stock_symbol = Column(String(20), primary_key=True)
    stock_name = Column(String(100), nullable=False)
    current_price = Column(DECIMAL(10, 2), nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# ================================================
# DATABASE CONNECTION
# ================================================

engine = create_engine(
    DB_CONNECTION_STRING,
    echo=False, 
    pool_pre_ping=True,
    pool_size=10,  
    max_overflow=20,  
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_timeout=30  # Add timeout
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ================================================
# DATABASE INITIALIZATION
# ================================================

def init_database():
    # Initialize database tables
    try:
        Base.metadata.create_all(bind=engine)
        return True, "Database initialized successfully"
    except Exception as e:
        return False, f"Error initializing database: {str(e)}"

def get_db_session():
    # Get database session
    return SessionLocal()

# ================================================
# STOCK DATA
# ================================================

STOCK_LIST = [
    ("TCS", "Tata Consultancy Services"),
    ("RELIANCE", "Reliance Industries"),
    ("INFY", "Infosys"),
    ("HDFCBANK", "HDFC Bank"),
    ("ICICIBANK", "ICICI Bank"),
    ("HINDUNILVR", "Hindustan Unilever"),
    ("ITC", "ITC Limited"),
    ("SBIN", "State Bank of India"),
    ("BHARTIARTL", "Bharti Airtel"),
    ("KOTAKBANK", "Kotak Mahindra Bank"),
    ("LT", "Larsen & Toubro"),
    ("AXISBANK", "Axis Bank"),
    ("WIPRO", "Wipro"),
    ("MARUTI", "Maruti Suzuki"),
    ("TATAMOTORS", "Tata Motors"),
    ("HCLTECH", "HCL Technologies"),
    ("SUNPHARMA", "Sun Pharmaceutical"),
    ("BAJFINANCE", "Bajaj Finance"),
    ("TITAN", "Titan Company"),
    ("ASIANPAINT", "Asian Paints")
]

# Default stock prices
DEFAULT_PRICES = {
    "TCS": 3850.00, "RELIANCE": 2450.00, "INFY": 1650.00,
    "HDFCBANK": 1580.00, "ICICIBANK": 1120.00, "HINDUNILVR": 2380.00,
    "ITC": 450.00, "SBIN": 785.00, "BHARTIARTL": 1520.00,
    "KOTAKBANK": 1750.00, "LT": 3450.00, "AXISBANK": 1085.00,
    "WIPRO": 485.00, "MARUTI": 12500.00, "TATAMOTORS": 920.00,
    "HCLTECH": 1820.00, "SUNPHARMA": 1680.00, "BAJFINANCE": 7250.00,
    "TITAN": 3420.00, "ASIANPAINT": 2890.00
}

def get_stock_list():
    # Return list of available stocks
    return STOCK_LIST

# ================================================
# VALIDATION FUNCTIONS
# ================================================

def validate_transaction(stock_symbol, quantity, unit_price):
    # Validate transaction data
    errors = []
    
    if quantity <= 0:
        errors.append("Quantity must be greater than 0")
    if unit_price <= 0:
        errors.append("Unit price must be greater than 0")
    
    # Check if stock exists in our list
    valid_symbols = [symbol for symbol, _ in STOCK_LIST]
    if stock_symbol not in valid_symbols:
        errors.append("Invalid stock symbol")
    
    return len(errors) == 0, errors

# ================================================
# TRANSACTION CRUD OPERATIONS
# ================================================

def add_transaction(stock_symbol, stock_name, transaction_date, quantity, unit_price):
    # Add transaction to the database
    # Validate first
    valid, errors = validate_transaction(stock_symbol, quantity, unit_price)
    if not valid:
        return False, "; ".join(errors)
    
    session = None
    try:
        session = get_db_session()
        
        # Create the transaction
        new_transaction = Transaction(
            stock_symbol=stock_symbol,
            stock_name=stock_name,
            transaction_date=transaction_date,
            quantity=quantity,
            unit_price=unit_price,
            transaction_type=TransactionType.BUY
        )
        
        session.add(new_transaction)
        
        # ⭐ CRITICAL FIX: Ensure current_price exists for this stock
        existing_price = session.query(CurrentPrice).filter(
            CurrentPrice.stock_symbol == stock_symbol
        ).first()
        
        if not existing_price:
            # If price doesn't exist, create it with the transaction's unit price
            new_price = CurrentPrice(
                stock_symbol=stock_symbol,
                stock_name=stock_name,
                current_price=unit_price  # Use transaction price as initial current price
            )
            session.add(new_price)
            print(f"Created new current_price entry for {stock_symbol}")
        
        # Commit both transaction and price (if new)
        session.commit()
        
        # Return transaction ID for reference
        transaction_id = new_transaction.id
        return True, f"Transaction #{transaction_id} added successfully"
    
    except Exception as e:
        if session:
            session.rollback()
        return False, f"Error adding transaction: {str(e)}"
    
    finally:
        if session:
            session.close()


# Also add this helper function to sync missing prices
def sync_missing_prices():
    # Sync missing current prices for stocks in transactions
    session = None
    try:
        session = get_db_session()
        
        # Get all unique stocks from transactions
        stocks_in_transactions = session.query(
            Transaction.stock_symbol,
            Transaction.stock_name,
            func.avg(Transaction.unit_price).label('avg_price')
        ).group_by(
            Transaction.stock_symbol,
            Transaction.stock_name
        ).all()
        
        # Get all stocks that have prices
        existing_prices = {
            p.stock_symbol 
            for p in session.query(CurrentPrice.stock_symbol).all()
        }
        
        # Find missing prices
        new_prices = []
        for stock in stocks_in_transactions:
            if stock.stock_symbol not in existing_prices:
                new_prices.append(
                    CurrentPrice(
                        stock_symbol=stock.stock_symbol,
                        stock_name=stock.stock_name,
                        current_price=float(stock.avg_price)  # Use average transaction price
                    )
                )
        
        if new_prices:
            session.bulk_save_objects(new_prices)
            session.commit()
            return True, f"Synced {len(new_prices)} missing price entries"
        else:
            return True, "All prices are already synced"
    
    except Exception as e:
        if session:
            session.rollback()
        return False, f"Error syncing prices: {str(e)}"
    
    finally:
        if session:
            session.close()

def get_all_transactions():
    # Fetch all transactions from database
    session = None
    try:
        session = get_db_session()
        transactions = session.query(Transaction).order_by(
            Transaction.transaction_date.desc(),
            Transaction.created_at.desc()
        ).all()
        
        result = [{
            'id': t.id,
            'stock_symbol': t.stock_symbol,
            'stock_name': t.stock_name,
            'transaction_date': t.transaction_date,
            'quantity': t.quantity,
            'unit_price': float(t.unit_price),
            'created_at': t.created_at
        } for t in transactions]
        
        return True, result
    
    except Exception as e:
        return False, f"Error fetching transactions: {str(e)}"
    
    finally:
        if session:
            session.close()

def delete_transaction(transaction_id):
    # Delete transaction by ID
    session = None
    try:
        session = get_db_session()
        transaction = session.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()
        
        if transaction:
            session.delete(transaction)
            session.commit()
            return True, "Transaction deleted successfully"
        else:
            return False, "Transaction not found"
    
    except Exception as e:
        if session:
            session.rollback()
        return False, f"Error deleting transaction: {str(e)}"
    
    finally:
        if session:
            session.close()

# ================================================
# PORTFOLIO OPERATIONS
# ================================================

def get_portfolio_summary():
    # Calculate portfolio summary
    session = None
    try:
        session = get_db_session()
        
        # Group by stock and calculate average buy price
        holdings = session.query(
            Transaction.stock_symbol,
            Transaction.stock_name,
            func.sum(Transaction.quantity).label('quantity'),
            func.sum(Transaction.quantity * Transaction.unit_price).label('total_cost')
        ).filter(
            Transaction.transaction_type == TransactionType.BUY
        ).group_by(
            Transaction.stock_symbol,
            Transaction.stock_name
        ).all()
        
        if not holdings:
            return True, []
        
        # Get all current prices in ONE query (OPTIMIZATION)
        symbols = [h.stock_symbol for h in holdings]
        prices = session.query(CurrentPrice).filter(
            CurrentPrice.stock_symbol.in_(symbols)
        ).all()
        
        # Create price lookup dictionary for O(1) access
        price_dict = {p.stock_symbol: float(p.current_price) for p in prices}
        
        result = []
        for holding in holdings:
            # Convert to int to ensure it's not zero
            quantity = int(holding.quantity)
            
            if quantity <= 0:
                continue
            
            # CRITICAL FIX: Convert both to float before division
            total_cost = float(holding.total_cost)
            avg_price = total_cost / quantity
            
            # Get current price, fallback to avg_price if not found
            current_price = price_dict.get(holding.stock_symbol, avg_price)
            
            result.append({
                'stock_symbol': holding.stock_symbol,
                'stock_name': holding.stock_name,
                'quantity': quantity,
                'avg_buy_price': round(avg_price, 2),
                'current_price': round(current_price, 2)
            })
        
        return True, result
    
    except Exception as e:
        import traceback
        error_msg = f"Error fetching portfolio summary: {str(e)}"
        print(f"DEBUG - {error_msg}")
        print(f"DEBUG - Traceback: {traceback.format_exc()}")
        return False, error_msg
    
    finally:
        if session:
            session.close()

def calculate_portfolio_metrics(portfolio_data):
    # Calculate portfolio performance metrics
    default_metrics = {
        'total_investment': 0.0,
        'current_value': 0.0,
        'net_pl': 0.0,
        'pl_percent': 0.0,
        'total_stocks': 0
    }
    
    if not portfolio_data or len(portfolio_data) == 0:
        return default_metrics
    
    try:
        total_investment = sum([
            holding['quantity'] * holding['avg_buy_price'] 
            for holding in portfolio_data
        ])
        
        current_value = sum([
            holding['quantity'] * holding['current_price'] 
            for holding in portfolio_data
        ])
        
        net_pl = current_value - total_investment
        pl_percent = (net_pl / total_investment * 100) if total_investment > 0 else 0.0
        
        return {
            'total_investment': round(total_investment, 2),
            'current_value': round(current_value, 2),
            'net_pl': round(net_pl, 2),
            'pl_percent': round(pl_percent, 2),
            'total_stocks': len(portfolio_data)
        }
    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
        return default_metrics

# ================================================
# PRICE MANAGEMENT 
# ================================================

def initialize_default_prices():
    # Initialize default prices in the database
    session = None
    try:
        session = get_db_session()
        
        # Check if any prices exist
        count = session.query(func.count(CurrentPrice.stock_symbol)).scalar()
        if count > 0:
            return True, "Prices already initialized"
        
        # Batch insert all prices at once (OPTIMIZATION)
        price_objects = [
            CurrentPrice(
                stock_symbol=symbol,
                stock_name=name,
                current_price=DEFAULT_PRICES.get(symbol, 1000.00)
            )
            for symbol, name in STOCK_LIST
        ]
        
        session.bulk_save_objects(price_objects)
        session.commit()
        return True, "Default prices initialized successfully"
    
    except Exception as e:
        if session:
            session.rollback()
        return False, f"Error initializing prices: {str(e)}"
    finally:
        if session:
            session.close()

def update_current_prices():
    # Update current prices with simulated data (OPTIMIZED)
    session = None
    try:
        import random
        
        session = get_db_session()
        
        # Get all existing prices in one query
        existing_prices = {
            p.stock_symbol: p 
            for p in session.query(CurrentPrice).all()
        }
        
        new_prices = []
        updates_count = 0
        
        for symbol, name in STOCK_LIST:
            if symbol in existing_prices:
                # Update with slight random change (simulating market movement)
                change_percent = random.uniform(-0.02, 0.02)
                new_price = float(existing_prices[symbol].current_price) * (1 + change_percent)
                existing_prices[symbol].current_price = round(new_price, 2)
                existing_prices[symbol].last_updated = datetime.utcnow()
                updates_count += 1
            else:
                # Insert default prices for stocks not in database
                new_prices.append(
                    CurrentPrice(
                        stock_symbol=symbol,
                        stock_name=name,
                        current_price=DEFAULT_PRICES.get(symbol, 1000.00)
                    )
                )
        
        # Batch insert new prices
        if new_prices:
            session.bulk_save_objects(new_prices)
        
        session.commit()
        
        total_updates = updates_count + len(new_prices)
        return True, f"Prices updated successfully ({total_updates} stocks)"
    
    except Exception as e:
        if session:
            session.rollback()
        return False, f"Error updating prices: {str(e)}"
    
    finally:
        if session:
            session.close()

def get_last_price_update():
    # Get timestamp of last price update
    session = None
    try:
        session = get_db_session()
        latest = session.query(func.max(CurrentPrice.last_updated)).scalar()
        return latest
    except Exception as e:
        print(f"Error getting last update: {str(e)}")
        return None
    finally:
        if session:
            session.close()

# ================================================
# UTILITY FUNCTIONS
# ================================================

def test_connection():
    # Test database connection
    session = None
    try:
        session = get_db_session()
        session.execute(text("SELECT 1"))  # Fixed: Use text() wrapper
        session.close()
        return True, "Database connection successful"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

def get_database_stats():
    # Get basic database statistics
    session = None
    try:
        session = get_db_session()
        
        total_transactions = session.query(func.count(Transaction.id)).scalar()
        total_stocks = session.query(func.count(func.distinct(Transaction.stock_symbol))).scalar()
        total_prices = session.query(func.count(CurrentPrice.stock_symbol)).scalar()
        
        return {
            'total_transactions': total_transactions or 0,
            'total_stocks': total_stocks or 0,
            'total_prices': total_prices or 0,
            'connection_status': 'Connected'
        }
    except Exception as e:
        return {
            'total_transactions': 0,
            'total_stocks': 0,
            'total_prices': 0,
            'connection_status': f'Error: {str(e)}'
        }
    finally:
        if session:
            session.close()
