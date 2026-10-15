from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import ClienteController, ProductoController, VentaController, DevolucionController
from models import Devolucion

# Se crea UN solo controlador de cada tipo.
# A ventas se le pasan los MISMOS clientes y productos.
clientes = ClienteController()
productos = ProductoController()
ventas = VentaController(clientes, productos)
# A devoluciones se le pasan las MISMAS ventas y productos.
devoluciones = DevolucionController(ventas, productos)


# =====================================================================
# AYUDAS DE PANTALLA
# =====================================================================
def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    """Devuelve un entero o None si el usuario escribió otra cosa."""
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    # Los controladores devuelven la TUPLA (exito, mensaje)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    """Sirve para clientes, productos y ventas: cada modelo sabe mostrarse."""
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# =====================================================================
# MENÚ DE CLIENTES
# =====================================================================
def crear_cliente():
    imprimir_titulo("CREAR CLIENTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "telefono": input("Teléfono: "),
        "ciudad": input("Ciudad: "),
    }
    mostrar_resultado(*clientes.crear(datos))
    pausa()


def listar_clientes():
    imprimir_titulo("CLIENTES")
    mostrar_lista(clientes.leer(), "Todavía no hay clientes.")
    pausa()


def buscar_cliente():
    imprimir_titulo("BUSCAR CLIENTE")
    termino = input("Nombre, email, teléfono o ciudad: ")
    encontrados = clientes.buscar(termino)
    mostrar_lista(encontrados, f"Ningún cliente coincide con '{termino}'.")
    pausa()


def ver_cliente():
    imprimir_titulo("VER CLIENTE POR ID")
    cliente = clientes.obtener(pedir_entero("Id: "))
    if cliente is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(cliente)
    pausa()


def actualizar_cliente():
    imprimir_titulo("ACTUALIZAR CLIENTE")
    id_cliente = pedir_entero("Id: ")
    cliente = clientes.obtener(id_cliente)
    if cliente is None:
        imprimir_error("No encontrado")
        return pausa()
    imprimir_info(f"Editando: {cliente.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")
    cambios = {}
    for campo in ("nombre", "apellido", "email", "telefono", "ciudad"):
        actual = getattr(cliente, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo
    mostrar_resultado(*clientes.actualizar(id_cliente, cambios))
    pausa()


def eliminar_cliente():
    imprimir_titulo("ELIMINAR CLIENTE")
    id_cliente = pedir_entero("Id: ")
    cliente = clientes.obtener(id_cliente)
    if cliente is None:
        imprimir_error("No encontrado")
        return pausa()
    imprimir_info(f"Se eliminará: {cliente.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*clientes.eliminar(id_cliente))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE PRODUCTOS
# =====================================================================
def crear_producto():
    imprimir_titulo("CREAR PRODUCTO")
    datos = {
        "nombre": input("Nombre: "),
        "precio": input("Precio: "),
        "stock": input("Stock: "),
    }
    mostrar_resultado(*productos.crear(datos))
    pausa()


def listar_productos():
    imprimir_titulo("PRODUCTOS")
    mostrar_lista(productos.leer(), "Todavía no hay productos.")
    pausa()


def buscar_producto():
    imprimir_titulo("BUSCAR PRODUCTO")
    termino = input("Nombre: ")
    mostrar_lista(productos.buscar(termino), "Sin coincidencias.")
    pausa()


def ver_producto():
    imprimir_titulo("VER PRODUCTO POR ID")
    producto = productos.obtener(pedir_entero("Id: "))
    if producto is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(producto)
        imprimir_info(f"Precio con IVA: ${producto.con_iva(producto.precio):.2f}")
    pausa()


def actualizar_producto():
    imprimir_titulo("ACTUALIZAR PRODUCTO")
    id_producto = pedir_entero("Id: ")
    producto = productos.obtener(id_producto)
    if producto is None:
        imprimir_error("No encontrado")
        return pausa()
    imprimir_info(f"Editando: {producto.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")
    cambios = {}
    for campo in ("nombre", "precio", "stock"):
        actual = getattr(producto, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo
    mostrar_resultado(*productos.actualizar(id_producto, cambios))
    pausa()


def eliminar_producto():
    imprimir_titulo("ELIMINAR PRODUCTO")
    id_producto = pedir_entero("Id: ")
    producto = productos.obtener(id_producto)
    if producto is None:
        imprimir_error("No encontrado")
        return pausa()
    imprimir_info(f"Se eliminará: {producto.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*productos.eliminar(id_producto))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE VENTAS
# =====================================================================
def registrar_venta():
    imprimir_titulo("REGISTRAR VENTA")
    imprimir_info("Clientes:")
    mostrar_lista(clientes.leer())
    imprimir_info("Productos:")
    mostrar_lista(productos.leer())
    datos = {
        "cliente_id": pedir_entero("\nId del cliente: "),
        "producto_id": pedir_entero("Id del producto: "),
        "cantidad": pedir_entero("Cantidad: "),
    }
    if None in datos.values():
        imprimir_error("Todos los datos deben ser números enteros")
        return pausa()
    mostrar_resultado(*ventas.crear(datos))
    pausa()


def listar_ventas():
    imprimir_titulo("VENTAS")
    mostrar_lista(ventas.leer(), "Todavía no hay ventas.")
    pausa()


def ver_comprobante():
    imprimir_titulo("COMPROBANTE")
    texto = ventas.comprobante(pedir_entero("Id de la venta: "))
    if texto is None:
        imprimir_error("No existe esa venta")
    else:
        print(texto)
    pausa()


def anular_venta():
    imprimir_titulo("ANULAR VENTA")
    id_venta = pedir_entero("Id de la venta: ")
    # Si ya tiene devoluciones, anularla devolvería el stock dos veces
    if id_venta and devoluciones.de_venta(id_venta):
        imprimir_error("La venta tiene devoluciones registradas: no se puede anular")
        return pausa()
    if id_venta and confirmar("Se devolverá el stock. ¿Confirma?"):
        mostrar_resultado(*ventas.eliminar(id_venta))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE DEVOLUCIONES
# =====================================================================
def registrar_devolucion():
    imprimir_titulo("REGISTRAR DEVOLUCIÓN")
    id_venta = pedir_entero("Id de la venta / factura: ")

    texto = ventas.comprobante(id_venta)
    if texto is None:
        imprimir_error("No existe esa venta")
        return pausa()
    print()
    print(texto)
    print()

    venta = ventas.obtener(id_venta)
    devueltas = devoluciones.cantidad_devuelta(id_venta)
    disponibles = devoluciones.disponible(id_venta)
    imprimir_info(f"Vendidas: {venta.cantidad} · Ya devueltas: {devueltas} · "
                  f"Disponibles para devolver: {disponibles}")
    if disponibles == 0:
        imprimir_error("Esta venta ya fue devuelta por completo")
        return pausa()

    cantidad = pedir_entero("\nCantidad a devolver: ")
    if cantidad is None:
        imprimir_error("La cantidad debe ser un número entero")
        return pausa()

    print("Motivos:")
    for numero, motivo in enumerate(Devolucion.MOTIVOS, start=1):
        print(f"  {numero}. {motivo}")
    opcion = pedir_entero("Motivo: ")
    if opcion is None or not 1 <= opcion <= len(Devolucion.MOTIVOS):
        imprimir_error("Motivo no válido")
        return pausa()

    datos = {
        "venta_id": id_venta,
        "cantidad": cantidad,
        "motivo": Devolucion.MOTIVOS[opcion - 1],
    }
    mostrar_resultado(*devoluciones.crear(datos))
    pausa()


def consultar_devoluciones():
    imprimir_titulo("DEVOLUCIONES DE UNA VENTA")
    id_venta = pedir_entero("Id de la venta / factura: ")
    venta = ventas.obtener(id_venta)
    if venta is None:
        imprimir_error("No existe esa venta")
        return pausa()
    lista = devoluciones.de_venta(id_venta)
    mostrar_lista(lista, f"La venta {id_venta} no tiene devoluciones.")
    if lista:
        reembolso = sum(d.monto for d in lista)
        imprimir_info(f"Vendidas: {venta.cantidad} · "
                      f"Devueltas: {devoluciones.cantidad_devuelta(id_venta)} · "
                      f"Disponibles: {devoluciones.disponible(id_venta)} · "
                      f"Reembolsado: ${reembolso:.2f}")
    pausa()


def resumen():
    imprimir_titulo("RESUMEN")
    print(f"  Clientes    : {len(clientes.leer())}")
    print(f"  Ciudades    : {', '.join(clientes.ciudades()) or '-'}")
    print(f"  Productos   : {len(productos.leer())}")
    bajos = productos.con_stock_bajo()
    print(f"  Stock bajo  : {', '.join(p.nombre for p in bajos) or 'ninguno'}")
    print(f"  Ventas      : {len(ventas.leer())}")
    print(f"  Vendido     : ${ventas.total_vendido():.2f}")
    print(f"  Devoluciones: {len(devoluciones.leer())}")
    print(f"  Reembolsado : ${devoluciones.total_reembolsado():.2f}")
    netas = ventas.total_vendido() - devoluciones.total_reembolsado()
    print(f"  Ventas netas: ${netas:.2f}")
    pausa()


# =====================================================================
# MENÚS: DICCIONARIOS tecla -> (texto, función)
# =====================================================================
MENU_CLIENTES = {
    "1": ("Crear cliente", crear_cliente),
    "2": ("Ver todos", listar_clientes),
    "3": ("Buscar", buscar_cliente),
    "4": ("Ver por id", ver_cliente),
    "5": ("Actualizar", actualizar_cliente),
    "6": ("Eliminar", eliminar_cliente),
    "0": ("Volver", None),
}

MENU_PRODUCTOS = {
    "1": ("Crear producto", crear_producto),
    "2": ("Ver todos", listar_productos),
    "3": ("Buscar", buscar_producto),
    "4": ("Ver por id", ver_producto),
    "5": ("Actualizar", actualizar_producto),
    "6": ("Eliminar", eliminar_producto),
    "0": ("Volver", None),
}

MENU_VENTAS = {
    "1": ("Registrar venta", registrar_venta),
    "2": ("Ver todas", listar_ventas),
    "3": ("Ver comprobante", ver_comprobante),
    "4": ("Anular venta", anular_venta),
    "0": ("Volver", None),
}

MENU_DEVOLUCIONES = {
    "1": ("Registrar devolución", registrar_devolucion),
    "2": ("Consultar devoluciones de una venta", consultar_devoluciones),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    """Un solo bucle para todos los submenús."""
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()
        tecla = input("Opción: ").strip()
        if tecla not in opciones:               # búsqueda por clave: instantánea
            imprimir_error("Opción no válida")
            pausa()
            continue
        _texto, funcion = opciones[tecla]
        if funcion is None:                      # la opción "Volver"
            break
        funcion()


def main():
    while True:
        imprimir_titulo("SISTEMA DE VENTAS")
        print("  1. Clientes")
        print("  2. Productos")
        print("  3. Ventas")
        print("  4. Devoluciones")
        print("  5. Resumen")
        print("  0. Salir\n")
        tecla = input("Opción: ").strip()
        if tecla == "1":
            ejecutar_menu("CLIENTES", MENU_CLIENTES)
        elif tecla == "2":
            ejecutar_menu("PRODUCTOS", MENU_PRODUCTOS)
        elif tecla == "3":
            ejecutar_menu("VENTAS", MENU_VENTAS)
        elif tecla == "4":
            ejecutar_menu("DEVOLUCIONES", MENU_DEVOLUCIONES)
        elif tecla == "5":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
