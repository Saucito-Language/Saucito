def escribir(*args, sep=" "):
    # Convertimos todo a string y lo unimos
    resultado = sep.join(str(a) for a in args)
    print(resultado)

def sumar(*args):
    return sum(args)

def restar(*args):
    # Tomamos el primer número y le restamos todos los demás
    if not args: return 0
    res = args[0]
    for n in args[1:]:
        res -= n
    return res

def dibujar(*args):
    for n in args:
        if isinstance(n, int):
            # Dibujamos N filas
            for i in range(n):
                # En cada fila dibujamos N estrellas
                print("*" * n)
        else:
            # Si es texto, dibujamos una línea del largo del texto
            print("*" * len(str(n)))
        print() # Espacio entre dibujos


def leer(mensaje="> "):
    respuesta = input(mensaje)
    try:
        if "." in respuesta:
            return float(respuesta)
        return int(respuesta)
    except ValueError:
        return respuesta