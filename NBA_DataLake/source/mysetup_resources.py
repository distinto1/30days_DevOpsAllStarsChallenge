import boto3
import json
import time
import requests
from dotenv import load_dotenv
import os
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

class NBADataLakeSetup:
    def __init__(self, region="us-east-1"):
        """
        Initialize AWS clients and configuration
        :param region: AWS region
        """
        self.region = region
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        if not self.bucket_name:
            self.bucket_name = f"nba-analytics-data-lake-{int(time.time())}"
        
        self.database_name = os.getenv('GLUE_DATABASE_NAME', 'glue_nba_datalake')
        self.athena_output_location = f"s3://{self.bucket_name}/athena-query-results/"

        # AWS Clients
        self.s3_client = boto3.client("s3", region_name=self.region)
        self.glue_client = boto3.client("glue", region_name=self.region)
        self.athena_client = boto3.client("athena", region_name=self.region)

        # API Configuration
        self.api_key = os.getenv("SPORTS_DATA_API_KEY")
        self.nba_endpoint = os.getenv("NBA_ENDPOINT")

    def create_s3_bucket(self):
        """Create S3 bucket with error handling and region-specific configuration"""
        try:
            if self.region == "us-east-1":
                self.s3_client.create_bucket(Bucket=self.bucket_name)
            else:
                self.s3_client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": self.region}
                )
            print(f"S3 bucket '{self.bucket_name}' created successfully.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                print(f"Bucket '{self.bucket_name}' already exists.")
            else:
                raise

    def create_glue_database(self):
        """Create Glue database with robust error handling"""
        try:
            self.glue_client.create_database(
                DatabaseInput={
                    "Name": self.database_name,
                    "Description": "Glue database for NBA sports analytics"
                }
            )
            print(f"Glue database '{self.database_name}' created successfully.")
        except self.glue_client.exceptions.AlreadyExistsException:
            print(f"Glue database '{self.database_name}' already exists.")

    def fetch_nba_data(self):
        """Fetch NBA data with robust error handling and validation"""
        try:
            headers = {"Ocp-Apim-Subscription-Key": self.api_key}
            response = requests.get(self.nba_endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Basic data validation
            if not isinstance(data, list) or not data:
                raise ValueError("Invalid or empty NBA data received")
            
            return data
        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching NBA data: {e}")
            return []

    def upload_data_to_s3(self, data):
        """Upload data to S3 with line-delimited JSON"""
        if not data:
            print("No data to upload.")
            return

        line_delimited_data = "\n".join([json.dumps(record) for record in data])
        file_key = f"raw-data/nba_player_data_{int(time.time())}.jsonl"

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=line_delimited_data.encode('utf-8')
            )
            print(f"Uploaded data to S3: {file_key}")
        except ClientError as e:
            print(f"S3 upload error: {e}")

    def create_glue_table(self):
        """Create Glue table with flexible schema"""
        try:
            self.glue_client.create_table(
                DatabaseName=self.database_name,
                TableInput={
                    "Name": "nba_players",
                    "StorageDescriptor": {
                        "Columns": [
                            {"Name": "PlayerID", "Type": "int"},
                            {"Name": "FirstName", "Type": "string"},
                            {"Name": "LastName", "Type": "string"},
                            {"Name": "Team", "Type": "string"},
                            {"Name": "Position", "Type": "string"},
                            {"Name": "Points", "Type": "int"}
                        ],
                        "Location": f"s3://{self.bucket_name}/raw-data/",
                        "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                        "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                        "SerdeInfo": {
                            "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe"
                        },
                    },
                    "TableType": "EXTERNAL_TABLE",
                },
            )
            print(f"Glue table 'nba_players' created successfully.")
        except ClientError as e:
            print(f"Glue table creation error: {e}")

    def configure_athena(self):
        """Configure Athena workgroup and output location"""
        try:
            self.athena_client.create_work_group(
                Name='nba_analytics_workgroup',
                Configuration={
                    'ResultConfiguration': {
                        'OutputLocation': self.athena_output_location
                    }
                }
            )
            print(f"Athena workgroup configured with output location: {self.athena_output_location}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'AlreadyExistsException':
                print("Athena workgroup already exists")
            else:
                print(f"Error configuring Athena: {e}")

    def run(self):
        """Orchestrate the entire data lake setup process"""
        try:
            self.create_s3_bucket()
            self.create_glue_database()
            nba_data = self.fetch_nba_data()
            
            if nba_data:
                self.upload_data_to_s3(nba_data)
                self.create_glue_table()
                self.configure_athena()
            else:
                print("Skipping data upload due to no data.")
        except Exception as e:
            print(f"Data lake setup failed: {e}")

def main():
    data_lake = NBADataLakeSetup()
    data_lake.run()

if __name__ == "__main__":
    main()
