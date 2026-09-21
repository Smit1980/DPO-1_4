# -*- coding: utf-8 -*-
"""png/urok4/N.png (N = 1..20) → png/urok4_podgotovka_i_riski/NN_slug.jpg. Отсутствующие слайды пропускаются (страница покажет заглушку)."""
import sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import img_name, SLIDES

ROOT = Path(__file__).resolve().parents[1]
SRC, DST = ROOT / "png" / "urok4", ROOT / "png" / "urok4_podgotovka_i_riski"

def main():
    DST.mkdir(parents=True, exist_ok=True)
    have = []
    for n in SLIDES:
        src = SRC / f"{n}.png"
        if src.is_file():
            im = Image.open(src).convert("RGB")
            if im.width > 2000:
                im = im.resize((2000, round(im.height * 2000 / im.width)))
            im.save(DST / img_name(n), quality=86, optimize=True, progressive=True)
            have.append(n)
    print(f"  ✓ слайдов принято: {len(have)} из {len(SLIDES)}", "; нет: " + ", ".join(map(str, sorted(set(SLIDES) - set(have)))) if len(have) < len(SLIDES) else "")

if __name__ == "__main__":
    main()
