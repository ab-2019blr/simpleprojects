#!/usr/bin/env python3
"""
Quick Fix Script - Sync Missing Current Prices
Run this ONCE to fix existing data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your backend
import data.portfolio_data_processor as backend

def main():
    print("=" * 60)
    print("QUICK FIX: Syncing Missing Current Prices")
    print("=" * 60)
    
    # Test connection first
    print("\n1. Testing database connection...")
    success, message = backend.test_connection()
    if success:
        print(f"   ✅ {message}")
    else:
        print(f"   ❌ {message}")
        return
    
    # Get database stats
    print("\n2. Checking database stats...")
    stats = backend.get_database_stats()
    print(f"   Transactions: {stats['total_transactions']}")
    print(f"   Stocks in portfolio: {stats['total_stocks']}")
    print(f"   Current prices: {stats.get('total_prices', 0)}")
    
    # Check for missing prices
    print("\n3. Checking for missing prices...")
    session = backend.get_db_session()
    
    try:
        # Get stocks from transactions
        from sqlalchemy import func
        stocks_in_trans = session.query(
            backend.Transaction.stock_symbol,
            backend.Transaction.stock_name
        ).group_by(
            backend.Transaction.stock_symbol,
            backend.Transaction.stock_name
        ).all()
        
        print(f"   Found {len(stocks_in_trans)} unique stocks in transactions:")
        for stock in stocks_in_trans:
            print(f"      - {stock.stock_symbol}: {stock.stock_name}")
        
        # Get stocks with prices
        stocks_with_prices = {
            p.stock_symbol 
            for p in session.query(backend.CurrentPrice.stock_symbol).all()
        }
        
        print(f"\n   Found {len(stocks_with_prices)} stocks with current prices:")
        for symbol in stocks_with_prices:
            print(f"      - {symbol}")
        
        # Find missing
        missing = []
        for stock in stocks_in_trans:
            if stock.stock_symbol not in stocks_with_prices:
                missing.append(stock)
        
        if missing:
            print(f"\n   ⚠️  Found {len(missing)} stocks WITHOUT current prices:")
            for stock in missing:
                print(f"      - {stock.stock_symbol}: {stock.stock_name}")
        else:
            print("\n   ✅ All stocks have current prices!")
    
    finally:
        session.close()
    
    # Sync missing prices
    if missing:
        print("\n4. Syncing missing prices...")
        success, message = backend.sync_missing_prices()
        if success:
            print(f"   ✅ {message}")
        else:
            print(f"   ❌ {message}")
    
    # Verify portfolio now works
    print("\n5. Testing portfolio summary...")
    success, data = backend.get_portfolio_summary()
    if success:
        print(f"   ✅ Portfolio loaded successfully!")
        print(f"   Holdings: {len(data)}")
        if data:
            print("\n   Portfolio contents:")
            for holding in data:
                print(f"      - {holding['stock_symbol']}: {holding['quantity']} shares")
                print(f"        Avg Buy: ₹{holding['avg_buy_price']:.2f}")
                print(f"        Current: ₹{holding['current_price']:.2f}")
        else:
            print("   ⚠️  Portfolio is still empty!")
    else:
        print(f"   ❌ Error: {data}")
    
    print("\n" + "=" * 60)
    print("Fix complete! Now refresh your Streamlit app.")
    print("=" * 60)

if __name__ == "__main__":
    main()
    