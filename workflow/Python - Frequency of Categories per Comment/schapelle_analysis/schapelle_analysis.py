import pandas as pd

# -----------------------------
# 1. Load hate terms file
# -----------------------------
hate_df = pd.read_excel("Hate_Terms_Clean.xlsx")

# Normalise
hate_df["term"] = hate_df["term"].astype(str).str.lower().str.strip()
hate_df["category"] = hate_df["category"].astype(str).str.strip()

# Build category → list of terms mapping
category_terms = (
    hate_df.groupby("category")["term"]
    .apply(list)
    .to_dict()
)

categories = list(category_terms.keys())

# -----------------------------
# 2. Load scraped comments file
# -----------------------------
comments_df = pd.read_excel("Total_comments.xlsx")

# Assume first column contains comments
comment_col = comments_df.columns[0]
comments_df[comment_col] = comments_df[comment_col].astype(str)

# -----------------------------
# 3. Create output columns
# -----------------------------
for cat in categories:
    comments_df[cat] = 0

# -----------------------------
# 4. Match terms to comments
# -----------------------------
for idx, row in comments_df.iterrows():
    text = row[comment_col].lower()

    for cat, terms in category_terms.items():
        # If ANY term from this category appears in the comment → mark 1
        if any(term in text for term in terms):
            comments_df.at[idx, cat] = 1

# -----------------------------
# 5. Save output
# -----------------------------
comments_df.to_excel("Comments_with_Hate_Categories.xlsx", index=False)

print("Done! Output saved as Comments_with_Hate_Categories.xlsx")
