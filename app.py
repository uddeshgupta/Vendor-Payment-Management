from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

CSV_FILE = "payments.csv"

# Ensure the CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Price", "Profit Margin", "Quantity", "Tax", "Vendor", "Reconciliation", "Total Payment"])

# Function to save payment data to CSV
def save_payment(data):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Function to load payment history from CSV
def load_payments():
    payments = []
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            payments.append(row)
    return payments

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        product_name = request.form.getlist("product_name")
        price = request.form.getlist("price")
        profit_margin = request.form.getlist("profit_margin")
        quantity = request.form.getlist("quantity")
        tax = request.form.getlist("tax")
        vendor = request.form.getlist("vendor")
        reconciliation = request.form.getlist("reconciliation")

        payments = []
        for i in range(len(product_name)):
            if not product_name[i] or not price[i] or not quantity[i] or not vendor[i]:
                continue  # Skip empty fields

            price_value = float(price[i])
            profit_value = float(profit_margin[i]) if profit_margin[i] else 0
            quantity_value = int(quantity[i])
            tax_value = float(tax[i]) if tax[i] else 0

            # Calculate Total Payment
            profit_amount = (profit_value / 100) * price_value
            tax_amount = (tax_value / 100) * price_value
            total_payment = (price_value + profit_amount + tax_amount) * quantity_value

            # Apply reconciliation discount (if applicable)
            if "discount" in reconciliation[i].lower():
                total_payment *= 0.9  # 10% discount

            payments.append([product_name[i], price_value, profit_value, quantity_value, tax_value, vendor[i], reconciliation[i], total_payment])

        save_payment(payments)  # Save to CSV

        return redirect(url_for("index"))  # Refresh page

    # Load existing payments from CSV
    payments = load_payments()

    return render_template("index.html", payments=payments)

if __name__ == "__main__":
    app.run(debug=True)
