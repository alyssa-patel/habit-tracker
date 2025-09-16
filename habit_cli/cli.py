# habit_cli/cli.py
import typer
from .storage import load_db, save_db
from .logic import add_habit

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



if __name__ == "__main__":
    app()