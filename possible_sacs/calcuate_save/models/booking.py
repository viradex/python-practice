from dataclasses import dataclass
from datetime import datetime


# booking_id,event_date,ticket_tier,num_adults,num_children,total_cost,date_entered
@dataclass
class Booking:
    PRICES = {
        "standard": {"adult": 40, "child": 25},
        "premium": {"adult": 70, "child": 45},
        "vip": {"adult": 110, "child": 70},
    }

    booking_id: int
    event_date: str
    ticket_tier: str
    num_adults: int
    num_children: int
    total_cost: float = 0
    date_entered: str = ""

    def calculate_total_cost(self):
        adult_price = self.PRICES[self.ticket_tier.lower()]["adult"]
        child_price = self.PRICES[self.ticket_tier.lower()]["child"]

        subtotal = (self.num_adults * adult_price) + (self.num_children * child_price)
        total_tickets = self.num_adults + self.num_children

        # Get 10% discount if five or more people have tickets
        discount = subtotal * 0.1 if total_tickets >= 5 else 0

        self.total_cost = subtotal - discount
        return self.total_cost

    def set_date_entered(self):
        self.date_entered = datetime.now().strftime("%Y-%m-%d")
        return self.date_entered
