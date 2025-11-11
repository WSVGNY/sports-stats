"""Data loading and player lookup functions."""
import csv


def load_skaters_data(filepath):
    """Load skater data from CSV file, filtering to 'all' situation only."""
    skaters = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include rows where situation is 'all' to avoid duplicates
            if row['situation'] == 'all':
                skaters.append(row)
    return skaters


def find_player(skaters, player_name):
    """Find a player by name (case-insensitive partial match)."""
    player_name_lower = player_name.lower().strip()

    for skater in skaters:
        if player_name_lower in skater['name'].lower():
            return skater

    return None


def get_all_game_scores(skaters):
    """Get list of all players' game scores."""
    scores_list = []
    for skater in skaters:
        score = float(skater['gameScore'])
        scores_list.append(score)
    return scores_list


def get_all_player_names(skaters):
    """Get list of all unique player names."""
    names = set()
    for skater in skaters:
        names.add(skater['name'])
    return sorted(names)
