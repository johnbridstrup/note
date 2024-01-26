import os


HOME = os.path.expanduser("~")
noteTaker_folder = os.path.join(HOME, ".noteTaker")
DB_PATH = os.path.join(noteTaker_folder, "notes.db")
INITIAL_NOTEBOOK = "general"
CUR_KEY = "current_notebook"
NB_KEY = "notebooks"

os.makedirs(noteTaker_folder, exist_ok=True)
