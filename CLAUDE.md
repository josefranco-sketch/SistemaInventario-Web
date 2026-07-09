# CLAUDE.md — Sistema Integral de Gestión Comercial (Los Altos)

Contexto persistente del proyecto para retomar el trabajo entre sesiones de Claude Code. Léelo completo antes de tocar código.

## Qué es esto

Sistema web para **Los Altos — Cosméticos, Accesorios y Más**, importadora mayorista en Guatemala (productos desde China: cosméticos, juguetes, flores). No es e-commerce con pago automático. Flujo real del negocio:

```
Consulta pública → Cotización → Pedido → Pago en tienda → Descuento de inventario
```

**3 módulos:** Público (catálogo + cotizaciones) · Administrativo (productos, inventario, ventas, usuarios) · Vendedores (buscar productos, armar pedidos, marcar pago, comprobantes).

**Fuera de alcance (fijo):** inventario de bodega, facturación fiscal/SAT, pagos en línea, manejo de proveedores, control de importaciones, impuestos.

## Estado actual del repo — IMPORTANTE

- Rama de trabajo real: **`dev`** (no `main`). `main` está congelado en un commit viejo ("Agrego archivo de prueba") y **no** refleja el avance — no te dejes engañar si haces `git checkout main`.
- Trabaja siempre desde `dev`, ramificando `feature/*` desde ahí.
- **Avance: Fases 1–7 completadas**. Siguiente paso: **Fase 8 — Deploy y Entrega** (README final → deploy en Vercel → presentación).
- Los 6 documentos fuente (PDF) están en la raíz del repo. Son la fuente de verdad; este CLAUDE.md es un resumen operativo, no un reemplazo.

## Reglas de negocio que NO se rompen

Estas son decisiones ADR aprobadas (Documento 6). No se cambian sin registrar la decisión explícitamente primero.

1. **Producto único**: un solo registro de producto alimenta catálogo, inventario, cotizaciones y ventas. Nunca duplicar.
2. **Inventario solo baja al confirmar pago.** Una cotización o un pedido pendiente NUNCA descuenta stock. Descuento ocurre una sola vez (evitar doble descuento).
3. **Nunca eliminar productos físicamente.** Solo estados: Activo / Inactivo / Archivado.
4. **Stock exacto nunca visible al cliente público.** Solo badges: Disponible / Baja disponibilidad / Agotado. El admin/vendedor sí ve stock exacto.
5. **Vendedores pueden marcar pedidos como pagados** (no es exclusivo del admin).
6. **Bajo stock configurable por subcategoría** (umbral no es global).
7. **Sin manejo de impuestos** en ningún cálculo.
8. Cada ajuste manual de inventario debe dejar historial (usuario, fecha, motivo) — obligatorio, sin excepción.

### Reglas de venta mínima por categoría (números exactos)

- **Cosméticos**: se venden por caja o display (ej. display de 24 unidades). No hay venta suelta/unidad individual.
- **Juguetes**: mínimo según precio del producto:
  - Precio > Q20 → mínimo **3 unidades** por modelo.
  - Precio < Q20 → mínimo **6 unidades** por modelo.
  - Precio < Q15 → mínimo **media docena** por modelo.
- **Flores**: venta por ramos; cada código = un color/estilo específico. Mínimo **3 ramos por código**.

### Estados del sistema

- **Producto:** Activo / Inactivo / Archivado.
- **Disponibilidad pública:** Disponible / Baja disponibilidad / Agotado.
- **Pedido:** Borrador / Pendiente de pago / Pagado / Cancelado.

## Arquitectura técnica

**Stack (fijo, no cambia sin ADR nuevo):** Python, Flask, Jinja2, Bootstrap 5, CSS propio, SQLite, SQLAlchemy, Flask-Login, Flask-WTF, Git/GitHub, deploy planeado en Vercel.

**Patrón:** Flask con render server-side, **Application Factory** (`create_app()`), **Blueprints** por módulo funcional: `public`, `admin`, `auth`, `quotes`, `sales`.

**Separación de capas (regla dura):** Routes (HTTP, sin lógica) → Services (reglas de negocio, cálculos, validaciones) → Models (SQLAlchemy) → Templates (solo presentación, Jinja2). **Nunca poner lógica de negocio ni cálculos de inventario en templates.**

**Estructura de carpetas real (verificada en `dev`):**
```
run.py                     # entry point (app.run(debug=True))
config.py                  # Config central (SECRET_KEY, SQLALCHEMY_DATABASE_URI=sqlite:///app.db)
requirements.txt
app/
  __init__.py               # create_app(), registra los 5 blueprints
  extensions.py              # db (SQLAlchemy), login_manager (Flask-Login) — instancias únicas
  blueprints/
    public/   (routes.py implementado: home, catalog, product_detail)
    quotes/   (routes.py implementado: quote_home con GET/POST, sesión)
    admin/    (solo __init__.py, blueprint vacío — Fase 4)
    auth/     (solo __init__.py, blueprint vacío — Fase 4)
    sales/    (solo __init__.py, blueprint vacío — Fase 5)
  templates/
    base.html, partials/navbar.html, partials/footer.html
    public/home.html, public/catalog.html, public/product_detail.html
    quotes/index.html
  static/
    css/styles.css
    img/logo-los-altos.svg, img/products/*.png
```

Nota: la arquitectura técnica original (Documento 2) proponía carpetas separadas `app/models/` y `app/services/` — **aún no existen**, porque no hay base de datos real todavía (todo Fase 3 usa datos de prueba hardcodeados en `routes.py` vía `_get_demo_products()`). Se crearán en Fase 4 cuando entre el módulo de Productos con SQLAlchemy real.

**Convenciones de código:** archivos Python en `lower_snake_case`; clases de modelos en `PascalCase` (Product, InventoryMovement, Order); CSS por área (public.css, admin.css, sales.css — hoy todo vive en un solo `styles.css`, se espera separar); tablas de BD en plural (products, orders, order_items).

**Modelo de datos previsto (Documento 2, aún no implementado):**
- `Product`: código único, categoría, subcategoría, estado, presentación comercial, precio.
- `Category` / `Subcategory`: color de identidad, umbral de bajo stock configurable.
- `Inventory`: existencia interna en tienda (stock exacto, oculto al público).
- `InventoryMovement`: historial de entradas/salidas/ajustes (usuario, fecha, motivo obligatorios).
- `Quote` / `QuoteItem`: cotización — no maneja pagos, no descuenta inventario.
- `Order` / `OrderItem`: pedido/venta — descuenta inventario solo al pasar a Pagado.
- `User`: admin o vendedor, permisos diferenciados.

## Git Flow (obligatorio, sin excepciones)

```
dev  →  feature/<nombre-en-inglés>  →  commit  →  push  →  Pull Request  →  review  →  merge a dev
```

- **Nunca** merge directo `feature/* → main`. `main` se actualiza aparte (deploy/entrega), no como parte del flujo diario.
- Nombres de rama: minúsculas, con guiones, en inglés, sin nombre de persona ni sufijos "-final"/"-v2" (ej. `feature/admin-login`, `feature/admin-products`).
- Commits en inglés, imperativo, específicos ("Add sales payment confirmation"), nunca genéricos ("changes", "fix", "update").
- Cada Sprint = una branch feature = un PR = una actualización de `PR_tracker.md`.
- El archivo `PR_tracker.md` en la raíz del repo es la bitácora oficial de PRs — actualízalo al cerrar cada sprint, siguiendo el formato ya usado ahí (Información general, Objetivo, Trabajo realizado, Archivos principales, Pull Request, Observaciones).

### Modo de trabajo real (override explícito del usuario)

El usuario trabaja **solo** en este proyecto (no en pareja, a pesar de que la rúbrica académica de la sección de abajo describe un formato de pareja). Reglas operativas que prevalecen sobre cualquier lectura literal de la rúbrica:

- **Nada se mergea a `main` hasta que el proyecto completo esté terminado.** Todo el desarrollo, sprint por sprint, vive y se integra en `dev`.
- Por cada sprint: crear una branch `feature/<nombre>` desde `dev`, desarrollar, y al terminar **generar el Pull Request** (`feature/* → dev`) con su documentación correspondiente (según el formato de `PR_tracker.md` y los puntos de la rúbrica que apliquen).
- **Yo (Claude) genero los PRs, pero el usuario es quien los revisa y mergea manualmente.** No hacer merge de un PR sin que el usuario lo pida explícitamente.
- Cuando corresponda documentar un PR, incluir explícitamente qué temas de la Sección 02 de la rúbrica (variables, condicionales, ciclos, listas, diccionarios, funciones, modularidad, librería estándar) se tocaron en ese sprint, para tener trazabilidad de cara a la evaluación.

## Design System — paleta oficial (canónica, usar estos hex)

Vive en `:root` de `app/static/css/styles.css`. El resto de estilos debe consumir estas variables, **nunca hardcodear hex**.

```css
:root {
  /* Brand */
  --la-brand: #F57EA7;
  --la-brand-hover: #D94F82;
  --la-brand-active: #C73A70;
  --la-brand-soft: #FDE8F1;
  --la-brand-border: #F7BBD2;

  /* Neutral base */
  --la-bg: #F8F9FB;
  --la-surface: #FFFFFF;
  --la-surface-alt: #F3F4F6;
  --la-border: #E6E8EC;
  --la-text: #1F1F1F;
  --la-text-muted: #6C757D;
  --la-carbon: #111111;

  /* Categories */
  --la-category-cosmetics: #F57EA7;   --la-category-cosmetics-soft: #FDE8F1;
  --la-category-toys: #3D8DDF;        --la-category-toys-soft: #E8F3FF;
  --la-category-flowers: #4CAF6F;     --la-category-flowers-soft: #E9F8EF;

  /* States */
  --la-success: #28A745;  --la-success-soft: #E8F6EC;
  --la-warning: #FFC107;  --la-warning-soft: #FFF4D6;
  --la-danger: #DC3545;   --la-danger-soft: #FDECEE;
  --la-info: #17A2B8;     --la-info-soft: #E6F7FA;
  --la-disabled: #CED4DA; --la-disabled-soft: #F3F4F6;

  --la-primary: var(--la-brand);
  --la-primary-hover: var(--la-brand-hover);
  --la-link: var(--la-brand-hover);
  --la-focus-ring: #F57EA73D;
  --la-sidebar-bg: var(--la-carbon);
  --la-sidebar-active: var(--la-brand);
}
```

- **Tipografía:** Inter (única fuente). H1 32-36px/700, H2 24-28px/700, H3 20-22px/600, texto 16px/400, tablas 14-15px, botones 14-15px/600.
- **Iconos:** Bootstrap Icons (única librería).
- **Espaciado:** múltiplos de 8px (xs=4, sm=8, md=16, lg=24, xl=32, 2xl=48, 3xl=64). Radios: botones 10-12px, cards 16px, inputs 10px, modales 18px.
- **Grid:** Bootstrap 12 col. Público desktop máx 1180-1200px. Admin: sidebar fija 256px (72px colapsada) + contenido fluido, fondo sidebar `--la-carbon`, activo en rosa.
- Rosa (`--la-brand`) es acento de marca, **no dominante** — máximo una acción primaria rosa por zona de pantalla.
- Badges de estado: siempre texto + color (nunca color solo).
- Tablas solo en pantallas internas (admin/ventas); el catálogo público usa cards.
- Login: tarjeta centrada, ancho máx 420px.
- Accesibilidad: contraste AA, focus visible, objetivos táctiles mín 40-44px.

## Cómo debo trabajar en este proyecto (reglas de colaboración)

Adaptado del Documento 5 (escrito originalmente para chats de ChatGPT por módulo; el espíritu aplica igual en Claude Code):

- Un sprint = un objetivo claro = una branch `feature/*` = un PR = una actualización de `PR_tracker.md`. No mezclar módulos en un mismo cambio.
- No cambiar reglas de negocio, arquitectura, stack o Git Flow sin que quede explícito y justificado (equivalente a un nuevo ADR). Si una instrucción del usuario contradice una regla de negocio fija (sección de arriba), **detente y pregunta** antes de escribir código.
- Lógica de negocio y cálculos van en services/models, nunca en templates.
- Para trabajo grande, plantear primero un plan breve antes de escribir código extenso; entregar en pasos pequeños verificables.
- Al cerrar una sesión/sprint: resumir qué se construyó, qué archivos cambiaron, qué reglas de negocio se respetaron, qué se probó y cuál es el siguiente paso sugerido (esto es lo que permite continuidad real entre sesiones).

**Errores a evitar explícitamente:**
- Descontar inventario antes de que el pago esté confirmado.
- Mostrar stock exacto al cliente público.
- Eliminar productos físicamente.
- Poner cálculos críticos en templates.
- Merge de `feature/*` directo a `main`.
- Abrir PR sin haber probado localmente.
- Ignorar la paleta/Design System de arriba.

## Historial de desarrollo

### ✅ Fase 1 — Análisis y Diseño (completada)
Se generaron los 6 documentos base del proyecto (los PDF en la raíz de este repo). Decisiones principales: arquitectura modular Flask, producto como fuente única, inventario descuenta solo al pagar, no eliminar productos, Design System unificado, Bootstrap + CSS, Flask + Jinja2, SQLite.

### ✅ Fase 2 — Configuración del Proyecto (completada)
**Sprint 2.1** — `feature/configuracion-flask` — PR #1. Construido: entorno virtual, `requirements.txt`, `config.py`, `create_app()`, SQLAlchemy, Flask-Login, blueprints, estructura de templates/static/instance. Resultado: base Flask funcionando.

### ✅ Fase 3 — Módulo Público (completada)
- **Sprint 3.1 — Navbar y Footer** — `feature/navbar-footer` — PR #2. `base.html`, navbar/footer reutilizables, logo oficial, responsive.
- **Sprint 3.2 — Home** — `feature/home` — PR #3. Hero, CTA, categorías (cosméticos/juguetes/flores), sección de confianza.
- **Sprint 3.3 — Catálogo** — `feature/catalog` — PR #4. Productos de prueba con imágenes reales, buscador, filtros por categoría/subcategoría/disponibilidad, cards.
- **Sprint 3.4 — Detalle de Producto** — `feature/product-detail` — PR #5. Ruta pública por código, integración catálogo→detalle, regreso conservando filtros.
- **Sprint 3.5 — Cotización** — `feature/quote` — PR #6. Blueprint `quotes`, cotización pública vía Flask Session, agregar/incrementar/disminuir/eliminar productos, vaciar cotización, cálculo automático, datos de cliente, validaciones HTML.

Flujo público terminado: `Home → Catálogo → Detalle → Cotización`, todo con datos de prueba hardcodeados (sin BD real todavía), sin mostrar stock exacto, sin descontar inventario.

### ✅ Fase 4 — Panel Administrativo (completada)
- Sprint 4.1 — Login Administrativo (`feature/admin-login`): Flask-Login real, login/logout, protección de rutas, roles, sesiones. (Ya existe el blueprint `auth` vacío y `login_manager` inicializado con `user_loader` que hoy retorna `None` — hay que implementarlo.)
- Sprint 4.2 — Dashboard Administrativo (`feature/admin-dashboard`): KPIs, accesos rápidos, resumen general.
- Sprint 4.3 — Gestión de Productos (`feature/admin-products`): CRUD productos, categorías, subcategorías, estados, imágenes, presentación comercial. **Aquí nace el modelo `Product` real en BD** — reemplaza `_get_demo_products()` de `public/routes.py`.
- Sprint 4.4 — Inventario (`feature/admin-inventory`): existencias, movimientos, bajo stock, historial.
- Sprint 4.5 — Usuarios (`feature/admin-users`): CRUD usuarios, roles, activación/desactivación.

### ✅ Fase 5 — Sistema de Ventas (completada)
Pedidos, pago, comprobantes, conversión Cotización → Pedido, descuento de inventario al pagar. Sprints previstos: 5.1 buscador vendedor, 5.2 nuevo pedido, 5.3 pago, 5.4 comprobante.

### ✅ Fase 6 — Integración (completada)
Conectar completamente Productos → Catálogo → Inventario → Cotizaciones → Ventas → Usuarios. Flujo esperado: Administrador → Productos → Catálogo → Cotización → Pedido → Pago → Inventario → Disponibilidad Pública.

### ✅ Fase 7 — Pruebas y Optimización (completada en una pasada: PR #20)
Validación funcional, responsive, UX, corrección de errores, casos borde.

### ⏳ Fase 8 — Deploy y Entrega (pendiente)
Deploy (Vercel), README final, documentación, presentación, entrega.

## Pull Requests completados

| Sprint | PR | Branch |
|--------|-----|--------|
| 2.1 | PR #1 | feature/configuracion-flask |
| 3.1 | PR #2 | feature/navbar-footer |
| 3.2 | PR #3 | feature/home |
| 3.3 | PR #4 | feature/catalog |
| 3.4 | PR #5 | feature/product-detail |
| 3.5 | PR #6 | feature/quote |
| 4.1 | PR #7 | feature/admin-login |
| 4.2 | PR #8 | feature/admin-dashboard |
| 4.3 | PR #9 | feature/admin-products |
| 4.4 | PR #10 | feature/admin-inventory |
| 4.5 | PR #11 | feature/admin-users |
| 5.1 | PR #12 | feature/sales-panel |
| 5.2 | PR #13 | feature/sales-orders |
| 5.3 | PR #14 | feature/sales-payment |
| 5.4 | PR #15 | feature/sales-receipts |
| 6.1 | PR #16 | feature/integration-products-catalog |
| 6.2 | PR #17 | feature/integration-quote-to-order |
| 6.3 | PR #18 | feature/integration-sales-inventory |
| 6.4 | PR #19 | feature/integration-end-to-end |
| 7.1–7.3 | PR #20 | feature/final-quality-pass |

## Rúbrica académica — UFM Fundamentos de Programación (Proyecto Final)

Este proyecto (Sistema Los Altos) es el **Proyecto Final del curso Fundamentos de Programación, UFM**. Fuente: `/Users/josefranco/Documents/U segundo verano/Progra 1/ProyectoFinalFundamentosProgramacion.pdf`. Vale **35 pts**.

> Nota de reconciliación: el enunciado original describe un proyecto "tema libre, en parejas" con merges directos a `main` — no coincide literalmente con nuestro proyecto Flask (que el usuario trabaja solo y con flujo `dev`-first, ver sección de arriba). El usuario decidió explícitamente mantener su flujo real (solo, todo por `dev`, sin tocar `main` hasta el final) y usar esta rúbrica solo como **checklist de contenido y de forma de evaluación**, no como instrucción literal de Git a seguir.

### Fechas clave

| Hito | Fecha |
|---|---|
| Explicación del proyecto | Martes 24 de junio |
| Días de dudas | Lunes 6 y martes 7 de julio |
| **Entrega en GitHub** (código, README y deploy) | **Miércoles 8 de julio, 12:00 pm** |
| Presentaciones | Jueves 9 y viernes 10 de julio |
| Tiempo por pareja | 15 min + preguntas |
| Valor | 35 pts |

### Checklist de contenido obligatorio (Sección 02 — lo que más pesa, 30%)

Todo esto tiene que aparecer **bien usado** en el proyecto (no forzado):

- [ ] **Variables y tipos de datos**: texto, números y booleanos, nombres de variable claros.
- [ ] **Entrada y salida**: `input()` para pedir datos, `print()` para mostrar resultados (aplica sobre todo a las partes de consola/scripts, no a las rutas Flask que responden HTTP).
- [ ] **Condicionales**: al menos una decisión real con `if`/`elif`/`else`, idealmente validando lo que escribe el usuario.
- [ ] **Ciclos `for` y `while`**: usar ambos al menos una vez — `for` para recorrer datos, `while` para repetir hasta que pase algo.
- [ ] **Listas**: guardar una colección y recorrerla (agregar elementos, sacar suma/promedio/máximo).
- [ ] **Diccionarios**: al menos uno para organizar información por clave/valor.
- [ ] **Funciones**: mínimo 3 funciones propias, con parámetros y `return` — nada de lógica suelta en un bloque.
- [ ] **Modularidad**: lógica separada en al menos 2 archivos conectados con `import`/`from`, y bloque `if __name__ == "__main__":`.
- [ ] **Librería estándar**: usar al menos una que aporte algo real (`math`, `random` o `datetime`).

### Ramas y Pull Requests (20% de la nota)

- La rama `main` solo guarda versiones que sirven; todo lo nuevo se trabaja en su propia rama que sale de `dev` (ej. `feature/registro`, `feature/reportes`).
- Mensajes de commit claros, **en inglés** — nunca genéricos ("changes", "asdf").
- **Cada PR debe quedar revisado y comentado** antes de mergear — aunque el cambio esté bien, dejar comentario (qué pareció, qué se haría distinto, alguna duda). En este proyecto (trabajo solo) esto lo hace el usuario al revisar los PRs que yo genero.
- Nunca push directo a `main` (prohibido por la rúbrica también).

### Deploy en Vercel (10%)

- El proyecto debe quedar publicado y funcionando en Vercel, con el link puesto en el README.
- Publicarlo suma pero **no es lo más importante** — primero dejar sólida la lógica de la Sección 02.

### Uso de IA e investigación

- Usar IA/investigación está permitido y suma, pero **lo del curso pesa más** que cualquier librería o API adicional.
- Regla dura: **si algo lo escribió la IA y el usuario no lo puede explicar, no debe quedar en el proyecto.** El día de la presentación puede preguntarse cualquier parte del código. Como asistente, priorizar código que el usuario realmente entienda y pueda defender en vivo, evitando abstracciones innecesarias.

### Entregables finales

- Repositorio GitHub con ramas, commits y PRs con comentarios visibles.
- Código en al menos 2 archivos, ordenado y comentado, entendible sin explicación adicional.
- Proyecto publicado en Vercel, link en el README.
- README explicando en palabras propias qué hace el programa, cómo correrlo, el link del deploy y qué se investigó por fuera del curso.
- Presentación de máximo 6 slides + demo en vivo del proyecto publicado.

### Cómo se califica

| Criterio | Peso |
|---|---|
| Uso correcto de lo visto en el curso (Sección 02) | 30% |
| Pull requests revisados y comentados | 20% |
| Dominio del proyecto explicado en vivo | 20% |
| Código ordenado, en varios archivos, bien comentado | 15% |
| Proyecto publicado y funcionando en Vercel | 10% |
| Presentación y manejo del tiempo (máx. 6 slides) | 5% |

## Próximo paso concreto

Iniciar **Fase 8 — Deploy y Entrega**: Sprint 8.1 (README final, branch `feature/final-documentation`), Sprint 8.2 (deploy en Vercel, `feature/vercel-deploy` — ojo: filesystem de solo lectura, definir estrategia de datos/imágenes para la demo), Sprint 8.3 (presentación y cierre, `feature/final-delivery`; el guion de demo de 13 pasos está en la entrada del PR #19 del PR_tracker.md). Notas operativas: la BD vive en `instance/app.db` (gitignored); usuarios demo: admin/admin123 y vendedor/venta123; scripts útiles: `seed_admin.py`, `seed_catalog.py`, `migrate_payment_fields.py`, `verify_integration.py` (regresión 9/9). El sistema completo funciona end-to-end con datos reales; ya no existe `_get_demo_products()`.
