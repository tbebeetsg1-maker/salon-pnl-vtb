"""P&L calculations: totals, tax, and net profit."""

from data_layer import load_entries, get_entries_by_month, get_entries_by_range


def totals_by_category(df):
    """Sum entry amounts grouped by category."""
    return df.groupby("category")["amount"].sum()


def totals_by_client(df):
    """Sum entry amounts grouped by client."""
    return df.groupby("client")["amount"].sum()


TAX_RATE = 0.08  # 8% flat rate


def calculate_tax_owed(df):
    """Calculate tax owed on sales for a given set of entries.

    Only sale entries are taxed — expenses are excluded. Uses the
    flat TAX_RATE defined above.

    Args:
        df: A DataFrame of entries with 'type' and 'amount' columns.

    Returns:
        The tax owed, rounded to 2 decimal places.
    """
    sales_total = df[df["type"] == "sale"]["amount"].sum()
    return round(sales_total * TAX_RATE, 2)


def monthly_pl_report(year, month):
    """Build a P&L summary for a single calendar month.

    Returns:
        A dict with total_sales, total_expenses, tax_owed, and
        net_profit, all rounded to 2 decimal places.
    """
    df = get_entries_by_month(year, month)
    total_sales = df[df["type"] == "sale"]["amount"].sum()
    total_expenses = df[df["type"] == "expense"]["amount"].sum()
    tax_owed = calculate_tax_owed(df)
    net_profit = total_sales - total_expenses - tax_owed
    return {
        "total_sales": round(total_sales, 2),
        "total_expenses": round(total_expenses, 2),
        "tax_owed": tax_owed,
        "net_profit": round(net_profit, 2)
    }


def range_pl_report(start_date, end_date):
    """Build a P&L summary for a custom date range.

    Same shape as monthly_pl_report, but for an arbitrary start/end
    date instead of a calendar month.
    """
    df = get_entries_by_range(start_date, end_date)
    total_sales = df[df["type"] == "sale"]["amount"].sum()
    total_expenses = df[df["type"] == "expense"]["amount"].sum()
    tax_owed = calculate_tax_owed(df)
    net_profit = total_sales - total_expenses - tax_owed
    return {
        "total_sales": round(total_sales, 2),
        "total_expenses": round(total_expenses, 2),
        "tax_owed": tax_owed,
        "net_profit": round(net_profit, 2)
    }
