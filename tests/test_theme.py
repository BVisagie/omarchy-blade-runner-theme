"""Regression checks for wallpapers, readability, shell sections, and launcher argv."""
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

HEX = re.compile(r"^#[0-9A-F]{6}$")
# Every section in Omarchy 4's generated shell.toml.
SHELL_SECTIONS = {"bar", "hyprland", "controls", "spacing", "font", "popups", "tooltip",
                  "notifications", "launcher", "menu", "polkit", "lock", "image-picker"}


def luminance(color):
    values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
    return sum(v * w for v, w in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(a, b):
    lo, hi = sorted((luminance(a), luminance(b)))
    return (hi + 0.05) / (lo + 0.05)


def delta_e(a, b):
    """CIE76 colour difference in CIELAB (D65)."""
    def lab(color):
        rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        r, g, b_ = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
        xyz = ((r * .4124 + g * .3576 + b_ * .1805) / .95047, r * .2126 + g * .7152 + b_ * .0722,
               (r * .0193 + g * .1192 + b_ * .9505) / 1.08883)
        fx, fy, fz = [t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116 for t in xyz]
        return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)
    return sum((p - q) ** 2 for p, q in zip(lab(a), lab(b))) ** 0.5


class ThemeTests(unittest.TestCase):
    def test_shipped_wallpapers_are_valid_4k_images(self):
        wallpapers = list((ROOT / "backgrounds").glob("*.jpg"))
        self.assertTrue(wallpapers)
        for path in wallpapers:
            with self.subTest(wallpaper=path.name), Image.open(path) as image:
                self.assertEqual(image.size, (3840, 2160))
                self.assertEqual(image.mode, "RGB")
                image.verify()

    @unittest.skipUnless(shutil.which("glslangValidator"), "glslangValidator is not installed")
    def test_haze_shader_compiles(self):
        with tempfile.TemporaryDirectory() as directory:
            shader = Path(directory) / "haze.frag"
            shader.write_text(
                "#version 330 core\nuniform vec3 iResolution;\nuniform sampler2D iChannel0;\nout vec4 color;\n"
                + (ROOT / "extras/haze.glsl").read_text()
                + "\nvoid main() { mainImage(color, gl_FragCoord.xy); }\n")
            result = subprocess.run(["glslangValidator", "-S", "frag", str(shader)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_text_contrast_and_ansi_aliases(self):
        colors = tomllib.loads((ROOT / "colors.toml").read_text())
        for bg in ("background", "lighter_background"):
            for key in ("foreground", "muted", "accent", "red", "yellow", "green", "cyan", "blue", "magenta"):
                self.assertGreaterEqual(contrast(colors[key], colors[bg]), 4.5, (key, bg))
        self.assertGreaterEqual(contrast(colors["selection_foreground"], colors["selection_background"]), 4.5)
        roles = ["background", "red", "green", "yellow", "blue", "magenta", "cyan", "foreground",
                 "muted", "bright_red", "bright_green", "bright_yellow", "bright_blue", "bright_magenta",
                 "bright_cyan", "bright_foreground"]
        for i, role in enumerate(roles):
            self.assertEqual(colors[f"color{i}"], colors[role])

    def test_syntax_colors_stay_off_muted_comments(self):
        colors = tomllib.loads((ROOT / "colors.toml").read_text())
        for hue in ("red", "yellow", "green", "cyan", "blue", "magenta"):
            for key in (hue, f"bright_{hue}"):
                with self.subTest(color=key):
                    self.assertGreaterEqual(delta_e(colors[key], colors["muted"]), 20)

    def test_shell_sections_are_valid_and_colors_stay_in_palette(self):
        colors = tomllib.loads((ROOT / "colors.toml").read_text())
        for path in ROOT.glob("shell.*.toml"):
            self.assertIn(path.name[len("shell."):-len(".toml")], SHELL_SECTIONS, path.name)
            values = tomllib.loads(path.read_text())
            self.assertFalse(any(isinstance(value, dict) for value in values.values()), path.name)
            for key, value in values.items():
                if isinstance(value, str) and value.startswith("#"):
                    self.assertIn(value, colors.values(), (path.name, key))
        lock = tomllib.loads((ROOT / "shell.lock.toml").read_text())
        self.assertGreaterEqual(contrast(lock["placeholder"], lock["background"]), 4.5)

    def test_hex_values_are_uppercase_six_digit(self):
        files = [ROOT / "colors.toml", *ROOT.glob("shell.*.toml")]
        for path in files:
            for key, value in tomllib.loads(path.read_text()).items():
                if isinstance(value, str) and value.startswith("#"):
                    self.assertRegex(value, HEX, (path.name, key))

    def test_selected_rows_stay_readable(self):
        for path in ROOT.glob("shell.*.toml"):
            values = tomllib.loads(path.read_text())
            if "selected-text" in values and "selected-background" in values:
                with self.subTest(section=path.name):
                    self.assertGreaterEqual(contrast(values["selected-text"], values["selected-background"]), 4.5)

    def test_launcher_preserves_command_arguments_and_scopes_prompt(self):
        with tempfile.TemporaryDirectory(prefix="blade runner test ") as directory:
            root = Path(directory)
            for terminal in ("ghostty", "foot"):
                stub = root / terminal
                stub.write_text(f"#!{sys.executable}\nimport os,sys,json\nprint(json.dumps([sys.argv[1:],os.environ.get('STARSHIP_CONFIG')]))\n")
                stub.chmod(0o755)
                command = ["printf", "%s", "hello space", "$(do-not-execute)"]
                env = dict(os.environ, PATH=f"{root}:{os.environ['PATH']}")
                result = subprocess.run([sys.executable, str(ROOT / "scripts/blade-runner-terminal"),
                                         "--terminal", terminal, "--", *command],
                                        env=env, capture_output=True, text=True, check=True)
                argv, prompt = json.loads(result.stdout)
                self.assertEqual(argv[-len(command):], command)
                self.assertEqual(prompt, str(ROOT / "extras/starship.toml"))

    def test_greeting_is_plain_when_not_a_terminal(self):
        result = subprocess.run([str(ROOT / "scripts/blade-runner-greeting")],
                                capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout, "Los Angeles\nNovember, 2019\n")

    def test_invalid_launcher_options_fail_before_launch(self):
        for argv in (["--font-size", "100"], ["--font-size", "nan"], ["--haze", "--terminal", "foot"]):
            result = subprocess.run([sys.executable, str(ROOT / "scripts/blade-runner-terminal"), *argv],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, (argv, result.stderr))


if __name__ == "__main__":
    unittest.main()
