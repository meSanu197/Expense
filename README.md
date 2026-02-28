# 💸 Expense Tracker Lite

A lightweight, full-stack **expense tracking web app** built with **Flask + SQLite**, featuring real-time charts, CSV export, category filtering, and a stunning dark UI.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat&logo=sqlite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CDN-06B6D4?style=flat&logo=tailwindcss&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?style=flat&logo=chartdotjs&logoColor=white)

---

## ✨ Features

- ➕ **Add expenses** with description, amount, date, and category
- 🗑️ **Delete expenses** with confirmation prompt
- 🔍 **Filter** by date range and category
- 📊 **Doughnut chart** — spending breakdown by category
- 📈 **Line chart** — daily spending trend over time
- ⬇️ **Export to CSV** respecting active filters
- 💡 **Stats bar** — total, entry count, average per entry
- 🎨 **Dark glassmorphism UI** with animated transitions
- ⚡ **Zero JS framework** — pure HTML + Jinja2 + Chart.js

---

## 🖥️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask 3 |
| Database | SQLite via Flask-SQLAlchemy |
| Templating | Jinja2 |
| Styling | Tailwind CSS (CDN) |
| Charts | Chart.js 4 |
| Fonts | Outfit + Space Grotesk (Google Fonts) |

---

## 📁 Project Structure

```
expense-tracker/
├── app.py                  # Flask app — routes, model, config
├── requirements.txt        # Python dependencies
├── README.md
└── templates/
    └── index.html          # Single-page Jinja2 template
```

> **Note:** `expenses.db` is auto-created at runtime and should be added to `.gitignore`.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

### 2. Create and activate a virtual environment

```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

The SQLite database (`expenses.db`) is created automatically on first run.

---

## 📸 Screenshots

> _Add screenshots here after running the app locally._
>
> Tip: Press `F12` → Device toolbar to capture a clean full-page screenshot.

---

## 🗺️ Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Main page — list, filter, charts |
| `/add` | POST | Add a new expense |
| `/delete/<id>` | POST | Delete an expense by ID |
| `/export` | GET | Download filtered expenses as CSV |

---

## 🏷️ Default Categories

`Food` · `Transport` · `Rent` · `Utilities` · `Health`

You can add or edit categories in `app.py`:

```python
CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Health"]
```

---

## ⚙️ Configuration

All config lives at the top of `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SECRET_KEY'] = 'change-me-in-production'
```

> ⚠️ **Never commit your real `SECRET_KEY` to GitHub.** Use environment variables in production:
>
> ```python
> import os
> app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-dev-key')
> ```

---

## 🧱 Database Model

```python
class Expense(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount      = db.Column(db.Float, nullable=False)
    category    = db.Column(db.String(50), nullable=False)
    date        = db.Column(db.Date, nullable=False, default=date.today)
```

---

## 📦 Dependencies

```
flask>=3.0
flask-sqlalchemy>=3.1
```

## 👤 Author

**Kumar Sanu**
- GitHub: [meSanu197](https://github.com/meSanu197)

---

> Built with ❤️ using Flask and Python
