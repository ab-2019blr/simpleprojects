# Model Portfolio Page for Stock Market Application
# This page records stock transactions and displays the user's portfolio performance. 

import streamlit as st
import pandas as pd
from datetime import date 
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data.portfolio_data_processor as backend
# Force disable all caching temporarily for testing
st.cache_data.clear()
# Set page configuration
st.set_page_config(page_title="Portfolio", layout="wide", page_icon="💼")

# st.title("Model Portfolio")
# st.caption("Track your stock transactions and portfolio performance.")

# ================================================
# SESSION STATE INITIALIZATION
# ================================================

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

if 'refresh_data' not in st.session_state:
    st.session_state.refresh_data = False

if 'show_delete_section' not in st.session_state:
    st.session_state.show_delete_section = False

if 'db_initialized' not in st.session_state:
    with st.spinner("Initializing database..."):
        success, message = backend.init_database()
        st.session_state.db_initialized = success
        if success:
            # Ensure current prices are available
            backend.initialize_default_prices()
        else:
            st.error(f"⚠️ {message}")
            st.stop()

# ================================================
# DATABASE HEALTH CHECK
# ================================================

# @st.cache_data(ttl=60)
def check_db_health():
    # Check database health
    return backend.test_connection()

# Perform health check at startup
health_success, health_message = check_db_health()
if not health_success:
    st.error(f"⚠️ Database connection issue: {health_message}")
    st.info("Please check your MySQL server and .env configuration")
    st.stop()

# ================================================
# DATA CACHING (Performance Optimization)
# ================================================

# @st.cache_data(ttl=60, show_spinner=False)  # Reduced TTL to 60 seconds
def get_cached_portfolio_summary():
    # Cached version of portfolio summary - Returns immutable tuple
    success, data = backend.get_portfolio_summary()
    # Return immutable tuple to prevent cache pollution
    return tuple(data) if success and data else ()

# @st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
def get_cached_stock_list():
    # Cached version of stock list
    return backend.get_stock_list()

# @st.cache_data(ttl=30, show_spinner=False)  # Reduced TTL to 30 seconds
def get_cached_transactions():
    # Cached version of all transactions - Returns immutable tuple
    success, data = backend.get_all_transactions()
    # Return immutable tuple to prevent cache pollution
    return tuple(data) if success and data else ()

# ================================================
# CUSTOM CSS STYLING
# ================================================

st.markdown("""
    <style> 
    /* Main header styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #21808D;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .subtitle {
        text-align: center;
        color: white;
        font-weight: 500
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
                    
    /* Metric card styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
    }
            
    /* Form styling */
    .stForm {
        background-color: skyblue;
        color: black;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(94, 82, 64, 0.2);
    }
    
    /* Form label styling */
    /* Change color of all form labels" */
    div[data-testid="stForm"] label {
        color: black !important;  /* Change this color */
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Button styling enhancements */
    .stButton > button {
        background-color: #21808D;
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
   
    /* Table styling */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(94, 82, 64, 0.12);
        border-radius: 0.5rem;
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid rgba(94, 82, 64, 0.2);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ================================================
# MAIN APP HEADER
# ================================================

st.markdown('<h1 class="main-header">Stock Portfolio Manager</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Track your investments, monitor performance, and make informed decisions</p>', unsafe_allow_html=True)

# ================================================
# TOP CONTROLS BAR
# ================================================

top_col1, top_col2, top_col3, top_col4 = st.columns([2, 1, 1, 1])

with top_col2:
    if st.button("Refresh Prices", use_container_width=True):
        with st.spinner("Updating current prices... Please wait"):
            # Clear all caches first
            st.cache_data.clear()
            
            # Update prices
            success, message = backend.update_current_prices()
            
            if success:
                # Wait for DB to commit
                time.sleep(0.8)
                
                # Clear caches again to ensure fresh data
                st.cache_data.clear()
                
                # Update session state
                st.session_state.refresh_data = True
                
                st.success(f"✅ {message}")
                time.sleep(0.5)  # Show success message briefly
                st.rerun()
            else:
                st.error(f"❌ {message}")

with top_col3:
    last_update = backend.get_last_price_update()
    if last_update:
        st.info(f"🕐 Last Updated: {last_update.strftime('%H:%M:%S')}")
    else:
        st.info("No updates yet")

with top_col4:
    if st.button("Manage Transactions", use_container_width=True):
        st.session_state.show_delete_section = not st.session_state.show_delete_section

st.divider()

# ================================================
# MAIN TWO-COLUMN LAYOUT
# ================================================

col_left, col_right = st.columns([2, 1], gap="large")

# ================================================
# LEFT COLUMN - PORTFOLIO DISPLAY
# ================================================

with col_left:
    # Header with manual refresh option
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.subheader("Portfolio Holdings")
    with col_header2:
        if st.button("Refresh Data", use_container_width=True, key="refresh_portfolio"):
            st.cache_data.clear()
            st.rerun()
    
    try:
        # LOADING STATE
        with st.spinner("Loading portfolio data..."):
            portfolio_data = get_cached_portfolio_summary()
        
        if portfolio_data and len(portfolio_data) > 0:
            # Convert tuple to list for processing
            portfolio_list = list(portfolio_data)
            
            # Calculate metrics using backend
            metrics = backend.calculate_portfolio_metrics(portfolio_list)
            
            # ============================================
            # PORTFOLIO SUMMARY CARDS
            # ============================================
            metric_cols = st.columns(4)
            
            with metric_cols[0]:
                st.metric(
                    label="Total Investment",
                    value=f"₹{metrics['total_investment']:,.2f}"
                )
            
            with metric_cols[1]:
                st.metric(
                    label="Current Value",
                    value=f"₹{metrics['current_value']:,.2f}"
                )
            
            with metric_cols[2]:
                delta_color = "normal" if metrics['net_pl'] >= 0 else "inverse"
                st.metric(
                    label="Net P/L",
                    value=f"₹{metrics['net_pl']:,.2f}",
                    delta=f"{metrics['pl_percent']:.2f}%",
                    delta_color=delta_color
                )
            
            with metric_cols[3]:
                st.metric(
                    label="Total Stocks",
                    value=metrics['total_stocks']
                )
            
            st.divider()
            
            # ============================================
            # HOLDINGS TABLE (OPTIMIZED)
            # ============================================
            
            st.markdown("#### Detailed Holdings")
            
            # Create DataFrame from tuple data
            df = pd.DataFrame(portfolio_list)
            
            # Vectorized calculations (OPTIMIZATION - faster than loops)
            df['Investment'] = df['quantity'] * df['avg_buy_price']
            df['Current Value'] = df['quantity'] * df['current_price']
            df['P/L Amount'] = df['Current Value'] - df['Investment']
            df['P/L %'] = (df['P/L Amount'] / df['Investment'] * 100).round(2)
            
            # Prepare display dataframe
            display_df = df[[
                'stock_name', 'stock_symbol', 'quantity', 
                'avg_buy_price', 'current_price', 'Investment', 
                'Current Value', 'P/L Amount', 'P/L %'
            ]].copy()
            
            display_df.columns = [
                'Stock Name', 'Symbol', 'Qty', 
                'Avg Buy Price', 'Current Price', 'Investment', 
                'Current Value', 'P/L Amount', 'P/L %'
            ]
            
            # Style the dataframe with color coding
            def highlight_pl(val):
                """Color code positive/negative values"""
                if isinstance(val, (int, float)):
                    if val >= 0:
                        return 'color: #21808D; font-weight: 600'
                    else:
                        return 'color: #C0152F; font-weight: 600'
                return ''
            
            def highlight_row(row):
                """Highlight entire row based on P/L"""
                if row['P/L Amount'] >= 0:
                    return ['background-color: rgba(33, 128, 141, 0.08)'] * len(row)
                else:
                    return ['background-color: rgba(192, 21, 47, 0.08)'] * len(row)
            
            styled_df = display_df.style.format({
                'Avg Buy Price': '₹{:.2f}',
                'Current Price': '₹{:.2f}',
                'Investment': '₹{:,.2f}',
                'Current Value': '₹{:,.2f}',
                'P/L Amount': '₹{:,.2f}',
                'P/L %': '{:.2f}%'
            }).applymap(
                highlight_pl, 
                subset=['P/L Amount', 'P/L %']
            ).apply(highlight_row, axis=1)
            
            # Display the table
            st.dataframe(
                styled_df,
                use_container_width=True,
                # height=400,
                hide_index=True
            )
            
            # Export to CSV option
            csv = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Portfolio as CSV",
                data=csv,
                file_name=f"portfolio_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        else:
            # Empty state
            st.info("📊 No portfolio data yet. Add your first transaction using the form on the right!")
            st.markdown("""
                ### 🚀 Getting Started
                1. Select a stock from the dropdown
                2. Enter transaction details
                3. Click "Add Transaction"
                4. Watch your portfolio grow!
            """)
    
    except Exception as e:
        st.error(f"⚠️ Error loading portfolio: {str(e)}")
        st.info("Please check your database connection and try refreshing the page.")

# ================================================
# DELETE TRANSACTIONS SECTION (Collapsible)
# ================================================

if st.session_state.show_delete_section:
    with col_left:
        st.markdown("---")
        with st.expander("Delete Transactions", expanded=True):
            try:
                # Only fetch when section is visible (LAZY LOADING)
                transactions = list(get_cached_transactions())  # Convert from tuple
                
                if transactions:
                    trans_df = pd.DataFrame(transactions)
                    trans_df['Display'] = trans_df.apply(
                        lambda x: f"{x['stock_name']} ({x['stock_symbol']}) - {x['quantity']} shares @ ₹{x['unit_price']} on {x['transaction_date'].strftime('%d-%b-%Y')}", 
                        axis=1
                    )
                    
                    selected_trans = st.selectbox(
                        "Select transaction to delete:",
                        options=trans_df['id'].tolist(),
                        format_func=lambda x: trans_df[trans_df['id']==x]['Display'].values[0]
                    )
                    
                    col_del1, col_del2 = st.columns(2)
                    
                    with col_del1:
                        if st.button("Confirm Delete", type="secondary", use_container_width=True):
                            with st.spinner("Deleting transaction..."):
                                success, message = backend.delete_transaction(selected_trans)
                                if success:
                                    st.success(f"✅ {message}")
                                    st.cache_data.clear()
                                    time.sleep(0.5)
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                    
                    with col_del2:
                        if st.button("❌ Cancel", use_container_width=True):
                            st.session_state.show_delete_section = False
                            st.rerun()
                else:
                    st.info("No transactions to delete")
                    
            except Exception as e:
                st.error(f"Error loading transactions: {str(e)}")

# ================================================
# RIGHT COLUMN - TRANSACTION FORM
# ================================================

with col_right:
    st.subheader("Add New Transaction")
    
    # LOADING STATE for stock list
    with st.spinner("Loading stock list..."):
        stock_list = get_cached_stock_list()
    
    st.markdown("""
    <style>
    /* Style form buttons specifically */
    div[data-testid="stForm"] button[kind="primary"],
    div[data-testid="stForm"] button[kind="secondary"] {
        background: linear-gradient(135deg, #48A9B4 0%, #3B8C95 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 0.5rem !important;
        box-shadow: 0 2px 8px rgba(72, 169, 180, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stForm"] button:hover {
        box-shadow: 0 4px 12px rgba(72, 169, 180, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    div[data-testid="stForm"] button p {
        color: white !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.form("transaction_form", clear_on_submit=True):
        st.markdown("##### Transaction Details")
        
        # Stock selection dropdown
        stock_options = {f"{s[0]} - {s[1]}": s for s in stock_list}
        
        selected_stock = st.selectbox(
            "Stock Name *",
            options=list(stock_options.keys()),
            help="Select the stock you want to add to your portfolio",
            key="stock_select"
        )
        
        # Transaction date with calendar picker
        trans_date = st.date_input(
            "Transaction Date *",
            value=date.today(),
            max_value=date.today(),
            help="Select the date when you purchased the stock",
            key="trans_date"
        )
        
        # Quantity input
        quantity = st.number_input(
            "Quantity *",
            min_value=1,
            value=1,
            step=1,
            help="Number of shares purchased",
            key="quantity"
        )
        
        # Unit price input
        unit_price = st.number_input(
            "Unit Price (₹) *",
            min_value=0.01,
            value=100.00,
            step=0.01,
            format="%.2f",
            help="Purchase price per share",
            key="unit_price"
        )
        
        # Auto-calculated total investment
        total_investment = quantity * unit_price
        st.markdown(f"### Total Investment")
        st.markdown(f"<h2 style='color: blue;'>₹{total_investment:,.2f}</h2>", unsafe_allow_html=True)
        
        st.divider()
        
        # Form submit buttons
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            submit = st.form_submit_button(
                "Add", 
                type="secondary", 
                use_container_width=True
            )
        
        with col_btn2:
            reset = st.form_submit_button(
                "Reset", 
                type="secondary", 
                use_container_width=True
            )
        
        # FORM SUBMISSION HANDLING (Enhanced with validation)
        if submit:
            # Client-side validation
            if not selected_stock:
                st.error("❌ Please select a stock")
            elif quantity <= 0:
                st.error("❌ Quantity must be greater than 0")
            elif unit_price <= 0:
                st.error("❌ Unit price must be greater than 0")
            else:
                try:
                    # Extract stock symbol and name
                    stock_symbol, stock_name = stock_options[selected_stock]
                    
                    # Add to database using backend (includes server-side validation)
                    success, message = backend.add_transaction(
                        stock_symbol=stock_symbol,
                        stock_name=stock_name,
                        transaction_date=trans_date,
                        quantity=quantity,
                        unit_price=unit_price
                    )
                    
                    if success:
                        # IMPORTANT: Clear ALL caches before showing success
                        st.cache_data.clear()
                        
                        # Show success message
                        st.success(f"✅ {message}")
                        
                        # Update session state
                        st.session_state.form_submitted = True
                        
                        # Show balloons animation
                        st.balloons()
                        
                        # Wait for DB to fully commit and caches to clear
                        time.sleep(1)
                        
                        # Force complete page refresh
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")
    
    # ============================================
    # QUICK STATS SIDEBAR
    # ============================================
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    
    try:
        stats = list(get_cached_portfolio_summary())  # Convert from tuple
        if stats:
            total_holdings = len(stats)
            total_qty = sum([s['quantity'] for s in stats])
            
            st.metric("Holdings", total_holdings)
            st.metric("Total Shares", f"{total_qty:,}")
            
            # Show last transaction info
            recent_trans = list(get_cached_transactions())  # Convert from tuple
            if recent_trans:
                last_trans = recent_trans[0]
                st.markdown(f"""
                    **Last Transaction:**  
                    {last_trans['stock_symbol']} - {last_trans['quantity']} shares  
                    on {last_trans['transaction_date'].strftime('%d %b %Y')}
                """)
        else:
            st.info("No portfolio data yet")
    except Exception as e:
        st.warning("Unable to load quick stats")

# ================================================
# FOOTER
# ================================================
st.divider()
st.markdown("""
    <style>
    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #888888;
        margin-top: 1rem;
        padding-top: 1rem;
    }
    </style>
    <div class="footer">
        Developed by Ayan class XII for StockMarketApp project. | © 2025-26 
    </div>
""", unsafe_allow_html=True)
# ================================================
# DEBUG INFO (Uncomment for debugging)
# ================================================
# with st.expander("🔧 Debug Info"):
#     st.write("Session State:", st.session_state)
#     db_stats = backend.get_database_stats()
#     st.write("Database Stats:", db_stats)
#     st.write("Health Check:", check_db_health())
# End of Portfolio Page Code