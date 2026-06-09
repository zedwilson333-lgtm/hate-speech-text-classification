import pandas as pd
import numpy as np
import os

# ---------------------------------------------------------
# 1. LOAD HATE TERMS AND BUILD LOOKUP DICTIONARIES
# ---------------------------------------------------------

hate_terms_path = r"C:\python\corby_analysis\hate_terms\Hate_Terms_Clean.xlsx"
hate_df = pd.read_excel(hate_terms_path)

# Normalise terms
hate_df["term"] = hate_df["term"].str.lower().str.strip()

# Term → hate value
HATE_MAP = dict(zip(hate_df["term"], hate_df["Media Hate Value"]))

# Term → category
CATEGORY_MAP = dict(zip(hate_df["term"], hate_df["category"]))

# Category weights (adjust anytime)
CATEGORY_WEIGHTS = {
    "Case Related": 0,
    "Crime based": 0,
    "Intelligence based": 3,
    "Familial based": 0,
    "Class based": 3,
    "Authority based": 1,
    "Moral condemnation": 3,
    "Legality based": 0
}

# List of all categories for column creation
ALL_CATEGORIES = hate_df["category"].unique()


# ---------------------------------------------------------
# 2. FUNCTION TO COMPUTE ALL HATE METRICS FOR A COMMENT
# ---------------------------------------------------------

def compute_hate_metrics(text):
    text = str(text).lower()

    # Find matched terms
    matched_terms = [term for term in HATE_MAP if term in text]

    if not matched_terms:
        return {
            "mean_hate_value": 0,
            "weighted_score": 0,
            "category_means": {}
        }

    # Mean hate value
    values = [HATE_MAP[t] for t in matched_terms]
    mean_hate = np.mean(values)

    # Per-category means
    category_values = {}
    for term in matched_terms:
        cat = CATEGORY_MAP[term]
        category_values.setdefault(cat, []).append(HATE_MAP[term])

    category_means = {
        cat: np.mean(vals)
        for cat, vals in category_values.items()
    }

    # Weighted score
    weighted_sum = sum(
        HATE_MAP[t] * CATEGORY_WEIGHTS[CATEGORY_MAP[t]]
        for t in matched_terms
    )
    weighted_score = weighted_sum / len(matched_terms)

    return {
        "mean_hate_value": mean_hate,
        "weighted_score": weighted_score,
        "category_means": category_means
    }


# ---------------------------------------------------------
# 3. PROCESS ALL SCRAPED EXCEL FILES
# ---------------------------------------------------------

scraped_folder = r"C:\python\corby_analysis\scraped"

for filename in os.listdir(scraped_folder):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(scraped_folder, filename)
        print(f"Processing: {filename}")

        df = pd.read_excel(file_path)

        # Compute metrics
        metrics = df["cleaned_text"].apply(compute_hate_metrics)

        # Add main metrics
        df["mean_hate_value"] = metrics.apply(lambda x: x["mean_hate_value"])
        df["weighted_score"] = metrics.apply(lambda x: x["weighted_score"])

        # Add per-category mean columns
        for cat in ALL_CATEGORIES:
            col_name = f"mean_{cat.lower().replace(' ', '_')}"
            df[col_name] = metrics.apply(
                lambda x: x["category_means"].get(cat, 0)
            )

        # Save output
        output_path = os.path.join(
            scraped_folder,
            filename.replace(".xlsx", "_scored.xlsx")
        )
        df.to_excel(output_path, index=False)

        print(f"Saved: {output_path}")

print("All files processed.")
