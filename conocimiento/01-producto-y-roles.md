# NexoStock: producto, usuarios y roles

NexoStock es una plataforma web de gestión de inventario y ventas para pequeños y medianos negocios. El lema del producto es: conectamos tu inventario con el crecimiento de tu negocio. El público son propietarios de tiendas, papelerías, comercios minoristas, administradores de inventario y empleados que registran productos y ventas.

El problema que atiende es el control con cuadernos u hojas de cálculo: existencias desconocidas, errores de entrada y salida, ventas perdidas, productos con bajo inventario sin alerta y falta de reportes.

## Acceso

El usuario inicia y cierra sesión en el panel. El servicio de autenticación valida las credenciales y entrega un JWT. El frontend no llama a cada microservicio por su cuenta: entra solo por el API Gateway. El token lleva el businessId del negocio. Productos, inventario, ventas y reportes verifican ese token y filtran los datos de ese negocio. Un usuario no ve información de otro negocio.

## Roles del negocio

Hay tres roles de negocio y uno de plataforma.

El Propietario (código OWNER) tiene todos los permisos del negocio: tablero, productos, inventario, ventas, reportes, usuarios, roles y datos del negocio. Solo un propietario puede modificar a otro propietario. Solo un propietario puede asignar el rol de propietario. El negocio no puede quedarse sin un propietario activo.

El Administrador de inventario (código INVENTORY_ADMIN) puede ver y administrar productos y puede ver y administrar inventario. No registra ventas, no administra usuarios y no cambia roles.

El Empleado de ventas (código SALES_EMPLOYEE) puede ver el catálogo y puede ver y registrar ventas. No modifica productos, no registra entradas de inventario y no ve la administración de usuarios.

El Superadministrador (código SUPER_ADMIN) no es un empleado de la tienda. Administra la plataforma NexoStock: usuarios de plataforma, roles, negocios y módulos. No se usa para operar el mostrador de un negocio.

## Planes

Cada negocio tiene un plan que recorta permisos aunque el rol los tenga.

El plan FREE incluye productos, inventario, ventas, usuarios, datos del negocio y módulos. En FREE no está la gestión de roles, no está el tablero y no están los reportes.

El plan BASIC suma al FREE la gestión de roles, la vista del tablero y la vista de reportes.

El plan PRO incluye todos los permisos de negocio.

## Qué puede pedir cada persona al soporte

Si un empleado de ventas pide crear un producto, el soporte indica que esa acción corresponde al administrador de inventario o al propietario. Si pide cambiar roles, corresponde al propietario y además el plan debe ser BASIC o PRO, porque FREE no incluye la gestión de roles.
