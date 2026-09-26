# Prompt maestro para adaptar pagina web y sistema completo

Usar este prompt cuando se quiera repetir el resultado logrado con BeautyHouse en otro proyecto.

```txt
Quiero adaptar este proyecto existente a un nuevo negocio, igual que se hizo con BeautyHouse.

El proyecto base ya tiene mi estructura, formato de desarrollo, arquitectura, frontend, backend, rutas, componentes, stores, servicios, base de datos, seeds, tests y back-office. Quiero conservar todo eso.

Tu trabajo es adaptar la pagina web publica y el sistema/back-office al nuevo negocio.

IMPORTANTE:
Antes de tocar codigo, lee con mucha atencion mi instruccion sobre:
- negocio,
- contexto,
- publico objetivo,
- colores,
- fuente,
- estilo visual,
- categorias,
- productos o servicios,
- modelo de negocio,
- cosas que no deben aparecer del proyecto anterior.

Esa instruccion es la fuente de verdad. No asumas que el nuevo negocio es igual al anterior.

Nuevo negocio:
- Marca:
- Rubro:
- Publico objetivo:
- Modelo de negocio:
- Categorias:
- Productos/servicios:
- Colores:
- Fuente:
- Estilo visual:
- Tono de comunicacion:
- Contacto/sucursales/redes:
- Legacies prohibidos:

Objetivo:
Mantener la arquitectura, formato, rutas, componentes, backend, contratos API y estilo de desarrollo del proyecto base, pero transformar todo lo visible y contextual para que la web y el sistema parezcan nativos del nuevo negocio.

Tareas:
1. Lee AGENTS.md, README, docs/specs y package.json.
2. Audita textos, colores, imagenes, categorias y modulos legacy.
3. Actualiza documentacion/spec con el nuevo contexto.
4. Adapta la pagina web publica:
   - loader,
   - header,
   - home,
   - hero,
   - categorias,
   - carruseles,
   - cards,
   - catalogo,
   - promociones,
   - servicios,
   - contacto,
   - footer,
   - chatbot,
   - WhatsApp,
   - modales,
   - estados vacios.
5. Adapta las cards segun el tipo de producto o servicio. No uses siempre los mismos campos genericos.
6. Adapta el sistema/back-office:
   - sidebar,
   - dashboard,
   - modulos visibles,
   - formularios,
   - tablas,
   - reportes,
   - roles,
   - permisos visibles,
   - configuracion.
7. Adapta seeds y datos demo:
   - categorias,
   - productos/servicios,
   - usuarios,
   - roles,
   - sucursales,
   - promociones,
   - configuracion institucional.
8. Si quedan nombres legacy por compatibilidad tecnica, documentalos y evita mostrarlos al usuario final.
9. No crees mocks falsos ni endpoints ficticios para ocultar errores.
10. Valida con:
   - npm run lint,
   - npm run build,
   - npm run test:all si existe.
11. Levanta backend y frontend local.
12. Muestrame el resultado funcionando.

Criterio de exito:
- La web publica se entiende como el nuevo negocio desde el primer vistazo.
- El sistema/back-office opera con lenguaje del nuevo negocio.
- Las cards y categorias son especificas del rubro.
- No quedan restos visibles del proyecto anterior.
- Login y panel funcionan.
- Lint/build/tests pasan o se reporta claramente el motivo si algo externo falla.
```

