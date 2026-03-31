import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from models.booking import Booking
from logic.booking_repo_csv import BookingRepoCSV


class BookingsScreen(ttk.Frame):
    def __init__(self, parent, repo: BookingRepoCSV):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.repo = repo
        self.booking = None
        self.all_bookings = self.repo.load_all()

        self.VALID_TICKET_TIERS = ("Standard", "Premium", "VIP")

        self.grid(row=0, column=0, sticky="NSEW")

        # Also ID, total cost, and date entered should be calculated automatically
        self.event_date_var = tk.StringVar()
        self.ticket_tier_var = tk.StringVar(value=self.VALID_TICKET_TIERS[0])
        self.num_adults_var = tk.StringVar()
        self.num_children_var = tk.StringVar()
        self.total_cost_var = tk.StringVar()

        self.setup_grid()
        self.create_widgets()

    def setup_grid(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def create_widgets(self):
        ttk.Label(
            self,
            text="Riverstone Arena Concert Venue Booking",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="W", pady=(0, 15))

        ttk.Label(self, text="Event date:").grid(
            row=1, column=0, sticky="W", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.event_date_var).grid(
            row=1, column=1, sticky="EW", pady=5
        )

        ttk.Label(self, text="Ticket tier:").grid(
            row=2, column=0, sticky="W", padx=(0, 10), pady=5
        )
        ttk.Combobox(
            self,
            textvariable=self.ticket_tier_var,
            state="readonly",
            values=self.VALID_TICKET_TIERS,
        ).grid(row=2, column=1, sticky="EW", pady=5)

        ttk.Label(self, text="Number of adults:").grid(
            row=3, column=0, sticky="W", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.num_adults_var).grid(
            row=3, column=1, sticky="EW", pady=5
        )

        ttk.Label(self, text="Number of children:").grid(
            row=4, column=0, sticky="W", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.num_children_var).grid(
            row=4, column=1, sticky="EW", pady=5
        )

        ttk.Label(self, text="Total cost:").grid(
            row=5, column=0, sticky="W", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.total_cost_var, state="readonly").grid(
            row=5, column=1, sticky="EW", pady=5
        )

        ttk.Button(self, text="Calculate", command=self.calculate).grid(
            row=6, column=0, sticky="W", pady=(12, 0)
        )
        ttk.Button(self, text="Save Order", command=self.save).grid(
            row=6, column=1, sticky="E", pady=(12, 0)
        )

    def get_inputs(self):
        event_date = self.event_date_var.get().strip()
        ticket_tier = self.ticket_tier_var.get().strip()
        num_adults = self.num_adults_var.get().strip()
        num_children = self.num_children_var.get().strip()
        total_cost = self.total_cost_var.get().strip()

        return event_date, ticket_tier, num_adults, num_children, total_cost

    def reset_inputs(self):
        self.event_date_var.set("")
        self.ticket_tier_var.set(self.VALID_TICKET_TIERS[0])
        self.num_adults_var.set("")
        self.num_children_var.set("")
        self.total_cost_var.set("")

    def validate_inputs(self):
        event_date, ticket_tier, num_adults, num_children, _ = self.get_inputs()

        if not all((event_date, ticket_tier, num_adults, num_children)):
            messagebox.showerror(
                "Empty Value(s)",
                "Please ensure all values are filled in before submitting.",
            )
            return False
        elif not self._is_valid_date(event_date):
            messagebox.showerror(
                "Invalid Date",
                "The date must be in a valid format (YYYY-MM-DD) and not be a past date.",
            )
            return False
        elif ticket_tier not in self.VALID_TICKET_TIERS:
            # Ordinarily, this should never happen
            messagebox.showerror(
                "Invalid Ticket Tier",
                "The ticket tier is not valid.",
            )
            return False

        try:
            num_adults = int(num_adults)
            num_children = int(num_children)
        except ValueError:
            messagebox.showerror(
                "Invalid People Amount",
                "The number of adults or children entered is not a valid number.",
            )
            return False

        if num_adults < 0 or num_children < 0:
            messagebox.showerror(
                "Invalid People Amount",
                "The number of adults or children entered cannot be a negative number.",
            )
            return False
        elif num_adults == 0 and num_children == 0:
            messagebox.showerror(
                "Invalid People Amount",
                "The total amount of people entered is zero. Please ensure some people are selected.",
            )
            return False

        return True

    def _is_valid_date(self, date_str):
        try:
            date = datetime.date.fromisoformat(date_str)
            return date >= datetime.date.today()
        except ValueError:
            # If parsing date fails, it means it was invalid
            return False

    def calculate(self):
        if not self.validate_inputs():
            return False

        event_date, ticket_tier, num_adults, num_children, _ = self.get_inputs()

        self.booking = self.repo.create_booking(
            event_date, ticket_tier, int(num_adults), int(num_children)
        )

        self.total_cost_var.set(self.booking.total_cost)
        return True

    def save(self):
        if not self.booking:
            validation_success = self.calculate()
            if validation_success is False:
                return

        self.repo.save(self.all_bookings, self.booking)
        self.all_bookings = self.repo.load_all()

        messagebox.showinfo(
            "Saved Data", f"Saved booking data with ID {self.booking.booking_id}."
        )
        self.reset_inputs()
        self.booking = None
