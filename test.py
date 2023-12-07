import tkinter as tk
from tkinter import ttk

class ClientContainer:
    def __init__(self):
        self.client_list = []
        self.current_client = None

    def add_new_client(self, client):
        self.client_list.append(client)
        print("Registration successful for user:", client.email)

    def login(self, email, password):
        for i in range(len(self.client_list)):
            if email == self.client_list[i].email and password == self.client_list[i].password:
                print("Login successful user:", email)
                self.current_client = self.client_list[i]
                return True
        print("Incorrect username or password")
        return False

    def logout(self):
        self.current_client = None

class Client:
    def __init__(self, email, password):
        self.client_id = email  # Utilizamos el email como ID para simplificar el ejemplo
        self.email = email
        self.password = password

# Clase para la interfaz gráfica
class ClientLoginApp:
    def __init__(self, root):
        self.main_frame = ttk.Frame(root)
        self.main_frame.place(x=100, y=100, height=300, width=300)

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

    def login(self):
        email = self.email_var.get()
        password = self.password_var.get()

        if self.client_container.login(email, password):
            # Aquí puedes realizar acciones adicionales después del login exitoso
            print("Redirect to main application after successful login.")
        else:
            # Aquí puedes mostrar un mensaje de error al usuario
            print("Login failed.")

    def register(self):
        email = self.email_var.get()
        password = self.password_var.get()

        new_client = Client(email, password)
        self.client_container.add_new_client(new_client)

clientContainer = ClientContainer()

def main():
    root = tk.Tk()
    root.geometry("900x600")
    app = ClientLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
