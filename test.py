import tkinter as tk
from tkinter import ttk

def get_select_value():
    selected_item = combo_box1.get()
    print(selected_item)

root = tk.Tk()
root.title("Visualiazdor canvas")

# combo-box

values = ["A", "B", "C", "D", "E"]
combo_box1 = ttk.Combobox(root, values=values)
combo_box1.set("Opciones: ")
combo_box1.pack(pady=10)

get_value_button = tk.Button(
    root,
    text="Consultar",
    command=get_select_value
)
get_value_button.pack()

label1 = tk.Label(
    
)

root.mainloop()