# Indian Stock Market App - Deployment Guide

This comprehensive guide covers all aspects of deploying the Stock Market App in various environments, from local development to production-ready cloud deployments.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Local Development Deployment](#local-development-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment Options](#cloud-deployment-options)
- [Database Setup](#database-setup)
- [Monitoring & Logging](#monitoring--logging)
- [Security Configuration](#security-configuration)
- [Performance Optimization](#performance-optimization)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements

| Component | Minimum | Recommended | Purpose |
|-----------|---------|-------------|---------|
| **CPU** | 2 cores | 4+ cores | Application processing |
| **RAM** | 4 GB | 8+ GB | Data processing & caching |
| **Storage** | 50 GB | 100+ GB | Database & logs |
| **Network** | 100 Mbps | 1 Gbps | API calls & data feeds |

### Software Dependencies

| Software | Version | Installation Command | Purpose |
|----------|---------|---------------------|---------|
| **Python** | 3.9+ | `sudo apt install python3.9` | Runtime environment |
| **MySQL** | 8.0+ | `sudo apt install mysql-server` | Database server |
| **Redis** | 6.0+ | `sudo apt install redis-server` | Caching (optional) |
| **Git** | Latest | `sudo apt install git` | Version control |
| **Docker** | 20.0+ | `curl -fsSL https://get.docker.com | sh` | Containerization |
| **Nginx** | Latest | `sudo apt install nginx` | Reverse proxy |

### Indian Stock Market App's API Requirements

The application requires access to **free Indian stock market APIs**:

| API Service | Purpose | Rate Limits | Features |
|-------------|---------|-------------|----------|
| **Alpha Vantage** | NSE/BSE data | 5 calls/minute (free) | Real-time prices, historical data |
| **Yahoo Finance API** | Indian equities | No strict limits | Price data, volume, dividends |
| **BSE/NSE Official APIs** | Direct exchange data | Varies | Official market data |
| **Polygon.io** | Indian markets | 5 calls/minute (free) | Comprehensive market data |

## 🌐 Environment Setup

### Environment Variables Configuration

#### `.env.development`
```bash
# Application Configuration
APP_NAME=Indian Stock Market Analytics
APP_VERSION=1.0.0
DEBUG=True
LOG_LEVEL=DEBUG
SECRET_KEY=development-secret-key-change-in-production
MARKET_TYPE=INDIAN
TIMEZONE=Asia/Kolkata

# Database Configuration
DATABASE_URL=mysql://stockapp:stockpass@localhost:3306/indian_stockmarket_dev
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Indian Stock Market API Keys
ALPHA_VANTAGE_API_KEY=your_dev_alpha_vantage_key
YAHOO_FINANCE_ENABLED=True
BSE_API_KEY=your_bse_api_key
NSE_API_KEY=your_nse_api_key
POLYGON_API_KEY=your_polygon_api_key

# News API Configuration
NEWS_API_KEY=your_dev_news_api_key
BUSINESS_NEWS_SOURCES=economic-times,moneycontrol,business-standard

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=300
CACHE_ENABLED=True

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=False

# Indian Market Specific Settings
MARKET_HOURS_START=09:15
MARKET_HOURS_END=15:30
MARKET_DAYS=MON,TUE,WED,THU,FRI
ENABLE_MARKET_HOURS_ONLY=True
DEFAULT_EXCHANGE=NSE

# Data Collection Settings
DATA_UPDATE_INTERVAL=300  # 5 minutes
HISTORICAL_DATA_YEARS=5
ENABLE_REALTIME_DATA=True
ENABLE_TECHNICAL_INDICATORS=True

# Watchlist & Analytics
MAX_WATCHLIST_STOCKS=50
ENABLE_PORTFOLIO_TRACKING=True
ENABLE_ALERTS=True

# Chart Configuration
CHART_LIBRARY=plotly
ENABLE_CANDLESTICK_CHARTS=True
ENABLE_VOLUME_CHARTS=True
DEFAULT_CHART_PERIOD=1Y
```

#### `.env.production`
```bash
# Application Configuration
APP_NAME=Indian Stock Market Analytics
APP_VERSION=1.0.0
DEBUG=False
LOG_LEVEL=INFO
SECRET_KEY=your-super-secure-production-secret-key
MARKET_TYPE=INDIAN
TIMEZONE=Asia/Kolkata

# Database Configuration
DATABASE_URL=mysql://produser:securepassword@prod-db-server:3306/indian_stockmarket_prod
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_TIMEOUT=60
DB_POOL_RECYCLE=1800

# Indian Stock Market API Keys (Production)
ALPHA_VANTAGE_API_KEY=your_prod_alpha_vantage_key
YAHOO_FINANCE_ENABLED=True
BSE_API_KEY=your_prod_bse_api_key
NSE_API_KEY=your_prod_nse_api_key
POLYGON_API_KEY=your_prod_polygon_api_key

# News API Configuration
NEWS_API_KEY=your_prod_news_api_key
BUSINESS_NEWS_SOURCES=economic-times,moneycontrol,business-standard,livemint

# Redis Configuration
REDIS_URL=redis://prod-redis-server:6379/0
CACHE_TTL=300
CACHE_ENABLED=True

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=False
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200

# Security
ALLOWED_ORIGINS=https://yourdomain.com
CORS_ENABLED=False
HTTPS_ONLY=True

# Performance
ENABLE_GZIP=True
STATIC_FILE_CACHING=True
DATABASE_CONNECTION_POOL_SIZE=50

# Indian Market Production Settings
MARKET_HOURS_START=09:15
MARKET_HOURS_END=15:30
MARKET_DAYS=MON,TUE,WED,THU,FRI
ENABLE_MARKET_HOURS_ONLY=True
DEFAULT_EXCHANGE=NSE
```

### Indian Stock Market Configuration

```python
# config/indian_market_settings.py
import os
from typing import Dict, List
from datetime import time
from enum import Enum

class IndianExchange(Enum):
    NSE = "NSE"
    BSE = "BSE"
    MCX = "MCX"  # Multi Commodity Exchange

class MarketConfig:
    """Configuration for Indian stock market specifics."""
    
    # Market timing (IST)
    MARKET_OPEN = time(9, 15)  # 9:15 AM
    MARKET_CLOSE = time(15, 30)  # 3:30 PM
    PRE_MARKET_OPEN = time(9, 0)  # 9:00 AM
    POST_MARKET_CLOSE = time(16, 0)  # 4:00 PM
    
    # Trading days (Monday to Friday)
    TRADING_DAYS = [0, 1, 2, 3, 4]  # 0=Monday, 6=Sunday
    
    # Major Indian indices
    MAJOR_INDICES = {
        "NIFTY50": "^NSEI",
        "SENSEX": "^BSESN",
        "NIFTY_BANK": "^NSEBANK",
        "NIFTY_IT": "^CNXIT",
        "NIFTY_PHARMA": "^CNXPHARMA",
        "NIFTY_AUTO": "^CNXAUTO",
        "NIFTY_FMCG": "^CNXFMCG",
        "NIFTY_METAL": "^CNXMETAL"
    }
    
    # Popular Indian stocks (NSE symbols)
    POPULAR_STOCKS = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HINDUNILVR.NS",
        "ICICIBANK.NS", "HDFCBANK.NS", "ITC.NS", "BHARTIARTL.NS",
        "SBIN.NS", "LT.NS", "ASIANPAINT.NS", "MARUTI.NS",
        "HCLTECH.NS", "AXISBANK.NS", "KOTAKBANK.NS", "WIPRO.NS",
        "ULTRACEMCO.NS", "BAJFINANCE.NS", "NESTLEIND.NS", "POWERGRID.NS"
    ]
    
    # Stock categories for analysis
    STOCK_CATEGORIES = {
        "Large Cap": ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HINDUNILVR.NS"],
        "Mid Cap": ["MCDOWELL-N.NS", "PAGEIND.NS", "PIDILITIND.NS"],
        "Small Cap": ["DIXON.NS", "ROUTE.NS", "ASTRAL.NS"],
        "Banking": ["ICICIBANK.NS", "HDFCBANK.NS", "SBIN.NS", "AXISBANK.NS"],
        "IT": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS"],
        "Pharma": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS"]
    }
    
    # Currency and formatting
    CURRENCY = "INR"
    CURRENCY_SYMBOL = "₹"
    NUMBER_FORMAT = "indian"  # Uses lakhs/crores
    
    @staticmethod
    def format_indian_currency(amount: float) -> str:
        """Format amount in Indian currency with lakhs/crores."""
        if amount >= 10000000:  # 1 crore
            return f"₹{amount/10000000:.2f} Cr"
        elif amount >= 100000:  # 1 lakh
            return f"₹{amount/100000:.2f} L"
        else:
            return f"₹{amount:,.2f}"
```

## 🏠 Local Development Deployment

### Quick Start Setup for Indian Stock Market

```bash
#!/bin/bash
# setup-indian-stock-app.sh

echo "Setting up Indian Stock Market Analytics Platform - Development Environment"

# 1. Clone repository
git clone https://github.com/your-username/indian-stock-market-app.git
cd indian-stock-market-app

# 2. Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Install Indian market specific packages
pip install yfinance nsepy yahooquery polygon-api-client

# 5. Setup environment variables
cp .env.example .env.development
echo "Please update .env.development with your Indian stock market API keys"

# 6. Setup database with Indian stock schema
sudo systemctl start mysql
mysql -u root -p  /etc/timezone

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create application directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/cache && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Expose port
EXPOSE 8501

# Start command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose for Indian Stock Application

#### `docker-compose.yml` (Development)

```yaml
version: '3.8'

services:
  # MySQL Database for Indian Stocks
  mysql:
    image: mysql:8.0
    container_name: indian-stockapp-mysql-dev
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: indian_stockmarket_dev
      MYSQL_USER: stockapp
      MYSQL_PASSWORD: stockpass
      TZ: Asia/Kolkata
    volumes:
      - mysql_data_dev:/var/lib/mysql
      - ./scripts/sql/indian_stock_schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
      - ./scripts/sql/indian_stock_universe.sql:/docker-entrypoint-initdb.d/02-universe.sql
      - ./config/mysql/dev.cnf:/etc/mysql/conf.d/custom.cnf
    ports:
      - "3306:3306"
    networks:
      - indian-stockapp-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache for market data
  redis:
    image: redis:6-alpine
    container_name: indian-stockapp-redis-dev
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data_dev:/data
    ports:
      - "6379:6379"
    networks:
      - indian-stockapp-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Main Indian Stock Application
  app:
    build: 
      context: .
      dockerfile: Dockerfile
      target: production
    container_name: indian-stockapp-main-dev
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=mysql://stockapp:stockpass@mysql:3306/indian_stockmarket_dev
      - REDIS_URL=redis://redis:6379/0
      - TZ=Asia/Kolkata
      - MARKET_TYPE=INDIAN
    env_file:
      - .env.development
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      - .:/app  # Mount source code for development
    ports:
      - "8501:8501"
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - indian-stockapp-network
    restart: unless-stopped

  # Background Job Worker for data collection
  worker:
    build: 
      context: .
      dockerfile: Dockerfile
      target: production
    container_name: indian-stockapp-worker-dev
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=mysql://stockapp:stockpass@mysql:3306/indian_stockmarket_dev
      - REDIS_URL=redis://redis:6379/0
      - TZ=Asia/Kolkata
      - MARKET_TYPE=INDIAN
    env_file:
      - .env.development
    volumes:
      - ./logs:/app/logs
    command: python scripts/indian_market_data_worker.py
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - indian-stockapp-network
    restart: unless-stopped

  # News aggregator service
  news-worker:
    build: 
      context: .
      dockerfile: Dockerfile
      target: production
    container_name: indian-stockapp-news-dev
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=mysql://stockapp:stockpass@mysql:3306/indian_stockmarket_dev
      - REDIS_URL=redis://redis:6379/0
      - TZ=Asia/Kolkata
    env_file:
      - .env.development
    volumes:
      - ./logs:/app/logs
    command: python scripts/indian_news_worker.py
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - indian-stockapp-network
    restart: unless-stopped

volumes:
  mysql_data_dev:
  redis_data_dev:

networks:
  indian-stockapp-network:
    driver: bridge
```

## 📊 Indian Market Specific Features Configuration

### Data Collection Scripts

```python
# scripts/indian_market_data_worker.py
import asyncio
import yfinance as yf
from nsepy import get_history
from datetime import datetime, timedelta
import logging
from typing import List, Dict
import mysql.connector
from config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class IndianMarketDataCollector:
    """Collects data for Indian stock markets."""
    
    def __init__(self):
        self.db_config = {
            'host': settings.database_url.split('@')[1].split(':')[0],
            'user': settings.database_url.split('://')[1].split(':')[0],
            'password': settings.database_url.split(':')[2].split('@')[0],
            'database': settings.database_url.split('/')[-1],
            'charset': 'utf8mb4'
        }
    
    async def collect_nifty_stocks_data(self):
        """Collect data for NIFTY 50 stocks."""
        nifty_50_symbols = [
            "RELIANCE.NS", "TCS.NS", "INFY.NS", "HINDUNILVR.NS",
            "ICICIBANK.NS", "HDFCBANK.NS", "ITC.NS", "BHARTIARTL.NS",
            "SBIN.NS", "LT.NS", "ASIANPAINT.NS", "MARUTI.NS",
            # Add all 50 symbols
        ]
        
        for symbol in nifty_50_symbols:
            try:
                await self.collect_stock_data(symbol)
                await asyncio.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error collecting data for {symbol}: {e}")
    
    async def collect_stock_data(self, symbol: str):
        """Collect comprehensive stock data."""
        try:
            # Get stock info
            stock = yf.Ticker(symbol)
            
            # Get historical data
            hist = stock.history(period="1y")
            
            # Get current data
            info = stock.info
            
            # Store in database
            await self.store_stock_data(symbol, hist, info)
            
        except Exception as e:
            logger.error(f"Error collecting data for {symbol}: {e}")
    
    async def store_stock_data(self, symbol: str, hist_data, stock_info):
        """Store stock data in MySQL database."""
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()
        
        try:
            # Insert daily data
            for date, row in hist_data.iterrows():
                query = """
                INSERT INTO daily_stock_data 
                (stock_id, trade_date, open_price, high_price, low_price, close_price, volume)
                VALUES ((SELECT id FROM indian_stocks WHERE symbol = %s), %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                open_price = VALUES(open_price),
                high_price = VALUES(high_price),
                low_price = VALUES(low_price),
                close_price = VALUES(close_price),
                volume = VALUES(volume)
                """
                
                cursor.execute(query, (
                    symbol,
                    date.date(),
                    float(row['Open']),
                    float(row['High']),
                    float(row['Low']),
                    float(row['Close']),
                    int(row['Volume'])
                ))
            
            connection.commit()
            logger.info(f"Successfully stored data for {symbol}")
            
        except Exception as e:
            connection.rollback()
            logger.error(f"Error storing data for {symbol}: {e}")
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    collector = IndianMarketDataCollector()
    asyncio.run(collector.collect_nifty_stocks_data())
```

### Analytics & Reporting Features

```python
# scripts/indian_market_analytics.py
import pandas as pd
import mysql.connector
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import numpy as np

class IndianMarketAnalytics:
    """Analytics engine for Indian stock market data."""
    
    def __init__(self, db_config: Dict):
        self.db_config = db_config
    
    def get_top_gainers_losers(self, period: str = 'daily') -> Dict:
        """Get top 5 gainers and losers for specified period."""
        connection = mysql.connector.connect(**self.db_config)
        
        if period == 'daily':
            query = """
            SELECT 
                s.symbol,
                s.company_name,
                d1.close_price as current_price,
                d2.close_price as previous_price,
                ((d1.close_price - d2.close_price) / d2.close_price * 100) as change_percent,
                d1.volume
            FROM indian_stocks s
            JOIN daily_stock_data d1 ON s.id = d1.stock_id
            JOIN daily_stock_data d2 ON s.id = d2.stock_id
            WHERE d1.trade_date = (SELECT MAX(trade_date) FROM daily_stock_data)
            AND d2.trade_date = (SELECT MAX(trade_date) FROM daily_stock_data WHERE trade_date = DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            AND d2.trade_date = DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            AND s.is_active = TRUE
            GROUP BY s.id, s.symbol, s.company_name, d1.close_price, d2.close_price
            ORDER BY change_percent DESC
            """
        
        df = pd.read_sql(query, connection)
        connection.close()
        
        return {
            'top_gainers': df.head(5).to_dict('records'),
            'top_losers': df.tail(5).to_dict('records')
        }
    
    def get_watchlist_performance(self, user_id: str) -> List[Dict]:
        """Get performance of user's watchlist stocks."""
        connection = mysql.connector.connect(**self.db_config)
        
        query = """
        SELECT 
            w.watchlist_name,
            s.symbol,
            s.company_name,
            d.close_price,
            d.volume,
            w.target_price,
            w.stop_loss,
            w.notes,
            CASE 
                WHEN d.close_price >= w.target_price THEN 'Target Reached'
                WHEN d.close_price  Dict:
        """Calculate technical indicators for a stock."""
        connection = mysql.connector.connect(**self.db_config)
        
        query = """
        SELECT trade_date, close_price, volume
        FROM daily_stock_data d
        JOIN indian_stocks s ON d.stock_id = s.id
        WHERE s.symbol = %s
        ORDER BY trade_date DESC
        LIMIT %s
        """
        
        df = pd.read_sql(query, connection, params=[symbol, period])
        connection.close()
        
        if len(df)  pd.Series:
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta  Tuple[pd.Series, pd.Series]:
        """Calculate Bollinger Bands."""
        sma = prices.rolling(window=period).mean()
        std_dev = prices.rolling(window=period).std()
        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)
        return upper_band, lower_band
```

## 🔐 Security Configuration

### Indian Market API Security

```python
# config/api_security.py
import os
import hashlib
from cryptography.fernet import Fernet
from typing import Dict

class APIKeyManager:
    """Secure management of Indian stock market API keys."""
    
    def __init__(self):
        self.encryption_key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
        self.cipher_suite = Fernet(self.encryption_key)
        
    def encrypt_api_key(self, api_key: str) -> str:
        """Encrypt API key for secure storage."""
        return self.cipher_suite.encrypt(api_key.encode()).decode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt API key for use."""
        return self.cipher_suite.decrypt(encrypted_key.encode()).decode()
    
    def validate_api_key_format(self, api_key: str, provider: str) -> bool:
        """Validate API key format for different providers."""
        validators = {
            'alpha_vantage': lambda key: len(key) == 16 and key.isalnum(),
            'polygon': lambda key: len(key) == 32 and key.isalnum(),
            'yahoo': lambda key: True,  # Yahoo doesn't require API key
        }
        
        return validators.get(provider, lambda x: False)(api_key)

# Rate limiting for API calls
class RateLimiter:
    """Rate limiting for Indian stock market APIs."""
    
    def __init__(self):
        self.call_history = {}
        self.limits = {
            'alpha_vantage': {'calls': 5, 'period': 60},  # 5 calls per minute
            'polygon': {'calls': 5, 'period': 60},        # 5 calls per minute
            'yahoo': {'calls': 100, 'period': 60},        # 100 calls per minute
        }
    
    def can_make_call(self, provider: str) -> bool:
        """Check if API call is allowed based on rate limits."""
        import time
        
        current_time = time.time()
        limit = self.limits.get(provider, {'calls': 1, 'period': 60})
        
        if provider not in self.call_history:
            self.call_history[provider] = []
        
        # Remove old calls outside the time window
        self.call_history[provider] = [
            call_time for call_time in self.call_history[provider]
            if current_time - call_time 
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #ff6b35;
        }
        .indian-flag-colors {
            background: linear-gradient(to right, #ff9933 33%, #ffffff 33%, #ffffff 66%, #138808 66%);
            height: 5px;
            margin-bottom: 1rem;
        }
        .market-status-open {
            color: #00ff00;
            font-weight: bold;
        }
        .market-status-closed {
            color: #ff0000;
            font-weight: bold;
        }
        .stock-price-up {
            color: #00ff00;
        }
        .stock-price-down {
            color: #ff0000;
        }
        
    """, unsafe_allow_html=True)
    
    # Indian flag header
    st.markdown('', unsafe_allow_html=True)
    st.title("🇮🇳 Indian Stock Market Analytics Platform")

def create_candlestick_chart(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Create candlestick chart for Indian stocks."""
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f'{symbol} - Price & Volume', 'Volume'),
        row_width=[0.2, 0.7]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['trade_date'],
            open=df['open_price'],
            high=df['high_price'],
            low=df['low_price'],
            close=df['close_price'],
            name="Price"
        ),
        row=1, col=1
    )
    
    # Volume chart
    fig.add_trace(
        go.Bar(
            x=df['trade_date'],
            y=df['volume'],
            name="Volume",
            marker_color='rgba(55, 126, 184, 0.6)'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f"{symbol} - Candlestick Chart with Volume",
        yaxis_title="Price (₹)",
        xaxis_rangeslider_visible=False,
        height=600,
        showlegend=False
    )
    
    return fig

def display_market_status():
    """Display current Indian market status."""
    from datetime import datetime
    import pytz
    
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    market_open = current_time.replace(hour=9, minute=15, second=0, microsecond=0)
    market_close = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    
    is_weekend = current_time.weekday() >= 5
    is_market_hours = market_open 🟢 Market is OPEN', unsafe_allow_html=True)
    else:
        st.markdown('🔴 Market is CLOSED', unsafe_allow_html=True)
    
    st.write(f"Current IST Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"Market Hours: 09:15 - 15:30 IST (Mon-Fri)")
```

This comprehensive deployment guide specifically tailored for an Indian Stock Market App includes all the necessary configurations, security measures, and deployment options needed to build and deploy a robust application. The guide covers everything from local development setup to production cloud deployments, with specific emphasis on Indian market requirements, data sources, and regulatory considerations.
