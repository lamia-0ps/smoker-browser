#!/usr/bin/env python3
"""Generate a tilted cigarette launcher icon at every Android density."""
import math
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lerp(a, b, t):
    return a + (b - a) * t


def draw_cigarette(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    # Charcoal rounded-square background
    top, bot = (58, 66, 72), (26, 31, 36)
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg_d = ImageDraw.Draw(bg)
    for y in range(size):
        t = y / max(1, size - 1)
        col = tuple(int(lerp(top[i], bot[i], t)) for i in range(3)) + (255,)
        bg_d.line([(0, y), (size, y)], fill=col)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=255
    )
    img.paste(bg, (0, 0), mask)
    d = ImageDraw.Draw(img, "RGBA")

    cx, cy = size * 0.5, size * 0.54
    angle = math.radians(-28)
    ca, sa = math.cos(angle), math.sin(angle)

    def xf(lx, ly):
        # local coords: origin at cigarette center, y+ toward filter
        return (
            cx + lx * ca - ly * sa,
            cy + lx * sa + ly * ca,
        )

    def poly(pts, fill):
        d.polygon([xf(*p) for p in pts], fill=fill)

    w = size * 0.085  # half-width of cigarette
    body_top = -size * 0.22
    body_bot = size * 0.16
    filt_bot = size * 0.32

    # Ember glow
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gx, gy = xf(0, body_top - size * 0.02)
    r = size * 0.16
    gd.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(255, 112, 67, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(size * 0.035))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img, "RGBA")

    # White body
    poly([(-w, body_top), (w, body_top), (w, body_bot), (-w, body_bot)], (244, 244, 244, 255))
    # Highlight
    poly([(-w * 0.45, body_top + 2), (-w * 0.1, body_top + 2),
          (-w * 0.1, body_bot - 2), (-w * 0.45, body_bot - 2)], (255, 255, 255, 220))
    # Ash ring
    poly([(-w, body_top), (w, body_top), (w, body_top + size * 0.03),
          (-w, body_top + size * 0.03)], (158, 158, 158, 255))
    # Filter
    poly([(-w, body_bot), (w, body_bot), (w, filt_bot), (-w, filt_bot)], (215, 168, 110, 255))
    # Filter cap
    poly([(-w, filt_bot - size * 0.02), (w, filt_bot - size * 0.02),
          (w, filt_bot), (-w, filt_bot)], (196, 146, 90, 255))

    # Ember disc
    ex, ey = xf(0, body_top)
    er = size * 0.055
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(255, 106, 0, 255))
    ir = er * 0.45
    d.ellipse([ex - ir, ey - ir, ex + ir, ey + ir], fill=(255, 213, 79, 255))

    # Smoke wisps
    smoke = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(smoke)
    sx, sy = xf(0, body_top - size * 0.02)
    lw = max(2, int(size * 0.018))
    for i, (dx, dy, col) in enumerate([
        (size * 0.02, -size * 0.22, (245, 245, 245, 150)),
        (size * 0.10, -size * 0.20, (230, 230, 230, 110)),
        (-size * 0.04, -size * 0.24, (255, 255, 255, 90)),
    ]):
        pts = []
        steps = 18
        for k in range(steps):
            t = k / (steps - 1)
            x = sx + dx * t + math.sin(t * 6 + i) * size * 0.025
            y = sy + dy * t
            pts.append((x, y))
        if len(pts) > 1:
            sd.line(pts, fill=col, width=lw, joint="curve")
    smoke = smoke.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.alpha_composite(img, smoke)
    return img


def main():
    densities = {
        "mdpi": 48,
        "hdpi": 72,
        "xhdpi": 96,
        "xxhdpi": 144,
        "xxxhdpi": 192,
    }
    for dpi, px in densities.items():
        folder = os.path.join(ROOT, "app", "src", "main", "res", f"mipmap-{dpi}")
        os.makedirs(folder, exist_ok=True)
        icon = draw_cigarette(px)
        icon.save(os.path.join(folder, "ic_launcher.png"), "PNG")
        icon.save(os.path.join(folder, "ic_launcher_round.png"), "PNG")
        print("wrote", dpi, px)

    play = os.path.join(ROOT, "fastlane", "metadata", "android", "en-US", "images")
    os.makedirs(play, exist_ok=True)
    draw_cigarette(512).save(os.path.join(play, "icon.png"), "PNG")
    print("wrote play store icon")


if __name__ == "__main__":
    main()
