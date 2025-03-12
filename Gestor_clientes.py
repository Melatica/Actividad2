import sys
import os
from datetime import datetime

# Diccionario para almacenar clientes
clientes = {}

# Archivo único para guardar toda la información de los clientes
archivo_clientes = "clientes_registros.txt"

# Función para cargar datos de clientes desde el archivo único
def cargar_clientes():
    if os.path.exists(archivo_clientes):
        with open(archivo_clientes, "r") as file:
            cliente_actual = None
            for linea in file:
                if linea.startswith("Nombre: "):
                    cliente_actual = linea.split(": ")[1].strip()
                    clientes[cliente_actual] = {
                        'direccion': "",
                        'telefono': "",
                        'correo': "",
                        'fecha_creacion': "",
                        'descripciones': []
                    }
                elif linea.startswith("Dirección: "):
                    clientes[cliente_actual]['direccion'] = linea.split(": ")[1].strip()
                elif linea.startswith("Teléfono: "):
                    clientes[cliente_actual]['telefono'] = linea.split(": ")[1].strip()
                elif linea.startswith("Correo: "):
                    clientes[cliente_actual]['correo'] = linea.split(": ")[1].strip()
                elif linea.startswith("Fecha de Creación: "):
                    clientes[cliente_actual]['fecha_creacion'] = linea.split(": ")[1].strip()
                elif linea.startswith("- "):
                    clientes[cliente_actual]['descripciones'].append(linea.strip().replace("- ", ""))

# Función para guardar todos los clientes en un archivo único
def guardar_todos_los_clientes():
    with open(archivo_clientes, "w") as file:
        # Guardar el valor original de sys.stdout
        original_stdout = sys.stdout
        # Redirigir salida estándar al archivo
        sys.stdout = file
        for nombre, datos in clientes.items():
            print(f"Nombre: {nombre}")
            print(f"Dirección: {datos['direccion']}")
            print(f"Teléfono: {datos['telefono']}")
            print(f"Correo: {datos['correo']}")
            print(f"Fecha de Creación: {datos['fecha_creacion']}")
            print("Descripciones:")
            for descripcion in datos['descripciones']:
                print(f"- {descripcion}")
            print()  # Espacio entre clientes
        # Restaurar salida estándar a la consola
        sys.stdout = original_stdout
    print(f"Información guardada en {archivo_clientes}")

# Función para crear o actualizar un cliente
def crear_cliente(nombre, descripcion, direccion, telefono, correo):
    if nombre in clientes:
        print("El cliente ya existe. Actualizando descripción...")
        clientes[nombre]['descripciones'].append(descripcion)
    else:
        print("Creando un nuevo cliente...")
        clientes[nombre] = {
            'direccion': direccion,
            'telefono': telefono,
            'correo': correo,
            'fecha_creacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'descripciones': [descripcion]
        }
    guardar_todos_los_clientes()

# Función para agregar un servicio a cliente existente
def agregar_servicio(nombre, descripcion):
    if nombre in clientes:
        clientes[nombre]['descripciones'].append(descripcion)
        guardar_todos_los_clientes()
        print(f"Servicio agregado al cliente {nombre}.")
    else:
        print("Cliente no encontrado.")

# Función para modificar información de un cliente existente
def modificar_cliente(nombre):
    if nombre in clientes:
        print(f"Información actual del cliente {nombre}:")
        leer_cliente(nombre)

        print("\nIntroduce los nuevos datos (presiona Enter para mantener los actuales):")
        nueva_direccion = input(f"Dirección [{clientes[nombre]['direccion']}]: ") or clientes[nombre]['direccion']
        nuevo_telefono = input(f"Teléfono [{clientes[nombre]['telefono']}]: ") or clientes[nombre]['telefono']
        nuevo_correo = input(f"Correo [{clientes[nombre]['correo']}]: ") or clientes[nombre]['correo']

        # Actualizar datos
        clientes[nombre]['direccion'] = nueva_direccion
        clientes[nombre]['telefono'] = nuevo_telefono
        clientes[nombre]['correo'] = nuevo_correo

        guardar_todos_los_clientes()
        print(f"Información del cliente {nombre} modificada correctamente.")
    else:
        print("Cliente no encontrado.")

# Función para eliminar un cliente
def eliminar_cliente(nombre):
    if nombre in clientes:
        del clientes[nombre]
        guardar_todos_los_clientes()
        print(f"Cliente {nombre} eliminado.")
    else:
        print("Cliente no encontrado.")

# Función para listar los clientes
def listar_clientes():
    if clientes:
        print("Lista de clientes:")
        for cliente in clientes:
            print(f"- {cliente}")
    else:
        print("No hay clientes registrados.")

# Función para leer un cliente específico
def leer_cliente(nombre):
    if nombre in clientes:
        print(f"Información del cliente {nombre}:")
        print(f"Dirección: {clientes[nombre]['direccion']}")
        print(f"Teléfono: {clientes[nombre]['telefono']}")
        print(f"Correo: {clientes[nombre]['correo']}")
        print(f"Fecha de Creación: {clientes[nombre]['fecha_creacion']}")
        print("Descripciones:")
        for descripcion in clientes[nombre]['descripciones']:
            print(f"- {descripcion}")
    else:
        print("Cliente no encontrado.")

# Modify menu function to accept inputs
def menu(args=None):
    cargar_clientes()
    while True:
        if args:
            opcion = args.pop(0) if args else "7"  # Default to exit
        else:
            print("\nMenú Clientes SKY:")
            print("1. Ver lista de clientes")
            print("2. Ver cliente")
            print("3. Crear cliente nuevo")
            print("4. Agregar servicio a cliente existente")
            print("5. Modificar cliente existente")
            print("6. Eliminar cliente")
            print("7. Salir")
            opcion = input("Selecciona una opción: ")

        if opcion == "1":
            listar_clientes()
        elif opcion == "2":
            nombre = input("Introduce el nombre del cliente: ") if not args else args.pop(0)
            leer_cliente(nombre)
        elif opcion == "3":
            nombre = input("Introduce el nombre del cliente nuevo: ") if not args else args.pop(0)
            direccion = input("Introduce la dirección del cliente: ") if not args else args.pop(0)
            telefono = input("Introduce el teléfono del cliente: ") if not args else args.pop(0)
            correo = input("Introduce el correo electrónico del cliente: ") if not args else args.pop(0)
            descripcion = input("Introduce la descripción del servicio: ") if not args else args.pop(0)
            crear_cliente(nombre, descripcion, direccion, telefono, correo)
        elif opcion == "4":
            nombre = input("Introduce el nombre del cliente: ") if not args else args.pop(0)
            descripcion = input("Introduce la descripción del nuevo servicio: ") if not args else args.pop(0)
            agregar_servicio(nombre, descripcion)
        elif opcion == "5":
            nombre = input("Introduce el nombre del cliente a modificar: ") if not args else args.pop(0)
            modificar_cliente(nombre)
        elif opcion == "6":
            nombre = input("Introduce el nombre del cliente a eliminar: ") if not args else args.pop(0)
            eliminar_cliente(nombre)
        elif opcion == "7":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Ejecución del programa
menu()
