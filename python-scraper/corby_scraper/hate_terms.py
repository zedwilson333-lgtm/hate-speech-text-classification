import pandas as pd

df = pd.read_excel("hate_terms.xlsx")

# Normalize terms
df["term"] = (
    df["term"]
    .astype(str)
    .str.lower()
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

# Normalize categories
df["category"] = (
    df["category"]
    .astype(str)
    .str.lower()
    .str.strip()
)

# Drop duplicates after normalization
df = df.drop_duplicates(subset=["term"])

# Build lists and maps
TERMS = df["term"].tolist()
TERM_MAP = dict(zip(df["term"], df["category"]))
