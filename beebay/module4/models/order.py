from dataclasses import dataclass


@dataclass
class Order:
    num_workers: int
    num_queens: int
    distance_km: float
    bonus_code: str
    final_cost: float = 0
    sales_id: int = None

    def _calculate_post(self):
        if self.distance_km <= 50:
            return 10
        elif self.distance_km <= 150:
            return 20
        else:
            return 30

    def calculate(self):
        # TODO: implement the calculation logic from Module 1
        # does not need to return a value, it would update the attributes.

        worker_price = 0.05
        queen_price = 15.00
        queen_surcharge_rate = 0.125

        worker_cost = self.num_workers * worker_price
        queen_cost = self.num_queens * queen_price
        bee_subtotal = worker_cost + queen_cost

        if self.num_queens > 0:
            surcharge_amount = bee_subtotal * queen_surcharge_rate
        else:
            surcharge_amount = 0

        postage_cost = self._calculate_post()
        WORKER_PRICE = 0.05
        QUEEN_PRICE = 15.00
        QUEEN_SURCHARGE_RATE = 0.125

        worker_cost = self.num_workers * WORKER_PRICE
        queen_cost = self.num_queens * QUEEN_PRICE
        bee_subtotal = worker_cost + queen_cost

        if self.num_queens > 0:
            surcharge_amount = bee_subtotal * QUEEN_SURCHARGE_RATE
        else:
            surcharge_amount = 0

        postage_cost = self.calculate_post()

        if self.bonus_code == "FREEPOST":
            postage_cost = 0
        elif self.bonus_code == "HALFPOST":
            postage_cost /= 2

        subtotal = bee_subtotal + surcharge_amount + postage_cost

        if self.bonus_code == "SALE":
            discount_amount = subtotal * 0.1
        else:
            discount_amount = 0

        self.final_cost = subtotal - discount_amount
        return self.final_cost

    def to_csv_row(self):
        # TODO: return this order as a list in the correct CSV field order
        # Order:
        # sales_id, num_workers, num_queens, distance_km, bonus_code, final_cost

        return {
            "sales_id": self.sales_id,
            "num_workers": self.num_workers,
            "num_queens": self.num_queens,
            "distance_km": self.distance_km,
            "bonus_code": self.bonus_code,
            "final_cost": self.final_cost,
        }
        pass
