from canvasapi import Canvas
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk

import sv_ttk

import datetime

def assignment_list(ass: list) -> str:
    msg = ""

    for assign in ass:
        nombre = assign["nombre"]

        try:
            fecha = datetime.datetime.fromisoformat(assign["fecha_fin"])
            fecha = fecha.strftime("%d/%m/%y")
        except TypeError:
            fecha = None
            msg += f"- {nombre} | Sin fecha límite\n"
        else:
            msg += f"- {nombre} | Entregar antes de {fecha}\n"

    return msg


############################################################################
API_URL = "https://cursos.canvas.uc.cl/"

API_KEY = "8976~v6mGRCmNZ446NC7JKuk4vhGUR42h2E6RUULEKa6FJL6YMTkyRPRGuWaVRhMPWJuW"
############################################################################


canvas = Canvas(API_URL, API_KEY)

user = canvas.get_current_user()



courses = user.get_courses()
course_info = dict()

for course in courses:
    #print(course.name)
    #print(course.course_code)
    course_info[course.name] = {"id": course.id, "assignments": []}
    assignments = course.get_assignments()
    
    for p in assignments:
        course_info[course.name]["assignments"].append(
        {
            "nombre": p.name,
            "fecha_fin": p.due_at,
        })

        #print(assignment)

# --------------- 

root = tk.Tk()
root.title("Visualizador de Canvas")
root.geometry("800x500")

left_panel = ctk.CTkFrame(
    root,
    width=300,
    height=500,
    border_width = 2,
    border_color= "#4E545C",
    fg_color= "#000000",
)
left_panel.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)

right_panel = ctk.CTkFrame(
    root,
    border_width = 2,
    border_color= "#4E545C",
    fg_color= "#000000",
)
right_panel.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.BOTH, expand=True)

label1 = tk.Label(
    left_panel,
    text = "Buscar cursos: ",
    fg = "black",
    font= ("Arial", 12)
)
label1.pack(padx= 10, pady=10)

selected_course = tk.StringVar()

search1 = ttk.Combobox(
    left_panel,
    state = "readonly",
    values= list(course_info.keys()),
    textvariable=selected_course,
    width = 25,
    font = ("Roboto", 12)
)
search1.pack(pady= 10)

display_label = tk.Label(
    right_panel,
    text = "Selecciona un curso para visualizar...",
    font = ("Roboto", 12),
    justify="left",
    bg= "#000000"
)
display_label.pack()

display_course_text = tk.Label(
    right_panel,
    text = "Este es un curso de la Universidad Católica",
    justify = "left",
    font = ("Roboto", 12),
    anchor="nw",
    bg= "#000000",
)
display_course_text.pack()

assignment_frame = ctk.CTkFrame(
    right_panel,
    corner_radius= 15,
    border_width= 2,
    border_color= "#4E545C",
    fg_color= "#000000",
    width = 200,
    height = 150
)
assignment_frame.pack(padx=5, pady=5, anchor="nw", fill="none", expand=True)

def update_label(event):
    current_course = selected_course.get()
    print(current_course)

    display_label.config(text= current_course)
    display_course_text.config(text= assignment_list(course_info[current_course]["assignments"]))
        
search1.bind("<<ComboboxSelected>>", update_label)


sv_ttk.set_theme("dark")

root.mainloop()