# Finance_api
Fabian Hernandez Castaño

endpoints utilizados:
Usuarios:

GET /users: Obtiene la información de todos los usuarios.
GET /users/{id}: Obtiene la información de un usuario específico.
PUT /users: Actualiza la información de un usuario.
POST /users: Crea un nuevo usuario.
DELETE /users/{id}: Elimina un usuario específico.

Ingresos y Gastos:

POST /income: Agrega un nuevo ingreso.
POST /expense: Agrega un nuevo gasto.
GET /income: Obtiene la lista de todos los ingresos.
GET /expense: Obtiene la lista de todos los gastos.
DELETE /income/{index}: Elimina un ingreso específico.
DELETE /expense/{index}: Elimina un gasto específico.

Reportes:

GET /report/basic: Obtiene un reporte básico de ingresos y gastos.
GET /report/extended: Obtiene un reporte ampliado de ingresos y gastos.
