from flask import Flask, request, jsonify, render_template
import mysql.connector
import requests
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
API_KEY = "bee4ef7db6ac42c293f80056251406"  # Replace with your actual WeatherAPI key
WEATHER_BASE_URL = "http://api.weatherapi.com/v1/current.json"

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root1234',  # Replace with your MySQL password
    'database': 'weather_app',
    'autocommit': True
}

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize database and create tables"""
    try:
        # Connect without specifying database first
        temp_config = DB_CONFIG.copy()
        temp_config.pop('database')
        connection = mysql.connector.connect(**temp_config)
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS weather_app")
        cursor.execute("USE weather_app")
        
        # Create cities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                country VARCHAR(50),
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_city (name, country)
            )
        """)
        
        # Create weather_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
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
                FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
            )
        """)
        
        # Create favorites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city_id INT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully!")
        
    except mysql.connector.Error as e:
        print(f"Database initialization error: {e}")

def fetch_weather_data(city_name):
    """Fetch weather data from WeatherAPI"""
    try:
        params = {
            'key': API_KEY,
            'q': city_name,
            'aqi': 'no'
        }
        
        response = requests.get(WEATHER_BASE_URL, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
            
    except requests.RequestException as e:
        print(f"API request error: {e}")
        return None

def save_city_and_weather(weather_data):
    """Save city and weather data to database"""
    connection = get_db_connection()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor()
        
        # Extract city information from WeatherAPI response
        city_name = weather_data['location']['name']
        country = weather_data['location']['country']
        lat = weather_data['location']['lat']
        lon = weather_data['location']['lon']
        
        # Insert or update city
        cursor.execute("""
            INSERT INTO cities (name, country, latitude, longitude) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            latitude = VALUES(latitude), 
            longitude = VALUES(longitude)
        """, (city_name, country, lat, lon))
        
        # Get city ID
        cursor.execute("SELECT id FROM cities WHERE name = %s AND country = %s", (city_name, country))
        city_id = cursor.fetchone()[0]
        
        # Extract weather information from WeatherAPI response
        current = weather_data['current']
        weather_info = {
            'city_id': city_id,
            'temperature': current['temp_c'],
            'feels_like': current['feelslike_c'],
            'humidity': current['humidity'],
            'pressure': current['pressure_mb'],
            'visibility': current['vis_km'],
            'wind_speed': current['wind_kph'] / 3.6,  # Convert kph to m/s
            'wind_direction': current['wind_degree'],
            'weather_main': current['condition']['text'].split()[0],  # First word of condition
            'weather_description': current['condition']['text'],
            'icon': current['condition']['icon'].split('/')[-1].replace('.png', '')  # Extract icon code
        }
        
        # Insert weather data
        cursor.execute("""
            INSERT INTO weather_data (
                city_id, temperature, feels_like, humidity, pressure, 
                visibility, wind_speed, wind_direction, weather_main, 
                weather_description, icon
            ) VALUES (
                %(city_id)s, %(temperature)s, %(feels_like)s, %(humidity)s, 
                %(pressure)s, %(visibility)s, %(wind_speed)s, %(wind_direction)s, 
                %(weather_main)s, %(weather_description)s, %(icon)s
            )
        """, weather_info)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return city_id
        
    except mysql.connector.Error as e:
        print(f"Database save error: {e}")
        return None

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/weather/<city_name>')
def get_weather(city_name):
    """Get weather data for a city"""
    weather_data = fetch_weather_data(city_name)
    
    if not weather_data:
        return jsonify({'error': 'City not found or API error'}), 404
    
    city_id = save_city_and_weather(weather_data)
    
    if not city_id:
        return jsonify({'error': 'Database error'}), 500
    
    # Format response for WeatherAPI data structure
    location = weather_data['location']
    current = weather_data['current']
    
    response_data = {
        'city': location['name'],
        'country': location['country'],
        'temperature': current['temp_c'],
        'feels_like': current['feelslike_c'],
        'humidity': current['humidity'],
        'pressure': current['pressure_mb'],
        'visibility': current['vis_km'],
        'wind_speed': current['wind_kph'] / 3.6,  # Convert kph to m/s
        'wind_direction': current['wind_degree'],
        'weather_main': current['condition']['text'].split()[0],
        'weather_description': current['condition']['text'],
        'icon': current['condition']['icon'].split('/')[-1].replace('.png', ''),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(response_data)

@app.route('/api/favorites', methods=['GET', 'POST'])
def handle_favorites():
    """Handle favorite cities"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'GET':
        # Get all favorite cities with latest weather data
        cursor.execute("""
            SELECT 
                c.id, c.name, c.country,
                wd.temperature, wd.weather_description, wd.icon,
                wd.timestamp
            FROM favorites f
            JOIN cities c ON f.city_id = c.id
            LEFT JOIN weather_data wd ON c.id = wd.city_id
            WHERE wd.id = (
                SELECT MAX(id) FROM weather_data WHERE city_id = c.id
            )
            ORDER BY f.added_at DESC
        """)
        
        favorites = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify(favorites)
    
    else:  # POST
        data = request.get_json()
        city_name = data.get('city_name')
        
        if not city_name:
            return jsonify({'error': 'City name required'}), 400
        
        # Get city ID
        cursor.execute("SELECT id FROM cities WHERE name = %s", (city_name,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'error': 'City not found in database'}), 404
        
        city_id = result['id']
        
        # Add to favorites
        try:
            cursor.execute("INSERT INTO favorites (city_id) VALUES (%s)", (city_id,))
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({'message': 'City added to favorites'})
            
        except mysql.connector.IntegrityError:
            return jsonify({'error': 'City already in favorites'}), 400

@app.route('/api/favorites/<int:city_id>', methods=['DELETE'])
def remove_favorite(city_id):
    """Remove city from favorites"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    cursor = connection.cursor()
    cursor.execute("DELETE FROM favorites WHERE city_id = %s", (city_id,))
    
    if cursor.rowcount > 0:
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'City removed from favorites'})
    else:
        cursor.close()
        connection.close()
        return jsonify({'error': 'City not found in favorites'}), 404

@app.route('/api/history/<city_name>')
def get_weather_history(city_name):
    """Get weather history for a city"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection error'}), 500
    
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            wd.temperature, wd.humidity, wd.pressure, wd.wind_speed,
            wd.weather_description, wd.timestamp
        FROM weather_data wd
        JOIN cities c ON wd.city_id = c.id
        WHERE c.name = %s
        ORDER BY wd.timestamp DESC
        LIMIT 20
    """, (city_name,))
    
    history = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(history)

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)