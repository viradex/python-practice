import csv
from pathlib import Path
from models.order import Order

class OrderRepo:
    def __init__(self, filename):
        self.filename = filename
        self.FIELDNAMES = (
            "sales_id",
            "num_workers",
            "num_queens",
            "distance_km",
            "bonus_code",
            "final_cost",
        )


    def create_file(self):

        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writeheader()

    def get_next_id(self):
        # TODO:
        # 1. If the file does not exist, create it, with headers and return 1
        if not Path(self.filename).exists():
            self.create_file()
            return 1
        # 2. Open the CSV file for reading
        highest_id = 0
        with open(self.filename, mode="r", newline="", encoding="UTF-8") as file:
        # 3. Skip the header row
            reader = csv.DictReader(file)
        # 4. Find the highest existing sales_id
            for row in reader:
                if int(row["sales_id"]) > highest_id:
                    highest_id = int(row["sales_id"])
        # 5. Return the next ID 
        return highest_id + 1

    def check_queen_count(self, num_queens):
        # TODO:
        # 1. ensure that num_queens (from new order) plus sum of queens in file < 11
        if num_queens > 10:
            return False
        
        total_queens = 0
        if not Path(self.filename).exists():
            return True

        with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_queens += int(row["num_queens"])

        # 2. return TRUE (if we can proceed with order) or FALSE (if too many queens)
        return (total_queens + num_queens) <= 10


    def save(self, order):
        # TODO:
        try:
            order.sales_id = self.get_next_id()
            
            # 1. Open the CSV file in append mode
            with open(self.filename, mode="a", newline="", encoding="utf-8") as file:
            # 2. Write order.to_csv_row()
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writerow(order.to_dict())

            return True
        except:
            return False #can get better error information, but this is enough for now
