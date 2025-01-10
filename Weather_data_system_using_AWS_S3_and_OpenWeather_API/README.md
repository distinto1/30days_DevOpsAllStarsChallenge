# Day 01 - Weather Data Collection System Using AWS S3 and OpenWeather API

This project is a Weather Data Collection System that demonstrates core DevOps principles by combining:

* External API Integration (OpenWeather API)
* Cloud Storage (AWS S3)
* Infrastructure as Code
* Version Control (Git)
* Python Development
* Error Handling
* Environment Management

## Components

* Fetches real-time weather data for multiple cities
* Displays temperature (°F), humidity, and weather conditions
* Automatically stores weather data in AWS S3
* Supports multiple cities tracking
* Timestamps all data for historical tracking

## Technical Stack

* Language: Python 3.x
* Cloud Provider: Amazon Web Services (AWS) - Specifically, S3 for object storage
* External API: OpenWeather API for accessing weather data
* Dependencies:
  * `boto3:` AWS SDK for Python, used for interacting with S3.
  * `python-dotenv:` For securely managing environment variables (e.g., API keys).
  * `requests:` Python library for making HTTP requests to the OpenWeather API.

## Implementation

1. sign up to the openweather website.

2. create an IAM user with S3 permissions

3. configure your AWS environment variables

```bash
aws configure
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_access_key
DEFAULT_REGION_NAME=us-east-1
DEFAULT_OUTPUT_FORMAT=json

```

4. Clone the repository:

```bash

git clone  https://github.com/distinto1/30days_DevOpsAllStarsChallenge.git
```

4. Move into weather_data_system_using_AWS_s3_and_OpenWeather_API folder

5. install dependencies:

```bash
pip install -r requirements.txt

pip install streamlit pandas plotly boto3
```

6. create your .env file for API and your Bucket Name

```bash
echo "OPENWEATHER_API_KEY=******" >> .env
echo "AWS_BUCKET_NAME=*******" >> .env
```

7. Retrieve data to AWS s3

```bash
python3 source/myweather_console.py
```

8. Set up environment variables in .streamlit/secrets.toml

```bash
AWS_ACCESS_KEY_ID = "your_access_key"
AWS_SECRET_ACCESS_KEY = "your_secret_key"
AWS_BUCKET_NAME = "your_bucket_name"
```


8. Run the weather dash board

```bash
streamlit run streamlit-weather-view.py
```
