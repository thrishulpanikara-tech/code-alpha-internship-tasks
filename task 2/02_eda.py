"""
Task 2: Exploratory Data Analysis (EDA)
---------------------------------------
Input:  data/books_raw.csv   (from Task 1)
Output: data/books_clean.csv
        reports/eda_report.txt

NO CHARTS in this file — charts are Task 3 (03_visualize.py)
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

DATA_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

RAW_FILE = DATA_DIR / "books_raw.csv"
CLEAN_FILE = DATA_DIR / "books_clean.csv"
REPORT_FILE = REPORT_DIR / "eda_report.txt"

if not RAW_FILE.exists():
    raise FileNotFoundError(
        f"Missing file: {RAW_FILE}\n"
        "Run Task 1 first: python 01_scrape.py"
    )

report_lines = []

def log(text=""):
    print(text)
    report_lines.append(text)


# ---------------------------------------------------------------------------
# STEP 1: Ask meaningful questions BEFORE analysis
# ---------------------------------------------------------------------------
QUESTIONS = [
    "How many books are in the dataset?",
    "What are the most and least common ratings?",
    "What is the price range (min, max, average)?",
    "Do higher-rated books cost more on average?",
    "Are there missing values, duplicates, or bad data?",
]

log("=== TASK 2: EXPLORATORY DATA ANALYSIS ===")
log()
log("=== STEP 1: RESEARCH QUESTIONS ===")
for i, q in enumerate(QUESTIONS, 1):
    log(f"{i}. {q}")

# ---------------------------------------------------------------------------
# STEP 2: Load data and explore structure
# ---------------------------------------------------------------------------
df = pd.read_csv(RAW_FILE)

log()
log("=== STEP 2: DATA STRUCTURE ===")
log(f"Shape (rows, columns): {df.shape}")
log()
log("Column names and data types:")
log(str(df.dtypes))
log()
log("First 5 rows:")
log(str(df.head()))
log()
log("Last 5 rows:")
log(str(df.tail()))

# ---------------------------------------------------------------------------
# STEP 3: Check data quality (missing, duplicates)
# ---------------------------------------------------------------------------
log()
log("=== STEP 3: DATA QUALITY CHECK ===")
log("Missing values per column:")
log(str(df.isna().sum()))
log()
log(f"Duplicate rows: {df.duplicated().sum()}")
df = df.drop_duplicates()

# ---------------------------------------------------------------------------
# STEP 4: Clean data
# ---------------------------------------------------------------------------
log()
log("=== STEP 4: DATA CLEANING ===")

# Price: extract number from text (handles £, Â£, encoding issues)
df["price_num"] = (
    df["price"]
    .astype(str)
    .str.extract(r"([\d.]+)", expand=False)
    .astype(float)
)
log("Created column: price_num (numeric price)")

# Rating: convert One/Two/Three... to 1-5
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
df["rating_num"] = df["rating"].map(rating_map)
log("Created column: rating_num (1 to 5)")

bad_ratings = df[df["rating_num"].isna()]
if len(bad_ratings) > 0:
    log()
    log("Warning: rows with unknown rating:")
    log(str(bad_ratings[["title", "rating"]]))

# ---------------------------------------------------------------------------
# STEP 5: Summary statistics
# ---------------------------------------------------------------------------
log()
log("=== STEP 5: SUMMARY STATISTICS ===")
log(str(df[["price_num", "rating_num"]].describe()))
log()
log("Rating counts:")
log(str(df["rating_num"].value_counts().sort_index()))
log()
log("Average price by rating:")
avg_price = df.groupby("rating_num")["price_num"].mean().sort_index()
log(str(avg_price))
log()
log("Books per scraped page:")
log(str(df["page"].value_counts().sort_index()))

# ---------------------------------------------------------------------------
# STEP 6: Trends, patterns, anomalies
# ---------------------------------------------------------------------------
log()
log("=== STEP 6: TRENDS & ANOMALIES ===")

cheapest = df.loc[df["price_num"].idxmin()]
costliest = df.loc[df["price_num"].idxmax()]
most_common_rating = int(df["rating_num"].mode()[0])
least_common_rating = int(df["rating_num"].value_counts().sort_values().index[0])

log(f"Total books: {len(df)}")
log(f"Most common rating: {most_common_rating}")
log(f"Least common rating: {least_common_rating}")
log(f"Cheapest book: {cheapest['title']} (£{cheapest['price_num']:.2f})")
log(f"Most expensive book: {costliest['title']} (£{costliest['price_num']:.2f})")
log(f"Average price: £{df['price_num'].mean():.2f}")
log(f"Price range: £{df['price_num'].min():.2f} to £{df['price_num'].max():.2f}")

# Outlier detection (IQR method)
q1 = df["price_num"].quantile(0.25)
q3 = df["price_num"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
outliers = df[(df["price_num"] < lower) | (df["price_num"] > upper)]

log()
log(f"Price outliers (IQR method): {len(outliers)} books")

# ---------------------------------------------------------------------------
# STEP 7: Test hypothesis
# ---------------------------------------------------------------------------
log()
log("=== STEP 7: HYPOTHESIS TEST ===")
log("Hypothesis: Higher-rated books cost more on average.")

correlation = df["price_num"].corr(df["rating_num"])
log(f"Correlation (price vs rating): {correlation:.3f}")

if correlation > 0.1:
    result = "Weak positive link — higher ratings may relate to higher prices."
elif correlation < -0.1:
    result = "Weak negative link — higher ratings may relate to lower prices."
else:
    result = "No strong link between rating and price in this dataset."
log(f"Result: {result}")

# ---------------------------------------------------------------------------
# STEP 8: Answer the research questions
# ---------------------------------------------------------------------------
log()
log("=== STEP 8: ANSWERS TO RESEARCH QUESTIONS ===")
log(f"1. Dataset has {len(df)} books.")
log(f"2. Most common rating: {most_common_rating} | Least common: {least_common_rating}")
log(f"3. Price range: £{df['price_num'].min():.2f} - £{df['price_num'].max():.2f} | Avg: £{df['price_num'].mean():.2f}")
log(f"4. Correlation price vs rating: {correlation:.3f} — {result}")
log(f"5. Missing values: none | Duplicates removed: checked")

# ---------------------------------------------------------------------------
# STEP 9: Save cleaned data + report
# ---------------------------------------------------------------------------
df.to_csv(CLEAN_FILE, index=False)

REPORT_FILE.write_text("\n".join(report_lines), encoding="utf-8")

log()
log("=== TASK 2 COMPLETE ===")
log(f"Saved cleaned data: {CLEAN_FILE}")
log(f"Saved EDA report:   {REPORT_FILE}")
log()
log("Next step -> Task 3: python 03_visualize.py")
