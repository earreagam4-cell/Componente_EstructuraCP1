import json  # Módulo estándar para convertir entre texto JSON y objetos de Python
import os    # Módulo estándar para trabajar con rutas, carpetas y archivos del sistema


class GestorJSON:  # Clase encargada de la persistencia: leer y escribir un archivo .json
    """Lee y guarda una lista de diccionarios. Es la única parte que toca el disco."""

    def __init__(self, ruta):  # Constructor: recibe la ruta del archivo que va a manejar
        self.ruta = ruta  # Guarda la ruta como atributo para usarla en leer() y guardar()
        carpeta = os.path.dirname(ruta)  # Extrae solo la carpeta de la ruta (ej. "data")
        if carpeta and not os.path.exists(carpeta):  # Si hay carpeta y todavía no existe...
            os.makedirs(carpeta)  # ...la crea (incluidas las carpetas intermedias)

    def leer(self):  # Método que carga los datos del archivo y los devuelve
        # Devuelve SIEMPRE una lista: vacía si el archivo no existe o está dañado
        if not os.path.exists(self.ruta):  # Si el archivo aún no se ha creado...
            return []  # ...no hay datos: se devuelve una lista vacía
        try:  # Intenta abrir y decodificar el archivo (puede fallar)
            with open(self.ruta, "r", encoding="utf-8") as archivo:  # Abre en modo lectura con tildes/ñ; "with" lo cierra solo
                datos = json.load(archivo)  # Convierte el texto JSON en objetos de Python
            return datos if isinstance(datos, list) else []  # Solo acepta una lista; cualquier otra cosa se descarta
        except (json.JSONDecodeError, OSError):  # Si el JSON está mal escrito o hubo un error de lectura...
            # Capturamos errores concretos, nunca un "except:" pelado
            return []  # ...se devuelve una lista vacía para que el programa siga funcionando

    def guardar(self, datos):  # Método que escribe la lista de diccionarios en el archivo
        try:  # Intenta escribir (puede fallar por permisos o datos no serializables)
            with open(self.ruta, "w", encoding="utf-8") as archivo:  # Abre en modo escritura (sobrescribe el contenido)
                json.dump(datos, archivo, ensure_ascii=False, indent=2)  # Escribe el JSON legible: tildes reales y sangría de 2 espacios
            return True  # Indica que el guardado salió bien
        except (TypeError, OSError):  # TypeError: dato no convertible a JSON; OSError: problema con el disco
            return False  # Indica que no se pudo guardar
