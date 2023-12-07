import tkinter as tk
from tkinter import ttk

class Passenger:
    def __init__(self, first_name, surname="", date_of_birth="", country="", service_type=""):
        self.first_name = first_name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.country = country
        self.service_type = service_type

class PassengerForm():
    SERVICE_OPTIONS = ["Service", "Premium Service", "Super Service"]

    def __init__(self, root):
        # self.add_passenger_callback = add_passenger_callback
        self.root = root

        self.main_frame = ttk.Frame(root)
        self.main_frame.place(x=100, y=200, height=300, width=650)
        
        self.passenger_list = []
        self.first_name_var = tk.StringVar()
        self.surname_var = tk.StringVar()
        self.date_of_birth_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.service_type_var = tk.StringVar()

        self.add_labels()
        
    def add_labels(self):
        # Etiquetas y campos de entrada
        ttk.Label(self.main_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.first_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Surname:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.surname_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Date of Birth:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.date_of_birth_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Country:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.country_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Service Type:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Dropdown menu for Service Type
        self.service_type_menu = ttk.Combobox(self.main_frame, textvariable=self.service_type_var, values=self.SERVICE_OPTIONS, state="readonly")
        self.service_type_menu.grid(row=4, column=1, padx=5, pady=5)

        # Botón para guardar la información del pasajero
        self.save_passenger_button = ttk.Button(self.root, text="Add Passenger 1", command=self.save_passenger)
        self.save_passenger_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Contador de pasajeros
        self.passenger_count = 1
        
    def save_passenger(self):
        # Crear un objeto Passenger con la información ingresada
        
        if (not self.first_name_var.get() or not self.surname_var.get() or not self.date_of_birth_var.get()
            or not self.country_var.get() or not self.service_type_var.get()):
            print("Tiene que completar todos los campos")
            return
        
        passenger = Passenger(
            first_name=self.first_name_var.get(),
            surname=self.surname_var.get(),
            date_of_birth=self.date_of_birth_var.get(),
            country=self.country_var.get(),
            # buscar objeto de service type
            service_type=self.service_type_var.get()
        )

        self.passenger_list.append(passenger)
        self.first_name_var.set("")
        self.surname_var.set("")
        self.date_of_birth_var.set("") 
        self.country_var.set("")
        self.service_type_var.set("") 
        self.passenger_count += 1

        # Actualizar el texto del botón con el número actual de pasajeros
        self.save_passenger_button["text"] = f"Add Passenger {self.passenger_count}"
        
    def dissapear(self):
        self.place_forget()
        self.pack_forget()
        
    def get_passenger_list(self):
        return print(len(self.passenger_list))

class App(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        # self.root.title("Main App")

        # Crear un contenedor para el formulario de pasajeros
        passenger_form_container = tk.Frame(self.root, width=300, height=200, bg="lightgray")
        passenger_form_container.place(x=100, y=200)

        # Colocar el formulario de pasajeros dentro del contenedor
        self.passenger_form = PassengerForm(passenger_form_container)
        self.passenger_form.pack(expand=True, fill="both")
        search_btn2 = tk.Button(self.root, text="Search", command=self.passenger_form.get_passenger_list)
        search_btn2.pack()



def main():
    root = tk.Tk()
    root.geometry("900x600")
    app = PassengerForm(root)
    # app.pack(expand=True, fill="both")
    root.mainloop()

main()
