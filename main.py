from canvasapi import Canvas
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
from PIL import ImageTk, Image
import json

import sv_ttk

import datetime

def assignment_list(ass: list) -> str:
    cubos = []

    for assign in ass:
        msg = ""
        nombre = assign["nombre"]

        try:
            fecha = datetime.datetime.fromisoformat(assign["fecha_fin"])
            fecha = fecha.strftime("%d/%m/%y")
        except TypeError:
            fecha = None
            msg += f"<< {nombre} >>\nSin fecha límite"
        else:
            msg += f"<< {nombre} >>\nEntregar antes de {fecha}"

        cubos.append(msg)
    
    return cubos


# REINGRESAR TOKENS PROPIOS

with open("user_config.json", mode="r") as info_user:
    info_canva = json.load(info_user)

############################################################################
api_url = info_canva["API_URL"]
api_token = info_canva["API_TOKEN"]
############################################################################

canvas = Canvas(api_url, api_token)
user = canvas.get_current_user()


courses = user.get_favorite_courses() # REEMPLAZAR POR .get_favorite_courses() en caso de no reconocer los dictados actualmente
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
root.minsize(800, 500)

entry = ctk.CTkEntry(master=root,
                               placeholder_text="CTkEntry",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

left_panel = ctk.CTkFrame(
    root,
    width=250,
    height=800,
    fg_color= "#000000",
)
left_panel.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)
left_panel.pack_propagate(False)

right_panel = ctk.CTkFrame(
    root,
    fg_color= "#000000",
)
right_panel.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

upper_right_panel = ctk.CTkFrame(
    right_panel,
    border_width = 2,
    border_color= "#4E545C",
    fg_color= "#000000",
    height=250,
)
upper_right_panel.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

lower_right_panel = ctk.CTkFrame(
    right_panel,
    border_width = 2,
    border_color= "#4E545C",
    fg_color= "#000000",
    height=250,
)
lower_right_panel.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

label1 = tk.Label(
    left_panel,
    text = "Buscar cursos: ",
    fg = "black",
    font= ("Roboto", 12)
)
label1.pack(padx= 10, pady=10)

selected_course = tk.StringVar()

search1 = ttk.Combobox(
    left_panel,
    state = "readonly",
    values= list(course_info.keys()),
    textvariable=selected_course,
    width = 10,
    font = ("Roboto", 12)
)
search1.pack(pady= 10)

display_label = tk.Label(
    upper_right_panel,
    text = "Selecciona un curso para visualizar...",
    font = ("Roboto", 14),
    justify="left",
    anchor="nw",
)
display_label.pack(padx=20, pady=10, anchor="w")

display_course_text = tk.Label(
    upper_right_panel,
    text = "Este es un curso de la Universidad Católica",
    justify = "left",
    font = ("Roboto", 12),
    anchor="nw",
    bg= "#000000",
)
display_course_text.pack(anchor="w", padx=20, pady=10)

ventanas = []


def update_label(event):
    if len(ventanas) != 0:
        for e in ventanas:
            e.destroy()

    current_course = selected_course.get()
    print(current_course)

    display_label.config(text= current_course)
    display_course_text.config(text= "")

    contenido = assignment_list(course_info[current_course]["assignments"])

    for c in contenido:
        assignment_frame = ctk.CTkFrame(
        upper_right_panel,
        corner_radius= 15,
        border_width= 2,
        border_color= "#4E545C",
        fg_color= "#000000",
        width = 200,
        height = 150
        )
        assignment_frame.pack(padx=5, pady=5, anchor="nw", fill="none", expand=True)

        content = ctk.CTkLabel(
            master= assignment_frame,
            text_color= "#ffffff",
            bg_color= "#000000",
            text= c
        )
        content.pack(padx=5, pady=5)

        ventanas.append(assignment_frame)

# ---------------- Titulo ascii ------------------------- #

image = Image.open("ascii_art.png")

img = ImageTk.PhotoImage(image)
ascii_title = tk.Label(
    lower_right_panel,
    image=img,
    bg="#000000",
)
ascii_title.pack(padx=5, pady=5, anchor="ne", side="bottom")


# --------------------- Gato tierno --------------------- #

cat_image = Image.open("cat.png")

cat_img = ImageTk.PhotoImage(cat_image)
cute_cat = tk.Button(
    left_panel,
    image=cat_img,
    bg="#000000",
    borderwidth=0,
    width=100,
    height=100,
)
cute_cat.pack(padx=5, pady=5, side="bottom", anchor="s")

cat_message = tk.Label(
    left_panel,
    text="Miau!",
    fg="white",
    bg="#000000",
    font=("Roboto", 10),
    justify="center",
    wraplength=150,
)
cat_message.pack(padx=5, pady=5, side="bottom", anchor="s")



# ---------------- Cálculo de nota final ---------------- # 

current_row = 2

grade_variables = []
weight_variables = []

grade_calculation_frame = ctk.CTkFrame(
    lower_right_panel,
    corner_radius= 15,
    border_color= "#4E545C",
    border_width= 2,
    fg_color= "#000000",
    width = 250,
    height = 250
)
grade_calculation_frame.pack(padx=5, pady=5, anchor="nw", fill="y", expand=True)

grade_text = tk.Label(
    grade_calculation_frame,
    text="Cálculo de Nota Final",
    font=("Roboto", 14),
    justify="left",
    anchor="nw",
)
grade_text.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

grade1_text = tk.Label(
    grade_calculation_frame,
    text="Nota",
    font=("Roboto", 10),
    justify="center",
    anchor="nw",
)
grade1_text.grid(column=0, row=1, padx=10, pady=0)

weight_text = tk.Label(
    grade_calculation_frame,
    text="Porcentaje (%)",
    font=("Roboto", 10),
    justify="center",
    anchor="nw",
)
weight_text.grid(column=1, row=1, padx=10, pady=0)

nota_final_label = tk.Label(
    grade_calculation_frame,
    text="Nota Final: ",
    font=("Roboto", 12),
    justify="left",
    anchor="nw",
)
nota_final_label.grid(column=0, row=current_row, padx=10, pady=10)




def add_grade():



    global current_row

    new_grade = tk.DoubleVar(value=0.0)
    new_weight = tk.DoubleVar(value=0.0)

    grade_variables.append(new_grade)
    weight_variables.append(new_weight)

    new_grade_entry = ctk.CTkEntry(
        grade_calculation_frame,
        width=100,
        height=30,
        placeholder_text="Nota",
        textvariable=new_grade,
    )
    new_grade_entry.grid(column=0, row=current_row, padx=10, pady=5)

    new_weight_entry = ctk.CTkEntry(
        grade_calculation_frame,
        width=100,
        height=30,
        placeholder_text="Porcentaje (%)",
        textvariable=new_weight,
    )
    new_weight_entry.grid(column=1, row=current_row, padx=10, pady=5)

    current_row += 1

    nota_final_label.grid(column=0, row=current_row, padx=10, pady=10)

    calculate_button.grid(column=1, row=current_row, padx=10, pady=10)

    current_row += 1

    add_grade_button.grid(column=0, row=current_row, padx=10, pady=10, columnspan=2)

    current_row += 1

final_grade = tk.StringVar(value="0.0")

def calculate_final_grade():
    total_weight = 0.0
    final_grade_value = 0.0

    for grade_var, weight_var in zip(grade_variables, weight_variables):
        grade = grade_var.get()
        weight = weight_var.get()

        final_grade_value += (grade * (weight / 100))
        total_weight += weight

    if total_weight != 100.0:
        messagebox.showinfo(title = "Error", message = "El porcentaje total debe ser 100%.")
        return
    
    if grade > 70 or grade < 0:
        messagebox.showinfo(title = "Error", message = "Las notas deben estar entre 0 y 7.")
        return

    final_grade.set(f"{final_grade_value:.0f}")
    nota_final_label.config(text=f"Nota Final: {final_grade.get()}")


calculate_button = ctk.CTkButton(
    grade_calculation_frame,
    text="Calcular Nota Final",
    width=150,
    height=30,
    command=calculate_final_grade,
)

add_grade_button = ctk.CTkButton(
    grade_calculation_frame,
    text="Agregar Nota",
    width=150,
    height=30,
    fg_color="#690500",
    command=add_grade,
)

add_grade()


search1.bind("<<ComboboxSelected>>", update_label)


sv_ttk.set_theme("dark")

root.mainloop()