# Population Growth Prediction

A Streamlit web app for exploring population trends and projecting a future population from historical data.

## Features
- Upload a CSV with `Year` and `Population` columns
- Choose a future prediction year
- Compare exponential-growth and linear-trend estimates
- View historical data and a projection chart
- Download cleaned data

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy publicly with Streamlit Community Cloud
1. Create/sign in to GitHub.
2. Create a new repository, for example `population-growth-prediction`.
3. Upload `app.py`, `requirements.txt`, and `README.md` to the repository.
4. Open https://share.streamlit.io/ and connect GitHub.
5. Choose the repository, branch `main`, and main file path `app.py`.
6. Click Deploy. Streamlit will provide a public `*.streamlit.app` URL.

## Dataset format
CSV file with headers `Year,Population`, for example:
```csv
Year,Population
2000,1050000000
2005,1140000000
2010,1230000000
```

## Important limitation
The included India values are illustrative example values to demonstrate the interface. Replace them with a verified dataset before presenting the predictions as research results. The model is a simple extrapolation and does not account for policy, migration, fertility changes, or other demographic factors.
