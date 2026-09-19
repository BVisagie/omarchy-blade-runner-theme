# Blade Runner

An Omarchy 4 (Quattro) theme for the 1982 film.

Los Angeles, November 2019. Sodium light through acid rain: a smog-blue night,
warm light that always comes *through* something (haze, blinds, rain, glass),
and one cold neon. The accent is sodium amber (`#E08A3A`); cyan is kept for the
things that should read cold.

## Install

Omarchy 4:

```sh
omarchy theme install https://github.com/BVisagie/omarchy-blade-runner-theme
```

Or *Install > Style > Theme* in the Omarchy menu (`Super + Space`) and paste that URL.

Backgrounds cycle with `Super + Ctrl + Space`. The theme opens on **Dusk**.

The base theme contains colors, shell styling, and static backgrounds. The
[optional Esper terminal](#esper-terminal) is launched separately.

Compatibility: targets **Omarchy 4 / Quickshell**, checked against the installed
**Omarchy 4.0.4** package, including its polkit prompt and image picker.
Omarchy 3's Waybar/Mako setup is not covered by these overrides.

## Palette

| Role | Hex | In the film |
| --- | --- | --- |
| Background | `#0A0E13` | The smog-blue night that never gets light |
| Accent | `#E08A3A` | Flare stacks over the city, the Voight-Kampff readout, the pyramid at sunset |
| Foreground | `#C3BBA9` | Lamplight on paper, warm through the haze |
| Muted | `#7C8791` | The smoke inside a light shaft |
| Selection | `#213946` | Blue bars of shadow from the blinds |
| Red | `#E05A45` | The opening title card |
| Yellow | `#D8AE5A` | Candlelight in the pyramid office |
| Cyan | `#5EC0CC` | Neon umbrella handles in the street crowd, the one cold neon |

Keywords stay in-world: the magenta slot carries title-card brick (`#C8745C`),
so editors paint keywords brick, never pink. Blue is a steel blue (`#7093C8`),
kept apart from both the cyan neon and muted comments, and green (`#8DAF7E`) rounds out the syntax
colours, each pulled toward the haze. Neon through smoke, not a synthwave
nightclub: no purple grids, no pink sunsets.

Every text colour, muted text and errors included, exceeds 4.5:1 contrast
against both the main background and the lifted panel background (`#151C24`).
Selection is the blinds' blue at two depths. Editors and terminals use
`#243C4A`, lifted so a visual-line selection is easy to find (cream text 9.31:1).
Menus, the launcher and btop fill the current row with a deeper `#213946` so
sodium text on it holds 4.52:1. `colors.toml` notes these floors next to the
keys they constrain.

## Esper terminal

From this repository, or after `cd ~/.config/omarchy/themes/blade-runner` for an
installed copy:

```sh
./scripts/blade-runner-terminal
./scripts/blade-runner-terminal --terminal foot
./scripts/blade-runner-terminal --font-size 12
./scripts/blade-runner-terminal --haze
```

Requires Python 3.11+, Ghostty or Foot, and JetBrainsMono Nerd Font. The default
is Ghostty. The launcher reads `colors.toml` directly, so it can preview the
palette before the desktop theme is applied. It keeps your normal terminal
configuration and overrides appearance for this session: 11pt type, additional
padding, an opaque background, and a steady block cursor. Ghostty also gets a
little extra line spacing and runs in a separate instance.

The companion Starship prompt shows directory, Git state, slow command duration,
and failed exit codes. SSH hosts appear as `off-world:host`, and root sessions
stay identifiable. Omarchy's usual shell startup initializes Starship; custom
shells need their own Starship initialization. `STARSHIP_CONFIG` is scoped to
the launched process and its children. No shell startup files, default terminal,
or keybindings are edited.

`--haze` enables a small static halation in Ghostty: bright glyphs bleed a
little amber-tinted light, like highlights through smoke. The halo radius follows
the display (about 6 px at 1440p, 7 px at 2160p), so it reads as haze, not as
sharpening. It adds no animation
loop, flicker, warping, or cursor trails, and the glow stays faint enough that
text and error colours read true. Foot uses the clean profile. Close the preview
window and open your normal terminal to return to your existing setup.

Run a specific command with arguments after `--`, or request the greeting by hand:

```sh
./scripts/blade-runner-terminal -- btop
./scripts/blade-runner-greeting
```

Alacritty and Kitty still receive the base palette through Omarchy. The optional
launcher supports Ghostty and Foot.

The launcher uses the documented [Ghostty configuration options](https://ghostty.org/docs/config/reference)
and [Starship prompt configuration](https://starship.rs/config/).

## Shell

The `shell.*.toml` files style the bar, controls, launcher, menus, notifications,
popups, tooltips, lock input, polkit prompt, and image picker. Sodium is kept for
focus and the current item, not for every card edge. Menus and the launcher sit
on the lifted panel with a muted edge, like tooltips; the selected row gets the
blinds-blue fill with sodium text. Keyboard focus gets a distinct 2px sodium
border. User font scaling remains inherited, and the bar keeps Omarchy's stock
size. Omarchy shares the bar's red active token among recording, updates, and
other attention states.

The active window border runs from sodium amber to a faint cyan: warm light
meeting cold. Notifications and popups carry the same gradient.

Omarchy replaces entire sections when applying these files, so overridden
sections include their supported defaults explicitly. Global user shell overrides
can still take precedence. No shell plugins or Hyprland behavior are installed.

## Backgrounds

All five are **3840×2160**.

1. **Dusk**: the top floor of a stepped megastructure at sunset, looking out through smog at pyramids and towers (first in the theme's cycle)
2. **Flight**: gliding down a rain-filled canyon of megastructures, air traffic, searchlights, and flare stacks where the canyon opens
3. **Blinds**: a sparse apartment at night, lamp against a passing searchlight sliced by venetian blinds across textile-block walls
4. **Noodle bar**: an empty street counter under a dripping overhang, crates and drums for seats, steam and one cyan tube on wet asphalt
5. **Atrium**: an iron-and-glass atrium in decay, searchlight shafts through the skylight onto a wet tiled floor

Each still is an original generation from a written prompt that rules out
people, faces, logos, readable text, and recreations of film frames. They were
generated at 1672×941. Blinds and Noodle bar were retouched where the generator
added a figure in a distant doorway and stencil-like marks on crates, a drum,
and a wall box.

Each was then fitted to 4K with Lanczos and restored with the one-step
[VOSR 2.0](https://github.com/cswry/VOSR) super-resolution model, using a wavelet
colour fix. That keeps composition, lighting, and grading those of the source.
Every result was compared with its source at 100% and checked by scaling it back
down, so added detail is fine structure, not new objects. These are finished
generations, not native 4K renders.

## Lock screen

This theme styles the lock input with readable placeholder text: a muted border
at rest, sodium amber while typing, and red on a wrong password. Selected text
in the field is tinted sodium, not boxed in a solid block. Polkit prompts match:
muted at rest and red on error. Polkit has no typing state for its border, so
sodium shows through its lock glyph and text selection instead. The theme does
not replace the lock design or authentication.

## What it themes

Omarchy generates the rest from `colors.toml` when the theme is applied:

- Omarchy shell (bar, menus, notifications, OSD, lock chrome, polkit prompt)
- Alacritty, Foot, Ghostty, Kitty
- Neovim (Aether), Helix, VS Code, Obsidian
- btop, Chromium
- Hyprland active border
- Keyboard RGB (`E08A3A`)
- Icons: `Yaru-yellow-dark`

## Validation

```sh
python -m unittest discover -s tests -v
./scripts/blade-runner-terminal --check
./scripts/blade-runner-terminal --terminal foot --check
./scripts/blade-runner-terminal --haze --check
```

The GitHub Actions workflow checks every shipped wallpaper's 4K dimensions,
palette contrast and ANSI aliases, that every shell file is a real Omarchy 4
section using only palette colours, launcher argument handling and invalid
options, the plain-text greeting, and GLSL compilation. The shader test requires
`glslangValidator` and skips locally if it is absent; CI installs it. Terminal
`--check` commands validate configs without opening a window.

Local validation uses Omarchy 4.0.4, Foot 1.28.0, and Starship 1.26.0. Shell
sections were also staged through Omarchy's own template generator, and the
theme was applied and reviewed live on an AMD Radeon RX 7900 XTX. Ghostty was not
installed for this review: the Ghostty profile and `--haze` are covered here by
the shader compile test, and by `--check` wherever Ghostty is installed.

## License

MIT. The stills are original generations. The unlock mark is the Omarchy
geometry recolored to sodium amber. An unofficial fan theme, not affiliated with
the film or its rights holders.
