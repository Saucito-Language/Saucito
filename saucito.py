import sys
import os
import time

# --- MOTOR DE FUNCIONES ---
colores = {
    "verde": "\033[92m",
    "rojo": "\033[91m",
    "azul": "\033[94m",
    "amarillo": "\033[93m",
    "reset": "\033[0m"
}


def escribir(*args, sep=" "):
    resultado = sep.join(str(a) for a in args)
    print(resultado)


def si_funcion(valor1, condicion, valor2):
    try:
        # Intentamos tratar todo como números para la comparación
        v1 = float(valor1) if str(valor1).replace('.', '', 1).isdigit() else f"'{valor1}'"
        v2 = float(valor2) if str(valor2).replace('.', '', 1).isdigit() else f"'{valor2}'"
        return eval(f"{v1} {condicion} {v2}")
    except:
        return False


def dibujar(n):
    try:
        n = int(n)
        if n > 50: return
        for i in range(n): print("*" * n)
    except:
        print("*" * len(str(n)))
    print()


# --- EL INTÉRPRETE ---
variables = {}


def mostrar_logo():
    print(r"""
    #########################################
    #     ____                              #
    #    / ___|  __ _ _   _  ___(_) |_ ___  #
    #    \___ \ / _` | | | |/ __| | __/ _ \ #
    #     ___) | (_| | |_| | (__| | || (_) |#
    #    |____/ \__,_|\__,_|\___|_|\__\___/ #
    #                                       #
    #      EL LENGUAJE DEL CAPIBARA         #
    #########################################
    """)


def ejecutar_codigo_sau(archivo_nombre):
    mostrar_logo()
    time.sleep(4)
    try:
        with open(archivo_nombre, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        i = 0
        while i < len(lineas):
            linea = linea_original = lineas[i].strip()
            if not linea or linea.startswith("#"):
                i += 1
                continue

            # 1. ASIGNACIÓN DE VARIABLES (Ej: x = 5 o x = x + 1)
            if "=" in linea and not any(linea.startswith(c) for c in ["si ", "repetir "]) and "==" not in \
                    linea.split('=')[0]:
                nombre_var, resto = [part.strip() for part in linea.split("=", 1)]

                if resto.startswith("leer"):
                    msj = resto.replace("leer", "").strip()
                    variables[nombre_var] = input(msj + " ")
                else:
                    try:
                        # Evaluamos la expresión usando el diccionario de variables actual
                        variables[nombre_var] = eval(resto, {}, variables)
                    except:
                        variables[nombre_var] = resto
                i += 1
                continue

            # 2. PROCESAR COMANDOS
            partes = linea.split(" ", 1)
            comando = partes[0]
            args = partes[1].strip() if len(partes) > 1 else ""

            if comando == "repetir":
                c_partes = args.split(" ")
                if len(c_partes) == 3:
                    v1 = variables.get(c_partes[0], c_partes[0])
                    op = c_partes[1]
                    v2 = variables.get(c_partes[2], c_partes[2])
                    if not si_funcion(v1, op, v2):
                        # Saltar hasta el finrepetir
                        buscar = i
                        while buscar < len(lineas) and lineas[buscar].strip() != "finrepetir":
                            buscar += 1
                        i = buscar + 1
                        continue
                i += 1
                continue

            elif comando == "finrepetir":
                # Volver al repetir correspondiente
                buscar = i - 1
                while buscar >= 0:
                    if lineas[buscar].strip().startswith("repetir"):
                        i = buscar  # Regresa al inicio del bucle para re-evaluar
                        break
                    buscar -= 1


                # --- COMANDO: PREGUNTAR ---
            elif comando == "preguntar":
                # Uso: preguntar nombre ¿Cómo te llamas?
                partes_p = args.split(" ", 1)
                if len(partes_p) > 1:
                    var_destino = partes_p[0]
                    pregunta = partes_p[1]

                    # El Capibara pregunta en amarillo para resaltar
                    print(f"{colores['amarillo']}{pregunta}{colores['reset']}", end=" ")
                    valor = input()

                    # Intentamos guardar como número si se puede, si no, como texto
                    try:
                        if "." in valor:
                            variables[var_destino] = float(valor)
                        else:
                            variables[var_destino] = int(valor)
                    except ValueError:
                        variables[var_destino] = valor


            elif comando == "escribir":
                # Soporta escribir variables o texto
                if "," in args:
                    trozos = [str(variables.get(t.strip(), t.strip())) for t in args.split(",")]
                    escribir(*trozos)
                else:
                    escribir(variables.get(args, args))

            elif comando == "color":
                if args in colores:
                    print(colores[args], end="")
                elif args == "reset":
                    print(colores["reset"], end="")

            elif comando == "esperar":
                try:
                    time.sleep(float(variables.get(args, args)))
                except:
                    pass

            elif comando == "limpiar":
                os.system('cls' if os.name == 'nt' else 'clear')

            elif comando == "dibujar":
                dibujar(variables.get(args, args))

            elif comando == "si":
                c_partes = args.split(" ")
                if len(c_partes) == 3:
                    v1 = variables.get(c_partes[0], c_partes[0])
                    op = c_partes[1]
                    v2 = variables.get(c_partes[2], c_partes[2])
                    if not si_funcion(v1, op, v2):
                        i += 1  # Salta la siguiente línea

            i += 1

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_nombre}' no existe.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ejecutar_codigo_sau(sys.argv[1])
    else:
        print("Uso: python saucito.py programa.sau")