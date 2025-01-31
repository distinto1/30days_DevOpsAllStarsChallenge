# 🏀Building a Data Lake for NBA Analytics on AWS: A Slam Dunk Step-by-Step Guide 🏀

This repository contains the mysetup_resources.py script, which automates the creation of a data lake for NBA analytics using AWS services.

The script integrates Amazon S3, AWS Glue, and Amazon Athena, and sets up the infrastructure needed to store and query NBA-related data.

## ARCHITECTURE

![](./image/NBA%20DataLake%20on%20AWS-2.jpg)

## Overview

The mysetup_resurces.py script performs the following actions:

1. Creates an Amazon S3 bucket to store raw and processed data.

2. Uploads sample NBA data (JSON format) to the S3 bucket.
3. Creates an AWS Glue database and an external table for querying the data.
4. Configures Amazon Athena for querying data stored in the S3 bucket.

## Prerequisites

* Before running the script, ensure you have the following:

* Go to Sportsdata.io and create a free account At the top left, you should see "Developers", if you hover over it you should see "API Resources" Click on "Introduction & Testing"

* Click on "SportsDataIO API Free Trial" and fill out the information & be sure to select NBA for this tutorial

* You will get an email and at the bottom it says "Launch Developer Portal"

* By default it takes you to the NFL, on the left click on NBA

* Scroll down until you see "Standings"

* You'll "Query String Parameters", the value in the drop down box is your API key.

* Copy this string because you will need to paste it later in the script

* IAM Role/Permissions: Ensure the user or role running the script has the proper permissions. Refer to the Ploicies folder in GitHub.



## LET'S BEGIN

### Step 1: Create a Virtual Environment

1. Go to aws.amazon.com & sign into your account

2. Go to AWS Console, search for EC2 and click on EC2 Dashboard.

3. Click launch instance; Set your instance name, Choose Ubuntu as your AMI,
select your instance type(t2.micro for free tier), create a key pair and set up a security group to allow port 22 and other ports.

4. Click Launch to create instance. Go to EC2 dash board find your instance, copy its public ip.

Connect via SSH

### Step 2: Create the mysetup_resources.py and cleanup_my_resources files

1. In your terminal, type

```bash
nano mysetup_resources.py
nano cleanup_my_resources.py
```

2. In another window, go to GitHub
Copy the contents inside the mysetup_resources.py and cleanup_my_resources.py files
Go back to your virtual environment and paste the contents inside the mysetup_resources.py and cleanup_my_resources.py files already created.

### Step 3: Setup your Python environment

1. Create a requirement file

```bash
nano requirement.txt
```

2. Paste the following files name in the requirements.txt file

```bash
boto3==1.34.28
requests==2.31.0
python-dotenv==1.0.0
```

Press ^X to exit, press Y to save the file, press enter to confirm the file name

3. Run the following commands:

```bash
sudo apt install python3-pip -y
sudo apt install python3.12-venv -y
python3 -m venv venv
source venv/bin/activate
```

4. Install all dependencies with this command

```bash
pip install -r requirements.txt
```

### Step 4: Create .env file

1. In your terminal, type

```bash
nano .env
```

Press ^X to exit, press Y to save the file, press enter to confirm the file name

2. Paste the following line of code into your file, ensure you swap out with your API key

```bash
SPORTS_DATA_API_KEY=your_sportsdata_api_key
NBA_ENDPOINT=https://api.sportsdata.io/v3/nba/scores/json/Players
S3_BUCKET_NAME=your_s3_bucket_name
GLUE_DATABASE_NAME=your_glue_database_name
AWS_DEFAULT_REGION=your_default_region
```

Press ^X to exit, press Y to save the file, press enter to confirm the file name

### Step 4: Run the Python Script

In your terminal, type

```bash
python3 source/mysetup_resources.py
```

-You should see the resources were successfully created, the sample data was uploaded successfully and the Data Lake Setup Completed

### Step 5: Manually Check For The Resources

In the Search Bar, type S3 and click blue hyper link name
-You should see 2 General purpose bucket named "the_name_you_gave_your_bucket"

-When you click the bucket name you will see 3 objects are in the bucket

Click on raw-data and you will see it contains "nba_player_data.json"

Click the file name and at the top you will see the option to Open the file

-You'll see a long string of various NBA data

Head over to Amazon Athena and you could paste the following sample query:

```bash
SELECT * FROM "glue_nba_datalake"."nba_players" limit 10;
```

  * Click Run -You should see an output if you scroll down under "Query Results"

```bash
SELECT FirstName, LastName, Position, Team
FROM  nba_players
WHERE Position = 'PG';
```

  * Click Run -You should see an output if you scroll down under "Query Results"

```bash
SELECT FirstName, LastName, Position, Team
FROM  nba_players
WHERE Position = 'SF';
```

  * Click Run -You should see an output if you scroll down under "Query Results"

## What We Learned

* Securing AWS services with least privilege IAM policies.
* Automating the creation of services with a script.
* Integrating external APIs into cloud-based workflows.

## Future Enhancements

* Automate data ingestion with AWS Lambda
* Implement a data transformation layer with AWS Glue ETL
* Add advanced analytics and visualizations (AWS QuickSight)
