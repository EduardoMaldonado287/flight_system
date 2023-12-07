import tkinter as tk
from tkinter import ttk

class FlightSummaryApp:
    def __init__(self, root):
        self.root = root
        # self.root.title("Flight Summary")
        self.counter = 0
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
        # self.flight_summary_window = tk.Toplevel(root)
        # self.flight_summary_window.title("Flight Summary")

        # Styling
        style = ttk.Style()
        style.configure("Flight.TLabel", font=(None, 12), padding=(5, 2))
        style.configure("Flight.TFrame", background="#EFEFEF")

        # Main frame
        main_frame = ttk.Frame(self.root, style="Flight.TFrame")
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

        # Display flight information in labels
        self.create_label(main_frame, "Origin:", self.origin)
        self.create_label(main_frame, "Destination:", self.destination)
        self.create_label(main_frame, "Departure Time:", self.departure_time)
        self.create_label(main_frame, "Duration:", self.duration)
        self.create_label(main_frame, "Status:", self.status)
        self.create_label(main_frame, "Date:", self.date)
        self.create_label(main_frame, "Flight Code:", self.code)
        self.create_label(main_frame, "Price:", self.price)
        self.create_label(main_frame, "Available Seats:", self.available_seats)

    def create_label(self, parent, label_text, value):
        ttk.Label(parent, text=f"{label_text} {value}", style="Flight.TLabel").grid(row=self.counter, column=0, padx=10, pady=5, sticky=tk.W)
        self.counter += 1

def main():
    root = tk.Tk()
    root.geometry("400x300")

    app = FlightSummaryApp(root)
    root.mainloop()

main()