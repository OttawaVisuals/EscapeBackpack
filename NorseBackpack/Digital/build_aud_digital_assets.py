"""Digital art for Aud's leg: the hoard coins and the two faces of Aud's comb.

Coins: each Props/Coins/<id>.svg relief (1000-unit canvas, art within radius 460) on a grey
blank, dark relief for common coins and gold for rare ones, matching the Coin Room key on
Aud's ticket. Comb: the outline from Digital/assets/comb.js (built from Props/Comb), with
its colours written in so it works as a plain image; the back face has no carving.

Run: python NorseBackpack/Digital/build_aud_digital_assets.py
Writes NorseBackpack/Digital/assets/Coin_<id>.svg, Comb_Front.svg, Comb_Back.svg
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
COINS = HERE.parent / "Props" / "Coins"
OUT = HERE / "assets"

RARE = {"02_dirham_rare", "04_denier_rare", "07_raven"}
COIN_IDS = ["01_dirham_common", "02_dirham_rare", "03_denier_common", "04_denier_rare",
            "05_hedeby_ship", "06_york_cross", "07_raven"]
BLANK, RIM, DARK, GOLD = "#a9a9a4", "#7d7d78", "#262b2b", "#e2b83a"
BONE, BONE_EDGE, BONE_CUT, BONE_BACK = "#e2d6bc", "#6e5a3c", "#9a8462", "#d8cbae"


def coin_svg(coin_id):
    src = (COINS / f"{coin_id}.svg").read_text(encoding="utf-8")
    paths = "".join(re.findall(r"<path\b[^>]*/>", src, flags=re.S))
    paths = re.sub(r'\sfill="[^"]*"', "", paths)
    relief = GOLD if coin_id in RARE else DARK
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">'
            f'<circle cx="500" cy="500" r="494" fill="{BLANK}" stroke="{RIM}" stroke-width="12"/>'
            f'<circle cx="500" cy="500" r="472" fill="none" stroke="{RIM}" stroke-width="4" opacity=".6"/>'
            f'<g fill="{relief}">{paths}</g></svg>\n')


def comb_svgs():
    js = (HERE / "assets" / "comb.js").read_text(encoding="utf-8")
    asset = json.loads(js[js.index("{"):js.rindex("}") + 1])
    svg = asset["svg"]
    front = (svg.replace('class="body"', f'class="body" fill="{BONE}" stroke="{BONE_EDGE}" stroke-width=".35"')
                .replace('class="cut"', f'class="cut" fill="{BONE_CUT}"')
                .replace('class="knot"', f'class="knot" fill="{BONE_CUT}"'))
    back = re.sub(r'<path class="cut".*?/>', "", svg, flags=re.S)
    back = re.sub(r'<g class="knot".*?</g>', "", back, flags=re.S)
    back = back.replace('class="body"', f'class="body" fill="{BONE_BACK}" stroke="{BONE_EDGE}" stroke-width=".35"')
    return front, back, asset


def main():
    OUT.mkdir(exist_ok=True)
    for coin_id in COIN_IDS:
        (OUT / f"Coin_{coin_id}.svg").write_text(coin_svg(coin_id), encoding="utf-8")
    front, back, asset = comb_svgs()
    (OUT / "Comb_Front.svg").write_text(front, encoding="utf-8")
    (OUT / "Comb_Back.svg").write_text(back, encoding="utf-8")
    print(f"{len(COIN_IDS)} coins, comb front/back; comb {asset['size_pt']} pt, holes {asset['holes_pt']}")


if __name__ == "__main__":
    main()
