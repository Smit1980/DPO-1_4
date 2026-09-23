# -*- coding: utf-8 -*-
"""png/urok5/N.png (N = 0..8) → png/urok5_socialnaya_inzheneriya/NN_slug.jpg. Отсутствующие слайды пропускаются (страница покажет заглушку)."""
import sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_urok5 import img_name5, SLIDES5

ROOT = Path(__file__).resolve().parents[1]
SRC, DST = ROOT / "png" / "urok5", ROOT / "png" / "urok5_socialnaya_inzheneriya"

def main():
    DST.mkdir(parents=True, exist_ok=True)
    have = []
    for n in SLIDES5:
        src = SRC / f"{n}.png"
        if src.is_file():
            im = Image.open(src).convert("RGB")
            if im.width > 2000:
                im = im.resize((2000, round(im.height * 2000 / im.width)))
            im.save(DST / img_name5(n), quality=86, optimize=True, progressive=True)
            have.append(n)
    print(f"  ✓ слайдов принято: {len(have)} из {len(SLIDES5)}", "; нет: " + ", ".join(map(str, sorted(set(SLIDES5) - set(have)))) if len(have) < len(SLIDES5) else "")

if __name__ == "__main__":
    main()
