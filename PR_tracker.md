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
