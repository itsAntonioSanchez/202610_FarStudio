# Applying the FarStudio brand to Crime Sudoku

A task for the agent working in the Crime Sudoku repository (`202610_crimesudoku`). Crime Sudoku is made by **FarStudio**; this repository (`202610_FarStudioBranding`) holds the studio's brand. Read its [README](../README.md) first: it says which file goes where and the rules every use must follow.

The game keeps its own identity (its app icon, the pulp look, the "CRIME SUDOKU" name). The studio only signs it, the way a publisher card or a "developed by" line does.

## Getting the files

Clone or pull this repository next to the game's, and copy into the game **only the files you use** (the whole package is 16 MB and most of it is for stores and social networks):

| File in this repository | Copy to | For |
|---|---|---|
| `png/logo-vertical/color-on-dark/farstudio-logo-vertical-color-on-dark-1024x711.png` | `Assets/_CrimeSudoku/Content/Art/Studio/` | Studio card at launch |
| `png/logo-horizontal/mono-black/farstudio-logo-horizontal-mono-black-1024x283.png` | `Assets/_CrimeSudoku/Content/Art/Studio/` | Title screen signature |
| `png/favicon/*` | The new WebGL template folder | Web build page |
| `png/banners/link-preview-1200x630.png` | The new WebGL template folder | Web build page |
| `svg/farstudio-logo-horizontal-color-on-dark.svg` | The new WebGL template folder | Web build page footer |

Import the PNGs as Sprites (UI), no compression artifacts on the edges (keep the import quality high; they are small). Never edit them: if a size is missing, regenerate it here (README, "Regenerating the files").

## Rules from the brand

- **Pieces.** Vertical logo (lighthouse above the name) is the primary one; horizontal logo (lighthouse | name, with a divider line) where there is little height; the symbol alone for anything square or under 32 px.
- **Variants.** `color-on-dark` (white lighthouse and name, amber light) is preferred and goes on black (`#111111`). `color-on-light` on white or light paper. `mono-black` / `mono-white` where the amber cannot read.
- **Clear space** is built into every file: do not crop it. **Minimum sizes**: vertical 120 px wide, horizontal 140 px wide, symbol 16 px.
- Never stretch, rotate, recolor, gray out, add effects to, or rearrange the logo. Amber (`#F5A623`) is only the lighthouse's light.

## To do

1. **Studio card at launch.** A short "FarStudio" card before the title screen on a cold start: black (`#111111`), the vertical logo `color-on-dark` centered at about 40 % of the screen width on the 1170 × 2532 reference, about 1.5 s with a fade in and out (LitMotion), a tap skips it, never shown again when coming back to the title from another scene. Prefer this in-game card over Unity's splash logos: it keeps the timing, the skip and the fade in our hands, and the Unity splash stays off as `Docs/ToDo/Release.md` says. Fit it with the loading flow in `Docs/Systems/LoadingScreen.md`.
2. **Title screen signature.** Sign the title screen's footer with the studio: the horizontal logo `mono-black` (the title screen is on paper), small but above its 140 px minimum on the reference screen, without pushing anything else out of the footer. Follow the layout rules in `Docs/Systems/TitleScreen.md` (the footer already holds the edition and the language link); if the footer has no room, a "A FARSTUDIO GAME" line in the footer's own type is the fallback, with the logo only on the studio card.
3. **Web build page.** The page around the WebGL build (the internal web build published on Cloudflare, `Docs/ToDo/Release.md`, "Web build (internal testing)") gets the studio's favicons (`favicon.ico`, 16, 32, the 180 apple-touch icon, 192 and 512), the page title "Crime Sudoku · FarStudio", the link preview image (`og:image`) and a slim black footer with the horizontal logo `color-on-dark` as SVG. This needs a WebGL template of our own instead of Unity's default page; leave the YouTube template as it is.
4. **Company name.** Set Player Settings' Company Name to `FarStudio` (today `DefaultCompany`). Unity keys `PlayerPrefs` by company and product name: check what `Docs/Systems/SaveSystem.md` and `Docs/Systems/Settings.md` keep there before changing it, and say in the commit whether saved progress carries over (it is fine to lose test saves before release, but say so). **Do not change the bundle identifier**: it is the owner's decision and cannot change once the game is on a store; leave it listed in `Docs/ToDo/Release.md`, "Still open".
5. **Store listings.** Note in `Docs/ToDo/Release.md` that when the listings are written the developer is "FarStudio", with `png/app-icon/square/farstudio-app-icon-1024x1024.png` from this repository as the developer icon and `png/banners/store-feature-graphic-1024x500.png` for Google Play's developer page.

## Done when

- The studio card shows on a cold start, fades, skips on tap and never shows on the way back to the title.
- The title screen footer carries the studio's signature and still lays out on the shortest and tallest supported screens.
- The web build's page has the favicons, title, link preview and footer.
- The project compiles from the CLI, the EditMode tests pass, and the game's documents are updated as its `Claude.md` asks: `TitleScreen.md`, `LoadingScreen.md`, `Release.md`, the folder tree in `Claude.md` (the new `Art/Studio/` folder and the WebGL template) and the docs index.
- Committed and pushed as the game's `Docs/Guidelines/GitWorkflow.md` says.

## Verifying

Capture the studio card and the title screen the way `Docs/Systems/TitleScreen.md` describes, on the reference screen and on a short one, and check them against this repository's README: clear space intact, above the minimum size, the right variant on the right background, amber only on the light.
