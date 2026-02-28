import io
import csv
from flask import Flask, render_template, request, url_for, flash, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from sqlalchemy import func

app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my-secret-key'

db = SQLAlchemy(app)

# ---------------- MODEL ----------------
class Expense(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount      = db.Column(db.Float, nullable=False)
    category    = db.Column(db.String(50), nullable=False)
    date        = db.Column(db.Date, nullable=False, default=date.today)

with app.app_context():
    db.create_all()

CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Health"]

# ---------------- HELPERS ----------------
def parse_date_or_none(s: str):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None

def build_query(start_date, end_date, selected_category):
    """Reusable filtered query — used by index and export."""
    q = Expense.query
    if start_date:
        q = q.filter(Expense.date >= start_date)
    if end_date:
        q = q.filter(Expense.date <= end_date)
    if selected_category:
        q = q.filter(Expense.category == selected_category)
    return q

# ---------------- ROUTES ----------------
@app.route('/')
def index():
    start_str         = (request.args.get('start') or "").strip()
    end_str           = (request.args.get('end') or "").strip()
    selected_category = (request.args.get('category') or "").strip()

    start_date = parse_date_or_none(start_str)
    end_date   = parse_date_or_none(end_str)

    # Validate date range
    if start_date and end_date and end_date < start_date:
        flash("End date cannot be before start date.", "error")
        start_date = end_date = None
        start_str  = end_str  = ""

    expenses = (
        build_query(start_date, end_date, selected_category)
        .order_by(Expense.date.desc(), Expense.id.desc())
        .all()
    )
    total = round(sum(e.amount for e in expenses), 2)

    # ── Chart: by category ──
    cat_q = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .filter(Expense.date >= start_date if start_date else True)
        .filter(Expense.date <= end_date   if end_date   else True)
    )
    if selected_category:
        cat_q = cat_q.filter(Expense.category == selected_category)
    cat_rows   = cat_q.group_by(Expense.category).all()
    cat_labels = [c for c, _ in cat_rows]
    cat_values = [round(float(s or 0), 2) for _, s in cat_rows]  # FIX: keep 2 decimal places

    # ── Chart: by day ──
    day_q = (
        db.session.query(Expense.date, func.sum(Expense.amount))
        .filter(Expense.date >= start_date if start_date else True)
        .filter(Expense.date <= end_date   if end_date   else True)
    )
    if selected_category:
        day_q = day_q.filter(Expense.category == selected_category)
    day_rows   = day_q.group_by(Expense.date).order_by(Expense.date).all()
    day_labels = [str(d) for d, _ in day_rows]
    day_values = [round(float(s or 0), 2) for _, s in day_rows]

    return render_template(
        "index.html",
        categories        = CATEGORIES,
        today             = date.today().isoformat(),
        expenses          = expenses,
        total             = total,
        start_str         = start_str,
        end_str           = end_str,
        selected_category = selected_category,
        cat_labels        = cat_labels,   # FIX: was missing
        cat_values        = cat_values,   # FIX: was missing
        day_labels        = day_labels,
        day_values        = day_values,
    )


@app.route('/add', methods=['POST'])
def add():
    description = (request.form.get('description') or "").strip()
    amount_str  = (request.form.get('amount')      or "").strip()
    category    = (request.form.get('category')    or "").strip()
    date_str    = (request.form.get('date')        or "").strip()

    if not description or not amount_str or not category or not date_str:
        flash("Please fill all fields.", "error")
        return redirect(url_for("index"))

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Amount must be a positive number.", "error")
        return redirect(url_for("index"))

    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        d = date.today()

    db.session.add(Expense(description=description, amount=amount, category=category, date=d))
    db.session.commit()
    flash("Expense added successfully!", "success")
    return redirect(url_for("index"))


# FIX: POST-only delete — GET delete is a security risk (CSRF / accidental deletion via URL)
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete(expense_id):
    e = Expense.query.get_or_404(expense_id)
    db.session.delete(e)
    db.session.commit()
    flash("Expense deleted.", "success")
    return redirect(url_for("index"))


@app.route('/export')
def export():
    """Download filtered expenses as a CSV file."""
    start_str         = (request.args.get('start')    or "").strip()
    end_str           = (request.args.get('end')      or "").strip()
    selected_category = (request.args.get('category') or "").strip()

    expenses = (
        build_query(
            parse_date_or_none(start_str),
            parse_date_or_none(end_str),
            selected_category,
        )
        .order_by(Expense.date.desc())
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Date", "Description", "Category", "Amount"])
    for e in expenses:
        writer.writerow([e.id, e.date.isoformat(), e.description, e.category, f"{e.amount:.2f}"])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=expenses.csv"},
    )


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)