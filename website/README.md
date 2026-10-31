# FarStudio website

La web del estudio: portada, una página por juego, About y Privacy, en inglés, español, chino simplificado y japonés. Estilo "Faro nocturno". La estructura y las decisiones de diseño están en [ESTRUCTURA.md](ESTRUCTURA.md).

Es un sitio estático sin dependencias: un único script (`build.mjs`) genera HTML plano en `dist/`. Sin frameworks ni JavaScript en las páginas (solo unas líneas para cargar el tráiler de YouTube al pulsar play). Una página pesa unos 50 KB en total, con la tipografía incluida.

## Comandos

Desde la carpeta `website/` (necesita Node 18 o más):

```
node build.mjs          # genera dist/
npm run preview         # genera y sirve dist/ en http://localhost:4321
```

## Dónde está cada cosa

```
build.mjs               Plantillas de todas las páginas y el proceso de build.
src/site.json           Dominio, idiomas, email de contacto, YouTube, equipo, fecha de la política.
src/i18n/<idioma>.json  Textos de la interfaz, portada y About en cada idioma.
src/games/<juego>.json  Un archivo por juego (nombre, frase, descripción, tiendas, tráiler, arte, puntos fuertes).
src/games/<juego>/      Imágenes del juego (opcional): arte clave, portada, icono, capturas.
src/privacy/<idioma>.html  Texto de la política de privacidad.
src/styles.css          Todo el estilo.
public/                 Se copia tal cual a dist/ (tipografía Outfit en woff2).
```

Los logos, favicons e imagen para compartir se copian de `../branding/` en cada build: no se duplican aquí.

## Tareas habituales

- **Añadir un juego:** crea `src/games/<slug>.json` copiando el de Crime Sudoku, y sus imágenes en `src/games/<slug>/` (los nombres de archivo van en `art`). La portada, el pie, el sitemap y la página `/<idioma>/games/<slug>/` salen solos. Añade su sección en `src/privacy/*.html` con `<h2 id="<slug>">`.
- **Enlaces de tienda:** rellena `url` en `stores`. Mientras esté vacío, el botón sale como "Pronto".
- **Tráiler:** pon el ID del vídeo de YouTube en `trailer`.
- **Añadir un idioma:** añade su código a `languages` en `src/site.json`, crea `src/i18n/<código>.json` y `src/privacy/<código>.html`, y añade los textos del idioma en cada juego (si faltan, se usa el inglés).
- **Equipo en About:** rellena `team` en `src/site.json` (`name`, `role` por idioma y `photo` opcional). Si está vacío, la sección no se muestra.

## Publicar (Cloudflare Pages)

- Directorio raíz: `website`
- Comando de build: `node build.mjs`
- Directorio de salida: `dist`

`dist/_headers` marca la política de privacidad como `noindex` y `dist/sitemap.xml` la deja fuera. La raíz `/` lleva a cada visitante a su idioma según el navegador (inglés si no hay coincidencia).

## Antes de publicar

- Confirmar dominio y email en `src/site.json`.
- Revisar la política de privacidad (es un borrador) y confirmar qué datos recoge cada juego.
- Revisar con nativos los textos en chino y japonés.
- Sustituir los textos y el arte provisionales de Crime Sudoku.
