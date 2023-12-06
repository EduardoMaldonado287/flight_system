from tkinter import *
from tkcalendar import Calendar
from datetime import datetime, timedelta

# Crear objeto Tk
root = Tk()

# Establecer geometría
root.geometry("400x400")

# Añadir calendario
today = datetime.today().date()
two_years_later = datetime.today().date() + timedelta(days=365 * 2)
cal = Calendar(root, selectmode='day', year=today.year, month=today.month, day=today.day, mindate=today, maxdate=two_years_later)
cal.pack(pady=20)


def on_date_select(event):
    return print(cal.get_date())
  
cal.bind("<<CalendarSelected>>", on_date_select)

# Ejecutar interfaz gráfica
root.mainloop()


# def get_date():
#     selected_date = cal.get_date()
#     # date.config(text="Selected Date is: " + selected_date)
#     print(selected_date)

# Añadir botón y etiqueta
# Button(root, text="Get Date", command=get_date).pack(pady=20)

# date = Label(root, text="CALENDARIO")
# date.pack(pady=20)
