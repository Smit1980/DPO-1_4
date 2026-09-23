# -*- coding: utf-8 -*-
"""Сборка части 2 урока 4 для слушателей: «Правовые и репутационные риски применения ИИ» (пара 2, 90 минут + ДЗ).

Запуск из корня проекта:  py tools/build_page2.py
Результат: web/urok4_2_pravovye_riski.html
Использует общий каркас (шапка, стили, скрипты, вспомогательные функции) из build_page.py — правьте content_p2.py, extra_p2.py и пересобирайте.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell  # noqa: E402
import demos  # noqa: E402
from lib import EXTRA_CSS_V4, EXTRA_CSS_V4_2, slide, pair_banner  # noqa: E402
from content_practice import s12  # noqa: E402
from content_p2 import P2_PLAN, pair2_sections  # noqa: E402
from content_hw2 import s13b  # noqa: E402
from build_page import HEAD, SCRIPT, checklist, CHECK_ITEMS_B, QUIZ, quiz, expand_prompts  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
OUT = ROOT / "web" / "urok4_2_pravovye_riski.html"
BASE = "https://smit1980.github.io/DPO-1_4"

SHORT = {'s7': 'Авторское право', 's8': 'Достоверность', 's9': 'Предвзятость', 's10': 'Дипфейки', 's11': 'Ответственность'}

NAV = ('<nav class="top" aria-label="Навигация по странице">'
       '<a class="nav-link" href="../index.html">← Главная</a><span class="nav-sep"></span>'
       f'<a class="nav-link" href="urok4_1_podgotovka_informacii.html">← Часть 1</a><span class="nav-sep"></span>'
       '<span class="nav-logo">Урок 4 · часть 2 из 2</span><span class="nav-sep"></span>'
       + "".join(f'<a class="nav-link" href="#{a}">{SHORT[a]}</a>' for _, t, a in P2_PLAN)
       + '<span class="nav-sep"></span><a class="nav-link" href="#s12">Практикум</a><a class="nav-link" href="#dl">Файлы</a>'
         '<a class="nav-link" href="#checklist">Чек-лист</a><a class="nav-link" href="#quiz">Квиз</a><a class="nav-link" href="#s13">ДЗ и промпты</a></nav>')

HERO = f"""<header id="hero">
  {slide(22, "Слайд «Часть 2: можно ли использовать результат ИИ?»: итог части 1 в одной строке; шкала времени из пяти блоков — авторское право 0–18, недостоверные сведения 18–38, предвзятость 38–56, дипфейки 56–76, ответственность 76–90; три живых показа в GigaChat, DeepSeek и ChatGPT",
         ["Эта страница — <b>часть 2</b> урока 4: она отвечает на главный вопрос «можно ли использовать результат ИИ?» и охватывает вторую половину исходной шестишаговой цепочки: результат ИИ, проверка рисков, решение человека. Первая половина — «что можно передать ИИ?» — на отдельной странице, в части 1.",
          "Структура части 2 по минутам: авторское право (0–18), недостоверные сведения (18–38), предвзятость (38–56), дипфейки (56–76), ответственность (76–90). В каждой части — реальные случаи, практика и интерактив; два живых показа проходят в трёх моделях."],
         takeaway="Результат ИИ → риск → проверка → действие человека → решение.")}
  <div class="hero-badges">
    <span class="hero-badge">ДПО-1 · Тема 3</span>
    <span class="hero-badge">Часть 2 из 2 · 90 минут + ДЗ</span>
    <span class="hero-badge">GigaChat · DeepSeek · ChatGPT</span>
    <span class="hero-badge">Для специалистов предприятий ОПК</span>
  </div>
  <h1 class="hero-title">Проверьте результат <em>после</em> того, как получили ответ ИИ</h1>
  <p class="hero-sub">Часть 2 отвечает на вопрос «что делать с результатом, который вернул ИИ?»: авторское право, недостоверные сведения, предвзятость, дипфейки, 152-ФЗ и политика конфиденциальности сервисов, ответственность пользователя.
  Если вы ещё не проходили часть 1 — она на отдельной странице: <a class="svc-link" href="urok4_1_podgotovka_informacii.html">«Подготовка информации для работы с ИИ»</a>.</p>
  <nav class="hero-nav" aria-label="Разделы страницы">
    <a href="#s8">▶ Проверка ответа ИИ</a>
    <a href="#s10">Дипфейки</a>
    <a href="#s11">Ответственность и 152-ФЗ</a>
    <a href="#s12">Практикум 1.3</a>
    <a href="#dl">📄 Файлы для скачивания</a>
  </nav>
</header>"""

PAIR2 = pair_banner(2, "Часть 2 · Правовые и репутационные риски применения ИИ",
                    "Авторское право и материалы, созданные ИИ. Политика конфиденциальности ИИ-сервисов и 152-ФЗ. Синтетический контент и недостоверная информация. Ошибочные, предвзятые и дискриминационные результаты. Дипфейки, имитация голоса и изображения. Ответственность пользователя за итоговый результат.",
                    P2_PLAN)

DL2 = """<section class="sec" id="dl">
  <div class="sec-head fade">
    <div class="num-badge n0">↓</div>
    <h2 class="sec-title">Файлы для скачивания</h2>
    <p class="sec-desc">Учебные файлы для практик и памятки части 2. Все данные в файлах вымышлены. Памятки не заменяют политику информационной безопасности Концерна ВКО «Алмаз – Антей» и локальные акты предприятия.</p>
  </div>
  <div class="dl-grid fade">
    <a class="dl" href="../data/urok4/pamyatka_obezlichivanie_dipfeyki_kak_ne_popast.xlsx" download><span class="ico">📊</span><div><b>Excel-памятка · обезличивание, подделки и дипфейки, как не попасть</b><span>XLSX · 7 листов с цветовой разметкой: принципы, каталог подделок, «не делайте / делайте», реальные случаи, чек-лист</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/pamyatka_2_proverka_rezultata_ii.pdf" download><span class="ico">✅</span><div><b>Памятка 2 · Проверка результата ИИ</b><span>PDF · пять проверок, проверка факта, тест «поменяй деталь», проверка поручения</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/prompty_urok4.docx" download><span class="ico">⌨️</span><div><b>Промпты урока 4</b><span>DOCX · 21 шаблон и 8 промптов практикума</span></div><span class="arrow">↓</span></a>
  </div>
  <div class="dl-grid fade">
    <a class="dl" href="../data/urok4/zhurnal_zayavok_50_uchebnyj.xlsx" download><span class="ico">🗂️</span><div><b>zhurnal_zayavok_50_uchebnyj.xlsx</b><span>Практика 3б: журнал на 50 строк с «ловушкой» — найдите скрытую инструкцию для ИИ</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/zhurnal_zayavok_bezopasnyj.csv" download><span class="ico">🧾</span><div><b>zhurnal_zayavok_bezopasnyj.csv</b><span>Образец безопасной таблицы</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/prompty_urok4.txt" download><span class="ico">📄</span><div><b>prompty_urok4.txt</b><span>Все промпты одним текстом</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4_materialy.zip" download><span class="ico">🗜️</span><div><b>urok4_materialy.zip</b><span>Все файлы урока одним архивом</span></div><span class="arrow">↓</span></a>
  </div>
</section>"""

CHECKLIST2 = checklist([("Перед использованием результата", CHECK_ITEMS_B, 100)],
                       desc="Отметки сохраняются в вашем браузере. Пройдите список перед использованием результата ИИ.")
QUIZ2 = quiz(QUIZ[5:])


def main() -> None:
    demos.build_all()
    body = NAV + HERO + "<main>" + PAIR2 + pair2_sections() + s12() + DL2 + CHECKLIST2 + QUIZ2 + s13b() + "</main>"
    body = expand_prompts(body)
    css = (TOOLS / "base_style.css").read_text(encoding="utf-8")
    tail = shell.TAIL_TMPL
    tail = re.sub(r"<footer>.*?</footer>", (
        "<footer><p>Урок 4, часть 2 «Правовые и репутационные риски применения ИИ» · ДПО-1 · Клуб «ИИ в образовании» · 2026</p>"
        "<p style=\"margin-top:6px\">Часть 1: <a class=\"svc-link\" href=\"urok4_1_podgotovka_informacii.html\">«Подготовка информации для работы с ИИ»</a>.</p>"
        "<p style=\"margin-top:6px\">Все данные на странице и в файлах вымышлены. Источники проверены по открытым материалам 21.09.2026; правила сервисов и нормы могут измениться — сверяйте актуальную редакцию.</p>"
        "<p style=\"margin-top:6px\">Учебный материал не заменяет политику информационной безопасности Концерна ВКО «Алмаз – Антей» и локальные акты предприятия и не является юридическим заключением.</p></footer>"),
        tail, flags=re.S)
    head = HEAD.replace("<title>Урок 4 · Подготовка данных для ИИ и правовые риски · 2 пары по 90 минут</title>",
                         "<title>Урок 4 · Часть 2 · Правовые и репутационные риски применения ИИ · 90 минут</title>")
    page = f"{head}{css}{shell.EXTRA_CSS}{EXTRA_CSS_V4}{EXTRA_CSS_V4_2}</style>\n</head>\n<body>\n\n{body}\n{tail}\n<script>{SCRIPT}</script>\n</body>\n</html>\n"
    OUT.write_text(page, encoding="utf-8")
    print("OK", OUT.relative_to(ROOT).as_posix(), f"{len(page) // 1024} KB")


if __name__ == "__main__":
    main()
