# Reportes e indicadores

El módulo de reportes muestra el estado general del inventario, los productos con bajo nivel de existencias, reportes básicos de ventas, los productos con mayor movimiento e indicadores generales del negocio.

Los datos salen de ventas e inventario. El reports-service no crea productos ni registra ventas: solo consulta y resume.

## Plan necesario

Ver reportes no está en el plan FREE. El plan FREE no incluye la vista de reportes ni la vista del tablero. Esas vistas llegan en el plan BASIC (vista de reportes y vista del tablero) y se mantienen en el plan PRO.

Si un negocio FREE pregunta por qué no ve reportes, el soporte explica que debe pasar a BASIC o PRO. No inventa un menú oculto.

## Quién consulta

En un plan que incluye reportes, el propietario puede verlos. El administrador de inventario y el empleado de ventas no tienen el permiso de reportes en su rol de sistema. La consulta de indicadores corresponde al propietario cuando el plan es BASIC o PRO.

El tablero (dashboard) sigue la misma regla de plan: no está en FREE; la vista está en BASIC y PRO.

## Servicio

El reports-service escucha en el puerto local 3005. El panel entra por el API Gateway. La documentación local queda en http://localhost:3005/api/docs.

La salud del sistema se consulta con GET /api/health en el gateway. Esa ruta informa si cada servicio responde. No es un reporte de ventas.

## Qué no calcula el reporte

El reporte no predice la demanda futura, no propone compras automáticas y no exporta a un sistema contable. Esas funciones están fuera del alcance del MVP. El soporte se limita a bajo inventario, historial resumido de ventas, mayor movimiento e indicadores que el panel ya muestra.
