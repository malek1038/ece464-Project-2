import requests
from bs4 import BeautifulSoup
import json

# Example list of team IDs
team_ids = ["1610612738", "1610612751", "1610612752", "1610612755", "1610612761", "1610612741", "1610612739", "1610612765", "1610612754", "1610612749",
             "1610612737", "1610612766", "1610612748", "1610612753", "1610612764", "1610612743", "1610612750", "1610612760", "1610612757", "1610612762",
               "1610612744", "1610612746", "1610612747", "1610612756", "1610612758", "1610612742", "1610612745", "1610612763", "1610612740", "1610612759"]

def fetch_player_ids_for_team(team_id):
    url = f"https://www.nba.com/team/{team_id}"
    response = requests.get(url)
    player_ids = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
        
        if script_tag:
            data = json.loads(script_tag.string)  # Load the JSON data from the <script> tag
            roster = data['props']['pageProps']['team']['roster']
            
            for player in roster:
                player_ids.append(player['PLAYER_ID'])
                
    else:
        print(f"Failed to fetch data for team ID {team_id}. Status code: {response.status_code}")
    
    return player_ids

# List to hold all player IDs across all teams
all_player_ids = []

# Loop through each team ID and fetch the player IDs, then extend the master list
for team_id in team_ids:
    player_ids = fetch_player_ids_for_team(team_id)
    all_player_ids.extend(player_ids)

# Print the complete list of player IDs
print(all_player_ids)
print(len(all_player_ids))
