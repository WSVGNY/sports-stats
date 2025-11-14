# NHL Player Stats

Static web app for evaluating NHL players across 6 criteria: scoring, shooting, playmaking, defense, physicality, and possession.

## Run Locally

```bash
cd static_site
python3 -m http.server 8000
```

Open http://localhost:8000

## Deploy

Deploy the `static_site/` directory to any static host:

- **Netlify**: Drag `static_site/` folder to https://app.netlify.com/drop
- **GitHub Pages**: Push `static_site/` contents and enable Pages in repo settings
- **Vercel/Cloudflare Pages**: Deploy the `static_site/` directory

## Update Data

When you have new NHL stats:

```bash
# 1. Replace the CSV file
cp new-stats.csv data/2024-2025-skaters.csv

# 2. Rebuild static data
python3 build_static_data.py

# 3. Deploy the updated static_site/ folder
```
