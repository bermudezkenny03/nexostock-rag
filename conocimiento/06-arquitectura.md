# Arquitectura y límites del MVP

NexoStock separa la interfaz y seis responsabilidades de backend. El frontend está en Vue.js con TypeScript, Vue Router, Pinia y Axios. El backend está en NestJS y TypeScript. La autenticación usa JWT. La base de datos del MVP es PostgreSQL. En la etapa inicial los servicios pueden compartir una instancia de PostgreSQL, con esquemas o tablas separados por dominio. Bases independientes por servicio quedan para una versión futura.

## Puerta de entrada

El frontend solo habla con el API Gateway. El gateway recibe la petición, aplica CORS, verifica el JWT y enruta al microservicio. En local el gateway publica el puerto 3000. El panel de desarrollo (npm run dev) publica el puerto 5173.

Puertos locales de cada servicio:

- api-gateway: 3000. Única puerta de entrada.
- auth-service: 3001. Identidad, negocios, roles y planes.
- products-service: 3002. Catálogo y categorías.
- inventory-service: 3003. Existencias, movimientos y alertas.
- sales-service: 3004. Ventas y descuento de inventario.
- reports-service: 3005. Indicadores de inventario y ventas.

En producción esos puertos no salen del servidor. Solo el frontend atiende el dominio. El MVP desplegado está en https://nexostock.pro. Producción no carga datos de prueba. En local, los datos de prueba se cargan si RUN_SEED=true.

GET /api/health en el gateway informa si cada servicio responde. La documentación de cada API queda en /api/docs de ese servicio.

## Alcance del MVP

El MVP incluye autenticación y roles, productos y categorías, entradas y salidas de inventario, ventas con actualización de existencias, alertas de bajo inventario y reportes básicos.

Están fuera del alcance: facturación electrónica, integración con sistemas contables, gestión de múltiples sucursales, aplicaciones móviles nativas, integración con pasarelas de pago, predicción de demanda mediante inteligencia artificial e integración con plataformas externas de comercio electrónico.

El soporte no describe cómo implementar esas funciones. Responde que están fuera del alcance del MVP.

## Entornos

Local usa docker-compose.yml. Producción usa docker-compose.prod.yml. No se mezclan. El chat de soporte de este laboratorio (Open WebUI en el puerto 8080) no forma parte de esos compose: es un asistente aparte y no reemplaza al gateway ni a la base de datos.
