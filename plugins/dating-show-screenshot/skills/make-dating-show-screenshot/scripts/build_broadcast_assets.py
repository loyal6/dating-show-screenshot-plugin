#!/usr/bin/env python3
"""Build flat broadcast emblems and premium fictional sponsor product shots."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ICON_OUTPUT = ROOT / "assets" / "station-icons"
SPONSOR_OUTPUT = ROOT / "assets" / "sponsors"
SCALE = 4


def scaled(point: tuple[float, float]) -> tuple[int, int]:
    return round(point[0] * SCALE), round(point[1] * SCALE)


def bezier(
    start: tuple[float, float],
    control_a: tuple[float, float],
    control_b: tuple[float, float],
    end: tuple[float, float],
    steps: int = 80,
) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for index in range(steps + 1):
        t = index / steps
        inverse = 1 - t
        x = (
            inverse**3 * start[0]
            + 3 * inverse**2 * t * control_a[0]
            + 3 * inverse * t**2 * control_b[0]
            + t**3 * end[0]
        )
        y = (
            inverse**3 * start[1]
            + 3 * inverse**2 * t * control_a[1]
            + 3 * inverse * t**2 * control_b[1]
            + t**3 * end[1]
        )
        points.append(scaled((x, y)))
    return points


def finish(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.resize(size, Image.Resampling.LANCZOS)


def icon_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (480 * SCALE, 300 * SCALE))
    return image, ImageDraw.Draw(image)


def rising_ribbon() -> Image.Image:
    image, draw = icon_canvas()
    navy = (17, 54, 111, 255)
    coral = (224, 45, 59, 255)
    gold = (244, 150, 35, 255)
    draw.line(
        bezier((61, 187), (153, 235), (250, 72), (420, 105)),
        fill=coral,
        width=28 * SCALE,
        joint="curve",
    )
    draw.line(
        bezier((77, 211), (174, 236), (278, 128), (404, 126)),
        fill=gold,
        width=17 * SCALE,
        joint="curve",
    )
    draw.line(
        bezier((104, 225), (189, 252), (285, 191), (373, 172)),
        fill=navy,
        width=12 * SCALE,
        joint="curve",
    )
    draw.ellipse((*scaled((278, 67)), *scaled((326, 115))), fill=gold)
    return finish(image, (480, 300))


def twin_river() -> Image.Image:
    image, draw = icon_canvas()
    blue = (12, 86, 160, 255)
    cyan = (25, 173, 181, 255)
    draw.line(
        bezier((62, 126), (151, 55), (267, 53), (416, 122)),
        fill=blue,
        width=31 * SCALE,
        joint="curve",
    )
    draw.line(
        bezier((63, 171), (176, 239), (293, 229), (416, 151)),
        fill=cyan,
        width=31 * SCALE,
        joint="curve",
    )
    draw.ellipse((*scaled((216, 121)), *scaled((274, 179))), fill=(255, 255, 255, 255))
    draw.ellipse((*scaled((231, 136)), *scaled((259, 164))), fill=blue)
    return finish(image, (480, 300))


def mountain_pulse() -> Image.Image:
    image, draw = icon_canvas()
    indigo = (41, 39, 116, 255)
    gold = (222, 159, 45, 255)
    draw.polygon(
        [scaled((76, 218)), scaled((211, 65)), scaled((343, 218))],
        fill=indigo,
    )
    draw.polygon(
        [scaled((145, 204)), scaled((213, 121)), scaled((282, 204))],
        fill=(0, 0, 0, 0),
    )
    draw.line(
        bezier((83, 224), (177, 189), (272, 232), (405, 135)),
        fill=gold,
        width=25 * SCALE,
        joint="curve",
    )
    return finish(image, (480, 300))


def moon_bay() -> Image.Image:
    image, draw = icon_canvas()
    navy = (17, 43, 95, 255)
    teal = (22, 148, 160, 255)
    draw.ellipse((*scaled((66, 43)), *scaled((304, 261))), fill=navy)
    draw.ellipse((*scaled((142, 29)), *scaled((335, 219))), fill=(0, 0, 0, 0))
    draw.line(
        bezier((102, 207), (185, 138), (273, 241), (409, 157)),
        fill=teal,
        width=29 * SCALE,
        joint="curve",
    )
    draw.line(
        bezier((151, 222), (237, 184), (303, 226), (386, 186)),
        fill=(255, 255, 255, 242),
        width=10 * SCALE,
        joint="curve",
    )
    return finish(image, (480, 300))


def star_orbit() -> Image.Image:
    image, draw = icon_canvas()
    blue = (20, 61, 137, 255)
    rose = (212, 52, 89, 255)
    draw.line(
        bezier((63, 183), (146, 57), (294, 52), (423, 132)),
        fill=rose,
        width=23 * SCALE,
        joint="curve",
    )
    draw.line(
        bezier((59, 184), (164, 262), (307, 250), (422, 139)),
        fill=blue,
        width=31 * SCALE,
        joint="curve",
    )
    cx, cy = 246, 150
    points: list[tuple[int, int]] = []
    for index in range(8):
        angle = math.radians(-90 + index * 45)
        radius = 67 if index % 2 == 0 else 22
        points.append(scaled((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius)))
    draw.polygon(points, fill=blue)
    return finish(image, (480, 300))


def sponsor_canvas() -> Image.Image:
    return Image.new("RGBA", (720 * SCALE, 260 * SCALE))


def product_shadow(image: Image.Image, box: tuple[float, float, float, float]) -> None:
    layer = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(layer)
    draw.ellipse((*scaled((box[0], box[1])), *scaled((box[2], box[3]))), fill=(0, 0, 0, 105))
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(12 * SCALE)))


def metallic_can(
    image: Image.Image,
    box: tuple[int, int, int, int],
    colors: tuple[tuple[int, int, int], tuple[int, int, int]],
) -> ImageDraw.ImageDraw:
    x0, y0, x1, y1 = box
    draw = ImageDraw.Draw(image)
    radius = 25
    mask = Image.new("L", image.size)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        (*scaled((x0, y0)), *scaled((x1, y1))),
        radius=radius * SCALE,
        fill=255,
    )
    gradient = Image.new("RGBA", image.size)
    gradient_draw = ImageDraw.Draw(gradient)
    span = max(1, x1 - x0)
    for x in range(x0 * SCALE, x1 * SCALE + 1):
        t = (x / SCALE - x0) / span
        shine = 0.18 * math.sin(math.pi * t)
        rgb = tuple(
            round(colors[0][index] * (1 - t) + colors[1][index] * t + 255 * shine)
            for index in range(3)
        )
        gradient_draw.line((x, y0 * SCALE, x, y1 * SCALE), fill=(*rgb, 255))
    image.alpha_composite(Image.composite(gradient, Image.new("RGBA", image.size), mask))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (*scaled((x0, y0)), *scaled((x1, y1))),
        radius=radius * SCALE,
        outline=(255, 255, 255, 175),
        width=3 * SCALE,
    )
    draw.ellipse(
        (*scaled((x0 + 8, y0 - 3)), *scaled((x1 - 8, y0 + 15))),
        fill=(225, 224, 219, 255),
        outline=(255, 255, 255, 220),
        width=2 * SCALE,
    )
    return draw


def sparkling_can() -> Image.Image:
    image = sponsor_canvas()
    product_shadow(image, (35, 214, 225, 248))
    draw = metallic_can(image, (73, 24, 185, 228), ((18, 68, 127), (39, 165, 178)))
    draw.line(
        bezier((92, 168), (115, 111), (146, 110), (169, 72)),
        fill=(255, 255, 255, 235),
        width=9 * SCALE,
    )
    draw.ellipse((*scaled((111, 94)), *scaled((145, 128))), fill=(229, 78, 86, 255))
    draw.line(
        bezier((205, 72), (298, 20), (397, 47), (505, 33)),
        fill=(218, 168, 77, 170),
        width=4 * SCALE,
    )
    return finish(image, (720, 260))


def mountain_tea() -> Image.Image:
    image = sponsor_canvas()
    product_shadow(image, (30, 215, 232, 250))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (*scaled((76, 38)), *scaled((190, 229))),
        radius=30 * SCALE,
        fill=(32, 80, 69, 255),
        outline=(224, 190, 112, 255),
        width=4 * SCALE,
    )
    draw.rounded_rectangle(
        (*scaled((98, 10)), *scaled((168, 50))),
        radius=10 * SCALE,
        fill=(218, 185, 110, 255),
    )
    draw.polygon(
        [scaled((88, 188)), scaled((132, 88)), scaled((179, 188))],
        fill=(239, 226, 188, 242),
    )
    draw.polygon(
        [scaled((113, 180)), scaled((143, 118)), scaled((175, 180))],
        fill=(126, 174, 142, 255),
    )
    draw.line(
        bezier((204, 74), (309, 31), (385, 62), (505, 42)),
        fill=(218, 168, 77, 170),
        width=4 * SCALE,
    )
    return finish(image, (720, 260))


def energy_pack() -> Image.Image:
    image = sponsor_canvas()
    product_shadow(image, (24, 213, 244, 250))
    draw = metallic_can(image, (61, 25, 197, 229), ((127, 19, 39), (235, 93, 38)))
    bolt = [
        scaled((140, 58)),
        scaled((99, 139)),
        scaled((135, 136)),
        scaled((111, 205)),
        scaled((170, 113)),
        scaled((137, 116)),
    ]
    draw.polygon(bolt, fill=(255, 212, 67, 255))
    draw.line(
        bezier((211, 63), (319, 19), (396, 65), (512, 35)),
        fill=(218, 168, 77, 170),
        width=4 * SCALE,
    )
    return finish(image, (720, 260))


def main() -> None:
    ICON_OUTPUT.mkdir(parents=True, exist_ok=True)
    SPONSOR_OUTPUT.mkdir(parents=True, exist_ok=True)
    icons = {
        "rising-ribbon.png": rising_ribbon(),
        "twin-river.png": twin_river(),
        "mountain-pulse.png": mountain_pulse(),
        "moon-bay.png": moon_bay(),
        "star-orbit.png": star_orbit(),
    }
    sponsors = {
        "sparkling-can.png": sparkling_can(),
        "mountain-tea.png": mountain_tea(),
        "energy-pack.png": energy_pack(),
    }
    for name, image in {**icons, **sponsors}.items():
        destination = (ICON_OUTPUT if name in icons else SPONSOR_OUTPUT) / name
        image.save(destination)
        print(destination)


if __name__ == "__main__":
    main()
