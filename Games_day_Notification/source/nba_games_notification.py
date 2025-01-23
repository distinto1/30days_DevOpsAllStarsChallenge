import urllib.request
import os
from _datetime import datetime, timedelta, timezone
import boto3
import json

def lambda_handler(event, context):
    sport_data_api_key = os.getenv("SPORTS_DATA_API_KEY")
    sns_arn = os.getenv("SNS_TOPIC_ARN")

    # get the game data from sport data api
    def get_game_data():
        """Fetch game data from sports data API"""
        utc_now = datetime.now(timezone.utc)
        central_time = utc_now - timedelta(hours=5)
        today_date = central_time.strftime("%Y-%m-%d")

        try:
            print(f"Fetching game data for {today_date}")

            url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{today_date}?key={sport_data_api_key}"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            return data
        except Exception as e:
            print(f'Error while fetching game data: {e}')
            return None

    # format the game data
    def format_game_data(data):
        """Format game data for notification"""
        if not data:
            return None

        status = data.get("Status", "Unknown")
        away_team = data.get("AwayTeam", "Unknown")
        home_team = data.get("HomeTeam", "Unknown")
        final_score = f"{data.get('AwayTeamScore', 'N/A')}-{data.get('HomeTeamScore', 'N/A')}"
        start_time = data.get("DateTime", "Unknown")
        channel = data.get("Channel", "Unknown")

        # Format quarters
        quarters = data.get("Quarters", [])
        quarter_scores = ', '.join([f"Q{q['Number']}: {q.get('AwayScore', 'N/A')}-{q.get('HomeScore', 'N/A')}" for q in quarters])

        base_message = (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Channel: {channel}\n"
        )

        if status == "Final":
            return base_message + f"Final Score: {final_score}\nStart Time: {start_time}\nQuarter Scores: {quarter_scores}\n"

        elif status == "InProgress":
            last_play = data.get("LastPlay", "N/A") if data else "N/A"
            return base_message + f"Current Score: {final_score}\nLast Play: {last_play}\n"

        elif status == "Scheduled":
            return base_message + f"Start Time: {start_time}\n"

        else:
            return base_message + "Details are unavailable at the moment.\n"

    # publish to sns topic
    def publish_to_sns(message):
        """Publish the message to SNS topic"""
        sns_client = boto3.client(
            'sns',
            region_name=os.getenv('AWS_DEFAULT_REGION') or 'us-east-1',
        )
        try:
            response = sns_client.publish(
                TopicArn=sns_arn,
                Message=message,
                Subject="NBA Game Day Notification"
            )

            print("Published message to SNS topic successfully.")
        except Exception as e:
            print(f"Error while publishing to SNS: {e}")

    # main function
    game_data = get_game_data()
    messages = [format_game_data(game) for game in game_data]
    final_message = "\n---\n".join(messages) if messages else "No games available for today."

    publish_to_sns(final_message)