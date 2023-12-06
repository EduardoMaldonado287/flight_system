import tkinter as tk
from tkinter import ttk

class LabelDisplayApp:
    def __init__(self, root, string_list):
        self.root = root
        self.string_list = string_list

        # Create a green container frame
        container_frame = tk.Frame(root, background="green")
        container_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a frame to hold the Label widgets
        self.frame = ttk.Frame(container_frame)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a scrollbar for the frame
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Canvas to contain the Label widgets
        self.canvas = tk.Canvas(self.frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Attach the scrollbar to the canvas
        scrollbar.config(command=self.canvas.yview)

        # Create a frame to contain the Label widgets inside the canvas
        self.label_frame = ttk.Frame(self.canvas)

        # Add the frame to the canvas
        self.canvas.create_window((0, 0), window=self.label_frame, anchor=tk.NW)

        # Bind the canvas to configure the scroll region
        self.canvas.bind("<Configure>", self.configure_scroll_region)

        # Add Label widgets to the label frame based on the string list
        self.label_widgets = []
        for text_string in self.string_list:
            label_widget = tk.Label(self.label_frame, text=text_string, wraplength=300)
            label_widget.pack(pady=5, anchor=tk.W)
            self.label_widgets.append(label_widget)

    def configure_scroll_region(self, event):
        # Update the scroll region when the size of the canvas changes
        self.label_frame.update_idletasks()
        self.frame_width = self.frame.winfo_width()
        self.frame_height = self.frame.winfo_height()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()

    # Lista de strings de ejemplo
    string_list = ["String 1", "String 2", "String 3", "String 4", "String 5", "String 6", "String 7",
                   "String 8", "String 9", "String 10", "String 11", "String 12", "String 13", "String 14"]

    app = LabelDisplayApp(root, string_list)
    root.title("Label Display App")

    # Set the size of the main window
    window_width = 500
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")

    # Center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"+{x_position}+{y_position}")

    root.mainloop()
