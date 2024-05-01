import pandas as pd
def clean_and_transform(dataframe):
    # Convert temperature to a numerical value
    dataframe['temperature'] = dataframe['temperature'].str.extract('(\d+)').astype(int)
    # Rename columns for clarity
    dataframe.rename(columns={'period': 'forecast_period', 'short_desc': 'description'}, inplace=True)
    # Fill any missing values, if necessary
    dataframe.fillna(method='ffill', inplace=True)
    return dataframe

def fetch_data_to_dataframe(connection):
    query = "SELECT * FROM weather_forecasts;"
    dataframe = pd.read_sql_query(query, connection)
    return dataframe

def aggregate_data(dataframe): 
    # Aggregate data by period, finding the average temperature
    aggregated_df = dataframe.groupby('forecast_period').agg({'temperature': 'mean'}).reset_index()
    aggregated_df['temperature'] = aggregated_df['temperature'].round(1)  # round the average temperature to one decimal
    return aggregated_df

def clean_and_transform(dataframe): # Convert temperature to a numerical value
    dataframe['temperature'] = dataframe['temperature'].str.extract('(\d+)').astype(int) # Rename columns for clarity
    dataframe.rename(columns={'period': 'forecast_period', 'short_desc': 'description'}, inplace=True) # Fill any missing values, if necessary
    dataframe.fillna(method='ffill', inplace=True)
    return dataframe
