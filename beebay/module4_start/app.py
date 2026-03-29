import tkinter as tk
from pathlib import Path
from datetime import date
from screens.order_screen import OrderScreen
from repos.order_repo import OrderRepo

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Beebay - Module 4")
        self.root.geometry("700x420")

        today = date.today()
        base_dir = Path(__file__).resolve().parent
        data_file = base_dir / "data" / f"{today}sales.csv"
        
        self.order_repo = OrderRepo(data_file)
        OrderScreen(self.root, self.order_repo)

    def run(self):
        self.root.mainloop()
