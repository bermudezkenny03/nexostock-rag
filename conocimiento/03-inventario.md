# Inventario

El módulo de inventario controla existencias. Permite registrar entradas de productos, registrar salidas de productos, consultar las existencias actuales y mantener un historial de movimientos de inventario.

## Nivel mínimo y alertas

Cada producto puede tener un nivel mínimo de existencias. Cuando la cantidad disponible llega a ese mínimo o queda por debajo, el sistema genera una alerta de bajo inventario. La alerta no compra mercancía sola: avisa para que el negocio registre una entrada.

## Reglas de movimiento

No se permiten movimientos que dejen existencias negativas. Una salida mayor que la cantidad disponible se rechaza. Una venta tampoco puede dejar el inventario en negativo: el servicio de ventas valida la disponibilidad antes de descontar.

El historial conserva entradas y salidas. Sirve para revisar quién movió mercancía y cuándo, sin editar el pasado para maquillar el stock.

## Quién mueve el inventario

El propietario puede ver y administrar inventario. El administrador de inventario puede ver y administrar inventario: entradas, salidas, mínimos y consulta de existencias. El empleado de ventas no registra entradas ni salidas manuales. Su efecto sobre el stock ocurre solo cuando registra una venta válida, y ese descuento lo hace el servicio de ventas.

El plan FREE ya incluye ver y administrar inventario.

## Servicio

El inventory-service escucha en el puerto local 3003. El panel entra por el API Gateway. La documentación local de esa API queda en http://localhost:3003/api/docs.

## Qué responde el soporte

El soporte explica cómo registrar una entrada, cómo consultar existencias, cómo configurar el nivel mínimo y por qué una salida fue rechazada si iba a dejar stock negativo. No dice cuántas unidades hay de un producto real. Esa cifra está en el panel, en existencias actuales, y el asistente no tiene acceso a la base de datos.

## Fuera de este módulo

La predicción de demanda por inteligencia artificial y la reposición automática con proveedores están fuera del alcance del MVP.
