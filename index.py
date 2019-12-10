from datetime import date,datetime
from tkinter import ttk
from tkinter import *

import sqlite3


class Lugar:

    db = 'database.db'

    def __init__(self, window):

        self.wind = window
        self.wind.title("Lugares Turisticos")

        # Este es un Frame Container

        frame =  LabelFrame(self.wind, text = "Registra un lugar turistico")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)


        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.nombre = Entry(frame)
        self.nombre.grid(row = 1, column = 1)

        Label(frame, text = 'Detalle: ').grid(row = 2, column = 0)
        self.detalle = Entry(frame)
        self.detalle.grid(row = 2, column = 1)

        Label(frame, text = 'Valor entrada: ').grid(row = 3, column = 0)
        self.valor_entrada = Entry(frame)
        self.valor_entrada.grid(row = 3, column = 1)


        ttk.Button(frame, text="Guardar", command = self.add_place).grid(row = 4 , columnspan = 2, sticky= W + E)
        

        self.message = Label(text = '', fg ='red')
        self.message.grid(row = 5 , columnspan = 2, sticky= W + E)


        self.tree = ttk.Treeview(height = 10, 
        columns=("Detalle","Valor Entrada","Fecha de registro"), selectmode="extended")
        self.tree.grid(row = 6, column=0, columnspan = 2)
        self.tree.heading("#0", text="Nombre", anchor = CENTER)
        self.tree.heading("#1", text="Detalle", anchor = CENTER)
        self.tree.heading("#2", text="Valor Entrada", anchor = CENTER)
        self.tree.heading("#3", text="Fecha de registro", anchor = CENTER)
        
        # Botones de actualizar y eliminar 

        ttk.Button(text = 'Eliminar', command=self.delete_place).grid(row = 7 , column = 0, sticky= W + E)
        ttk.Button(text = 'Editar', command =self.edit_place).grid(row = 7 , column = 1, sticky= W + E)

        # Llenando las filas de la tabla
        self.get_places()

    def run_query(self, query, paremeters = ()):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, paremeters)
            conn.commit()
        return result

    def get_places(self):

        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        query = "select * from lugares order by nombre desc"
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[4]))

    
    def validation(self):
        return self.nombre.get() != "" and self.valor_entrada != 0

    def get_date(self):
        return str(datetime.now())

    def add_place(self):

        if self.validation():
            query = "INSERT INTO lugares VALUES(NULL, ?,?,?,?)"
            paremeters = (self.nombre.get() , self.detalle.get(), self.valor_entrada.get(), self.get_date())
            self.run_query(query, paremeters)
            self.message['text'] = "Lugar guardado satisfactoriamente"
        else:
            self.message['text'] = 'Nombre, valor de la entrada debe ser requerido'

        self.get_places()
    
    def delete_place(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor selecciona un registro'
            return
        
        name = self.tree.item(self.tree.selection())['text']
        query = "delete from lugares Where nombre = ?"
        self.run_query(query, (name,))
        self.message['text'] = "Dato {0} eliminado correctamente".format(name)
        self.get_places()
   

    def edit_place(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor selecciona un registro'
            return

        name = self.tree.item(self.tree.selection())['text']
        old_detalle = self.tree.item(self.tree.selection())['values'][0]
        old_valor = self.tree.item(self.tree.selection())['values'][1]

        self.edit_wind = Toplevel()
        self.edit_wind.title = "Editar lugar"
        
        Label(self.edit_wind, text="Nombre: ").grid(row=0, column=1)
        new_name = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=name)).grid(row=0, column=2)
        
        Label(self.edit_wind, text="Detalle: ").grid(row=1, column=1)
        new_detalle = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_detalle)).grid(row=1, column=2)
        

        Label(self.edit_wind, text="valor: ").grid(row=2, column=1)
        new_valor = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value=old_valor)).grid(row=2, column=2)
        

        print("Este es jdfkdhfkdj "+new_name.get())

        Button(self.edit_wind, text = 'Actualizar', 
        command = lambda: self.edit_fill(new_name.get(),
        new_detalle.get(),new_valor.get(),name)).grid(row=3, column=2 , sticky=W + E)

    def edit_fill(self, new_name, new_detalle, new_valor, name):
        query = "UPDATE lugares SET nombre = ?, detalle = ?, valor = ? WHERE nombre = ?"
        parametes = (new_name,new_detalle,new_valor,name)
        self.run_query(query,parametes)
        self.edit_wind.destroy()
        self.message['text'] = "Atualizacion correctamente"
        self.get_place()

if __name__ == '__main__':
    window = Tk()
    aplication = Lugar(window)
    window.mainloop()