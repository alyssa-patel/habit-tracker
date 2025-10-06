# habit_cli/cli.py
import typer
from datetime import date
from .storage import load_db, save_db
from .logic import add_habit
from .logic import mark_done
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
        t.add_row(h["name"], str(h["streak"]), h["last_done"] or "-", str(h.get("goal_week") or "-"))
    console.print(t)
    

if __name__ == "__main__":
    app()