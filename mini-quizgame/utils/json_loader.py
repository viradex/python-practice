import json
from pathlib import Path


class JSONLoader:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.base_dir / "data"
        self.json_path = self.data_dir / "questions.json"

    def _ensure_data_dir(self):
        pass

    def _ensure_csv_exists(self):
        pass

    def load_all(self):
        pass
