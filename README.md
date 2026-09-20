# Restaurante App - Semana 14

## Descripción

Proyecto académico de Programación Orientada a Objetos correspondiente a la **Semana 14: Componentes y contenedores**.

La aplicación continúa la evolución de `restaurante_app` y mantiene una arquitectura modular separando datos, modelos, servicios, interfaz gráfica y punto de entrada. La interfaz fue mejorada con componentes y contenedores de **Tkinter/ttk** para consultar usuarios y gestionar productos.

## Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
└── main.py

README.md
```

## Componentes y contenedores utilizados

- `Tk` como ventana principal.
- `ttk.Frame` para dividir la interfaz en áreas.
- `ttk.LabelFrame` para agrupar navegación, formularios y tablas.
- `ttk.Label` para títulos, etiquetas y mensajes.
- `ttk.Entry` para capturar datos del producto.
- `ttk.Button` con `command=` para ejecutar las acciones.
- `ttk.Treeview` para mostrar productos y usuarios.
- `ttk.Scrollbar` para apoyar la visualización de registros.
- Gestores de geometría `grid()` y `pack()` usados según el contenedor.

## Mejoras realizadas en la Semana 14

- Se conserva el inicio de sesión gráfico de la semana anterior.
- Se mejora la organización del panel principal mediante contenedores.
- Se mantiene la consulta de usuarios.
- Se incorpora un formulario completo de productos.
- La tabla de productos se actualiza después de registrar, actualizar o eliminar.
- Las validaciones y operaciones se mantienen dentro de `RestauranteServicio`.
- La interfaz no lee ni escribe directamente los archivos JSON.
- Los cambios de productos se guardan en `productos.json`.

## Operaciones sobre productos

Desde la sección **Productos** se puede:

1. **Registrar** un producto nuevo.
2. **Cargar / Consultar** un producto por su ID.
3. **Actualizar** los datos de un producto existente.
4. **Eliminar** un producto.
5. **Limpiar** el formulario.

Las operaciones validan ID, nombre, categoría, precio y cantidad antes de modificar los datos.

## Persistencia

La información se conserva en archivos JSON dentro de `restaurante_app/datos/`.

- `usuarios.json`: contiene las credenciales y roles de prueba.
- `productos.json`: contiene los productos del restaurante y recibe los cambios realizados desde la interfaz.

La lectura y escritura se realiza mediante `ArchivoServicio`. `RestauranteServicio` concentra las reglas y solicita la persistencia correspondiente.

## Credenciales de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | admin123 | Administrador |
| mesero | 1234 | Mesero |
| caja | caja123 | Cajero |

## Ejecución

Se requiere Python 3 con Tkinter.

1. Abra una terminal en la carpeta del repositorio.
2. Ingrese a la carpeta de la aplicación:

```bash
cd restaurante_app
```

3. Ejecute:

```bash
python main.py
```

En Windows también puede utilizar:

```bash
py main.py
```

## Comprobación sugerida

1. Inicie sesión con `admin / admin123`.
2. Abra la sección **Usuarios** y compruebe la consulta de registros.
3. Abra **Productos**.
4. Registre un producto con un ID nuevo.
5. Consulte el producto por su ID.
6. Modifique alguno de sus datos y presione **Actualizar**.
7. Elimine el producto.
8. Cierre y vuelva a ejecutar la aplicación para comprobar la persistencia.

## Observación

El proyecto utiliza botones mediante `command=` y no implementa manejo avanzado de eventos con `bind()`, doble clic, teclado o mouse, de acuerdo con el alcance de la Semana 14.
