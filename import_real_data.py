"""One-time script to convert the raw Kaggle salon dataset into the
app's entry format and load it into data/entries.csv.

Run directly with: python import_real_data.py
This overwrites entries.csv, so only run it if you actually want to
reset your data back to the original Kaggle seed dataset.
"""

import pandas as pd
from data_layer import FILE_PATH

RAW_FILE = "data/Receipt_Transactions0.csv"


def convert_and_import():
    """Read the raw Kaggle transactions CSV and write it out in the
    app's entry format (date, type, category, client, amount).

    Every row becomes a "sale" entry. Transactions marked with a
    "HOUSE" staff member are treated as discounts/promotions rather
    than a real service category.
    """
    raw = pd.read_csv(RAW_FILE)

    # Build the new rows to match our entries.csv format
    converted = pd.DataFrame({
        "date": pd.to_datetime(raw["Date"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d"),
        "type": "sale",
        "category": raw.apply(
            lambda row: "Discount/Promotion" if row["Staff"] == "HOUSE" else row["Description"],
            axis=1
        ),
        "client": raw["Client"],
        "amount": raw["Amount"]
    })

    converted.to_csv(FILE_PATH, index=False)
    print(f"Imported {len(converted)} rows into {FILE_PATH}")


if __name__ == "__main__":
    convert_and_import()
