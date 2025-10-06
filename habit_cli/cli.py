# habit_cli/cli.py
import typer
from datetime import date
from .storage import load_db, save_db
from .logic import add_habit, mark_done, remove_habit, rename_habit, weekly_stats
from rich.table import Table
from rich.console import Console

console = Console()


app = typer.Typer(help="Track habits with streaks and weekly goals.")

@app.command(name="hello")
def hello(name: str):
    """Say hello (test command)."""
    print(f"Hello, {name}!")

@app.command()
def add(name: str, goal: int = typer.Option(None, "--goal", "-g", help="Optional weekly goal")):
    """ Create a habit 
        Example: habit-cli add "Exercise" --g 5
        habit add "Read a book" --g 3
    """
    db = load_db()
    add_habit(db, name, goal)
    save_db(db)
    print(f"Added habit: {name} (goal/week: {goal or '-'})")

@app.command()
def done(name:str):
    """ Mark a habit done for today.
    Example: habit done "Gym"
    """
    
    db = load_db()
    mark_done(db, name, date.today())
    save_db(db)
    print(f"Done: {name}")

@app.command("list")
def list_cmd():
    """ Show habits: name, streak, last_done
    """
    db = load_db()
    habits = list(db["habits"].values())
    habits.sort(key=lambda x: x["name"].lower())
    t = Table(title="Habits")
    for c in ["Name","Streak","Last Done","Goal/week"]:
        t.add_column(c)
    for h in habits:
        t.add_row(h["name"], str(h["streak"]), h["last_done"] or "-", str(h.get("goal") or "-"))
    console.print(t)

@app.command()
def remove(name: str):
    """Remove a habit completely."""
    db = load_db()
    remove_habit(db, name)
    save_db(db)
    console.print(f"Removed: [bold]{name}[/]")

@app.command()
def rename(old: str, new: str):
    """Rename an existing habit."""
    db = load_db()
    rename_habit(db, old, new)
    save_db(db)
    console.print(f"Renamed: [bold]{old}[/] → [bold]{new}[/]")

@app.command()
def stats():
    """Show completions for the current week vs goal, plus streaks."""
    db = load_db()
    data = weekly_stats(db)
    table = Table(title="This Week")
    table.add_column("Name"); table.add_column("Done"); table.add_column("Goal"); table.add_column("Streak")
    for name in sorted(data.keys(), key=str.lower):
        s = data[name]
        table.add_row(name, str(s["done_this_week"]), str(s["goal"] or "-"), str(s["streak"]))
    console.print(table)

@app.command("export-csv")
def export_csv(path: str = "habits.csv"):
    """Export habits (name, streak, last_done, goal) to a CSV file."""
    import csv
    from pathlib import Path
    db = load_db()
    rows = [["name", "streak", "last_done", "goal"]]
    for h in db["habits"].values():
        rows.append([h["name"], h.get("streak", 0), h.get("last_done") or "", h.get("goal") or ""])
    with open(Path(path), "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    console.print(f"Exported to [bold]{path}[/]")
    

if __name__ == "__main__":
    app()