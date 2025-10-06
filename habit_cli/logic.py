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
    
def remove_habit(db: dict, name: str) -> None:
    """Delete a habit if it exists."""
    if name in db["habits"]:
        del db["habits"][name]
    else:
        raise KeyError("habit not found")

def rename_habit(db: dict, old: str, new: str) -> None:
    """Rename a habit key, preserving history and streak."""
    if old not in db["habits"]:
        raise KeyError("habit not found")
    if not new.strip():
        raise ValueError("new name required")
    if new in db["habits"]:
        raise ValueError("target name already exists")
    h = db["habits"].pop(old)
    h["name"] = new
    db["habits"][new] = h

def weekly_stats(db: dict, anchor: date | None = None) -> dict:
    """
    Return per-habit summary for the current ISO week:
    { name: {"done_this_week": int, "goal": int|None, "streak": int } }
    """
    if anchor is None:
        anchor = date.today()
    year, week, _ = anchor.isocalendar()

    def in_this_week(iso: str) -> bool:
        y, w, _ = date.fromisoformat(iso).isocalendar()
        return (y, w) == (year, week)

    out = {}
    for name, h in db["habits"].items():
        done = sum(1 for d in h.get("history", []) if in_this_week(d))
        out[name] = {
            "done_this_week": done,
            "goal": h.get("goal"),
            "streak": h.get("streak", 0),
        }
    return out