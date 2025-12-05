from canvasapi import Canvas
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import sv_ttk


############################################################################
API_URL = "https://cursos.canvas.uc.cl/"

API_KEY = "8976~v6mGRCmNZ446NC7JKuk4vhGUR42h2E6RUULEKa6FJL6YMTkyRPRGuWaVRhMPWJuW"
############################################################################


canvas = Canvas(API_URL, API_KEY)

user = canvas.get_current_user()



courses = user.get_courses()
course_list = list()
course_list_id = list()
assignments_list = list()

zip_pares = zip(course_list, course_list_id)

dict_courses_id = dict(zip_pares)

for course in courses:
    #print(course.name)
    #print(course.course_code)
    course_list.append(course.name)
    course_list_id.append(course.id)
    assignments = course.get_assignments()
    
    
    for assignment in assignments:
        assignments_list.append(assignment.name)
        #print(assignment)

# --------------- 

root = tk.Tk()
root.title("Visualizador de Canvas")
root.geometry("800x500")

left_panel = tk.Frame(
    root,
    width=300,
    height=500,
    bd=2, relief=tk.GROOVE
)
left_panel.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)

right_panel = tk.Frame(
    root,
    bd = 2, relief=tk.GROOVE
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
    values=course_list,
    textvariable=selected_course
)
search1.pack(pady= 10)

display_label = tk.Label(
    right_panel,
    text = "Selecciona un curso para visualizar...",
    font = ("Arial", 12),
    justify="left"
)
display_label.pack()

display_course_text = tk.Label(
    right_panel,
    text = "Este es un curso de la Universidad Católica",
    justify = "left",
    anchor="nw"
)
display_course_text.pack()

assignment_frame = tk.Frame(
    
)

def update_label(event):
    current_course = selected_course.get()
    print(current_course)

    display_label.config(text= current_course)
        
search1.bind("<<ComboboxSelected>>", update_label)


sv_ttk.set_theme("dark")

root.mainloop()