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
        return str(self.hour) + ":" + str(self.minute)
        

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

    def flight_info(self):
        return(self.date, self.departure_time.get_time(), self.duration.get_time(), self.price)
        
        
class FlightManager:
    def __init__(self):
        self.flights = []
        
    def add_flight(self, flight):
        self.flights.append(flight)
        
    # def get_flights(self):
    #     for flight in self.flights:
    #         print(flight.flight_info())
        
    def get_flights_in_route_and_date(self, origin, destination, date):
        flights = []
        print("info:", origin, destination, date)
        print("info2", self.flights[0].route.origin.name, self.flights[0].route.destination.name, self.flights[0].date)
        print(len(self.flights))
        for i in range(len(self.flights)):
            if (self.flights[i].route.origin.name == origin and self.flights[i].route.destination.name == destination
                and str(self.flights[i].date) == date):
                flights.append(str(self.flights[i].price))
                
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
        self.current_client = Client("me", "pass")
    def add_new_client(self, client):
        self.client_list.append(client)
    def login(self, email, password):
        for i in range(len(self.client_list)):
            if email == self.client_list[i].email and password == self.client_list[i].password:
                print("Login succesfull user: ", email)
                self.current_client = self.client_list[i]
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
        flight.available_seats -= len(passengers)
        
        self.tickets.append(Ticket(flight, passengers, booking_number))


class Ticket:
    def __init__(self, flight, passengers, booking_number):
        self.flight = flight
        self.passengers = passengers
        self.booking_number = booking_number
        # clientContainer.current_client.add_ticket(self)
   
        
class Service:
    def __init__(self, name="Basic Service", description="Just the seat", price = 0):
        self.name = name
        self.description = description
        self.price = price
   
        
class Passenger:
    def __init__(self, first_name, surname = "", date_of_birth = "", country="", service_type=Service()):
        self.first_name = first_name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.country = country
        self.service_type = service_type
        # self.seat = seat


class EconomyClass(Service):
    def __init__(self, price, features):
        super().__init__('Economy Class', 'Basic services', price)
        self.features = features


class BusinessClass(Service):
    def __init__(self, price, features):
        super().__init__('Business Class', 'Enhanced services', price)
        self.features = features
        

clientContainer = ClientContainer()
flightManager = FlightManager()
routeContainer = RouteContainer()
cityContainer = CityContainer()

route1 = Route(City(), City())
Route(City("Aarhus"), City("Billund"))
Route(City("Aarhus"), City("Amsterdam"))

Route(City("Billund"), City("Aarhus"))

print(routeContainer.get_destinations_by_origin("Aarhus"))
today = datetime.date.today()
flightManager.create_flight_schedule(route1, Time(1, 2), Time(1, 3), 1, "232", 123, 200, today, 30, [0,1, 2, 3, 4, 5, 6])


class FlightSelection:
    def __init__(self, root):
        self.root = root

    def create_widget(self):
        # Combobox para mostrar rutas existentes
        self.departure_combobox = ttk.Combobox(self.root, state="readonly")
        self.departure_combobox.pack(pady=10)
        self.departure_combobox.set("From")
        self.departure_combobox.place(x=100, y=30, width=150, height=25)
        self.departure_combobox['values'] = tuple(routeContainer.get_route_origin_list())
        self.departure_combobox.bind('<<ComboboxSelected>>', self.change_destinations_options_by_departure)    

        self.destination_combobox = ttk.Combobox(self.root, state="readonly")
        self.destination_combobox.pack(pady=10)
        self.destination_combobox.set("To")
        self.destination_combobox.place(x=300, y=30, width=150, height=25)
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

        # Lista de strings de ejemplo
        self.string_list = []

        # Crear el marco principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.place(x=x_coord, y=y_coord, height=300, width=500)

    def create_display(self, values):

        # Crear un Listbox para mostrar las strings
        self.listbox = tk.Listbox(self.main_frame, selectmode=tk.SINGLE, bg="white", font=("Arial", 12))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=(0, 5))

        self.string_list = values
        # Agregar las strings al Listbox con un espacio en blanco al final
        for string in self.string_list:
            self.listbox.insert(tk.END, string + "\n" + ".")

        # Crear una barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.place(x=465, y=5, height=290)

        self.prev_selected_index = None

        # Asociar la función de clic al evento <<ListboxSelect>>
        self.listbox.bind("<<ListboxSelect>>", self.on_item_select)
        
        
    def on_item_select(self, event):
        # Obtener el índice del elemento seleccionado
        selected_index = self.listbox.curselection()

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

    def add_items(self, lista):
        self.string_list.extend(lista)
        
    def get_flights(self, flights):
        pass

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
        self.cal.place(x=500, y=30)
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
            self.calendar_button.place(x= 500, y = 30, width=100, height= 30)

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
            
class FlightBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Booking App")
        root.geometry("900x600")

        # Crear y agregar widgets a la interfaz utilizando la clase CreateWidget
        self.route_widget = FlightSelection(root)
        self.route_widget.create_widget()

        self.calendar = Calendar(self.root)
        
        search_btn = Button(self.root, text ="search", command = self.get_flight_params)
        search_btn.place(x=820,y=30)
        
        self.display = FlightDisplay(self.root, 200, 200)
        
        # display.add_items(["hola", "aidos"])
        
        
    def get_flight_params(self):
        origin = self.route_widget.get_origin()
        destination = self.route_widget.get_destination()
        date = self.calendar.get_date()
        
        if (origin and destination and date):
            print(origin, destination, date)
            flighs_list = flightManager.get_flights_in_route_and_date(origin, destination, date)
            self.display.create_display(flighs_list)
        else:
            print("error")
        
# Función principal para ejecutar la aplicación
def main():
    root = tk.Tk()
    app = FlightBookingApp(root)
    root.mainloop()

main()
