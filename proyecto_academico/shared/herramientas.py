import os  # Módulo estándar del sistema operativo; aquí se usa para limpiar la consola

# DICCIONARIO: cada color tiene su etiqueta y su código de consola
COLORES = {  # Diccionario nombre -> secuencia de escape ANSI que cambia el color del texto
    "ROJO": "\033[91m",      # Código ANSI para texto rojo brillante (errores)
    "VERDE": "\033[92m",     # Código ANSI para texto verde brillante (éxitos)
    "AZUL": "\033[94m",      # Código ANSI para texto azul brillante (títulos)
    "AMARILLO": "\033[93m",  # Código ANSI para texto amarillo brillante
    "CYAN": "\033[96m",      # Código ANSI para texto cian brillante (información)
    "BLANCO": "\033[97m",    # Código ANSI para texto blanco brillante (color por defecto)
    "RESET": "\033[0m",      # Código ANSI que vuelve al color normal de la consola
}  # Fin del diccionario de colores

# TUPLA: respuestas afirmativas aceptadas. Es fija, por eso no es lista.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")  # Todas las formas válidas de decir "sí"


def limpiar_pantalla():  # Función que borra todo lo que hay en la consola
    os.system("clear" if os.name == "posix" else "cls")  # En Linux/Mac usa "clear"; en Windows usa "cls"


def imprimir_color(texto, color):  # Imprime un texto con el color indicado por su nombre
    codigo = COLORES.get(color, COLORES["BLANCO"])   # .get evita el error si el color no existe
    print(f"{codigo}{texto}{COLORES['RESET']}")  # Imprime: código de color + texto + reset para no "pintar" lo siguiente


def imprimir_titulo(texto):  # Muestra un encabezado de pantalla
    limpiar_pantalla()  # Primero deja la consola en blanco
    imprimir_color("=" * 60, "AZUL")  # Línea superior de 60 signos "=" en azul
    print(f"  {texto}".center(60))  # Imprime el título centrado en un ancho de 60 caracteres
    imprimir_color("=" * 60, "AZUL")  # Línea inferior de 60 signos "=" en azul
    print()  # Línea en blanco para separar el título del contenido


def imprimir_exito(mensaje):  # Atajo para mensajes de operación exitosa
    imprimir_color(f"✓ {mensaje}", "VERDE")  # Antepone un check y lo imprime en verde


def imprimir_error(mensaje):  # Atajo para mensajes de error
    imprimir_color(f"✗ {mensaje}", "ROJO")  # Antepone una X y lo imprime en rojo


def imprimir_info(mensaje):  # Atajo para mensajes informativos
    imprimir_color(f"ℹ {mensaje}", "CYAN")  # Antepone el símbolo de información y lo imprime en cian


def confirmar(pregunta):  # Hace una pregunta de sí/no al usuario
    # Devuelve True si el usuario respondió algo de la tupla RESPUESTAS_SI
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()  # Lee la respuesta, quita espacios y la pasa a minúsculas
    return respuesta in RESPUESTAS_SI  # True si la respuesta está entre las afirmativas; False en cualquier otro caso


def es_email_valido(texto):  # Comprueba si un texto tiene forma básica de email
    # Validación mínima: un @, algo antes, algo después y un punto al final
    texto = texto.strip()  # Quita espacios al inicio y al final
    if texto.count("@") != 1:  # Debe haber exactamente una arroba
        return False  # Si hay cero o más de una, no es válido
    usuario, dominio = texto.split("@")  # Separa la parte antes y después de la arroba
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")  # Usuario no vacío, dominio con punto y que no termine en punto
