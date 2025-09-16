from datetime import date

def add_habit(db: dict, name: str, goal: int | None=None) -> None:
    """Add a new habit to the database with an optional weekly goal."""

    if not name or not name.strip():
        raise ValueError("Habit name cannot be empty.")
    if name in db["habits"]:
        raise ValueError(f"Habit '{name}' already exists.")
    
    db["habits"][name] = {
        "name": name,
        "created": date.today().isoformat(), # for history
        "streak": 0, # current streak, consecutive days counter
        "last_done": None, # last date the habit was done
        "goal": goal, # optional weekly goal
        "history": [] # list of dates when the habit was done
    }
