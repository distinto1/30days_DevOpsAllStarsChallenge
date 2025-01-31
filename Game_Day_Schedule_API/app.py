from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

SERP_API_URL = "https://serpapi.com/search.json"
SERP_API_KEY = os.getenv("SERP_API_KEY")  # Fixed environment variable name

@app.route('/nfl-schedule', methods=['GET'])  # More specific endpoint
def get_nfl_schedule():
    try:
        params = {
            "engine": "google_events",  # Adjusted engine for events/sports
            "q": "nfl schedule",
            "api_key": SERP_API_KEY,
            "hl": "en"  # Example: Language parameter
        }
        response = requests.get(SERP_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Check for SerpAPI-specific errors (e.g., invalid key)
        if "error" in data:
            return jsonify({"message": data.get("error", "SerpAPI error")}), 500

        games = data.get("sports_results", {}).get("games", [])
        if not games:
            return jsonify({"message": "No NFL schedule found.", "games": []}), 200

        formatted_games = []
        for game in games:
            teams = game.get("teams", [])
            # Find home/away teams using 'type' field
            home_team = next((t.get("name") for t in teams if t.get("type") == "home"), "Unknown")
            away_team = next((t.get("name") for t in teams if t.get("type") == "away"), "Unknown")

            raw_time = game.get("time", "Unknown")
            # Avoid adding " ET" if already present
            time = f"{raw_time} ET" if raw_time != "Unknown" and "ET" not in raw_time else raw_time

            game_info = {
                "away_team": away_team,
                "home_team": home_team,
                "venue": game.get("venue", "Unknown"),
                "date": game.get("date", "Unknown"),
                "time": time
            }
            formatted_games.append(game_info)

        return jsonify({"message": "Success", "games": formatted_games}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"message": "HTTP request failed", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
