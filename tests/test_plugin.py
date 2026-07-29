from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "dating-show-screenshot"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "make-dating-show-screenshot"
RENDERER = SKILL_ROOT / "scripts" / "render_dating_show.py"


def load_renderer_module():
    specification = importlib.util.spec_from_file_location(
        "dating_show_renderer",
        RENDERER,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("Could not load renderer module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_json(relative_path: str) -> dict:
    return json.loads((SKILL_ROOT / relative_path).read_text(encoding="utf-8"))


class PluginTests(unittest.TestCase):
    def test_manifest_and_marketplace_are_consistent(self) -> None:
        plugin = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(plugin["name"], "dating-show-screenshot")
        self.assertEqual(plugin["version"], "1.3.9")
        self.assertEqual(plugin["skills"], "./skills/")
        self.assertEqual(marketplace["plugins"][0]["name"], plugin["name"])
        for asset in [
            plugin["interface"]["composerIcon"],
            plugin["interface"]["logo"],
            *plugin["interface"]["screenshots"],
        ]:
            self.assertTrue((PLUGIN_ROOT / asset).is_file())

    def test_station_presets_use_exactly_one_bug_mode(self) -> None:
        presets = read_json("references/station-presets.json")["presets"]
        self.assertEqual(len(presets), 10)
        self.assertEqual({preset["bug_mode"] for preset in presets}, {"map", "icon"})
        for preset in presets:
            self.assertNotIn("station_asset", preset)
            self.assertNotIn("map_asset", preset)
            self.assertNotIn("icon_asset", preset)
            self.assertTrue(preset["bug_asset"].endswith(".png"))
            folder = "maps" if preset["bug_mode"] == "map" else "station-icons"
            self.assertTrue(
                (SKILL_ROOT / "assets" / folder / preset["bug_asset"]).is_file()
            )

    def test_generated_assets_have_real_transparency(self) -> None:
        for folder, minimum_count in [
            ("station-icons", 5),
            ("flourishes", 6),
            ("sponsors", 8),
            ("maps", 10),
        ]:
            assets = sorted((SKILL_ROOT / "assets" / folder).glob("*.png"))
            self.assertGreaterEqual(len(assets), minimum_count)
            for asset in assets:
                with Image.open(asset) as image:
                    self.assertEqual(image.mode, "RGBA")
                    alpha = image.getchannel("A")
                    minimum, maximum = alpha.getextrema()
                    self.assertEqual(minimum, 0)
                    self.assertGreaterEqual(maximum, 200)
                    self.assertEqual(alpha.getpixel((0, 0)), 0)

    def test_role_fonts_are_bundled(self) -> None:
        font_dir = SKILL_ROOT / "assets" / "fonts"
        for filename in [
            "NotoSansSC-Regular.ttf",
            "NotoSansSC-SemiBold.ttf",
            "NotoSerifSC-Regular.ttf",
            "NotoSerifSC-SemiBold.ttf",
            "OFL.txt",
        ]:
            path = font_dir / filename
            self.assertTrue(path.is_file(), filename)
            self.assertGreater(path.stat().st_size, 1_000)

    def test_like_icon_is_white_with_real_transparency(self) -> None:
        path = SKILL_ROOT / "assets" / "ui" / "like-white.png"
        self.assertTrue(path.is_file())
        with Image.open(path) as image:
            self.assertEqual(image.mode, "RGBA")
            alpha = image.getchannel("A")
            self.assertEqual(alpha.getpixel((0, 0)), 0)
            self.assertEqual(alpha.getextrema(), (0, 255))
            opaque = image.getpixel((image.width // 2, image.height // 2))
            self.assertEqual(opaque[:3], (255, 255, 255))

    def test_no_real_show_reference_material_remains(self) -> None:
        forbidden_names = {
            "station-dongbei-reference.png",
            "station-jilin-reference.png",
            "station-shuangyashan-reference.png",
            "lower-third-reference.jpg",
            "bullet-comments-reference.jpg",
        }
        names = {path.name for path in SKILL_ROOT.rglob("*") if path.is_file()}
        self.assertTrue(names.isdisjoint(forbidden_names))
        self.assertFalse(
            any("reference" in name.lower() and name != "icon-sources.md" for name in names)
        )
        self.assertFalse((SKILL_ROOT / "assets" / "stations").exists())
        self.assertFalse((SKILL_ROOT / "assets" / "icons").exists())
        self.assertNotIn("参考截图原句", read_json("references/dialogues.json"))

    def test_presets_reference_flourishes_and_station_sponsors(self) -> None:
        dialogue_categories = set(read_json("references/dialogues.json"))
        dialogue_categories -= {"观察室点评", "弹幕"}
        flourishes = read_json("references/flourish-presets.json")
        sponsors = read_json("references/sponsor-presets.json")
        stations = read_json("references/station-presets.json")["presets"]
        self.assertLessEqual(dialogue_categories, set(flourishes["categories"]))
        for filename in set(flourishes["categories"].values()) | {flourishes["default"]}:
            self.assertTrue(
                (SKILL_ROOT / "assets" / "flourishes" / filename).is_file()
            )
        self.assertEqual(
            {station["id"] for station in stations},
            set(sponsors["stations"]),
        )
        for preset in [sponsors["default"], *sponsors["stations"].values()]:
            self.assertTrue(
                (SKILL_ROOT / "assets" / "sponsors" / preset["asset"]).is_file()
            )
            self.assertTrue(preset["brand"])
            self.assertEqual(preset["designation"], "独家冠名")

    def run_renderer(
        self,
        output_dir: Path,
        preset: str,
        category: str,
        *extra: str,
    ) -> Path:
        output = output_dir / f"{preset}-{category}.png"
        completed = subprocess.run(
            [
                sys.executable,
                str(RENDERER),
                "--input",
                str(REPO_ROOT / "examples" / "demo-input.png"),
                "--output",
                str(output),
                "--station-preset",
                preset,
                "--category",
                category,
                "--width",
                "640",
                "--height",
                "360",
                "--seed",
                "9",
                *extra,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn(f"preset={preset}", completed.stdout)
        return output

    def test_renderer_smoke_icon_and_map_modes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            icon_output = self.run_renderer(
                output_dir,
                "xihu",
                "做饭吃饭",
                "--comments",
                "2",
            )
            map_output = self.run_renderer(
                output_dir,
                "shuangyashan",
                "合住日常",
            )
            for output in [icon_output, map_output]:
                with Image.open(output) as image:
                    self.assertEqual(image.size, (640, 360))
                    self.assertEqual(image.mode, "RGBA")
                    self.assertEqual(image.getbbox(), (0, 0, 640, 360))

    def test_renderer_supports_diy_and_no_sponsor(self) -> None:
        custom_bug = SKILL_ROOT / "assets" / "station-icons" / "moon-bay.png"
        custom_flourish = SKILL_ROOT / "assets" / "flourishes" / "between-us.png"
        with tempfile.TemporaryDirectory() as temporary:
            output = self.run_renderer(
                Path(temporary),
                "mudanjiang",
                "朋友闲聊",
                "--station-bug",
                str(custom_bug),
                "--flourish",
                str(custom_flourish),
                "--line",
                "杯子先放这儿，等会儿一起收。",
                "--no-sponsor",
            )
            self.assertTrue(output.is_file())

    def test_renderer_supports_reference_layout_variants(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = self.run_renderer(
                Path(temporary),
                "lijiang",
                "做饭吃饭",
                "--presentation",
                "photo-card",
                "--name-tag",
                "阿岚@0.34,0.29",
                "--name-tag",
                "小满@0.62,0.25",
                "--comments",
                "3",
            )
            self.assertTrue(output.is_file())

    def test_renderer_supports_role_specific_font_overrides(self) -> None:
        fonts = SKILL_ROOT / "assets" / "fonts"
        with tempfile.TemporaryDirectory() as temporary:
            output = self.run_renderer(
                Path(temporary),
                "lijiang",
                "做饭吃饭",
                "--station-font",
                str(fonts / "NotoSansSC-SemiBold.ttf"),
                "--caption-font",
                str(fonts / "NotoSerifSC-Regular.ttf"),
                "--sponsor-font",
                str(fonts / "NotoSerifSC-SemiBold.ttf"),
            )
            self.assertTrue(output.is_file())

    def test_first_generation_lower_third_stays_wide_and_above_line(self) -> None:
        renderer = load_renderer_module()
        background = (118, 118, 118, 255)
        image = Image.new("RGBA", (1000, 500), background)
        renderer.draw_lower_third(
            image,
            SKILL_ROOT / "assets" / "fonts" / "NotoSerifSC-SemiBold.ttf",
            "嘉宾",
            "今天聊点日常。",
            (185, 41, 80, 235),
            SKILL_ROOT / "assets" / "flourishes" / "little-moments.png",
        )
        underline_y = int(500 * 0.890) + int(500 * 0.018)
        upper = image.getpixel((500, int(500 * 0.815)))
        lower = image.getpixel((500, underline_y - 5))
        upper_change = sum(abs(upper[index] - background[index]) for index in range(3))
        lower_change = sum(abs(lower[index] - background[index]) for index in range(3))
        self.assertTrue(
            any(
                image.getpixel((x, underline_y)) != background
                for x in range(image.width)
            )
        )
        line_xs = [
            x
            for x in range(image.width)
            if image.getpixel((x, underline_y)) != background
        ]
        gradient_y = underline_y - 5
        self.assertNotEqual(
            image.getpixel(((min(line_xs) + max(line_xs)) // 2, gradient_y)),
            background,
        )
        if min(line_xs) > 1:
            self.assertEqual(
                image.getpixel((min(line_xs) - 2, gradient_y)),
                background,
            )
        if max(line_xs) < image.width - 2:
            self.assertEqual(
                image.getpixel((max(line_xs) + 2, gradient_y)),
                background,
            )
        self.assertGreater(lower_change, upper_change)
        self.assertEqual(image.getpixel((500, underline_y + 5)), background)

    def test_lower_third_text_group_is_centered(self) -> None:
        renderer = load_renderer_module()
        image = Image.new("RGBA", (1000, 500), (70, 70, 70, 255))
        renderer.draw_lower_third(
            image,
            SKILL_ROOT / "assets" / "fonts" / "NotoSerifSC-SemiBold.ttf",
            "嘉宾",
            "你们先走，我把这一张拍完。",
            (185, 41, 80, 235),
            SKILL_ROOT / "assets" / "flourishes" / "wander-together.png",
        )
        xs = [
            x
            for y in range(int(500 * 0.845), int(500 * 0.890))
            for x in range(1000)
            if min(image.getpixel((x, y))[:3]) > 220
        ]
        self.assertTrue(xs)
        actual_center = (min(xs) + max(xs)) / 2
        safe_center = ((0.125 + 0.820) / 2) * 1000
        self.assertAlmostEqual(actual_center, safe_center, delta=12)
        underline_y = int(500 * 0.890) + int(500 * 0.018)
        line_xs = [
            x
            for x in range(1000)
            if image.getpixel((x, underline_y)) != (70, 70, 70, 255)
        ]
        self.assertTrue(line_xs)
        self.assertLessEqual(min(line_xs), min(xs))
        self.assertGreaterEqual(max(line_xs), max(xs))
        self.assertLessEqual(min(xs) - min(line_xs), 20)
        self.assertLessEqual(max(line_xs) - max(xs), 35)

    def test_native_output_preserves_size_color_profile_and_clean_pixels(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            input_path = temporary_path / "native-input.png"
            output_path = temporary_path / "native-output.png"
            source = Image.new("RGB", (800, 450), (31, 79, 127))
            source.save(input_path, icc_profile=b"test-icc-profile")
            subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                    "--station-preset",
                    "lijiang",
                    "--category",
                    "出游行动",
                    "--line",
                    "你们先走，我把这一张拍完。",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            with Image.open(output_path) as output:
                self.assertEqual(output.size, source.size)
                self.assertEqual(output.info.get("icc_profile"), b"test-icc-profile")
                self.assertEqual(output.convert("RGB").getpixel((500, 220)), (31, 79, 127))

    def test_renderer_supports_exact_comments(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = self.run_renderer(
                Path(temporary),
                "lijiang",
                "做饭吃饭",
                "--comment",
                "冰棍要化了",
                "--comment",
                "她真的很会拍",
            )
            self.assertTrue(output.is_file())

    def test_renderer_supports_danmaku_density_and_protect_zones(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = self.run_renderer(
                Path(temporary),
                "erhai",
                "采访回应",
                "--danmaku-density",
                "medium",
                "--protect-zone",
                "0.36,0.02,0.64,0.34",
            )
            self.assertTrue(output.is_file())

    def test_renderer_supports_subject_mask(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            with Image.open(REPO_ROOT / "examples" / "demo-input.png") as input_image:
                input_size = input_image.size
            mask = Image.new("L", input_size, 0)
            mask.paste(
                255,
                (
                    input_size[0] // 3,
                    0,
                    input_size[0] * 2 // 3,
                    input_size[1],
                ),
            )
            mask_path = temporary_path / "subject-mask.png"
            mask.save(mask_path)
            output = self.run_renderer(
                temporary_path,
                "erhai",
                "采访回应",
                "--danmaku-density",
                "full",
                "--subject-mask",
                str(mask_path),
            )
            self.assertTrue(output.is_file())

    def test_public_demo_is_synthetic_and_complete(self) -> None:
        input_image = REPO_ROOT / "examples" / "demo-input.png"
        output_image = REPO_ROOT / "examples" / "demo-output.png"
        photo_card_image = REPO_ROOT / "examples" / "demo-photo-card.png"
        self.assertTrue(input_image.is_file())
        self.assertTrue(output_image.is_file())
        self.assertTrue(photo_card_image.is_file())
        for path in [output_image, photo_card_image]:
            with Image.open(path) as image:
                self.assertEqual(image.size, (1920, 1080))


if __name__ == "__main__":
    unittest.main()
