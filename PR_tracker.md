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
