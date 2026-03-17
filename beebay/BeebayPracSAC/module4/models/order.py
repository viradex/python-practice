from dataclasses import dataclass

@dataclass
class Order:
    num_workers: int
    num_queens: int
    distance_km: float
    bonus_code: str
    final_cost: float = 0
    sales_id: int = None
    
    def calculate(self):
        # TODO: implement the calculation logic from Module 1
        # does not need to return a value, it would update the attributes.
        self.final_cost = 999.99
    
    def to_csv_row(self):
        # TODO: return this order as a list in the correct CSV field order
        # Order:
        # sales_id, num_workers, num_queens, distance_km, bonus_code, final_cost
        pass


