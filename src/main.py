#!/usr/bin/env python3
from pathlib import Path
from nicegui import ui
from data import load_skaters_data, find_player, get_all_game_scores, get_all_player_names
from stats import calculate_percentile, get_rating, get_rating_color

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

answer_label = None
percentile_label = None
bar_label = None


def submit_question():
    player_name = player_input.value

    if not player_name:
        show_answer("Please enter a player name", None)
        return

    player = find_player(skaters, player_name)

    if not player:
        show_answer(f"Player '{player_name}' not found", None)
        return

    player_game_score = float(player['gameScore'])
    percentile = calculate_percentile(player_game_score, all_game_scores)
    rating = get_rating(percentile)

    show_answer(rating, percentile)


def show_answer(text, percentile):
    global answer_label, percentile_label, bar_label

    # Update existing labels instead of clearing
    answer_label.set_text(f'Answer: {text}')

    if percentile is not None:
        percentile_label.set_text(f'({percentile:.1f}th percentile)')

        # ASCII progress bar
        bar_length = 50
        filled = int((percentile / 100) * bar_length)
        bar = '▓' * filled + '░' * (bar_length - filled)
        bar_label.set_text(bar)
    else:
        percentile_label.set_text('')
        bar_label.set_text('')


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

    # Pre-create answer elements to prevent layout shift
    answer_label = ui.label('').style('color: black; margin-top: 20px; min-height: 20px;')
    percentile_label = ui.label('').style('color: black; margin-top: 5px; min-height: 20px;')
    bar_label = ui.label('').style('color: black; margin-top: 10px; letter-spacing: 1px; min-height: 20px; font-family: monospace; white-space: pre;')

ui.run()
