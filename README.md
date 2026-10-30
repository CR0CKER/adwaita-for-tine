# Adwaita for Tine

Makes [Tine](https://github.com/martinkoutecky/tine), the Logseq-compatible outliner, look like a
native GNOME app: Adwaita colours, GNOME Files' sidebar, round GNOME buttons, light and dark. It is a
port of [Adwaita for Logseq](https://github.com/CR0CKER/adwaita-for-logseq) (v0.3.3), so Tine and
Logseq look the same side by side.

Built for **Tine 0.8.1** on GNOME 49. The CSS targets Tine's markup, which can change
between releases.

## What's in it

Tine has two theming layers, and neither can carry everything, so the theme comes in two parts:

| File | Tine calls it | What it can hold | What this one sets |
|---|---|---|---|
| `theme.json` | a theme package | ~20 Logseq colour tokens, literal colours only (no `var()`, no `url()`) | The Adwaita palette for light and dark: surfaces, text, borders, selection, highlights, and the accent for links, tags and bullets |
| `global.css` | device global CSS | any CSS | Everything else: fonts, layout, buttons, icons, motion |

Tine's plugins can't inject CSS, so a plugin isn't an option.

The configuration is fixed rather than set in options: the **yellow** GNOME accent, Adwaita for
Logseq's **"Text Editor (Adwaita scheme)"** text colours, **Adwaita Sans** and **Adwaita Mono**,
**close-only** window controls, and the **graph picker at the bottom**. To change the accent, see
[Changing the accent](#changing-the-accent).

## Install

1. **Theme package:** in Tine, Settings → Appearance → Theme packages, choose `theme.json`, then
   select **GNOME Adwaita**.
2. **CSS:** copy `global.css` to Tine's config folder. Tine reloads it when its window regains
   focus:

   ```bash
   cp global.css ~/.config/page.tine.Tine/global.css
   ```

   Or paste it in Settings → Appearance → Edit global CSS. Don't put it in the graph's
   `logseq/custom.css`: Logseq reads that file too, and it would fight Adwaita for Logseq there.

To undo: select another theme, and empty `global.css`. The CSS applies whichever theme is selected.

Also recommended:

- **Window frame:** leave Settings → Appearance → *native window frame* off. The theme styles Tine's
  own frameless title bar.
- **Rounded window corners:** Tine's window is an opaque GTK window with no transparency option, so
  CSS can't round it. The GNOME Shell extension
  [Rounded Window Corners Reborn](https://extensions.gnome.org/extension/7048/rounded-window-corners-reborn/)
  can. Set it to allow-list mode (`whitelist` on) and add Tine with the window picker in its
  preferences; 15px matches Adwaita for Logseq.

## What changes

**Colours** (`theme.json`):
- Adwaita's light and dark surfaces, text and borders. The accent goes through Adwaita for Logseq's
  oklab lightness clamps, pre-computed by `scripts/accent.py` because packages take literal colours
  only.

**Text** (`global.css`):
- Adwaita Sans for the interface and pages, Adwaita Mono for code.
- Page titles and journal dates in Text Editor's softer grey. Headings teal, inline code violet,
  quote bars grey, as in GNOME Text Editor's Adwaita scheme.

**Toolbar:**
- A flat header bar in the page's own colour, with no bottom line.
- Window controls are GNOME's round 24px buttons, close only, with GTK's own close icon.
- Tab titles at 11pt, the interface size (Tine uses 13px). Tab close buttons are libadwaita's flat
  24px circle, shown on the selected tab and on hover.

**Left sidebar**, laid out like Adwaita for Logseq's, which follows GNOME Files:
- The workspace picker is the sidebar header bar's title: flat, centred, bold, with GTK's
  `pan-down` arrow. It stays put while the sidebar scrolls, and lines up with the toolbar's buttons.
- Files-style rows: 36px, 9px radius, 11pt regular, 20px icons at 70% opacity. The icon size was
  measured against Files at the same scale.
- Rows sit 12px in from the sidebar's edge. The scrollbar sits at the sidebar's right edge, as in
  the main view, with a gutter so it doesn't cover the rows, even when it widens on hover.
- Journals and All pages first, then Favorites, Recent and Namespaces, with mixed-case headings and
  a chevron that turns when a section collapses.
- Page icons on All pages and the Recent rows. Favorites get a monochrome outline star in place of
  the yellow emoji, in the same column as the other icons.
- "+ New group" slides and fades in only while the pointer (or keyboard focus) is in Favorites;
  always shown on touch screens.
- Only the page list scrolls: the workspace title stays at the top, and New page and the graph
  picker stay at the bottom. The picker sits behind a divider, and its menu opens upwards.
- libadwaita's undershoot shadow (a 1px line and a 4px fade) at whichever end of the list has more
  to scroll to, as GNOME's sidebars draw it.
- Flat buttons (New page), with no outlines. The sidebar meets the page with a dark shade instead of
  a light line.

**Page:**
- The favourite star sits right after the page title, with the hover options (⋯, Table) after it,
  all level with the middle of the title's letters. A favourite's star is filled in the text colour,
  not yellow.

**Right sidebar:**
- Close and menu buttons are flat 24px circles with GNOME's `window-close` and `view-more` icons.

**Motion:**
- Both sidebars slide in when they open (250ms), pushing the page aside, like libadwaita's split
  views. Reduced motion turns this off.

## Known limits

These need changes in Tine itself, proposed upstream:

| What | Why CSS can't do it | Upstream |
|---|---|---|
| Sidebars close instantly | Tine removes a sidebar from the page the moment it closes, so there's nothing left to animate | [tine#806](https://github.com/martinkoutecky/tine/issues/806) |
| The sidebar's header row can't be grabbed to move the window | Tine marks drag areas with an HTML attribute in its code, which CSS can't add | [tine#815](https://github.com/martinkoutecky/tine/issues/815) |
| Ctrl+Q doesn't quit (use Alt+F4) | Tine has no quit command to bind | [tine#805](https://github.com/martinkoutecky/tine/issues/805) |

Also:
- **Scrollbars appear when the pointer moves**, not only while scrolling, and widen on hover. That
  is WebKitGTK's overlay scrollbar; CSS can't change when it shows, and sizing it would turn it into
  a classic bar that takes up room. (Logseq, on Chromium, only shows them while scrolling.)
- **Section headings** are re-cased from Tine's upper-case strings ("FAVORITES" → "Favorites"). For
  a language where lower-casing changes meaning, remove that rule.
- **Not ported from Adwaita for Logseq:** the merged headerbar, the ☰ app menu and the search button
  in the sidebar header. They would need markup Tine doesn't have.

## Changing the accent

```bash
scripts/accent.py teal        # any GNOME accent name, or a hex colour like '#3584e4'
```

It prints the five accent tokens for both modes. Paste them into `theme.json` and install the
package again: one with the same `id` and `version` replaces the installed copy. `global.css` has no
accent colours of its own.

## How it was checked

- `theme.json` passes Tine's own checker (`npm run theme:check -- <folder>` in a Tine clone).
- Sizes were measured in screenshots against GNOME Files at the same scale: text width and height,
  icon height and row spacing.
- Alignment was measured with element positions read in Tine's developer tools (Ctrl+Shift+J).

## License

MIT, see [LICENSE](LICENSE). `global.css` embeds GNOME's Adwaita symbolic icons (LGPL-3.0 or
CC-BY-SA-3.0, GNOME Project) and [Tabler Icons](https://tabler.io/icons) (MIT).
