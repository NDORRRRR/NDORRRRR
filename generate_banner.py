"""Generate a code-designed, editable animated GitHub profile banner.

Requires: Pillow (`pip install pillow`). No image-generation model, remote assets,
HTML/CSS or GitHub Actions. Edit CONTENT and COLORS below, then run:

    python generate_banner.py

Writes assets/dev-terminal.gif and assets/preview.png next to this file.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "assets"
OUT.mkdir(exist_ok=True)

# EDIT ME --------------------------------------------------------------
NAME_FIRST = "Adhim"
NAME_LAST = "Musafak."
ROLE = "MOBILE  /  WEB  /  BACKEND"
DESCRIPTION = "Building apps, interfaces and the APIs behind them."
EDUCATION = "Informatics Engineering Student at State University of Surabaya"
LOCATION = "GRESIK, INDONESIA"
CURRENT_PROJECT = "JAGATANI"
PROMPT = "adhim@dev ~ % "
SCENES = [
    ("cat about.txt", ["web / mobile / APIs", "Flutter  |  React  |  Python"]),
    ("cat education.txt", ["Informatics Engineering Student", "State University of Surabaya"]),
    ("ls projects/", ["JagaTani     UrbanMotion", "SakuMahasiswa"]),
    ("cat now.txt", ["Current focus: JagaTani", "Flutter + Python integration"]),
]
COLORS = {
    "background": "#0D0E13",
    "surface": "#17181F",
    "surface_2": "#1C1C24",
    "border": "#333039",
    "red": "#B64B58",
    "muted_red": "#70313B",
    "yellow": "#EED79F",
    "white": "#F4F0EB",
    "soft": "#C0BEC4",
    "muted": "#86828C",
}
WIDTH, HEIGHT = 1200, 328
FPS = 12
SCENE_FRAMES = 46  # Four scenes; loops continuously
# ----------------------------------------------------------------------

FONT_DIR = Path("/usr/share/fonts/opentype/inter")
MONO_DIR = Path("/usr/share/fonts/truetype/dejavu")
WINDOWS_FONTS = Path("C:/Windows/Fonts")
MAC_FONTS = Path("/System/Library/Fonts")


def font(path, size, fallback=None):
    if path.exists():
        return ImageFont.truetype(str(path), size)
    if fallback and fallback.exists():
        return ImageFont.truetype(str(fallback), size)
    return ImageFont.load_default()


def system_font(paths, size):
    for item in paths:
        if item.exists():
            return ImageFont.truetype(str(item), size)
    return ImageFont.load_default(size=size)


f_name = system_font([FONT_DIR / "InterDisplay-Bold.otf", WINDOWS_FONTS / "segoeuib.ttf", MAC_FONTS / "Helvetica.ttc", MONO_DIR / "DejaVuSans-Bold.ttf"], 66)
f_role = system_font([MONO_DIR / "DejaVuSansMono.ttf", WINDOWS_FONTS / "consola.ttf", MAC_FONTS / "Menlo.ttc"], 15)
f_tag = system_font([MONO_DIR / "DejaVuSansMono.ttf", WINDOWS_FONTS / "consola.ttf", MAC_FONTS / "Menlo.ttc"], 11)
f_education = system_font([FONT_DIR / "Inter-Regular.otf", WINDOWS_FONTS / "segoeui.ttf", MAC_FONTS / "Helvetica.ttc", MONO_DIR / "DejaVuSans.ttf"], 13)
f_desc = system_font([FONT_DIR / "Inter-Regular.otf", WINDOWS_FONTS / "segoeui.ttf", MAC_FONTS / "Helvetica.ttc", MONO_DIR / "DejaVuSans.ttf"], 15)
f_code = system_font([MONO_DIR / "DejaVuSansMono.ttf", WINDOWS_FONTS / "consola.ttf", MAC_FONTS / "Menlo.ttc"], 16)
f_code_small = system_font([MONO_DIR / "DejaVuSansMono.ttf", WINDOWS_FONTS / "consola.ttf", MAC_FONTS / "Menlo.ttc"], 12)
C = COLORS


def round_rect(draw, rect, radius, *, fill=None, outline=None, width=1):
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=width)


def base_image():
    im = Image.new("RGB", (WIDTH, HEIGHT), C["background"])
    d = ImageDraw.Draw(im)

    # Quiet structural details: no glow, stock art or gratuitous doodles.
    d.rectangle((0, 0, WIDTH - 1, HEIGHT - 1), outline="#27252D", width=1)
    d.line((0, 0, 8, 0), fill=C["red"], width=2)
    d.rectangle((0, 0, 5, HEIGHT), fill=C["red"])
    d.rectangle((6, 0, 7, HEIGHT), fill=C["muted_red"])

    d.text((55, 36), "01 / PROFILE", font=f_tag, fill=C["yellow"])
    d.line((55, 59, 182, 59), fill=C["muted_red"], width=2)

    d.text((50, 83), NAME_FIRST, font=f_name, fill=C["white"])
    d.text((50, 151), NAME_LAST, font=f_name, fill=C["red"])
    d.text((55, 230), ROLE, font=f_role, fill=C["yellow"])
    d.text((55, 259), DESCRIPTION, font=f_desc, fill=C["soft"])
    d.line((55, 286, 505, 286), fill=C["border"], width=1)
    d.text((55, 291), EDUCATION, font=f_education, fill=C["yellow"])

    # Right panel, handcrafted terminal window.
    tx0, ty0, tx1, ty1 = (619, 29, 1155, 289)
    round_rect(d, (tx0, ty0, tx1, ty1), 14, fill=C["surface"], outline=C["border"], width=2)
    d.rounded_rectangle((tx0 + 1, ty0 + 1, tx1 - 1, ty0 + 39), radius=12, fill=C["surface_2"])
    d.rectangle((tx0 + 2, ty0 + 27, tx1 - 2, ty0 + 39), fill=C["surface_2"])
    d.line((tx0 + 2, ty0 + 39, tx1 - 2, ty0 + 39), fill=C["border"], width=1)
    for i, dotc in enumerate([C["red"], C["yellow"], C["muted"]]):
        x = tx0 + 20 + i * 18
        d.ellipse((x, ty0 + 16, x + 7, ty0 + 23), fill=dotc)
    d.text((tx0 + 208, ty0 + 12), "~/ndorrrrr", font=f_code_small, fill=C["soft"])
    # terminal line markers
    d.text((647, 91), "01", font=f_code_small, fill="#5A5862")
    d.text((647, 134), "02", font=f_code_small, fill="#5A5862")
    d.text((647, 173), "03", font=f_code_small, fill="#5A5862")
    # terminal footer
    d.line((648, 246, 1123, 246), fill="#37333A", width=1)
    d.text((649, 259), "CURRENT BRANCH", font=f_code_small, fill=C["muted"])
    d.text((803, 259), "building", font=f_code_small, fill=C["yellow"])

    # Footnote outside the terminal.
    d.text((620, 300), "STATUS", font=f_tag, fill=C["muted"])
    d.text((684, 300), CURRENT_PROJECT, font=f_tag, fill=C["yellow"])
    d.ellipse((1129, 303, 1137, 311), fill=C["red"])
    return im


def scene_frame(scene_idx, frame_idx):
    im = base_image()
    d = ImageDraw.Draw(im)
    cmd, result = SCENES[scene_idx]
    # The command types in over ~1.7 seconds; the result then holds.
    n = min(len(cmd), max(0, frame_idx - 3))
    d.text((678, 88), PROMPT, font=f_code, fill=C["yellow"])
    tw = d.textlength(PROMPT, font=f_code)
    d.text((678 + int(tw), 88), cmd[:n], font=f_code, fill=C["white"])
    if n < len(cmd) or frame_idx < SCENE_FRAMES - 4:
        # Blinks instead of permanently covering the last character.
        if (frame_idx // 5) % 2 == 0:
            x = 678 + int(tw) + int(d.textlength(cmd[:n], font=f_code)) + 2
            d.rectangle((x, 91, x + 7, 108), fill=C["red"])

    if frame_idx >= len(cmd) + 5:
        d.text((679, 132), ">  " + result[0], font=f_code, fill=C["soft"])
        if len(result) > 1:
            d.text((679, 171), "   " + result[1], font=f_code, fill=C["soft"])
    elif frame_idx >= len(cmd) + 2:
        d.text((679, 132), ">", font=f_code, fill=C["red"])
    # Tiny moving segmented activity bar. Not a fabricated statistic.
    for i in range(12):
        active = (i == (frame_idx // 4) % 12) or i == ((frame_idx // 4 - 1) % 12)
        x0 = 989 + 12 * i
        d.rounded_rectangle((x0, 263, x0 + 8, 267), radius=2, fill=C["red"] if active else "#343139")
    return im


def export():
    frames = [scene_frame(s, t) for s in range(len(SCENES)) for t in range(SCENE_FRAMES)]
    preview = scene_frame(1, 32)
    preview.save(OUT / "preview.png")
    # Deterministic palette and adaptive optimization keep GIF small.
    frames[0].save(
        OUT / "dev-terminal.gif",
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        loop=0,
        duration=round(1000 / FPS),
        disposal=2,
    )
    print(f"Generated {OUT / 'dev-terminal.gif'} ({len(frames)} frames @ {FPS} fps)")


if __name__ == "__main__":
    export()
