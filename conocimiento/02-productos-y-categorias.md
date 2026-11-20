# Productos y categorías

El módulo de productos permite crear, consultar, editar y desactivar productos. Desactivar un producto lo oculta de la operación diaria sin borrar su historial. El catálogo se consulta desde el panel.

## Datos de un producto

Cada producto registra nombre, descripción, categoría, precio y cantidad disponible. El precio lo define quien administra el catálogo. En una venta el cliente del API no envía el precio: el sistema usa el precio guardado en el producto.

Los productos se organizan por categorías. El servicio de productos administra las categorías y el catálogo.

## Quién administra el catálogo

El propietario puede ver y administrar productos. El administrador de inventario puede ver y administrar productos. El empleado de ventas solo puede ver el catálogo para elegir qué vende. No crea, no edita y no desactiva productos.

El plan FREE ya incluye ver y administrar productos, igual que BASIC y PRO.

## Servicio

El products-service escucha en el puerto local 3002. El panel no debe llamar a ese puerto: la petición pasa por el API Gateway. La documentación de esa API, en local, queda en http://localhost:3002/api/docs.

## Consultas que el soporte sí responde

El soporte explica cómo dar de alta un producto, cómo cambiar la categoría, cómo desactivarlo y qué campos son obligatorios en el registro: nombre, descripción, categoría, precio y cantidad disponible. El soporte no conoce el precio ni la existencia de un producto concreto de un negocio, porque no consulta la base de datos. Indica al usuario que abra el catálogo en el panel.

## Consultas que no corresponden a este módulo

Crear sucursales, publicar en una tienda en línea o sincronizar con un comercio electrónico externo no es parte del catálogo del MVP. Esas funciones están fuera del alcance.
