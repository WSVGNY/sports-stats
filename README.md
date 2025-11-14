# Is _XYZ_ a good hockey player?

This small website gives the answer.

## Run Locally

```bash
cd static_site
python3 -m http.server 8000
```

Open http://localhost:8000

## Update Data

When you have new NHL stats:

```bash
# 1. Replace the CSV file
cp new-stats.csv data/2024-2025-skaters.csv

# 2. Rebuild static data
python3 build_static_data.py

# 3. Deploy the updated static_site/ folder
```
