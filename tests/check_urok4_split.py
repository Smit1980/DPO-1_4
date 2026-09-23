# -*- coding: utf-8 -*-
"""Структурные проверки разделённых страниц урока 4 (часть 1 и часть 2). Запуск: py -m unittest discover -s tests -p "check_*.py" -v"""
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
PAGE1 = ROOT / "web" / "urok4_1_podgotovka_informacii.html"
PAGE2 = ROOT / "web" / "urok4_2_pravovye_riski.html"


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.iframes, self.imgs = [], [], [], []

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


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    p = P()
    p.feed(text)
    return text, p


class SplitPagesExist(unittest.TestCase):
    def test_files_exist(self):
        self.assertTrue(PAGE1.is_file())
        self.assertTrue(PAGE2.is_file())


class Page1(unittest.TestCase):
    TEXT, PARSED = parse(PAGE1)

    def test_ids_unique(self):
        self.assertEqual(len(self.PARSED.ids), len(set(self.PARSED.ids)))

    def test_anchors_resolve(self):
        for h in self.PARSED.hrefs:
            if h.startswith("#"):
                self.assertIn(h[1:], self.PARSED.ids, h)

    def test_sections_present(self):
        for sid in ["pair1"] + [f"s{i}" for i in range(1, 7)] + ["checklist", "quiz", "s13"]:
            self.assertIn(sid, self.PARSED.ids)
        self.assertNotIn("pair2", self.PARSED.ids)

    def test_no_unresolved_placeholders(self):
        self.assertNotIn("{{", self.TEXT)

    def test_no_teacher_layer(self):
        for bad in ["Опорный конспект", "Можно сказать", "Если зал молчит", "Перерыв: после", "Блок для преподавателя"]:
            self.assertNotIn(bad, self.TEXT, bad)

    def test_local_links_exist(self):
        for h in self.PARSED.hrefs:
            if h.startswith(("http", "#", "mailto")):
                continue
            target = (PAGE1.parent / h.split("#")[0]).resolve()
            self.assertTrue(target.exists(), h)

    def test_links_to_part2(self):
        self.assertIn("urok4_2_pravovye_riski.html", self.TEXT)

    def test_quiz_five_questions(self):
        self.assertEqual(len(re.findall(r'class="quiz-question"', self.TEXT)), 5)


class Page2(unittest.TestCase):
    TEXT, PARSED = parse(PAGE2)

    def test_ids_unique(self):
        self.assertEqual(len(self.PARSED.ids), len(set(self.PARSED.ids)))

    def test_anchors_resolve(self):
        for h in self.PARSED.hrefs:
            if h.startswith("#"):
                self.assertIn(h[1:], self.PARSED.ids, h)

    def test_sections_present(self):
        for sid in ["pair2"] + [f"s{i}" for i in range(7, 13)] + ["dl", "checklist", "quiz", "s13"]:
            self.assertIn(sid, self.PARSED.ids)
        self.assertNotIn("pair1", self.PARSED.ids)

    def test_no_unresolved_placeholders(self):
        self.assertNotIn("{{", self.TEXT)

    def test_no_teacher_layer(self):
        for bad in ["Опорный конспект", "Можно сказать", "Если зал молчит", "Перерыв: после", "Блок для преподавателя"]:
            self.assertNotIn(bad, self.TEXT, bad)

    def test_local_links_exist(self):
        for h in self.PARSED.hrefs:
            if h.startswith(("http", "#", "mailto")):
                continue
            target = (PAGE2.parent / h.split("#")[0]).resolve()
            self.assertTrue(target.exists(), h)

    def test_links_to_part1(self):
        self.assertIn("urok4_1_podgotovka_informacii.html", self.TEXT)

    def test_quiz_four_questions(self):
        self.assertEqual(len(re.findall(r'class="quiz-question"', self.TEXT)), 4)

    def test_new_legal_content_present(self):
        for marker in ("Пять вопросов к любому ИИ-сервису", "во сколько раз выросла ответственность", "автокодировщики и GAN", "1344.1"):
            self.assertIn(marker, self.TEXT, marker)

    def test_iframes_have_files(self):
        for f in [f for f in self.PARSED.iframes if f.get("src")]:
            self.assertTrue((ROOT / "web" / f["src"]).is_file(), f["src"])


if __name__ == "__main__":
    unittest.main()
