#!/usr/bin/env python3
from pathlib import Path
from nicegui import ui
from data import load_skaters_data, find_player, get_all_points, get_all_player_names
from stats import calculate_percentile, get_rating, get_rating_color


# Load data once at startup
DATA_FILE = Path(__file__).parent / 'data' / '2024-2025-skaters.csv'
skaters = load_skaters_data(DATA_FILE)
all_points = get_all_points(skaters)
all_player_names = get_all_player_names(skaters)

answer_label = None


def submit_question():
    global answer_label
    player_name = player_input.value

    if not player_name:
        show_answer("Please enter a player name", "gray")
        return

    player = find_player(skaters, player_name)

    if not player:
        show_answer(f"Player '{player_name}' not found", "gray")
        return

    player_points = float(player['I_F_points'])
    percentile = calculate_percentile(player_points, all_points)
    rating = get_rating(percentile)
    color = get_rating_color(rating)

    show_answer(rating, color)


def show_answer(text, color):
    global answer_label
    if answer_label is None:
        with center_column:
            answer_label = ui.label(text).style(f'color: {color}; font-size: 2em; font-weight: bold;')
    else:
        answer_label.set_text(text)
        answer_label.style(f'color: {color}; font-size: 2em; font-weight: bold;')


with ui.column().classes('items-center justify-center w-full h-screen'):
    with ui.row().classes('items-center'):
        ui.label('Is').style('font-size: 2.5em; font-weight: bold;')
        player_input = ui.input(autocomplete=all_player_names)
        player_input.style('font-size: 2.5em; font-weight: bold;')
        ui.label('a good hockey player?').style('font-size: 2.5em; font-weight: bold;')

    ui.button('Submit', on_click=submit_question)

    center_column = ui.column().classes('items-center')

ui.run()
