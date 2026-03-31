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

        self.all_bookings: list[Booking] = self.repo.load_all()
        self.selected_booking = None

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
        self.refresh_tree()

        self.tree.bind("<<TreeviewSelect>>", self.tree_select)

    def setup_grid(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)

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

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=5, column=0, columnspan=4, sticky="EW", pady=(10, 20))

        for i in range(3):
            btn_frame.columnconfigure(i, weight=1)

        self.add_btn = ttk.Button(btn_frame, text="Add", command=self.add)
        self.add_btn.grid(row=0, column=0, sticky="EW", padx=5)

        self.edit_btn = ttk.Button(
            btn_frame, text="Edit", state="disabled", command=self.edit
        )
        self.edit_btn.grid(row=0, column=1, sticky="EW", padx=5)

        self.delete_btn = ttk.Button(
            btn_frame, text="Delete", state="disabled", command=self.delete
        )
        self.delete_btn.grid(row=0, column=2, sticky="EW", padx=5)

        self.tree = ttk.Treeview(
            self, columns=self.repo.fields, show="headings", height=12
        )
        self.tree.grid(row=6, column=0, columnspan=2, sticky="NSEW")

        headings = {
            "booking_id": "Booking ID",
            "event_date": "Event Date",
            "ticket_tier": "Ticket Tier",
            "num_adults": "Adults",
            "num_children": "Children",
            "total_cost": "Total Cost",
            "date_entered": "Date Entered",
        }

        for column_name in self.repo.fields:
            self.tree.heading(column_name, text=headings[column_name])
            self.tree.column(column_name, width=110, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=6, column=2, sticky="NS")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def get_inputs(self):
        event_date = self.event_date_var.get().strip()
        ticket_tier = self.ticket_tier_var.get().strip()
        num_adults = self.num_adults_var.get().strip()
        num_children = self.num_children_var.get().strip()

        return event_date, ticket_tier, num_adults, num_children

    def reset_inputs(self):
        self.event_date_var.set("")
        self.ticket_tier_var.set(self.VALID_TICKET_TIERS[0])
        self.num_adults_var.set("")
        self.num_children_var.set("")

    def set_button_add_mode(self):
        self.add_btn.config(state="normal")
        self.edit_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")

    def set_button_edit_mode(self):
        self.add_btn.config(state="disabled")
        self.edit_btn.config(state="normal")
        self.delete_btn.config(state="normal")

    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for booking in self.all_bookings:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    str(booking.booking_id),
                    booking.event_date,
                    Booking.beautify_tier(booking.ticket_tier),
                    str(booking.num_adults),
                    str(booking.num_children),
                    str(booking.total_cost),
                    booking.date_entered,
                ),
            )

    def validate_inputs(self):
        event_date, ticket_tier, num_adults, num_children = self.get_inputs()

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

    def add(self):
        if not self.validate_inputs():
            return

        event_date, ticket_tier, num_adults, num_children = self.get_inputs()

        booking = self.repo.create_booking(
            event_date, ticket_tier, int(num_adults), int(num_children)
        )

        self.repo.save(self.all_bookings, booking)
        self.all_bookings = self.repo.load_all()

        self.reset_inputs()
        self.refresh_tree()

        self.set_button_add_mode()

        messagebox.showinfo(
            "Saved Data", f"Saved booking data with ID {booking.booking_id}."
        )

    def edit(self):
        if not self.validate_inputs() or not self.selected_booking:
            return

        event_date, ticket_tier, num_adults, num_children = self.get_inputs()

        old_values = (
            self.selected_booking[1],
            self.selected_booking[2],
            self.selected_booking[3],
            self.selected_booking[4],
        )
        new_values = (event_date, ticket_tier, num_adults, num_children)

        if old_values == new_values:
            messagebox.showinfo("No Changes Made", "You haven't changed any values.")
        else:
            booking = self.repo.create_booking(
                event_date,
                ticket_tier,
                int(num_adults),
                int(num_children),
                booking_id=int(self.selected_booking[0]),
            )

            self.repo.update(self.all_bookings, booking)
            self.all_bookings = self.repo.load_all()

            messagebox.showinfo(
                "Updated Data", f"Updated booking data with ID {booking.booking_id}."
            )

        self.reset_inputs()
        self.refresh_tree()

        self.set_button_add_mode()

    def delete(self):
        if not self.selected_booking:
            return

        target = int(self.selected_booking[0])
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the booking with ID {target}?",
            icon="warning",
        )

        if not confirm:
            return

        deleted = self.repo.delete(self.all_bookings, target)
        if not deleted:
            messagebox.showerror("Error", "Item not found!")

        self.refresh_tree()
        self.reset_inputs()

        self.set_button_add_mode()

    def tree_select(self, _=None):
        selected_row = self.tree.selection()
        if not selected_row:
            return

        self.selected_booking = self.tree.item(selected_row[0], "values")
        self.event_date_var.set(self.selected_booking[1])
        self.ticket_tier_var.set(self.selected_booking[2])
        self.num_adults_var.set(self.selected_booking[3])
        self.num_children_var.set(self.selected_booking[4])

        self.set_button_edit_mode()
