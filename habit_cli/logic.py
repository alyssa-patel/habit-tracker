from datetime import date, timedelta

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

def mark_done(db:dict, name: str, when: date) -> None:
    """ Mark a habit as completed for a specific date 
     Streaks:
        -If last_done was yesterday --> streak +=1
        - Else --> streak = 1
        - Same day repeated --> no-op
    """

    h = db["habits"].get(name)
    if not h:
        raise KeyError("habit not found")
    
    today_iso = when.isoformat()

    #If habit is already marked done for that day, no-op
    if h["last_done"] == today_iso:
        return
    
    if h["last_done"] is None:
        h["streak"] = 1
    else:
        prev = date.fromisoformat(h["last_done"])
        h["streak"] = h["streak"] + 1 if prev == when - timedelta(days=1) else 1

    h["last_done"] = today_iso

    #Keep an append-only history of days completed for weekly stats
    if today_iso not in h["history"]:
        h["history"].append(today_iso)
    
