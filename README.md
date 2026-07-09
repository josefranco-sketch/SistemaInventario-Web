# Sistema Web Mayorista para Importadora — Los Altos

Sistema web con catálogo digital público, cotizaciones en línea, panel
administrativo y sistema de ventas en tienda, conectados a un mismo
inventario.

> **Deploy (demo):** https://sistema-inventario-web-josefranco-sketchs-projects.vercel.app
>
> Usuarios de la demo: `admin` / `admin123` y `vendedor` / `venta123`.
>
> La demo en línea corre en Vercel como función serverless con una base de
> datos de demostración: todo funciona (catálogo, cotizaciones, login,
> ventas), pero los cambios hechos en línea son **temporales** — cuando la
> función se reinicia, la demo vuelve a su estado inicial. La subida de
> imágenes solo está disponible en local (el filesystem del deploy es de
> solo lectura). La operación real del negocio es local.

## Descripción

Este proyecto consiste en el desarrollo de un sistema web para una empresa importadora que vende productos al por mayor en Guatemala, principalmente en las categorías de cosméticos, juguetes y flores. El objetivo principal es digitalizar el catálogo de productos, controlar el inventario en tienda y registrar ventas internas de forma más ordenada, evitando el uso de talonarios manuales y reduciendo errores en precios, cantidades y disponibilidad.

La plataforma está pensada para dos tipos de uso: una página pública donde los clientes pueden consultar el catálogo mayorista y realizar cotizaciones, y un sistema interno donde el administrador y los vendedores pueden gestionar productos, ventas e inventario en tiempo real.

## Módulos principales

### Página web pública

La página pública funciona como un catálogo mayorista para clientes, con productos organizados por categorías (Cosméticos, Juguetes y Flores). Cada producto muestra nombre, código, imagen, categoría, presentación de venta, precio, cantidad mínima de compra y estado de disponibilidad. Por seguridad, el cliente no puede ver la cantidad exacta de inventario, únicamente estados generales:

- Disponible
- Baja disponibilidad
- Agotado

Los clientes pueden agregar productos a una cotización (que arranca con la cantidad mínima de venta de cada categoría) y enviarla con sus datos. Al enviarla reciben un número único de cotización (ej. COT-0001) y la solicitud llega a la bandeja de los vendedores.

### Panel administrativo

El administrador puede gestionar productos (crear, editar, activar, inactivar y archivar — nunca se eliminan físicamente), subir imágenes, controlar el inventario en tienda con historial de movimientos (usuario, fecha y motivo obligatorios), configurar el umbral de "bajo stock" por subcategoría y administrar los usuarios internos con sus roles. El dashboard muestra indicadores reales: total de productos, productos activos, bajo stock, cotizaciones pendientes, pedidos recientes y usuarios.

### Sistema de ventas

Los vendedores cuentan con un panel interno donde buscan productos por código, nombre o descripción, arman pedidos con cálculo automático de subtotales y total, revisan la bandeja de cotizaciones recibidas y las convierten en pedidos, marcan pedidos como pagados y generan comprobantes internos de venta (no fiscales). El inventario se descuenta únicamente cuando el pedido se marca como pagado, una sola vez, validando antes que haya existencias suficientes.

## Reglas de negocio principales

- **Producto único:** un solo registro de producto alimenta catálogo, inventario, cotizaciones y ventas.
- **El inventario solo baja al confirmar el pago.** Las cotizaciones y los pedidos pendientes nunca descuentan stock, y un pedido pagado no puede descontarse dos veces.
- **Los productos no se eliminan:** solo cambian de estado (Activo / Inactivo / Archivado). Los inactivos y archivados desaparecen del catálogo público.
- **El cliente público nunca ve el stock exacto,** solo el badge de disponibilidad, que se calcula automáticamente según el inventario y el umbral de su subcategoría.
- **Cada movimiento de inventario deja historial** con usuario, fecha y motivo.
- **Los vendedores pueden marcar pedidos como pagados** (no es exclusivo del administrador).

### Reglas de venta mínima por categoría

- **Cosméticos:** se venden por caja o display completo (no hay venta por unidad individual).
- **Juguetes:** con precio mayor a Q20, mínimo 3 unidades por modelo; con precio de Q20 o menos, mínimo 6 unidades (media docena).
- **Flores:** se venden por ramos; cada código es un color/estilo. Mínimo 3 ramos por código.

El sistema valida estos mínimos al armar pedidos y al convertir cotizaciones (si un cliente cotizó menos del mínimo, la cantidad se ajusta hacia arriba y se le avisa al vendedor).

## Tecnologías utilizadas

- **Python 3 + Flask** — aplicación web con render en el servidor.
- **Jinja2** — plantillas HTML.
- **Bootstrap 5 + CSS propio** — interfaz responsive con Design System propio (paleta en variables CSS).
- **SQLite + SQLAlchemy** — base de datos y ORM.
- **Flask-Login** — autenticación y sesiones de usuarios internos.
- **Flask-WTF / WTForms** — formularios con validaciones y protección CSRF.
- **Git + GitHub** — control de versiones con flujo de ramas `feature/* → dev` y Pull Requests.

**Arquitectura:** patrón Application Factory (`create_app()`) con Blueprints por módulo (`public`, `quotes`, `auth`, `admin`, `sales`) y separación de capas: rutas (HTTP) → servicios (reglas de negocio) → modelos (SQLAlchemy) → templates (solo presentación).

## Cómo ejecutar el proyecto localmente

Requisitos: Python 3.10 o superior.

```bash
# 1. Clonar el repositorio y entrar a la carpeta
git clone https://github.com/josefranco-sketch/SistemaInventario-Web.git
cd SistemaInventario-Web

# 2. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

# 3. Instalar las dependencias
pip install -r requirements.txt

# 4. Crear el usuario administrador y el catálogo inicial de ejemplo
python seed_admin.py             # pide los datos; Enter acepta los valores por defecto
python seed_catalog.py           # categorías, subcategorías y productos de ejemplo

# 5. Iniciar el servidor
python run.py
```

La aplicación queda en `http://127.0.0.1:5000`. La base de datos SQLite se crea sola en `instance/app.db`.

> Nota para Mac: si el navegador muestra "acceso denegado" en el puerto 5000, desactiva el *Receptor de AirPlay* en Configuración del Sistema (usa ese puerto), o cierra la pestaña y abre una nueva.

### Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador |

El vendedor de prueba se crea desde el panel: **Usuarios → Nuevo usuario** (rol Vendedor).

### Configuración

- `SECRET_KEY`: se lee de la variable de entorno del mismo nombre; si no existe, usa un valor por defecto **solo para desarrollo**.
- No se necesita ninguna otra configuración para correr en local.

### Scripts útiles

| Script | Para qué sirve |
|---|---|
| `seed_admin.py` | Crea el usuario administrador inicial (por consola). |
| `seed_catalog.py` | Siembra categorías, subcategorías y productos de ejemplo (se puede repetir; no duplica). |
| `verify_integration.py` | Corre 9 verificaciones automáticas de las reglas de negocio de punta a punta y deja la base como estaba. |
| `migrate_payment_fields.py` | Solo para bases creadas antes del Sprint 5.3 (agrega columnas de pago). Un clon nuevo no lo necesita. |
| `build_demo_db.py` | Regenera la base de demostración del deploy (`deploy/demo_app.db`). |

## Estructura del proyecto

```
run.py                      # punto de entrada
config.py                   # configuración central
requirements.txt
seed_admin.py / seed_catalog.py / verify_integration.py
app/
  __init__.py               # create_app(): registra blueprints, login y errores
  extensions.py             # instancias únicas de SQLAlchemy y Flask-Login
  models/                   # tablas: User, Category, Subcategory, Product,
                            # Inventory, InventoryMovement, Order, Quote...
  services/                 # reglas de negocio: productos, inventario,
                            # pedidos, cotizaciones, catálogo, usuarios
  blueprints/
    public/                 # home, catálogo, detalle de producto
    quotes/                 # cotización pública
    auth/                   # login/logout y control de roles
    admin/                  # dashboard, productos, inventario, usuarios
    sales/                  # panel vendedor, pedidos, pagos, comprobantes
  templates/                # vistas Jinja2 por módulo
  static/                   # css por área (styles, admin, sales) e imágenes
```

## Flujo completo del sistema

```
Administrador crea producto y registra inventario
        ↓
Producto aparece en el catálogo público (con badge de disponibilidad)
        ↓
Cliente arma su cotización y la envía (recibe número COT)
        ↓
Vendedor la ve en su bandeja y la convierte en pedido (pendiente de pago)
        ↓                          — el inventario NO cambia —
Cliente paga en tienda y el vendedor marca el pedido como pagado
        ↓
Inventario se descuenta (una vez, con historial) y la disponibilidad
pública se actualiza sola
        ↓
Se genera el comprobante interno de venta
```

## Qué se investigó fuera del curso

El curso cubrió los fundamentos de Python (variables, condicionales, ciclos, listas, diccionarios, funciones y modularidad). Para construir este proyecto se investigó adicionalmente:

- **Flask**: rutas, blueprints, sesiones, manejo de errores y el patrón Application Factory.
- **Jinja2**: herencia de plantillas, macros y filtros.
- **SQLAlchemy**: definición de modelos, relaciones entre tablas y consultas con filtros.
- **Flask-Login**: autenticación, protección de rutas y roles.
- **Flask-WTF/WTForms**: validación de formularios, subida de archivos y protección CSRF.
- **Werkzeug**: hash seguro de contraseñas.
- **Bootstrap 5**: sistema de grid, componentes y diseño responsive.
- **Git Flow**: trabajo con ramas feature, Pull Requests y revisión de código.

## Alcance y limitaciones

Este sistema **no** incluye (decisión de alcance del proyecto):

- Facturación fiscal ni integración con SAT (los comprobantes son internos, sin valor tributario).
- Pagos en línea (el pago se realiza y registra en tienda).
- Inventario de bodega (solo existencias de sala de ventas).
- Manejo de proveedores ni control de importaciones.
- Cálculo de impuestos.

## Estado del proyecto

Proyecto funcional de punta a punta: catálogo público, cotizaciones, panel administrativo (productos, inventario, usuarios), sistema de ventas (pedidos, pagos, comprobantes) e integración completa entre módulos, con las reglas de negocio verificadas automáticamente (`verify_integration.py`). Desarrollado por sprints con un Pull Request por módulo (ver `PR_tracker.md`).
