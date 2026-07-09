# Guía de Entrega y Presentación — Sistema Los Altos

Documento de cierre del proyecto (Sprint 8.3). Todo lo necesario para la
entrega y la presentación en un solo lugar.

---

## 1. Datos clave (memorizar)

| Qué | Valor |
|---|---|
| Deploy | https://sistema-inventario-web-josefranco-sketchs-projects.vercel.app |
| Repositorio | https://github.com/josefranco-sketch/SistemaInventario-Web |
| Admin (demo y local) | `admin` / `admin123` |
| Vendedor (demo) | `vendedor` / `venta123` |
| Correr local | `source .venv/bin/activate && python run.py` |
| Verificación automática | `python verify_integration.py` (9 reglas, deja la base intacta) |

---

## 2. Estado final del proyecto

Las 8 fases del Roadmap están completadas:

| Fase | Contenido | Estado |
|---|---|---|
| 1 | Análisis y diseño (6 documentos) | ✅ |
| 2 | Configuración Flask (factory, blueprints) | ✅ PR #1 |
| 3 | Módulo público (home, catálogo, detalle, cotización) | ✅ PRs #2–#6 |
| 4 | Panel admin (login, dashboard, productos, inventario, usuarios) | ✅ PRs #7–#11 |
| 5 | Ventas (panel, pedidos, pago, comprobantes) | ✅ PRs #12–#15 |
| 6 | Integración end-to-end | ✅ PRs #16–#19 |
| 7 | Pruebas, UX y limpieza | ✅ PRs #20–#21 |
| 8 | README, deploy en Vercel y cierre | ✅ PRs #22–#36 |

Módulos entregados: sitio público con catálogo y cotizaciones ·
panel administrativo (productos, inventario con historial, usuarios,
dashboard con KPIs reales) · sistema de ventas (pedidos, pagos,
comprobantes, bandeja de cotizaciones) · deploy de demostración.

---

## 3. Validación final de las reglas de negocio

Ejecutada con `verify_integration.py` (9/9 correctas) y verificada a mano
en producción:

- ✅ **Producto único**: un solo registro alimenta catálogo, inventario,
  cotizaciones y ventas (no hay duplicación en ningún flujo).
- ✅ **El inventario solo baja al pagar**, exactamente una vez
  (`mark_as_paid` es el único punto de descuento; doble pago rechazado).
- ✅ **Las cotizaciones no descuentan** (ni al crearse ni al convertirse).
- ✅ **El cliente nunca ve stock exacto** (solo badges; verificado en el
  HTML de producción).
- ✅ **Los productos no se eliminan** (solo Activo/Inactivo/Archivado).
- ✅ **Rutas protegidas por roles** (admin, vendedor; el público no entra).

---

## 4. Guion de la demo en vivo (~5 minutos)

Contar la historia completa con un producto nuevo, en el deploy:

1. **Público** (sin sesión): mostrar Home → Catálogo → detalle de un
   producto → señalar el badge de disponibilidad y que NO se ve stock.
2. **Cotizar como cliente**: "Agregar a cotización" (mostrar que arranca
   en la venta mínima de la categoría) → enviar con nombre y teléfono →
   mostrar el número COT que recibe el cliente.
3. **Login admin** (`admin/admin123`): dashboard con KPIs → crear un
   producto nuevo (mostrar que nace "Agotado") → Inventario → registrar
   entrada (motivo obligatorio) → recargar el catálogo público: ya
   aparece "Disponible".
4. **Login vendedor** (`vendedor/venta123`): bandeja de Cotizaciones →
   convertir la cotización del paso 2 en pedido → mostrar que quedó
   "Pendiente de pago" y que el inventario NO cambió.
5. **Cobrar**: "Registrar pago" → mostrar el mensaje de descuento →
   historial de inventario con el movimiento "venta" → catálogo público
   con la disponibilidad actualizada → **comprobante interno** (señalar
   la leyenda "no es factura fiscal").

Plan B si el wifi falla: la misma demo corre local con `python run.py`
(los datos locales son más ricos: historial completo de pruebas).

---

## 5. Propuesta de 6 slides

1. **Portada**: nombre del sistema, problema que resuelve (talonarios →
   sistema integrado), stack en una línea.
2. **El negocio**: los 3 tipos de usuario y el flujo
   Catálogo → Cotización → Pedido → Pago → Inventario.
3. **Reglas de negocio**: venta mínima por categoría, inventario solo
   baja al pagar, stock oculto al público, nada se elimina.
4. **Arquitectura**: Flask + Blueprints + capas
   (rutas → servicios → modelos → templates), SQLite, diagrama simple.
5. **Cómo se construyó**: 8 fases, ~36 PRs con revisión, un sprint = una
   rama = un PR; lo investigado fuera del curso.
6. **Demo** (dejar esta slide abierta e ir al navegador).

---

## 6. Preguntas probables y dónde está el código

**¿Cómo guardan las contraseñas?**
Con hash scrypt de Werkzeug, nunca en texto plano.
→ `app/models/user.py` (`set_password` / `check_password`)

**¿Cómo funciona el login?**
Flask-Login: `user_loader` carga el usuario de la sesión; rutas
protegidas con `@login_required` y decoradores de rol propios.
→ `app/__init__.py`, `app/blueprints/auth/`

**¿Dónde se valida la venta mínima por categoría?**
En el servicio de productos (`get_minimum_sale`: cosméticos 1 caja,
juguetes 3 ó 6 según precio, flores 3 ramos) y se aplica al armar
pedidos, al disminuir cantidades y al convertir cotizaciones.
→ `app/services/products_service.py`, `app/services/orders_service.py`

**¿Cómo evitan el doble descuento de inventario?**
`mark_as_paid` valida el estado (un pedido pagado se rechaza), valida
TODAS las existencias antes de descontar la primera, y confirma todo en
una sola transacción. → `app/services/orders_service.py`

**¿Por qué el cliente no ve el stock?**
El servicio del catálogo público solo expone el nivel de disponibilidad
(calculado del stock y el umbral de la subcategoría), nunca el número.
→ `app/services/catalog_service.py`, `app/services/inventory_service.py`

**¿Qué pasa si dos pedidos quieren el mismo stock?**
Los pendientes no reservan; el primero en pagar se lo lleva y al segundo
se le rechaza el pago con un mensaje claro (validación al pagar).

**¿Por qué usan Decimal para el dinero?**
Los float acumulan errores de redondeo; `Decimal`/`Numeric(10,2)` son
exactos para dinero. → modelos de producto, pedido y cotización

**¿Cómo funciona el deploy si Vercel es de solo lectura?**
La base de demostración viaja en el repo y se copia a `/tmp` (escribible)
en cada arranque en frío: la demo funciona completa y se restaura sola.
→ `api/index.py`

**¿Qué fue lo más difícil?**
Depurar el deploy: Vercel excluye del bundle cualquier carpeta llamada
`public` (la reserva para estáticos). Lo encontramos con un diagnóstico
que listaba el árbol de archivos dentro de la función, y se resolvió
renombrando las carpetas a `site` sin cambiar los endpoints (el
blueprint conserva su nombre). Historia completa en `PR_tracker.md`.

**¿Qué usaron del curso?**
Variables y tipos, condicionales (reglas de negocio), ciclos for/while,
listas y diccionarios (en servicios y seeds), 40+ funciones propias con
parámetros y return, modularidad (26 módulos Python conectados con
imports, scripts con `if __name__ == "__main__"`), librería estándar
(`datetime`, `decimal`, `os`, `functools`, `re`).

---

## 7. Checklist de entrega

- [x] Repositorio en GitHub con ramas `feature/*` → `dev` → `main`
- [x] 36 Pull Requests revisados y mergeados (bitácora en `PR_tracker.md`)
- [x] Código en múltiples archivos, comentado en español
- [x] README final con instrucciones verificadas en clon fresco
- [x] Deploy publicado y funcionando, link en el README
- [x] Reglas de negocio validadas automáticamente (9/9)
- [x] `main` actualizado con la versión final
- [ ] Slides (máximo 6 — propuesta en la sección 5)
- [ ] Ensayar la demo una vez completa (guion en la sección 4)
