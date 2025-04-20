import json
import random
from pathlib import Path

DATA_PATH = Path("player_data.json")

# === 🔧 Spieler-Daten laden/speichern ===
def load_players():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_players(players):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=2, ensure_ascii=False)

# === 🔁 Spieler hinzufügen/updaten/löschen ===
def add_or_update_player(name, value):
    players = load_players()
    players[name] = value
    save_players(players)

def remove_player(name):
    players = load_players()
    if name in players:
        del players[name]
        save_players(players)

# === ⚽ Team-Logik ===
def team_strength(team, player_points):
    return sum(player_points[p] for p in team)

def calculate_variance(teams, player_points):
    scores = [team_strength(team, player_points) for team in teams]
    return max(scores) - min(scores)

def generate_one_team_distribution(players, player_points, num_teams, team_size):
    random.shuffle(players)
    teams = [[] for _ in range(num_teams)]

    for player in players:
        eligible_teams = [t for t in teams if len(t) < team_size]
        if not eligible_teams:
            break
        weakest_team = min(eligible_teams, key=lambda t: team_strength(t, player_points))
        weakest_team.append(player)

    return teams

def generate_multiple_distributions(selected_players, num_teams, team_size=5, trials=100, top_n=3):
    player_points = load_players()
    all_distributions = []

    for _ in range(trials):
        players_copy = selected_players.copy()
        teams = generate_one_team_distribution(players_copy, player_points, num_teams, team_size)
        variance = calculate_variance(teams, player_points)
        all_distributions.append((variance, teams))

    all_distributions.sort(key=lambda x: x[0])
    return all_distributions[:top_n]
