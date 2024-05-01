from flask import Flask, jsonify, send_file
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Matplotlib
import matplotlib.pyplot as plt
import io
import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

def connect_to_db():
    load_dotenv()
    try:
        # Replace 'dbname', 'user', 'password', and 'host' with your database details
        connection = psycopg2.connect(
            dbname= os.getenv('DBNAME'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST')
        )
        connection.autocommit = True
        print("Connected to the database successfully")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")

def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn


def fetch_data(db_connection):
    cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM weather_forecasts;")
    records = cursor.fetchall()
    for record in records:
        print(record)

def fetch_data_to_dataframe(connection):
    query = "SELECT * FROM weather_forecasts;"
    dataframe = pd.read_sql_query(query, connection)
    return dataframe

# To save back to the database (assuming a new table for processed data)
def save_processed_data(connection, dataframe):
    dataframe.to_sql('processed_weather_forecasts', con=connection, if_exists='replace', index=False)
    print("Processed data saved to the database successfully")

def insert_weather_data(db_connection, weather_data):
    cursor = db_connection.cursor()

    cursor.execute("DELETE FROM weather_forecasts;")
    print("Existing data cleared from table.")

    query = """
    INSERT INTO weather_forecasts (period, short_desc, temperature)
    VALUES (%s, %s, %s);
    """
    for data in weather_data:
        cursor.execute(query, (data['period'], data['short_desc'], data['temp']))
    print("Data inserted successfully")

load_dotenv()  # This is to load your environment variables from .env file
app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def get_weather():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, period, short_desc, temperature, scraped_at
        FROM weather_forecasts
        WHERE scraped_at >= current_date - INTERVAL '1 week'
        ORDER BY scraped_at DESC;
    """)
    weather_data = cur.fetchall()
    cur.close()
    conn.close()

    columns = ['id', 'period', 'short_desc', 'temperature', 'scraped_at']
    result = [dict(zip(columns, row)) for row in weather_data]
    return jsonify(result)

def create_temperature_plot():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT period, temperature
        FROM weather_forecasts
        WHERE scraped_at >= current_date - INTERVAL '7 days'
        ORDER BY scraped_at;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()

    df = pd.DataFrame(data, columns=['period', 'temperature'])
    df['temperature'] = df['temperature'].str.extract('(\d+)').astype(int)

    fig, ax = plt.subplots()
    ax.plot(df['period'], df['temperature'], marker='o', linestyle='-', color='b')
    ax.set(title='Weekly Temperature Trends', xlabel='Period', ylabel='Temperature (°F)')
    ax.grid(True)
    ax.set_xticklabels(df['period'], rotation=45)
    return fig

@app.route('/temperature_trends')
def temperature_trends():
    fig = create_temperature_plot()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)