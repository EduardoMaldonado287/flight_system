import tkinter as tk
from tkinter import ttk

class FlightSummaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Summary")

        # Flight information
        self.origin = "New York"
        self.destination = "Los Angeles"
        self.departure_time = "08:00 AM"
        self.duration = "4 hours"
        self.status = "Scheduled"
        self.date = "2023-12-15"
        self.code = "ABC123"
        self.price = "$500"
        self.available_seats = 50

        # Create a Toplevel window for the flight summary
        self.flight_summary_window = tk.Toplevel(root)
        self.flight_summary_window.title("Flight Summary")

        # Display flight information in labels
        ttk.Label(self.flight_summary_window, text="Origin:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.flight_summary_window, text=self.origin).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.flight_summary_window, text="Destination:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.flight_summary_window, text=self.destination).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.flight_summary_window, text="Departure Time:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.flight_summary_window, text=self.departure_time).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.flight_summary_window, text="Duration:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.flight_summary_window, text=self.duration).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.flight_summary_window, text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.flight_summary_window, text=self.status).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.flight_summary_window, text="Date:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.flight_summary_window, text=self.date).grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.flight_summary_window, text="Flight Code:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.flight_summary_window, text=self.code).grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self.flight_summary_window, text="Price:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.flight_summary_window, text=self.price).grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(self.flight_summary_window, text="Available Seats:").grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self.flight_summary_window, text=self.available_seats).grid(row=8, column=1, padx=5, pady=5)

def main():
    root = tk.Tk()
    app = FlightSummaryApp(root)
    root.geometry("300x300")
    root.mainloop()

if __name__ == "__main__":
    main()
