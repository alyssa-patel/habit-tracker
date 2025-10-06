# Habit Tracker CLI


![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

A lightweight Python command-line app to track daily habits, maintain streaks, and monitor weekly goals.  
Built as a personal project to practice CLI development, testing, and packaging.

---

## 🚀 Quickstart

### 1. Clone & navigate
```bash
git clone https://github.com/alyssa-patel/habit-tracker.git
cd habit-tracker
```

### 2. Create & activate a virtual environment

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install in editable mode
```bash
pip install --upgrade pip setuptools wheel
pip install -e .
```

### 4. View help / commands
```bash
habit --help
```

Or, without installing:
```bash
python -m habit_cli.cli --help
```

---

## 🧰 Usage Examples

Add habits (with optional weekly goals):
```bash
habit add "Gym" -g 4
habit add "Study DSA" -g 5
habit add "Read 20min"
```

Mark a habit as done:
```bash
habit done "Gym"
habit done "Read 20min"
```

List habits:
```bash
habit list
```

Example output:
```
┏━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Name        ┃ Streak ┃ Last Done  ┃ Goal/week ┃
┡━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ Gym         │ 1      │ 2025-09-14 │ 4         │
│ Study DSA   │ 0      │ -          │ 5         │
│ Read 20min  │ 0      │ -          │ -         │
└─────────────┴────────┴────────────┴───────────┘
```

Weekly stats:
```bash
habit stats
```

Example output:
```
┏━━━━━━━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━━━┓
┃ Name       ┃ Done ┃ Goal ┃ Streak ┃
┡━━━━━━━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━━━┩
│ Gym        │ 1    │ 4    │ 1      │
│ Study DSA  │ 0    │ 5    │ 0      │
│ Read 20min │ 0    │ -    │ 0      │
└────────────┴──────┴──────┴────────┘
```

Rename / Remove:
```bash
habit rename "Read 20min" "Read 10min"
habit remove "Read 10min"
```

(If you add CSV export later)
```bash
habit export-csv
```

---

## 📂 Project Structure

```
habit-tracker/
├─ habit_cli/
│   ├─ __init__.py
│   ├─ cli.py          # CLI commands (Typer)
│   ├─ logic.py        # streaks, add/done/rename/remove, weekly stats
│   └─ storage.py      # JSON file load/save
├─ tests/
│   └─ test_logic.py   # unit tests
├─ .github/workflows/ci.yml  # run pytest on push
├─ pyproject.toml
├─ README.md
├─ LICENSE
└─ .gitignore
```

---

## 🧪 Development & Testing

Run locally without installing:
```bash
python -m habit_cli.cli --help
```

Run tests:
```bash
pytest -q
```

Format/lint (if installed):
```bash
pip install black ruff
black .
ruff check .
```

---

## ⚠️ Troubleshooting

- **`habit: command not found`** → Run `pip install -e .` inside your virtual environment.  
- **Windows venv activation blocked** → In PowerShell (once):  
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- **Weird table characters** → Your terminal font may not support box-drawing. Functionality is unaffected.

---


