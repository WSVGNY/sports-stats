"""Data loading and player lookup functions."""
import csv


def load_skaters_data(filepath):
    """Load skater data from CSV file."""
    skaters = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            skaters.append(row)
    return skaters


def find_player(skaters, player_name):
    """Find a player by name (case-insensitive partial match)."""
    player_name_lower = player_name.lower().strip()

    for skater in skaters:
        if player_name_lower in skater['name'].lower():
            return skater

    return None


def get_all_points(skaters):
    """Get list of all players' points."""
    points_list = []
    for skater in skaters:
        points = float(skater['I_F_points'])
        points_list.append(points)
    return points_list


def get_all_player_names(skaters):
    """Get list of all unique player names."""
    names = set()
    for skater in skaters:
        names.add(skater['name'])
    return sorted(names)
