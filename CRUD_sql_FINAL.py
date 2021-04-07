from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import re


class EntraInvalidaExcepicion(Exception):
    pass


# Funcion que conecta y en su defecto crea la base de datos con las tablas correspondientes
def inicializar_bd():
    global conexion
    global c

    conexion = sqlite3.connect('base_articulos.db')
    c = conexion.cursor()
    try:
        c.execute("CREATE TABLE articulos(ID integer PRIMARY KEY AUTOINCREMENT,art_cod varchar, art_des varchar,art_pro text,art_pre INTEGER)")
        messagebox.showinfo("CONEXION", "Base de datos creada exitosamente")
        log.destroy()
    except:
        messagebox.showinfo("CONEXION", "Conexion exitosa")
        log.destroy()


# Ventana inicio de aplicacion y conexion a base de datos
log = Tk()
log.title("CONECTAR")
log.geometry("+800+500")
b_conectar = ttk.Button(log, text='Iniciar', width=35, command=inicializar_bd)
b_conectar.grid(column=0, row=0)
log.mainloop()


# Ventana principal de la aplicacion
ventana = Tk()
ventana.title("Retail software")
ventana.geometry("+450+400")
art_id = StringVar()
art_codigo = StringVar()
art_descripcion = StringVar()
art_proveedor = StringVar()
art_precio = StringVar()


# Funcion de cierre de aplicacion
def salir():
    respuesta = messagebox.askquestion("SALIR", "¿Desea salir de la aplicacion?")
    if respuesta == "yes":
        ventana.destroy()


# Funcion para limpiar cuadros de entrada
def clean():
    e_codigo.delete(0, END)
    e_descripcion.delete(0, END)
    e_proveedor.delete(0, END)
    e_precio.delete(0, END)


# Esta funcion refresca la vista de arbol, primero borrando los datos y luego cargandolos de nuevo desde la base sql
def show_grid():
  
    registros = tree.get_children()
    for i in registros:
        tree.delete(i)
    try:
        c.execute("SELECT * FROM articulos")
        for row in c:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
    except:
        pass


# Funcion de carga de datos en base de datos SQL
def submit():       
    
    try:
        if not validar_entradas():
            raise EntraInvalidaExcepicion("Formato no admitido")
        datos = art_codigo.get(), art_descripcion.get(), art_proveedor.get(), art_precio.get()
        c.execute("INSERT INTO articulos VALUES (NULL,?,?,?,?)", datos)
        conexion.commit()
        messagebox.showinfo("ATENCION", "Articulo ingresado exitosamente")
    except EntraInvalidaExcepicion:
        messagebox.showwarning("ATENCION", "Caracter invalido en precio, los valores ingreados deben ser numericos")
        pass
    except:
        messagebox.showwarning("ATENCION", "Ocurrio un error al intentar crear registro, verifique la base de datos")
        pass
    clean()
    show_grid()


# Funcion de actualizacion de articulos en base de datos sql
def update():
    try:
        if not validar_entradas():
            raise EntraInvalidaExcepicion("Formato no admitido")
        datos = art_codigo.get(), art_descripcion.get(), art_proveedor.get(), art_precio.get()
        c.execute("UPDATE articulos SET art_cod=?, art_des=?, art_pro=?, art_pre=? WHERE ID=" + art_id.get(), datos)
        conexion.commit()
        messagebox.showinfo("ATENCION", "Articulo actualizado exitosamente")
    except EntraInvalidaExcepicion:
        messagebox.showwarning("ATENCION",  "Caracter invalido en precio, los valores ingreados deben ser numericos")
        pass
    except:
        messagebox.showwarning("ATENCION", "Ocurrio un error al intentar actualizar el registro")
        pass
    clean()
    show_grid()


# Funcion de eliminacion de articulos en base de datos sql
def delete():
    
    try:
        if messagebox.askyesno(message="¿Desea eliminar el registro?", title="ADVERTENCIA"):
            c.execute("DELETE FROM articulos WHERE ID="+art_id.get())
            conexion.commit()
            messagebox.showinfo("ATENCION", "Articulo eliminado exitosamente")
    except:
        messagebox.showwarning("ATENCION", "Ocurrio un error al intentar eliminar el registro")
        pass
    clean()
    show_grid()


# Grilla de visualizacion y seleccion de altas

tree = ttk.Treeview(ventana)
tree["columns"] = ("col1", "col2", "col3", "col4")
tree.column("#0", width=50, minwidth=50)
tree.column("col1", width=50, minwidth=50)
tree.column("col2", width=50, minwidth=50)
tree.column("col3", width=50, minwidth=50)
tree.column("col4", width=50, minwidth=50)
tree.heading("#0", text="ID")
tree.heading("col1", text="CODIGO")
tree.heading("col2", text="DESCRIPCION")
tree.heading("col3", text="PROVEEDOR")
tree.heading("col4", text="PRECIO")


# Funcion que carga en entradas alta de la grilla para su modificacion/eliminacion
def on_select(event):
    item = tree.identify("item", event.x, event.y)

    art_id.set(tree.item(item, "text"))
    art_codigo.set(tree.item(item, "values")[0])
    art_descripcion.set(tree.item(item, "values")[1])
    art_proveedor.set(tree.item(item, "values")[2])
    art_precio.set(tree.item(item, "values")[3])


tree.bind("<Double-1>", on_select)


# Funcion REGEX, solo precios numericos y solo codigo alfanumericos
def validar_entradas():
    price_pattern = re.compile("[0-9]")

    return bool(price_pattern.search(art_precio.get()))


# etiquetas
l_codigo = ttk.Label(ventana, text='CODIGO', width=30)
l_descripcion = ttk.Label(ventana, text='DESCRIPCION', width=30)
l_proveedor = ttk.Label(ventana, text='PROVEEDOR', width=30)
l_precio = ttk.Label(ventana, text='PRECIO', width=30)
# entradas
e_id = ttk.Entry(ventana, textvariable=art_id)
e_codigo = ttk.Entry(ventana, width=30, textvariable=art_codigo)
e_descripcion = ttk.Entry(ventana, width=30, textvariable=art_descripcion)
e_proveedor = ttk.Entry(ventana,  width=30, textvariable=art_proveedor)
e_precio = ttk.Entry(ventana,  width=30, textvariable=art_precio)
# botones
b_ingresar = ttk.Button(ventana, text='Ingresar', width=35, command=submit)
b_editar = ttk.Button(ventana, text='Editar', width=35, command=update)
b_eliminar = ttk.Button(ventana, text='Eliminar', width=35, command=delete)
b_salir = ttk.Button(ventana, text='SALIR', width=35, command=salir)
# Posiciono los controles
l_codigo.grid(column=0, row=0)
e_codigo.grid(column=1, row=0, sticky="nsew")
l_descripcion.grid(column=2, row=0)
e_descripcion.grid(column=3, row=0, sticky="nsew")
l_proveedor.grid(column=0, row=1)
e_proveedor.grid(column=1, row=1, sticky="nsew")
l_precio.grid(column=2, row=1)
e_precio.grid(column=3, row=1, sticky="nsew")
b_ingresar.grid(column=0, row=2)
b_editar.grid(column=1, row=2)
b_eliminar.grid(column=2, row=2)
b_salir.grid(column=3, row=2)
tree.grid(column=0, row=3, columnspan=4, sticky="nsew")

show_grid()
ventana.mainloop()
