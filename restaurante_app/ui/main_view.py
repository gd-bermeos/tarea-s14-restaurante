import tkinter as tk
from tkinter import messagebox, ttk


class MainView(ttk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, on_logout):
        super().__init__(master, padding=15)
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Listo para gestionar productos.")
        self.tabla_productos = None

        self._construir_interfaz()
        self._mostrar_inicio()

    def _construir_interfaz(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        encabezado = ttk.Frame(self, padding=(5, 5, 5, 10))
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew")
        encabezado.columnconfigure(0, weight=1)

        ttk.Label(
            encabezado,
            text="Restaurante App - Semana 14",
            font=("Arial", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            encabezado,
            text=f"Sesión: {self.usuario_actual.nombre} ({self.usuario_actual.rol})",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))
        ttk.Button(
            encabezado, text="Cerrar sesión", command=self.on_logout
        ).grid(row=0, column=1, rowspan=2, padx=(20, 0))

        menu = ttk.LabelFrame(self, text="Navegación", padding=10)
        menu.grid(row=1, column=0, sticky="ns", padx=(0, 12))

        ttk.Button(
            menu, text="Inicio", width=20, command=self._mostrar_inicio
        ).pack(fill="x", pady=4)
        ttk.Button(
            menu,
            text="Productos",
            width=20,
            command=self._mostrar_productos,
        ).pack(fill="x", pady=4)
        ttk.Button(
            menu,
            text="Usuarios",
            width=20,
            command=self._mostrar_usuarios,
        ).pack(fill="x", pady=4)

        self.contenido = ttk.Frame(self, padding=5)
        self.contenido.grid(row=1, column=1, sticky="nsew")
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(0, weight=1)

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def _mostrar_inicio(self):
        self._limpiar_contenido()

        panel = ttk.LabelFrame(self.contenido, text="Resumen del sistema", padding=25)
        panel.grid(row=0, column=0, sticky="nsew")
        panel.columnconfigure(0, weight=1)

        ttk.Label(
            panel, text="Bienvenido al panel principal", font=("Arial", 17, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 15))

        resumen = (
            f"Productos registrados: {self.restaurante_servicio.cantidad_productos()}\n"
            f"Usuarios registrados: {self.restaurante_servicio.cantidad_usuarios()}\n\n"
            "Utilice el menú lateral para consultar usuarios o gestionar productos.\n"
            "Los cambios realizados en productos se guardan en productos.json."
        )
        ttk.Label(panel, text=resumen, justify="left", font=("Arial", 11)).grid(
            row=1, column=0, sticky="nw"
        )

    def _mostrar_productos(self):
        self._limpiar_contenido()

        contenedor = ttk.Frame(self.contenido)
        contenedor.grid(row=0, column=0, sticky="nsew")
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        ttk.Label(
            contenedor, text="Gestión de productos", font=("Arial", 16, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        formulario = ttk.LabelFrame(
            contenedor, text="Datos del producto", padding=12
        )
        formulario.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        for col in range(5):
            formulario.columnconfigure(col, weight=1)

        campos = [
            ("ID", self.id_var),
            ("Nombre", self.nombre_var),
            ("Categoría", self.categoria_var),
            ("Precio", self.precio_var),
            ("Cantidad", self.cantidad_var),
        ]
        for columna, (texto, variable) in enumerate(campos):
            ttk.Label(formulario, text=f"{texto}:").grid(
                row=0, column=columna, sticky="w", padx=4
            )
            ttk.Entry(formulario, textvariable=variable).grid(
                row=1, column=columna, sticky="ew", padx=4, pady=(3, 8)
            )

        acciones = ttk.Frame(formulario)
        acciones.grid(row=2, column=0, columnspan=5, pady=(4, 0))
        ttk.Button(
            acciones, text="Registrar", command=self._registrar_producto
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones, text="Cargar / Consultar", command=self._cargar_producto
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones, text="Actualizar", command=self._actualizar_producto
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones, text="Eliminar", command=self._eliminar_producto
        ).pack(side="left", padx=4)
        ttk.Button(
            acciones, text="Limpiar", command=self._limpiar_formulario
        ).pack(side="left", padx=4)

        tabla_frame = ttk.LabelFrame(
            contenedor, text="Productos registrados", padding=8
        )
        tabla_frame.grid(row=2, column=0, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)

        columnas = ("id", "nombre", "categoria", "precio", "cantidad")
        self.tabla_productos = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", height=12
        )
        encabezados = {
            "id": "ID",
            "nombre": "Producto",
            "categoria": "Categoría",
            "precio": "Precio",
            "cantidad": "Cantidad",
        }
        anchos = {
            "id": 60,
            "nombre": 220,
            "categoria": 160,
            "precio": 100,
            "cantidad": 100,
        }
        for columna in columnas:
            self.tabla_productos.heading(columna, text=encabezados[columna])
            self.tabla_productos.column(
                columna, width=anchos[columna], anchor="center"
            )

        barra = ttk.Scrollbar(
            tabla_frame, orient="vertical", command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=barra.set)
        self.tabla_productos.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")

        ttk.Label(contenedor, textvariable=self.estado_var).grid(
            row=3, column=0, sticky="w", pady=(8, 0)
        )
        self._actualizar_tabla_productos()

    def _mostrar_usuarios(self):
        self._limpiar_contenido()

        panel = ttk.LabelFrame(
            self.contenido, text="Consulta de usuarios", padding=10
        )
        panel.grid(row=0, column=0, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        ttk.Label(
            panel, text="Usuarios registrados", font=("Arial", 16, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        columnas = ("id", "nombre", "usuario", "rol")
        tabla = ttk.Treeview(panel, columns=columnas, show="headings", height=14)
        encabezados = {
            "id": "ID",
            "nombre": "Nombre",
            "usuario": "Usuario",
            "rol": "Rol",
        }
        for columna in columnas:
            tabla.heading(columna, text=encabezados[columna])
            tabla.column(columna, anchor="center", width=160)

        for usuario in self.restaurante_servicio.listar_usuarios():
            tabla.insert(
                "", tk.END, values=(usuario.id, usuario.nombre, usuario.usuario, usuario.rol)
            )
        tabla.grid(row=1, column=0, sticky="nsew")

    def _registrar_producto(self):
        try:
            producto = self.restaurante_servicio.registrar_producto(
                self.id_var.get(),
                self.nombre_var.get(),
                self.categoria_var.get(),
                self.precio_var.get(),
                self.cantidad_var.get(),
            )
            self.estado_var.set(f"Producto '{producto.nombre}' registrado correctamente.")
            self._actualizar_tabla_productos()
            self._limpiar_formulario()
        except ValueError as error:
            messagebox.showwarning("Validación", str(error))

    def _cargar_producto(self):
        producto = self.restaurante_servicio.buscar_producto(self.id_var.get())
        if producto is None:
            messagebox.showinfo("Consulta", "No se encontró un producto con ese ID.")
            return

        self.id_var.set(str(producto.id))
        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(f"{producto.precio:.2f}")
        self.cantidad_var.set(str(producto.cantidad))
        self.estado_var.set(f"Producto '{producto.nombre}' cargado en el formulario.")

    def _actualizar_producto(self):
        try:
            producto = self.restaurante_servicio.actualizar_producto(
                self.id_var.get(),
                self.nombre_var.get(),
                self.categoria_var.get(),
                self.precio_var.get(),
                self.cantidad_var.get(),
            )
            self.estado_var.set(f"Producto '{producto.nombre}' actualizado correctamente.")
            self._actualizar_tabla_productos()
        except ValueError as error:
            messagebox.showwarning("Validación", str(error))

    def _eliminar_producto(self):
        producto = self.restaurante_servicio.buscar_producto(self.id_var.get())
        if producto is None:
            messagebox.showinfo("Eliminar", "No se encontró un producto con ese ID.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar el producto '{producto.nombre}'?",
        )
        if not confirmar:
            return

        try:
            eliminado = self.restaurante_servicio.eliminar_producto(self.id_var.get())
            self.estado_var.set(f"Producto '{eliminado.nombre}' eliminado correctamente.")
            self._actualizar_tabla_productos()
            self._limpiar_formulario()
        except ValueError as error:
            messagebox.showwarning("Validación", str(error))

    def _actualizar_tabla_productos(self):
        if self.tabla_productos is None:
            return

        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.id,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.cantidad,
                ),
            )

    def _limpiar_formulario(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.cantidad_var.set("")
