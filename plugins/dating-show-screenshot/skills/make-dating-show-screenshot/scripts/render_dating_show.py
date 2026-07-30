#!/usr/bin/env python3
"""Deterministically add a fictional Chinese lifestyle-show broadcast package."""

from __future__ import annotations

import argparse
import json
import math
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DIALOGUES = ROOT / "references" / "dialogues.json"
STATION_PRESETS = ROOT / "references" / "station-presets.json"
FLOURISH_PRESETS = ROOT / "references" / "flourish-presets.json"
SPONSOR_PRESETS = ROOT / "references" / "sponsor-presets.json"
MAP_ASSETS = ROOT / "assets" / "maps"
STATION_ICON_ASSETS = ROOT / "assets" / "station-icons"
FLOURISH_ASSETS = ROOT / "assets" / "flourishes"
SPONSOR_ASSETS = ROOT / "assets" / "sponsors"
UI_ASSETS = ROOT / "assets" / "ui"
LIKE_ICON_ASSET = UI_ASSETS / "like-white.png"
CAST_NAME_CURVE_ASSET = UI_ASSETS / "cast-name-curve.png"
BUNDLED_FONT = ROOT / "assets" / "fonts" / "NotoSansSC-Regular.ttf"
BUNDLED_BOLD_FONT = ROOT / "assets" / "fonts" / "NotoSansSC-SemiBold.ttf"
BUNDLED_DIALOGUE_FONT = ROOT / "assets" / "fonts" / "LXGWWenKai-Regular.ttf"
BUNDLED_CAPTION_FONT = ROOT / "assets" / "fonts" / "NotoSerifSC-Regular.ttf"
BUNDLED_CAPTION_BOLD_FONT = ROOT / "assets" / "fonts" / "NotoSerifSC-SemiBold.ttf"
BUNDLED_NAME_FONT = ROOT / "assets" / "fonts" / "BaiLuTongTong-Regular.ttf"

DANMAKU_COUNTS = {
    "none": 0,
    "light": 3,
    "medium": 7,
    "full": 14,
}

DEFAULT_PRESET_BY_CATEGORY = {
    "合住日常": "mudanjiang",
    "游戏互动": "dunhuang",
    "做饭吃饭": "xihu",
    "出游行动": "lijiang",
    "朋友闲聊": "erhai",
    "轻松吐槽": "shuangyashan",
    "采访回应": "mudanjiang",
    "暧昧试探": "shuangyashan",
    "嘴硬逗趣": "yalongwan",
    "认真拉扯": "mohe",
    "心动回应": "shuangyashan",
}
UNDERLINE_BY_CATEGORY: dict[str, tuple[int, int, int, int]] = {}
LOCKUP_LABEL_Y = {
    "snack-lockup.png": 0.84,
    "noodle-bowl-lockup.png": 0.84,
    "fish-platter-lockup.png": 0.84,
    "dairy-snack-lockup.png": 0.84,
    "dessert-bowl-lockup.png": 0.88,
    "camel-milk-lockup.png": 0.88,
}
COMMON_CJK_FONTS = [
    str(BUNDLED_FONT),
    "/System/Library/Fonts/PingFang.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/source-han-sans/SourceHanSansSC-Regular.otf",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--line")
    parser.add_argument("--category", default="合住日常")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--speaker", default="嘉宾")
    parser.add_argument("--station")
    parser.add_argument("--station-preset")
    parser.add_argument("--station-bug", type=Path)
    parser.add_argument("--station-icon", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--badge", default="独播")
    parser.add_argument("--flourish", type=Path)
    parser.add_argument("--sponsor", help="Override the fictional sponsor brand name.")
    parser.add_argument("--sponsor-tagline")
    parser.add_argument("--sponsor-designation")
    parser.add_argument(
        "--sponsor-style",
        help="Bundled sponsor asset stem, for example noodle-bowl-lockup.",
    )
    parser.add_argument(
        "--sponsor-asset",
        type=Path,
        help="DIY transparent sponsor lockup. Overrides --sponsor-style.",
    )
    parser.add_argument("--no-sponsor", action="store_true")
    parser.add_argument(
        "--comments",
        type=int,
        default=0,
        help="Legacy exact count for automatic comments (0–24).",
    )
    parser.add_argument(
        "--danmaku-density",
        choices=list(DANMAKU_COUNTS),
        help="Preset density: none=0, light=3, medium=7, full=14.",
    )
    parser.add_argument(
        "--comment",
        action="append",
        default=[],
        help=(
            "Add an exact floating comment; repeat 1–24 times. "
            "Overrides --comments and --danmaku-density."
        ),
    )
    parser.add_argument(
        "--protect-zone",
        action="append",
        default=[],
        metavar="X1,Y1,X2,Y2",
        help=(
            "Normalized important-subject rectangle avoided by comments; "
            "repeat for multiple faces or subjects."
        ),
    )
    parser.add_argument(
        "--subject-mask",
        type=Path,
        help=(
            "Optional grayscale/alpha mask aligned to the input: white subject "
            "pixels are restored over comments so danmaku passes behind people."
        ),
    )
    parser.add_argument(
        "--presentation",
        choices=["standard", "photo-card"],
        default="standard",
        help="Use photo-card to recreate the tilted white-frame reference layout.",
    )
    parser.add_argument(
        "--name-tag",
        action="append",
        default=[],
        metavar="TEXT@X,Y",
        help="Add a cast name at normalized coordinates; repeat as needed.",
    )
    parser.add_argument(
        "--font",
        type=Path,
        help="Global font override kept for backward compatibility.",
    )
    parser.add_argument(
        "--station-font",
        type=Path,
        help="Override the station-name, badge, and floating-comment font.",
    )
    parser.add_argument(
        "--caption-font",
        type=Path,
        help="Override the lower-third dialogue and speaker font.",
    )
    parser.add_argument(
        "--name-font",
        type=Path,
        help="Override the cast-name handwriting font.",
    )
    parser.add_argument(
        "--name-curve",
        type=Path,
        help="Override the transparent pink brush curve beneath cast names.",
    )
    parser.add_argument(
        "--sponsor-font",
        type=Path,
        help="Override the sponsor lockup font.",
    )
    parser.add_argument(
        "--width",
        type=int,
        help="Optional output width. Omit with --height to preserve native resolution.",
    )
    parser.add_argument(
        "--height",
        type=int,
        help="Optional output height. Omit with --width to preserve native resolution.",
    )
    return parser.parse_args()


def has_cjk(text: str) -> bool:
    return any("\u3400" <= character <= "\u9fff" for character in text)


def resolve_font(explicit: Path | None, text: str) -> Path:
    if explicit:
        if not explicit.exists():
            raise SystemExit(f"Font not found: {explicit}")
        return explicit
    for candidate in COMMON_CJK_FONTS:
        path = Path(candidate)
        if path.exists():
            return path
    if not has_cjk(text):
        try:
            result = subprocess.run(
                ["fc-match", "-f", "%{file}", "DejaVu Sans"],
                check=True,
                capture_output=True,
                text=True,
            )
            path = Path(result.stdout.strip())
            if path.exists():
                return path
        except Exception:
            pass
    raise SystemExit(
        "No CJK font found. Pass --font with PingFang, Microsoft YaHei, "
        "Source Han Sans SC, Noto Sans CJK SC, or WenQuanYi Zen Hei."
    )


def resolve_role_font(
    role_override: Path | None,
    global_override: Path | None,
    bundled_default: Path,
    text: str,
) -> Path:
    """Resolve a role-specific font while preserving the legacy --font override."""
    explicit = role_override or global_override
    if explicit:
        return resolve_font(explicit, text)
    if bundled_default.exists():
        return bundled_default
    return resolve_font(None, text)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(
        image,
        size,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )


def native_broadcast_size(image: Image.Image) -> tuple[int, int]:
    """Return a 16:9 canvas that never downsizes the source photo."""
    target_ratio = 16 / 9
    source_ratio = image.width / image.height
    if abs(source_ratio - target_ratio) < 0.015:
        return image.size
    if source_ratio < target_ratio:
        return (math.ceil(image.height * target_ratio), image.height)
    return (image.width, math.ceil(image.width / target_ratio))


def broadcast_canvas(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Return a 16:9 canvas without cropping a non-16:9 source."""
    source_ratio = image.width / image.height
    target_ratio = size[0] / size[1]
    if abs(source_ratio - target_ratio) < 0.015:
        if image.size == size:
            return image.copy()
        return cover(image, size)

    background = cover(image, size).filter(
        ImageFilter.GaussianBlur(radius=max(18, round(size[1] * 0.035)))
    )
    background = ImageEnhance.Brightness(background).enhance(0.70).convert("RGBA")
    foreground = ImageOps.contain(
        image,
        size,
        method=Image.Resampling.LANCZOS,
    ).convert("RGBA")
    x = (size[0] - foreground.width) // 2
    y = (size[1] - foreground.height) // 2

    shadow = Image.new("RGBA", size)
    shadow_patch = Image.new("RGBA", foreground.size, (0, 0, 0, 70))
    shadow.alpha_composite(shadow_patch, (x + 8, y + 8))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=12))
    background.alpha_composite(shadow)
    background.alpha_composite(foreground, (x, y))
    return background.convert("RGB")


def broadcast_mask(mask: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Align an input-space subject mask with the standard broadcast canvas."""
    mask = ImageOps.exif_transpose(mask).convert("L")
    source_ratio = mask.width / mask.height
    target_ratio = size[0] / size[1]
    if abs(source_ratio - target_ratio) < 0.015:
        return cover(mask, size).convert("L")

    foreground = ImageOps.contain(
        mask,
        size,
        method=Image.Resampling.LANCZOS,
    )
    canvas = Image.new("L", size, 0)
    canvas.paste(
        foreground,
        ((size[0] - foreground.width) // 2, (size[1] - foreground.height) // 2),
    )
    return canvas


def photo_card_canvas(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Recreate the tilted white-border still used by the first references."""
    width, height = size
    background = cover(image, size).filter(
        ImageFilter.GaussianBlur(radius=max(20, round(height * 0.045)))
    )
    background = ImageEnhance.Brightness(background).enhance(0.48).convert("RGBA")

    contained = ImageOps.contain(
        image,
        (int(width * 0.73), int(height * 0.84)),
        method=Image.Resampling.LANCZOS,
    ).convert("RGBA")
    border = max(10, int(height * 0.016))
    card = ImageOps.expand(contained, border=border, fill=(255, 255, 255, 255))
    card = card.rotate(
        -5.0,
        resample=Image.Resampling.BICUBIC,
        expand=True,
        fillcolor=(0, 0, 0, 0),
    )
    x = (width - card.width) // 2 + int(width * 0.018)
    y = (height - card.height) // 2 + int(height * 0.035)

    shadow = Image.new("RGBA", size)
    shadow_mask = Image.new("RGBA", card.size, (0, 0, 0, 115))
    shadow_mask.putalpha(card.getchannel("A"))
    shadow.alpha_composite(shadow_mask, (x + 14, y + 18))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(8, int(height * 0.018))))
    background.alpha_composite(shadow)
    background.alpha_composite(card, (x, y))
    return background.convert("RGB")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    path: Path,
    max_width: int,
    start: int,
    floor: int,
) -> ImageFont.FreeTypeFont:
    for size in range(start, floor - 1, -2):
        candidate = font(path, size)
        if draw.textbbox((0, 0), text, font=candidate, stroke_width=1)[2] <= max_width:
            return candidate
    return font(path, floor)


def centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    selected_font: ImageFont.FreeTypeFont,
    *,
    fill: tuple[int, ...] = (255, 255, 255, 255),
    stroke_width: int = 2,
    stroke_fill: tuple[int, ...] = (25, 25, 25, 180),
) -> None:
    draw.text(
        xy,
        text,
        font=selected_font,
        anchor="mm",
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )


def trimmed_asset(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    return image.crop(bbox) if bbox else image


def resolve_station_asset(preset: dict, override: Path | None) -> Path:
    if override:
        if not override.exists():
            raise SystemExit(f"Station bug not found: {override}")
        return override
    mode = preset["bug_mode"]
    if mode not in {"map", "icon"}:
        raise SystemExit(f"Invalid station bug mode: {mode}")
    root = MAP_ASSETS if mode == "map" else STATION_ICON_ASSETS
    path = root / preset["bug_asset"]
    if not path.exists():
        raise SystemExit(f"Station bug asset not found: {path}")
    return path


def draw_station(
    base: Image.Image,
    font_path: Path,
    station: str,
    badge: str,
    station_bug: Path,
) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size)
    x, y = int(width * 0.052), int(height * 0.058)
    max_size = (int(width * 0.052), int(height * 0.064))

    emblem = trimmed_asset(station_bug)
    emblem.thumbnail(max_size, Image.Resampling.LANCZOS)
    emblem_x = x
    emblem_y = y + (max_size[1] - emblem.height) // 2
    shadow = Image.new("RGBA", emblem.size, (0, 0, 0, 0))
    shadow.putalpha(emblem.getchannel("A").filter(ImageFilter.GaussianBlur(3)))
    dark = Image.new("RGBA", emblem.size, (5, 10, 18, 130))
    dark.putalpha(shadow.getchannel("A").point(lambda value: min(130, value)))
    layer.alpha_composite(dark, (emblem_x + 3, emblem_y + 3))
    layer.alpha_composite(emblem, (emblem_x, emblem_y))

    draw = ImageDraw.Draw(layer)
    station_font = fit_font(
        draw,
        station,
        font_path,
        int(width * 0.15),
        int(height * 0.047),
        int(height * 0.034),
    )
    text_x = emblem_x + emblem.width + int(width * 0.010)
    text_y = y + max_size[1] // 2
    draw.text(
        (text_x + 2, text_y + 2),
        station,
        font=station_font,
        anchor="lm",
        fill=(10, 10, 10, 135),
    )
    draw.text(
        (text_x, text_y),
        station,
        font=station_font,
        anchor="lm",
        fill="white",
        stroke_width=1,
        stroke_fill=(20, 20, 20, 135),
    )
    bounds = draw.textbbox(
        (text_x, text_y),
        station,
        font=station_font,
        anchor="lm",
        stroke_width=2,
    )
    badge_x = bounds[2] + int(width * 0.010)
    badge_y = y + int(max_size[1] * 0.12)
    badge_font = font(font_path, max(16, int(height * 0.021)))
    badge_bounds = draw.textbbox((0, 0), badge, font=badge_font)
    badge_width = badge_bounds[2] - badge_bounds[0] + int(width * 0.014)
    badge_height = badge_bounds[3] - badge_bounds[1] + int(height * 0.012)
    draw.rounded_rectangle(
        (badge_x, badge_y, badge_x + badge_width, badge_y + badge_height),
        radius=6,
        fill=(255, 255, 255, 245),
    )
    centered_text(
        draw,
        (badge_x + badge_width // 2, badge_y + badge_height // 2 - 1),
        badge,
        badge_font,
        fill=(32, 32, 32, 255),
        stroke_width=0,
    )
    base.alpha_composite(layer)


def draw_lower_third(
    base: Image.Image,
    font_path: Path,
    speaker: str,
    line: str,
    underline: tuple[int, int, int, int],
    flourish_path: Path,
) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size)
    draw = ImageDraw.Draw(layer)
    baseline = int(height * 0.890)
    underline_y = baseline + int(height * 0.018)
    safe_left = int(width * 0.125)
    safe_right = int(width * 0.820)
    safe_width = safe_right - safe_left
    text_y = baseline - int(height * 0.025)
    speaker_font = fit_font(
        draw,
        speaker,
        font_path,
        int(width * 0.14),
        int(height * 0.052),
        int(height * 0.038),
    )
    speaker_width = round(draw.textlength(speaker, font=speaker_font))
    slash_width = round(draw.textlength("/", font=speaker_font))
    group_gap = int(width * 0.018)
    max_line_width = max(
        int(width * 0.28),
        safe_width - speaker_width - slash_width - group_gap * 2,
    )
    line_font = fit_font(
        draw,
        line,
        font_path,
        max_line_width,
        int(height * 0.052),
        int(height * 0.038),
    )
    line_width = round(draw.textlength(line, font=line_font))
    group_width = (
        speaker_width
        + group_gap
        + slash_width
        + group_gap
        + line_width
    )
    group_left = round((safe_left + safe_right - group_width) / 2)
    group_left = max(safe_left, min(group_left, safe_right - group_width))
    underline_padding = int(width * 0.012)
    underline_left = max(safe_left, group_left - underline_padding)
    underline_right = min(
        safe_right,
        group_left + group_width + underline_padding,
    )

    # Match the first-generation result: one broad, quiet pink-gray airbrush
    # stroke whose horizontal span follows the measured caption underline.
    # It should read as broadcast atmosphere, not as a colored panel or a stack
    # of visibly separate glow bands.
    panel_x = underline_left
    panel_y = int(height * 0.805)
    panel_width = max(1, underline_right - underline_left + 1)
    panel_height = underline_y - panel_y
    blur_radius = max(7, int(height * 0.012))
    # Extend the working mask below the visible crop so Gaussian blur does not
    # weaken the color at the underline.  Only the area above the line is
    # composited, so the lower third remains completely transparent below it.
    work_height = panel_height + blur_radius * 2
    work_size = (panel_width, work_height)
    panel = Image.new("RGBA", work_size)
    gray_mask = Image.new("L", work_size)
    rose_mask = Image.new("L", work_size)
    gray_pixels = gray_mask.load()
    rose_pixels = rose_mask.load()
    for y in range(work_height):
        progress_y = min(1.0, y / max(1, panel_height - 1))
        gray_vertical = progress_y * progress_y * (3 - 2 * progress_y)
        rose_vertical = progress_y ** 2.7
        for x in range(panel_width):
            edge_distance = min(x, panel_width - 1 - x)
            edge_progress = min(1.0, edge_distance / max(1, panel_width * 0.10))
            horizontal = edge_progress * edge_progress * (3 - 2 * edge_progress)
            gray_pixels[x, y] = round(30 * horizontal * gray_vertical)
            rose_pixels[x, y] = round(72 * horizontal * rose_vertical)
    gray_layer = Image.new("RGBA", panel.size, (96, 99, 108, 255))
    gray_layer.putalpha(gray_mask)
    panel.alpha_composite(gray_layer)
    rose_layer = Image.new("RGBA", panel.size, (151, 55, 85, 255))
    rose_layer.putalpha(rose_mask)
    panel.alpha_composite(rose_layer)
    panel = panel.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    panel = panel.crop((0, 0, panel_width, panel_height))
    haze = Image.new("RGBA", base.size)
    haze.alpha_composite(panel, (panel_x, panel_y))
    base.alpha_composite(haze)

    flourish = trimmed_asset(flourish_path)
    flourish.thumbnail(
        (int(width * 0.094), int(height * 0.064)),
        Image.Resampling.LANCZOS,
    )
    flourish.putalpha(
        flourish.getchannel("A").point(lambda value: round(value * 0.72))
    )
    flourish = flourish.rotate(
        -4,
        resample=Image.Resampling.BICUBIC,
        expand=True,
        fillcolor=(0, 0, 0, 0),
    )
    layer.alpha_composite(
        flourish,
        (
            group_left - int(width * 0.006),
            text_y - int(height * 0.061),
        ),
    )
    draw.text(
        (group_left, text_y),
        speaker,
        font=speaker_font,
        anchor="lm",
        fill="white",
        stroke_width=1,
        stroke_fill=(25, 25, 25, 125),
    )
    slash_x = group_left + speaker_width + group_gap
    draw.text(
        (slash_x, text_y),
        "/",
        font=speaker_font,
        anchor="lm",
        fill=(245, 245, 245, 230),
    )
    draw.text(
        (slash_x + slash_width + group_gap, text_y),
        line,
        font=line_font,
        anchor="lm",
        fill="white",
        stroke_width=1,
        stroke_fill=(25, 25, 25, 125),
    )
    draw.line(
        (underline_left, underline_y, underline_right, underline_y),
        fill=underline,
        width=max(2, int(height * 0.003)),
    )
    base.alpha_composite(layer)


def draw_comments(
    base: Image.Image,
    font_path: Path,
    comments: list[str],
    count: int,
    rng: random.Random,
    protect_zones: list[tuple[float, float, float, float]],
) -> None:
    if count <= 0:
        return
    width, height = base.size
    layer = Image.new("RGBA", base.size)
    draw = ImageDraw.Draw(layer)
    like_icon_source = trimmed_asset(LIKE_ICON_ASSET)
    if count <= len(comments):
        chosen = rng.sample(comments, k=count)
    else:
        chosen = [comments[index % len(comments)] for index in range(count)]
        rng.shuffle(chosen)

    lane_count = 2 if len(chosen) <= 3 else 3
    lane_y = [
        int(height * 0.018),
        int(height * 0.100),
        int(height * 0.182),
    ][:lane_count]
    margin = int(width * 0.018)
    gap = max(10, int(width * 0.013))
    station_zone = (0.0, 0.045, 0.305, 0.148)
    absolute_zones = [
        (
            int(width * x1),
            int(height * y1),
            int(width * x2),
            int(height * y2),
        )
        for x1, y1, x2, y2 in [station_zone, *protect_zones]
    ]

    items: list[dict] = []
    for index, original_text in enumerate(chosen):
        liked = index in ({1} if len(chosen) < 10 else {1, 8})
        like_count = rng.randint(1, 99) if liked else None
        selected_font = fit_font(
            draw,
            original_text,
            font_path,
            int(width * 0.260),
            max(28, int(height * (0.036 if len(chosen) <= 7 else 0.032))),
            max(22, int(height * 0.026)),
        )
        bounds = draw.textbbox(
            (0, 0),
            original_text,
            font=selected_font,
            stroke_width=2,
        )
        text_width = bounds[2] - bounds[0]
        like_width = 0
        like_font = None
        if liked:
            like_icon = like_icon_source.copy()
            icon_size = max(17, int(height * 0.024))
            like_icon.thumbnail((icon_size, icon_size), Image.Resampling.LANCZOS)
            like_font = font(
                font_path,
                max(18, int(selected_font.size * 0.76)),
            )
            like_bounds = draw.textbbox(
                (0, 0),
                str(like_count),
                font=like_font,
                stroke_width=1,
            )
            like_width = (
                like_icon.width
                + int(width * 0.005)
                + like_bounds[2]
                - like_bounds[0]
            )
        else:
            like_icon = None
        items.append(
            {
                "text": original_text,
                "font": selected_font,
                "like_font": like_font,
                "like_icon": like_icon,
                "width": text_width + like_width,
                "text_width": text_width,
                "like_width": like_width,
                "height": bounds[3] - bounds[1],
                "like_count": like_count,
            }
        )

    lanes: list[list[dict]] = [[] for _ in range(lane_count)]
    for index, item in enumerate(items):
        lanes[index % lane_count].append(item)

    def open_segments(y: int, line_height: int) -> list[tuple[int, int]]:
        intervals = [
            (max(margin, x1 - gap), min(width - margin, x2 + gap))
            for x1, y1, x2, y2 in absolute_zones
            if y < y2 and y + line_height > y1
        ]
        intervals.sort()
        merged: list[list[int]] = []
        for start, end in intervals:
            if start >= end:
                continue
            if merged and start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        segments: list[tuple[int, int]] = []
        cursor = margin
        for start, end in merged:
            if start > cursor:
                segments.append((cursor, start))
            cursor = max(cursor, end)
        if cursor < width - margin:
            segments.append((cursor, width - margin))
        return segments

    for lane_index, lane_items in enumerate(lanes):
        if not lane_items:
            continue
        y = lane_y[lane_index]
        total_width = sum(item["width"] for item in lane_items)
        total_width += gap * (len(lane_items) - 1)
        line_height = max(item["height"] for item in lane_items) + int(height * 0.012)
        segments = open_segments(y, line_height)
        fitting = [
            segment for segment in segments if segment[1] - segment[0] >= total_width
        ]
        align_right = lane_index == 0
        if fitting:
            segment = fitting[-1] if align_right else fitting[0]
        else:
            segment = max(segments, key=lambda candidate: candidate[1] - candidate[0])
        x = segment[1] - total_width if align_right else segment[0]

        for item in lane_items:
            draw.text(
                (x, y),
                item["text"],
                font=item["font"],
                fill=(255, 255, 255, 248),
                stroke_width=2,
                stroke_fill=(35, 35, 35, 145),
            )
            if item["like_count"] is not None:
                icon_x = x + item["text_width"] + int(width * 0.005)
                icon_y = y + int(height * 0.006)
                layer.alpha_composite(item["like_icon"], (icon_x, icon_y))
                draw.text(
                    (
                        icon_x + item["like_icon"].width + int(width * 0.004),
                        y + int(height * 0.003),
                    ),
                    str(item["like_count"]),
                    font=item["like_font"],
                    fill=(255, 255, 255, 248),
                    stroke_width=1,
                    stroke_fill=(35, 35, 35, 145),
                )
            x += item["width"] + gap
    base.alpha_composite(layer)


def parse_protect_zones(
    specifications: list[str],
) -> list[tuple[float, float, float, float]]:
    parsed: list[tuple[float, float, float, float]] = []
    for specification in specifications:
        try:
            values = tuple(float(value) for value in specification.split(","))
        except ValueError as error:
            raise SystemExit(
                f"Invalid --protect-zone {specification!r}; expected X1,Y1,X2,Y2."
            ) from error
        if len(values) != 4:
            raise SystemExit(
                f"Invalid --protect-zone {specification!r}; expected X1,Y1,X2,Y2."
            )
        x1, y1, x2, y2 = values
        if not (0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1):
            raise SystemExit(
                f"Invalid --protect-zone {specification!r}; "
                "coordinates must satisfy 0≤X1<X2≤1 and 0≤Y1<Y2≤1."
            )
        parsed.append((x1, y1, x2, y2))
    return parsed


def parse_name_tags(specifications: list[str]) -> list[tuple[str, float, float]]:
    parsed: list[tuple[str, float, float]] = []
    for specification in specifications:
        text, separator, coordinates = specification.rpartition("@")
        if not separator or not text:
            raise SystemExit(
                f"Invalid --name-tag {specification!r}; expected TEXT@X,Y."
            )
        try:
            x_text, y_text = coordinates.split(",", maxsplit=1)
            x, y = float(x_text), float(y_text)
        except ValueError as error:
            raise SystemExit(
                f"Invalid --name-tag {specification!r}; expected TEXT@X,Y."
            ) from error
        if not 0.0 <= x <= 1.0 or not 0.0 <= y <= 1.0:
            raise SystemExit(
                f"Invalid --name-tag {specification!r}; X and Y must be 0–1."
            )
        parsed.append((text, x, y))
    return parsed


def draw_name_tags(
    base: Image.Image,
    font_path: Path,
    tags: list[tuple[str, float, float]],
    curve_path: Path = CAST_NAME_CURVE_ASSET,
) -> None:
    """Draw handwritten cast names with the supplied pink brush curve."""
    if not tags:
        return
    if not curve_path.exists():
        raise SystemExit(f"Cast-name curve not found: {curve_path}")
    width, height = base.size
    layer = Image.new("RGBA", base.size)
    tag_font = font(font_path, max(24, int(height * 0.039)))
    with Image.open(curve_path) as opened_curve:
        curve_source = opened_curve.convert("RGBA")
    for text, relative_x, relative_y in tags:
        x, y = int(width * relative_x), int(height * relative_y)
        probe = ImageDraw.Draw(Image.new("L", (1, 1)))
        bounds = probe.textbbox((0, 0), text, font=tag_font, stroke_width=1)
        text_width = max(1, bounds[2] - bounds[0])
        text_height = max(1, bounds[3] - bounds[1])
        padding = max(10, int(height * 0.010))
        curve_width = max(text_width, int(text_width * 1.13))
        curve_height = max(
            7,
            round(curve_source.height * curve_width / curve_source.width),
        )
        curve = curve_source.resize(
            (curve_width, curve_height),
            Image.Resampling.LANCZOS,
        )
        patch = Image.new(
            "RGBA",
            (
                max(text_width, curve_width) + padding * 2,
                text_height + curve_height + padding * 2,
            ),
        )
        curve_x = (patch.width - curve.width) // 2
        curve_y = padding + max(0, int(text_height * 0.72))
        patch.alpha_composite(curve, (curve_x, curve_y))
        patch_draw = ImageDraw.Draw(patch)
        origin = (
            (patch.width - text_width) // 2 - bounds[0],
            padding - bounds[1],
        )
        patch_draw.text(
            (origin[0] + 1, origin[1] + 2),
            text,
            font=tag_font,
            fill=(26, 22, 24, 125),
            stroke_width=1,
            stroke_fill=(26, 22, 24, 75),
        )
        patch_draw.text(
            origin,
            text,
            font=tag_font,
            fill=(255, 255, 255, 248),
            stroke_width=1,
            stroke_fill=(255, 255, 255, 150),
        )
        patch = patch.rotate(
            3.0,
            resample=Image.Resampling.BICUBIC,
            expand=True,
        )
        text_x = x - patch.width // 2
        text_y = y - patch.height // 2
        layer.alpha_composite(patch, (text_x, text_y))
    base.alpha_composite(layer)


def draw_sponsor(
    base: Image.Image,
    font_path: Path,
    brand: str,
    tagline: str,
    designation: str,
    sponsor_asset: Path,
) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size)
    plate = trimmed_asset(sponsor_asset)
    target_width, target_height = int(width * 0.128), int(height * 0.115)
    plate.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    x = width - plate.width - int(width * 0.025)
    y = height - plate.height - int(height * 0.025)
    layer.alpha_composite(plate, (x, y))

    draw = ImageDraw.Draw(layer)
    is_lockup = sponsor_asset.name in LOCKUP_LABEL_Y or sponsor_asset.stem.endswith(
        "lockup"
    )
    if is_lockup:
        combined = f"{brand}{designation}"
        label_y = LOCKUP_LABEL_Y.get(sponsor_asset.name, 0.85)
        brand_center = (x + int(plate.width * 0.50), y + int(plate.height * label_y))
        max_brand_width = int(plate.width * 0.90)
        brand_fill = (58, 35, 21, 255)
        tagline_center = None
        designation_center = None
    else:
        shadow = Image.new("RGBA", base.size)
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            (
                x + int(plate.width * 0.27),
                y + int(plate.height * 0.30),
                x + int(plate.width * 0.98),
                y + int(plate.height * 0.93),
            ),
            radius=max(8, int(height * 0.012)),
            fill=(10, 12, 18, 115),
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(max(5, int(height * 0.010))))
        layer.alpha_composite(shadow)
        layer.alpha_composite(plate, (x, y))
        brand_center = (x + int(plate.width * 0.64), y + int(plate.height * 0.53))
        max_brand_width = int(plate.width * 0.57)
        designation_center = (
            x + int(plate.width * 0.76),
            y + int(plate.height * 0.78),
        )
        tagline_center = (
            x + int(plate.width * 0.49),
            y + int(plate.height * 0.78),
        )
        brand_fill = (255, 249, 230, 255)
        designation_fill = (235, 190, 93, 255)

    brand_font = fit_font(
        draw,
        combined if is_lockup else brand,
        font_path,
        max_brand_width,
        int(height * 0.025),
        int(height * 0.017),
    )
    centered_text(
        draw,
        brand_center,
        combined if is_lockup else brand,
        brand_font,
        fill=brand_fill,
        stroke_width=0 if is_lockup else 1,
        stroke_fill=(255, 245, 213, 95) if is_lockup else (0, 0, 0, 150),
    )
    if tagline_center and designation_center:
        small_font = fit_font(
            draw,
            tagline,
            font_path,
            int(plate.width * 0.25),
            int(height * 0.015),
            int(height * 0.011),
        )
        centered_text(
            draw,
            tagline_center,
            tagline,
            small_font,
            fill=designation_fill,
            stroke_width=0,
        )
        designation_font = fit_font(
            draw,
            designation,
            font_path,
            int(plate.width * 0.25),
            int(height * 0.017),
            int(height * 0.012),
        )
        centered_text(
            draw,
            designation_center,
            designation,
            designation_font,
            fill=designation_fill,
            stroke_width=0,
        )
    base.alpha_composite(layer)


def main() -> None:
    args = parse_args()
    if (args.width is None) != (args.height is None):
        raise SystemExit("--width and --height must be provided together.")
    if args.width is not None and (args.width <= 0 or args.height <= 0):
        raise SystemExit("Width and height must be positive.")
    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")
    if not 0 <= args.comments <= 24:
        raise SystemExit("--comments must be between 0 and 24.")
    if len(args.comment) > 24:
        raise SystemExit("--comment can be repeated at most 24 times.")
    if args.subject_mask and not args.subject_mask.exists():
        raise SystemExit(f"Subject mask not found: {args.subject_mask}")
    if args.name_curve and not args.name_curve.exists():
        raise SystemExit(f"Cast-name curve not found: {args.name_curve}")
    if args.subject_mask and args.presentation != "standard":
        raise SystemExit("--subject-mask currently supports --presentation standard only.")
    name_tags = parse_name_tags(args.name_tag)
    protect_zones = parse_protect_zones(args.protect_zone)

    dialogue_bank = load_json(DIALOGUES)
    if args.category not in dialogue_bank:
        raise SystemExit(
            f"Unknown category: {args.category}. Available: {', '.join(dialogue_bank)}"
        )
    station_bank = load_json(STATION_PRESETS)["presets"]
    station_presets = {item["id"]: item for item in station_bank}
    preset_id = args.station_preset or DEFAULT_PRESET_BY_CATEGORY.get(
        args.category,
        "mudanjiang",
    )
    if preset_id not in station_presets:
        raise SystemExit(
            f"Unknown station preset: {preset_id}. Available: {', '.join(station_presets)}"
        )
    preset = station_presets[preset_id]
    station = args.station or preset["station"]
    station_override = args.station_bug or args.station_icon
    station_asset = resolve_station_asset(preset, station_override)

    flourish_bank = load_json(FLOURISH_PRESETS)
    flourish_path = args.flourish or FLOURISH_ASSETS / flourish_bank["categories"].get(
        args.category,
        flourish_bank["default"],
    )
    if not flourish_path.exists():
        raise SystemExit(f"Flourish asset not found: {flourish_path}")

    sponsor_bank = load_json(SPONSOR_PRESETS)
    sponsor_preset = sponsor_bank.get("stations", {}).get(
        preset_id,
        sponsor_bank["default"],
    )
    sponsor = args.sponsor if args.sponsor is not None else sponsor_preset["brand"]
    sponsor_tagline = (
        args.sponsor_tagline
        if args.sponsor_tagline is not None
        else sponsor_preset["tagline"]
    )
    sponsor_designation = (
        args.sponsor_designation
        if args.sponsor_designation is not None
        else sponsor_preset["designation"]
    )
    sponsor_filename = sponsor_preset["asset"]
    if args.sponsor_style:
        sponsor_filename = (
            args.sponsor_style
            if args.sponsor_style.endswith(".png")
            else f"{args.sponsor_style}.png"
        )
    sponsor_asset = args.sponsor_asset or SPONSOR_ASSETS / sponsor_filename
    if not args.no_sponsor and not sponsor_asset.exists():
        raise SystemExit(f"Sponsor asset not found: {sponsor_asset}")

    rng = random.Random(args.seed)
    line = args.line or rng.choice(dialogue_bank[args.category])
    comment_count = (
        len(args.comment)
        if args.comment
        else (
            DANMAKU_COUNTS[args.danmaku_density]
            if args.danmaku_density
            else args.comments
        )
    )
    rendered_comments = args.comment if args.comment else (
        dialogue_bank["弹幕"] if comment_count else []
    )
    all_text = " ".join(
        [
            station,
            args.badge,
            args.speaker,
            line,
            "" if args.no_sponsor else sponsor,
            "" if args.no_sponsor else sponsor_tagline,
            "" if args.no_sponsor else sponsor_designation,
        ]
        + rendered_comments
    )
    station_font_path = resolve_role_font(
        args.station_font,
        args.font,
        BUNDLED_BOLD_FONT,
        all_text,
    )
    caption_font_path = resolve_role_font(
        args.caption_font,
        args.font,
        BUNDLED_DIALOGUE_FONT,
        all_text,
    )
    name_font_path = resolve_role_font(
        args.name_font or args.caption_font,
        args.font,
        BUNDLED_NAME_FONT,
        " ".join(text for text, _, _ in name_tags) or all_text,
    )
    sponsor_font_path = resolve_role_font(
        args.sponsor_font,
        args.font,
        BUNDLED_CAPTION_BOLD_FONT,
        all_text,
    )

    with Image.open(args.input) as opened_source:
        source_info = dict(opened_source.info)
        source = ImageOps.exif_transpose(opened_source).convert("RGB")
    output_size = (
        (args.width, args.height)
        if args.width is not None and args.height is not None
        else native_broadcast_size(source)
    )
    canvas_builder = (
        photo_card_canvas if args.presentation == "photo-card" else broadcast_canvas
    )
    base = canvas_builder(source, output_size).convert("RGBA")
    clean_photo = base.copy()
    draw_comments(
        base,
        station_font_path,
        args.comment or dialogue_bank["弹幕"],
        comment_count,
        rng,
        protect_zones,
    )
    if args.subject_mask:
        subject_mask = ImageOps.exif_transpose(
            Image.open(args.subject_mask)
        ).convert("L")
        if subject_mask.size != source.size:
            raise SystemExit(
                "--subject-mask must have the same pixel dimensions as --input."
            )
        aligned_mask = broadcast_mask(subject_mask, output_size)
        base = Image.composite(clean_photo, base, aligned_mask).convert("RGBA")
    draw_station(base, station_font_path, station, args.badge, station_asset)
    underline = UNDERLINE_BY_CATEGORY.get(args.category, (185, 41, 80, 235))
    draw_lower_third(
        base,
        caption_font_path,
        args.speaker,
        line,
        underline,
        flourish_path,
    )
    draw_name_tags(
        base,
        name_font_path,
        name_tags,
        args.name_curve or CAST_NAME_CURVE_ASSET,
    )
    if not args.no_sponsor:
        draw_sponsor(
            base,
            sponsor_font_path,
            sponsor,
            sponsor_tagline,
            sponsor_designation,
            sponsor_asset,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    save_kwargs: dict[str, object] = {}
    if source_info.get("icc_profile"):
        save_kwargs["icc_profile"] = source_info["icc_profile"]
    if source_info.get("dpi"):
        save_kwargs["dpi"] = source_info["dpi"]
    if args.output.suffix.lower() in {".jpg", ".jpeg"}:
        base.convert("RGB").save(
            args.output,
            quality=100,
            subsampling=0,
            **save_kwargs,
        )
    else:
        base.save(args.output, **save_kwargs)
    print(args.output)
    print(f"line={line}")
    print(
        f"station={station} preset={preset_id} "
        f"bug_mode={preset['bug_mode']} asset={station_asset.name}"
    )
    print(f"flourish={flourish_path.name}")
    print(
        f"danmaku={comment_count} "
        f"density={args.danmaku_density or 'custom'} "
        f"protect_zones={len(protect_zones)} "
        f"subject_mask={'on' if args.subject_mask else 'off'}"
    )
    print(
        "sponsor=off"
        if args.no_sponsor
        else f"sponsor={sponsor} / {sponsor_tagline} / {sponsor_designation}"
    )


if __name__ == "__main__":
    main()
