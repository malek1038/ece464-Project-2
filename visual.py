import matplotlib.pyplot as plt
import pandas as pd
from query import get_database, simulate_game_stats

def plot_top_players(stat, n=5):
    db = get_database()
    # Find top players in the stat
    players_data = db.players.find().sort(f"stats.{stat}", -1).limit(n)
    players_list = list(players_data)
    
    # Convert to DataFrame for easier plotting ( I dont completely understand why, but chatGPT said it was necessary and who am I to argue with a computer?)
    df = pd.DataFrame(players_list)
    df['player_stat'] = df['stats'].apply(lambda x: x.get(stat, 'N/A'))

    # Plotting
    df.plot(kind='bar', x='name', y='player_stat', color='blue')
    plt.title(f'Top {n} Players by {stat}')
    plt.xlabel('Player')
    plt.ylabel(stat)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjusts subplots to fit
    plt.show()

def simulate_and_plot_stats(team_name, num_games=10):
    aggregated_stats = {}
    for _ in range(num_games):
        # Simulate game stats and aggregate them
        game_stats, _ = simulate_game_stats(team_name)
        for player_stats in game_stats:
            player_name = player_stats['Name']
            if player_name not in aggregated_stats:
                aggregated_stats[player_name] = {'Points': 0, 'Rebounds': 0, 'Assists': 0}
            aggregated_stats[player_name]['Points'] += player_stats['Points']
            aggregated_stats[player_name]['Rebounds'] += player_stats['Rebounds']
            aggregated_stats[player_name]['Assists'] += player_stats['Assists']
    
    # Creating DataFrames for pie charts
    points_df = pd.DataFrame.from_dict(aggregated_stats, orient='index', columns=['Points'])
    rebounds_df = pd.DataFrame.from_dict(aggregated_stats, orient='index', columns=['Rebounds'])
    assists_df = pd.DataFrame.from_dict(aggregated_stats, orient='index', columns=['Assists'])
    
    # Plotting (ChatGPT basically did this whole part)
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    
    points_df.plot(kind='pie', y='Points', ax=axs[0], autopct='%1.1f%%', startangle=140, legend=None)
    axs[0].set_ylabel('')
    axs[0].set_title(f'{team_name} Points Distribution')
    
    rebounds_df.plot(kind='pie', y='Rebounds', ax=axs[1], autopct='%1.1f%%', startangle=140, legend=None)
    axs[1].set_ylabel('')
    axs[1].set_title(f'{team_name} Rebounds Distribution')
    
    assists_df.plot(kind='pie', y='Assists', ax=axs[2], autopct='%1.1f%%', startangle=140, legend=None)
    axs[2].set_ylabel('')
    axs[2].set_title(f'{team_name} Assists Distribution')
    
    plt.tight_layout()
    plt.show()

def plot_mvp_scores():
    # Get all players
    db = get_database()
    players_collection = db.players
    players_data = players_collection.find({})

    player_names = []
    mvp_scores = []

    # Calculate MVP score for each player
    for player in players_data:
        stats = player['stats']
        ppg = float(stats.get('PPG', 0))
        rpg = float(stats.get('RPG', 0))
        apg = float(stats.get('APG', 0))
        # You can change these, but this is something that gave me results that made sense
        weights = [0.5, 0.3, 0.2]
        mvp_score = ppg * weights[0] + rpg * weights[1] + apg * weights[2]
        player_names.append(player['name'])
        mvp_scores.append(mvp_score)

    # Convert to DataFrame
    df = pd.DataFrame({
        'Player': player_names,
        'MVP Score': mvp_scores
    }).sort_values(by='MVP Score', ascending=False)

    # Plotting
    plt.figure(figsize=(10, 50))
    plt.barh(df['Player'][:20], df['MVP Score'][:20], color='skyblue') # Top 20 players
    plt.xlabel('MVP Score')
    plt.title('Top 20 Players by MVP Score')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest score on top
    plt.tight_layout()
    plt.show()

def main_visual():
    # Example: Plot top 5 players by PPG
    plot_top_players('PPG', 5)
    simulate_and_plot_stats('Dallas Mavericks', num_games=10)
    simulate_and_plot_stats('New York Knicks', num_games=10)
    simulate_and_plot_stats('Brooklyn Nets', num_games=10)
    plot_mvp_scores()

if __name__ == "__main__":
    main_visual()
