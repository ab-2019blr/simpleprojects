# Indian Stock Market Analytics Platform

A comprehensive web-based stock market analytics application built with Python and Streamlit, designed to provide real-time Indian stock market data, advanced analytics, and portfolio management tools.

## 🚀 Features Overview

- **Real-time Stock Data** - Live prices and market updates from Indian stock exchanges
- **Interactive Charts** - Candlestick charts with technical indicators and volume analysis
- **Watchlist Management** - Create and manage multiple stock watchlists
- **Market Analytics** - Daily, weekly, and monthly performance analysis
- **News Integration** - Stock-specific and market news aggregation
- **Technical Analysis** - RSI, MACD, Moving Averages

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.9+ | Core application logic |
| **Web Framework** | Streamlit | Interactive web interface |
| **Database** | MySQL 8.0 | Data storage and management |
| **ORM** | SQLAlchemy | Database operations |
| **Data Source** | Yahoo Finance API / Alpha Vantage | Stock market data |
| **Visualization** | Plotly | Interactive charts and graphs |
| **Data Processing** | Pandas, NumPy | Data manipulation and analysis |

## 📊 Application Modules

### Core Modules

| Module | Location | Functionality | Key Features |
|--------|----------|---------------|--------------|
| **Dashboard** | `pages/dashboard.py` | Main overview interface | • Market indices summary<br>• Top gainers/losers<br>• Quick watchlist view<br>• Market heat map |
| **Analytics** | `pages/analytics.py` | Performance analysis tools | • Historical trend analysis<br>• Sector-wise comparisons<br>• Volume pattern analysis<br>• Custom date range reports |
| **Watchlist** | `pages/watchlist.py` | Portfolio tracking system | • Multiple watchlist creation<br>• Real-time price monitoring<br>• Performance tracking<br>• Alert configuration |
| **Charts** | `pages/charts.py` | Advanced charting interface | • Interactive candlestick charts<br>• Technical indicator overlays<br>• Multi-timeframe analysis<br>• Pattern recognition |
| **News** | `pages/news.py` | Market intelligence hub | • Stock-specific news feed<br>• Market sentiment analysis<br>• News filtering & search<br>• Breaking news alerts |

### Data Layer Modules

| Module | Location | Functionality | Key Features |
|--------|----------|---------------|--------------|
| **Database Manager** | `data/database.py` | Data persistence layer | • MySQL connection management<br>• ORM model definitions<br>• Transaction handling<br>• Connection pooling |
| **API Client** | `data/api_client.py` | External data integration | • Multi-provider API support<br>• Rate limiting & retry logic<br>• Data validation & cleaning<br>• Failover mechanisms |
| **Data Processor** | `data/data_processor.py` | Analytics computation engine | • Technical indicator calculations<br>• Performance metrics<br>• Market statistics<br>• Data aggregation |

### Utility Modules

| Module | Location | Functionality | Key Features |
|--------|----------|---------------|--------------|
| **Chart Utilities** | `utils/charts.py` | Visualization components | • Plotly chart configurations<br>• Custom styling functions<br>• Interactive features<br>• Export capabilities |
| **Calculations** | `utils/calculations.py` | Financial computations | • Moving averages (SMA, EMA)<br>• Momentum indicators (RSI, MACD)<br>• Volatility measures<br>• Support/resistance levels |
| **Helper Functions** | `utils/helpers.py` | Common utilities | • Data formatting functions<br>• Validation utilities<br>• Error handling<br>• Configuration management |

## 🎯 Key Functionalities

### Market Analysis Features

| Feature | Description | Module |
|---------|-------------|--------|
| **Historical Analysis** | 1-year equity performance tracking | Analytics |
| **Gainers/Losers** | Top 5 daily, weekly, monthly performers | Dashboard/Analytics |
| **Volume Analysis** | Trading volume patterns and trends | Charts/Analytics |

### Technical Analysis Tools

| Tool | Description | Implementation |
|------|-------------|----------------|
| **Moving Averages** | SMA (20, 50, 200) and EMA (12, 26) | Calculations module |
| **Momentum Indicators** | RSI, MACD, Stochastic oscillators | Calculations module |
| **Chart Patterns** | Support/resistance, trend lines | Charts module |
| **Volume Indicators** | OBV, Volume Profile | Charts module |

### User Management Features

| Feature | Description | Module |
|---------|-------------|--------|
| **Watchlist Creation** | Unlimited custom watchlists | Watchlist |
| **Stock Tracking** | Real-time monitoring of selected stocks | Watchlist |


### Prerequisites
- Python 3.9 or higher
- MySQL 8.0 or higher
- Git


## 📞 Support & Documentation

| Resource | Link | Description |
|----------|------|-------------|
| **Architecture Guide** | [ARCHITECTURE.md](./doc/architecture.md) | Detailed technical documentation |
| **API Documentation** | [API.md](./doc/api_documentation.md) | API endpoints and usage |
| **Deployment Guide** | [DEPLOYMENT.md](./doc/deployment_guide.md) | Production deployment instructions |
| **Contributing** | [CONTRIBUTING.md](./doc/how_to_contribute.md) | Development guidelines |
| **Issue Tracker** | GitHub Issues | Bug reports and feature requests |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./doc/LICENSE.md) file for details.


## For further details, contact : [Ayan_class_XII](mailto:ab.2019blr@gmail.com)
