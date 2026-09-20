from modelos.producto import Producto
from modelos.usuario import Usuario


class RestauranteServicio:
    def __init__(self, archivo_servicio, ruta_usuarios, ruta_productos):
        self.archivo_servicio = archivo_servicio
        self.ruta_usuarios = ruta_usuarios
        self.ruta_productos = ruta_productos
        self.usuarios = []
        self.productos = []
        self.recargar_datos()

    def recargar_datos(self):
        datos_usuarios = self.archivo_servicio.leer_json(self.ruta_usuarios)
        datos_productos = self.archivo_servicio.leer_json(self.ruta_productos)
        self.usuarios = [Usuario(**dato) for dato in datos_usuarios]
        self.productos = [Producto(**dato) for dato in datos_productos]

    def validar_acceso(self, nombre_usuario, contrasena):
        nombre_usuario = nombre_usuario.strip()
        contrasena = contrasena.strip()

        if not nombre_usuario or not contrasena:
            return None

        for usuario in self.usuarios:
            if usuario.usuario == nombre_usuario and usuario.contrasena == contrasena:
                return usuario
        return None

    def listar_usuarios(self):
        return list(self.usuarios)

    def listar_productos(self):
        return list(self.productos)

    def cantidad_usuarios(self):
        return len(self.usuarios)

    def cantidad_productos(self):
        return len(self.productos)

    def buscar_producto(self, id_producto):
        try:
            id_producto = int(str(id_producto).strip())
        except ValueError:
            return None

        for producto in self.productos:
            if producto.id == id_producto:
                return producto
        return None

    def registrar_producto(self, id_producto, nombre, categoria, precio, cantidad):
        datos = self._validar_producto(
            id_producto, nombre, categoria, precio, cantidad
        )

        if self.buscar_producto(datos["id"]) is not None:
            raise ValueError("Ya existe un producto con ese ID.")

        producto = Producto(**datos)
        self.productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(self, id_producto, nombre, categoria, precio, cantidad):
        datos = self._validar_producto(
            id_producto, nombre, categoria, precio, cantidad
        )
        producto = self.buscar_producto(datos["id"])

        if producto is None:
            raise ValueError("No existe un producto con ese ID.")

        producto.nombre = datos["nombre"]
        producto.categoria = datos["categoria"]
        producto.precio = datos["precio"]
        producto.cantidad = datos["cantidad"]
        self._guardar_productos()
        return producto

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto(id_producto)

        if producto is None:
            raise ValueError("No existe un producto con ese ID.")

        self.productos.remove(producto)
        self._guardar_productos()
        return producto

    def _validar_producto(self, id_producto, nombre, categoria, precio, cantidad):
        nombre = nombre.strip()
        categoria = categoria.strip()

        if not nombre or not categoria:
            raise ValueError("Nombre y categoría son obligatorios.")

        try:
            id_num = int(str(id_producto).strip())
        except ValueError as error:
            raise ValueError("El ID debe ser un número entero.") from error

        try:
            precio_num = float(str(precio).strip().replace(",", "."))
        except ValueError as error:
            raise ValueError("El precio debe ser un número válido.") from error

        try:
            cantidad_num = int(str(cantidad).strip())
        except ValueError as error:
            raise ValueError("La cantidad debe ser un número entero.") from error

        if id_num <= 0:
            raise ValueError("El ID debe ser mayor que cero.")
        if precio_num < 0:
            raise ValueError("El precio no puede ser negativo.")
        if cantidad_num < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        return {
            "id": id_num,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio_num,
            "cantidad": cantidad_num,
        }

    def _guardar_productos(self):
        datos = [producto.a_diccionario() for producto in self.productos]
        self.archivo_servicio.escribir_json(self.ruta_productos, datos)
