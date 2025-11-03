# StockMarketApp - Technical Architecture Design

## Overview

A comprehensive Indian stock market analytics application built with Streamlit and Python, providing real-time market data, advanced technical analysis, portfolio management, and intelligent insights. The application demonstrates enterprise-level software development practices applied to financial technology, integrating multiple data sources with sophisticated analytical capabilities.

**Key Features:**
- Real-time market dashboard with live tickers and analytics
- Advanced charting system with technical indicators (RSI, Moving Averages)
- Portfolio management with P&L tracking and performance metrics
- Watchlist management with dynamic stock selection
- News integration with market updates and global coverage
- Interactive data visualization using Plotly charts

## Table of Contents

- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Architecture Layers](#architecture-layers)
- [Feature Implementation](#feature-implementation)
- [Performance Optimization](#performance-optimization)
- [Deployment Guide](#deployment-guide)
- [Development Workflow](#development-workflow)

## Technology Stack

### Core Framework
- **Streamlit 1.28+**: Modern web application framework for rapid development
- **MySQL 8.0+**: Primary database for historical and real-time stock data
- **SQLAlchemy 1.4+**: ORM for database operations and connection management
- **Python 3.9+**: Core programming language with type hints

### Data Sources & APIs
- **yfinance**: Primary Yahoo Finance API wrapper for Indian stock data
- **Alpha Vantage**: Secondary data source for technical indicators and news
- **NSE Tools**: Integration for NSE-specific data and indices
- **pandas 1.5+**: Advanced data manipulation and analysis
- **numpy 1.21+**: Numerical computations for technical indicators

### Visualization & UI
- **Plotly 5.15+**: Interactive charts with candlestick and technical overlays
- **plotly.graph_objects**: Advanced chart customization and real-time updates
- **Streamlit components**: Custom UI elements for enhanced user experience

### Performance & Optimization
- **Streamlit caching**: @st.cache_data for expensive operations
- **Database indexing**: Optimized queries with proper indexing strategy
- **Session state management**: Persistent user data across page interactions
- **Lazy loading**: On-demand data loading for improved performance

## Project Structure

```
StockMarketApp/
├── app.py                    # Main Streamlit application entry point
├── requirements.txt          # Python dependencies
├── readme.md                # Project overview and setup instructions
├── .gitignore               # Git ignore patterns
│
├── config/                  # Configuration management
│   ├── __init__.py
│   ├── database_config.py   # Database connection settings
│   ├── api_config.py        # API configurations and keys
│   └── settings.py          # Application-wide settings
│
├── data/                    # Data layer and processing
│   ├── __init__.py
│   ├── database.py          # MySQL integration with SQLAlchemy
│   ├── api_client.py        # External API integrations (Yahoo, Alpha Vantage)
│   ├── data_processor.py    # Technical analysis calculations
│   ├── data_fetch.py        # Data collection and validation
│   ├── portfolio_data_processor.py # Portfolio-specific calculations
│   ├── file_data_processor.py # File-based data processing
│   └── *.csv               # Static data files (symbols, indices)
│
├── pages/                   # Application pages and modules
│   ├── __init__.py
│   ├── dashboard.py         # Market overview and real-time analytics
│   ├── charts.py            # Advanced charting with technical indicators
│   ├── portfolio.py         # Portfolio management and P&L tracking
│   ├── watchlist.py         # Stock watchlist management
│   └── news.py              # Market news integration
│
├── utils/                   # Utility functions and helpers
│   ├── __init__.py
│   ├── calculations.py      # Financial calculations and metrics
│   ├── charts.py            # Chart generation utilities
│   ├── helpers.py           # Common helper functions
│   └── constants.py         # Application constants
│
├── assets/                  # Static assets and styling
│   ├── css/
│   │   └── custom.css       # Custom CSS styling
│   └── images/
│       ├── stock_market_image.jpg
│       └── stock_market_2.jpg
│
├── scripts/                 # Database and deployment scripts
│   ├── backup_restore.py    # Database backup utilities
│   ├── data_migration.py    # Data migration scripts
│   ├── db_setup.sql         # Database schema setup
│   ├── initial_setup.py     # Initial application setup
│   ├── portfolio_tables.sql # Portfolio-specific tables
│   └── seed_data.sql        # Sample data insertion
│
└── doc/                     # Comprehensive documentation
    ├── StockMarketApp_Project_Report.md # Main project report
    ├── architecture.md      # Technical architecture guide
    ├── api_documentation.md # API integration documentation
    ├── functional_modules.md # Module specifications
    ├── deployment_guide.md  # Deployment instructions
    ├── srs_document.md      # System requirements specification
    ├── brd.md              # Business requirements document
    ├── project_plan.md     # Development project plan
    └── *.mermaid           # Architecture diagrams
```

## Database Schema

### Core Tables for Indian Stock Market Data

#### indian_stocks (Master Stock Information)
```sql
CREATE TABLE indian_stocks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    market_cap DECIMAL(15,2),
    exchange ENUM('NSE', 'BSE') DEFAULT 'NSE',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_symbol (symbol),
    INDEX idx_sector (sector),
    INDEX idx_exchange (exchange)
);
```

#### daily_stock_data (Historical OHLCV Data)
```sql
CREATE TABLE daily_stock_data (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    stock_id INT NOT NULL,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10,2) NOT NULL,
    high_price DECIMAL(10,2) NOT NULL,
    low_price DECIMAL(10,2) NOT NULL,
    close_price DECIMAL(10,2) NOT NULL,
    volume BIGINT NOT NULL,
    turnover DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (stock_id) REFERENCES indian_stocks(id) ON DELETE CASCADE,
    UNIQUE KEY unique_stock_date (stock_id, trade_date),
    INDEX idx_trade_date (trade_date),
    INDEX idx_stock_date (stock_id, trade_date)
);
```

#### portfolio_transactions (Portfolio Management)
```sql
CREATE TABLE portfolio_transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    stock_symbol VARCHAR(20) NOT NULL,
    transaction_type ENUM('BUY', 'SELL') NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    transaction_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_stock_symbol (stock_symbol),
    INDEX idx_transaction_date (transaction_date)
);
```

#### nifty_indexes_data (Market Indices)
```sql
CREATE TABLE nifty_indexes_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    index_name VARCHAR(50) NOT NULL,
    index_value DECIMAL(10,2) NOT NULL,
    change_points DECIMAL(10,2),
    change_percent DECIMAL(5,2),
    pe_ratio DECIMAL(8,2),
    pb_ratio DECIMAL(8,2),
    date_recorded DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_index_date (index_name, date_recorded),
    INDEX idx_date_recorded (date_recorded)
);
```

#### nifty50_stock_quotes_data (Real-time Stock Quotes)
```sql
CREATE TABLE nifty50_stock_quotes_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    symbol VARCHAR(20) NOT NULL,
    company_name VARCHAR(255),
    current_price DECIMAL(10,2),
    change_points DECIMAL(10,2),
    change_percent DECIMAL(5,2),
    volume BIGINT,
    market_cap DECIMAL(15,2),
    pe_ratio DECIMAL(8,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_symbol (symbol),
    INDEX idx_last_updated (last_updated)
);
```

#### bank_nifty_data (Bulk Trading Data)
```sql
CREATE TABLE bank_nifty_data (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    symbol VARCHAR(20) NOT NULL,
    series VARCHAR(10),
    trade_date DATE NOT NULL,
    prev_close DECIMAL(10,2),
    open_price DECIMAL(10,2),
    high_price DECIMAL(10,2),
    low_price DECIMAL(10,2),
    last_price DECIMAL(10,2),
    close_price DECIMAL(10,2),
    avg_price DECIMAL(10,2),
    ttl_trd_qnty BIGINT,
    turnover_lacs DECIMAL(15,2),
    no_of_trades INT,
    deliv_qty BIGINT,
    deliv_per DECIMAL(5,2),
    
    INDEX idx_symbol_date (symbol, trade_date),
    INDEX idx_trade_date (trade_date)
);
```

## Architecture Layers

### 1. Data Layer (`data/`)

#### database.py
```python
"""
Database connection and ORM models
- SQLAlchemy engine configuration
- Database session management
- Table models definition
- Connection pooling setup
- Migration utilities
"""

Key Components:
- DatabaseManager class
- SQLAlchemy models for all tables
- Connection pool configuration
- Transaction management
- Error handling and logging
```

#### api_client.py
```python
"""
External API integration layer
- Multiple API provider support
- Rate limiting and retry logic
- Data validation and cleaning
- Caching mechanisms
- Error handling
"""

Key Features:
- APIClient base class
- YahooFinanceClient implementation
- AlphaVantageClient implementation
- Rate limiting decorator
- Response validation
- Failover mechanisms
```

#### data_processor.py
```python
"""
Data processing and calculation engine
- Technical indicator calculations
- Market analytics computations
- Data aggregation functions
- Performance metrics calculation
"""

Key Functions:
- calculate_technical_indicators()
- identify_gainers_losers()
- compute_market_statistics()
- aggregate_timeframe_data()
- calculate_portfolio_metrics()
```

### 2. User Interface Layer

#### Main Application (app.py)
```python
"""
Main Streamlit application entry point
- Page configuration and routing
- Navigation menu setup
- Session state initialization
- Global styling application
"""

Key Features:
- Multi-page navigation
- Session state management
- Custom CSS loading
- Authentication (if needed)
- Global error handling
```

#### Page Components (`pages/`)

**dashboard.py**
- Market overview widgets
- Real-time index values
- Top gainers/losers tables
- Market heat map
- Quick watchlist access

**analytics.py**
- Historical performance analysis
- Sector-wise comparisons
- Volume analysis charts
- Custom date range reports
- Export functionality

**watchlist.py**
- Watchlist creation/management
- Real-time price monitoring
- Performance tracking
- Alert configuration
- Bulk operations

**charts.py**
- Interactive candlestick charts
- Technical indicator overlays
- Volume analysis
- Multi-timeframe views
- Chart pattern recognition

**news.py**
- Stock-specific news feed
- Market news aggregation
- Sentiment analysis display
- News filtering options

### 3. Utility Layer (`utils/`)

#### charts.py
```python
"""
Chart generation and visualization utilities
- Plotly chart configurations
- Technical indicator overlays
- Custom styling functions
- Interactive features
"""

Key Functions:
- create_candlestick_chart()
- add_technical_indicators()
- create_volume_chart()
- generate_heatmap()
- create_comparison_chart()
```

#### calculations.py
```python
"""
Technical analysis and financial calculations
- Moving averages (SMA, EMA)
- Momentum indicators (RSI, MACD)
- Volatility measures
- Support/resistance levels
"""

Key Functions:
- calculate_sma()
- calculate_ema()
- calculate_rsi()
- calculate_macd()
- calculate_bollinger_bands()
```

## Feature Implementation

### 1. Real-time Data Updates

```python
# Auto-refresh mechanism
@st.fragment(run_every=300)  # 5-minute refresh
def update_market_data():
    with st.spinner("Updating market data..."):
        # Fetch latest data
        return updated_data

# Manual refresh button
if st.button("🔄 Refresh Data", key="refresh_btn"):
    st.rerun()
```

### 2. Interactive Charting

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_advanced_chart(df, indicators=None):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=('Price', 'Volume'),
        row_width=[0.2, 0.7]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name="Price"
        ),
        row=1, col=1
    )
    
    # Volume bars
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['volume'],
            name="Volume",
            marker_color='rgba(158,202,225,0.8)'
        ),
        row=2, col=1
    )
    
    # Add technical indicators
    if indicators:
        for indicator in indicators:
            add_technical_indicator(fig, df, indicator)
    
    return fig
```

### 3. Caching Strategy

```python
# Data caching
@st.cache_data(ttl=300, max_entries=1000)
def get_stock_data(symbol: str, period: str) -> pd.DataFrame:
    """Cache stock data for 5 minutes"""
    return fetch_stock_data(symbol, period)

# Resource caching
@st.cache_resource
def init_database():
    """Cache database connection"""
    return DatabaseManager()

# Custom cache key
@st.cache_data(ttl=60)
def get_market_summary(_date: datetime.date) -> dict:
    """Cache market summary data"""
    return calculate_market_summary(_date)
```

### 4. Session State Management

```python
# Initialize session state
def init_session_state():
    if 'watchlists' not in st.session_state:
        st.session_state.watchlists = load_default_watchlists()
    
    if 'selected_stocks' not in st.session_state:
        st.session_state.selected_stocks = []
    
    if 'chart_settings' not in st.session_state:
        st.session_state.chart_settings = {
            'timeframe': '1D',
            'indicators': ['SMA_20'],
            'chart_type': 'candlestick'
        }

# Update session state
def update_watchlist(action: str, stock_symbol: str, watchlist_name: str):
    if action == 'add':
        st.session_state.watchlists[watchlist_name].append(stock_symbol)
    elif action == 'remove':
        st.session_state.watchlists[watchlist_name].remove(stock_symbol)
```

## Performance Optimization

### 1. Database Optimization

**Indexing Strategy:**
```sql
-- Composite indexes for common queries
CREATE INDEX idx_stock_date_range ON stock_prices(stock_id, date);
CREATE INDEX idx_volume_analysis ON stock_prices(date, volume);
CREATE INDEX idx_price_range ON stock_prices(date, close_price);

-- Partitioning for large tables
ALTER TABLE stock_prices PARTITION BY RANGE (YEAR(date)) (
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

**Query Optimization:**
```python
# Efficient bulk operations
def bulk_insert_prices(price_data: List[dict]):
    """Bulk insert stock prices using SQLAlchemy Core"""
    stmt = insert(StockPrice)
    connection.execute(stmt, price_data)

# Optimized queries with proper joins
def get_watchlist_performance(watchlist_id: int) -> pd.DataFrame:
    query = """
    SELECT s.symbol, s.company_name,
           sp.close_price, sp.volume,
           LAG(sp.close_price) OVER (
               PARTITION BY s.id ORDER BY sp.date
           ) as prev_close
    FROM watchlist_stocks ws
    JOIN stocks s ON ws.stock_id = s.id
    JOIN stock_prices sp ON s.id = sp.stock_id
    WHERE ws.watchlist_id = %s
    AND sp.date = CURDATE()
    """
    return pd.read_sql(query, connection, params=[watchlist_id])
```

### 2. Caching Strategy

**Multi-level Caching:**
```python
# Level 1: Streamlit built-in caching
@st.cache_data(ttl=300)
def get_realtime_data(symbols: List[str]):
    return api_client.fetch_multiple_stocks(symbols)

# Level 2: Redis caching (optional)
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_data(key: str, fetch_func, ttl: int = 300):
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    
    data = fetch_func()
    redis_client.setex(key, ttl, json.dumps(data))
    return data

# Level 3: Database-level caching
def get_technical_indicators_cached(stock_id: int, date: datetime.date):
    # Check if indicators exist in database
    existing = session.query(TechnicalIndicator).filter_by(
        stock_id=stock_id, date=date
    ).first()
    
    if existing:
        return existing
    
    # Calculate and store if not exists
    indicators = calculate_indicators(stock_id, date)
    session.add(TechnicalIndicator(**indicators))
    session.commit()
    return indicators
```

### 3. Data Loading Optimization

```python
# Lazy loading for large datasets
@st.cache_data
def load_historical_data(symbol: str, start_date: datetime.date, end_date: datetime.date):
    """Load data in chunks to avoid memory issues"""
    chunks = []
    current_date = start_date
    chunk_size = timedelta(days=90)  # 3-month chunks
    
    while current_date < end_date:
        chunk_end = min(current_date + chunk_size, end_date)
        chunk_data = fetch_data_chunk(symbol, current_date, chunk_end)
        chunks.append(chunk_data)
        current_date = chunk_end + timedelta(days=1)
    
    return pd.concat(chunks, ignore_index=True)

# Pagination for large result sets
def get_paginated_stocks(page: int = 1, per_page: int = 50, filters: dict = None):
    query = session.query(Stock)
    
    if filters:
        if 'sector' in filters:
            query = query.filter(Stock.sector == filters['sector'])
        if 'min_market_cap' in filters:
            query = query.filter(Stock.market_cap >= filters['min_market_cap'])
    
    total = query.count()
    stocks = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        'stocks': stocks,
        'total': total,
        'pages': math.ceil(total / per_page),
        'current_page': page
    }
```

## Deployment Guide

### 1. Environment Setup

**.env Configuration:**
```bash
# Database Configuration
DATABASE_URL=mysql://username:password@localhost:3306/stock_market_db
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# API Keys
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
FINNHUB_API_KEY=your_finnhub_key
NEWS_API_KEY=your_news_api_key

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
CACHE_TTL=300
MAX_WATCHLIST_STOCKS=50

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1

# External Services
REDIS_URL=redis://localhost:6379/0
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 2. Docker Configuration

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Start application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: stock_market_db
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppassword
    volumes:
      - mysql_data:/var/lib/mysql
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    
  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    
  app:
    build: .
    ports:
      - "8501:8501"
    depends_on:
      - mysql
      - redis
    environment:
      - DATABASE_URL=mysql://appuser:apppassword@mysql:3306/stock_market_db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./logs:/app/logs

volumes:
  mysql_data:
```

### 3. Background Jobs

**Data Update Scheduler:**
```python
# scripts/data_updater.py
import schedule
import time
from datetime import datetime
from data.api_client import APIClient
from data.database import DatabaseManager

def update_stock_prices():
    """Update stock prices for all active stocks"""
    print(f"Starting price update at {datetime.now()}")
    
    api_client = APIClient()
    db_manager = DatabaseManager()
    
    active_stocks = db_manager.get_active_stocks()
    
    for stock in active_stocks:
        try:
            latest_data = api_client.fetch_latest_price(stock.symbol)
            db_manager.update_stock_price(stock.id, latest_data)
            print(f"Updated {stock.symbol}")
        except Exception as e:
            print(f"Error updating {stock.symbol}: {e}")
    
    print("Price update completed")

def update_technical_indicators():
    """Calculate and update technical indicators"""
    print("Updating technical indicators...")
    # Implementation here

# Schedule jobs
schedule.every(15).minutes.do(update_stock_prices)
schedule.every(1).hours.do(update_technical_indicators)
schedule.every().day.at("09:00").do(lambda: print("Market opening soon!"))

if __name__ == "__main__":
    print("Starting background job scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(1)
```

### 4. Monitoring and Logging

**logging_config.py:**
```python
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(log_level="INFO"):
    """Setup application logging"""
    
    # Create logger
    logger = logging.getLogger("stock_market_app")
    logger.setLevel(getattr(logging, log_level))
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
```

## Development Workflow

### 1. Setup Instructions

```bash
# Clone repository
git clone https://github.com/your-username/stock-market-app.git
cd stock-market-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration

# Setup database
python scripts/initial_setup.py

# Run application
streamlit run app.py
```

### 2. Testing Strategy

```python
# tests/test_api_client.py
import pytest
from unittest.mock import Mock, patch
from data.api_client import YahooFinanceClient

class TestAPIClient:
    def setup_method(self):
        self.client = YahooFinanceClient()
    
    @patch('yfinance.download')
    def test_fetch_stock_data(self, mock_download):
        # Mock API response
        mock_download.return_value = Mock()
        
        result = self.client.fetch_stock_data('RELIANCE.NS', '1y')
        
        assert result is not None
        mock_download.assert_called_once()

# tests/test_calculations.py
import pandas as pd
from utils.calculations import calculate_sma, calculate_rsi

class TestCalculations:
    def test_sma_calculation(self):
        data = pd.Series([100, 102, 101, 103, 105, 104, 106])
        sma = calculate_sma(data, period=3)
        
        expected = pd.Series([None, None, 101, 102, 103, 104, 105])
        pd.testing.assert_series_equal(sma, expected, check_names=False)
```

### 3. Code Quality

**pre-commit-config.yaml:**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3
        
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        args: [--max-line-length=88]
        
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        args: [--profile=black]
```

### 4. CI/CD Pipeline

**.github/workflows/main.yml:**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: testpass
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306
        options: >-
          --health-cmd="mysqladmin ping"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=3
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=./ --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## Contributing Guidelines

### Code Standards
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write comprehensive docstrings for all functions and classes
- Maintain test coverage above 80%

### Commit Message Format
```
type(scope): description

body (optional)

footer (optional)
```

Types: feat, fix, docs, style, refactor, test, chore

### Pull Request Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE.md) file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the [documentation](./functional_modules.md)
- Contact the development team

---

**Note:** This architecture is designed to be scalable and maintainable. Regular updates and optimizations should be made based on usage patterns and performance metrics.
