import csv
from pathlib import Path
from datetime import date

from models.order import Order


class OrderRepo:
    def __init__(self):
        today = date.today()
        base_dir = Path(__file__).resolve().parent.parent
        self.filename = base_dir / "data" / f"{today}_sales.csv"

        self.fields = [
            "sales_id",
            "num_workers",
            "num_queens",
            "distance_km",
            "bonus_code",
            "final_cost",
        ]

    def _ensure_csv_exists(self):
        if self.filename.exists():
            return True

        self.filename.parent.mkdir(parents=True, exist_ok=True)

        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()

        return False

    def get_next_id(self):
        # TODO:
        # 1. If the file does not exist, create it, with headers and return 1
        # 2. Open the CSV file for reading
        # 3. Skip the header row
        # 4. Find the highest existing sales_id
        # 5. Return the next ID

        if not self._ensure_csv_exists():
            return 1

        max_id = 0
        with open(self.filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row.get("sales_id", "").isdigit():
                    continue

                current_id = int(row.get("sales_id", 0))
                if current_id > max_id:
                    max_id = current_id

        return max_id + 1

    def check_queen_count(self, num_queens):
        # TODO:
        # 1. ensure that num_queens (from new order) plus sum of queens in file < 11
        # 2. return TRUE (if we can proceed with order) or FALSE (if too many queens)

        self._ensure_csv_exists()

        saved_queens = 0
        with open(self.filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row.get("sales_id", "").isdigit():
                    continue

                saved_queens += int(row.get("num_queens", 0))

        return (saved_queens + num_queens) < 11

    def save(self, order):
        # TODO:
        # 1. Open the CSV file in append mode
        # 2. Write order.to_csv_row()

        self._ensure_csv_exists()

        with open(self.filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writerow(order.to_csv_row())
