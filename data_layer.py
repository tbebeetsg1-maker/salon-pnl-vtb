"""CSV-backed storage for entries (sales and expenses).

All reads and writes go through data/entries.csv via pandas. There's
no real database here — the CSV file is the source of truth.
"""

import pandas as pd
import os

FILE_PATH = "data/entries.csv"


def load_entries():
    """Load all entries from the CSV file.

    Returns an empty DataFrame with the correct columns if the file
    doesn't exist yet, so callers don't need to handle a missing file
    as a special case.
    """
    if not os.path.exists(FILE_PATH):
        return pd.DataFrame(columns=["date", "type", "category", "client", "amount"])
    return pd.read_csv(FILE_PATH)


def add_entry(date, entry_type, category, client, amount):
    """Append a new sale or expense entry to the CSV file.

    Args:
        date: Entry date, as a string (YYYY-MM-DD).
        entry_type: Either "sale" or "expense".
        category: Service category (for sales) or expense category.
        client: Client name (blank for expenses).
        amount: Dollar amount.

    Returns:
        The full DataFrame of entries after the new row was added.
    """
    df = load_entries()
    new_row = pd.DataFrame([{
        "date": date, "type": entry_type, "category": category,
        "client": client, "amount": amount
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)
    return df


def get_entries_by_month(year, month):
    """Return all entries that fall within a given calendar month."""
    df = load_entries()
    df["date"] = pd.to_datetime(df["date"])
    return df[(df["date"].dt.year == year) & (df["date"].dt.month == month)]


def get_entries_by_range(start_date, end_date):
    """Return all entries between two dates (inclusive)."""
    df = load_entries()
    df["date"] = pd.to_datetime(df["date"])
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    return df[(df["date"] >= start) & (df["date"] <= end)]


def export_range_to_excel(start_date, end_date, output_path="generated/export.xlsx"):
    """Write entries in a date range to an Excel file.

    Creates the output directory if it doesn't exist yet.

    Returns:
        The filepath the Excel file was written to.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    df = get_entries_by_range(start_date, end_date)
    df.to_excel(output_path, index=False)
    return output_path
