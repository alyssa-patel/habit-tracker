# habit_cli/cli.py
import typer

app = typer.Typer(help="Track habits with streaks and weekly goals.")

@app.command(name="hello")
def hello(name: str):
    """Say hello (test command)."""
    print(f"Hello, {name}!")

@app.command(name="ping")
def ping():
    """Simple ping."""
    print("pong")

if __name__ == "__main__":
    app()
