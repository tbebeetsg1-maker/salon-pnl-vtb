# Salon P&L

A small-business invoicing and profit-and-loss tracker, built for a salon: log sales and expenses, generate client invoices, and pull monthly or custom-range P&L reports with tax calculated automatically.

## <h2><ins>Why I built this</ins></h2>

This started as a class assignment and grew into a full solo rebuild — I redesigned the UI, restructured the data layer, wrote a real test suite, and rebuilt it around a Kaggle salon transaction dataset to simulate what an actual small salon business would need day to day.

## <h2><ins>What it does</ins></h2>

- **Log entries** — record sales (by service category and client) or expenses, with the category list adjusting to match the entry type
- **Generate invoices** — every sale entry produces a downloadable PDF invoice for the client
- **Monthly P&L** — automatic profit-and-loss report for the current month: total sales, total expenses, tax owed, net profit
- **Custom date-range reports** — pull P&L for any date range
- **Export to Excel** — download any range report as an `.xlsx` file

## <h2><ins>About the data</ins></h2>

The seed data (`data/Receipt_Transactions0.csv`) is a Kaggle dataset simulating salon transactions — it's not real customer or business data, but it's structured to reflect what an actual salon's transaction history looks like. `import_real_data.py` converts it into the app's entry format.

## <h2><ins>Tech stack</ins></h2>

- **Flask** — web framework
- **pandas** — data handling and reporting logic
- **fpdf2** — PDF invoice generation
- **openpyxl** — Excel export
- **pytest** — test suite

## <h2><ins>Running it locally</ins></h2>

```bash
git clone https://github.com/tbebeetsg1-maker/salon-pnl-vtb.git
cd salon-pnl-vtb
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## <h2><ins>Running the tests</ins></h2>

```bash
pytest
```

13 tests cover the data layer (adding entries, filtering by month/date range, Excel export) and the reporting logic (category/client totals, tax calculation, monthly and range P&L). Tests run against temporary files, so they never touch the real seed data.

## <h2><ins>Project structure</ins></h2>

```
app.py                  Flask routes
data_layer.py             CSV-backed storage (pandas)
logic.py                  P&L calculations and tax logic
import_real_data.py       Converts the raw Kaggle CSV into the app's entry format
templates/                 home.html, report.html
static/style.css           Styling
generated/                 PDF invoices and Excel exports (created automatically, gitignored)
test_data.py, test_logic.py    pytest suites
```
