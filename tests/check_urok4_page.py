# -*- coding: utf-8 -*-
"""Структурные проверки страницы урока 4 (для слушателей). Запуск: py -m unittest discover -s tests -p "check_*.py" -v"""
import json
import re
import sys
import unittest
import zipfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
PAGE = ROOT / "web" / "urok4_podgotovka_i_riski.html"
TEXT = PAGE.read_text(encoding="utf-8")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.iframes, self.imgs, self.scripts, self.links = [], [], [], [], [], []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if tag == "iframe":
            self.iframes.append(a)
        if tag == "img":
            self.imgs.append(a)
        if tag == "script":
            self.scripts.append(a)
        if tag == "link":
            self.links.append(a)


P_ = P()
P_.feed(TEXT)


class Page(unittest.TestCase):
    def test_ids_unique_and_anchors_resolve(self):
        self.assertEqual(len(P_.ids), len(set(P_.ids)))
        for h in P_.hrefs:
            if h.startswith("#"):
                self.assertIn(h[1:], P_.ids, h)

    def test_pairs_and_sections(self):
        for sid in ["pair1", "pair2"] + [f"s{i}" for i in range(1, 12)] + ["dl", "checklist", "quiz"]:
            self.assertIn(sid, P_.ids)
        self.assertLess(TEXT.index('id="pair1"'), TEXT.index('id="s6"'))
        self.assertLess(TEXT.index('id="s6"'), TEXT.index('id="pair2"'))
        self.assertLess(TEXT.index('id="pair2"'), TEXT.index('id="s7"'))

    def test_pair_plans_sum_to_90(self):
        from content_p1 import P1_PLAN
        from content_p2 import P2_PLAN
        for plan in (P1_PLAN, P2_PLAN):
            edges = [tuple(map(int, m.replace("–", "-").split("-"))) for m, _, _ in plan]
            self.assertEqual(edges[0][0], 0)
            self.assertEqual(edges[-1][1], 90)
            for a, b in zip(edges, edges[1:]):
                self.assertEqual(a[1], b[0])

    def test_twenty_slides_each_explained(self):
        for n in range(0, 31):
            self.assertIn(f'id="slide-{n:02d}"', TEXT)
            self.assertIn(f"Пояснение к слайду {n:02d}", TEXT)
        for im in [i for i in P_.imgs if i.get("src")]:
            self.assertTrue(im.get("alt"), im)
            self.assertIn("onerror", im)

    def test_iframes(self):
        self.assertGreaterEqual(len([f for f in P_.iframes if f.get("src")]), 8)
        for f in [f for f in P_.iframes if f.get("src")]:
            self.assertTrue(f.get("title"))
            self.assertTrue(f.get("height"))
            self.assertIn("data-autofit", f)
            self.assertTrue((ROOT / "web" / f["src"]).is_file(), f["src"])

    def test_every_interactive_explained(self):
        n = len([f for f in P_.iframes if f.get('src')])
        self.assertEqual(TEXT.count('class="inter-card'), n)
        for k in ("Что это", "Как работать", "Что вы должны увидеть"):
            self.assertGreaterEqual(TEXT.count(f"<h4>{k}</h4>"), n)

    def test_no_teacher_layer(self):
        for bad in ["Опорный конспект", "Можно сказать", "Если зал молчит", "Перерыв: после", "Блок для преподавателя",
                    "Чек-лист преподавателя", "план Б", "Вопрос группе", "Где не перегибать", "Чат запросов ведёт"]:
            self.assertNotIn(bad, TEXT, bad)

    def test_no_external_resources(self):
        for s in P_.scripts:
            self.assertNotIn("src", s)
        for l in P_.links:
            self.assertFalse(l.get("href", "").startswith("http"))
        for im in P_.imgs:
            self.assertFalse(im.get("src", "").startswith("http"))

    def test_real_cases_have_sources(self):
        cases = re.findall(r'<div class="case-real fade">.*?</ul></div></div>', TEXT, flags=re.S)
        self.assertGreaterEqual(len(cases), 15)
        for c in cases:
            self.assertIn('href="https://', c)
            self.assertIn("Источники", c)

    def test_local_links_exist(self):
        for h in P_.hrefs:
            if h.startswith(("http", "#", "mailto")):
                continue
            target = (PAGE.parent / h.split("#")[0]).resolve()
            self.assertTrue(target.exists(), h)

    def test_prompts_present(self):
        from prompts import PROMPTS
        for p in PROMPTS:
            self.assertIn(f'id="pk-{p["id"].lower()}"', TEXT)  # нижний блок: все 20 промптов
        for pid in ("u01", "u02", "u03", "u04", "u05", "u06", "u07", "u08", "u09", "u10"):
            self.assertIn(f'id="prompt-{pid}"', TEXT)
        for pid in ("pr1", "pr2", "pr3", "pr4", "pr5", "pr6", "pr7", "prd"):
            self.assertIn(f'id="prompt-{pid}"', TEXT)
        self.assertEqual(len(PROMPTS), 21)
        self.assertIn('id="prompt-analytic"', TEXT)
        self.assertIn('id="prompt-cand"', TEXT)
        self.assertNotIn("{{", TEXT)

    def test_prompts_are_safe(self):
        from prompts import PROMPTS
        for p in PROMPTS:
            self.assertIsNone(re.search(r"\+7\s?\(?\d{3}", p["content"]), p["id"])
            self.assertIsNone(re.search(r"@\w+\.\w+", p["content"]), p["id"])

    def test_copy_targets_exist_and_are_complete(self):
        for target in re.findall(r'data-copy="([^"]+)"', TEXT):
            self.assertIn(f'id="{target}"', TEXT, target)
        self.assertIn("textContent", TEXT)
        self.assertIn("execCommand", TEXT)

    def test_no_presentation_files(self):
        self.assertNotIn("slaydy_urok4", TEXT)
        self.assertEqual(list((ROOT / "data").rglob("*.pptx")) + list((ROOT / "data").rglob("slaydy*")), [])

    def test_all_slide_images_exist(self):
        from lib import SLIDES, img_name
        for n in SLIDES:
            self.assertTrue((ROOT / "png" / "urok4_podgotovka_i_riski" / img_name(n)).is_file(), n)

    def test_role_is_accented(self):
        self.assertIn("Указывайте роль в промпте", TEXT)
        self.assertIn("формат, тон и позицию", TEXT)

    def test_bottom_block_is_last(self):
        self.assertGreater(TEXT.index('id="s13"'), TEXT.index('id="quiz"'))
        self.assertGreater(TEXT.index('id="s13"'), TEXT.index('id="s12"'))
        self.assertLess(TEXT.index('id="slide-00"'), TEXT.index('id="slide-21"'))
        self.assertLess(TEXT.index('id="slide-00"'), TEXT.index('class="hero-title"'))

    def test_three_models_named(self):
        for m in ("GigaChat", "DeepSeek", "ChatGPT"):
            self.assertGreater(TEXT.count(m), 5)

    def test_policy_reference_not_invented(self):
        self.assertIn("политик", TEXT)
        self.assertIn("Концерна ВКО «Алмаз – Антей»", TEXT)

    def test_quiz_has_right_answer_and_explanation(self):
        qs = re.findall(r'<div class="quiz-question".*?</p></div>', TEXT, flags=re.S)
        self.assertGreaterEqual(len(qs), 9)
        for q in qs:
            self.assertEqual(q.count('value="right"'), 1)
            self.assertIn("data-explain=", q)

    def test_slide_prompts_ten_each(self):
        for f, rng in (("para1", range(1, 11)), ("para2", range(11, 21))):
            t = (ROOT / "slides" / f"prompty_slaydov_{f}.md").read_text(encoding="utf-8")
            self.assertEqual(len(re.findall(r"^## \d+\.png", t, flags=re.M)), 10)
            for n in rng:
                self.assertIn(f"## {n}.png", t)

    def test_downloads_zip(self):
        z = zipfile.ZipFile(ROOT / "data" / "urok4_materialy.zip")
        names = z.namelist()
        for n in ("zayavka_uchebnaya_s_metadannymi.docx", "zhurnal_zayavok_uchebnyj.xlsx", "pamyatka_1_pered_otpravkoy_v_ii.pdf",
                  "pamyatka_2_proverka_rezultata_ii.pdf", "prompty_urok4.docx", "foto_uchebnoe_s_exif.jpg"):
            self.assertIn(n, names)

    def test_metadata_docx_has_hidden_traps(self):
        z = zipfile.ZipFile(ROOT / "data" / "urok4" / "zayavka_uchebnaya_s_metadannymi.docx")
        self.assertIn("word/comments.xml", z.namelist())
        self.assertIn("<w:vanish", z.read("word/document.xml").decode("utf-8"))
        self.assertIn("Учебное предприятие", z.read("docProps/app.xml").decode("utf-8"))
        self.assertIn("Комарова", z.read("docProps/core.xml").decode("utf-8"))


class Demos(unittest.TestCase):
    def test_sorter_keys_valid(self):
        for f in ("demo_svetofor_prava", "demo_proverka_otveta", "demo_neobychnoe_poruchenie"):
            t = (ROOT / "web" / f"{f}.html").read_text(encoding="utf-8")
            data = json.loads(re.search(r"const ROUNDS = (.*?);\n/\* /DATA \*/", t, flags=re.S).group(1))
            for rd in data:
                ids = {o["id"] for o in rd["options"]}
                for c in rd["cards"]:
                    self.assertIn(c["key"], ids)
                    self.assertTrue(c["why"])

    def test_demos_offline(self):
        for p in (ROOT / "web").glob("demo_*.html"):
            t = p.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r'<(script|link)[^>]+(src|href)="https?://', t), p.name)
            self.assertNotIn("fetch(", t, p.name)
            self.assertNotIn("XMLHttpRequest", t, p.name)
            self.assertNotIn("parent.", t, p.name)


class Repo(unittest.TestCase):
    def test_teacher_files_ignored(self):
        g = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for x in ("_konspekt_out/", "tools/konspekt_data.py", "Docs/private/", "slides/"):
            self.assertIn(x, g)


if __name__ == "__main__":
    unittest.main()
