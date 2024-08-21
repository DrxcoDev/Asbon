import tkinter as tk
from tkinter import filedialog, Text, ttk
from tkinter import simpledialog
import os

# Función para abrir un archivo en el editor de texto
def open_file(file_path):
    if file_path and os.path.isfile(file_path):
        try:
            with open(file_path, "r") as file:
                code = file.read()
                # Limpiar el contenido del editor de texto
                text_area.delete(1.0, tk.END)
                # Insertar el contenido del archivo
                text_area.insert(tk.END, code)
        except Exception as e:
            print(f"Error al abrir el archivo: {e}")

# Función para guardar el archivo actual
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".py", 
                                             filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                code = text_area.get(1.0, tk.END)
                file.write(code)
            update_treeview(file_path)
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

# Función para actualizar la vista de árbol con la estructura de carpetas
def update_treeview(selected_file_path=None):
    for item in tree.get_children():
        tree.delete(item)
    
    # Obtener la carpeta del archivo seleccionado o la carpeta actual
    if selected_file_path:
        directory = os.path.dirname(selected_file_path)
    else:
        directory = os.getcwd()
    
    # Agregar la raíz
    insert_tree_items('', directory)
    
    # Expandir el nodo del archivo seleccionado
    if selected_file_path:
        expand_to_file(selected_file_path)

# Función para expandir el Treeview hasta el archivo seleccionado
def expand_to_file(file_path):
    path_parts = file_path.split(os.sep)
    node_id = ''
    for part in path_parts[:-1]:
        if not node_id:
            node_id = tree.insert('', 'end', text=part, open=True)
        else:
            node_id = tree.insert(node_id, 'end', text=part, open=True)
    last_node = tree.insert(node_id, 'end', text=path_parts[-1])
    tree.selection_set(last_node)
    tree.see(last_node)

# Función para insertar elementos en el Treeview
def insert_tree_items(parent, path):
    if not os.path.isdir(path):
        return
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                node = tree.insert(parent, 'end', text=item, open=False)
                insert_tree_items(node, item_path)
            else:
                tree.insert(parent, 'end', text=item)
    except Exception as e:
        print(f"Error al insertar elementos en el Treeview: {e}")

# Función para manejar la selección en el Treeview
def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        file_path = get_full_path(selected_item[0])
        if os.path.isfile(file_path):
            open_file(file_path)

# Función para obtener la ruta completa del archivo a partir del Treeview
def get_full_path(item):
    path_parts = []
    while item:
        path_parts.insert(0, tree.item(item, 'text'))
        item = tree.parent(item)
    return os.path.join(*path_parts) if path_parts else ""

# Función para crear un nuevo archivo o directorio
def create_new(is_directory=False):
    selected_item = tree.selection()
    if selected_item:
        parent_item = selected_item[0] if tree.item(selected_item[0], 'open') else tree.parent(selected_item[0])
        parent_path = get_full_path(parent_item) if parent_item else os.getcwd()

        new_name = simpledialog.askstring("Nuevo", f"Ingrese el nombre del nuevo {'directorio' if is_directory else 'archivo'}:")
        if new_name:
            new_path = os.path.join(parent_path, new_name)
            if not os.path.exists(new_path):
                try:
                    if is_directory:
                        os.makedirs(new_path)
                    else:
                        with open(new_path, 'w') as f:
                            f.write("")
                    update_treeview()
                except Exception as e:
                    print(f"Error al crear {'directorio' if is_directory else 'archivo'}: {e}")
            else:
                print("El archivo o directorio ya existe.")

# Función para eliminar un archivo o directorio
def delete_file():
    selected_item = tree.selection()
    if selected_item:
        file_path = get_full_path(selected_item[0])
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
            update_treeview()
        except Exception as e:
            print(f"Error al eliminar: {e}")

# Función para renombrar un archivo o directorio
def rename_file():
    selected_item = tree.selection()
    if selected_item:
        old_path = get_full_path(selected_item[0])
        new_name = simpledialog.askstring("Renombrar", "Ingrese el nuevo nombre:")
        if new_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            if not os.path.exists(new_path):
                try:
                    os.rename(old_path, new_path)
                    update_treeview()
                except Exception as e:
                    print(f"Error al renombrar: {e}")
            else:
                print("El nuevo nombre ya existe.")

# Función para actualizar los números de línea
def update_line_numbers(event=None):
    try:
        lines = text_area.get(1.0, 'end-1c').split('\n')
        line_numbers = '\n'.join(f'{i+1}' for i in range(len(lines)))
        line_numbers_canvas.config(state=tk.NORMAL)
        line_numbers_canvas.delete(1.0, tk.END)
        line_numbers_canvas.insert(tk.END, line_numbers)
        line_numbers_canvas.config(state=tk.DISABLED)
    except Exception as e:
        print(f"Error al actualizar números de línea: {e}")

# Crear y configurar la ventana principal
root = tk.Tk()
root.title("IDE Moderno")

# Configuración de estilos
style = ttk.Style()
style.configure("Treeview", background="#f0f0f0", foreground="#000000", rowheight=25, fieldbackground="#f0f0f0")
style.configure("Treeview.Heading", background="#d0d0d0", foreground="#000000")
style.configure("TScrollbar", gripcount=0, background="#d0d0d0", troughcolor="#e0e0e0", arrowcolor="#000000")

# Configuración del marco principal
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Configuración del marco para el Treeview y la barra de desplazamiento
tree_frame = tk.Frame(main_frame)
tree_frame.pack(side='left', fill='both', expand=True)

tree_scrollbar = tk.Scrollbar(tree_frame, orient='vertical')
tree_scrollbar.pack(side='right', fill='y')

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set)
tree.pack(side='left', fill='both', expand=True)

tree_scrollbar.config(command=tree.yview)

# Configuración del marco para el editor de texto y la barra de desplazamiento
text_frame = tk.Frame(main_frame)
text_frame.pack(side='right', fill='both', expand=True)

text_scrollbar = tk.Scrollbar(text_frame, orient='vertical')
text_scrollbar.pack(side='right', fill='y')

# Crear un marco para los números de línea y el área de texto
line_numbers_frame = tk.Frame(text_frame)
line_numbers_frame.pack(side='left', fill='y')

# Crear el widget Canvas para los números de línea
line_numbers_canvas = tk.Text(line_numbers_frame, width=4, bg="#e0e0e0", fg="#000000", padx=5, takefocus=0, state=tk.DISABLED)
line_numbers_canvas.pack(side='left', fill='y')

text_area = Text(text_frame, wrap="word", yscrollcommand=text_scrollbar.set, bg="#f9f9f9", fg="#000000", font=("Consolas", 12))
text_area.pack(side='left', fill='both', expand=True)

text_scrollbar.config(command=text_area.yview)

# Asociar la actualización de números de línea con los eventos de cambio de texto
text_area.bind('<KeyRelease>', update_line_numbers)
text_area.bind('<MouseWheel>', update_line_numbers)
text_area.bind('<Button-4>', update_line_numbers)
text_area.bind('<Button-5>', update_line_numbers)

# Menú contextual para el Treeview
def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Nuevo archivo", command=lambda: create_new(is_directory=False))
context_menu.add_command(label="Nueva carpeta", command=lambda: create_new(is_directory=True))
context_menu.add_command(label="Eliminar", command=delete_file)
context_menu.add_command(label="Renombrar", command=rename_file)

tree.bind("<Button-3>", show_context_menu)

# Creación del menú
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Archivo", menu=file_menu)
file_menu.add_command(label="Abrir", command=lambda: open_file(filedialog.askopenfilename(defaultextension=".py", 
                                                                                  filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])))
file_menu.add_command(label="Guardar", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)

# Inicialización del Treeview
update_treeview()

# Asociar el evento de selección del Treeview
tree.bind('<<TreeviewSelect>>', on_tree_select)

# Actualizar los números de línea inicialmente
update_line_numbers()

# Loop principal de la interfaz
root.mainloop()
