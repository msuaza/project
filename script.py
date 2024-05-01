import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2 
from datetime import datetime 
from db import connect_to_db, insert_weather_data, fetch_data
from pdFuncs import fetch_data_to_dataframe, clean_and_transform, aggregate_data
from pltFuncs import plot_temperature_comparison, plot_temperature_trends
db_connection = connect_to_db()

def fetch_weather_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch web page. Status code: {response.status_code}")

def parse_weather_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Modify the selector based on the data you need
    forecast_items = soup.find_all('div', class_='tombstone-container')
    weather_data = []
    for item in forecast_items:
        period = item.find('p', class_='period-name').get_text()
        short_desc = item.find('p', class_='short-desc').get_text()
        temp = item.find('p', class_='temp').get_text()
        weather_data.append({'period': period, 'short_desc': short_desc, 'temp': temp})
    return weather_data


# Example usage
url = "https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168"
try:
    page_content = fetch_weather_page(url)
    weather_data = parse_weather_data(page_content)
except Exception as e:
    print(f"An error occurred: {e}")
    print('=======================================')
for data_point in weather_data:
    print(data_point)

# Connect to the database
db_connection = connect_to_db()
# Insert weather data into the database
insert_weather_data(db_connection, weather_data)
# Fetch data from the database
fetch_data(db_connection)
# Fetch data to a DataFrame
df = fetch_data_to_dataframe(db_connection)
# Clean and transform the DataFrame
df_cleaned = clean_and_transform(df)
# Aggregate the data
df_aggregated = aggregate_data(df_cleaned)
# Plot temperature comparison
plot_temperature_comparison(df)




