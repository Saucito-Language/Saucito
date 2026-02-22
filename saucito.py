import sys
import os
import time

# --- MOTOR DE FUNCIONES ---
# --- COLORES ---
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

def sumar(*args):
    return sum(args)

def restar(*args):
    if not args: return 0
    res = args[0]
    for n in args[1:]:
        res -= n
    return res


# En la función si_funcion, asegúrate de que se vea así:
def si_funcion(valor1, condicion, valor2):
    try:
        # Intentamos convertir a número para comparar correctamente
        v1 = float(valor1) if str(valor1).replace('.', '', 1).isdigit() else f"'{valor1}'"
        v2 = float(valor2) if str(valor2).replace('.', '', 1).isdigit() else f"'{valor2}'"

        expresion = f"{v1} {condicion} {v2}"
        return eval(expresion)
    except:
        return False

def dibujar(n_o_texto):
    if isinstance(n_o_texto, int) or (isinstance(n_o_texto, str) and n_o_texto.isdigit()):
        n = int(n_o_texto)
        if n > 50: # Límite de seguridad
            print("¡Error! Número muy grande.")
            return
        for i in range(n):
            print("*" * n)
    else:
        print("*" * len(str(n_o_texto)))
    print()

def leer(mensaje="> "):
    respuesta = input(mensaje)
    try:
        if "." in respuesta: return float(respuesta)
        return int(respuesta)
    except ValueError:
        return respuesta

# --- EL INTÉRPRETE ---

variables = {}
saltar_linea = False

def mostrar_logo():
    logo = r"""
    #########################################
    #     ____                              #
    #    / ___|  __ _ _   _  ___(_) |_ ___  #
    #    \___ \ / _` | | | |/ __| | __/ _ \ #
    #     ___) | (_| | |_| | (__| | || (_) |#
    #    |____/ \__,_|\__,_|\___|_|\__\___/ #
    #                                       #
    #      EL LENGUAJE DE PROGRAMACION      #
    #########################################
    """
    print(logo)



# Y lo llamas al inicio de ejecutar_codigo_sau
def ejecutar_codigo_sau(archivo_nombre):
    mostrar_logo()
    time.sleep(5)
    global saltar_linea
    try:
        with open(archivo_nombre, "r", encoding="utf-8") as f:
            for num_linea, linea in enumerate(f, 1):
                linea = linea.strip()
                if not linea or linea.startswith("#"): continue



                # Si el 'si' anterior falló, saltamos esta línea
                if saltar_linea:
                    saltar_linea = False
                    continue

                # 1. Lógica de Asignación (x = ...)
                if "=" in linea:
                    nombre_var, resto = linea.split("=", 1)
                    nombre_var = nombre_var.strip()
                    resto = resto.strip()

                    if resto.startswith("leer"):
                        msj = resto.replace("leer", "").strip()
                        variables[nombre_var] = leer(msj)
                    else:
                        try:
                            variables[nombre_var] = eval(resto, {}, variables)
                        except:
                            variables[nombre_var] = resto
                    continue

                # 2. Lógica de Comandos
                partes = linea.split(" ", 1)
                comando = partes[0]
                args = partes[1].strip() if len(partes) > 1 else ""
                # --- COMANDO: COLOR ---
                if comando == "color":
                    # Uso: color verde
                    if args in colores:
                        print(colores[args], end="")
                    elif args == "reset":
                        print(colores["reset"], end="")
                    continue

                if comando == "si":
                    c_partes = args.split(" ")
                    if len(c_partes) == 3:
                        v1 = variables.get(c_partes[0], c_partes[0])
                        op = c_partes[1]
                        v2 = variables.get(c_partes[2], c_partes[2])
                        if not si_funcion(v1, op, v2):
                            saltar_linea = True
                    continue
                    # --- COMANDO: ESPERAR ---

                elif comando == "limpiar":
                    # 'nt' significa Windows. Si es Windows usa 'cls', si no 'clear'
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue

                elif comando == "esperar":
                    try:
                        # Convertimos el argumento a segundos (ejemplo: esperar 2)
                        segundos = float(variables.get(args, args))
                        time.sleep(segundos)
                    except ValueError:
                        print(f"Error: '{args}' no es un tiempo válido.")


                elif comando == "escribir":
                    if "," in args:
                        trozos = args.split(",")
                        final = [str(variables.get(t.strip(), t.strip())) for t in trozos]
                        escribir(*final)
                    else:
                        escribir(variables.get(args, args))

                elif comando == "dibujar":
                    valor = variables.get(args, args)
                    dibujar(valor)

                elif comando == "sumar":
                    nums = [int(n) for n in args.split() if n.isdigit()]
                    print(sumar(*nums))

                else:
                    print(f"Error en línea {num_linea}: Comando '{comando}' desconocido.")

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_nombre}' no existe.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ejecutar_codigo_sau(sys.argv[1])
    else:
        print("Uso: python saucito.py programa.sau")