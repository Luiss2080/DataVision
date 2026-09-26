# Skill: Desarrollo de pagina web adaptada al nuevo negocio

Usar esta guia cuando el objetivo sea adaptar o construir la web publica de un proyecto existente manteniendo el formato, estructura y arquitectura del proyecto base.

## Regla principal

Antes de tocar la pagina web, leer la instruccion del usuario sobre:

- Negocio.
- Contexto comercial.
- Publico objetivo.
- Colores.
- Fuente.
- Estilo visual.
- Categorias.
- Productos o servicios.
- Modelo de venta.
- Tono de comunicacion.

La web debe sentirse nativa del nuevo negocio desde el primer viewport.

## Que se conserva

- Arquitectura frontend.
- Rutas existentes.
- Layout base.
- Sistema de componentes.
- Stores.
- Servicios API.
- Formato visual general del proyecto si el usuario quiere conservarlo.
- Flujo de navegacion.
- Contratos con backend.

## Que se adapta

- Marca.
- Logo.
- Favicon.
- Loader.
- Header.
- Footer.
- Home.
- Hero.
- Carruseles.
- Cards.
- Catalogo.
- Detalle de producto o servicio.
- Promociones.
- Sucursales.
- Contacto.
- Nosotros.
- Paginas legales.
- Chatbot.
- WhatsApp.
- Modales.
- Estados vacios.
- Imagenes.
- Iconos.
- Colores.
- Fuente o tratamiento tipografico.
- Copy y microcopy.

## Auditoria inicial

Buscar textos y estilos del negocio anterior:

```bash
rg -n "nombreAnterior|rubroAnterior|categoriaVieja|colorViejo|textoLegacy" src public docs README.md
```

Buscar colores heredados:

```bash
rg -n "#[A-Fa-f0-9]{6}|rgba\\(" src
```

## Estructura recomendada de la web

La pagina web publica debe revisar como minimo:

1. Loader.
2. Header.
3. Hero principal.
4. Seccion de categorias.
5. Carrusel o grilla de destacados.
6. Catalogo real.
7. Promociones.
8. Servicios o beneficios.
9. Sucursales/contacto.
10. Footer.
11. Chat/WhatsApp.
12. Login/registro/carrito si aplica.

## Hero

El hero debe responder rapido:

- Que marca es.
- Que vende o que hace.
- Para quien es.
- Cual es la accion principal.

Evitar textos genericos como "la mejor experiencia" si no explican el negocio.

Ejemplo:

```txt
BeautyHouse reune mucho mas que maquillaje: cuidado personal, accesorios para cabello, bisuteria, unas, cuidado facial y corporal, cuidado capilar y moda beauty para mujeres que buscan variedad y cercania.
```

## Categorias

Las categorias deben salir del contexto real del negocio.

Ejemplo BeautyHouse:

- Maquillaje.
- Cabello y accesorios.
- Bisuteria.
- Unas.
- Facial y corporal.
- Cuidado personal.
- Moda beauty.
- Regalos y packs.

No usar categorias heredadas solo porque existen en el proyecto base.

## Cards adaptadas

Las cards no deben ser genericas si los productos son distintos.

Cada tipo de producto debe tener metricas propias.

Ejemplo BeautyHouse:

- Maquillaje: acabado, tono, uso, piel.
- Cabello: uso, agarre, look, llevar.
- Bisuteria: pieza, estilo, ocasion, look.
- Unas: acabado, kit, nivel, detalle.
- Skincare: zona, textura, rutina, piel.
- Cuidado corporal: zona, uso, formato, llevar.
- Accesorios: uso, formato, cartera, rutina.
- Regalos: incluye, empaque, ocasion, compra.

## Imagenes

Las imagenes deben mostrar el producto, servicio o experiencia real.

Evitar:

- Imagenes del negocio anterior.
- Imagenes oscuras o irrelevantes.
- Ilustraciones genericas si el producto necesita verse.
- Iconos que contradigan el rubro.

## Textos

El texto debe hablar en el tono que el usuario pidio.

Si el proyecto usa espanol boliviano con voseo, mantener:

- explora / explora segun el estilo elegido.
- pedi / compra.
- encontra.
- coordina.

Evitar mezclar tonos formales y casuales sin criterio.

## Validacion visual

Antes de terminar:

- Abrir home.
- Revisar header.
- Revisar hero.
- Revisar cards.
- Revisar catalogo.
- Revisar mobile si es posible.
- Revisar que no haya texto cortado.
- Revisar que botones no se desborden.
- Revisar que no queden colores viejos visibles.

## Resultado esperado

La web debe poder mostrarse al usuario como un producto coherente del nuevo negocio, no como una plantilla renombrada.

