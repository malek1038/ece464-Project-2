# Slight ChatGPT use nothing major, mostly debugging and small adjustments
from pymongo import MongoClient

# Function to get the database connection
def get_database():
    # Connect to MongoDB (adjust to match yours if you decide to run it)
    client = MongoClient('mongodb://localhost:27017/')

    # Select the database
    db = client["nba_stats_db"]

    return db

# Function to get the players collection
def get_players_collection():
    db = get_database()
    return db["players"]
