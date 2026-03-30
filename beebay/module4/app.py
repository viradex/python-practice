import tkinter as tk

from screens.order_screen import OrderScreen
from repos.order_repo import OrderRepo


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Beebay - Module 4")
        self.root.geometry("700x420")

        self.order_repo = OrderRepo()
        OrderScreen(self.root, self.order_repo)

    def run(self):
        self.root.mainloop()
