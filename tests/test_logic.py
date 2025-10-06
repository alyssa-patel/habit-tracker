from datetime import date, timedelta
from habit_cli.logic import add_habit, mark_done

def test_streak_increases_day_after():
    db = {"habits": {}}
    add_habit(db, "Gym")
    y = date.today() - timedelta(days=1)
    mark_done(db, "Gym", y)
    mark_done(db, "Gym", date.today())
    assert db["habits"]["Gym"]["streak"] == 2

def test_streak_resets_after_gap():
    db = {"habits": {}}
    add_habit(db, "Read")
    mark_done(db, "Read", date(2025, 9, 10))
    mark_done(db, "Read", date(2025, 9, 14))
    assert db["habits"]["Read"]["streak"] == 1