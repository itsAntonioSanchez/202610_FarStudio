# Estructura de la web de FarStudio (propuesta)

Cuatro tipos de página: la portada, una página por juego, "About us" y privacidad. Todo en varios idiomas.

## Mapa del sitio

Cada página existe en cada idioma, con el idioma al principio de la URL:

```
/<lang>/                    Portada: promociona los juegos
/<lang>/games/<juego>/      Una página por juego (p. ej. /en/games/crime-sudoku/)
/<lang>/about/              About us: quiénes somos
/<lang>/privacy/            Privacidad: accesible por enlace, no indexada
/<lang>/press/              (más adelante) Kit de prensa
```

Una URL por juego, corta y estable: el slug del juego no cambia nunca, porque irá en las fichas de las tiendas. El slug es el mismo en todos los idiomas.

## Idiomas

- **Pedidos:** inglés (`en`), español (`es`), chino simplificado (`zh-hans`) y japonés (`ja`).
- **Propongo añadir:** coreano (`ko`) y portugués de Brasil (`pt-br`), que son mercados muy grandes de juegos de móvil y puzles. Después, si se quiere más alcance en Steam: alemán (`de`) y francés (`fr`).
- **Inglés es el idioma por defecto.** `/` mira el idioma del navegador y redirige a `/es/`, `/ja/`, etc.; si no hay coincidencia, a `/en/`.
- **Selector de idioma** en la cabecera, que lleva a la misma página en el otro idioma (no a la portada).
- **Para Google:** cada página declara sus versiones en los demás idiomas (`hreflang`), con `en` como `x-default`.
- **Textos:** un archivo de textos por idioma para las partes comunes, y el contenido de cada juego traducido en su propio archivo de datos. Si falta una traducción, se muestra en inglés.
- **Tipografía:** Outfit no tiene caracteres chinos, japoneses ni coreanos. En esos idiomas el texto usa Noto Sans SC / JP / KR (u otra equivalente), y Outfit se queda para los títulos en alfabeto latino y el logo.

## Privacidad `/<lang>/privacy/`

- **No indexada:** lleva `<meta name="robots" content="noindex">`, no aparece en el `sitemap.xml` y no está en el menú principal.
- **Accesible por enlace:** la URL es pública y estable, para ponerla en App Store, Google Play, Steam y dentro de los juegos. Un enlace discreto en el pie, también con `noindex` en la página.
- **Una sola política del estudio**, con una sección por juego si alguno recoge datos distintos (anuncios, analítica, compras). Cada juego puede enlazar directamente a su sección: `/en/privacy/#crime-sudoku`.
- **En todos los idiomas**, pero la versión en inglés es la que manda legalmente (lo dice la propia página). La traducción de textos legales conviene revisarla.
- Incluye fecha de última actualización y email de contacto.

## Partes comunes a todas las páginas

- **Cabecera:** logo horizontal `color-on-dark` a la izquierda (enlace a la portada), y a la derecha "Games", "About" y el selector de idioma.
- **Pie:** símbolo pequeño, enlaces a YouTube y tiendas, "© FarStudio", enlace discreto a privacidad.
- **Estilo:** el de la marca. Fondo negro `#111111`, texto blanco, ámbar `#F5A623` solo como acento (el faro, botones), tipografía Outfit.
- **Favicons e imagen para compartir:** los de `branding/png/favicon/` y `branding/png/banners/link-preview-1200x630.png`.

## Portada `/`

1. **Hero:** el logo vertical con la animación del faro encendiéndose (`branding/svg/animated/`), una frase del estudio y un botón "Ver juegos".
2. **Juego destacado:** el último lanzamiento a todo lo ancho: arte del juego, nombre, una línea, tráiler y botones de tienda.
3. **Todos los juegos:** rejilla de tarjetas (icono o portada, nombre, plataformas). Cada tarjeta lleva a la página del juego.
4. **Del estudio:** dos líneas sobre nosotros y enlace a About.
5. **Seguir:** YouTube y redes (y más adelante, newsletter).

## Página de juego `/<lang>/games/<juego>/`

La misma plantilla para todos, pero cada página luce la identidad del juego (su arte, sus colores, su logo). El estudio solo firma, como en el juego.

1. **Hero del juego:** arte clave, logo del juego, una línea y botones de tienda (App Store, Google Play, Steam: solo los que existan).
2. **Tráiler** (YouTube).
3. **Qué es:** 3 o 4 puntos fuertes con una captura cada uno.
4. **Galería de capturas.**
5. **Datos:** plataformas, fecha de salida, idiomas, precio o "gratis".
6. **Firma:** "Un juego de FarStudio" con el símbolo, y enlaces a otros juegos.
7. **Soporte y privacidad:** enlace a su sección de la política de privacidad y un contacto de soporte (las tiendas piden ambas URL por app).

Cada juego se describe en un único archivo de datos (nombre, slug, frase, enlaces de tienda, tráiler, capturas, colores). Añadir un juego es añadir ese archivo y sus imágenes: la portada y la página salen solas.

## About us `/<lang>/about/`

1. **Quiénes somos:** qué es FarStudio y por qué hacemos juegos (el faro: algo que se ve desde lejos).
2. **El equipo:** foto o avatar, nombre y rol de cada persona.
3. **Cómo trabajamos / lo que nos importa:** tres ideas cortas.
4. **Contacto:** email del estudio (prensa, soporte, negocios).

## Cómo lo construiría

Un sitio estático (por ejemplo Astro), publicado en Cloudflare Pages, que ya usáis para la build web de Crime Sudoku. Sin servidor ni base de datos: rápido, barato y fácil de mantener. Astro trae rutas por idioma de serie, y los juegos y textos van como archivos de datos, como arriba.

## Por decidir

- **Idiomas extra:** ¿añadimos coreano y portugués de Brasil a los cuatro pedidos?
- **Dominio:** ¿farstudio.com u otro?
- **Juegos en la portada:** ¿solo Crime Sudoku de momento, o también los que están en desarrollo con un "Próximamente"?
