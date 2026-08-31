"""Tests for data_layer.py: adding entries, loading, filtering by
month/date range, and Excel export.

Every test uses the temp_data_file fixture, which points FILE_PATH at
a scratch file for the duration of the test. This means these tests
never read or write the real data/entries.csv seed data.
"""

import pandas as pd
import pytest
import data_layer


@pytest.fixture
def temp_data_file(tmp_path, monkeypatch):
    """Point data_layer at a scratch CSV so tests never touch the real seed data."""
    temp_file = tmp_path / "entries.csv"
    monkeypatch.setattr(data_layer, "FILE_PATH", str(temp_file))
    return str(temp_file)


def test_load_entries_returns_empty_df_when_file_missing(temp_data_file):
    df = data_layer.load_entries()
    assert list(df.columns) == ["date", "type", "category", "client", "amount"]
    assert len(df) == 0


def test_add_entry_creates_file_and_appends_row(temp_data_file):
    data_layer.add_entry("2026-08-01", "sale", "Haircut", "Jordan M.", 45.0)
    df = data_layer.load_entries()
    assert len(df) == 1
    assert df.iloc[0]["client"] == "Jordan M."
    assert df.iloc[0]["amount"] == 45.0


def test_add_entry_appends_multiple_rows_in_order(temp_data_file):
    data_layer.add_entry("2026-08-01", "sale", "Haircut", "Jordan M.", 45.0)
    data_layer.add_entry("2026-08-02", "expense", "Supplies", "N/A", 20.0)
    df = data_layer.load_entries()
    assert len(df) == 2
    assert df.iloc[1]["type"] == "expense"


def test_get_entries_by_month_filters_correctly(temp_data_file):
    data_layer.add_entry("2026-08-05", "sale", "Haircut", "A", 50.0)
    data_layer.add_entry("2026-09-05", "sale", "Haircut", "B", 60.0)
    august = data_layer.get_entries_by_month(2026, 8)
    assert len(august) == 1
    assert august.iloc[0]["client"] == "A"


def test_get_entries_by_range_filters_correctly(temp_data_file):
    data_layer.add_entry("2026-08-01", "sale", "Haircut", "A", 50.0)
    data_layer.add_entry("2026-08-15", "sale", "Haircut", "B", 60.0)
    data_layer.add_entry("2026-09-01", "sale", "Haircut", "C", 70.0)
    ranged = data_layer.get_entries_by_range("2026-08-01", "2026-08-31")
    assert len(ranged) == 2
    assert set(ranged["client"]) == {"A", "B"}


def test_export_range_to_excel_creates_file(temp_data_file, tmp_path):
    data_layer.add_entry("2026-08-01", "sale", "Haircut", "A", 50.0)
    output_path = tmp_path / "export_test.xlsx"
    result_path = data_layer.export_range_to_excel(
        "2026-08-01", "2026-08-31", output_path=str(output_path)
    )
    assert output_path.exists()
    exported = pd.read_excel(result_path)
    assert len(exported) == 1
    assert exported.iloc[0]["client"] == "A"
