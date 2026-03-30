

import csv
import os


ARCHIVO_CSV = "estudiantes.csv"

def pedir_texto(mensaje):
    """Pide un texto no vacío al usuario."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("   El campo no puede estar vacío.")



def pedir_entero(mensaje, minimo=0, maximo=None):
    """Pide un número entero dentro de un rango opcional."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print(f"   Debe ser mayor o igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"   Debe ser menor o igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("   Ingresa un número entero.")




def guardar_csv(lista_estudiantes):
    """
    Guarda la lista de diccionarios en el archivo CSV.
    Escribe encabezado + una fila por estudiante.
    """
    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        
        writer.writerow(["id", "nombre", "apellido", ])
        for e in lista_estudiantes:
            writer.writerow([
                e["id"], e["nombre"], e["apellido"],
            ])


def cargar_csv():
    """
    Carga el CSV y retorna una lista de diccionarios.
    Si el archivo no existe, retorna lista vacía.
    Usa split() para separar nombre completo si es necesario.
    """
    estudiantes = []

    if not os.path.exists(ARCHIVO_CSV):
        return estudiantes                   

    with open(ARCHIVO_CSV, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()

        if not contenido:
            return estudiantes              

        lineas = contenido.split("\n")       

        
        for linea in lineas[1:]:
            if not linea.strip():
                continue

            
            partes = linea.split(",")

            
            if len(partes) != 7:
                print(f"  ⚠ Línea con formato incorrecto ignorada: {linea}")
                continue

            try:
                estudiantes.append({
                    "id":       int(partes[0]),
                    "nombre":   partes[1].strip(),
                    "apellido": partes[2].strip(),
                })
            except ValueError:
                print(f"  ⚠ No se pudo leer la línea: {linea}")

    return estudiantes


def siguiente_id(lista_estudiantes):
    """Genera el próximo ID basándose en el máximo actual."""
    if not lista_estudiantes:
        return 1
    return max(e["id"] for e in lista_estudiantes) + 1

def agregar_estudiante(lista_estudiantes):
    """Pide datos al usuario y agrega un nuevo estudiante."""
    print("\n  ── Agregar estudiante ──")
    nombre   = pedir_texto("  Nombre:   ").capitalize()
    apellido = pedir_texto("  Apellido: ").capitalize()


    nuevo = {
        "id":       siguiente_id(lista_estudiantes),
        "nombre":   nombre,
        "apellido": apellido}

    lista_estudiantes.append(nuevo)
    guardar_csv(lista_estudiantes)
    print(f"\n   {nombre} {apellido} agregado. ")


def eliminar_estudiante(lista_estudiantes):
    """Elimina un estudiante por su ID."""
    if not lista_estudiantes:
        print("\n   No hay estudiantes registrados.")
        return

    ver_todos(lista_estudiantes)
    id_eliminar = pedir_entero("\n  ID del estudiante a eliminar: ", minimo=1)

    
    encontrado = None
    for e in lista_estudiantes:
        if e["id"] == id_eliminar:
            encontrado = e
            break

    if encontrado is None:
        print(f"  ✗ No existe un estudiante con ID {id_eliminar}.")
        return

    confirmacion = input(f"  ¿Eliminar a {encontrado['nombre']} {encontrado['apellido']}? (s/n): ").strip().lower()
    if confirmacion == "s":
        lista_estudiantes.remove(encontrado)
        guardar_csv(lista_estudiantes)
        print("   Estudiante eliminado.")
    else:
        print("  Operación cancelada.")


def ver_todos(lista_estudiantes):
    """Muestra todos los estudiantes con sus promedios."""
    if not lista_estudiantes:
        print("\n   No hay estudiantes registrados.")
        return

    print(f"\n  {'ID':<5} {'Nombre':<15} {'Apellido':<15}Estado")
    print("  " + "─" * 68)

    for e in lista_estudiantes:
        print(f"  {e['id']:<5} {e['nombre']:<15} {e['apellido']:<15} ")



def buscar_estudiante(lista_estudiantes):
    """Busca un estudiante por nombre o apellido."""
    if not lista_estudiantes:
        print("\n  ✗ No hay estudiantes registrados.")
        return

    termino = pedir_texto("  Buscar (nombre o apellido): ").lower()

    resultados = [
        e for e in lista_estudiantes
        if termino in e["nombre"].lower() or termino in e["apellido"].lower()
    ]

    if not resultados:
        print(f"  ✗ No se encontraron resultados para '{termino}'.")
        return

    print(f"\n  Resultados para '{termino}':")
    for e in resultados:
        print(f"  → {e['nombre']} {e['apellido']} | ")



def main():
    estudiantes = cargar_csv()
    print(f"\n  Sistema de Estudiantes — {len(estudiantes)} registro(s) cargado(s) desde '{ARCHIVO_CSV}'.")

    while True:
        print("""
  ╔══════════════════════════════════╗
  ║     SISTEMA DE ESTUDIANTES       ║
  ╠══════════════════════════════════╣
  ║  1. Agregar estudiante           ║
  ║  2. Eliminar estudiante          ║
  ║  3. Ver todos los estudiantes    ║
  ║  4. Buscar estudiante            ║
  ║  0. Salir                        ║
  ╚══════════════════════════════════╝""")

        opcion = pedir_entero("  Opción: ", minimo=0, maximo=4)

        if opcion == 0:
            print("\n  ¡Hasta luego! \n")
            break
        elif opcion == 1:
            agregar_estudiante(estudiantes)
        elif opcion == 2:
            eliminar_estudiante(estudiantes)
        elif opcion == 3:
            ver_todos(estudiantes)
        elif opcion == 4:
            buscar_estudiante(estudiantes)


if __name__ == "__main__":
    main()