import pandas as pd
import os
import sqlite3 as dba_object 
from sqlite3 import Error

#Creo Listas
list_hora = []
list_ciudad = []
list_consumo = []
list_ciudadUnica = []
Horas = 0

class ControladorOperador:

    if os.path.isfile("operador.db"):

        def consulta_operador():
            conn = dba_object.connect('operador.db')
            cursor = conn.execute("SELECT id_operador, nombre_operador from operadores")
            for row in cursor:
                print ("Id: ", row[0], "Nombre: ", row[1])
            conn.close()
        consulta_operador()

    else:
           
        def crea_base_datos():
            try:
                conexion = dba_object.connect("operador.db")
                return conexion
            except Error as err:
                print(err)
        crea_base_datos()

        def crea_tabla_operador():
            conn = dba_object.connect('operador.db')
            conn.execute('''CREATE TABLE IF NOT EXISTS operadores
                    (id_operador INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_operador TEXT NOT NULL, num_subestacion INT);''')
            conn.close()
        crea_tabla_operador()

        def valida_operador():
            conn = dba_object.connect('operador.db')
            existe = conn.execute("SELECT COUNT(nombre_operador) FROM operadores").fetchone()[0]
            if existe < 1:
                nombre = str(input("Introduce tu nombre: "))
                conn.execute("INSERT INTO operadores (nombre_operador) \
                VALUES (?)", [nombre]);
                conn.commit()
                cursor = conn.execute("SELECT id_operador, nombre_operador from operadores")
                for row in cursor:
                    print ("Id: ", row[0], "Nombre: ", row[1])
                conn.close()
            else:
                conn.close()
        valida_operador()

class ControladorSubestacion:
       
    def valida_subestacion():
        conn = dba_object.connect('operador.db')
        existe = conn.execute("SELECT num_subestacion FROM operadores WHERE id_operador = 1").fetchone()[0]
        if existe == "":
            datosubestacion = int(input("Introduce el numero de subestacion: "))
            conn.execute("UPDATE operadores SET num_subestacion = (?) WHERE id_operador = 1", [datosubestacion])
            conn.commit()
            cursor = conn.execute("SELECT id_operador, num_subestacion from operadores")
            for row in cursor:
                print ("Id: ", row[0], "Subestacion: ", row[1])
            conn.close()
            conn.close()
        else:
            cursor = conn.execute("SELECT id_operador, num_subestacion from operadores")
            for row in cursor:
                print ("Id: ", row[0], "Subestacion: ", row[1])
            conn.close()
    valida_subestacion()

        # Funcion escribir CSV
    def escribir_csv():

        #Verifico si el archivo existe
        if os.path.exists("consumo.csv"):
            #Si existe no creo nada
            print("")
        else:
            # Creo un csv con permisos de escritura
            datos_ice = open("consumo.csv", "w") 

            # Establesco los datos a ingresar
            datoscsv = { "Hora" : [23, 2, 10, 3, 7, 21, 10, 9, 4, 6, 11, 22], 
            "Ciudad" : [1, 4, 3, 5, 8, 1, 4, 2, 6, 6, 3, 13], 
            "Medicion" : [42.8, 60.5, 44.2, 23.6, 45.8, 89.1, 50.6, 89.6, 156.9, 35.5, 99.9, 1456.7] }

            # Defino el objeto de kis datos
            objeto_csv = pd.DataFrame(datoscsv, columns = ["Hora", "Ciudad", "Medicion"])

            # Inyecto los datos al archivo
            objeto_csv.to_csv("consumo.csv", sep=";")
    escribir_csv()

    # Funcion leer CSV
    def leer_csv(): 
        
        # Leo el archivo
        df = pd.read_csv("consumo.csv", sep=";", index_col=0)

        # Cargo las listas por columna
        list_hora = df["Hora"]
        list_ciudad = df["Ciudad"]
        list_consumo = df["Medicion"]

        # Creo una lista de Ciudades unicas
        list_ciudadUnica = set(list_ciudad)
        print("Lista Ciudad Unica: ", list_ciudadUnica)
        H = 0
        C = 0
        recorre = 0
        for ciudadunica in list_ciudadUnica:
            recorre = ciudadunica
            for ciudad, hora, consumo in zip(list_ciudad, list_hora, list_consumo):
                if ciudadunica == ciudad:
                    H = H + hora
                    C = C + consumo
            print(ciudadunica, H, C)

    leer_csv()
            