import requests
import time
import schedule
from datetime import datetime
import matplotlib.pyplot as plt

# Constants
API_KEY = '0d7ea86c17931502ccca862474423bde'  
CITY_LIST = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
WEATHER_DATA = []
DAILY_SUMMARIES = []

# Function to convert Kelvin to Celsius
def kelvin_to_celsius(kelvin_temp):
    return kelvin_temp - 273.15

# Function to fetch weather data from OpenWeatherMap API
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'city': city,
            'temperature': kelvin_to_celsius(data['main']['temp']),
            'feels_like': kelvin_to_celsius(data['main']['feels_like']),
            'weather_condition': data['weather'][0]['main'],
            'timestamp': datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
        }
        WEATHER_DATA.append(weather_info)
        print(f"Data fetched for {city}: {weather_info}")
    else:
        print(f"Failed to fetch data for {city}. Status code: {response.status_code}")

# Function to process daily weather summary
def process_daily_summary():
    if not WEATHER_DATA:
        print("No data to summarize.")
        return
    
    daily_summary = {}
    
    for city in CITY_LIST:
        city_data = [data for data in WEATHER_DATA if data['city'] == city]
        if city_data:
            temperatures = [entry['temperature'] for entry in city_data]
            dominant_condition = max(set([entry['weather_condition'] for entry in city_data]), key=[entry['weather_condition'] for entry in city_data].count)
            
            summary = {
                'city': city,
                'avg_temp': sum(temperatures) / len(temperatures),
                'max_temp': max(temperatures),
                'min_temp': min(temperatures),
                'dominant_weather': dominant_condition,
                'summary_time': datetime.now().strftime('%Y-%m-%d')
            }
            daily_summary[city] = summary
    
    DAILY_SUMMARIES.append(daily_summary)
    print("Daily summary processed.")
    visualize_data()

# Function to visualize weather summary
def visualize_data():
    for summary in DAILY_SUMMARIES:
        for city, data in summary.items():
            plt.figure(figsize=(8, 6))
            plt.title(f"Weather Summary for {city} on {data['summary_time']}")
            plt.bar(['Avg Temp', 'Max Temp', 'Min Temp'], [data['avg_temp'], data['max_temp'], data['min_temp']])
            plt.ylabel("Temperature (Celsius)")
            plt.savefig(f"{city}_summary_{data['summary_time']}.png")
            plt.close()
    print("Visualizations created for daily summaries.")

# Function to check alert thresholds and trigger alerts
def check_alert_thresholds():
    for data in WEATHER_DATA:
        if data['temperature'] > 35:
            print(f"ALERT: High temperature in {data['city']}! Current temperature: {data['temperature']}°C")

# Function to clear old data at the end of the day
def reset_data():
    global WEATHER_DATA
    WEATHER_DATA = []
    print("Weather data reset for a new day.")

# Scheduler to fetch weather data every 5 minutes for all cities
def start_weather_monitoring():
    for city in CITY_LIST:
        fetch_weather_data(city)
    process_daily_summary()
    check_alert_thresholds()

# Schedule the tasks
schedule.every(10).seconds.do(start_weather_monitoring)
schedule.every().day.at("23:59").do(reset_data)  # Reset data at the end of the day

# Main loop to run the scheduled tasks
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
