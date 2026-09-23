# -*- coding: utf-8 -*-
"""Структурные проверки страницы урока 5. Запуск: py -m unittest discover -s tests -p "check_*.py" -v"""
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
PAGE = ROOT / "web" / "urok5_socialnaya_inzheneriya.html"
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
    def test_file_exists(self):
        self.assertTrue(PAGE.is_file())

    def test_ids_unique_and_anchors_resolve(self):
        self.assertEqual(len(P_.ids), len(set(P_.ids)))
        for h in P_.hrefs:
            if h.startswith("#"):
                self.assertIn(h[1:], P_.ids, h)

    def test_sections_present(self):
        for sid in ["u1", "u2", "u3", "u4", "src5", "checklist", "quiz", "hw5"]:
            self.assertIn(sid, P_.ids)
        self.assertLess(TEXT.index('id="u1"'), TEXT.index('id="u4"'))
        self.assertLess(TEXT.index('id="u4"'), TEXT.index('id="quiz"'))

    def test_nine_slides_each_explained(self):
        for n in range(0, 9):
            self.assertIn(f'id="slide-{n:02d}"', TEXT)
            self.assertIn(f"Пояснение к слайду {n:02d}", TEXT)
        for im in [i for i in P_.imgs if i.get("src")]:
            self.assertTrue(im.get("alt"), im)
            self.assertIn("onerror", im)

    def test_no_unresolved_placeholders(self):
        self.assertNotIn("{{", TEXT)

    def test_no_teacher_layer(self):
        for bad in ["Опорный конспект", "Можно сказать", "Если зал молчит", "Перерыв: после", "Блок для преподавателя",
                    "Чек-лист преподавателя", "план Б", "Вопрос группе"]:
            self.assertNotIn(bad, TEXT, bad)

    def test_no_external_resources(self):
        for s in P_.scripts:
            self.assertNotIn("src", s)
        for im in P_.imgs:
            self.assertFalse(im.get("src", "").startswith("http"))

    def test_real_cases_have_sources(self):
        cases = re.findall(r'<div class="case-real fade">.*?</ul></div></div>', TEXT, flags=re.S)
        self.assertGreaterEqual(len(cases), 3)
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
        from prompts_urok5 import PROMPTS5
        self.assertEqual(len(PROMPTS5), 6)
        for p in PROMPTS5:
            self.assertIn(f'id="prompt-{p["id"].lower()}"', TEXT)

    def test_prompts_are_safe(self):
        from prompts_urok5 import PROMPTS5
        for p in PROMPTS5:
            self.assertIsNone(re.search(r"\+7\s?\(?\d{3}", p["content"]), p["id"])
            self.assertIsNone(re.search(r"@\w+\.\w+", p["content"]), p["id"])

    def test_copy_targets_exist(self):
        for target in re.findall(r'data-copy="([^"]+)"', TEXT):
            self.assertIn(f'id="{target}"', TEXT, target)

    def test_iframe_reused_demo_exists(self):
        for f in [f for f in P_.iframes if f.get("src")]:
            self.assertTrue((ROOT / "web" / f["src"]).is_file(), f["src"])

    def test_sources_list_has_eleven_links(self):
        block = re.search(r'id="src5".*?</section>', TEXT, flags=re.S).group(0)
        self.assertGreaterEqual(block.count("svc-link"), 11)

    def test_quiz_has_right_answer_and_explanation(self):
        qs = re.findall(r'<div class="quiz-question".*?</p></div>', TEXT, flags=re.S)
        self.assertEqual(len(qs), 6)
        for q in qs:
            self.assertEqual(q.count('value="right"'), 1)
            self.assertIn("data-explain=", q)

    def test_downloads_file_exists(self):
        self.assertTrue((ROOT / "data" / "urok5" / "prompty_urok5.txt").is_file())

    def test_links_urok4_part2(self):
        self.assertIn("urok4_2_pravovye_riski.html", TEXT)


if __name__ == "__main__":
    unittest.main()
