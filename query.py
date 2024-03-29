from pymongo import MongoClient
import random

def get_database():
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    return client['nba_stats_db']

def get_team_players(team_name):
    db = get_database()
    players = db.players.find({"team": {"$regex": team_name, "$options": "i"}})
    return list(players)

def calculate_offensive_score(team_name):
    players = get_team_players(team_name)
    if not players:
        print("Team not found or no players data available.")
        return

    total_points = 0
    total_rebounds = 0
    total_assists = 0
    total_players = len(players)

    for player in players:
        stats = player.get("stats", {})
        total_points += float(stats.get("PPG", 0))
        total_rebounds += float(stats.get("RPG", 0))
        total_assists += float(stats.get("APG", 0))

    avg_points = total_points / total_players
    avg_rebounds = total_rebounds / total_players
    avg_assists = total_assists / total_players

    # Weights: You can adjust these weights based on your analysis
    weights = {"PPG": 0.6, "RPG": 0.2, "APG": 0.2}
    offensive_score = (avg_points * weights["PPG"]) + (avg_rebounds * weights["RPG"]) + (avg_assists * weights["APG"])

    # Normalize the score to a scale of 100
    # Assuming the maximum average score for points, rebounds, and assists is 30, 15, and 10 respectively
    max_score = (28 * weights["PPG"]) + (12 * weights["RPG"]) + (8 * weights["APG"])
    offensive_score_normalized = (offensive_score / max_score) * 100

    return offensive_score_normalized

def simulate_game_stats(team_name):
    players = get_team_players(team_name)
    team_offensive_score = calculate_offensive_score(team_name)
    print(f"Team Offensive Score: {team_offensive_score:.2f}")

    team_totals = {"Points": 0, "Rebounds": 0, "Assists": 0}
    game_stats = []

    for player in players:
        stats = player.get("stats", {})
        ppg = float(stats.get("PPG", 0))
        rpg = float(stats.get("RPG", 0))
        apg = float(stats.get("APG", 0))

        # Adjust player stats based on team's offensive score and add randomness
        points = round(random.uniform(0.8, 1.2) * 2.5 * ppg * (team_offensive_score / 100))
        rebounds = round(random.uniform(0.8, 1.2) * 2.5 * rpg * (team_offensive_score / 100))
        assists = round(random.uniform(0.8, 1.2) * 2.5 * apg * (team_offensive_score / 100))

        player_game_stats = {
            "Name": player["name"],
            "Points": points,
            "Rebounds": rebounds,
            "Assists": assists
        }
        game_stats.append(player_game_stats)

        team_totals["Points"] += points
        team_totals["Rebounds"] += rebounds
        team_totals["Assists"] += assists

    return game_stats, team_totals

def player_lookup(name):
    db = get_database()
    player = db.players.find_one({"name": {"$regex": name, "$options": "i"}})
    if player:
        print(f"Stats for {player['name']} | {player['team']}:")
        for stat, value in player['stats'].items():
            print(f"{stat}: {value}")
    else:
        print("Player not found.")

def player_lookup_no_print(name):
    db = get_database()
    player = db.players.find_one({"name": {"$regex": name, "$options": "i"}})
    if player:
        return player['stats']  # Return the entire stats dictionary
    else:
        print("Player not found.")
        return None  # Ensure function returns None if player is not found


def player_compare(player1, player2):
    player1_stats = player_lookup_no_print(player1)
    player2_stats = player_lookup_no_print(player2)
    if player1_stats and player2_stats:  # Check that both are not None
        print(f"\nComparing {player1} and {player2}:\n")
        print(f"{'Stat':<20} {player1:<20} {player2:<20}")
        print("-" * 60)
        for stat in player1_stats.keys():  # Iterate over the keys of player1_stats
            value1 = player1_stats.get(stat, "N/A")
            value2 = player2_stats.get(stat, "N/A")
            print(f"{stat:<20} {value1:<20} {value2:<20}")
    else:
        print("One or more players not found.")


def top_players(stat, n=5):
    db = get_database()
    players = db.players.find().sort(f"stats.{stat}", -1).limit(n)
    print(f"Top {n} players in {stat}:")
    for player in players:
        print(f"{player['name']} ({player['team']}): {player['stats'].get(stat, 'N/A')}")

def main():
    while True:
        # Display the options to the user
        print("\nPlease choose an option (enter the number):")
        print("1 - Player Lookup")
        print("2 - Player Comparison")
        print("3 - Top 5 Players by PPG")
        print("4 - Top 5 Players by RPG")
        print("5 - Top 5 Players by APG")
        print("6 - Top 5 Players by PIE")
        print("7 - Calculate Offensive Score for a Team")
        print("8 - Calculate Points for a Game For a Team")
        print("9 - Simulate a Game")
        print("0 - Exit")

        # Get user input
        choice = input("Your choice: ")

        # Process the user's choice
        if choice == "1":
            name = input("Enter player's name: ")
            player_lookup(name)
        elif choice == "2":
            player1 = input("Enter first player's name: ")
            player2 = input("Enter second player's name: ")
            player_compare(player1, player2)
        elif choice == "3":
            top_players("PPG")
        elif choice == "4":
            top_players("RPG")
        elif choice == "5":
            top_players("APG")
        elif choice == "6":
            top_players("PIE")
        elif choice == "7":
            team = input("Enter team name: ")
            offensive_score = calculate_offensive_score(team)
            if offensive_score:
                print(f"Offensive Score for {team}: {offensive_score:.2f}")
        elif choice == "8":
            team = input("Enter team name: ")
            game_stats, team_totals = simulate_game_stats(team)
            print("\nGame Stats:")
            print(team_totals)
            print("\nIndividual Player Stats:")
            for player_stats in game_stats:
                print(player_stats)
        elif choice == "9":
            team1 = input("Enter first team name: ")
            team2 = input("Enter second team name: ")
            game1_stats, game1_totals = simulate_game_stats(team1)
            game2_stats, game2_totals = simulate_game_stats(team2)

            # Print final scores
            print(f"{team1}: {game1_totals['Points']} vs {game2_totals['Points']} {team2}")

            # Determine and print the winner
            if game1_totals['Points'] > game2_totals['Points']:
                print(f"{team1} wins!")
            elif game1_totals['Points'] < game2_totals['Points']:
                print(f"{team2} wins!")
            else:  # Tiebreaker
                tiebreaker1 = game1_totals['Assists'] + game1_totals['Rebounds']
                tiebreaker2 = game2_totals['Assists'] + game2_totals['Rebounds']
                
                if tiebreaker1 > tiebreaker2:
                    print(f"{team1} wins by tiebreaker!")
                    game1_totals['Points'] += 1  # Adjusting score for the win
                elif tiebreaker1 < tiebreaker2:
                    print(f"{team2} wins by tiebreaker!")
                    game2_totals['Points'] += 1  # Adjusting score for the win
                else:
                    # Random choice in case everything is tied
                    winner = random.choice([team1, team2])
                    print(f"{winner} wins by random decision!")
                    if winner == team1:
                        game1_totals['Points'] += 1
                    else:
                        game2_totals['Points'] += 1

            # Print adjusted final score if there was a tiebreaker or random decision
            if game1_totals['Points'] == game2_totals['Points']:
                print(f"Adjusted Final Score: {team1}: {game1_totals['Points']} vs {game2_totals['Points']} {team2}")


        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()
