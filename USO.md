# FarStudio · Paquete de marca

<p align="center"><img src="docs/readme/hero.png" alt="Logo de FarStudio" width="100%"></p>

Guía rápida de qué archivo usar en cada sitio. La misma guía en inglés está en el [README](README.md).

## Qué hay en el paquete

```
svg/        Maestros vectoriales. El texto ya está convertido a trazos: no hace falta tener la fuente.
  animated/         Faro con la luz animada (giro, parpadeo o encendido), SVG.
png/        Los mismos archivos en PNG, de 3840 px hacia abajo.
  symbol/           El faro solo.
  logo-vertical/    Faro encima del nombre. Versión principal.
  logo-horizontal/  Faro | nombre, con separador. Versión secundaria.
  wordmark/         Solo el nombre.
  app-icon/         Icono de tienda: square (cuadrado, sin transparencia) y rounded (esquinas redondeadas).
  avatar/           Foto de perfil: square (la plataforma lo recorta) y circle (ya recortado).
  favicon/          Iconos para webs: favicon.ico, 16, 32, 48, 192, 512 y apple-touch-icon de 180.
  banners/          Cabeceras y pantallas ya compuestas sobre fondo.
fonts/      Outfit (licencia OFL, se puede distribuir con el juego).
```

Cada PNG lleva su tamaño en el nombre: `farstudio-logo-horizontal-color-on-dark-1024x283.png` mide 1024 × 283 px. El número que se escoge es el lado más largo.

## Variantes de color

<table>
<tr><td><img src="docs/readme/variant-color-on-dark.png" alt="variant-color-on-dark"></td><td><img src="docs/readme/variant-color-on-light.png" alt="variant-color-on-light"></td></tr>
<tr><td><img src="docs/readme/variant-mono-black.png" alt="variant-mono-black"></td><td><img src="docs/readme/variant-mono-white.png" alt="variant-mono-white"></td></tr>
</table>

| Variante | Cuándo |
|---|---|
| `color-on-light` | Fondos blancos o claros. Faro y nombre en negro, luz en ámbar. |
| `color-on-dark` | Fondos negros u oscuros. Faro y nombre en blanco, luz en ámbar. **Es la versión preferida**: la luz luce más sobre negro. |
| `mono-black` | Todo en negro, sin ámbar. Impresión a una tinta, sellos, grabados, documentos en blanco y negro. |
| `mono-white` | Todo en blanco, sin ámbar. Sobre fotos o fondos de color donde el ámbar no se distinguiría. |

Fondo transparente en todas, salvo `app-icon`, `avatar` y `banners`, que ya llevan su fondo negro.

## Qué pieza usar

<table>
<tr><td><img src="docs/readme/piece-logo-vertical.png" alt="piece-logo-vertical"></td><td><img src="docs/readme/piece-logo-horizontal.png" alt="piece-logo-horizontal"></td></tr>
<tr><td><img src="docs/readme/piece-symbol.png" alt="piece-symbol"></td><td><img src="docs/readme/piece-wordmark.png" alt="piece-wordmark"></td></tr>
</table>

- **Vertical**: la principal. Créditos, splash, carteles, portadas, kit de prensa.
- **Horizontal** (faro | nombre): cuando hay poco alto. Cabeceras de webs y canales, pies de página, firmas, marca de agua en tráileres.
- **Símbolo**: todo lo que es cuadrado o muy pequeño. Iconos, avatares, favicon, por debajo de 32 px.
- **Wordmark**: solo el nombre, cuando el faro ya aparece cerca (por ejemplo, junto al avatar en una ficha de tienda).

## Qué archivo para cada sitio

| Dónde | Archivo |
|---|---|
| **App Store**, icono de developer | `app-icon/square/…-1024x1024.png` (Apple no admite transparencias; redondea él) |
| **Google Play**, icono | `app-icon/square/…-512x512.png` |
| **Google Play**, gráfico destacado | `banners/store-feature-graphic-1024x500.png` |
| **Steam**, avatar de desarrollador | `avatar/square/…-256x256.png` o `…-512x512.png` |
| **Steam**, cabecera de la página de desarrollador | `logo-horizontal/color-on-dark/…-1920x531.png` sobre negro, o `banners/social-header-1500x500.png` |
| **YouTube**, foto del canal | `avatar/square/…-800x800.png` |
| **YouTube**, banner | `banners/youtube-banner-2560x1440.png` (el logo cae dentro de la zona segura) |
| **Redes** (X, Instagram, TikTok, LinkedIn), foto de perfil | `avatar/square/…-400x400.png` u `…-800x800.png` |
| **Redes**, cabecera | `banners/social-header-1500x500.png` |
| **Gmail / Google**, foto de la cuenta | `avatar/square/…-800x800.png` |
| **Web**, cabecera | `svg/farstudio-logo-horizontal-color-on-light.svg` (o `-on-dark` si la cabecera es oscura) |
| **Web**, pie | `svg/farstudio-logo-horizontal-color-on-dark.svg` o `mono-white` |
| **Web**, favicon | `favicon/favicon.ico` + `favicon-32x32.png` + `favicon-16x16.png` + `apple-touch-icon-180x180.png` |
| **Web**, icono de app instalable | `favicon/favicon-192x192.png` y `favicon-512x512.png` |
| **Web**, vista previa al compartir un enlace | `banners/link-preview-1200x630.png` |
| **Juego**, splash de arranque | `banners/splash-dark-1920x1080.png` (o `-3840x2160` en 4K); en vertical, `logo-vertical/color-on-dark` centrado sobre negro |
| **Juego**, créditos | `logo-vertical/color-on-dark/…-1024x….png` |
| **Juego / tráiler**, firma en una esquina | `logo-horizontal/color-on-dark/…-512x….png` |
| **Kit de prensa, presentaciones** | Vertical u horizontal en SVG; PNG de 2560 o 3840 si no aceptan vectores |
| **Impresión** (tarjetas, pegatinas, camisetas) | Siempre SVG. Para una sola tinta, `mono-black` o `mono-white` |
| **Firma de correo** | `symbol/color-on-light/…-64x….png` (se ve nítido en pantallas de alta densidad) |

Si un sitio pide un tamaño que no está, escoge el siguiente más grande y deja que lo reduzca la plataforma, o exporta desde el SVG.

## Logo animado

<p align="center"><img src="docs/readme/ignite.gif" alt="El faro de FarStudio encendiéndose: unos destellos rápidos, un momento a oscuras y la luz se enciende despacio" width="480"></p>

En `svg/animated/` está el faro con la luz en movimiento, para webs, splash e intros. Es SVG + CSS puro: se reproduce dentro de una etiqueta `<img>`, sin JavaScript, y se queda quieto para quien tenga activado reducir el movimiento en su sistema.

| Animación | Qué hace | Ciclo |
|---|---|---|
| `rotate` (giro) | El haz da la vuelta: derecha, hacia ti (destello en la linterna), izquierda y por detrás (la luz se atenúa). | 6 s |
| `blink` (parpadeo) | La luz queda encendida y se apaga dos veces muy rápido, como la señal de un faro. | 3,2 s |
| `ignite` (encendido) | El faro encendiéndose: un parpadeo rápido que va cogiendo fuerza, un segundo a oscuras y luego la luz se enciende del todo, despacio, y se queda encendida. Para intros y splash. | una vez, 4 s |

Cada una está en `symbol`, `logo-vertical` y `logo-horizontal`, en `color-on-dark` (preferida) y `color-on-light`; por ejemplo, `svg/animated/farstudio-symbol-color-on-dark-rotate.svg`. Solo se mueve la luz: el faro y el nombre no cambian. Para montar el encendido en un motor de juego u otra herramienta, en [`animation/ignite/`](animation/ignite/README.md) están el logo separado en capas, la línea de tiempo en JSON y los pasos. Un logo animado por pantalla como mucho; donde el logo va pequeño o junto a texto, el estático.

### Versiones cortas (1,5 s)

Las mismas tres animaciones con tiempos que caben en **1,5 s contando una pausa quieta al final**, para arranques de app, transiciones y cortinillas. Se reproducen una vez y acaban en el logo estático. Hay dos opciones de cada una, con nombres `…-rotate-short-a.svg`, `…-rotate-short-b.svg`, etc., en las mismas piezas y colores.

| El archivo acaba en | Qué hace | Movimiento + quieto |
|---|---|---|
| `rotate-short-a` | Medio giro: derecha, hacia ti (destello), izquierda y se abren los dos haces. | 1,1 s + 0,4 s |
| `rotate-short-b` | Una vuelta entera rápida y se abren los dos haces. | 1,15 s + 0,35 s |
| `blink-short-a` | Dos apagones cortos, como el parpadeo largo. | 0,73 s + 0,77 s |
| `blink-short-b` | Tres apagones más seguidos, como la señal de un faro. | 0,68 s + 0,82 s |
| `ignite-short-a` | Tres destellos en crescendo, un momento a oscuras y la luz sube. | 1,15 s + 0,35 s |
| `ignite-short-b` | Los cinco destellos del encendido largo, comprimidos, casi sin pausa. | 1,1 s + 0,4 s |

Los tiempos están en `tools/short_timelines.py`.

## Reglas rápidas

<img src="docs/readme/clear-space.png" alt="Área de respeto X alrededor del logo">

- **Área de respeto**: deja libre alrededor al menos la altura de las mayúsculas del nombre (X). Los SVG y PNG ya la incluyen.
- **Tamaños mínimos**: vertical 120 px de ancho (30 mm), horizontal 140 px (35 mm), símbolo 16 px (5 mm). Por debajo, solo el símbolo.
- **No**: deformar, girar, cambiar la tipografía, aclarar o poner en gris, usar sobre fondos sin contraste, añadir sombras o efectos, cambiar el orden de las piezas ni separarlas más de lo que vienen.
- **El ámbar es solo la luz del faro**: linterna y haces. Nunca en el nombre ni en el resto del faro.

## Colores

<img src="docs/readme/palette.png" alt="Paleta">

| Color | HEX | RGB | Uso |
|---|---|---|---|
| Negro | `#111111` | 17 17 17 | Faro, nombre, fondos oscuros |
| Blanco | `#FFFFFF` | 255 255 255 | Fondos, logo en negativo |
| Luz de faro | `#F5A623` | 245 166 35 | Solo la linterna y los haces; los haces se apagan del 100 % al 15 % hacia fuera |
| Gris texto | `#555555` | 85 85 85 | Textos secundarios |
| Gris claro | `#E8E8E5` | 232 232 229 | Fondos de apoyo y separadores |

## Tipografía

<img src="docs/readme/typeface.png" alt="FARSTUDIO en Outfit">

Outfit (Google Fonts, licencia OFL). En el nombre: **FAR** en peso 600 y STUDIO en peso 300, todo en mayúsculas y con un espaciado entre letras de 0,22 em. Para textos de apoyo, Outfit 400.
