import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Population Growth Predictor", page_icon="🌍", layout="wide")

st.markdown("""
<style>
.main {background-color: #f7fafc;}
.hero {padding: 1.5rem; border-radius: 18px; background: linear-gradient(120deg,#123b5d,#168aad); color: white;}
.hero h1 {color:white; margin-bottom:0.3rem;}
.metric-card {background:white; padding:1rem; border-radius:12px; border:1px solid #dbe5ee;}
</style>
<div class="hero">
<h1>🌍 Population Growth Predictor</h1>
<p>Explore historical population trends and estimate future population with a transparent mathematical model.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.info("Educational prototype: estimates are based on the selected historical data and a simple exponential-growth assumption. They are not official forecasts.")

DEFAULT_DATA = pd.DataFrame({
    "Year": [2000, 2005, 2010, 2015, 2020, 2023],
    "Population": [1050000000, 1140000000, 1230000000, 1320000000, 1390000000, 1428000000]
})

with st.sidebar:
    st.header("⚙️ Prediction settings")
    country = st.text_input("Country / region", "India")
    st.caption("The built-in example data is illustrative. Replace it with verified data for your chosen region.")
    st.subheader("Historical data")
    uploaded = st.file_uploader("Upload CSV (columns: Year, Population)", type=["csv"])
    st.subheader("Prediction")
    forecast_year = st.slider("Predict population for year", min_value=2024, max_value=2100, value=2035)
    method = st.selectbox("Prediction method", ["Exponential growth", "Linear trend"])

def clean_data(df):
    cols = {str(c).strip().lower(): c for c in df.columns}
    if "year" not in cols or "population" not in cols:
        raise ValueError("CSV must contain columns named Year and Population.")
    out = df[[cols["year"], cols["population"]]].copy()
    out.columns = ["Year", "Population"]
    out["Year"] = pd.to_numeric(out["Year"], errors="coerce")
    out["Population"] = pd.to_numeric(out["Population"], errors="coerce")
    out = out.dropna().sort_values("Year").drop_duplicates("Year")
    out = out[(out["Population"] > 0)]
    if len(out) < 2:
        raise ValueError("Please provide at least two valid year/population rows.")
    return out

try:
    data = clean_data(pd.read_csv(uploaded)) if uploaded else DEFAULT_DATA.copy()
    if uploaded is None:
        st.warning("Using built-in example values for India. For a real project submission, upload a verified CSV dataset.")
except Exception as e:
    st.error(str(e))
    st.stop()

first_year = int(data["Year"].min())
last_year = int(data["Year"].max())
if forecast_year <= last_year:
    st.warning(f"The selected prediction year should be later than the latest data year ({last_year}).")
    st.stop()

x = data["Year"].to_numpy(dtype=float)
y = data["Population"].to_numpy(dtype=float)
target = float(forecast_year)

if method == "Exponential growth":
    slope, intercept = np.polyfit(x, np.log(y), 1)
    predicted = float(np.exp(intercept + slope * target))
    growth_rate = (np.exp(slope) - 1) * 100
    formula_note = "Fits a straight line to log(population), then extrapolates exponentially."
else:
    slope, intercept = np.polyfit(x, y, 1)
    predicted = float(intercept + slope * target)
    predicted = max(0, predicted)
    growth_rate = (slope / np.mean(y)) * 100
    formula_note = "Fits a straight line to population versus year, then extrapolates linearly."

c1, c2, c3 = st.columns(3)
c1.metric("Latest recorded population", f"{y[-1]:,.0f}", f"{last_year}")
c2.metric(f"Estimated population in {forecast_year}", f"{predicted:,.0f}")
c3.metric("Approx. annual growth", f"{growth_rate:.2f}%")

left, right = st.columns([1.6, 1])
with left:
    st.subheader("📈 Historical data and projection")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(x, y, marker="o", linewidth=2, label="Historical data")
    future_years = np.arange(last_year, forecast_year + 1)
    if method == "Exponential growth":
        future_pop = np.exp(intercept + slope * future_years)
    else:
        future_pop = np.maximum(0, intercept + slope * future_years)
    ax.plot(future_years, future_pop, linestyle="--", marker=".", label="Model projection")
    ax.axvline(last_year, linestyle=":", linewidth=1)
    ax.set_xlabel("Year")
    ax.set_ylabel("Population")
    ax.set_title(f"{country.strip() or 'Selected region'}: population trend")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("🧾 Model details")
    st.write(f"**Region:** {country.strip() or 'Not specified'}")
    st.write(f"**Historical period:** {first_year}–{last_year}")
    st.write(f"**Method:** {method}")
    st.write(formula_note)
    st.write("**Interpretation:** This is a mathematical extrapolation, not a guarantee of future population.")
    st.download_button("Download cleaned data (CSV)", data.to_csv(index=False).encode("utf-8"), file_name="population_data_cleaned.csv", mime="text/csv")

st.subheader("📋 Historical population table")
display_data = data.copy()
display_data["Population"] = display_data["Population"].map(lambda v: f"{v:,.0f}")
st.dataframe(display_data, use_container_width=True, hide_index=True)

st.subheader("🧪 Try your own dataset")
st.write("Upload a CSV containing two columns named `Year` and `Population`. Example:")
st.code("Year,Population\n2000,1050000000\n2005,1140000000\n2010,1230000000", language="csv")

st.caption("Population Growth Prediction Project • Built with Python, Streamlit, Pandas, NumPy and Matplotlib")
