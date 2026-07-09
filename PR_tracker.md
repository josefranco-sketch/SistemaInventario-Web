# Pull Request Tracker

## Sistema Integral de Gestión Comercial para una Importadora Mayorista

---

## Propósito

Este documento registra el historial oficial de desarrollo del proyecto mediante
Pull Requests (PR).

Su objetivo es mantener la trazabilidad de cada fase y sprint desarrollado,
indicando el alcance del trabajo realizado, la rama utilizada, el Pull Request
correspondiente y el estado de integración en la rama **dev**.

Este documento complementa:

- Documento 4 – Development Roadmap
- Project Manager
- Historial de GitHub

No reemplaza ninguno de ellos; únicamente sirve como bitácora técnica del
desarrollo del proyecto.

---

## Flujo de trabajo utilizado

Cada Sprint seguirá el siguiente flujo:

Roadmap
↓
Branch feature
↓
Desarrollo
↓
Pruebas
↓
Revisión
↓
Commit
↓
Push
↓
Pull Request
↓
Actualización de este documento
↓
Actualización del Project Manager
↓
Merge hacia dev

---

# Historial de Pull Requests
# Fase 1 – Análisis y Diseño

> **Nota**

Durante esta fase no se realizaron Pull Requests debido a que el proyecto se
encontraba en la etapa de análisis, diseño y planificación.

El trabajo realizado consistió en la elaboración de la documentación oficial
que serviría como base para todo el desarrollo posterior.

## Documentos elaborados

- Documento 0 – Project Context
- Documento 1 – Software Design Document (SDD)
- Documento 2 – Arquitectura Técnica
- Documento 3 – Design System (UI/UX Guide)
- Documento 4 – Development Roadmap
- Documento 5 – Chat Development Guide
- Documento 6 – Architecture Decision Record (ADR)

**Estado**

✅ Fase completada.

**Pull Request**

No aplica.

# PR #1 — Configuración inicial del proyecto Flask

## Información general

**Fase**

2 – Configuración del Proyecto

**Sprint**

Fase 2 completa

**Branch**

feature/configuracion-flask

**Estado**

✅ Completado

---

## Objetivo

Construir la base técnica del proyecto Flask para permitir el desarrollo del
resto del sistema siguiendo la arquitectura definida.

---

## Trabajo realizado

- Configuración del entorno virtual.
- Configuración del repositorio Git.
- Inicialización del proyecto Flask.
- Implementación del patrón Application Factory.
- Configuración central mediante `config.py`.
- Inicialización de SQLAlchemy.
- Inicialización de Flask-Login.
- Creación de la estructura modular del proyecto.
- Configuración de Blueprints.
- Organización inicial de templates y archivos estáticos.
- Configuración del archivo `run.py`.
- Configuración de `.gitignore`.
- Verificación del correcto funcionamiento de Flask.

---

## Archivos principales

- run.py
- config.py
- app/__init__.py
- app/extensions.py
- app/blueprints/
- app/templates/
- app/static/
- requirements.txt
- .gitignore

---

## Pull Request

**PR:** #1

**Enlace**

> *((https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/configuracion-flask?expand=1))*

---

## Observaciones

Durante esta fase se estableció la base técnica del proyecto.
A partir de este punto el desarrollo continuará utilizando un Pull Request por
Sprint para mantener una trazabilidad más detallada del proyecto.

# PR #2 – Navbar y Footer

## Información general

**Fase**

3 – Módulo Público

**Sprint**

3.1 – Navbar y Footer

**Branch**

feature/navbar-footer

**Estado**

✅ Completado y fusionado en `dev`

---

## Objetivo

Construir la base visual del módulo público mediante una Navbar y un Footer reutilizables, alineados con la Arquitectura Técnica y el Design System.

---

## Trabajo realizado

- Creación de la plantilla base pública (`base.html`).
- Desarrollo de la Navbar pública reutilizable.
- Desarrollo del Footer público reutilizable.
- Integración de ambos componentes mediante Jinja2.
- Creación de la primera vista `home.html`.
- Actualización de la ruta pública para renderizar la vista Home.
- Integración del logo oficial de la empresa.
- Implementación de la paleta oficial y estilos CSS.
- Validación responsive en escritorio y dispositivos móviles.
- Revisión visual y ajustes conforme al Design System.

---

## Archivos principales

- PR_tracker.md
- app/__init__.py
- app/blueprints/public/routes.py
- app/static/css/styles.css
- app/static/img/logo-los-altos.svg
- app/templates/base.html
- app/templates/partials/navbar.html
- app/templates/partials/footer.html
- app/templates/public/home.html

---

## Pull Request

**PR:** #2

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/feature/navbar-footer?expand=1

---

## Observaciones

Durante el desarrollo se detectó que la especificación visual de la Navbar pública necesitaba mayor detalle para evitar decisiones de diseño durante la implementación. La sección correspondiente del Design System fue actualizada desde el Project Manager antes de continuar con el desarrollo, manteniendo la coherencia entre la documentación y el código.

El Sprint 3.1 finalizó con la Navbar y el Footer completamente funcionales, reutilizables, responsive y alineados con la arquitectura, el Roadmap y el Design System.

## Sprint 3.3 – Catálogo

- **Branch:** `feature/catalog`
- **Pull Request:** `#4 – Feature: Add public catalog`
- **Estado:** Completado

### Resumen
Se implementó el catálogo público con productos reales de prueba, filtros por categoría, subcategoría y disponibilidad, búsqueda por texto y tarjetas alineadas al Design System. También se validó responsive, navegación pública y estructura modular.

### Archivos modificados
- `app/blueprints/public/routes.py`
- `app/static/css/styles.css`
- `app/templates/partials/navbar.html`
- `app/templates/public/catalog.html`
- `app/static/img/products/labial-mate-mes3107.png`
- `app/static/img/products/juguete.png`
- `app/static/img/products/tulipan-rojo.png`

### Pruebas realizadas
- Búsqueda por código, nombre y descripción.
- Filtro por categoría.
- Filtro por subcategoría dependiente de la categoría.
- Filtro por disponibilidad.
- Validación visual responsive en navegador.

### Decisiones o impacto documental
- ADR: sin cambios.
- Roadmap: Sprint 3.3 completado.
- Design System: sin cambios estructurales.
- Arquitectura Técnica: sin cambios estructurales.

**PR:** #4

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/feature/catalog?expand=1


### Pendientes
- Ninguno bloqueante para este sprint.

Sprint 3.4 – Detalle del Producto

Branch:
feature/product-detail

Pull Request:
#5 – Feature: Add public product detail page

Estado:
✅ Completado

Resumen:
- Se implementó la página pública de detalle del producto.
- Se creó la ruta pública para visualizar un producto por su código.
- Se desarrolló la plantilla product_detail.html siguiendo el Design System.
- Se agregaron estilos específicos para la ficha del producto.
- Se conectó el catálogo con la vista de detalle mediante navegación directa.
- Se implementó el retorno al catálogo conservando los filtros aplicados.
- Se reutilizaron los productos reales de prueba del Sprint 3.3.
- Se respetó la regla de no mostrar cantidades exactas de inventario.
- Se mantuvo la arquitectura Flask + Jinja2 + Bootstrap + CSS propio.

Archivos modificados:
- app/blueprints/public/routes.py
- app/templates/public/catalog.html
- app/templates/public/product_detail.html
- app/static/css/styles.css

link:
https://github.com/josefranco-sketch/SistemaInventario-Web/pull/new/feature/product-detail
# PR #7 – Admin Login (Sprint 4.1)

## Información general

**Fase**

4 – Panel Administrativo

**Sprint**

4.1 – Login Administrativo

**Branch**

feature/admin-login

**Estado**

🔍 En revisión

---

## Objetivo

Crear el acceso interno al sistema: autenticación real con Flask-Login,
modelo de usuario con roles (administrador/vendedor), protección de rutas
internas y pantalla de login alineada al Design System.

---

## Trabajo realizado

- Creación del modelo `User` con SQLAlchemy (tabla `users`): username único,
  nombre, rol (admin/vendedor), estado activo y contraseña como hash
  (Werkzeug, nunca texto plano).
- Nace la capa `app/models/` prevista en la Arquitectura Técnica.
- Nace la capa `app/services/` con `auth_service.py`: la validación de
  credenciales (usuario existe, está activo, contraseña coincide) vive en
  servicios, no en rutas ni templates.
- Implementación del blueprint `auth`: rutas de login (GET/POST) y logout.
- Formulario `LoginForm` con Flask-WTF (validaciones y token CSRF).
- `user_loader` real en `create_app()` (antes retornaba `None`).
- Configuración de `login_view`: rutas protegidas redirigen al login con
  mensaje claro y regresan a la ruta original tras autenticarse (`?next=`),
  aceptando solo rutas internas.
- Decorador `admin_required` (control de rol) en el blueprint `auth`.
- Pantalla base del panel administrativo (`/admin/`) protegida con
  `@login_required` + `@admin_required`; será reemplazada por el dashboard
  completo en el Sprint 4.2.
- Vista de login: tarjeta centrada de máximo 420px, paleta oficial vía
  variables CSS, campos con objetivo táctil de 44px, responsive.
- Partial de mensajes flash reutilizable incluido en `base.html`.
- Navbar: enlaces de Panel (solo admin) y Cerrar sesión cuando hay sesión.
- Script de consola `seed_admin.py` para crear el usuario administrador de
  prueba (pide datos con `input()`, guarda hash, evita duplicados).
- Creación de tablas con `db.create_all()` al iniciar la aplicación.
- `.gitignore` actualizado: `instance/` y `*.db` no se suben al repositorio.

---

## Archivos principales

- app/models/__init__.py, app/models/user.py (nuevos)
- app/services/__init__.py, app/services/auth_service.py (nuevos)
- app/blueprints/auth/routes.py, forms.py, decorators.py (nuevos)
- app/blueprints/admin/routes.py (nuevo)
- app/templates/auth/login.html, app/templates/admin/dashboard.html (nuevos)
- app/templates/partials/flash_messages.html (nuevo)
- seed_admin.py (nuevo)
- app/__init__.py, app/blueprints/auth/__init__.py,
  app/blueprints/admin/__init__.py (modificados)
- app/templates/base.html, app/templates/partials/navbar.html (modificados)
- app/static/css/styles.css, .gitignore (modificados)

---

## Pruebas realizadas

- Ruta protegida sin sesión redirige al login (302 → /login?next=/admin/).
- Login con credenciales incorrectas muestra mensaje genérico sin revelar
  cuál dato falló.
- Login correcto crea sesión y regresa a la ruta original (?next=).
- Usuario ya autenticado que visita /login es redirigido a su panel.
- Logout cierra la sesión; la ruta protegida vuelve a exigir login.
- Usuario inactivo no puede iniciar sesión.
- Vendedor autenticado no puede entrar a /admin/ (control de rol).
- POST sin token CSRF no procesa el login ni crea sesión.
- Campos vacíos muestran errores de validación por campo.
- La contraseña se guarda como hash scrypt (verificado en la base de datos).
- Módulo público intacto: /, /catalog, /catalog/<código> y /cotizacion
  responden 200.

---

## Pull Request

**PR:** #7

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/admin-login?expand=1

---

## Observaciones

Temas de la Sección 02 (rúbrica UFM) utilizados en este sprint: variables y
tipos de datos (textos, booleanos), entrada y salida por consola (`input()` /
`print()` en `seed_admin.py`), condicionales (`if`/`else` en el servicio de
autenticación y redirección por rol), funciones propias con parámetros y
`return` (`authenticate_user`, `ask_value`, `create_admin_user`,
`_safe_next_url`), modularidad (modelos, servicios, formularios y rutas en
archivos separados conectados con `import`, más bloque
`if __name__ == "__main__":` en `seed_admin.py`) y librería estándar
(`functools.wraps` en el decorador de roles, `os` en configuración).

# PR #8 – Admin Dashboard (Sprint 4.2)

## Información general

**Fase**

4 – Panel Administrativo

**Sprint**

4.2 – Dashboard Administrativo

**Branch**

feature/admin-dashboard

**Estado**

🔍 En revisión

---

## Objetivo

Crear la pantalla principal del panel administrativo: layout interno
reutilizable (sidebar + header), dashboard con indicadores y accesos rápidos
hacia los módulos del sistema.

---

## Trabajo realizado

- Plantilla base administrativa `base_admin.html`, separada del sitio
  público, con bloques reutilizables (`page_title`, `admin_content`) para
  todas las vistas internas de la Fase 4 en adelante.
- Sidebar según el Design System: 256px fija en escritorio, fondo carbón
  (`--la-carbon`), elemento activo en rosa; en móvil se convierte en menú
  deslizable (offcanvas de Bootstrap).
- Navegación interna completa: Dashboard activo y los módulos futuros
  (Productos, Inventario, Usuarios, Cotizaciones, Ventas) visibles pero
  deshabilitados, con el sprint/fase en que estarán disponibles.
- Header administrativo con título de página, usuario en sesión, badge de
  rol y botón de salir; botón hamburguesa en móvil.
- Servicio `dashboard_service.py`: entrega los indicadores en un
  diccionario; ningún cálculo vive en el template. El conteo de usuarios
  internos es real (tabla `users`); productos, inventario, cotizaciones y
  ventas entregan valores de demostración marcados con la bandera
  `demo_data` hasta que existan sus modelos (Sprints 4.3, 4.4, Fases 5-6).
- Dashboard con 6 tarjetas KPI (total de productos, activos, bajo stock,
  cotizaciones pendientes, pedidos recientes, usuarios internos) y aviso
  visible de datos de demostración.
- Accesos rápidos hacia los 5 módulos internos (deshabilitados con su
  sprint) más el acceso real al sitio público.
- Nuevo `admin.css` (CSS por área, según la convención del proyecto), que
  consume las variables de la paleta oficial sin hardcodear colores.
- Bootstrap Icons integrado en el layout administrativo (única librería de
  iconos del Design System).
- Ruta `/admin/` protegida con `@login_required` + `@admin_required`
  (sin cambios de seguridad respecto al Sprint 4.1).

---

## Archivos principales

- app/templates/admin/base_admin.html (nuevo)
- app/static/css/admin.css (nuevo)
- app/services/dashboard_service.py (nuevo)
- app/templates/admin/dashboard.html (reescrito sobre la pantalla base 4.1)
- app/blueprints/admin/routes.py (modificado)

---

## Pruebas realizadas

- /admin/ sin sesión redirige al login (protección intacta).
- Login como administrador abre el dashboard (200).
- Las 6 tarjetas KPI renderizan sus valores; el conteo de usuarios internos
  sale de la base de datos real.
- El aviso de datos de demostración se muestra.
- Sidebar, marca, offcanvas y Bootstrap Icons presentes en el HTML.
- admin.css se sirve correctamente (200).
- Módulo público intacto: /, /catalog y /cotizacion responden 200.
- Sin errores en el log de Flask.

---

## Pull Request

**PR:** #8

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/admin-dashboard?expand=1

---

## Observaciones

Temas de la Sección 02 (rúbrica UFM) utilizados en este sprint: diccionarios
(el servicio entrega los KPIs como diccionario y las tarjetas se definen como
lista de diccionarios), listas y ciclos `for` (las tarjetas KPI y los accesos
rápidos se recorren con bucles de Jinja2), funciones con `return`
(`get_dashboard_summary`), modularidad (servicio nuevo conectado con
`import`) y condicionales (aviso de datos demo, elemento activo de la
sidebar).

# PR #9 – Admin Products (Sprint 4.3)

## Información general

**Fase**

4 – Panel Administrativo

**Sprint**

4.3 – Gestión de Productos

**Branch**

feature/admin-products

**Estado**

🔍 En revisión

---

## Objetivo

Crear el módulo administrativo de productos con base de datos real:
aquí nace el modelo Product (fuente única de verdad del sistema), junto
con Category y Subcategory.

---

## Trabajo realizado

- Modelos nuevos con SQLAlchemy: `Category` (con slug estable para lógica
  y estilos), `Subcategory` (con umbral de bajo stock configurable por
  subcategoría, listo para el Sprint 4.4) y `Product` (código único
  indexado, nombre, descripción, marca, precio Numeric, presentación
  comercial, unidad de venta, estado, disponibilidad pública, imagen,
  fechas de creación/actualización).
- Producto → Subcategoría → Categoría normalizado: el producto no duplica
  la categoría; se obtiene por la relación (regla de fuente única).
- Servicio `products_service.py`: listado con filtros (texto, categoría,
  estado), creación y edición validando código único (normalizado a
  mayúsculas), cambio de estado activo/inactivo/archivado como única vía
  de "retiro" (NUNCA eliminación física, regla ADR), y la regla de venta
  mínima por categoría del ADR (cosméticos por caja/display; juguetes 3
  unidades arriba de Q20 y 6 debajo; flores 3 ramos por código).
- Formularios Flask-WTF: `ProductForm` (validaciones + CSRF, subcategorías
  agrupadas por categoría en el select) y `StatusChangeForm` (los cambios
  de estado viajan por POST con CSRF, nunca por GET).
- Rutas admin protegidas: listado con filtros, crear, editar y cambio de
  estado; todas con @login_required + @admin_required.
- Listado interno con tabla responsive, badges de estado y disponibilidad
  (texto + color), chips de categoría con los colores de identidad de la
  paleta, estado vacío y confirmación antes de archivar.
- Formulario crear/editar compartido con macros Jinja2 para campos.
- Sidebar: "Productos" habilitado con estado activo; dashboard con
  conteos reales de productos (total y activos) y acceso rápido real.
- Script de consola `seed_catalog.py`: siembra idempotente de las 3
  categorías, 9 subcategorías y los 3 productos de demostración del
  catálogo público.
- Corrección durante pruebas: campos opcionales (marca, descripción,
  imagen) manejan None de forma segura en el servicio.

---

## Archivos principales

- app/models/category.py, app/models/product.py (nuevos)
- app/services/products_service.py (nuevo)
- app/blueprints/admin/forms.py (nuevo)
- app/templates/admin/products/list.html, form.html (nuevos)
- seed_catalog.py (nuevo)
- app/blueprints/admin/routes.py, app/models/__init__.py (modificados)
- app/services/dashboard_service.py (conteos reales de productos)
- app/templates/admin/base_admin.html, dashboard.html (modificados)
- app/static/css/admin.css (modificado)

---

## Pruebas realizadas

- Rutas de productos sin sesión redirigen al login.
- Listado muestra los 3 productos sembrados con badges correctos.
- Filtros por texto, categoría y estado funcionan contra la BD.
- Crear producto: guarda, normaliza el código a mayúsculas y redirige.
- Código duplicado (incluso en minúsculas) se rechaza con mensaje claro.
- Validaciones de campos obligatorios muestran errores por campo.
- Editar producto guarda cambios (incluido el caso de campos opcionales
  vacíos, corregido durante las pruebas).
- Ciclo de estados completo: inactivar → archivar → reactivar; estado
  inválido rechazado con aviso; el producto NUNCA desaparece de la BD.
- Regla de venta mínima verificada por categoría y por precio de juguete.
- Dashboard muestra conteos reales; módulo público intacto (sigue con
  datos demo hasta el Sprint 6.1, como marca el Roadmap).

---

## Pull Request

**PR:** #9

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/admin-products?expand=1

---

## Observaciones

La imagen del producto se maneja como nombre de archivo dentro de
static/img/products/ (no upload de archivos): decisión alineada con el
deploy en Vercel, cuyo sistema de archivos es de solo lectura en
serverless. El catálogo público se conectará a estos productos reales en
el Sprint 6.1 (Integración), según el Roadmap.

Temas de la Sección 02 (rúbrica UFM): variables y tipos, condicionales
(regla de venta mínima por categoría y precio), ciclos for (seeds y
templates), listas y diccionarios (CATALOG/PRODUCTS del seed, choices
agrupadas, etiquetas de estado), funciones con parámetros y return (todo
el servicio), modularidad (modelos/servicios/formularios/rutas separados,
if __name__ == "__main__" en seed_catalog.py) y librería estándar
(decimal para precios, datetime en el modelo).

### Adición al PR #9 (misma branch, tras revisión local del usuario)

1. **Fix sidebar en escritorio**: Bootstrap fuerza fondo transparente
   (!important) en offcanvas-lg a partir de 992px y resetea el padding del
   cuerpo, por lo que la sidebar se veía blanca con letras blancas en
   escritorio (en móvil sí se veía bien). Se recupera el fondo carbón y el
   padding dentro del media query de escritorio.
2. **Subida de imágenes desde el panel**: el campo de texto "nombre de
   archivo" se reemplazó por un campo de subida real (Flask-WTF FileField):
   extensiones permitidas PNG/JPG/WEBP, límite de 5 MB (MAX_CONTENT_LENGTH),
   nombre de archivo seguro basado en el código único del producto (ej.
   mes3107.png, así re-subir reemplaza la imagen anterior y nunca chocan dos
   productos), guardado en static/img/products/ desde el servicio. Al editar
   se muestra la imagen actual en miniatura y solo se reemplaza si se sube
   un archivo nuevo. Probado: crear con imagen, editar conservando imagen,
   y rechazo de archivos no-imagen con mensaje claro.

   Nota de alcance: en el deploy de Vercel (Fase 8) el filesystem es de solo
   lectura/efímero, por lo que las imágenes subidas en producción no
   persisten; la administración real del catálogo (y la demo) es local.
   La estrategia de datos para producción se define en la Fase 8.

# PR #10 – Admin Inventory (Sprint 4.4)

## Información general

**Fase**

4 – Panel Administrativo

**Sprint**

4.4 – Gestión de Inventario

**Branch**

feature/admin-inventory

**Estado**

🔍 En revisión

---

## Objetivo

Controlar las existencias en tienda: stock por producto, movimientos con
historial obligatorio, umbral de bajo stock configurable por subcategoría y
disponibilidad pública calculada desde el inventario.

---

## Trabajo realizado

- Modelos nuevos: `Inventory` (existencia por producto, relación 1 a 1 con
  el producto existente — nunca se duplican productos) e
  `InventoryMovement` (historial con usuario, fecha, motivo obligatorio,
  tipo entrada/salida, cantidad y stock antes/después para auditoría).
- Servicio `inventory_service.py`:
  - `register_movement`: valida TODO antes de tocar la base (tipo,
    cantidad positiva, motivo obligatorio, stock suficiente — una salida
    jamás deja stock negativo), actualiza existencia, deja historial y
    recalcula la disponibilidad pública.
  - `compute_availability`: stock 0 → Agotado; 1..umbral → Baja
    disponibilidad; mayor → Disponible. El cliente ve solo el badge,
    nunca el número.
  - Umbral de bajo stock configurable por subcategoría (regla ADR), con
    pantalla de configuración; al cambiar un umbral se recalcula la
    disponibilidad de los productos afectados.
  - `count_low_stock` para el KPI del dashboard (ahora real).
- Vistas admin protegidas: inventario con stock exacto y filtros (texto,
  categoría, solo bajo stock), formulario de movimiento, historial (global
  y por producto) y umbrales por subcategoría.
- La disponibilidad pública dejó de ser manual: se quitó el selector del
  formulario de producto; un producto nuevo nace agotado (sin stock) hasta
  su primera entrada. Nota informativa en el formulario.
- Sidebar y dashboard: Inventario habilitado; KPI de bajo stock real.
- Regla ADR respetada: el inventario NO baja por cotizaciones ni pedidos
  pendientes; el descuento por venta pagada llega en la Fase 5 (reusará
  este servicio para dejar historial).

---

## Archivos principales

- app/models/inventory.py (nuevo)
- app/services/inventory_service.py (nuevo)
- app/templates/admin/inventory/{list,movement_form,history,thresholds}.html (nuevos)
- app/blueprints/admin/routes.py, app/blueprints/admin/forms.py (modificados)
- app/services/products_service.py, app/services/dashboard_service.py (modificados)
- app/templates/admin/{base_admin,dashboard}.html (modificados)
- app/templates/admin/products/form.html (modificado — sin selector manual)
- app/models/__init__.py, app/static/css/admin.css (modificados)

---

## Pruebas realizadas

- Servicio: tipo inválido, cantidad 0, motivo vacío y salida sin stock
  rechazados SIN tocar la base; entradas y salidas actualizan stock e
  historial; transiciones disponible → baja → agotado → disponible
  verificadas; umbral inválido (texto o negativo) rechazado.
- HTTP con sesión real: vista de inventario, movimiento (entrada),
  salida sin motivo rechazada por el formulario, salida excesiva rechazada
  por el servicio con mensaje claro, filtro "solo bajo stock", historial
  global y por producto con usuario visible, umbrales GET/POST.
- Dashboard: KPI de bajo stock real (verificado con umbral modificado).
- Regresión: producto nuevo nace agotado y el formulario ya no tiene
  selector de disponibilidad; módulo público intacto.
- Bugs corregidos durante pruebas: (1) un movimiento rechazado dejaba un
  INSERT pendiente en la sesión; (2) crear el inventario por product_id
  no actualizaba la relación en memoria y podía duplicar la fila. Se
  reestructuró el servicio: validar primero, tocar la base al final, y
  crear el inventario vía relación.

---

## Pull Request

**PR:** #10

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/admin-inventory?expand=1

---

## Observaciones

Decisión de diseño (alineada al Roadmap "preparar disponibilidad pública
según inventario"): la disponibilidad dejó de ser un campo manual del
producto y ahora se deriva del stock y el umbral de la subcategoría. El
badge del catálogo público reflejará esto al integrar en el Sprint 6.1.

Temas de la Sección 02 (rúbrica UFM): condicionales (validaciones del
movimiento y cálculo de disponibilidad), ciclos for y while implícitos en
conteos (count_low_stock recorre productos), listas y diccionarios
(umbrales por formulario dinámico), funciones con parámetros y return
(todo el servicio), modularidad (modelo/servicio/rutas/templates) y
librería estándar (datetime en los movimientos).

# PR #11 – Admin Users (Sprint 4.5)

## Información general

**Fase**

4 – Panel Administrativo

**Sprint**

4.5 – Gestión de Usuarios

**Branch**

feature/admin-users

**Estado**

🔍 En revisión

---

## Objetivo

Gestionar los usuarios internos del sistema (administradores y
vendedores), dejándolos listos para el sistema de ventas de la Fase 5.
Cierra la Fase 4 – Panel Administrativo.

---

## Trabajo realizado

- Servicio `users_service.py`: listado con filtros (texto, rol), creación
  y edición validando username único (normalizado a minúsculas: "Admin" y
  "admin" no pueden coexistir), y activar/inactivar como única forma de
  retiro — los usuarios no se eliminan, para que el historial de
  inventario y las ventas futuras nunca pierdan a su autor.
- Contraseñas SIEMPRE con hash (Werkzeug/scrypt): en creación es
  obligatoria con confirmación (mínimo 6 caracteres); en edición es
  opcional (en blanco conserva la actual) y jamás se muestra ni precarga.
- Reglas de seguridad: un admin no puede desactivarse a sí mismo ni
  cambiarse su propio rol (evita quedarse fuera del sistema); la UI ni
  siquiera muestra el botón para el propio usuario y el servicio lo
  rechaza aunque llegue el POST directo.
- Formularios Flask-WTF con herencia: `UserBaseForm` → `UserCreateForm`
  (contraseña obligatoria + EqualTo) / `UserEditForm` (opcional).
- Rutas protegidas con @login_required + @admin_required: listado, crear,
  editar y toggle activo (POST con CSRF y confirmación al inactivar).
- UI según Design System: tabla con badges de rol (Administrador rosa /
  Vendedor info) y estado, badge "tú" en el propio usuario, filtros y
  estado vacío. Usuarios habilitado en sidebar y dashboard.
- Usuario inactivo no puede iniciar sesión (ya lo validaba el servicio
  de autenticación del 4.1; verificado end-to-end).
- Queda creado el vendedor de demostración (vendedor / venta123) listo
  para el panel de ventas del Sprint 5.1.

---

## Archivos principales

- app/services/users_service.py (nuevo)
- app/templates/admin/users/{list,form}.html (nuevos)
- app/blueprints/admin/routes.py, app/blueprints/admin/forms.py (modificados)
- app/templates/admin/{base_admin,dashboard}.html (modificados)
- app/static/css/admin.css (modificado)

---

## Pruebas realizadas

- Servicio: username normalizado y duplicado rechazado (aun con
  mayúsculas), rol inválido rechazado, contraseña en blanco conserva el
  hash, contraseña nueva lo reemplaza y el login funciona con ella,
  cambio de rol propio rechazado, toggle propio rechazado, usuario
  inactivo no puede autenticarse y reactivado sí.
- HTTP con sesión real: protección sin sesión, listado con badge "tú" y
  sin botón de toggle propio, crear vendedor, contraseñas que no
  coinciden, username duplicado (mensaje visible), edición sin contraseña
  precargada, ciclo inactivar → login rechazado → activar → login OK,
  vendedor sin acceso a /admin/users, auto-toggle rechazado con aviso,
  KPI de usuarios = 2, módulo público intacto, log sin errores.

---

## Pull Request

**PR:** #11

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/admin-users?expand=1

---

## Observaciones

Con este sprint la **Fase 4 – Panel Administrativo queda completada**
(login, dashboard, productos, inventario y usuarios).

Temas de la Sección 02 (rúbrica UFM): condicionales (reglas de seguridad
del servicio), funciones con parámetros y return, diccionarios
(ROLE_LABELS), listas y ciclos (listados y filtros), modularidad
(servicio/formularios/rutas/templates separados) y herencia de clases en
formularios (UserBaseForm → Create/Edit).

# PR #12 – Sales Panel (Sprint 5.1)

## Información general

**Fase**

5 – Sistema de Ventas

**Sprint**

5.1 – Panel de Vendedores y Buscador de Productos

**Branch**

feature/sales-panel

**Estado**

🔍 En revisión

---

## Objetivo

Crear la entrada operativa para vendedores: panel propio con buscador de
productos sobre la fuente única, respetando roles. Inicia la Fase 5.

---

## Trabajo realizado

- Blueprint `sales` activado con prefijo /sales y sus rutas.
- Decorador `seller_required`: acceso para vendedores y administradores;
  el cliente público jamás entra (sin sesión → login).
- Servicio `sales_service.py`: búsqueda de productos para venta que
  reutiliza el buscador de productos (código, nombre, descripción) y el
  servicio de inventario — solo productos ACTIVOS (inactivos y archivados
  no se venden), con stock exacto (el vendedor sí lo ve, regla ADR),
  venta mínima por categoría con etiqueta legible ("1 caja",
  "3 unidades", "3 ramos") y disponibilidad.
- Layout propio del vendedor (`base_sales.html`): barra superior carbón
  con sección activa en rosa (misma identidad del panel interno),
  usuario/rol/salir, responsive con menú colapsable; enlace "Panel admin"
  visible solo para administradores. Pedidos marcado como 5.2.
- Vista del panel: buscador prominente (texto + categoría), estado
  inicial que invita a buscar, tabla de resultados con miniatura, código,
  presentación comercial, precio, venta mínima, stock y disponibilidad,
  estado "sin resultados" y nota de que el stock es información interna.
- Nuevo `sales.css` (CSS por área); reutiliza los componentes internos
  compartidos de admin.css (badges, tablas, filtros).
- Login del vendedor ahora redirige a su panel (/sales/); navbar pública
  muestra "Panel de ventas" al vendedor con sesión; sidebar admin habilita
  "Ventas".
- Corrección durante desarrollo: pluralización correcta en español de la
  venta mínima (diccionario UNIT_PLURALS en el modelo, etiqueta construida
  en el servicio — no en el template).

---

## Archivos principales

- app/blueprints/sales/routes.py, app/services/sales_service.py (nuevos)
- app/templates/sales/{base_sales,panel}.html (nuevos)
- app/static/css/sales.css (nuevo)
- app/blueprints/sales/__init__.py (prefijo + rutas)
- app/blueprints/auth/decorators.py (seller_required)
- app/blueprints/auth/routes.py (redirect del vendedor a su panel)
- app/models/product.py (UNIT_PLURALS)
- app/templates/partials/navbar.html, app/templates/admin/base_admin.html

---

## Pruebas realizadas

- Público sin sesión → redirigido al login (no accede).
- Login vendedor → redirige a /sales/; badge de rol visible.
- Panel inicial invita a buscar (no vuelca todo el catálogo).
- Búsqueda por código (insensible a mayúsculas), por descripción y
  filtro por categoría, todas contra la base de datos real.
- Solo productos activos: inactivo y archivado desaparecen del buscador
  (verificado a nivel de servicio en ambos estados).
- Stock exacto y venta mínima visibles para el vendedor.
- Admin accede a /sales/ y ve el enlace de regreso a su panel; sidebar
  admin marca Ventas activo.
- Regresión: vendedor sigue sin poder entrar a /admin/; módulo público
  intacto; sales.css servido; log sin errores.

---

## Pull Request

**PR:** #12

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/sales-panel?expand=1

---

## Observaciones

Decisión de diseño menor: el vendedor usa barra superior (no sidebar)
porque tiene pocas secciones y así gana espacio de trabajo en móvil; la
identidad visual (carbón + activo rosa) es la misma del panel interno.

Temas de la Sección 02 (rúbrica UFM): condicionales (roles, estados del
buscador), ciclos for (resultados), listas y diccionarios (resultados del
servicio como lista de diccionarios, UNIT_PLURALS), funciones con
parámetros y return, modularidad (blueprint + servicio que reutiliza
otros dos servicios vía import).

# PR #13 – Sales Orders (Sprint 5.2)

## Información general

**Fase**

5 – Sistema de Ventas

**Sprint**

5.2 – Creación de Pedido

**Branch**

feature/sales-orders

**Estado**

🔍 En revisión

---

## Objetivo

Permitir que el vendedor cree pedidos internos: armar el pedido con
productos existentes, validar mínimos por categoría, calcular totales
automáticamente y confirmarlo como Pendiente de pago — sin tocar
inventario.

---

## Trabajo realizado

- Modelos nuevos `Order` y `OrderItem` (tablas orders/order_items según
  la Arquitectura Técnica): estados borrador → pendiente → pagado /
  cancelado, código legible único (PED-0001), vendedor con trazabilidad,
  datos básicos del cliente, y renglones que apuntan SIEMPRE a productos
  existentes con restricción única por pedido (no duplicar) y precio
  congelado al momento de agregar (un cambio de precio posterior no
  altera pedidos armados). Subtotales y total son propiedades calculadas,
  nunca datos escritos a mano.
- Servicio `orders_service.py`:
  - Un borrador activo por vendedor ("pedido actual"); al confirmarse,
    el siguiente producto abre borrador nuevo.
  - Agregar producto: usa la venta mínima de la categoría como cantidad
    inicial; repetir un producto incrementa su renglón (no se duplica);
    productos no activos rechazados.
  - Incrementar/disminuir con piso en la venta mínima (para menos, se
    quita el renglón completo); quitar producto.
  - Confirmación: exige productos, nombre de cliente, productos aún
    activos y mínimos cumplidos; pasa a Pendiente de pago.
  - REGLA ADR: el servicio no importa siquiera el inventario — un
    borrador o pendiente jamás descuenta stock (el pago llega en 5.3).
- Rutas protegidas en el blueprint sales: pedido actual, agregar desde el
  buscador (regresando a la búsqueda), cambiar cantidad, quitar,
  confirmar, lista "Mis pedidos" y detalle de pedido (el vendedor ve los
  suyos; el admin puede ver todos). Verificación de propiedad: nadie
  manipula renglones de pedidos ajenos o ya confirmados.
- Vistas: pedido actual (tabla de renglones con + / −, resumen, datos del
  cliente y confirmación con aviso de que no descuenta inventario),
  detalle de solo lectura y lista de pedidos con badges de estado.
- Buscador del vendedor: botón "Agregar" por producto (POST con CSRF,
  cantidad = venta mínima) que regresa a la búsqueda actual.
- Navegación de ventas: "Pedido actual" y "Mis pedidos" habilitados.

---

## Archivos principales

- app/models/order.py, app/services/orders_service.py (nuevos)
- app/blueprints/sales/forms.py (nuevo)
- app/templates/sales/{order,order_detail,orders_list}.html (nuevos)
- app/blueprints/sales/routes.py (rutas de pedido)
- app/templates/sales/{base_sales,panel}.html (nav y botón Agregar)
- app/models/__init__.py, app/static/css/sales.css

---

## Pruebas realizadas

- Servicio: borrador único por vendedor; mínimos por categoría al agregar
  (cosmético 1, juguete 3, flores 3) y su piso al disminuir; repetir
  producto incrementa el renglón; quitar; precio congelado verificado
  cambiando el precio del producto; totales automáticos correctos;
  confirmación rechazada sin cliente o con producto inactivado en el
  camino; pedido confirmado inmodificable; nuevo borrador tras confirmar.
- REGLA ADR verificada dos veces (servicio y HTTP): el stock quedó
  idéntico antes y después de armar y confirmar pedidos.
- HTTP con sesión real: agregar desde el buscador regresa a la búsqueda,
  vista de pedido con + / −, mensaje al intentar bajar del mínimo,
  confirmar sin nombre muestra error, confirmación correcta redirige al
  detalle, lista de pedidos, y un vendedor no puede tocar renglones de
  pedidos ajenos (verificación de propiedad).
- Módulo público intacto; log sin errores.
- Quedan dos pedidos pendientes de pago como datos de demostración para
  el Sprint 5.3.

---

## Pull Request

**PR:** #13

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/sales-orders?expand=1

---

## Observaciones

Decisión de diseño: un solo borrador activo por vendedor (su "pedido
actual"), igual que la cotización pública usa una sesión única — simplifica
la operación en mostrador. El precio se congela por renglón al agregarse.

Temas de la Sección 02 (rúbrica UFM): condicionales (validaciones de
mínimos y estados), ciclos for (totales calculados recorriendo renglones,
render de tablas), listas (order.items), diccionarios (etiquetas de
estado), funciones con parámetros y return (todo el servicio), modularidad
(modelo/servicio/formularios/rutas/templates) y librería estándar
(decimal para dinero, datetime).

# PR #14 – Sales Payment (Sprint 5.3)

## Información general

**Fase**

5 – Sistema de Ventas

**Sprint**

5.3 – Pago y Descuento de Inventario

**Branch**

feature/sales-payment

**Estado**

🔍 En revisión

---

## Objetivo

Implementar la confirmación de pago con el descuento correcto de
inventario: una sola vez, validando existencias, con trazabilidad
completa y disponibilidad pública actualizada. El sprint más crítico del
ADR.

---

## Trabajo realizado

- `mark_as_paid()` en orders_service — el ÚNICO punto del sistema donde
  una venta descuenta inventario. Secuencia todo-o-nada:
  1. Estado: solo un pedido Pendiente puede pagarse; pagado se rechaza
     (sin doble descuento); borrador y cancelado se rechazan.
  2. Existencias: se validan TODOS los renglones antes de descontar el
     primero; si un producto no alcanza, no se descuenta nada.
  3. Descuento por renglón vía inventory_service con el nuevo tipo de
     movimiento "venta" (usuario, fecha, motivo "Venta pedido PED-XXXX"
     — trazabilidad completa) y disponibilidad pública recalculada.
  4. Estado Pagado + fecha de pago + quién cobró, confirmado en UNA sola
     transacción (register_movement ganó el parámetro commit=False para
     que el pago de varios renglones sea atómico).
- Nuevo tipo de movimiento "venta": solo lo genera el sistema al pagar;
  el formulario manual de inventario quedó restringido a entrada/salida
  (constante MANUAL_MOVEMENT_TYPES) y el historial lo muestra con su
  propio badge.
- Campos de trazabilidad en Order: paid_at y paid_by (con foreign_keys
  explícitos por la doble relación hacia users).
- Ruta POST /sales/orders/<id>/pay protegida (CSRF): el vendedor cobra
  sus pedidos y el administrador puede cobrar cualquiera (regla de
  negocio: marcar pagado no es exclusivo del admin).
- Detalle del pedido: botón "Registrar pago" con confirmación y monto
  (solo pendientes); pagados muestran fecha, quién cobró y aviso de
  inventario descontado.
- Script `migrate_payment_fields.py` (idempotente) para agregar las
  columnas nuevas a bases locales creadas antes de este sprint
  (create_all no altera tablas existentes).

---

## Archivos principales

- app/services/orders_service.py (mark_as_paid)
- app/services/inventory_service.py (commit=False, tipo venta)
- app/models/order.py (paid_at, paid_by), app/models/inventory.py (venta)
- app/blueprints/sales/routes.py (ruta de pago)
- app/blueprints/admin/forms.py (formulario manual sin "venta")
- app/templates/sales/order_detail.html, app/static/css/admin.css
- migrate_payment_fields.py (nuevo)

---

## Pruebas realizadas

- Borrador y cancelado no se pueden pagar; pendiente sí.
- Pago correcto: stock descontado exactamente una vez, movimiento
  "venta" con usuario/fecha/motivo en el historial, paid_at y paid_by
  registrados, disponibilidad pública recalculada (tulipán pasó a Baja
  disponibilidad al quedar en el umbral).
- Doble pago rechazado con mensaje claro y stock intacto (verificado a
  nivel servicio y por HTTP).
- Todo-o-nada: pedido con un renglón sin stock suficiente → rechazo
  ANTES de descontar nada; los demás renglones quedaron intactos y el
  pedido siguió pendiente.
- El vendedor (rol vendedor) ejecutó los pagos — regla de negocio
  verificada.
- Formulario manual de inventario solo ofrece entrada/salida ("venta"
  no se puede registrar a mano).
- Historial de inventario en el panel admin muestra las ventas con su
  badge y el código del pedido.
- Módulo público intacto; log sin errores.
- Los pedidos PED-0001 y PED-0003 quedaron pendientes en la base local
  para que el usuario pruebe el flujo completo él mismo.

---

## Pull Request

**PR:** #14

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/sales-payment?expand=1

---

## Observaciones

IMPORTANTE para probar localmente: correr una vez
`python migrate_payment_fields.py` antes de `python run.py` (agrega las
columnas de pago a la base existente; es seguro repetirlo).

Temas de la Sección 02 (rúbrica UFM): condicionales (validaciones de
estado y existencias), ciclos for (validación y descuento por renglón),
funciones con parámetros y return, diccionarios (etiquetas de
movimiento), modularidad (orders_service reutiliza inventory_service) y
librería estándar (datetime para la fecha de pago, sqlalchemy.text en la
migración).

# PR #15 – Sales Receipts & History (Sprint 5.4)

## Información general

**Fase**

5 – Sistema de Ventas

**Sprint**

5.4 – Comprobante e Historial de Ventas

**Branch**

feature/sales-receipts

**Estado**

🔍 En revisión

---

## Objetivo

Consultar ventas y generar comprobantes internos: historial de pedidos
con filtros, comprobante imprimible (NO factura fiscal) y cancelación de
pedidos sin romper historial. Cierra la Fase 5 – Sistema de Ventas.

---

## Trabajo realizado

- Historial de pedidos de la tienda para todo el personal con filtros
  simples: estado (los 4 visibles: Borrador / Pendiente de pago /
  Pagado / Cancelado), vendedor, cliente (texto) y rango de fechas
  (desde/hasta inclusivo). Columna de vendedor y acceso a comprobante
  desde la lista.
- Comprobante interno de venta imprimible, SOLO para pedidos pagados:
  página independiente y minimalista (logo, código, cliente, vendedor,
  quién cobró y cuándo, renglones con precios congelados, total) con
  botón de imprimir y CSS @media print. Incluye de forma explícita la
  leyenda "No es factura fiscal y no tiene valor tributario" (sin SAT,
  sin pagos en línea — alcance del ADR respetado).
- Cancelación de pedidos sin romper historial: solo borradores y
  pendientes (un pagado ya descontó inventario y no se cancela), solo el
  vendedor que lo creó o un administrador; el pedido y sus renglones se
  conservan con estado Cancelado y el inventario no se toca. Botones en
  el detalle (pendiente) y en el carrito (borrador), con confirmación.
- Decisión de operación en mostrador: cualquier usuario interno puede
  ver el detalle de un pedido y registrar el pago de un pendiente
  (regla de negocio: marcar pagado no es exclusivo del admin); editar
  un borrador sigue siendo solo de su vendedor, y cancelar solo del
  dueño o admin.
- Dashboard: el indicador de pedidos ahora es real ("Pedidos (7 días)",
  vía count_recent_orders con datetime/timedelta); acceso rápido de
  Ventas habilitado; solo cotizaciones sigue como demo (Fase 6).
- BUG encontrado y corregido durante las pruebas: las fechas se
  guardaban en UTC (datetime.utcnow) pero la tienda opera en Guatemala
  (UTC-6), por lo que el filtro "pedidos de hoy" devolvía vacío y las
  horas mostradas iban 6 horas adelantadas. Decisión registrada: el
  sistema guarda hora local de la tienda (datetime.now) — apropiado
  para un negocio de una sola zona horaria. Se normalizaron además las
  fechas ya guardadas en la base local (-6h, ajuste único).

---

## Archivos principales

- app/templates/sales/receipt.html (nuevo)
- app/templates/sales/orders_list.html (reescrito con filtros)
- app/templates/sales/{order_detail,order}.html (cancelar/comprobante)
- app/templates/sales/base_sales.html ("Pedidos")
- app/blueprints/sales/routes.py (historial, cancelar, comprobante)
- app/services/orders_service.py (list_orders, cancel_order,
  count_recent_orders)
- app/services/dashboard_service.py, app/templates/admin/dashboard.html
- app/models/{order,product,inventory}.py (hora local)
- app/static/css/sales.css (comprobante + impresión)

---

## Pruebas realizadas

- Filtros del historial contra BD real: estado, vendedor, cliente
  (parcial e insensible a mayúsculas), fecha desde/hasta y combinados.
- Comprobante de pagado: contenido completo (cliente, cobrador, fecha de
  pago, renglones, total) y leyenda de no-factura; un pendiente redirige
  con aviso (no tiene comprobante).
- Cancelación: pendiente y borrador cancelan conservando renglones e
  historial, inventario intacto; pagado y ya-cancelado rechazados;
  regla de permisos verificada.
- Dashboard con conteo real de pedidos (7 días).
- Fechas: filtro "hoy" verificado tras la corrección de zona horaria.
- Módulo público intacto; log sin errores.

---

## Pull Request

**PR:** #15

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/sales-receipts?expand=1

---

## Observaciones

Con este sprint la **Fase 5 – Sistema de Ventas queda completada**
(panel/buscador, pedidos, pago con descuento único y comprobante/historial).

Temas de la Sección 02 (rúbrica UFM): condicionales (reglas de
cancelación y permisos), ciclos for (tablas e historial), listas y
diccionarios, funciones con parámetros y return, modularidad, y librería
estándar (datetime/timedelta en filtros de fecha y conteo de recientes —
incluida la corrección de zona horaria).

# PR #16 – Integration: Products → Public Catalog (Sprint 6.1)

## Información general

**Fase**

6 – Integración

**Sprint**

6.1 – Integración Productos Admin → Catálogo Público

**Branch**

feature/integration-products-catalog

**Estado**

🔍 En revisión

---

## Objetivo

Conectar los productos administrados desde el panel con el catálogo
público: el catálogo deja los datos de prueba de la Fase 3 y lee la base
de datos real. Inicia la Fase 6.

---

## Trabajo realizado

- Nuevo `catalog_service.py`: la ÚNICA puerta de los datos reales hacia
  el cliente público. Solo entrega productos ACTIVOS y jamás incluye el
  stock exacto (regla ADR): únicamente el nivel de disponibilidad con su
  etiqueta (Disponible / Baja disponibilidad / Agotado). Entrega la misma
  estructura que los templates públicos ya consumían, por lo que el
  cambio de fuente fue transparente para las vistas.
- Rutas públicas reescritas: catálogo con filtros reales contra BD
  (texto sobre código/nombre/descripción, categoría, subcategoría,
  disponibilidad) y detalle por código (los inactivos/archivados
  devuelven 404 al público). `_get_demo_products()` eliminado — sin
  datos mock en el flujo público.
- Filtros de categorías/subcategorías del catálogo generados desde la
  base real.
- El flujo de cotización pública funciona con los productos reales sin
  cambios (recibe código/nombre/precio desde el detalle, verificado
  end-to-end con la sesión).
- Imagen genérica `placeholder.svg` para productos sin fotografía.
- Fix CSS: la ficha de detalle generaba la clase `availability-baja`
  (nivel real de BD) pero el CSS solo tenía `availability-baja-
  disponibilidad`; se agregó la regla para que el badge ámbar aplique.

---

## Archivos principales

- app/services/catalog_service.py (nuevo)
- app/blueprints/public/routes.py (reescrito — sin datos mock)
- app/static/img/products/placeholder.svg (nuevo)
- app/static/css/styles.css (fix badge baja disponibilidad)

---

## Pruebas realizadas

- Catálogo muestra los productos reales con los 3 niveles de
  disponibilidad reflejando el inventario (baja / disponible / agotado).
- El HTML público no contiene la palabra "stock" ni clases internas —
  el cliente no ve existencias exactas.
- Filtros contra BD: texto, categoría, subcategoría dependiente y
  disponibilidad, incluidas combinaciones.
- Detalle real: precio, marca, descripción y badge con el CSS corregido;
  "Agregar a cotización" desde la ficha real funciona (item en sesión).
- Admin inactiva → desaparece del catálogo y su detalle da 404; archiva
  → igual; reactiva → vuelve a aparecer.
- Cadena completa de la DoD: admin crea producto (ROSA-01) → aparece de
  inmediato en el catálogo público como Agotado (nace sin stock) con la
  imagen genérica → primera entrada de inventario → el catálogo lo
  muestra Disponible sin exponer la cantidad.
- Home, login y paneles internos intactos; log sin errores.

---

## Pull Request

**PR:** #16

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/integration-products-catalog?expand=1

---

## Observaciones

El flujo público completo (Home → Catálogo → Detalle → Cotización) opera
ahora sobre la fuente única de productos. La conversión de cotización a
pedido llega en el Sprint 6.2.

Temas de la Sección 02 (rúbrica UFM): funciones con parámetros y return,
diccionarios (vista pública del producto), listas y ciclos (catálogo y
filtros), condicionales (visibilidad por estado), modularidad (servicio
de catálogo que compone productos e inventario indirectamente vía
disponibilidad).

# PR #17 – Integration: Quote → Order (Sprint 6.2)

## Información general

**Fase**

6 – Integración

**Sprint**

6.2 – Integración Cotización → Pedido

**Branch**

feature/integration-quote-to-order

**Estado**

🔍 En revisión

---

## Objetivo

Que las cotizaciones del sitio público lleguen a los vendedores y puedan
convertirse en pedidos internos Pendientes de pago, manteniendo
cantidades, precios y las reglas de venta mínima.

---

## Trabajo realizado

- Modelos nuevos `Quote`/`QuoteItem` (previstos en la Arquitectura
  Técnica): la cotización que el cliente arma en su sesión ahora SE
  PERSISTE al enviarla, con código legible (COT-0001), datos del
  cliente, renglones enlazados a productos existentes (fuente única) y
  el precio congelado que el cliente vio. Estados: Pendiente /
  Convertida en pedido, con referencia al pedido generado
  (trazabilidad bidireccional).
- Servicio `quotes_service.py`: persistencia desde la sesión (los
  renglones cuyo producto ya no existe se omiten), listado por estado,
  conteo de pendientes para el dashboard y la conversión a pedido.
- Conversión Cotización → Pedido: nace directamente Pendiente de pago a
  nombre del vendedor que la atiende, reutiliza los productos
  existentes (sin duplicar), mantiene los precios cotizados, y valida
  la venta mínima por categoría: las cantidades por debajo del mínimo
  se AJUSTAN HACIA ARRIBA con un mensaje que detalla cada ajuste
  (decisión: el cliente público puede cotizar menos, pero no se vende
  menos). Si algún producto ya no está activo, la conversión completa
  se rechaza. NO descuenta inventario (regla ADR).
- Bandeja de cotizaciones en el panel de ventas: listado con filtro por
  estado y detalle con datos del cliente, mínimos por renglón (avisando
  qué se ajustará) y botón de conversión con confirmación.
- Sitio público: el enlace "Agregar a cotización" del detalle ahora
  arranca con la VENTA MÍNIMA de la categoría (antes cotizaba 1), y al
  enviar la cotización el cliente recibe confirmación con su código de
  seguimiento (el template no mostraba el mensaje de éxito — corregido).
- Dashboard: el KPI de cotizaciones pendientes es REAL — con esto TODOS
  los indicadores son reales y el aviso de datos de demostración
  desapareció. Acceso rápido de Cotizaciones habilitado.

---

## Archivos principales

- app/models/quote.py, app/services/quotes_service.py (nuevos)
- app/templates/sales/{quotes_list,quote_detail}.html (nuevos)
- app/blueprints/quotes/routes.py (persistencia al enviar)
- app/blueprints/sales/routes.py (bandeja + conversión)
- app/templates/public/product_detail.html (cotiza con venta mínima)
- app/templates/quotes/index.html (mensaje de confirmación)
- app/templates/sales/base_sales.html, app/templates/admin/dashboard.html
- app/services/dashboard_service.py, app/models/__init__.py
- app/static/css/sales.css

---

## Pruebas realizadas

- Servicio: persistencia desde sesión con producto inexistente omitido,
  código COT generado, total correcto; conversión con ajuste de mínimos
  (1 → 3 informado), precios cotizados mantenidos, pedido Pendiente,
  cliente heredado; trazabilidad quote↔order; re-conversión rechazada;
  producto inactivo bloquea la conversión; inventario intacto.
- HTTP end-to-end: el detalle público cotiza con quantity=venta mínima;
  cliente arma cotización (incluido tulipán x1 forzado) y la envía con
  confirmación y código; el vendedor la ve en su bandeja, el detalle
  avisa "se ajustará a 3", convierte y aterriza en el pedido Pendiente
  de pago a nombre de Ana Pérez; la cotización queda Convertida con
  enlace al pedido; inventario sin cambios; dashboard sin aviso de demo
  y con todos los KPIs reales; módulo público intacto; log limpio.
- COT-0002 (convertida) y el pedido PED-0009 (pendiente) quedan como
  datos de demostración del flujo completo.

---

## Pull Request

**PR:** #17

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/integration-quote-to-order?expand=1

---

## Observaciones

Decisión registrada: al convertir, las cantidades bajo el mínimo de
categoría se ajustan hacia arriba (con aviso detallado) en lugar de
rechazar la conversión — el pedido nace Pendiente (no editable) y el
vendedor no podría corregirlo después.

Temas de la Sección 02 (rúbrica UFM): condicionales (validaciones de
conversión), ciclos for (persistencia y conversión por renglón), listas
y diccionarios (estado de sesión → modelos), funciones con parámetros y
return, modularidad (quotes_service compone products/orders) y librería
estándar (datetime, decimal).

# PR #18 – Integration: Sales → Inventory → Public Availability (Sprint 6.3)

## Información general

**Fase**

6 – Integración

**Sprint**

6.3 – Integración Ventas → Inventario → Disponibilidad Pública

**Branch**

feature/integration-sales-inventory

**Estado**

🔍 En revisión

---

## Objetivo

Verificar y completar el flujo de inventario después de una venta
pagada: descuento único, historial, disponibilidad pública recalculada y
reflejada en el catálogo, sin descuentos por cotizaciones ni pendientes.

---

## Trabajo realizado

- Script de consola `verify_integration.py`: verificación REPETIBLE del
  ciclo completo con 9 reglas del ADR. Crea sus propios datos de prueba
  (producto, pedidos, cotización), valida cada regla y limpia todo al
  terminar — la base queda intacta y puede correrse cuantas veces se
  quiera (útil también para la Fase 7 y antes del deploy):
  1. Producto nuevo nace Agotado. 2. Entrada → Disponible.
  3. Pedido pendiente no descuenta. 4. Pagar descuenta una vez con
  movimiento "venta". 5. Disponibilidad recalculada al pagar.
  6. Doble pago rechazado. 7. Pago sin stock rechazado sin descontar
  nada. 8. Cotización y su conversión no descuentan. 9. Limpieza.
- BRECHA detectada y corregida: al editar un producto y cambiarlo de
  subcategoría, el umbral de bajo stock cambia pero la disponibilidad
  pública no se recalculaba (badge desactualizado hasta el siguiente
  movimiento). products_service.update_product ahora reasigna la
  relación de subcategoría y recalcula la disponibilidad de inmediato.
  (El primer intento del fix falló en la prueba —asignar solo el id no
  actualiza la relación en memoria— y se corrigió asignando la
  relación; ambas variantes quedaron probadas.)
- Verificación EN VIVO con los datos reales del sistema:
  - El catálogo público mostraba el tulipán Agotado.
  - Pagar el PED-0009 (convertido de la cotización de Ana Pérez en el
    6.2, con tulipanes sin stock) fue RECHAZADO con el mensaje "Stock
    insuficiente para MES2655-2: hay 0... No se descontó nada" y el
    pedido siguió Pendiente.
  - El admin registró una entrada de 12 tulipanes → el catálogo público
    pasó a Disponible de inmediato.
  - El segundo intento de pago descontó ambos renglones (juguete 12→9,
    tulipán 12→9), dejó los 2 movimientos "venta" en el historial y el
    catálogo reflejó el estado final sin exponer cantidades.

---

## Archivos principales

- verify_integration.py (nuevo)
- app/services/products_service.py (fix disponibilidad al cambiar
  subcategoría)

---

## Pruebas realizadas

- verify_integration.py: 9/9 verificaciones correctas (dos corridas,
  demostrando que es repetible y que limpia la base).
- Flujo en vivo por HTTP con la sesión del vendedor y del admin (pago
  rechazado por stock → reabastecimiento → pago exitoso → catálogo
  actualizado), descrito arriba.
- Fix de subcategoría probado en ambos sentidos (umbral mayor → baja;
  regreso → disponible).
- Historial con los movimientos de la venta verificado a nivel de datos.
- Log sin errores.

---

## Pull Request

**PR:** #18

**Enlace**

https://github.com/josefranco-sketch/SistemaInventario-Web/compare/dev...feature/integration-sales-inventory?expand=1

---

## Observaciones

Este sprint confirma que las reglas más importantes del ADR funcionan
integradas de punta a punta con datos reales. verify_integration.py
queda como herramienta de regresión para la Fase 7 y el deploy.

Temas de la Sección 02 (rúbrica UFM): el script de verificación usa
funciones propias con parámetros y return (check, build_order, cleanup),
listas de tuplas para acumular resultados, ciclos for para el resumen,
condicionales para cada regla, entrada/salida por consola con print y
modularidad (importa y compone 4 servicios del sistema).
