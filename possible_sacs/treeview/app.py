import tkinter as tk

from logic.booking_repo_csv import BookingRepoCSV
from screens.bookings_screen import BookingsScreen


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Module 4 Practice SAC")
        self.root.geometry("900x600")
        self.root.minsize(900, 600)

        self.booking_repo = BookingRepoCSV()
        BookingsScreen(self.root, self.booking_repo)

    def run(self):
        self.root.mainloop()
