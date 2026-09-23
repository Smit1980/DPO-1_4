# -*- coding: utf-8 -*-
"""Сборка части 1 урока 4 для слушателей: «Подготовка информации для работы с ИИ» (пара 1, 90 минут + ДЗ).

Запуск из корня проекта:  py tools/build_page1.py
Результат: web/urok4_1_podgotovka_informacii.html
Использует общий каркас (шапка, стили, скрипты, вспомогательные функции) из build_page.py — правьте content_p1.py и пересобирайте.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell  # noqa: E402
import demos  # noqa: E402
from lib import EXTRA_CSS_V4, EXTRA_CSS_V4_2, slide, pair_banner  # noqa: E402
from content_p1 import P1_PLAN, pair1_sections  # noqa: E402
from content_hw1 import s13a  # noqa: E402
from build_page import HEAD, SCRIPT, checklist, CHECK_ITEMS_A, QUIZ, quiz, expand_prompts  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
OUT = ROOT / "web" / "urok4_1_podgotovka_informacii.html"
BASE = "https://smit1980.github.io/DPO-1_4"

SHORT = {'s1': 'Файл', 's2': 'Метаданные', 's3': 'Обезличивание', 's4': 'Условные данные', 's5': 'История и настройки', 's6': 'Паспорт задачи'}

NAV = ('<nav class="top" aria-label="Навигация по странице">'
       '<a class="nav-link" href="../index.html">← Главная</a><span class="nav-sep"></span>'
       '<span class="nav-logo">Урок 4 · часть 1 из 2</span><span class="nav-sep"></span>'
       + "".join(f'<a class="nav-link" href="#{a}">{SHORT[a]}</a>' for _, t, a in P1_PLAN)
       + '<span class="nav-sep"></span><a class="nav-link" href="#checklist">Чек-лист</a><a class="nav-link" href="#quiz">Квиз</a>'
         '<a class="nav-link" href="#s13">ДЗ и промпты</a>'
         f'<span class="nav-sep"></span><a class="nav-link" href="urok4_2_pravovye_riski.html">Часть 2 →</a></nav>')

HERO = f"""<header id="hero">
  {slide(21, "Слайд «Подготовьте данные до запроса, проверьте результат после»: цепочка из шести шагов — задача, роль ИИ, подготовка информации, результат ИИ, проверка рисков, решение человека; часть 1 — что можно передать ИИ, часть 2 — что делать с результатом",
         ["Слайд задаёт логику всего урока 4, который проходит в двух частях по 90 минут. Шесть карточек — это путь любой задачи с ИИ: <b>задача</b> → <b>роль ИИ</b> → <b>подготовка информации</b> → <b>результат ИИ</b> → <b>проверка рисков</b> → <b>решение человека</b>.",
          "Эта страница — <b>часть 1</b>: она отвечает на вопрос «что можно передать ИИ?» и охватывает первые три карточки. Часть 2 «Правовые и репутационные риски применения ИИ» — на отдельной странице — охватывает последние три."],
         takeaway="Часть 1 — подготовка. Часть 2 (отдельная страница) — проверка результата.")}
  <div class="hero-badges">
    <span class="hero-badge">ДПО-1 · Тема 2</span>
    <span class="hero-badge">Часть 1 из 2 · 90 минут + ДЗ</span>
    <span class="hero-badge">GigaChat · DeepSeek · ChatGPT</span>
    <span class="hero-badge">Для специалистов предприятий ОПК</span>
  </div>
  <h1 class="hero-title">Подготовьте данные <em>до</em> того, как обратились к ИИ</h1>
  <p class="hero-sub">Часть 1 отвечает на вопрос «что и в каком виде можно передать ИИ?». Обезличивание, минимизация, метаданные, условные данные, история запросов и настройки хранения, паспорт безопасной задачи.
  Продолжение — <a class="svc-link" href="urok4_2_pravovye_riski.html">часть 2 «Правовые и репутационные риски применения ИИ»</a>.</p>
  <nav class="hero-nav" aria-label="Разделы страницы">
    <a href="#s1">▶ Что уходит вместе с файлом</a>
    <a href="#s2">Метаданные файла</a>
    <a href="#s3">Обезличивание</a>
    <a href="#s6">Паспорт безопасной задачи</a>
    <a href="#s13">🏠 Домашнее задание</a>
  </nav>
</header>"""

PAIR1 = pair_banner(1, "Часть 1 · Подготовка информации для передачи в ИИ",
                    "Обезличивание, обобщение и условные данные. Правила загрузки документов: только необходимая информация. История запросов, настройки хранения и конфиденциальность. Ответственный подход к корпоративной информации.",
                    P1_PLAN)

CHECKLIST1 = checklist([("Перед отправкой в ИИ", CHECK_ITEMS_A, 1)],
                       desc="Отметки сохраняются в вашем браузере. Пройдите список перед отправкой запроса в ИИ.")
QUIZ1 = quiz(QUIZ[:5])


def main() -> None:
    demos.build_all()
    body = NAV + HERO + "<main>" + PAIR1 + pair1_sections() + CHECKLIST1 + QUIZ1 + s13a() + "</main>"
    body = expand_prompts(body)
    css = (TOOLS / "base_style.css").read_text(encoding="utf-8")
    tail = shell.TAIL_TMPL
    tail = re.sub(r"<footer>.*?</footer>", (
        "<footer><p>Урок 4, часть 1 «Подготовка информации для работы с ИИ» · ДПО-1 · Клуб «ИИ в образовании» · 2026</p>"
        "<p style=\"margin-top:6px\">Продолжение: <a class=\"svc-link\" href=\"urok4_2_pravovye_riski.html\">часть 2 «Правовые и репутационные риски применения ИИ»</a>.</p>"
        "<p style=\"margin-top:6px\">Все данные на странице и в файлах вымышлены. Источники проверены по открытым материалам 21.09.2026; правила сервисов и нормы могут измениться — сверяйте актуальную редакцию.</p>"
        "<p style=\"margin-top:6px\">Учебный материал не заменяет политику информационной безопасности Концерна ВКО «Алмаз – Антей» и локальные акты предприятия и не является юридическим заключением.</p></footer>"),
        tail, flags=re.S)
    head = HEAD.replace("<title>Урок 4 · Подготовка данных для ИИ и правовые риски · 2 пары по 90 минут</title>",
                         "<title>Урок 4 · Часть 1 · Подготовка информации для работы с ИИ · 90 минут</title>")
    page = f"{head}{css}{shell.EXTRA_CSS}{EXTRA_CSS_V4}{EXTRA_CSS_V4_2}</style>\n</head>\n<body>\n\n{body}\n{tail}\n<script>{SCRIPT}</script>\n</body>\n</html>\n"
    OUT.write_text(page, encoding="utf-8")
    print("OK", OUT.relative_to(ROOT).as_posix(), f"{len(page) // 1024} KB")


if __name__ == "__main__":
    main()
