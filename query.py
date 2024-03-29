# Slight ChatGPT use nothing major, mostly debugging and small adjustments
import random
from dataBase import get_database

# Given a team name, return a list of players in the team
def get_team_players(team_name):
    db = get_database()
    players = db.players.find({"team": {"$regex": team_name, "$options": "i"}})
    return list(players)

# Given a player's name, looks up the player and prints their stats
def player_lookup(name):
    db = get_database()
    player = db.players.find_one({"name": {"$regex": name, "$options": "i"}})
    if player:
        print(f"Stats for {player['name']} | {player['team']}:")
        for stat, value in player['stats'].items():
            print(f"{stat}: {value}")
    else:
        print("Player not found.")

# Same as above, but doesnt print, used for comparison
def player_lookup_no_print(name):
    db = get_database()
    player = db.players.find_one({"name": {"$regex": name, "$options": "i"}})
    if player:
        return player['stats']  # Return the entire stats dictionary
    else:
        print("Player not found.")
        return None  # Return None if player not found

# Given two player names, compares their stats
def player_compare(player1, player2):
    player1_stats = player_lookup_no_print(player1)
    player2_stats = player_lookup_no_print(player2)
    if player1_stats and player2_stats:  # Check that both are not None
        # Shout out to chatGPT for the formatting idea
        print(f"\nComparing {player1} and {player2}:\n")
        print(f"{'Stat':<20} {player1:<20} {player2:<20}")
        print("-" * 60)
        for stat in player1_stats.keys():  # Iterate over the keys of one player (since they have the same stats)
            value1 = player1_stats.get(stat, "N/A")
            value2 = player2_stats.get(stat, "N/A")
            print(f"{stat:<20} {value1:<20} {value2:<20}")
    else:
        print("One or more players not found.")

# Given a team name, calculate the offensive score for the team
def calculate_offensive_score(team_name):
    players = get_team_players(team_name)
    if not players:
        print("Team not found or no players data available.")
        return

    total_points = 0
    total_rebounds = 0
    total_assists = 0
    total_players = len(players)

    # Calculate the average points, rebounds, and assists for the team
    for player in players:
        stats = player.get("stats", {})
        total_points += float(stats.get("PPG", 0))
        total_rebounds += float(stats.get("RPG", 0))
        total_assists += float(stats.get("APG", 0))

    avg_points = total_points / total_players
    avg_rebounds = total_rebounds / total_players
    avg_assists = total_assists / total_players

    # You can adjust these but I got the most "realistic" results with these weights (This is very much only my opinion, so feel free to adjust!)
    weights = {"PPG": 0.6, "RPG": 0.2, "APG": 0.2}
    offensive_score = (avg_points * weights["PPG"]) + (avg_rebounds * weights["RPG"]) + (avg_assists * weights["APG"])

    # Normalize the score to a scale of 100
    # Assuming the maximum average score for points, rebounds, and assists is 28, 12, and 8 respectively
    max_score = (28 * weights["PPG"]) + (12 * weights["RPG"]) + (8 * weights["APG"])
    offensive_score_normalized = (offensive_score / max_score) * 100

    return offensive_score_normalized # This score turns out to be slightly redundant, but I kept it because I spent a lot of time on it, most teams score between 29-35

# Given a team name, simulate a game and return the game stats and team totals
def simulate_game_stats(team_name):
    # Yes I understand that basketball is way more complex than this, but since I have no defensive stats, I can't really simulate a game properly, so it is what it is
    # There is a simpler way to do this, without calculating the stats for each player, and instead using team averages, but I use players stats in the visuals so it turned out to be usefull.
    players = get_team_players(team_name)
    team_offensive_score = calculate_offensive_score(team_name)

    team_totals = {"Points": 0, "Rebounds": 0, "Assists": 0}
    game_stats = []

    # Simulate stats for each player
    for player in players:
        stats = player.get("stats", {})
        ppg = float(stats.get("PPG", 0))
        rpg = float(stats.get("RPG", 0))
        apg = float(stats.get("APG", 0))

        # Adjust player stats based on team's offensive score and add randomness
        # (multiplying by 2 gives 90's like stats, 2.2-2.5 is more realistic for today's game)
        # We need to multiply because the offensive score essentially maxes out at like 35 so dividing by 100 gives a low number
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

        # Update team totals
        team_totals["Points"] += points
        team_totals["Rebounds"] += rebounds
        team_totals["Assists"] += assists

    return game_stats, team_totals

# Given a stat, finds the top n players in that stat, default is 5
def top_players(stat, n=5):
    db = get_database()
    players = db.players.find().sort(f"stats.{stat}", -1).limit(n)
    print(f"Top {n} players in {stat}:")
    for player in players:
        print(f"{player['name']} ({player['team']}): {player['stats'].get(stat, 'N/A')}")

def main():
    # Simple text-based menu for user interaction
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
        print("8 - Simulate a Game")
        print("0 - Exit")

        choice = input("Your choice: ")

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
            # This is supposed to simulate a game between two teams
            # What is really does it it simulates the stats for both teams and then compares the totals, this doesn't consider matchups, defense, etc.
            team1 = input("Enter first team name: ")
            team2 = input("Enter second team name: ")
            game1_stats, game1_totals = simulate_game_stats(team1)
            game2_stats, game2_totals = simulate_game_stats(team2)


            # Determine and print the winner
            if game1_totals['Points'] > game2_totals['Points']:
                print(f"{team1} wins!")
                print(f"{team1}: {game1_totals['Points']} vs {game2_totals['Points']} {team2}")
            elif game1_totals['Points'] < game2_totals['Points']:
                print(f"{team2} wins!")
                print(f"{team1}: {game1_totals['Points']} vs {game2_totals['Points']} {team2}")
            else:  # If the scored are tied, it trying to break the tie using assists and rebounds
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
