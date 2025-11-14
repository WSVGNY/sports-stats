"""Data loading and player lookup functions."""
import csv


def load_skaters_data(filepath, min_icetime_minutes=500):
    """Load skater data from CSV file, filtering to 'all' situation only.

    Args:
        filepath: Path to CSV file
        min_icetime_minutes: Minimum ice time in minutes to include player (default: 500)
                            This filters out small sample sizes that can skew statistics.
    """
    skaters = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include rows where situation is 'all' to avoid duplicates
            if row['situation'] == 'all':
                icetime_seconds = float(row['icetime'])
                icetime_minutes = icetime_seconds / 60
                # Filter by minimum ice time to avoid small sample size issues
                if icetime_minutes >= min_icetime_minutes:
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


def get_player_criteria_stats(player):
    """Extract the 6 criteria statistics for a player."""
    icetime_seconds = float(player['icetime'])
    icetime_minutes = icetime_seconds / 60  # Convert from seconds to minutes

    # Defense: return dict with three components for percentile calculation
    # Component 1: onIce_xGoalsPercentage (possession/dominance)
    # Component 2: Takeaways per 60 (active defense)
    # Component 3: Blocks per 60 (shot blocking)
    xg_pct = float(player['onIce_xGoalsPercentage']) * 100  # Convert to percentage

    if icetime_minutes > 0:
        takeaways = float(player['I_F_takeaways'])
        takeaways_p60 = (takeaways / icetime_minutes) * 60

        blocks = float(player['shotsBlockedByPlayer'])
        blocks_p60 = (blocks / icetime_minutes) * 60
    else:
        takeaways_p60 = 0
        blocks_p60 = 0

    # Store as dict for multi-component percentile calculation
    defense_components = {
        'xg_pct': xg_pct,
        'takeaways_p60': takeaways_p60,
        'blocks_p60': blocks_p60
    }

    return {
        'scoring': float(player['I_F_points']),
        'shooting': float(player['I_F_highDangerxGoals']),
        'playmaking': float(player['I_F_primaryAssists']),
        'defense': defense_components,  # Dict with 3 components
        'physicality': float(player['I_F_hits']) + blocks_p60 * icetime_minutes / 60,  # Total hits + blocks
        'possession': float(player['onIce_corsiPercentage']) * 100  # Convert to percentage
    }


def get_all_criteria_values(skaters):
    """Get all values for each criterion across all players."""
    all_criteria = {
        'scoring': [],
        'shooting': [],
        'playmaking': [],
        'defense': {
            'xg_pct': [],
            'takeaways_p60': [],
            'blocks_p60': []
        },
        'physicality': [],
        'possession': []
    }

    for skater in skaters:
        stats = get_player_criteria_stats(skater)
        for criterion, value in stats.items():
            if criterion == 'defense':
                # Defense is a dict with 3 components
                all_criteria['defense']['xg_pct'].append(value['xg_pct'])
                all_criteria['defense']['takeaways_p60'].append(value['takeaways_p60'])
                all_criteria['defense']['blocks_p60'].append(value['blocks_p60'])
            else:
                all_criteria[criterion].append(value)

    return all_criteria
