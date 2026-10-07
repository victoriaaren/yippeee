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
    face(d, 48, 31)
    if label:
        d.rectangle([40, 35, 56, 38], fill=label)
    sparkles(d, [(12, 28), (84, 30), (18, 46), (80, 8)])
    return img


def chawan():
    img, d = canvas(["#dff0d8", "#d3e8cb", "#c8e0bf", "#bcd8b3"], ("#e9d9bf", "#d3bf9c"))
    clouds(d, [(70, 6), (8, 10)])
    d.pieslice([24, 26, 72, 58], 0, 180, fill="#f2e6d0")
    d.pieslice([24, 26, 72, 58], 20, 90, fill="#e6d4b4")
    d.ellipse([24, 28, 72, 40], fill="#e6d4b4")
    d.ellipse([27, 29, 69, 38], fill="#8fb58a")
    d.ellipse([32, 31, 54, 36], fill="#b9d6a8")
    for x, y in [(36, 32), (44, 33), (58, 34)]:
        d.rectangle([x, y, x + 1, y], fill="#d6ebc6")
    d.rectangle([36, 56, 60, 57], fill="#d8c5a2")
    d.rectangle([10, 40, 12, 52], fill="#d9b88a")
    d.polygon([(6, 52), (16, 52), (14, 60), (8, 60)], fill="#e8d3a8")
    for x in range(7, 15, 2):
        d.line([(x, 54), (x, 59)], fill="#caa874")
    face(d, 48, 43, "#f3b2b2")
    steam(d, 40, 22, "#ffffff")
    steam(d, 56, 20, "#ffffff")
    sparkles(d, [(84, 30), (16, 26), (80, 14)], "#f4fbe9")
    return img


def iced_latte():
    img, d = canvas(["#d9ecfa", "#cfe5f6", "#c5def2", "#bcd8ee"], ("#eef4f9", "#d3e1ee"))
    clouds(d, [(8, 8), (70, 16)])
    d.rectangle([34, 14, 62, 52], fill="#eaf6ff")
    d.rectangle([35, 36, 61, 51], fill="#fdf6e6")
    d.rectangle([35, 21, 61, 35], fill="#9cc58f")
    d.rectangle([35, 21, 61, 24], fill="#b9d6a8")
    d.rectangle([35, 33, 61, 35], fill="#c9dfb8")
    for x, y in [(37, 14), (46, 16), (53, 14), (41, 22)]:
        d.rectangle([x, y, x + 6, y + 6], fill="#e1f1ff", outline="#b9d8ee")
    d.line([(56, 2), (52, 20)], fill="#f4a3b0", width=3)
    d.line([(37, 15), (38, 48)], fill="#ffffff", width=1)
    d.rectangle([34, 52, 62, 53], fill="#b9d8ee")
    face(d, 48, 42, "#f3c0b2")
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


def nyc_event():
    img, d = canvas(["#bfdcf2", "#cde5f6", "#ddeefa", "#f0f7fc"])
    clouds(d, [(8, 12), (66, 20)])
    for (x, y, w, h, c) in [(2, 36, 12, 28, "#7f9fbc"), (12, 28, 10, 36, "#6e8fae"), (22, 40, 12, 24, "#7f9fbc"),
                            (64, 34, 12, 30, "#7f9fbc"), (74, 24, 8, 40, "#6e8fae"), (82, 38, 14, 26, "#7f9fbc")]:
        d.rectangle([x, y, x + w, y + h], fill=c)
    d.rectangle([77, 18, 78, 24], fill="#6e8fae")
    for (x, y) in [(5, 40), (8, 46), (15, 34), (15, 42), (26, 46), (68, 40), (68, 48), (77, 30), (77, 38), (86, 44)]:
        d.rectangle([x, y, x + 1, y + 1], fill="#fff1b8")
    d.rectangle([0, 54, W, H], fill="#e9d9bf")
    d.line([(0, 4), (48, 12), (96, 4)], fill=INK, width=1)
    for i, c in enumerate(["#f4a3b0", "#fff1b8", "#b9d6a8", "#f4a3b0", "#fff1b8", "#b9d6a8", "#f4a3b0"]):
        x = 8 + i * 13
        y = 4 + int(8 * (1 - ((x - 48) / 48.0) ** 2))
        d.polygon([(x - 2, y), (x + 2, y), (x, y + 5)], fill=c)
    d.rectangle([38, 36, 58, 56], fill=WHITE)
    d.rectangle([38, 36, 58, 39], fill="#f4a3b0")
    d.rectangle([58, 40, 62, 48], fill=WHITE)
    d.rectangle([60, 42, 61, 46], fill="#bfdcf2")
    face(d, 48, 46, "#f3b2b2")
    steam(d, 44, 32)
    steam(d, 52, 30)
    sparkles(d, [(30, 22), (90, 18)], "#ffffff")
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
    d.pieslice([44, 36, 82, 60], 0, 180, fill="#e6edf5")
    d.pieslice([44, 36, 82, 60], 30, 90, fill="#cfd9e6")
    d.ellipse([44, 36, 82, 46], fill="#cfd9e6")
    d.ellipse([47, 37, 79, 44], fill="#fdf7ec")
    d.ellipse([52, 38, 66, 42], fill="#ffffff")
    face(d, 63, 47, "#f3b2b2")
    steam(d, 52, 30, "#ffffff")
    sparkles(d, [(12, 18), (88, 28), (44, 14), (86, 56)], "#ffffff")
    return img


def peach_milk_tea():
    img, d = canvas(["#ffe9d6", "#ffdfc7", "#ffd4b8", "#ffc8a8"], ("#f1cfae", "#dcb28a"))
    clouds(d, [(6, 10), (72, 8)], "#fff6ec")
    d.rectangle([24, 22, 54, 52], fill=WHITE)
    d.rectangle([24, 22, 27, 52], fill="#f1e6d6")
    d.rectangle([54, 28, 62, 34], fill=WHITE)
    d.rectangle([60, 28, 63, 44], fill=WHITE)
    d.rectangle([54, 40, 62, 44], fill=WHITE)
    d.rectangle([56, 31, 59, 41], fill="#ffd4b8")
    d.rectangle([26, 24, 52, 32], fill="#d6a574")
    d.rectangle([26, 24, 52, 25], fill="#e8c298")
    d.rectangle([24, 52, 54, 53], fill="#e6d6c0")
    face(d, 39, 40, "#f4a3b0")
    steam(d, 34, 18)
    steam(d, 44, 16)
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
    face(d, 48, 40)
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
    save(boba("#e8b4b8", "#f4cfd2", pink, tbl, label="#f4a3b0"), "superboba-1")
    save(boba("#cdb4e0", "#e1d0ee", ["#efe6f8", "#e7dbf3", "#decfee", "#d5c4e8"], tbl,
              straw="#f4a3b0", label="#ffffff"), "superboba-2")
    save(boba("#f3d68a", "#fae6b0", ["#fff3d6", "#ffeabf", "#ffe2a8", "#ffd990"], tbl,
              straw="#8fc0e0", label="#f4a3b0"), "superboba-3")
    save(chawan(), "kyohayashiyamatcha-1")
    save(iced_latte(), "aozen-matcha-1")
    save(matcha_tin(), "tagashirachaho-1")
    save(teapot(), "itea-world-1")
    save(nyc_event(), "oftea-1")
    save(makku(), "makku-1")
    save(peach_milk_tea(), "shineteameet-1")
    save(cup(["#eaf4fb", "#dff0fa", "#d3e8f5", "#c8e0f0"], tbl, "#b9d6a8"), "generic-matcha")
    save(cup(["#f6ecd2", "#f1e2bd", "#ead6a8", "#e2c997"], ("#c9a373", "#b08658"), "#d9a06b"), "generic-tea")
    save(boba("#e8b4b8", "#f4cfd2", pink, tbl), "generic-boba")


if __name__ == "__main__":
    main()
