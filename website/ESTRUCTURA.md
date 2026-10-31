# Estructura de la web de FarStudio (propuesta)

Tres tipos de página: la portada, una página por juego y "About us". Todo lo demás (avisos legales, prensa) se cuelga de ahí.

## Mapa del sitio

```
/                       Portada: promociona los juegos
/games/<juego>/         Una página por juego (p. ej. /games/crime-sudoku/)
/about/                 About us: quiénes somos
/privacy/               Política de privacidad (las tiendas la piden; una para el estudio
                        y, si hace falta, una sección por juego)
/press/                 (más adelante) Kit de prensa: logos, capturas, datos
```

Una URL por juego, corta y estable: el slug del juego no cambia nunca, porque irá en las fichas de las tiendas.

## Partes comunes a todas las páginas

- **Cabecera:** logo horizontal `color-on-dark` a la izquierda (enlace a la portada), y a la derecha "Games" y "About".
- **Pie:** símbolo pequeño, enlaces a YouTube y tiendas, "© FarStudio", enlace a privacidad.
- **Estilo:** el de la marca. Fondo negro `#111111`, texto blanco, ámbar `#F5A623` solo como acento (el faro, botones), tipografía Outfit.
- **Favicons e imagen para compartir:** los de `branding/png/favicon/` y `branding/png/banners/link-preview-1200x630.png`.

## Portada `/`

1. **Hero:** el logo vertical con la animación del faro encendiéndose (`branding/svg/animated/`), una frase del estudio y un botón "Ver juegos".
2. **Juego destacado:** el último lanzamiento a todo lo ancho: arte del juego, nombre, una línea, tráiler y botones de tienda.
3. **Todos los juegos:** rejilla de tarjetas (icono o portada, nombre, plataformas). Cada tarjeta lleva a la página del juego.
4. **Del estudio:** dos líneas sobre nosotros y enlace a About.
5. **Seguir:** YouTube y redes (y más adelante, newsletter).

## Página de juego `/games/<juego>/`

La misma plantilla para todos, pero cada página luce la identidad del juego (su arte, sus colores, su logo). El estudio solo firma, como en el juego.

1. **Hero del juego:** arte clave, logo del juego, una línea y botones de tienda (App Store, Google Play, Steam: solo los que existan).
2. **Tráiler** (YouTube).
3. **Qué es:** 3 o 4 puntos fuertes con una captura cada uno.
4. **Galería de capturas.**
5. **Datos:** plataformas, fecha de salida, idiomas, precio o "gratis".
6. **Firma:** "Un juego de FarStudio" con el símbolo, y enlaces a otros juegos.
7. **Privacidad y soporte** del juego (las tiendas piden una URL de soporte por app).

Cada juego se describe en un único archivo de datos (nombre, slug, frase, enlaces de tienda, tráiler, capturas, colores). Añadir un juego es añadir ese archivo y sus imágenes: la portada y la página salen solas.

## About us `/about/`

1. **Quiénes somos:** qué es FarStudio y por qué hacemos juegos (el faro: algo que se ve desde lejos).
2. **El equipo:** foto o avatar, nombre y rol de cada persona.
3. **Cómo trabajamos / lo que nos importa:** tres ideas cortas.
4. **Contacto:** email del estudio (prensa, soporte, negocios).

## Cómo lo construiría

Un sitio estático (por ejemplo Astro), publicado en Cloudflare Pages, que ya usáis para la build web de Crime Sudoku. Sin servidor ni base de datos: rápido, barato y fácil de mantener. Los juegos como colección de archivos de datos, como arriba.

## Por decidir

- **Idiomas:** propongo inglés primero (las tiendas y el público son internacionales) y español después con `/es/`.
- **Dominio:** ¿farstudio.com u otro?
- **Juegos en la portada:** ¿solo Crime Sudoku de momento, o también los que están en desarrollo con un "Próximamente"?
