# NYC Airbnb Sample Dashboard

A Streamlit dashboard for exploring the NYC Airbnb 2019 dataset with interactive filters, visualizations, and a modular code structure.

## Features

- **Interactive Filters**: Filter by borough, room type, price range, minimum nights, and availability
- **Multiple Visualizations**:
  - Price distribution histogram
  - Borough price comparison (median/mean)
  - Interactive map with hover tooltips
  - Price vs availability scatter plot
  - Top neighborhoods table
  - Filtered listings table
- **Two-Tab Interface**: Overview and Map + Drilldown sections
- **Modular Code Structure**: Organized into separate modules for data, state, filters, and charts

## Project Structure

```
airbnb_streamlit_sample/
├── app.py                 # Main Streamlit application
├── src/
│   ├── data.py           # Data loading and preprocessing
│   ├── state.py          # Session state management
│   ├── filters.py        # Filter UI and logic
│   └── charts.py         # Visualization functions
├── data/
│   └── AB_NYC_2019.csv   # Dataset
└── requirements.txt       # Python dependencies
```

## Installation

## Prerequisites
- Python 3.11+
- Git (optional)

Check Python:
```bash
python3 --version
```

Option A: Run with Poetry (recommended)

1. Install pipx
```bash
brew install pipx
pipx ensurepath
exec $SHELL -l
```

2. Install Poetry
```bash
pipx install poetry
```

If Poetry was previously installed via Homebrew:
```bash
brew unlink poetry || true
hash -r
```

3. Install dependencies
```bash
poetry install
```

4. Run the app
```bash
poetry run streamlit run app.py
```

Option B: Run without Poetry (pip only)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Dataset

This dashboard uses the [NYC Airbnb Open Data (2019)](https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data) dataset, which includes information about Airbnb listings in New York City.

## Technologies

- **Streamlit**: Interactive web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computing

## Deployment (Streamlit Community Cloud)

Streamlit Cloud typically installs from `requirements.txt`. If you're developing with Poetry, you can export a compatible file before deploying:

```bash
poetry export -f requirements.txt --without-hashes -o requirements.txt
```

Then push your repo and point Streamlit Cloud at `app.py`.