# SistemaInventario-Web
Este es un sistema que incluye un catálogo digital, conectado a un sistema de inventario interno para utilizar en sala de ventas. Además incluye un sistema para vendedores para realizar descuentos. Tendrá un usuario administrador el cual permitirá modificar productos, ventas y más.

# Sistema Web Mayorista para Importadora

Este proyecto consiste en el desarrollo de un sistema web para una empresa importadora que vende productos al por mayor en Guatemala, principalmente en las categorías de cosméticos, juguetes y flores. El objetivo principal es digitalizar el catálogo de productos, controlar el inventario en tienda y registrar ventas internas de forma más ordenada, evitando el uso de talonarios manuales y reduciendo errores en precios, cantidades y disponibilidad.

La plataforma está pensada para dos tipos de uso: una página pública donde los clientes pueden consultar el catálogo mayorista y realizar cotizaciones, y un sistema interno donde el administrador y los vendedores pueden gestionar productos, ventas e inventario en tiempo real.

## Objetivo del proyecto

Crear una solución web que permita a la empresa mostrar sus productos de forma profesional, recibir cotizaciones de clientes mayoristas y controlar las ventas realizadas en tienda, conectando automáticamente cada venta pagada con el inventario disponible.

## Módulos principales

### Página web pública

La página pública funciona como un catálogo mayorista para clientes. En ella se muestran los productos disponibles organizados por categorías:

- Cosméticos
- Juguetes
- Flores

Cada producto cuenta con información como nombre, código, imagen, categoría, presentación de venta, precio, cantidad mínima de compra y estado de disponibilidad. Por seguridad, el cliente no puede ver la cantidad exacta de inventario, únicamente estados generales como:

- Disponible
- Baja disponibilidad
- Agotado

Además, los clientes pueden agregar productos a una cotización y enviar su solicitud para que posteriormente sea atendida por la empresa.

### Sistema de inventario en tienda

El sistema permite llevar control del inventario disponible en tienda utilizando la misma información registrada en el catálogo. Cada producto tiene un stock interno que solo puede ver el administrador o los usuarios autorizados.

El inventario se actualiza únicamente cuando una venta es marcada como pagada. Esto permite diferenciar entre una cotización, un pedido pendiente y una venta confirmada.

### Sistema de ventas

Los vendedores cuentan con un panel interno donde pueden registrar pedidos sin necesidad de escribir talonarios a mano. Desde este módulo pueden buscar productos por código o nombre, agregar cantidades, ver precios, calcular subtotales y generar el total del pedido automáticamente.

También pueden cargar una cotización existente mediante su número de cotización, convertirla en pedido y finalizar la venta cuando el cliente realiza el pago.

## Reglas de venta mayorista

El sistema está diseñado según las reglas reales de venta de la empresa:

### Cosméticos

Los cosméticos se venden por caja o display. La mayoría de productos vienen en presentaciones de 24 unidades y no se venden por unidad individual.

Ejemplo:

- 1 caja de labiales
- 1 display de maquillaje
- 10 cajas para aplicar precio especial mayorista, según configuración del producto

### Juguetes

Los juguetes se venden según el precio del producto. La cantidad mínima puede variar dependiendo del costo:

- Productos con precio mayor a Q20: mínimo 3 unidades por modelo
- Productos con precio menor a Q20: mínimo 6 unidades por modelo
- Productos con precio menor a Q15: mínimo media docena por modelo

### Flores

Las flores se venden por ramos. Cada código representa un color y estilo específico. La cantidad mínima de venta es de 3 ramos por código.

## Roles del sistema

El sistema contempla dos tipos principales de usuario:

### Administrador

El administrador puede:

- Registrar productos
- Editar información del catálogo
- Subir imágenes
- Definir precios
- Configurar cantidades mínimas de venta
- Definir descuentos mayoristas por producto
- Controlar inventario en tienda
- Ver ventas realizadas
- Consultar reportes básicos
- Crear usuarios vendedores

### Vendedor

El vendedor puede:

- Iniciar sesión en el sistema
- Buscar productos por código o nombre
- Crear pedidos en tienda
- Cargar cotizaciones existentes
- Registrar cantidades vendidas
- Calcular totales automáticamente
- Marcar pedidos como pagados, según permisos
- Generar comprobantes de venta

## Funcionalidades destacadas

- Catálogo público profesional para clientes mayoristas
- Organización de productos por categoría y subcategoría
- Cotizador en línea para clientes
- Número único de cotización
- Panel administrativo para gestión de productos
- Panel de vendedores para ventas en tienda
- Control de inventario en tiempo real
- Descuento de inventario únicamente al confirmar pago
- Reglas de venta mínima según tipo de producto
- Estados públicos de disponibilidad sin mostrar stock exacto
- Cálculo automático de precios, subtotales y totales
- Registro de ventas realizadas por vendedores

## Problema que resuelve

Actualmente, muchas ventas pueden registrarse de forma manual, lo que puede generar errores al escribir códigos, precios, cantidades o totales. Además, si no existe un control actualizado del inventario, pueden ocurrir problemas cuando un producto se vende en tienda pero todavía aparece como disponible para clientes que cotizan en línea.

Este sistema busca resolver esos problemas centralizando la información del catálogo, inventario y ventas en una misma plataforma.

## Descripción general

El proyecto representa una solución web enfocada en una empresa importadora mayorista. Combina una página pública para mostrar productos y recibir cotizaciones con un sistema interno para administrar inventario y ventas. Su propósito es mejorar la atención al cliente, facilitar el trabajo de los vendedores y brindar al administrador mayor control sobre la operación diaria de la empresa.
