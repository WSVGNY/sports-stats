#!/usr/bin/env python3
"""Build static JSON data files for the static website."""
import json
from pathlib import Path
from src.data import (
    load_skaters_data,
    get_all_criteria_values,
    get_player_criteria_stats,
    get_all_game_scores
)
from src.stats import (
    calculate_criteria_percentiles,
    calculate_percentile,
    get_grade,
    get_rating
)


def slugify(name):
    """Convert player name to URL-friendly slug."""
    return name.lower().replace(' ', '-').replace('.', '').replace("'", '')


def build_player_data(player, all_criteria_values, all_game_scores):
    """Build complete data object for a single player."""
    # Calculate statistics
    player_stats = get_player_criteria_stats(player)
    percentiles = calculate_criteria_percentiles(player_stats, all_criteria_values)

    # Calculate overall rating from game score
    player_game_score = float(player['gameScore'])
    overall_percentile = calculate_percentile(player_game_score, all_game_scores)
    overall_grade = get_grade(overall_percentile)

    # Build complete player object
    return {
        "name": player['name'],
        "slug": slugify(player['name']),
        "team": player['team'],
        "position": player['position'],
        "games": int(player['games_played']),
        "ice_time_minutes": round(float(player['icetime']) / 60, 1),

        # Overall rating
        "overall_grade": overall_grade,
        "overall_percentile": round(overall_percentile, 1),

        # Category breakdowns with all needed data
        "categories": {
            "scoring": {
                "percentile": round(percentiles['scoring'], 1),
                "grade": get_grade(percentiles['scoring']),
                "rating": get_rating(percentiles['scoring']),
                "value": int(player_stats['scoring']),
                "label": "Points"
            },
            "shooting": {
                "percentile": round(percentiles['shooting'], 1),
                "grade": get_grade(percentiles['shooting']),
                "rating": get_rating(percentiles['shooting']),
                "value": round(player_stats['shooting'], 2),
                "label": "High Danger xGoals"
            },
            "playmaking": {
                "percentile": round(percentiles['playmaking'], 1),
                "grade": get_grade(percentiles['playmaking']),
                "rating": get_rating(percentiles['playmaking']),
                "value": int(player_stats['playmaking']),
                "label": "Primary Assists"
            },
            "defense": {
                "percentile": round(percentiles['defense'], 1),
                "grade": get_grade(percentiles['defense']),
                "rating": get_rating(percentiles['defense']),
                "components": {
                    "xg_pct": round(player_stats['defense']['xg_pct'], 1),
                    "takeaways_p60": round(player_stats['defense']['takeaways_p60'], 2),
                    "blocks_p60": round(player_stats['defense']['blocks_p60'], 2)
                },
                "label": "Defense"
            },
            "physicality": {
                "percentile": round(percentiles['physicality'], 1),
                "grade": get_grade(percentiles['physicality']),
                "rating": get_rating(percentiles['physicality']),
                "value": round(player_stats['physicality'], 1),
                "label": "Hits + Blocks"
            },
            "possession": {
                "percentile": round(percentiles['possession'], 1),
                "grade": get_grade(percentiles['possession']),
                "rating": get_rating(percentiles['possession']),
                "value": round(player_stats['possession'], 1),
                "label": "Corsi %"
            }
        }
    }


def build_index_entry(player_data):
    """Build lightweight index entry for search."""
    return {
        "name": player_data['name'],
        "slug": player_data['slug'],
        "team": player_data['team'],
        "position": player_data['position'],
        "grade": player_data['overall_grade']
    }


def main():
    """Build all static data files."""
    print("Building static data files...")

    # Load source data
    data_file = Path(__file__).parent / 'data' / '2024-2025-skaters.csv'
    print(f"Loading data from {data_file}...")

    skaters = load_skaters_data(data_file)
    all_criteria_values = get_all_criteria_values(skaters)
    all_game_scores = get_all_game_scores(skaters)

    print(f"Processing {len(skaters)} players...")

    # Build data for all players
    all_players_data = []
    index_data = []

    for i, player in enumerate(skaters):
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(skaters)} players...")

        player_data = build_player_data(player, all_criteria_values, all_game_scores)
        all_players_data.append(player_data)
        index_data.append(build_index_entry(player_data))

    # Create output directory
    output_dir = Path(__file__).parent / 'static_data'
    output_dir.mkdir(exist_ok=True)

    # Write index.json (lightweight - for search/autocomplete)
    index_file = output_dir / 'index.json'
    print(f"\nWriting {index_file}...")
    with open(index_file, 'w') as f:
        json.dump(index_data, f, separators=(',', ':'))  # Compact format

    index_size = index_file.stat().st_size
    print(f"  Size: {index_size:,} bytes ({index_size / 1024:.1f} KB)")

    # Write players-full.json (complete data)
    full_file = output_dir / 'players-full.json'
    print(f"\nWriting {full_file}...")
    with open(full_file, 'w') as f:
        json.dump(all_players_data, f, separators=(',', ':'))  # Compact format

    full_size = full_file.stat().st_size
    print(f"  Size: {full_size:,} bytes ({full_size / 1024:.1f} KB, {full_size / 1024 / 1024:.2f} MB)")

    # Also write pretty version for debugging
    debug_file = output_dir / 'players-full-pretty.json'
    print(f"\nWriting {debug_file} (for debugging)...")
    with open(debug_file, 'w') as f:
        json.dump(all_players_data, f, indent=2)

    debug_size = debug_file.stat().st_size
    print(f"  Size: {debug_size:,} bytes ({debug_size / 1024:.1f} KB)")

    print(f"\n✅ Done! Generated {len(all_players_data)} player records")
    print(f"\nOutput files:")
    print(f"  - {index_file} (search index)")
    print(f"  - {full_file} (complete data)")
    print(f"  - {debug_file} (pretty formatted)")

    # Show sample data
    print(f"\n--- Sample player data ---")
    sample = all_players_data[0]
    print(f"Name: {sample['name']}")
    print(f"Team: {sample['team']}, Position: {sample['position']}")
    print(f"Overall: {sample['overall_grade']} ({sample['overall_percentile']}th percentile)")
    print(f"Scoring: {sample['categories']['scoring']['grade']} - {sample['categories']['scoring']['value']} points")


if __name__ == '__main__':
    main()
