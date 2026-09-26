# Skill: Desarrollo de sistema / back-office adaptado al nuevo negocio

Usar esta guia cuando el objetivo sea adaptar el panel interno, sistema administrativo o back-office de un proyecto existente a un nuevo negocio.

## Regla principal

El sistema interno tambien debe responder al contexto del negocio. No basta con adaptar la web publica.

Antes de tocar modulos internos, leer la instruccion del usuario sobre:

- Operacion del negocio.
- Roles reales.
- Procesos internos.
- Productos o servicios.
- Inventario.
- Ventas.
- Sucursales.
- Reportes.
- Flujos de trabajo.
- Paleta y estilo visual.
- Nombres que NO deben aparecer.

## Que se conserva

- Arquitectura del sistema.
- Rutas internas.
- Permisos.
- Backend.
- Base de datos.
- Componentes compartidos.
- Layout del panel.
- Contratos API.
- Modulos tecnicos necesarios.

## Que se adapta

- Sidebar.
- Dashboard.
- KPIs.
- Formularios.
- Tablas.
- Filtros.
- Empty states.
- Modales.
- Reportes.
- Roles visibles.
- Permisos visibles.
- Modulos operativos.
- Nombres comerciales.
- Ayudas y placeholders.
- Datos semilla del sistema.

## Mapeo de modulos legacy

Cuando el proyecto viene de otro rubro, algunos nombres pueden quedar por compatibilidad tecnica, pero no deben verse asi en la UI.

Ejemplos:

| Legacy tecnico | Nombre visible sugerido |
|---|---|
| cocina / horno | Armado / Produccion / Preparacion |
| mesas | Pedidos asistidos / Atencion |
| recetas | Formulas / Kits / Componentes |
| insumos | Inventario / Componentes / Materia prima |
| salteñas / menu | Productos / Catalogo |
| catering | Packs / Servicios / Regalos |
| colegios / cursos | Clientes / Programas / Servicios segun rubro |

## BeautyHouse como ejemplo logrado

En BeautyHouse, el sistema debia dejar de sentirse gastronomico y pasar a operar como retail beauty.

Se adapto el enfoque visible a:

- Catalogo beauty.
- Productos.
- Categorias.
- Stock.
- Compras.
- Proveedores.
- Ventas/POS.
- Cajas.
- Delivery.
- Promociones.
- Clientas.
- Fidelidad.
- Sucursales Santa Cruz.
- Armado de kits/gift boxes.
- Asesoria.
- Reportes.
- Roles.
- Configuracion.

Algunos endpoints legacy como `horno` o `pedidos_mesa` pueden mantenerse por contrato, pero se deben documentar y evitar en lenguaje final si contradicen el negocio.

## Dashboard

El dashboard debe mostrar indicadores del negocio nuevo.

Ejemplo BeautyHouse:

- Ventas del dia.
- Productos mas vendidos.
- Stock bajo.
- Pedidos pendientes.
- Entregas.
- Promociones activas.
- Clientas nuevas.
- Ventas por categoria beauty.
- Sucursales.
- Compras por mayor.

No mostrar indicadores del negocio anterior.

## Formularios

Actualizar labels y placeholders.

Ejemplo:

- Producto.
- Categoria beauty.
- Tono.
- Variante.
- Stock.
- Precio.
- Proveedor.
- Sucursal.
- Kit/regalo.
- Observaciones para clienta.

## Roles

Los roles deben tener sentido operativo.

Ejemplo BeautyHouse:

- Administradora.
- Asesora Beauty.
- Cajera.
- Inventario.
- Armado de packs.
- Delivery.
- Marketing.
- Personal BeautyHouse.

## Reportes

Los reportes deben medir el nuevo negocio.

Ejemplo:

- Ventas por categoria.
- Ventas por sucursal.
- Stock por producto.
- Productos con mayor rotacion.
- Promociones usadas.
- Compras a proveedores.
- Clientas frecuentes.
- Delivery por zona.

## Seeds del sistema

Actualizar:

- Usuarios iniciales.
- Roles.
- Permisos visibles.
- Productos.
- Categorias.
- Sucursales.
- Proveedores.
- Insumos/componentes.
- Movimientos de stock.
- Ventas demo.
- Configuracion institucional.

## Validacion

Antes de terminar:

- Login admin funciona.
- Acceso al panel funciona.
- Sidebar no tiene nombres incorrectos.
- Dashboard habla del nuevo negocio.
- Formularios usan labels correctos.
- Tablas muestran datos coherentes.
- Reportes responden.
- Endpoints protegidos siguen protegidos.
- Tests pasan si existen.

