#!/usr/bin/env python3
"""Generate Smoker Browser launcher + tools icons from the flame logo (assets/logo_webp.part*)."""
import base64
import glob
import io
import os
from PIL import Image, ImageDraw, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG = (18, 22, 29)  # #12161D — matches the artwork backdrop


def load_logo():
    parts = sorted(glob.glob(os.path.join(ROOT, "assets", "logo_webp.part*")))
    single = os.path.join(ROOT, "assets", "logo_webp.b64")
    if parts:
        text = "".join(open(p, encoding="ascii").read().strip() for p in parts)
    else:
        text = open(single, encoding="ascii").read()
    data = base64.b64decode(text)
    return Image.open(io.BytesIO(data)).convert("RGBA")


def circle(img):
    size = img.size[0]
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def foreground(logo, size):
    """Adaptive-icon foreground: logo at ~62% centered on transparent (safe zone)."""
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    inner = int(size * 0.62)
    art = logo.resize((inner, inner), Image.LANCZOS)
    off = (size - inner) // 2
    out.paste(art, (off, off), art)
    return out


def main():
    logo = load_logo()  # 512x512
    densities = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
    fg_sizes = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}

    for dpi, px in densities.items():
        folder = os.path.join(ROOT, "app", "src", "main", "res", f"mipmap-{dpi}")
        os.makedirs(folder, exist_ok=True)
        square = logo.resize((px, px), Image.LANCZOS)
        square.save(os.path.join(folder, "ic_launcher.png"), "PNG")
        circle(square).save(os.path.join(folder, "ic_launcher_round.png"), "PNG")
        print("wrote mipmap", dpi, px)

    for dpi, px in fg_sizes.items():
        folder = os.path.join(ROOT, "app", "src", "main", "res", f"drawable-{dpi}")
        os.makedirs(folder, exist_ok=True)
        foreground(logo, px).save(os.path.join(folder, "ic_launcher_foreground.png"), "PNG")
        print("wrote adaptive foreground", dpi, px)

    # old vector foreground would shadow nothing but is obsolete — remove it
    vec = os.path.join(ROOT, "app", "src", "main", "res", "drawable", "ic_launcher_foreground.xml")
    if os.path.exists(vec):
        os.remove(vec)
        print("removed obsolete vector foreground")

    # solid dark adaptive background
    with open(os.path.join(ROOT, "app", "src", "main", "res", "drawable", "ic_launcher_background.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="utf-8"?>\n'
                 '<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">\n'
                 '    <solid android:color="#12161D" />\n'
                 '</shape>\n')
    print("wrote solid background")

    # smokey tools icon for the toolbar menu button (round badge)
    nodpi = os.path.join(ROOT, "app", "src", "main", "res", "drawable-nodpi")
    os.makedirs(nodpi, exist_ok=True)
    badge = circle(logo.resize((192, 192), Image.LANCZOS))
    ring = ImageDraw.Draw(badge)
    ring.ellipse([2, 2, 189, 189], outline=(255, 112, 67, 255), width=5)
    badge.save(os.path.join(nodpi, "tools_icon.png"), "PNG")
    print("wrote tools_icon.png")

    play = os.path.join(ROOT, "fastlane", "metadata", "android", "en-US", "images")
    os.makedirs(play, exist_ok=True)
    logo.save(os.path.join(play, "icon.png"), "PNG")
    print("wrote play store icon")


if __name__ == "__main__":
    main()
