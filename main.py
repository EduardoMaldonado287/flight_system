import datetime
# from datetime import datetime
import uuid
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar as WCalendar
from datetime import timedelta

class Time:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute
        
    def get_time(self):
        hour = str(self.hour)
        minute = str(self.minute)
        if len(hour) == 1:
            hour = "0" + hour
        if len(minute) == 1:
            minute = "0" + minute
        return hour + ":" + minute
        

class City:
    def __init__(self, name = "aalborg", info = "city in demnark"):
        self.city_id = str(uuid.uuid4()) 
        self.name = name
        self.info = info

        
class CityContainer:
    def __init__(self):
        self.cities = []
    
    def add_city(self, city):
        self.cities.append(city)


class Route:
    def __init__(self, origin, destination):
        self.route_id = str(uuid.uuid4()) 
        self.origin = origin
        self.destination = destination
        routeContainer.add_route(self)
     
        
class RouteContainer:
    def __init__(self):
        self.routes = []
    
    def add_route(self, route):
        self.routes.append(route)
    def get_routes(self):
        for route in self.routes:
            print(route.origin.name, route.destination.name)
            
    def get_route_origin_list(self):
        return set([self.routes[x].origin.name for x in range(len(self.routes))])
    
    def get_route_destination_list(self):
        return [self.routes[x].destination.name for x in range(len(self.routes))]
            
    def get_destinations_by_origin(self, origin):
        return [route.destination.name for route in self.routes if route.origin.name == origin]
        
    def get_origin_by_destination(self, destination):
        return [route.origin.name for route in self.routes if route.destination.name == destination]


class Flight:
    def __init__(self, route, departure_time, duration, status, date, code, price, available_seats):
        self.flight_id = str(uuid.uuid4()) 
        self.route = route
        self.departure_time = departure_time
        self.duration = duration
        self.status = status
        self.date = date
        self.code = code
        self.price = price
        self.available_seats = available_seats
        
        hour_sum, minute_sum = duration.hour + departure_time.hour, duration.minute + departure_time.minute
        if (minute_sum > 60):
            hour_sum += 1
            minute_sum -= 60
        if hour_sum > 24:
            hour_sum -= 24
        self.arrival_time = Time(hour_sum, minute_sum)
        

    def flight_info(self):
        fInfo = ("From: " + self.route.origin.name + " to: " + self.route.destination.name + " - departure time"
                 + self.departure_time.get_time() + " - duration: " + self.duration.get_time() + " - price: " + str(self.price))
        return fInfo
        
        
class FlightManager:
    def __init__(self):
        self.flights = []
        
    def add_flight(self, flight):
        self.flights.append(flight)
        
    def get_flight_by_id(self, fid):
        for flight in self.flights:
            if flight.flight_id == fid:
                return flight
        print("The flight does not exist")
        
    def get_flights_in_route_and_date(self, origin, destination, date):
        flights = []
        # print("info:", origin, destination, date)
        # print("info2", self.flights[0].route.origin.name, self.flights[0].route.destination.name, self.flights[0].date)
        # print(len(self.flights))
        for i in range(len(self.flights)):
            if (self.flights[i].route.origin.name == origin and self.flights[i].route.destination.name == destination
                and str(self.flights[i].date) == date and self.flights[i].available_seats > 0):
                flights.append(self.flights[i])
                
        if len(flights) == 0:
            print("No flights to display at that date")           
        return flights    
    
    def create_flight_schedule(self, route, departure_time, duration, status, code, 
                               price, available_seats, start_date, days, weekdays):
        current_date = datetime.date.today()
        days_to_advance = days - (current_date.day - start_date.day)

        for i in range(days_to_advance + 1):
            date = current_date + datetime.timedelta(days=i)
            if date.weekday() in weekdays:
                self.flights.append(Flight(route, departure_time, duration, status, date, code, price, available_seats))
  
                
class ClientContainer:
    def __init__(self):
        self.client_list = []
        self.current_client = None
    def add_new_client(self, client):
        self.client_list.append(client)
        self.current_client = client
    def login(self, email, password):
        for i in range(len(self.client_list)):
            if email == self.client_list[i].email and password == self.client_list[i].password:
                print("Login succesfull user: ", email)
                self.current_client = self.client_list[i]
                return True
            else:
                print("Incorrect username or password")
    def logout(self):
        self.current_client = None                


class Client:
    def __init__(self, email, password):
        self.client_id = str(uuid.uuid4()) 
        self.email = email
        self.password = password
        self.tickets = []
    
    def get_tickets(self):
        for ticket in self.tickets:
            print(ticket.flight.code, ticket.flight.route.origin.name)
   
    def buy_ticket(self, flight, passengers, booking_number):
        if (flight.available_seats - len(passengers) < 0):
            print("NOT ENOUGH AVAILABLE SEATS")
            return
        
        #
        flight.available_seats -= len(passengers)
        
        self.tickets.append(Ticket(flight, passengers, booking_number))


class Ticket:
    def __init__(self, flight, passengers, booking_number):
        self.flight = flight
        self.passengers = passengers
        self.booking_number = booking_number
        # clientContainer.current_client.add_ticket(self)


class ServiceContainer:
    def __init__(self):
        self.services = []
        
    def add_service(self, service):
        self.services.append(service)


class Service:
    def __init__(self, name="Basic Service", description="Just the seat", price = 0):
        self.name = name
        self.description = description
        self.price = price
        serviceContainer.add_service(self)
    #     self.add_to_service_container()
    
    # def add_to_service_container(self):
    #     serviceContainer.add_service(self)
        
        
class EconomyClass(Service):
    def __init__(self, price, features):
        super().__init__('Economy Class', 'Basic services', price)
        self.features = features


class BusinessClass(Service):
    def __init__(self, price, features):
        super().__init__('Business Class', 'Enhanced services', price)
        self.features = features
        
        
class Passenger:
    def __init__(self, first_name, surname = "", date_of_birth = "", country="", service_type=""):
        self.first_name = first_name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.country = country
        self.service_type = service_type
        # self.seat = seat
        
    def passenger_info(self):
        pass_info = self.first_name + " " + self.surname
        return pass_info 
        
# BusinessClass(100)
clientContainer = ClientContainer()
flightManager = FlightManager()
routeContainer = RouteContainer()
cityContainer = CityContainer()
serviceContainer = ServiceContainer()

route1 = Route(City(), City())
Route(City("Aarhus"), City("Billund"))
Route(City("Aarhus"), City("Amsterdam"))

Route(City("Billund"), City("Aarhus"))

print(routeContainer.get_destinations_by_origin("Aarhus"))
today = datetime.date.today()
flightManager.create_flight_schedule(route1, Time(1, 2), Time(1, 3), 1, "232", 123, 200, today, 30, [0,1, 2, 3, 4, 5, 6])

flightManager.create_flight_schedule(route1, Time(14, 20), Time(1, 0), 1, "232", 123, 200, today, 30, [0,1, 2, 3, 4, 5, 6])

me = Client("e", "e")
clientContainer.add_new_client(me)
passenger1 = Passenger(first_name="John", surname="Doe", date_of_birth="1990-01-01", country="USA", service_type="Service")
passenger2 = Passenger(first_name="Alice", surname="Smith", date_of_birth="1985-05-15", country="Canada", service_type="Premium Service")
me.buy_ticket(flightManager.flights[0], [passenger1, passenger2], "BK98332")
me.buy_ticket(flightManager.flights[4], [passenger1, passenger2], "BK98332")

clientContainer.login(me.email, me.password)

class FlightSelection:
    def __init__(self, root):
        self.root = root
        self.create_widget()
        
    def create_widget(self):
        # Combobox para mostrar rutas existentes
        self.departure_combobox = ttk.Combobox(self.root, state="readonly")
        self.departure_combobox.pack(pady=10)
        self.departure_combobox.set("From")
        self.departure_combobox.place(x=100, y=40, width=150, height=25)
        self.departure_combobox['values'] = tuple(routeContainer.get_route_origin_list())
        self.departure_combobox.bind('<<ComboboxSelected>>', self.change_destinations_options_by_departure)    

        self.destination_combobox = ttk.Combobox(self.root, state="readonly")
        self.destination_combobox.pack(pady=10)
        self.destination_combobox.set("To")
        self.destination_combobox.place(x=300, y=40, width=150, height=25)
        self.destination_combobox['values'] = tuple(routeContainer.get_route_destination_list())

    def get_origin(self):
        origin = self.departure_combobox.get()
        if origin == "From":
            return False
        return origin
    
    def get_destination(self):
        destination = self.destination_combobox.get()
        if destination == "To":
            return False
        return destination
    
    def change_destinations_options_by_departure(self, event):
        origin = self.departure_combobox.get()
        self.destination_combobox['values'] = tuple(routeContainer.get_destinations_by_origin(origin))
    
    
class FlightDisplay:
    def __init__(self, root, x_coord, y_coord):
        self.root = root
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.flights = ""
        # Lista de strings de ejemplo
        self.string_list = []

        # Crear el marco principal
        self.main_frame = ttk.Frame(root)

    def show_available_flights(self, flights):
        self.main_frame.place(x=self.x_coord, y=self.y_coord, height=300, width=650)
        self.flights = flights
        # Crear un Listbox para mostrar las strings
        self.listbox = tk.Listbox(self.main_frame, selectmode=tk.SINGLE, bg="white", font=("Arial", 12))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=(0, 5))
        # Crear una barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        # scrollbar.place(x=615, y=5, height=290)
        self.prev_selected_index = None
        
        self.string_list = []
        
        for i in range (len(flights)):
            self.string_list.append(flights[i].flight_info())
            
        # Agregar las strings al Listbox con un espacio en blanco al final
        for string in self.string_list:
            self.listbox.insert(tk.END, string)



        # Asociar la función de clic al evento <<ListboxSelect>>
        self.listbox.bind("<<ListboxSelect>>", self.on_item_select)
        
        
    def on_item_select(self, event):
        # Obtener el índice del elemento seleccionado
        selected_index = self.listbox.curselection()
        # print(selected_index[0])

        if selected_index:
            # Restaurar el color original de la cadena seleccionada anteriormente
            if self.prev_selected_index is not None:
                self.listbox.itemconfig(self.prev_selected_index[0], {'bg': 'white'})

            # Cambiar el color de fondo del nuevo elemento seleccionado
            self.listbox.itemconfig(selected_index[0], {'bg': 'lightblue'})

            # Almacenar el índice de la cadena seleccionada actualmente
            self.prev_selected_index = selected_index

            # Obtener el valor de la cadena seleccionada
            selected_value = self.string_list[selected_index[0]]
            print(f"Valor seleccionado: {selected_value}")


    def get_flight_index(self):
        return self.listbox.curselection()[0]
    
    def get_selected_flight(self):
        if (self.listbox.curselection()):
            index = self.listbox.curselection()[0]
            return flightManager.get_flight_by_id(self.flights[index].flight_id)
        print("No hay ningun vuelo seleccionado")
        return False
        
    def hide(self):
        self.main_frame.place_forget()


class Calendar:
    def __init__(self, root):
        self.root = root
        self.active = False
        self.fdate = ""
        self.cal = WCalendar()
        self.create_calendar_button()
        
    def create_calendar(self):
        today = datetime.date.today()
        two_years_later = datetime.date.today() + timedelta(days=365 * 2)
        self.cal = WCalendar(self.root, selectmode='day', year=today.year, month=today.month, day=today.day, mindate=today, maxdate=two_years_later)
        # self.cal.pack(pady=20)
        self.cal.bind("<<CalendarSelected>>", self.on_date_select)
        self.cal.place(x=500, y=70)
        self.active = True

    def on_date_select(self, event):
        # print(datetime(self.cal.get_date()))
        date = self.cal.get_date()
        if len(date) == 7:
            self.fdate = "20" + date[5:7]  + "-" + date[0:2] + "-" + "0" + date[3]
        else:
            self.fdate = "20" + date[6:8]  + "-" + date[0:2] +  "-" + date[3:5]

        return self.fdate
    
    def create_calendar_button(self):
            self.calendar_button = Button(self.root, text="Toggle Calendar", command=self.toggle_calendar)
            self.calendar_button.place(x= 500, y = 40, width=100, height= 30)

    def toggle_calendar(self):
        if self.active:
            print("deactivating")
            self.cal.pack_forget()  # Oculta el calendario si ya está visible
            self.cal.place_forget()
            self.active = False
            # self.cal = Nonez
        else:
            self.create_calendar()  # Muestra el calendario si no está visible
            
    def get_date(self):
        if self.fdate == "":
            return False
        return self.fdate


class PassengerForm:
    SERVICE_OPTIONS = ["Service", "Premium Service", "Super Service"]

    def __init__(self, root):
        # self.add_passenger_callback = add_passenger_callback
        self.root = root

        self.main_frame = ttk.Frame(root)
        
        self.passenger_list = []
        self.first_name_var = tk.StringVar()
        self.surname_var = tk.StringVar()
        self.date_of_birth_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.service_type_var = tk.StringVar()
        self.save_passenger_button = ttk.Button(self.root, text="Add Passenger 1", command=self.save_passenger)

        # self.add_labels()
        
    def add_labels(self):
        # Etiquetas y campos de entrada
        # self.passenger_list.clear()
        self.main_frame.place(x=100, y=200, height=300, width=650)

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
        self.save_passenger_button.place(x=100, y= 450)

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
        # view order and pay
    def hide(self):
        self.main_frame.place_forget()
        self.save_passenger_button.place_forget()
        
    def get_passenger_list(self):
        if len(self.passenger_list) == 0:
            return False
        return self.passenger_list
            
    
class ClientLogin:
    def __init__(self, root):
        style = ttk.Style()
        style.configure("Gray.TFrame", background="gray")
        self.main_frame = ttk.Frame(root, style="Gray.TFrame")
        self.display_user_name = tk.Label(root, text="User:")
        self.display_user_name.place(x=700, y=6)

        self.root = root
        self.root.title("Client Login")

        self.client_container = clientContainer

        # Variables de control para los campos de entrada
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Etiquetas y campos de entrada
        ttk.Label(self.main_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.email_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

        # Botones de Login y Register
        ttk.Button(self.main_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2, pady=10)

    def show_login(self):
        self.main_frame.place(x=350, y=200, height=180, width=210)

    def login(self):
        email = self.email_var.get()
        password = self.password_var.get()

        if self.client_container.login(email, password):
            # Aquí puedes realizar acciones adicionales después del login exitoso
            self.display_user_name.config(text="User: " + email)
            self.hide()
            print("Redirect to main application after successful login.")
        else:
            # Aquí puedes mostrar un mensaje de error al usuario
            print("Login failed.")

    def register(self):
        email = self.email_var.get()
        password = self.password_var.get()
        
        if not email or not password:
            print("Cannot registrer, empty fields")
            return

        self.hide()
        self.display_user_name.config(text="User: " + email)

        new_client = Client(email, password)
        self.client_container.add_new_client(new_client)
    
    def hide(self):
        self.main_frame.place_forget()
    
    
class FlightSummary:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.style.configure("new.TFrame", background="#d3dce6")
        self.counter = 0
        
    def display_flight_summary(self, flight, passenger_list):
        self.main_frame = ttk.Frame(self.root, style="new.TFrame")
        self.style.configure("Flight.TLabel", background="#c3cfdb", font=(None, 13))

        self.main_frame.place(x=225, y= 120, height=375, width=450)
        self.flight = flight
        self.passenger_list = passenger_list
        self.label_list = []
        
        # print(clientContainer.current_client.email)
        # print(flight.flight_info())
        # for passenger in passenger_list:
        #     print(passenger.passenger_info())
        tab = "    "
        arrow = "-------------------->" 
        route_info = ("From: " + self.flight.route.origin.name + tab*2 + arrow
                 + tab*2 + "To: " + self.flight.route.destination.name)
        
        space = " "* 8 + " " * len(self.flight.route.origin.name)
        departure_and_arrival_time = (self.flight.departure_time.get_time() + " hrs" + space +  arrow + tab*2 +
                                      self.flight.arrival_time.get_time() + " hrs")
        # self.create_label(self.main_frame, "")
        self.create_label(self.main_frame, str(self.flight.date) + " - (" + self.flight.code + ")")
        self.create_label(self.main_frame, route_info)
        # self.create_label(self.main_frame, "To:", self.flight.route.destination.name)
        self.create_label(self.main_frame, departure_and_arrival_time)
        # self.create_label(self.main_frame, "")
        # self.create_label(self.main_frame, "Duration:" +  self.flight.duration.get_time())

        self.create_label(self.main_frame, "-/"*38)
        self.create_label(self.main_frame, "Passengers: ")
        self.create_label(self.main_frame, self.passengers_info())

        self.create_label(self.main_frame, "Price" )
        self.create_label(self.main_frame, str(self.flight.price)  + " * "  + str(len(self.passenger_list)) + " Passengers" + 
                          " = " + str(self.flight.price * len(self.passenger_list)))
        # self.create_label(self.main_frame, " = " + str(self.flight.price * len(self.passenger_list)))


    def create_label(self, parent, value):
        print("Add labels")
        ttk.Label(parent, text=f"{value}", style="Flight.TLabel").grid(row=self.counter, column=0, padx=10, pady=5, sticky=tk.W)
        # print(label)
        self.counter += 1
    
    def passengers_info(self):
        passenger_str = ""
        len_passenger_list = len(self.passenger_list)
        for i in range(len_passenger_list-1):
            passenger_str += str(i+1) + " - " + self.passenger_list[i].passenger_info() + "\n"
        passenger_str += str(len_passenger_list) + " - " + self.passenger_list[len_passenger_list-1].passenger_info()
        return passenger_str
    
    def hide(self):
        # self.main_frame.destroy()
        self.main_frame.place_forget()
        for label in self.label_list:
            print(label)
    
class FlightBookingApp:
    def __init__(self, root):
        self.root = root
        self.selected_flight = ""
        self.is_getting_client_tickets = False
        # Crear y agregar widgets a la interfaz utilizando la clase CreateWidget
        self.route_widget = FlightSelection(root)
        self.calendar = Calendar(self.root)
        self.flight_display = FlightDisplay(self.root, 100, 150)
        self.passenger_widget = PassengerForm(self.root)
        self.client_login_widget = ClientLogin(self.root)
        self.flight_summary_widget = FlightSummary(self.root)
        
        line_btn = Button(self.root)
        line_btn.place(x=5, y=30, width= 880, height=4)
        
        search_btn = Button(self.root, text ="search", command = self.search_flight)
        search_btn.place(x=820,y=40)
        
        self.my_bookings_btn = Button(self.root, text ="My Bookings", command = self.show_user_bookings)
        self.my_bookings_btn.place(x=80,y=2)
        
        self.profile_btn = Button(self.root, text ="Profile", command = self.client_login)
        self.profile_btn.place(x=10, y=2)
        
        self.select_flight_btn = tk.Button(self.root, text="Select Flight", command= self.select_flight)
        
        # view order and pay
        self.view_order_and_pay_btn = tk.Button(self.root, text="View order and pay", command= self.check_out)

        self.complete_order_btn = tk.Button(self.root, text="Click here to confirm the order", command= self.finish_order)

            # TEST ------------------        
        # self.selected_flight = flightManager.flights[0]
        # passenger1 = Passenger(first_name="John", surname="Doe", date_of_birth="1990-01-01", country="USA", service_type="Service")
        # passenger2 = Passenger(first_name="Alice", surname="Smith", date_of_birth="1985-05-15", country="Canada", service_type="Premium Service")
        # self.flight_summary_widget.display_flight_summary(self.selected_flight, [passenger1, passenger2])


# //////////////////////////////////////////////////////7


    def show_user_bookings(self):
        if not clientContainer.current_client:
            return print("You need to log in to see your bookings")
        
        if len(clientContainer.current_client.tickets) == 0:
            return print("There are no flights to select")
        
        client_flights = [ticket.flight for ticket in clientContainer.current_client.tickets]
        self.flight_display.show_available_flights(client_flights)
        # self.select_flight_in_bookings_btn = tk.Button(self.root, text="Select Flight", command= self.select_flight)

        self.close_btn = tk.Button(self.root, text=" X ",  bg="blue", fg="white", 
                                   command= lambda:(self.flight_summary_widget.hide(), self.close_btn.place_forget()))

        self.select_flight_in_bookings_btn = tk.Button(self.root, text="Select Flight", 
            command=lambda: (self.flight_summary_widget.display_flight_summary(
                self.flight_display.get_selected_flight(),
                clientContainer.current_client.tickets[self.flight_display.get_flight_index()].passengers
            ),
            self.close_btn.place(x=650, y=95)
            )
        )
        self.select_flight_in_bookings_btn.place(x= 100, y=500)


    def finish_order(self):
        # self.booking_number = str(uuid.uuid4()) 
        clientContainer.current_client.buy_ticket(self.select_flight, self.passenger_widget.get_passenger_list, str(uuid.uuid4()))
        # self.ticket = Ticket(self.selected_flight, self.passenger_widget.get_passenger_list(), self.booking_number)
        
    # When view_order_and_pay_button is pressed
    def check_out(self):
        if not self.passenger_widget.get_passenger_list():
            print("You need to add a passenger to buy a tikcet")
            return
        
        if (len(self.passenger_widget.get_passenger_list()) > self.selected_flight.available_seats):
            print("Only " +  str(self.selected_flight.available_seats) + " seats left")
            return 
        
        self.passenger_widget.hide()
        self.view_order_and_pay_btn.place_forget()
        
        # click here to confirm the order
        
        # login or register to confirm the order
        
        if not clientContainer.current_client:
            self.complete_order_btn["text"] = "Login or Register \n to complete Order"
        
        else:
            self.complete_order_btn.place(x=100, y = 450)

        # if not clientContainer.current_client:
        #     self.client_login_widget.show_login()
            #create account
        self.flight_summary_widget.display_flight_summary(self.selected_flight, self.passenger_widget.get_passenger_list())
        

    def client_login(self):
        self.client_login_widget.show_login()
        
    def search_flight(self):
        self.calendar.toggle_calendar()
        origin = self.route_widget.get_origin()
        destination = self.route_widget.get_destination()
        date = self.calendar.get_date()
        
        if (origin and destination and date):
            flighs_list = flightManager.get_flights_in_route_and_date(origin, destination, date)
            self.flight_display.show_available_flights(flighs_list)
            self.select_flight_btn.place(x=100, y=500)
        else:
            print("error, tiene que completar todos los campos")
        
    def select_flight(self):
        self.selected_flight = self.flight_display.get_selected_flight()
        
        if not self.selected_flight:
            print("no flight selected")
            return
    
        self.select_flight_btn.place_forget()
        self.flight_display.hide()
        self.passenger_widget.add_labels()
        self.view_order_and_pay_btn.place(x= 225, y= 450)

        
# Función principal para ejecutar la aplicacion
def main():
    root = tk.Tk()
    root.title("Flight Booking App")
    root.geometry("900x600")
    app = FlightBookingApp(root)
    root.mainloop()
main()
