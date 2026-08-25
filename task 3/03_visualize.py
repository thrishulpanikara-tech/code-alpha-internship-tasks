"""
Task 3: Data Visualization
--------------------------
Input:  data/books_clean.csv   (from Task 2)
Output: charts/*.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHARTS_DIR = BASE_DIR / "charts"

CHARTS_DIR.mkdir(exist_ok=True)

CLEAN_FILE = DATA_DIR / "books_clean.csv"

if not CLEAN_FILE.exists():
    raise FileNotFoundError(
        f"Missing file: {CLEAN_FILE}\n"
        "Run Task 2 first: python 02_eda.py"
    )

df = pd.read_csv(CLEAN_FILE)
sns.set_theme(style="whitegrid")

print("=== TASK 3: DATA VISUALIZATION ===")
print(f"Loaded {len(df)} rows from {CLEAN_FILE}")

# Chart 1: Rating distribution
chart1 = CHARTS_DIR / "rating_distribution.png"
plt.figure(figsize=(7, 4))
sns.countplot(data=df, x="rating_num", order=[1, 2, 3, 4, 5], palette="Blues")
plt.title("Book Rating Distribution")
plt.xlabel("Rating (1 = lowest, 5 = highest)")
plt.ylabel("Number of Books")
plt.tight_layout()
plt.savefig(chart1, dpi=150)
plt.show()
print("Saved:", chart1)

# Chart 2: Price distribution
chart2 = CHARTS_DIR / "price_distribution.png"
plt.figure(figsize=(7, 4))
sns.histplot(df["price_num"], bins=15, kde=True, color="steelblue")
plt.title("Book Price Distribution")
plt.xlabel("Price (£)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(chart2, dpi=150)
plt.show()
print("Saved:", chart2)

# Chart 3: Price vs Rating
chart3 = CHARTS_DIR / "price_vs_rating.png"
plt.figure(figsize=(7, 4))
sns.boxplot(data=df, x="rating_num", y="price_num", order=[1, 2, 3, 4, 5])
plt.title("Price vs Rating")
plt.xlabel("Rating")
plt.ylabel("Price (£)")
plt.tight_layout()
plt.savefig(chart3, dpi=150)
plt.show()
print("Saved:", chart3)

# Chart 4: Average price by rating
chart4 = CHARTS_DIR / "avg_price_by_rating.png"
avg_price = df.groupby("rating_num")["price_num"].mean().reset_index()
plt.figure(figsize=(7, 4))
sns.barplot(data=avg_price, x="rating_num", y="price_num", palette="viridis")
plt.title("Average Price by Rating")
plt.xlabel("Rating")
plt.ylabel("Average Price (£)")
plt.tight_layout()
plt.savefig(chart4, dpi=150)
plt.show()
print("Saved:", chart4)

print()
print("=== TASK 3 COMPLETE ===")
print("Open the charts/ folder in VS Code to view all PNG files.")
