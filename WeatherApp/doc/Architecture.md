# Weather App - Architecture Documentation

## 🏗️ System Architecture Overview

The City Weather Web App follows a **3-tier architecture pattern** with clear separation of concerns:

1. **Presentation Layer** (Client-side)
2. **Application Layer** (Server-side logic)
3. **Data Layer** (Database and external APIs)

---

## 📊 Architecture Components

### 1. Client Layer (Frontend)

#### **Web Browser/Mobile Interface**
- **Technology**: Modern web browsers with responsive design
- **Compatibility**: Desktop, tablet, and mobile devices
- **Features**: Progressive web app capabilities

#### **JavaScript Frontend**
- **Framework**: Vanilla JavaScript (ES6+)
- **Responsibilities**:
  - DOM manipulation and event handling
  - AJAX requests to backend APIs
  - Client-side validation
  - Dynamic UI updates
  - Local state management

#### **HTML Templates**
- **Engine**: Flask Jinja2 templating
- **Structure**: Semantic HTML5 markup
- **Accessibility**: ARIA labels and semantic elements

#### **CSS Styling**
- **Approach**: Modern CSS3 with Flexbox/Grid
- **Features**: 
  - Responsive design with media queries
  - CSS animations and transitions
  - Glass morphism design elements
  - Dark/light theme support

---

### 2. Application Layer (Backend)

#### **Flask Web Server**
- **Framework**: Flask 2.3.3 (Python microframework)
- **Features**:
  - Lightweight and flexible
  - Built-in development server
  - Template rendering engine
  - Request/response handling

#### **Route Handlers**
```python
@app.route('/')                           # Main page
@app.route('/api/weather/<city_name>')    # Weather data
@app.route('/api/favorites')              # Favorites management
@app.route('/api/history/<city_name>')    # Weather history
```

#### **REST API Endpoints**
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/weather/<city>` | GET | Fetch current weather |
| `/api/favorites` | GET | List favorite cities |
| `/api/favorites` | POST | Add city to favorites |
| `/api/favorites/<id>` | DELETE | Remove from favorites |
| `/api/history/<city>` | GET | Weather history |

#### **CORS Middleware**
- **Purpose**: Enable cross-origin requests
- **Configuration**: Allows all origins in development
- **Production**: Should be restricted to specific domains

#### **Business Logic Services**

##### **Weather Service**
- Interfaces with WeatherAPI.com
- Handles API request/response formatting
- Implements error handling and retry logic
- Caches weather data to reduce API calls

##### **Database Service**
- Manages database connections
- Implements CRUD operations
- Handles connection pooling
- Provides transaction management

##### **Favorites Service**
- Manages user favorite cities
- Prevents duplicate entries
- Handles favorite addition/removal
- Links favorites to weather data

##### **History Service**
- Stores historical weather data
- Provides weather trend analysis
- Implements data retention policies
- Supports date range queries

---

### 3. Data Layer

#### **MySQL Database Schema**

##### **Cities Table**
```sql
CREATE TABLE cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_city (name, country)
);
```

##### **Weather Data Table**
```sql
CREATE TABLE weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT,
    temperature DECIMAL(5, 2),
    feels_like DECIMAL(5, 2),
    humidity INT,
    pressure INT,
    visibility INT,
    wind_speed DECIMAL(5, 2),
    wind_direction INT,
    weather_main VARCHAR(50),
    weather_description VARCHAR(100),
    icon VARCHAR(10),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);
```

##### **Favorites Table**
```sql
CREATE TABLE favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);
```

---

### 4. External Services

#### **WeatherAPI.com**
- **Purpose**: Primary weather data source
- **Endpoint**: `http://api.weatherapi.com/v1/current.json`
- **Rate Limit**: 1 million calls/month (free tier)
- **Data Format**: JSON responses
- **Features**:
  - Current weather conditions
  - Global city coverage
  - Real-time updates
  - Detailed meteorological data

---

## 🔄 Data Flow Architecture

### 1. Weather Data Request Flow
```
User Input → Frontend JS → Flask Route → Weather Service → WeatherAPI → Database → Response
```

1. User enters city name in search form
2. JavaScript captures form submission
3. AJAX request sent to Flask `/api/weather/<city>` endpoint
4. Weather Service calls WeatherAPI.com
5. Response data processed and stored in database
6. Formatted JSON response sent to frontend
7. JavaScript updates UI with weather information

### 2. Favorites Management Flow
```
User Action → Frontend JS → Flask API → Favorites Service → Database → UI Update
```

### 3. Database Interaction Flow
```
Service Layer → Database Service → MySQL Connection → Query Execution → Result Processing
```

---

## 🔧 Technical Specifications

### **Backend Stack**
- **Language**: Python 3.8+
- **Framework**: Flask 2.3.3
- **Database**: MySQL 8.0+
- **ORM**: Native MySQL Connector
- **HTTP Client**: Requests library

### **Frontend Stack**
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Modern CSS with Flexbox/Grid
- **AJAX**: Fetch API for HTTP requests
- **Icons**: Unicode emojis for weather icons

### **Database Configuration**
- **Engine**: InnoDB (default)
- **Character Set**: UTF-8
- **Timezone**: UTC
- **Connection Pool**: Single connection per request
- **Auto-commit**: Enabled

---

## 🚀 Deployment Architecture

### **Development Environment**
- Flask development server
- Local MySQL instance
- Debug mode enabled
- Hot reloading for development

### **Production Considerations**
- **Web Server**: Gunicorn + Nginx
- **Database**: MySQL with replication
- **Caching**: Redis for session/API caching
- **Monitoring**: Application performance monitoring
- **SSL**: HTTPS with Let's Encrypt certificates

---

## 🔒 Security Architecture

### **Data Protection**
- SQL injection prevention with parameterized queries
- Input validation and sanitization
- CORS configuration for API security
- Rate limiting on API endpoints

### **API Security**
- WeatherAPI key stored as environment variable
- Database credentials externalized
- Error handling without sensitive data exposure

---

## 📈 Scalability Considerations

### **Horizontal Scaling**
- Stateless application design
- Database connection pooling
- API response caching
- Load balancer support

### **Performance Optimization**
- Database indexing on frequently queried fields
- Weather data caching to reduce API calls
- Lazy loading of weather history
- Compressed JSON responses

---

## 🔍 Monitoring and Logging

### **Application Monitoring**
- Flask request/response logging
- Database query performance tracking
- WeatherAPI response time monitoring
- Error rate tracking

### **Health Checks**
- Database connectivity checks
- External API availability
- Application startup validation
- Dependency health monitoring

---

## 🧪 Testing Strategy

### **Unit Testing**
- Service layer business logic
- Database operations
- API response formatting
- Input validation functions

### **Integration Testing**
- End-to-end API workflows
- Database transaction testing
- External API integration
- Frontend-backend communication

### **Performance Testing**
- Database query optimization
- API response time benchmarks
- Concurrent user simulation
- Memory usage profiling

---

## 📋 Maintenance and Operations

### **Regular Maintenance**
- Database backup and recovery procedures
- WeatherAPI usage monitoring
- Log rotation and cleanup
- Security updates and patches

### **Operational Procedures**
- Application deployment process
- Database migration scripts
- Configuration management
- Incident response procedures
