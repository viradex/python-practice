import tkinter as tk

from logic.booking_repo_csv import BookingRepoCSV
from screens.bookings_screen import BookingsScreen


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Module 4 Practice SAC")
        self.root.geometry("700x420")

        self.order_repo = BookingRepoCSV()
        BookingsScreen(self.root, self.order_repo)

    def run(self):
        self.root.mainloop()
