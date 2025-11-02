# Simple Learning Projects Repository

A collection of educational software development projects demonstrating various technologies and programming concepts.

## 📚 Project Portfolio

### 1. Weather App (HTML & JavaScript)
- **Technology**: HTML, CSS, JavaScript, Weather API
- **Purpose**: Basic web development and API integration learning
- **Features**: Real-time weather data display

### 2. Enhanced Weather App (Python + Flask)
- **Technology**: Python, Flask, MySQL, RESTful APIs
- **Purpose**: Backend development and database integration
- **Features**: Advanced architecture with comprehensive API documentation

### 3. Alumni Management System
- **Technology**: Python, Django, MySQL
- **Purpose**: Full-stack web application development
- **Features**: Alumni tracking and management system

### 4. 🏆 **StockMarketApp** - *Featured Project*
- **Technology**: Python, Streamlit, MySQL, Pandas, Plotly, APIs
- **Purpose**: Advanced financial application development
- **Status**: **Complete & Production Ready**

## 🌟 Featured Project: StockMarketApp

### Overview
A comprehensive stock market analysis and portfolio management application focused on Indian equities. This project demonstrates advanced software engineering principles, real-time data processing, and modern web application development.

### 🚀 Key Features
- **Real-time Market Dashboard** with live tickers and analytics
- **Advanced Charting System** with technical indicators (RSI, Moving Averages)
- **Portfolio Management** with P&L tracking and performance metrics
- **Watchlist Management** with dynamic stock selection
- **News Integration** with market updates and global coverage
- **Interactive Data Visualization** using Plotly charts

### 🏗️ Technical Architecture
```
StockMarketApp/
├── app.py                    # Main Streamlit application
├── config/                   # Configuration management
│   ├── database_config.py    # Database connection settings
│   └── api_config.py         # API configurations
├── data/                     # Data layer
│   ├── database.py           # MySQL integration with SQLAlchemy
│   ├── api_client.py         # External API integrations
│   └── data_processor.py     # Technical analysis calculations
├── pages/                    # Application pages
│   ├── dashboard.py          # Market overview and analytics
│   ├── charts.py             # Advanced charting with indicators
│   ├── portfolio.py          # Portfolio management system
│   ├── watchlist.py          # Stock watchlist management
│   └── news.py               # Market news integration
├── utils/                    # Utility functions
│   ├── calculations.py       # Financial calculations
│   ├── charts.py             # Chart generation utilities
│   └── helpers.py            # Common helper functions
└── doc/                      # Comprehensive documentation
```

### 📊 Core Functionalities

#### 1. Market Dashboard
- **Live Index Ticker**: Real-time Nifty indices with animated scrolling
- **Stock Price Ticker**: Continuous display of Nifty 50 stocks
- **Market Analytics**: Advance/decline analysis, top gainers/losers
- **Index Valuation**: P/E, P/B ratios for major indices

#### 2. Technical Analysis
- **Candlestick Charts**: Interactive OHLC visualization
- **RSI Indicator**: 14-day Relative Strength Index with overbought/oversold levels
- **Moving Averages**: 20-day and 50-day DMA calculations
- **Volume Analysis**: Trading volume patterns and trends

#### 3. Portfolio Management
- **Transaction Recording**: Add/delete stock transactions
- **Real-time P&L**: Automatic profit/loss calculations
- **Performance Metrics**: Investment tracking and analytics
- **Data Export**: CSV download functionality

#### 4. Data Integration
- **Multiple APIs**: Yahoo Finance, Alpha Vantage integration
- **MySQL Database**: Normalized schema with optimized queries
- **Real-time Updates**: Live market data synchronization
- **Caching Strategy**: Performance optimization with Streamlit caching

### 🛠️ Technology Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive web interface |
| **Backend** | Python 3.9+ | Core application logic |
| **Database** | MySQL 8.0 | Data persistence |
| **ORM** | SQLAlchemy | Database operations |
| **APIs** | Yahoo Finance, Alpha Vantage | Market data |
| **Visualization** | Plotly | Interactive charts |
| **Data Processing** | Pandas, NumPy | Analysis & calculations |

### 📈 Mathematical Implementations

#### Technical Indicators
```python
# RSI Calculation
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
```

#### Portfolio Metrics
- **Total Investment** = Σ(Quantity × Average Buy Price)
- **Current Value** = Σ(Quantity × Current Price)
- **P&L** = Current Value - Total Investment
- **P&L Percentage** = (P&L / Total Investment) × 100

### 🎯 Educational Value

#### Programming Concepts Demonstrated
1. **Object-Oriented Programming**: Modular class-based architecture
2. **Database Design**: Normalized schema with relationships
3. **API Integration**: RESTful services with error handling
4. **Data Visualization**: Interactive charts and real-time updates
5. **Financial Mathematics**: Technical analysis calculations
6. **Web Development**: Modern responsive web application

#### Software Engineering Principles
1. **Separation of Concerns**: Clean modular code organization
2. **Performance Optimization**: Caching and efficient algorithms
3. **Error Handling**: Comprehensive exception management
4. **Documentation**: Extensive code and API documentation
5. **Scalability**: Architecture designed for future enhancements

### 📊 Project Statistics
- **Development Time**: 3+ months
- **Lines of Code**: 2,500+ across all modules
- **Database Tables**: 5+ normalized tables
- **API Integrations**: 3+ external data sources
- **Features**: 15+ major functionalities
- **Documentation**: 10+ comprehensive guides

### 🏆 Key Achievements
1. **Full-Stack Development**: Complete application from database to UI
2. **Real-time Processing**: Live market data integration
3. **Advanced Analytics**: Technical indicators and financial calculations
4. **Professional UI/UX**: Interactive and responsive design
5. **Industry Standards**: Production-ready code quality

### 📁 Project Files
- **Main Application**: [StockMarketApp/](./StockMarketApp/)
- **Detailed Report**: [StockMarketApp_Project_Report.md](./StockMarketApp_Project_Report.md)
- **Architecture Guide**: [StockMarketApp/doc/architecture.md](./StockMarketApp/doc/architecture.md)
- **API Documentation**: [StockMarketApp/doc/api_documentation.md](./StockMarketApp/doc/api_documentation.md)

---

## 🎓 Academic Information
- **Student**: Ayan Banerjee, Class XII
- **Subject**: Computer Science Project
- **Academic Year**: 2025-26
- **Institution**: [School Name]
- **Project Focus**: Full-Stack Development, Financial Technology, Data Analysis

## 📞 Contact
For project inquiries and technical discussions:
- **Email**: [ab.2019blr@gmail.com](mailto:ab.2019blr@gmail.com)
- **Project Repository**: Available for academic review and collaboration

---

*This repository showcases progressive learning in software development, from basic web applications to advanced financial technology solutions.*