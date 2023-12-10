class Vehicle:
    def __init__(self):
        self.a= 1

    def create_atr(self, brand, model):
        self.brand = brand
        self.model = model
        
    def display_info(self):
        print(f"Vehicle: {self.brand} {self.model}")
        

class Car(Vehicle):
    def __init__(self, num_doors):
        super().__init__()  # Calling the constructor of the base class
        self.num_doors = num_doors

    def display_info(self):  # Overriding the display_info method in the derived class
        super().display_info()  # Calling the display_info method of the base class
        print(super().brand)
        print(f"Number of doors: {self.num_doors}")

v1 = Vehicle()
v1.create_atr("ford", "attitude")
# Creating an instance of the Car class
my_car = Car(num_doors=4)

# Calling the display_info method of the Car class
my_car.display_info()
