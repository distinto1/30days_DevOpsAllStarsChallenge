import streamlit as st
import boto3
import json
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

class WeatherDashboardViewer:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        
    def load_data_from_s3(self, bucket_name):
        """Load all weather data from S3 and convert to DataFrame"""
        weather_data = []
        
        # List all objects in the weather-data prefix
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name, Prefix='weather-data/'):
            for obj in page.get('Contents', []):
                response = self.s3_client.get_object(Bucket=bucket_name, Key=obj['Key'])
                data = json.loads(response['Body'].read())
                
                # Extract city name from the file key
                city = obj['Key'].split('/')[1].split('-')[0]
                
                # Flatten the nested JSON structure
                flat_data = {
                    'city': city,
                    'timestamp': data['timestamp'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'weather_description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed']
                }
                weather_data.append(flat_data)
        
        return pd.DataFrame(weather_data)

def main():
    st.set_page_config(page_title="Weather Dashboard", layout="wide")
    st.title("Multi-City Weather Dashboard")
    
    # Initialize dashboard
    dashboard = WeatherDashboardViewer()
    
    # Load data
    try:
        df = dashboard.load_data_from_s3(st.secrets["AWS_BUCKET_NAME"])
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d-%H%M%S')
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    selected_cities = st.sidebar.multiselect(
        "Select Cities",
        options=df['city'].unique(),
        default=df['city'].unique()
    )
    
    # Filter data
    filtered_df = df[df['city'].isin(selected_cities)]
    
    # Current weather metrics
    st.header("Current Weather Conditions")
    latest_data = filtered_df.sort_values('timestamp').groupby('city').last()
    
    cols = st.columns(len(selected_cities))
    for idx, city in enumerate(selected_cities):
        with cols[idx]:
            city_data = latest_data.loc[city]
            st.metric(
                city,
                f"{city_data['temperature']:.1f}°F",
                f"{city_data['feels_like'] - city_data['temperature']:.1f}°F"
            )
    
    # Temperature comparison
    st.header("Temperature Comparison")
    fig_temp = px.line(
        filtered_df,
        x='timestamp',
        y='temperature',
        color='city',
        title='Temperature Trends Across Cities'
    )
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Humidity and Wind Speed
    col1, col2 = st.columns(2)
    
    with col1:
        fig_humidity = px.box(
            filtered_df,
            x='city',
            y='humidity',
            title='Humidity Distribution by City'
        )
        st.plotly_chart(fig_humidity)
    
    with col2:
        fig_wind = px.scatter(
            filtered_df,
            x='temperature',
            y='wind_speed',
            color='city',
            title='Temperature vs Wind Speed'
        )
        st.plotly_chart(fig_wind)
    
    # Weather conditions summary
    st.header("Weather Conditions Summary")
    weather_summary = filtered_df.groupby(['city', 'weather_description']).size().unstack(fill_value=0)
    st.dataframe(weather_summary)
    
    # Download data
    st.download_button(
        "Download Data as CSV",
        filtered_df.to_csv(index=False).encode('utf-8'),
        "weather_data.csv",
        "text/csv"
    )

if __name__ == "__main__":
    main()