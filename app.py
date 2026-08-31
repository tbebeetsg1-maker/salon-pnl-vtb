"""Flask routes for the Salon P&L app.

Handles the entry form, PDF invoice generation, monthly/range P&L
reporting, and Excel export.
"""

from flask import Flask, render_template, request, redirect, send_file
from data_layer import add_entry, export_range_to_excel
from logic import monthly_pl_report, range_pl_report
from datetime import datetime
from fpdf import FPDF
import os

GENERATED_DIR = "generated"

app = Flask(__name__)


def generate_invoice_pdf(client, amount, date):
    """Generate a simple one-page PDF invoice for a sale entry.

    Creates the generated/ directory if it doesn't exist yet, so this
    works on a fresh clone of the repo without any manual setup.

    Args:
        client: Client name to print on the invoice.
        amount: Amount due.
        date: Date of the sale.

    Returns:
        The filepath the PDF was written to.
    """
    os.makedirs(GENERATED_DIR, exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="INVOICE", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Client: {client}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
    pdf.cell(200, 10, txt=f"Amount Due: ${amount}", ln=True)
    filepath = os.path.join(GENERATED_DIR, "invoice.pdf")
    pdf.output(filepath)
    return filepath


@app.route("/")
def home():
    """Render the entry form.

    If invoice_client/amount/date are present in the query string
    (set by the redirect after adding a sale), the template auto-
    triggers a PDF download for that invoice on page load.
    """
    invoice_client = request.args.get("invoice_client")
    invoice_amount = request.args.get("invoice_amount")
    invoice_date = request.args.get("invoice_date")
    return render_template(
        "home.html",
        invoice_client=invoice_client,
        invoice_amount=invoice_amount,
        invoice_date=invoice_date,
    )


@app.route("/add", methods=["POST"])
def add():
    """Save a new sale or expense entry from the form submission.

    Sale entries redirect back to the home page with invoice details
    in the query string, which triggers an automatic invoice download.
    Expense entries just redirect back to a blank form.
    """
    date = request.form["date"]
    entry_type = request.form["entry_type"]
    category = request.form["category"]
    client = request.form["client"]
    amount = float(request.form["amount"])
    add_entry(date, entry_type, category, client, amount)
    if entry_type == "sale":
        return redirect(f"/?invoice_client={client}&invoice_amount={amount}&invoice_date={date}")
    return redirect("/")


@app.route("/report")
def report():
    """Render the current month's P&L, plus an optional custom-range report."""
    now = datetime.now()
    current_report = monthly_pl_report(now.year, now.month)

    start = request.args.get("start")
    end = request.args.get("end")
    range_report = None
    if start and end:
        range_report = range_pl_report(start, end)

    return render_template(
        "report.html",
        current=current_report,
        range_report=range_report,
        start=start,
        end=end,
    )


@app.route("/invoice/<client>/<amount>/<date>")
def invoice(client, amount, date):
    """Generate and download a PDF invoice for a single sale."""
    filepath = generate_invoice_pdf(client, amount, date)
    return send_file(filepath, as_attachment=True)


@app.route("/export")
def export():
    """Export a date-range report to an Excel file for download."""
    start = request.args.get("start")
    end = request.args.get("end")
    filepath = export_range_to_excel(start, end)
    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
