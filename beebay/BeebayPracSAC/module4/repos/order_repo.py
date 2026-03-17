import csv
from models.order import Order

class OrderRepo:
    def __init__(self, filename):
        self.filename = filename

    def get_next_id(self):
        # TODO:
        # 1. If the file does not exist, create it, with headers and return 1
        # 2. Open the CSV file for reading
        # 3. Skip the header row
        # 4. Find the highest existing sales_id
        # 5. Return the next ID 

        #remove this next line to start your coding
        pass

    def check_queen_count(self, num_queens):
        # TODO:
        # 1. ensure that num_queens (from new order) plus sum of queens in file < 11
        # 2. return TRUE (if we can proceed with order) or FALSE (if too many queens)

        return True

    def save(self, order):
        # TODO:
        # 1. Open the CSV file in append mode
        # 2. Write order.to_csv_row()

        #remove this next line to start your coding
        pass
