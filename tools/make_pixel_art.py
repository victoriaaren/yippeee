"""Generates the pixel art card thumbnails into static/img/.

Run: python tools/make_pixel_art.py
Each scene is drawn on a tiny 96x64 canvas and upscaled with nearest-neighbor.
"""
from pathlib import Path
from PIL import Image, ImageDraw

W, H, SCALE = 96, 64, 4
OUT = Path(__file__).resolve().parent.parent / "static" / "img"

INK = "#6b4f3b"
WHITE = "#fffaf3"
BLUSH = "#f4a3b0"


def canvas(bands, table=None):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    step = H // len(bands)
    for i, c in enumerate(bands):
        d.rectangle([0, i * step, W, H if i == len(bands) - 1 else (i + 1) * step], fill=c)
    if table:
        d.rectangle([0, 50, W, H], fill=table[0])
        d.rectangle([0, 50, W, 51], fill=table[1])
    return img, d


def sparkle(d, x, y, c=WHITE):
    d.point([(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)], fill=c)


def sparkles(d, spots, c=WHITE):
    for x, y in spots:
        sparkle(d, x, y, c)


def face(d, x, y, blush=BLUSH):
    d.rectangle([x - 5, y, x - 5, y + 1], fill=INK)
    d.rectangle([x + 5, y, x + 5, y + 1], fill=INK)
    d.rectangle([x - 8, y + 3, x - 6, y + 3], fill=blush)
    d.rectangle([x + 6, y + 3, x + 8, y + 3], fill=blush)
    d.point([(x - 1, y + 3), (x + 1, y + 3), (x, y + 4)], fill=INK)


def steam(d, x, y, c=WHITE):
    for i in range(3):
        d.point([(x, y - i * 3), (x + 1, y - i * 3 - 1), (x, y - i * 3 - 2)], fill=c)


def clouds(d, spots, c="#ffffff"):
    for x, y in spots:
        d.rectangle([x, y, x + 9, y + 2], fill=c)
        d.rectangle([x + 2, y - 2, x + 6, y], fill=c)


def boba(milk, milk_hi, bg, table, straw="#a8d5b5", pearls="#4a3226", label=None):
    img, d = canvas(bg, table)
    clouds(d, [(6, 8), (76, 14)], "#ffffff")
    d.polygon([(33, 20), (63, 20), (59, 52), (37, 52)], fill=milk)
    d.polygon([(35, 26), (61, 26), (60, 28), (36, 28)], fill=milk_hi)
    d.rectangle([32, 17, 64, 20], fill=WHITE)
    d.rectangle([34, 14, 62, 17], fill="#f6efe6")
    d.line([(52, 3), (48, 16)], fill=straw, width=3)
    d.line([(52, 3), (48, 16)], fill="#ffffff", width=1)
    for (px, py) in [(40, 49), (45, 49), (50, 49), (55, 49), (42, 45), (48, 45), (53, 45), (45, 41), (51, 41)]:
        d.rectangle([px, py, px + 2, py + 2], fill=pearls)
        d.point((px, py), fill="#7a5a44")
    d.line([(38, 24), (41, 45)], fill="#ffffff", width=1)
    sparkles(d, [(12, 28), (84, 30), (18, 46), (80, 8)])
    return img


def chawan():
    img, d = canvas(["#dff0d8", "#d3e8cb", "#c8e0bf", "#bcd8b3"], ("#e9d9bf", "#d3bf9c"))
    clouds(d, [(70, 6), (8, 10)])
    d.pieslice([24, 11, 72, 55], 0, 180, fill="#f2e6d0")
    d.rectangle([28, 36, 34, 42], fill="#fbf3e2")
    d.ellipse([24, 28, 72, 38], fill="#e6d4b4")
    d.ellipse([27, 29, 69, 37], fill="#8fb58a")
    d.ellipse([32, 31, 54, 35], fill="#b9d6a8")
    for x, y in [(36, 32), (44, 33), (58, 34)]:
        d.rectangle([x, y, x + 1, y], fill="#d6ebc6")
    d.rectangle([38, 55, 58, 57], fill="#d8c5a2")
    d.rectangle([10, 40, 12, 52], fill="#d9b88a")
    d.polygon([(6, 52), (16, 52), (14, 60), (8, 60)], fill="#e8d3a8")
    for x in range(7, 15, 2):
        d.line([(x, 54), (x, 59)], fill="#caa874")
    steam(d, 40, 22, "#ffffff")
    steam(d, 56, 20, "#ffffff")
    sparkles(d, [(84, 30), (16, 26), (80, 14)], "#f4fbe9")
    return img


def ice_cream_cone():
    img, d = canvas(["#d9ecfa", "#cfe5f6", "#c5def2", "#bcd8ee"], ("#eef4f9", "#d3e1ee"))
    clouds(d, [(8, 8), (70, 16)])
    d.polygon([(36, 34), (60, 34), (48, 60)], fill="#e2b877")
    for i in range(5):
        d.line([(37 + i * 5, 34), (48, 60)], fill="#c99a56", width=1)
    for y in (40, 46, 52):
        half = int((60 - y) * 0.46)
        d.line([(48 - half, y), (48 + half, y)], fill="#c99a56", width=1)
    d.ellipse([32, 18, 64, 40], fill="#fdf3dc")
    d.ellipse([32, 18, 48, 30], fill="#fffaf0")
    d.ellipse([34, 12, 62, 26], fill="#fdf3dc")
    d.ellipse([40, 6, 56, 18], fill="#fdf3dc")
    d.rectangle([32, 32, 64, 36], fill="#f3e4c4")
    d.polygon([(36, 18), (60, 18), (62, 24), (34, 24)], fill="#8fbf86")
    for x, ln in [(36, 8), (42, 4), (47, 10), (53, 5), (58, 7)]:
        d.rectangle([x, 22, x + 2, 22 + ln], fill="#8fbf86")
        d.rectangle([x, 22 + ln, x + 2, 23 + ln], fill="#6f9a70")
    d.rectangle([40, 14, 50, 15], fill="#b9d6a8")
    d.rectangle([70, 38, 72, 40], fill="#8fb58a")
    d.rectangle([72, 36, 74, 38], fill="#b9d6a8")
    d.rectangle([20, 44, 22, 46], fill="#8fb58a")
    sparkles(d, [(20, 24), (80, 26), (84, 44)], "#ffffff")
    return img


def matcha_tin():
    img, d = canvas(["#eaf4e1", "#dfeed3", "#d4e7c5", "#c8dfb6"], ("#efe3cc", "#d9c7a6"))
    clouds(d, [(70, 8), (10, 14)])
    d.rectangle([30, 22, 58, 52], fill="#6f9a70")
    d.rectangle([30, 22, 33, 52], fill="#86b087")
    d.rectangle([54, 22, 58, 52], fill="#597f5b")
    d.rectangle([28, 17, 60, 23], fill="#f2e6d0")
    d.rectangle([28, 17, 60, 18], fill="#ffffff")
    d.ellipse([34, 30, 54, 46], fill="#f6eedc")
    d.polygon([(44, 33), (49, 38), (44, 43), (39, 38)], fill="#6f9a70")
    d.line([(44, 33), (44, 43)], fill="#b9d6a8", width=1)
    d.line([(66, 60), (84, 42)], fill="#d9b88a", width=2)
    d.ellipse([80, 38, 88, 44], fill="#d9b88a")
    d.ellipse([71, 53, 83, 59], fill="#a7cf8f")
    d.ellipse([73, 52, 80, 56], fill="#c3e0ad")
    for x, y in [(66, 56), (86, 56), (62, 58), (88, 50), (76, 60)]:
        d.point((x, y), fill="#9cc58f")
    sparkles(d, [(14, 30), (22, 44), (82, 20)], "#ffffff")
    return img


def teapot():
    img, d = canvas(["#f6ecd2", "#f1e2bd", "#ead6a8", "#e2c997"], ("#c9a373", "#b08658"))
    clouds(d, [(6, 8), (72, 10)], "#fff8e6")
    d.ellipse([28, 26, 62, 54], fill="#b8794a")
    d.ellipse([28, 26, 44, 44], fill="#cc8d5a")
    d.ellipse([34, 21, 56, 31], fill="#a46b3f")
    d.ellipse([41, 17, 49, 23], fill="#d9a06b")
    d.polygon([(30, 36), (18, 28), (16, 31), (29, 44)], fill="#a46b3f")
    d.arc([54, 30, 72, 48], 270, 100, fill="#a46b3f", width=3)
    face(d, 45, 38, "#e8a08a")
    d.rectangle([72, 42, 86, 54], fill="#fff8e6")
    d.rectangle([73, 43, 85, 46], fill="#d9a06b")
    d.rectangle([86, 44, 89, 50], fill="#fff8e6")
    steam(d, 78, 40)
    steam(d, 82, 38)
    for x, y in [(12, 48), (20, 52), (66, 58)]:
        d.polygon([(x, y), (x + 3, y - 2), (x + 5, y + 1), (x + 2, y + 2)], fill="#7e9a58")
    sparkles(d, [(16, 16), (80, 18), (88, 8)], "#ffffff")
    return img


def mocktail():
    img, d = canvas(["#d9ecfa", "#cfe5f6", "#c5def2", "#bcd8ee"], ("#f0e2cc", "#d9c5a3"))
    clouds(d, [(8, 8), (70, 12)])
    d.polygon([(22, 16), (46, 16), (44, 52), (24, 52)], fill="#f7fbff")
    d.polygon([(24, 24), (44, 24), (43, 36), (25, 36)], fill="#ffb79a")
    d.polygon([(25, 36), (43, 36), (44, 52), (24, 52)], fill="#f4789a")
    d.polygon([(24, 30), (44, 30), (43.5, 36), (24.5, 36)], fill="#ff9a8a")
    for x, y in [(26, 18), (34, 19), (29, 25)]:
        d.rectangle([x, y, x + 6, y + 6], fill="#e9f5ff", outline="#bcd8ee")
    d.line([(40, 4), (34, 30)], fill="#8fbf86", width=2)
    d.ellipse([44, 12, 56, 24], fill="#ffd36e", outline="#f2a93b")
    d.line([(50, 12), (50, 24)], fill="#f2a93b", width=1)
    d.line([(44, 18), (56, 18)], fill="#f2a93b", width=1)
    d.polygon([(22, 16), (26, 10), (30, 16)], fill="#9fd08c")
    d.line([(26, 18), (27, 50)], fill="#ffffff", width=1)
    d.rectangle([24, 52, 44, 53], fill="#d9e8f2")
    d.rectangle([62, 38, 80, 52], fill="#e8f1fb")
    d.rectangle([66, 33, 76, 38], fill="#e8f1fb")
    d.rectangle([62, 38, 65, 52], fill="#fdfeff")
    d.rectangle([62, 49, 80, 52], fill="#cfe1f2")
    stems = [(71, 33, 64, 18), (71, 33, 71, 12), (71, 33, 78, 18), (71, 33, 68, 24)]
    for x1, y1, x2, y2 in stems:
        d.line([(x1, y1), (x2, y2)], fill="#7fae6f", width=1)
    for (cx, cy, c) in [(64, 17, "#f4a3b0"), (71, 11, "#fff1b8"), (78, 17, "#ffffff"), (68, 23, "#f4a3b0")]:
        d.rectangle([cx - 2, cy - 1, cx + 2, cy + 1], fill=c)
        d.rectangle([cx - 1, cy - 2, cx + 1, cy + 2], fill=c)
        d.point((cx, cy), fill="#f2a93b")
    d.polygon([(67, 28), (72, 25), (73, 29)], fill="#9fd08c")
    sparkles(d, [(14, 30), (88, 30), (54, 36)], "#ffffff")
    return img


def makku():
    img, d = canvas(["#fbe8e8", "#f7dede", "#f3d3d6", "#efc8cd"], ("#e6c2a2", "#cda37e"))
    clouds(d, [(70, 8), (6, 12)], "#fff5f5")
    d.rectangle([26, 14, 32, 24], fill="#8fc0a2")
    d.rectangle([24, 24, 34, 28], fill="#8fc0a2")
    d.rectangle([20, 28, 38, 52], fill="#a8d5b5")
    d.rectangle([22, 28, 25, 50], fill="#c6e8d0")
    d.rectangle([25, 11, 33, 14], fill="#f4a3b0")
    d.rectangle([22, 36, 36, 44], fill=WHITE)
    d.rectangle([25, 38, 33, 41], fill="#f4a3b0")
    d.pieslice([44, 23, 82, 59], 0, 180, fill="#e6edf5")
    d.rectangle([48, 46, 54, 52], fill="#f4f8fc")
    d.ellipse([44, 36, 82, 46], fill="#cfd9e6")
    d.ellipse([47, 37, 79, 45], fill="#fdf7ec")
    d.ellipse([52, 38, 66, 42], fill="#ffffff")
    d.rectangle([56, 58, 70, 59], fill="#cfd9e6")
    steam(d, 52, 30, "#ffffff")
    sparkles(d, [(12, 18), (88, 28), (44, 14), (86, 56)], "#ffffff")
    return img


def peach_milk_tea():
    img, d = canvas(["#ffe9d6", "#ffdfc7", "#ffd4b8", "#ffc8a8"], ("#f1cfae", "#dcb28a"))
    clouds(d, [(6, 10), (72, 8)], "#fff6ec")
    d.polygon([(22, 18), (52, 18), (49, 52), (25, 52)], fill="#fff8f0")
    d.polygon([(24, 26), (50, 26), (49, 36), (25, 36)], fill="#e9c79c")
    d.polygon([(25, 36), (49, 36), (49, 52), (25, 52)], fill="#d6a574")
    for x, y in [(26, 19), (34, 20), (41, 19), (29, 28), (38, 30)]:
        d.rectangle([x, y, x + 6, y + 6], fill="#fffdf8", outline="#f3dcc2")
    d.line([(44, 4), (38, 28)], fill="#f4a3b0", width=2)
    d.line([(27, 20), (28, 48)], fill="#ffffff", width=1)
    d.rectangle([25, 52, 49, 53], fill="#e6d6c0")
    d.pieslice([46, 14, 60, 26], 180, 360, fill="#ffa97e")
    d.line([(46, 20), (60, 20)], fill="#f08e66", width=1)
    d.ellipse([66, 34, 90, 56], fill="#ffa97e")
    d.ellipse([66, 34, 80, 48], fill="#ffbf99")
    d.line([(78, 36), (78, 55)], fill="#f08e66", width=1)
    d.ellipse([76, 28, 88, 36], fill="#8fb87a")
    d.polygon([(78, 34), (84, 26), (86, 32)], fill="#a7cf8f")
    sparkles(d, [(12, 22), (60, 14), (92, 20), (16, 48)], "#ffffff")
    return img


def cup(bg, table, liquid):
    img, d = canvas(bg, table)
    d.rectangle([34, 28, 62, 52], fill=WHITE)
    d.rectangle([34, 28, 62, 33], fill=liquid)
    d.rectangle([62, 33, 68, 38], fill=WHITE)
    d.rectangle([66, 33, 69, 46], fill=WHITE)
    d.rectangle([62, 42, 68, 46], fill=WHITE)
    steam(d, 44, 24)
    steam(d, 52, 22)
    sparkles(d, [(16, 20), (82, 16)])
    return img


def save(img, name):
    OUT.mkdir(parents=True, exist_ok=True)
    img.resize((W * SCALE, H * SCALE), Image.NEAREST).save(OUT / f"{name}.png", optimize=True)


def main():
    pink = ["#fbe3e6", "#f8d7dc", "#f5ccd3", "#f1c0ca"]
    tbl = ("#f0d7c0", "#dcbb9c")
    save(boba("#e8b4b8", "#f4cfd2", pink, tbl), "superboba-1")
    save(boba("#cdb4e0", "#e1d0ee", ["#efe6f8", "#e7dbf3", "#decfee", "#d5c4e8"], tbl,
              straw="#f4a3b0"), "superboba-2")
    save(boba("#f3d68a", "#fae6b0", ["#fff3d6", "#ffeabf", "#ffe2a8", "#ffd990"], tbl,
              straw="#8fc0e0"), "superboba-3")
    save(chawan(), "kyohayashiyamatcha-1")
    save(ice_cream_cone(), "aozen-matcha-1")
    save(matcha_tin(), "tagashirachaho-1")
    save(teapot(), "itea-world-1")
    save(mocktail(), "oftea-1")
    save(makku(), "makku-1")
    save(peach_milk_tea(), "shineteameet-1")
    save(cup(["#eaf4fb", "#dff0fa", "#d3e8f5", "#c8e0f0"], tbl, "#b9d6a8"), "generic-matcha")
    save(cup(["#f6ecd2", "#f1e2bd", "#ead6a8", "#e2c997"], ("#c9a373", "#b08658"), "#d9a06b"), "generic-tea")
    save(boba("#e8b4b8", "#f4cfd2", pink, tbl), "generic-boba")


if __name__ == "__main__":
    main()
