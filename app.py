from flask import Flask, jsonify, send_file
from db import get_db_connection, fetch_data_to_dataframe
from pdFuncs import clean_and_transform, aggregate_data
from pltFuncs import plot_temperature_comparison, plot_temperature_trends

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

@app.route('/temperature_trends')
def temperature_trends():
    conn = get_db_connection()
    df = fetch_data_to_dataframe(conn)
    conn.close()

    df_cleaned = clean_and_transform(df)
    df_aggregated = aggregate_data(df_cleaned)

    plot_temperature_trends(df_aggregated)
    return send_file('temperature_trends.png', mimetype='image/png')

@app.route('/temperature_comparison')
def temperature_comparison():
    conn = get_db_connection()
    df = fetch_data_to_dataframe(conn)
    conn.close()

    df_cleaned = clean_and_transform(df)
    df_aggregated = aggregate_data(df_cleaned)

    plot_temperature_comparison(df_aggregated)
    return send_file('temperature_comparison.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)