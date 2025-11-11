#!/usr/bin/env python3
from pathlib import Path
from nicegui import ui
from data import load_skaters_data, find_player, get_all_game_scores, get_all_player_names, get_player_criteria_stats, get_all_criteria_values
from stats import calculate_percentile, get_grade, calculate_criteria_percentiles

# Plain text styling
ui.add_head_html('''
<style>
    * {
        font-family: 'Courier New', monospace;
    }
    body {
        background-color: white;
    }
    input {
        text-decoration: underline;
        font-weight: bold !important;
    }
    input::placeholder {
        color: #d0d0d0;
        opacity: 1;
    }
</style>
''')

# Load data once at startup
DATA_FILE = Path(__file__).parent.parent / 'data' / '2024-2025-skaters.csv'
skaters = load_skaters_data(DATA_FILE)
all_game_scores = get_all_game_scores(skaters)
all_player_names = get_all_player_names(skaters)
all_criteria_values = get_all_criteria_values(skaters)

result_container = None


def submit_question():
    player_name = player_input.value

    if not player_name:
        show_error("Please enter a player name")
        return

    player = find_player(skaters, player_name)

    if not player:
        show_error(f"Player '{player_name}' not found")
        return

    # Calculate overall grade from gameScore
    player_game_score = float(player['gameScore'])
    percentile = calculate_percentile(player_game_score, all_game_scores)
    grade = get_grade(percentile)

    # Calculate criteria breakdown
    player_stats = get_player_criteria_stats(player)
    criteria_percentiles = calculate_criteria_percentiles(player_stats, all_criteria_values)

    show_answer(grade, percentile, criteria_percentiles)


def show_error(message):
    global result_container
    result_container.clear()
    with result_container:
        ui.label(message).style('color: black; margin-top: 20px;')


def show_answer(grade, percentile, criteria_percentiles):
    global result_container

    result_container.clear()

    with result_container:
        # Overall goodness
        ui.label(f'Overall goodness: {grade} ({percentile:.1f}th percentile)').style('color: black; margin-top: 20px; font-weight: bold;')

        # Criteria breakdown
        criteria_order = [
            ('scoring', 'Scoring'),
            ('shooting', 'Shooting'),
            ('playmaking', 'Playmaking'),
            ('defense', 'Defense'),
            ('physicality', 'Physicality'),
            ('possession', 'Possession')
        ]

        for key, label in criteria_order:
            pct = criteria_percentiles[key]
            bar_length = 20
            filled = int((pct / 100) * bar_length)
            empty = bar_length - filled
            bar = '█' * filled + '░' * empty
            grade_letter = get_grade(pct)

            with ui.row().classes('items-center').style('gap: 2px; margin-bottom: -8px;'):
                ui.label(label).style('color: black; width: 100px;')
                ui.label(bar).style('color: black;')
                ui.label(grade_letter).style('color: black;')


# Main layout - simple, left-aligned
with ui.column().style('width: 800px; margin: 50px auto; padding: 20px;'):
    # Title is the question itself
    with ui.row().classes('items-center gap-1').style('margin-bottom: 10px;'):
        ui.label('Is').style('color: black; font-weight: bold;')

        player_input = ui.input(placeholder='player name', autocomplete=all_player_names)
        player_input.props('borderless').style('border: none; padding: 2px 4px; width: 200px;')
        player_input.on('keydown.enter', submit_question)

        ui.label('a good hockey player?').style('color: black; font-weight: bold;')

    submit_label = ui.label('submit').style('color: black; text-decoration: underline; cursor: pointer;')
    submit_label.on('click', submit_question)

    # Container for results
    result_container = ui.column()

ui.run()
