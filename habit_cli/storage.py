#save and load storage 

import json, os ,tempfile, shutil
from pathlib import Path


#store data  in users home directory
DB_DIR = Path(os.path.expanduser("~/.habit_cli"))
DB_PATH = DB_DIR / "habits.json"


def _ensure():
    """ private function to ensure the data directory anf JSON file exist
        lets the rest of the code assume the file is present    
    """

    DB_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        DB_PATH.write_text(json.dumps({"habits": {}}, indent = 2)) #empty structure
    
def load_db() -> dict:
    """ load current database state as a python dict 
        to be called at the start of each cli command   
    """

    _ensure()
    return json.loads(DB_PATH.read_text())

def save_db(db: dict) -> None:
    """ Save the database to a disk  to minimise corruption if the process is interrupted"""

    _ensure()
    with tempfile.NamedTemporaryFile("w", delete=False, dir=DB_DIR, prefix="habits.") as tmp:
        json.dump(db, tmp, indent=2)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = tmp.name
    shutil.move(tmp_path, DB_PATH) # atomic operation on most OSes, replace in one step

    
    
