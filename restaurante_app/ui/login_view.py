import tkinter as tk
from tkinter import ttk


class LoginView(ttk.Frame):
    def __init__(self, master, restaurante_servicio, on_login_success):
        super().__init__(master, padding=30)
        self.restaurante_servicio = restaurante_servicio
        self.on_login_success = on_login_success

        self.usuario_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.mensaje_var = tk.StringVar()

        self._construir_interfaz()

    def _construir_interfaz(self):
        self.columnconfigure(0, weight=1)

        tarjeta = ttk.LabelFrame(self, text="Acceso al sistema", padding=25)
        tarjeta.grid(row=0, column=0, padx=30, pady=40)
        tarjeta.columnconfigure(1, weight=1)

        ttk.Label(
            tarjeta, text="Restaurante App", font=("Arial", 22, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 6))
        ttk.Label(
            tarjeta, text="Semana 14 - Componentes y contenedores"
        ).grid(row=1, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(tarjeta, text="Usuario:").grid(
            row=2, column=0, sticky="e", padx=8, pady=8
        )
        entrada_usuario = ttk.Entry(
            tarjeta, textvariable=self.usuario_var, width=30
        )
        entrada_usuario.grid(row=2, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(tarjeta, text="Contraseña:").grid(
            row=3, column=0, sticky="e", padx=8, pady=8
        )
        ttk.Entry(
            tarjeta,
            textvariable=self.contrasena_var,
            show="*",
            width=30,
        ).grid(row=3, column=1, sticky="ew", padx=8, pady=8)

        ttk.Button(
            tarjeta, text="Ingresar", command=self._intentar_ingreso
        ).grid(row=4, column=0, columnspan=2, pady=14)

        ttk.Label(
            tarjeta, textvariable=self.mensaje_var, font=("Arial", 10)
        ).grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Label(
            tarjeta,
            text="Credencial de prueba: admin / admin123",
            font=("Arial", 9),
        ).grid(row=6, column=0, columnspan=2, pady=(12, 0))

        entrada_usuario.focus()

    def _intentar_ingreso(self):
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get().strip()

        if not usuario or not contrasena:
            self.mensaje_var.set("Complete el usuario y la contraseña.")
            return

        usuario_validado = self.restaurante_servicio.validar_acceso(
            usuario, contrasena
        )
        if usuario_validado is None:
            self.mensaje_var.set("Credenciales incorrectas.")
            return

        self.mensaje_var.set("")
        self.on_login_success(usuario_validado)
