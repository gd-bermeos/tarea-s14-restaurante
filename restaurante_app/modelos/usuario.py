class Usuario:
    def __init__(self, id, nombre, usuario, contrasena, rol):
        self.id = int(id)
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    def __str__(self):
        return f"{self.nombre} | Usuario: {self.usuario} | Rol: {self.rol}"
