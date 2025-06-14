# City Weather Web App - Setup Guide

## 📋 Requirements

### Python Packages
Create a `requirements.txt` file:

```
Flask==2.3.3
mysql-connector-python==8.1.0
requests==2.31.0
flask-cors==4.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

### System Requirements
- Python 3.8+
- MySQL 8.0+
- WeatherAPI key (free at weatherapi.com)

## 🚀 Setup Instructions

### 1. Get WeatherAPI Key
1. Visit [weatherapi.com](https://www.weatherapi.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier includes 1 million API calls per month

### 2. Database Setup
1. Install MySQL and start the service
2. The app will automatically create the database and tables on first run
3. Update the database credentials in `app.py`:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'weather_app',
       'autocommit': True
   }
   ```

### 3. API Configuration
1. Replace the API key in `app.py`:
   ```python
   API_KEY = "your_weatherapi_key_here"
   ```

### 4. Project Structure
```
weather_app/
├── app.py
├── requirements.txt
└── templates/
    └── index.html
```

### 5. Run the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

The app will be available at: `http://localhost:5000`

## 🌟 Features

### Core Features
- **Real-time Weather Data**: Get current weather for any city worldwide
- **Comprehensive Weather Info**: Temperature, humidity, pressure, wind speed, visibility
- **Favorites System**: Save and manage favorite cities  
- **Weather History**: Track historical weather data for cities
- **Responsive Design**: Works on desktop and mobile devices

### API Endpoints
- `GET /api/weather/<city_name>` - Get weather data for a city
- `GET /api/favorites` - Get all favorite cities
- `POST /api/favorites` - Add city to favorites
- `DELETE /api/favorites/<city_id>` - Remove city from favorites
- `GET /api/history/<city_name>` - Get weather history for a city

### Database Schema
- **cities**: Store city information (name, country, coordinates)
- **weather_data**: Store historical weather data
- **favorites**: Track user's favorite cities

## 🔧 Customization

### WeatherAPI vs OpenWeatherMap
This app now uses WeatherAPI.com which offers:
- More generous free tier (1M calls/month vs 1K calls/day)
- Better data accuracy
- More detailed weather information
- Easier integration

### Adding Features
You can extend the app by:
- Adding weather forecasts (5-day, hourly)
- Implementing user authentication
- Adding weather alerts and notifications
- Creating weather maps integration
- Adding more detailed weather analytics

## 🐛 Troubleshooting

### Common Issues
1. **Database Connection Error**: Check MySQL service and credentials
2. **API Key Error**: Verify your WeatherAPI key is valid and active
3. **City Not Found**: Some city names may need country specification (e.g., "London, UK")
4. **Port Already in Use**: Change the port in app.py if 5000 is occupied

### Error Handling
The app includes comprehensive error handling for:
- Invalid city names
- API rate limits
- Database connection issues
- Network connectivity problems

## 📝 Notes

- The free WeatherAPI tier has a limit of 1 million calls per month
- Weather data is cached in the database to reduce API calls
- The app automatically creates the database schema on first run
- All timestamps are stored in UTC format