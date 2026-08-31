"""Tests for logic.py: category/client totals, tax calculation, and
monthly/range P&L reports.

The first few tests use a hand-built DataFrame directly, since the
totals/tax functions don't touch the filesystem. The report tests
further down need real entries, so they use the temp_data_file
fixture (same pattern as test_data.py) to avoid touching the real
seed data.
"""

import pandas as pd
import pytest
import data_layer
import logic


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {"date": "2026-08-01", "type": "sale", "category": "Haircut", "client": "A", "amount": 100.0},
        {"date": "2026-08-02", "type": "sale", "category": "Color", "client": "B", "amount": 200.0},
        {"date": "2026-08-03", "type": "expense", "category": "Supplies", "client": "N/A", "amount": 30.0},
    ])


def test_totals_by_category(sample_df):
    totals = logic.totals_by_category(sample_df)
    assert totals["Haircut"] == 100.0
    assert totals["Color"] == 200.0
    assert totals["Supplies"] == 30.0


def test_totals_by_client(sample_df):
    totals = logic.totals_by_client(sample_df)
    assert totals["A"] == 100.0
    assert totals["B"] == 200.0


def test_calculate_tax_owed_applies_flat_rate_to_sales_only(sample_df):
    # sales total = 300.0, tax rate = 8% -> 24.0. Expenses are excluded.
    tax = logic.calculate_tax_owed(sample_df)
    assert tax == 24.0


def test_calculate_tax_owed_with_no_sales_is_zero():
    df = pd.DataFrame([
        {"date": "2026-08-01", "type": "expense", "category": "Rent", "client": "N/A", "amount": 500.0},
    ])
    assert logic.calculate_tax_owed(df) == 0.0


@pytest.fixture
def temp_data_file(tmp_path, monkeypatch):
    """Point data_layer at a scratch CSV so report tests never touch the real seed data."""
    temp_file = tmp_path / "entries.csv"
    monkeypatch.setattr(data_layer, "FILE_PATH", str(temp_file))
    return str(temp_file)


def test_monthly_pl_report_calculates_net_profit(temp_data_file):
    data_layer.add_entry("2026-08-01", "sale", "Haircut", "A", 100.0)
    data_layer.add_entry("2026-08-02", "expense", "Supplies", "N/A", 20.0)
    report = logic.monthly_pl_report(2026, 8)
    # sales 100, expenses 20, tax = 8% of 100 = 8, net = 100 - 20 - 8 = 72
    assert report["total_sales"] == 100.0
    assert report["total_expenses"] == 20.0
    assert report["tax_owed"] == 8.0
    assert report["net_profit"] == 72.0


def test_monthly_pl_report_excludes_other_months(temp_data_file):
    data_layer.add_entry("2026-08-01", "sale", "Haircut", "A", 100.0)
    data_layer.add_entry("2026-09-01", "sale", "Haircut", "B", 500.0)
    report = logic.monthly_pl_report(2026, 8)
    assert report["total_sales"] == 100.0


def test_range_pl_report_calculates_net_profit(temp_data_file):
    data_layer.add_entry("2026-08-01", "sale", "Haircut", "A", 100.0)
    data_layer.add_entry("2026-08-15", "sale", "Color", "B", 200.0)
    data_layer.add_entry("2026-08-20", "expense", "Rent", "N/A", 50.0)
    report = logic.range_pl_report("2026-08-01", "2026-08-31")
    # sales 300, expenses 50, tax = 8% of 300 = 24, net = 300 - 50 - 24 = 226
    assert report["total_sales"] == 300.0
    assert report["total_expenses"] == 50.0
    assert report["tax_owed"] == 24.0
    assert report["net_profit"] == 226.0
