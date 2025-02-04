# NCAAGameHighlights

# HighlightProcessor

This project uses RapidAPI to obtain NCAA game highlights using a Docker container and uses AWS Media Convert to convert the media file.

## File Overview

The config.py script performs the following actions: Imports necessary environment variables and assigns them to Python variables, providing default values where appropriate. This approach allows for flexible configuration management, enabling different settings for various environments (e.g., development, staging, production) without modifying the source code.

### The fetch.py script performs the following actions

Establishes the date and league that will be used to find highlights. We are using NCAA in this example because it's included in the free version. This will fetch the highlights from the API and store them in an S3 bucket as a JSON file (basketball_highlight.json)

### Process_1_video.py performs the following actions

Connects to the S3 bucket and retrieves the JSON file. Extracts the first video URL from within the JSON file. Downloads the video fiel from the internet into the memory using the requests library. Saves the video as a new file in the S3 bucket under a different folder (videos/) Logs the status of each step

### Mediaconvert_process.py performs the following actions

Creates and submits a MediaConvert job Uses MediaConvert to process a video file - configures the video codec, resolution and bitrate. Also configured the audio settings Stores the processed video back into an S3 bucket

### Run_all.py performs the following actions -  

Runs the scripts in a chronological order and provides buffer time for the tasks to be created.

## .env file

Stores all over the environment variables, these are variables that we don't want to hardcode into our script.

### Dockerfile

Performs the following actions: Provides the step by step approach to build the image.

### Terraform Scripts -

These scripts are used to created resources in AWS in a scalable and repeatable way. All of the resources we work with like S3, creating IAM user roles, elastic registry service and elastic container services is built here.

### Prerequisites

Before running the scripts, ensure you have the following:

1. Create Rapidapi Account
Rapidapi.com account, will be needed to access highlight images and videos.

For this project we will be using NCAA (USA College Basketball) highlights since it's included for free in the basic plan.

Sports Highlights API is the endpoint we will be using

2. Verify prerequites are installed
Docker should be pre-installed in most regions docker --version

AWS CloudShell has AWS CLI pre-installed aws --version

Python3 should be pre-installed also python3 --version

3. Retrieve AWS Account ID
Copy your AWS Account ID Once logged in to the AWS Management Console Click on your account name in the top right corner You will see your account ID Copy and save this somewhere safe because you will need to update codes in the labs later

4. Retrieve Access Keys and Secret Access Keys
You can check to see if you have an access key in the IAM dashboard Under Users, click on a user and then "Security Credentials" Scroll down until you see the Access Key section You will not be able to retrieve your secret access key so if you don't have that somewhere, you need to create an access key.
