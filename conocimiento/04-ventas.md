# Ventas

El módulo de ventas registra ventas de productos. El usuario selecciona productos y cantidades. El sistema calcula solo el total de la venta. Al confirmar, descuenta las unidades vendidas del inventario en la misma operación.

## Precio e idempotencia

La venta no acepta un precio enviado por el cliente. El total sale del precio guardado en el catálogo por la cantidad pedida. La operación usa una clave de idempotencia para no descontar dos veces el mismo registro si la petición se repite.

## Stock insuficiente

El sistema evita ventas que superen las existencias disponibles. Si la cantidad pedida es mayor que la existencia, la venta se rechaza y el inventario no cambia. No queda una venta a medias con stock negativo.

## Historial

El negocio puede consultar el historial de ventas. Cada venta guarda el detalle de productos y cantidades. El sales-service calcula los totales y coordina la actualización del inventario.

## Quién vende

El propietario puede ver y registrar ventas. El empleado de ventas puede ver y registrar ventas. El administrador de inventario no tiene permiso de ventas: no registra ventas ni consulta el historial de ventas por ese rol. Si necesita vender, debe hacerlo un empleado de ventas o el propietario.

El plan FREE ya incluye ver y registrar ventas.

## Servicio

El sales-service escucha en el puerto local 3004. El panel entra por el API Gateway. La documentación local queda en http://localhost:3004/api/docs.

## Qué no hace una venta en el MVP

Registrar una venta no emite factura electrónica, no se conecta con un sistema contable y no cobra por una pasarela de pago. Esas funciones están fuera del alcance. El soporte explica el registro operativo y el descuento de inventario, no el cobro con tarjeta ni la factura ante la autoridad tributaria.
