from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    return client['nba_stats_db']

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
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()
