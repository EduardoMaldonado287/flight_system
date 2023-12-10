import datetime
import uuid
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar as WCalendar
from datetime import timedelta

is_testing = True
app = None


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
        fInfo = ("From: " + self.route.origin.name + "   === >   to: " + self.route.destination.name + "   |   Time: "
                 + self.departure_time.get_time() + "   |   Duration: " + self.duration.get_time() + "   |   price: " + str(self.price))
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
        return False
        
    def get_flights_in_route_and_date(self, origin, destination, date):
        flights = []
        for i in range(len(self.flights)):
            if (self.flights[i].route.origin.name == origin and self.flights[i].route.destination.name == destination
                and str(self.flights[i].date) == date and self.flights[i].available_seats > 0):
                flights.append(self.flights[i])
                
        if len(flights) == 0:
            print("No flights to display at that date")    
            return False       
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
                # print("Login succesfull user: ", email)
                self.current_client = self.client_list[i]
                print("THE LOGIN IS SUCCESFULL, CHANGED CURRENT CLIENT")
                return True
        return False
    
    def logout(self):
        self.current_client = None                

    def is_user_unique(self, email):
        return len([0 for client in self.client_list if client.email == email])
    
    
class Client:
    def __init__(self, email, password):
        self.client_id = str(uuid.uuid4()) 
        self.email = email
        self.password = password
        self.tickets = []
    
    def get_tickets(self):
        for ticket in self.tickets:
            print(ticket.flight.code, ticket.passengers[0].first_name)
   
    def buy_ticket(self, flight, passengers, booking_number):        
        flight.available_seats -= len(passengers)
        new_ticket = Ticket(flight, passengers, booking_number)
        self.tickets.append(new_ticket)
        return True


class Ticket:
    def __init__(self, flight, passengers, booking_number):
        self.flight = flight
        self.passengers = passengers
        self.booking_number = booking_number


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
        self.features = ["1 luggage"]
        serviceContainer.add_service(self)
        
        
class EconomyClass(Service):
    def __init__(self, price, features):
        super().__init__('Economy Class', 'Basic services', price)
        self.features = ["2 luggage"]


class BusinessClass(Service):
    def __init__(self, price, features):
        super().__init__('Business Class', 'Enhanced services', price)
        self.features = ["3 luggage", "Fast track"]
        
        
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
        
clientContainer = ClientContainer()
flightManager = FlightManager()
routeContainer = RouteContainer()
cityContainer = CityContainer()
serviceContainer = ServiceContainer()

route2 = Route(City("Aarhus"), City("Billund"))
route3 = Route(City("Aalborg"), City("Berlin"))
route4= Route(City("Billund"), City("Aarhus"))

today = datetime.date.today()
flightManager.create_flight_schedule(route2, Time(1, 2), Time(1, 3), 1, "232", 123, 200, today, 60, [0,1, 2, 3, 4, 5, 6])
flightManager.create_flight_schedule(route3, Time(18, 00), Time(2, 0), 1, "232", 500, 200, today, 60, [0,1, 2, 3, 4, 5, 6])
flightManager.create_flight_schedule(route4, Time(20, 30), Time(1, 0), 1, "232", 1000, 200, today, 60, [0,1, 2, 3, 4, 5, 6])

me = Client("e", "e")
clientContainer.add_new_client(me)
passenger1 = Passenger(first_name="John", surname="Doe", date_of_birth="1990-01-01", country="USA", service_type="Service")
me.buy_ticket(flightManager.flights[0], [passenger1], "BK98332")

class FlightBookingApp:
    def __init__(self, root):
        self.root = root
        self.selected_flight = ""
        self.is_getting_client_tickets = False
        self.route_widget = FlightSelection(self.root)
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
        
        self.profile_btn = Button(self.root, text ="Profile", command = self.client_login_widget.show_login)
        self.profile_btn.place(x=10, y=2)
    
        self.select_flight_btn = tk.Button(self.root, text="Select Flight", command= self.select_flight)
        
        self.view_order_and_pay_btn = tk.Button(self.root, text="View order and pay", command= self.check_out)

        self.complete_order_btn = tk.Button(self.root, text="Click here to confirm the order", command= self.finish_order)

        self.purchase_completed_label = tk.Label(self.root, text="")
        
        self.my_booking_label = tk.Label(self.root, text= "Your trips:", font=(None, 14))

        self.select_flight_in_bookings_btn = tk.Button(self.root, text="View Flight", 
            command=lambda: (self.flight_summary_widget.display_flight_summary(
                self.flight_display.get_selected_flight(),
                clientContainer.current_client.tickets[self.flight_display.get_flight_index()].passengers
            ),
            self.close_btn.place(x=650, y=95),
            )
        )
        
    def show_user_bookings(self):
        if not clientContainer.current_client:
            return print("You need to log in to see your bookings")
        
        if len(clientContainer.current_client.tickets) == 0:
            return print("There are no flights to select")
        
        self.hide_widgets()
        self.my_booking_label.place(x=100, y= 120)
        
        client_flights = [ticket.flight for ticket in clientContainer.current_client.tickets]
        self.flight_display.show_available_flights(client_flights)
        self.close_btn = tk.Button(self.root, text=" X ",  bg="blue", fg="white", 
                                   command= lambda:(self.flight_summary_widget.hide(), self.close_btn.place_forget()))
        self.select_flight_in_bookings_btn.place(x= 100, y=500)

    def finish_order(self):
        if not clientContainer.current_client:
            print("Log in first")
            return False
        
        booking_number = str(uuid.uuid4())
        if (clientContainer.current_client.buy_ticket(self.selected_flight, self.passenger_widget.get_passenger_list(), booking_number)):
            self.purchase_completed_label.config(text=str("Order completed \n Booking number: " 
                + booking_number + '\nClick on "My bookings" to see your tickets'), font=(None, 12)) 
            self.purchase_completed_label.place(x=220, y=520)
            self.complete_order_btn.place_forget()
            
        else:
            return print("Cannot flinish order")

    # When view_order_and_pay_button is pressed
    def check_out(self):
        if not self.passenger_widget.get_passenger_list():
            print("You need to add a passenger to buy a tikcet")
            return False
        
        # This is the original function, but there are two
        if (len(self.passenger_widget.get_passenger_list()) > self.selected_flight.available_seats):
            print("Cannot buy, only " +  str(self.selected_flight.available_seats) + " seats left")
            return False
        
        self.passenger_widget.hide()
        self.view_order_and_pay_btn.place_forget()
        self.flight_summary_widget.display_flight_summary(self.selected_flight, self.passenger_widget.get_passenger_list())

        if not clientContainer.current_client:
            print("You need to register first in order to buy")
            self.client_login_widget.show_login()
        
        self.complete_order_btn.place(x=220, y = 520)
        
    def search_flight(self):
        self.calendar.hide()
        origin = self.route_widget.get_origin()
        destination = self.route_widget.get_destination()
        date = self.calendar.get_date()
        
        if (origin and destination and date):
            app.hide_widgets()
            flighs_list = flightManager.get_flights_in_route_and_date(origin, destination, date)
            self.flight_display.show_available_flights(flighs_list)
            self.select_flight_btn.place(x=100, y=500)
        else:
            print("error, tiene que completar todos los campos")
        
    def select_flight(self):
        self.selected_flight = self.flight_display.get_selected_flight()
        
        if not self.selected_flight:
            return print("no flight selected")

        self.select_flight_btn.place_forget()
        self.flight_display.hide()
        self.passenger_widget.add_labels()
        self.view_order_and_pay_btn.place(x= 225, y= 450)
        self.view_order_and_pay_btn.lift()

    def hide_widgets(self):
        elements_to_hide = [
            self.flight_display, 
            self.flight_summary_widget, 
            self.complete_order_btn, 
            self.select_flight_btn, 
            self.purchase_completed_label,
            self.passenger_widget, 
            self.select_flight_in_bookings_btn, 
            self.my_booking_label
        ]

        for element in elements_to_hide:
            try:
                element.hide() if hasattr(element, 'hide') else element.place_forget()
            except Exception as e:
                print(f"Unable to hide or place_forget: {e}")

            
class FlightSelection:
    def __init__(self, root):
        self.root = root
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
        self.string_list = []
        self.main_frame = ttk.Frame(self.root)
        self.listbox = tk.Listbox(self.main_frame, selectmode=tk.SINGLE, bg="white", font=("Arial", 12))

    def show_available_flights(self, flights):
        self.main_frame.place(x=self.x_coord, y=self.y_coord, height=300, width=650)
        self.listbox.delete(0, tk.END)

        self.flights = flights
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=(0, 5))
        # scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        # scrollbar.place(x=615, y=5, height=290)
        self.prev_selected_index = None
        self.string_list = []
        
        if not flights:
            self.listbox.insert(0, "NO FLIGHTS AT THE SELECTED DATE, TRY OTHER DAY")
            return False
            
        for i in range (len(flights)):
            self.string_list.append(flights[i].flight_info())
            
        for string in self.string_list:
            self.listbox.insert(tk.END, string)

        self.listbox.bind("<<ListboxSelect>>", self.on_item_select)
    
    def on_item_select(self, event):
        selected_index = self.listbox.curselection()

        if selected_index:
            # Restore item original color
            if self.prev_selected_index is not None:
                self.listbox.itemconfig(self.prev_selected_index[0], {'bg': 'white'})

            # change item color
            self.listbox.itemconfig(selected_index[0], {'bg': 'lightblue'})

            self.prev_selected_index = selected_index

    def get_flight_index(self):
        if not self.listbox.curselection():
            print("not flight selected")
            return False
        return self.listbox.curselection()[0]
    
    def get_selected_flight(self):
        if (self.listbox.curselection() and self.flights):
            index = self.listbox.curselection()[0]
            return flightManager.get_flight_by_id(self.flights[index].flight_id)
        print("No hay ningun vuelo seleccionado")
        return False
        
    def hide(self):
        self.main_frame.place_forget()
        self.listbox.pack_forget()


class Calendar:
    def __init__(self, root):
        self.root = root
        self.active = False
        self.fdate = ""
        self.cal = WCalendar()
        self.calendar_button = Button(self.root, text="Select Date", command=self.toggle_calendar)
        self.calendar_button.place(x= 500, y = 40, width=100, height= 30)

    def create_calendar(self):
        today = datetime.date.today()
        two_years_later = datetime.date.today() + timedelta(days=365 * 2)
        self.cal = WCalendar(self.root, selectmode='day', year=today.year, month=today.month, day=today.day, mindate=today, maxdate=two_years_later)
        self.cal.bind("<<CalendarSelected>>", self.on_date_select)
        self.cal.place(x=500, y=70)
        self.active = True

    def on_date_select(self, event):
        date = self.cal.get_date()
        parsed_date = datetime.datetime.strptime(date, "%m/%d/%y")
        self.fdate = parsed_date.strftime("%Y-%m-%d")
        fdate_btn = parsed_date.strftime("%d-%m-%Y")
        self.calendar_button.config(text=fdate_btn)
        return self.fdate
    
    def toggle_calendar(self):
        if self.active:
            self.cal.place_forget()
            self.active = False
        else:
            self.create_calendar() 
            
    def hide(self):
        self.cal.place_forget()
        self.active = False
        
    def get_date(self):
        if self.fdate == "":
            return False
        return self.fdate


class PassengerForm:
    SERVICE_OPTIONS = ["Basic Service", "Economy Class", "Business Class"]
    
    def __init__(self, root):
        self.root = root
        self.passenger_list = []
        self.first_name_var = tk.StringVar()
        self.surname_var = tk.StringVar()
        self.date_of_birth_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.service_type_var = tk.StringVar()


    def add_labels(self):
        self.main_frame = ttk.Frame(self.root)
        self.save_passenger_button = ttk.Button(self.root, text="Add Passenger 1", command=self.save_passenger)
        self.save_passenger_button.place(x=100, y= 450)
        self.passenger_count = 0
        self.save_passenger_button["text"] = "Add Passenger 1"
        self.passenger_list = []
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
                
    def save_passenger(self):
        if not is_testing:
            if (not self.first_name_var.get() or not self.surname_var.get() or not self.date_of_birth_var.get()
                or not self.country_var.get() or not self.service_type_var.get()):
                print("Tiene que completar todos los campos")
                return
        
        passenger = Passenger(
            first_name=self.first_name_var.get(),
            surname=self.surname_var.get(),
            date_of_birth=self.date_of_birth_var.get(),
            country=self.country_var.get(),
            service_type=self.service_type_var.get() # Match service with type ...
        )
        
        self.passenger_list.append(passenger)
        self.first_name_var.set("")
        self.surname_var.set("")
        self.date_of_birth_var.set("") 
        self.country_var.set("")
        self.service_type_var.set("") 
        self.passenger_count += 1

        # Update passenger button
        self.save_passenger_button["text"] = f"Add Passenger {self.passenger_count+1}"
        
    def hide(self):
        self.main_frame.destroy()
        self.save_passenger_button.place_forget()
        
    def get_passenger_list(self):
        if len(self.passenger_list) == 0:
            return False
        return self.passenger_list
            
    
class ClientLogin:
    def __init__(self, root):
        self.root = root
        style = ttk.Style()
        style.configure("Gray.TFrame", background="gray")
        self.display_user_name = tk.Label(root, text="User:")
        self.display_user_name.place(x=700, y=6)
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.show_close_btn = False
        self.main_frame = ttk.Frame(self.root, style="Gray.TFrame")
        self.close_btn = tk.Button(self.root, text=" X ", bg="red", fg="white", 
                                   command= lambda:(self.hide(), self.close_btn.place_forget()))
        
    def show_login(self, show_close_btn = False):
        self.show_close_btn = show_close_btn
        self.main_frame.place(x=350, y=200, height=190, width=210)
        self.main_frame.lift()

        ttk.Label(self.main_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.email_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

        # Log in, register, and log out buttons
        ttk.Button(self.main_frame, text="Log in", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2, pady=2)
        ttk.Button(self.main_frame, text="Log out", command=self.logout).grid(row=4, column=0, columnspan=2, pady=15)
        
        if show_close_btn:
            self.close_btn.place(x=536, y=174)
            self.close_btn.lift()

    def logout(self):
        if clientContainer.current_client == None:
            print("You need to log in first")
            return False
        
        clientContainer.current_client = None
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.close_btn.place_forget()
        self.hide()
        self.display_user_name.config(text="User: ")
        print("Log out Succesfull")
        if not self.show_close_btn:
            app.hide_widgets()

    def login(self):
        email = self.email_var.get()
        password = self.password_var.get()

        if clientContainer.login(email, password):
            self.display_user_name.config(text="User: " + email)
            self.hide()
            self.close_btn.place_forget()
            print("Redirect to main application after successful login.")
        else:
            print("Login failed")

        if not self.show_close_btn:
            app.hide_widgets()
            
    def register(self):
        email = self.email_var.get()
        password = self.password_var.get()
        
        if not email or not password:
            print("Cannot registrer, empty fields")
            return
        
        if clientContainer.is_user_unique(email):
            print("User already exists, log in or try different username")
            return
            
        self.close_btn.place_forget()
        self.hide()
        self.display_user_name.config(text="User: " + email)
        new_client = Client(email, password)
        clientContainer.add_new_client(new_client)
        print("Register successfull")    

    def hide(self):
        self.main_frame.place_forget()
        
    
class FlightSummary:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.style.configure("new.TFrame", background="#d3dce6")
        self.counter = 0

    def display_flight_summary(self, flight, passenger_list=[]):    
        self.main_frame = ttk.Frame(self.root, style="new.TFrame")
        self.style.configure("Flight.TLabel", background="#c3cfdb", font=(None, 13))
        self.main_frame.place(x=225, y= 120, height=375, width=450)
        self.flight = flight
        self.passenger_list = passenger_list
        self.label_list = []
        
        tab = "    "
        arrow = "-------------------->" 
        route_info = ("From: " + self.flight.route.origin.name + tab*2 + arrow + tab*2 
            + "To: " + self.flight.route.destination.name)
        space = " "* 8 + " " * len(self.flight.route.origin.name)
        departure_and_arrival_time = (self.flight.departure_time.get_time() + " hrs" + space +  arrow + tab*2 +
                                      self.flight.arrival_time.get_time() + " hrs")
        
        self.create_label(str(self.flight.date) + " - (" + self.flight.code + ")")
        self.create_label(route_info)
        self.create_label(departure_and_arrival_time)
        self.create_label("-/"*38)
        self.create_label("Passengers: ")
        self.create_label(self.passengers_info())
        self.create_label("Price" )
        self.create_label(str(self.flight.price)  + " * "  + str(len(self.passenger_list)) + " Passengers" + 
                          " = " + str(self.flight.price * len(self.passenger_list)))

    def create_label(self, value):
        self.label_list.append(ttk.Label(self.main_frame, text=f"{value}", 
            style="Flight.TLabel").grid(row=self.counter, column=0, padx=10, pady=5, sticky=tk.W))
        self.counter += 1
    
    def passengers_info(self):
        passenger_str = ""
        len_passenger_list = len(self.passenger_list)
        for i in range(len_passenger_list-1):
            passenger_str += str(i+1) + " - " + self.passenger_list[i].passenger_info() + "\n"
        passenger_str += str(len_passenger_list) + " - " + self.passenger_list[len_passenger_list-1].passenger_info()
        return passenger_str
    
    def hide(self):
        self.main_frame.destroy()
    
    
def main():
    global app
    root = tk.Tk()
    root.title("Flight Booking App")
    root.geometry("900x600")
    app = FlightBookingApp(root)
    root.mainloop()
main()

