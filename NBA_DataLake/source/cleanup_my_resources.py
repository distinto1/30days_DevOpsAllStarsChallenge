import os
import time
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

class NBADataLakeCleanup:
    def __init__(self, region=None):
        """
        Initialize AWS clients and configuration
        :param region: AWS region
        """
        self.region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        if not self.bucket_name:
            self.bucket_name = f"nba-analytics-data-lake-{int(time.time())}"
            
        self.database_name = os.getenv('GLUE_DATABASE_NAME', 'glue_nba_datalake')

        # AWS Clients
        self.s3_client = boto3.client('s3', region_name=self.region)
        self.glue_client = boto3.client('glue', region_name=self.region)
        self.athena_client = boto3.client('athena', region_name=self.region)

    def delete_bucket_contents(self):
        """Delete all objects in the S3 bucket"""
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            for result in paginator.paginate(Bucket=self.bucket_name):
                if 'Contents' in result:
                    objects = [{'Key': obj['Key']} for obj in result['Contents']]
                    self.s3_client.delete_objects(
                        Bucket=self.bucket_name,
                        Delete={'Objects': objects}
                    )
                    print(f"Deleted {len(objects)} objects from bucket {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting bucket contents: {e}")

    def delete_s3_bucket(self):
        """Delete S3 bucket and its contents"""
        try:
            self.delete_bucket_contents()
            self.s3_client.delete_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} deleted successfully.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                print(f"Bucket {self.bucket_name} does not exist.")
            else:
                print(f"Error deleting bucket {self.bucket_name}: {e}")

    def delete_glue_database(self):
        """Delete Glue database and its tables"""
        try:
            tables = self.glue_client.get_tables(DatabaseName=self.database_name)['TableList']
            for table in tables:
                self.glue_client.delete_table(
                    DatabaseName=self.database_name, 
                    Name=table['Name']
                )
                print(f"Deleted table: {table['Name']}")

            self.glue_client.delete_database(Name=self.database_name)
            print(f"Database {self.database_name} deleted successfully.")
        except self.glue_client.exceptions.EntityNotFoundException:
            print(f"Glue database {self.database_name} does not exist.")
        except ClientError as e:
            print(f"Error deleting Glue database: {e}")

    def delete_athena_query_results(self):
        """Delete Athena query results from S3"""
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            for result in paginator.paginate(
                Bucket=self.bucket_name, 
                Prefix="athena-query-results/"
            ):
                if 'Contents' in result:
                    objects = [{'Key': obj['Key']} for obj in result['Contents']]
                    self.s3_client.delete_objects(
                        Bucket=self.bucket_name,
                        Delete={'Objects': objects}
                    )
                    print(f"Deleted {len(objects)} Athena query results")
        except ClientError as e:
            print(f"Error deleting Athena query results: {e}")

    def delete_athena_workgroup(self):
        """Delete Athena workgroup"""
        try:
            self.athena_client.delete_work_group(
                WorkGroup='nba_analytics_workgroup',
                RecursiveDeleteOption=True
            )
            print("Deleted Athena workgroup: nba_analytics_workgroup")
        except ClientError as e:
            if 'EntityNotFoundException' in str(e):
                print("Athena workgroup does not exist")
            else:
                print(f"Error deleting Athena workgroup: {e}")

    def cleanup(self):
        """Orchestrate complete resource cleanup"""
        print("Starting NBA Data Lake cleanup...")
        try:
            self.delete_glue_database()
            self.delete_athena_workgroup()
            self.delete_athena_query_results()
            self.delete_s3_bucket()
            print("Data Lake cleanup completed successfully.")
        except Exception as e:
            print(f"Cleanup process encountered an error: {e}")

def main():
    cleanup = NBADataLakeCleanup()
    cleanup.cleanup()

if __name__ == "__main__":
    main()