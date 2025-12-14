# Is X a good hockey player?

This website gives the answer, at last.

Evaluate NHL players based on 2024-2025 season statistics and compare them side-by-side.

## Features

- **Player Evaluation**: Search for any NHL player and see their performance grades across 6 categories
- **Player Comparison**: Compare up to 4 players side-by-side with differential indicators
- **Shareable Links**: URL parameters allow sharing specific player views and comparisons
- **Responsive Design**: Works on desktop and mobile with a clean monospace aesthetic

## Run Locally

```bash
cd docs
python3 -m http.server 8000
```

Open http://localhost:8000

## Usage

### Single Player Lookup
1. Type a player name in the search box
2. Select from autocomplete suggestions
3. View their performance grades

### Compare Players
1. Search for a player and click **"+ Add to comparison"**
2. Search for another player and add them too
3. View side-by-side comparison with performance differentials
4. Share the comparison using the URL (automatically updated)

Example comparison URL:
```
http://localhost:8000/?player=connor-mcdavid&compare=auston-matthews,nathan-mackinnon
```

## Update Data

When you have new NHL stats:

```bash
# 1. Replace the CSV file
cp new-stats.csv data/2024-2025-skaters.csv

# 2. Rebuild static data
python3 build_static_data.py

# 3. Deploy the updated static_site/ folder
```
