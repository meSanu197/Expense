💸 Expense Tracker Lite
A lightweight, full-stack expense tracking web app built with Flask + SQLite, featuring real-time charts, CSV export, category filtering, and a stunning dark UI.

✨ Features
➕ Add expenses with description, amount, date, and category
🗑️ Delete expenses with confirmation prompt
🔍 Filter by date range and category
📊 Doughnut chart — spending breakdown by category
📈 Line chart — daily spending trend over time
⬇️ Export to CSV respecting active filters
💡 Stats bar — total, entry count, average per entry
🎨 Dark glassmorphism UI with animated transitions
⚡ Zero JS framework — pure HTML + Jinja2 + Chart.js


🖥️ Tech Stack
LayerTechnologyBackendPython 3, Flask 3DatabaseSQLite via Flask-SQLAlchemyTemplatingJinja2StylingTailwind CSS (CDN)ChartsChart.js 4FontsOutfit + Space Grotesk (Google Fonts)

📁 Project Structure
expense-tracker/
├── app.py                  # Flask app — routes, model, config
├── requirements.txt        # Python dependencies
├── README.md
└── templates/
    └── index.html          # Single-page Jinja2 template
