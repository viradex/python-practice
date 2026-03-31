from dataclasses import dataclass

@dataclass
class Order:
    WORKER_PRICE = 0.05
    QUEEN_PRICE = 15.00
    QUEEN_SURCHARGE_RATE = 0.125

    num_workers: int
    num_queens: int
    distance_km: float
    bonus_code: str
    final_cost: float = 0
    sales_id: int = None


# class Order:
#     def __init__(self, num_workers, num_queens, distance_km, bonus_code, final_cost = 0, sales_id = None):
#         pass
    
    def calculate_post(self):

        postage_cost = 0
        if self.distance_km < 50:
            postage_cost = 10
        elif self.distance_km < 150:
            postage_cost = 20
        else:
            postage_cost = 30

        return postage_cost

    def calculate(self):
        # TODO: implement the calculation logic from Module 1
        # does not need to return a value, it would update the attributes.

        #bee costs
        workers_cost = self.num_workers * self.WORKER_PRICE
        queen_cost = self.num_queens * self.QUEEN_PRICE
        bee_subtotal = workers_cost + queen_cost
        
        #queen surcharge
        surcharge_amount = 0
        if self.num_queens > 0:
            surcharge_amount = bee_subtotal * self.QUEEN_SURCHARGE_RATE

        #postage
        postage_cost = self.calculate_post()
        if self.bonus_code == "FREEPOST":
            postage_cost = 0
        elif self.bonus_code == "HALFPOST":
            postage_cost = postage_cost / 2

        subtotal = bee_subtotal + surcharge_amount + postage_cost

        #discount
        discount_amount = 0
        if self.bonus_code == "SALE":
            discount_amount = subtotal * 0.10

        self.final_cost = subtotal - discount_amount
    
    def to_csv_row(self):
        # TODO: return this order as a list in the correct CSV field order
        # Order:
        # sales_id, num_workers, num_queens, distance_km, bonus_code, final_cost
        pass
    
    def to_dict(self):
        #this is better called to_dict - sorry!!
        return {
            "sales_id": self.sales_id,
            "num_workers": self.num_workers,
            "num_queens": self.num_queens,
            "distance_km": self.distance_km,
            "bonus_code": self.bonus_code,
            "final_cost": self.final_cost,
        }


