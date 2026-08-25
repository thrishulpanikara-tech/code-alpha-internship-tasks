"""
Task 3+: Interactive Dashboard
------------------------------
Run: streamlit run 04_dashboard.py

Input:  data/books_clean.csv
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "books_clean.csv"

st.set_page_config(
    page_title="Books Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        return None
    df = pd.read_csv(DATA_FILE)
    if "price_num" not in df.columns or "rating_num" not in df.columns:
        df["price_num"] = (
            df["price"].astype(str).str.extract(r"([\d.]+)", expand=False).astype(float)
        )
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        df["rating_num"] = df["rating"].map(rating_map)
    return df


df = load_data()

if df is None:
    st.error("Data not found. Run these first:")
    st.code("python 01_scrape.py\npython 02_eda.py")
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
st.sidebar.title("Filters")

min_price = float(df["price_num"].min())
max_price = float(df["price_num"].max())

price_range = st.sidebar.slider(
    "Price range (£)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
)

selected_ratings = st.sidebar.multiselect(
    "Rating",
    options=sorted(df["rating_num"].unique()),
    default=sorted(df["rating_num"].unique()),
)

selected_pages = st.sidebar.multiselect(
    "Scraped page",
    options=sorted(df["page"].unique()),
    default=sorted(df["page"].unique()),
)

filtered = df[
    (df["price_num"] >= price_range[0])
    & (df["price_num"] <= price_range[1])
    & (df["rating_num"].isin(selected_ratings))
    & (df["page"].isin(selected_pages))
]

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("📊 Books Analytics Dashboard")
st.caption("Internship Project | Web Scraping → EDA → Visualization")
st.markdown("---")

# ---------------------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Books", len(filtered))

with col2:
    st.metric("Average Price", f"£{filtered['price_num'].mean():.2f}")

with col3:
    st.metric("Average Rating", f"{filtered['rating_num'].mean():.2f} / 5")

with col4:
    corr = filtered["price_num"].corr(filtered["rating_num"])
    st.metric("Price vs Rating", f"{corr:.3f}")

st.markdown("---")

# ---------------------------------------------------------------------------
# Charts row 1
# ---------------------------------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Rating Distribution")
    rating_counts = filtered["rating_num"].value_counts().sort_index().reset_index()
    rating_counts.columns = ["rating_num", "count"]
    fig1 = px.bar(
        rating_counts,
        x="rating_num",
        y="count",
        color="count",
        color_continuous_scale="Blues",
        labels={"rating_num": "Rating", "count": "Number of Books"},
    )
    fig1.update_layout(showlegend=False, coloraxis_showscale=False, height=380)
    st.plotly_chart(fig1, use_container_width=True)

with right:
    st.subheader("Price Distribution")
    fig2 = px.histogram(
        filtered,
        x="price_num",
        nbins=15,
        color_discrete_sequence=["#2563eb"],
        labels={"price_num": "Price (£)", "count": "Number of Books"},
    )
    fig2.update_layout(height=380)
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Charts row 2
# ---------------------------------------------------------------------------
left2, right2 = st.columns(2)

with left2:
    st.subheader("Price vs Rating")
    fig3 = px.box(
        filtered,
        x="rating_num",
        y="price_num",
        color="rating_num",
        labels={"rating_num": "Rating", "price_num": "Price (£)"},
    )
    fig3.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig3, use_container_width=True)

with right2:
    st.subheader("Average Price by Rating")
    avg_price = filtered.groupby("rating_num")["price_num"].mean().reset_index()
    fig4 = px.bar(
        avg_price,
        x="rating_num",
        y="price_num",
        text=avg_price["price_num"].round(2),
        color="rating_num",
        color_continuous_scale="Viridis",
        labels={"rating_num": "Rating", "price_num": "Avg Price (£)"},
    )
    fig4.update_traces(texttemplate="£%{text}", textposition="outside")
    fig4.update_layout(showlegend=False, coloraxis_showscale=False, height=380)
    st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------------------------------
# Charts row 3
# ---------------------------------------------------------------------------
st.subheader("Books Collected per Page")
page_counts = filtered["page"].value_counts().sort_index().reset_index()
page_counts.columns = ["page", "count"]
fig5 = px.pie(
    page_counts,
    names="page",
    values="count",
    hole=0.4,
    title="",
    color_discrete_sequence=px.colors.sequential.Teal,
)
fig5.update_layout(height=350)
st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------------------------------
# Insights + data table
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("Key Insights")

cheapest = filtered.loc[filtered["price_num"].idxmin()]
costliest = filtered.loc[filtered["price_num"].idxmax()]
most_common_rating = int(filtered["rating_num"].mode()[0])

st.info(
    f"**Most common rating:** {most_common_rating} | "
    f"**Cheapest book:** {cheapest['title']} (£{cheapest['price_num']:.2f}) | "
    f"**Most expensive:** {costliest['title']} (£{costliest['price_num']:.2f}) | "
    f"**Price range:** £{filtered['price_num'].min():.2f} – £{filtered['price_num'].max():.2f}"
)

st.subheader("Dataset Preview")
st.dataframe(
    filtered[["title", "price_num", "rating_num", "page"]].rename(
        columns={
            "title": "Book Title",
            "price_num": "Price (£)",
            "rating_num": "Rating",
            "page": "Page",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

st.caption("Dashboard built with Streamlit + Plotly | Internship Data Science Project")
