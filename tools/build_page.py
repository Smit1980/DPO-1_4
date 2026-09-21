# -*- coding: utf-8 -*-
"""Сборка страницы урока 4 для слушателей (без преподавательского слоя).

Запуск из корня проекта:  py tools/build_page.py
Результат: web/urok4_podgotovka_i_riski.html и демо в web/.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shell  # noqa: E402
import demos  # noqa: E402
import prompts as P  # noqa: E402
from lib import EXTRA_CSS_V4, img_name, SLIDES, pair_banner, table  # noqa: E402
from content_p1 import P1_PLAN, pair1_sections  # noqa: E402
from content_p2 import P2_PLAN, pair2_sections  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
OUT = ROOT / "web" / "urok4_podgotovka_i_riski.html"
BASE = "https://smit1980.github.io/DPO-1_4"
E = html.escape

SCRIPT = shell.SCRIPT.replace('feedback.textContent = (isCorrect ? "Верно. " : "Не совсем. ") + QUIZ_EXPLAIN[index];',
                              'feedback.textContent = (isCorrect ? "Верно. " : "Не совсем. ") + (question.dataset.explain || "");')
assert "question.dataset.explain" in SCRIPT
SCRIPT = SCRIPT.replace('const QUIZ_EXPLAIN = {', 'const QUIZ_EXPLAIN_UNUSED = {')


def prompt_box(p: dict) -> str:
    pid = p["id"].lower()
    return (f'<div class="prompt-box fade"><div class="prompt-head"><span>{p["id"]} · {E(p["title"])}</span>'
            f'<button type="button" class="copy-btn" data-copy="prompt-{pid}">Копировать</button></div>'
            f'<p class="prompt-desc">{E(p["description"])}</p><pre id="prompt-{pid}">{E(p["content"])}</pre></div>')


SHORT = {'s1':'Файл','s2':'Метаданные','s3':'Обезличивание','s4':'Условные данные','s5':'История и настройки','s6':'Паспорт задачи',
         's7':'Авторское право','s8':'Достоверность','s9':'Предвзятость','s10':'Дипфейки','s11':'Ответственность'}

NAV = ('<nav class="top" aria-label="Навигация по странице">'
       '<a class="nav-link" href="../index.html">← Главная</a><span class="nav-sep"></span>'
       '<span class="nav-logo">Урок 4 · ИИ: данные и риски</span><span class="nav-sep"></span>'
       '<a class="nav-link" href="#pair1">Пара 1</a>'
       + "".join(f'<a class="nav-link" href="#{a}">{SHORT[a]}</a>' for _, t, a in P1_PLAN)
       + '<span class="nav-sep"></span><a class="nav-link" href="#pair2">Пара 2</a>'
       + "".join(f'<a class="nav-link" href="#{a}">{SHORT[a]}</a>' for _, t, a in P2_PLAN)
       + '<span class="nav-sep"></span><a class="nav-link" href="#dl">Файлы</a><a class="nav-link" href="#checklist">Чек-лист</a>'
         '<a class="nav-link" href="#quiz">Квиз</a></nav>')

HERO = f"""<header id="hero">
  <div class="hero-badges">
    <span class="hero-badge">ДПО-1 · Темы 2 и 3</span>
    <span class="hero-badge">Две пары · 2 × 90 минут</span>
    <span class="hero-badge">GigaChat · DeepSeek · ChatGPT</span>
    <span class="hero-badge">Для специалистов предприятий ОПК</span>
  </div>
  <h1 class="hero-title">Подготовьте данные <em>до</em> запроса и проверьте результат <em>после</em></h1>
  <p class="hero-sub">Пара 1 отвечает на вопрос «что и в каком виде можно передать ИИ?». Пара 2 — «что делать с результатом, который вернул ИИ?». Сквозная цепочка: <b>задача → роль ИИ → подготовка информации → результат → проверка рисков → решение человека</b>.</p>
  <nav class="hero-nav" aria-label="Разделы страницы">
    <a href="#pair1">▶ Пара 1 · Подготовка данных</a>
    <a href="#s2">Метаданные файла</a>
    <a href="#s3">Обезличивание</a>
    <a href="#pair2">▶ Пара 2 · Правовые риски</a>
    <a href="#s8">Проверка ответа ИИ</a>
    <a href="#s10">Дипфейки</a>
    <a href="#dl">📄 Файлы для скачивания</a>
  </nav>
</header>"""

PAIR1 = pair_banner(1, "Пара 1 · Подготовка информации для передачи в ИИ",
                    "Обезличивание, обобщение и условные данные. Правила загрузки документов: только необходимая информация. История запросов, настройки хранения и конфиденциальность. Ответственный подход к корпоративной информации.",
                    P1_PLAN)
PAIR2 = pair_banner(2, "Пара 2 · Правовые и репутационные риски применения ИИ",
                    "Авторское право и материалы, созданные ИИ. Синтетический контент и недостоверная информация. Ошибочные, предвзятые и дискриминационные результаты. Дипфейки, имитация голоса и изображения. Ответственность пользователя за итоговый результат.",
                    P2_PLAN)
PAIR_END = '<div class="pair-end"><span>Конец пары 1 · Начало пары 2</span></div>'

DL = """<section class="sec" id="dl">
  <div class="sec-head fade">
    <div class="num-badge n0">↓</div>
    <h2 class="sec-title">Файлы для скачивания</h2>
    <p class="sec-desc">Учебные файлы для практик и памятки. Все данные в файлах вымышлены. Памятки не заменяют политику информационной безопасности Концерна ВКО «Алмаз – Антей» и локальные акты предприятия.</p>
  </div>
  <div class="dl-grid fade">
    <a class="dl" href="../data/urok4/pamyatka_1_pered_otpravkoy_v_ii.pdf" download><span class="ico">🚦</span><div><b>Памятка 1 · Перед отправкой в ИИ</b><span>PDF · пять вопросов, четыре приёма, метаданные, если данные уже ушли</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/pamyatka_2_proverka_rezultata_ii.pdf" download><span class="ico">✅</span><div><b>Памятка 2 · Проверка результата ИИ</b><span>PDF · пять проверок, проверка факта, тест «поменяй деталь», проверка поручения</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/pasport_bezopasnoy_zadachi.docx" download><span class="ico">📋</span><div><b>Паспорт безопасной задачи</b><span>DOCX · бланк и заполненный образец</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/prompty_urok4.docx" download><span class="ico">⌨️</span><div><b>Промпты урока 4</b><span>DOCX · десять шаблонов: письмо, записка, проверка, роль</span></div><span class="arrow">↓</span></a>
  </div>
  <div class="dl-grid fade">
    <a class="dl" href="../data/urok4/zayavka_uchebnaya_s_metadannymi.docx" download><span class="ico">📝</span><div><b>zayavka_uchebnaya_s_metadannymi.docx</b><span>Для практики 2: скрытое внутри файла</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/zhurnal_zayavok_uchebnyj.xlsx" download><span class="ico">📊</span><div><b>zhurnal_zayavok_uchebnyj.xlsx</b><span>Для практики 3: журнал заявок, в файле есть скрытый лист</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/zhurnal_zayavok_bezopasnyj.csv" download><span class="ico">🧾</span><div><b>zhurnal_zayavok_bezopasnyj.csv</b><span>Образец безопасной таблицы (ключ практики 3)</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/foto_uchebnoe_s_exif.jpg" download><span class="ico">📷</span><div><b>foto_uchebnoe_s_exif.jpg</b><span>Учебное фото со скрытыми данными съёмки (EXIF)</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4/prompty_urok4.txt" download><span class="ico">📄</span><div><b>prompty_urok4.txt</b><span>Те же промпты одним текстом</span></div><span class="arrow">↓</span></a>
    <a class="dl" href="../data/urok4_materialy.zip" download><span class="ico">🗜️</span><div><b>urok4_materialy.zip</b><span>Все файлы урока одним архивом</span></div><span class="arrow">↓</span></a>
  </div>
</section>"""

CHECK_ITEMS_A = [
    "Могу назвать, что именно нужно ИИ для этой задачи, — и передаю только это",
    "Взял фрагмент, а не документ целиком, если хватает фрагмента",
    "Убрал прямые признаки (ФИО, телефон, почта, номера) и проверил сочетания",
    "Заменил или обобщил то, что нужно для смысла, но не нужно в точном виде",
    "Проверил метаданные: свойства, примечания, скрытый текст, колонтитулы, имя файла",
    "Знаю режим хранения и настройки конкретного сервиса; понимаю, что «обучение выключено» ≠ «данные удалены»",
    "Инструмент допустим по политике безопасности предприятия; если не уверен — уточнил у ответственного",
]
CHECK_ITEMS_B = [
    "Проверил факты, цифры и ссылки по первоисточнику — не повторным запросом к той же модели",
    "Проверил, что материал не содержит чужих узнаваемых элементов и что условия использования допускают мой случай",
    "Если результат касается людей, проверил критерии и сделал тест «поменяй одну деталь»",
    "Необычное поручение подтвердил по независимому каналу",
    "Понимаю, что подпись и отправка — моя ответственность",
]


def checklist() -> str:
    def group(title: str, items: list[str], start: int) -> str:
        li = "".join(f'<li><label><input type="checkbox" data-checklist-item="c{start + i}"> {t}</label></li>' for i, t in enumerate(items))
        return f'<div class="check-group"><h3>{title}</h3><ul class="checklist-items">{li}</ul></div>'
    return ('<section class="sec" id="checklist"><div class="sec-head fade"><div class="num-badge n10">✓</div>'
            '<h2 class="sec-title">Мой чек-лист</h2><p class="sec-desc">Отметки сохраняются в вашем браузере. Пройдите список перед отправкой запроса и перед использованием результата.</p></div>'
            '<div class="card fade"><div class="checklist-progress-bar"><div class="checklist-progress-fill" id="checklist-progress"></div></div>'
            + group("Перед отправкой в ИИ (пара 1)", CHECK_ITEMS_A, 1)
            + group("Перед использованием результата (пара 2)", CHECK_ITEMS_B, 100)
            + '<p class="checklist-done" id="checklist-done" hidden>Готово — можно работать с ИИ ответственно.</p></div></section>')


QUIZ = [
    ("Вам нужно краткое резюме раздела 4 из внутреннего отчёта на 28 страниц. Что правильно?",
     ["Загрузить все 28 страниц — так «полнее»", "Передать только текст раздела 4, убрав контакты, номера и комментарии", "Загрузить файл, но выключить обучение на диалогах"], 1,
     "Нужен минимум для задачи. Остальные страницы не улучшают результат, но увеличивают объём передаваемого."),
    ("Вы удалили все ФИО из текста письма в Word. Где ФИО всё ещё может остаться?",
     ["Нигде — в тексте их нет", "В свойствах файла, примечаниях, скрытом тексте, колонтитулах и имени файла", "Только в подписи"], 1,
     "Метаданные и скрытые элементы уходят вместе с файлом. Надёжнее вставить фрагмент текста или проверить копию Инспектором документов."),
    ("Коллега предлагает: «Попросим нейросеть обезличить служебную записку, а потом поработаем с обезличенной». Что не так?",
     ["Нейросеть плохо обезличивает", "Чтобы обезличить, ей придётся отправить оригинал — передача уже состоится", "Всё так, это экономит время"], 1,
     "Обезличивать нужно у себя: вручную, «Найти и заменить», встроенные средства Office."),
    ("В настройках ChatGPT вы выключили «Improve the model for everyone». Что это значит?",
     ["Рабочие документы теперь можно загружать", "Данные сразу удаляются", "Модель не учится на диалогах, но они по-прежнему хранятся на серверах сервиса"], 2,
     "Обучение и хранение — разные вопросы. Настройки снижают риск, но не делают публичный сервис допустимым для рабочих документов."),
    ("Начало запроса: «Ты — профессор, эксперт по договорам». Что это даёт?",
     ["Ответы модели становятся точнее", "Нельзя вставлять настоящий договор — роль не даёт прав на данные и не повышает точность; полезны критерии и позиция", "Можно не проверять ответ"], 1,
     "Исследование 2024 года на 162 ролях не показало роста точности. Роль полезна как позиция и критерии проверки."),
    ("ИИ указал источник и год для статистики. Как проверить?",
     ["Спросить ту же модель: «Ты уверена?»", "Открыть источник: существует ли он, совпадают ли год и цифра, подтверждает ли он именно это", "Спросить другую модель"], 1,
     "Проверка заканчивается на первоисточнике. Повторный запрос к машине — не проверка."),
    ("Вы отправили ИИ две одинаковые характеристики сотрудников, в которых различается только возраст, и получили разные оценки. Что это показывает?",
     ["Модель хорошо различает людей", "Возраст повлиял на результат при равных деловых качествах — это признак возможной предвзятости", "Ничего: ответы всегда случайны"], 1,
     "Тест «поменяй одну деталь» выявляет зависимость от признаков, не связанных с деловыми качествами."),
    ("Пришло голосовое сообщение «руководителя»: срочно отправьте сводку на новый адрес и никого не подключайте. Что делаете?",
     ["Отправляю: голос знакомый", "Перезваниваю по номеру из сообщения", "Останавливаюсь и подтверждаю поручение по ранее известному контакту; при подозрении сообщаю в ИБ"], 2,
     "Голос и фото ничего не доказывают. Номер из сообщения — не независимый канал."),
    ("Вы подписали справку с выдуманной ИИ цифрой. Кто отвечает?",
     ["Нейросеть", "Разработчик сервиса", "Тот, кто подписал и отправил документ"], 2,
     "Подпись — принятие ответственности за содержание. «Так написал ИИ» — не аргумент."),
]


def quiz() -> str:
    out = []
    for i, (q, opts, right, why) in enumerate(QUIZ, 1):
        labels = "".join(f'<label><input type="radio" name="q{i}" value="{"right" if j == right else "wrong"}"> {E(o)}</label>' for j, o in enumerate(opts))
        out.append(f'<div class="quiz-question" data-quiz="{i}" data-explain="{E(why, quote=True)}"><p class="quiz-text">{i}. {E(q)}</p>'
                   f'<div class="quiz-options">{labels}</div><button type="button" class="quiz-check" data-quiz-check="{i}">Проверить</button>'
                   f'<p class="quiz-feedback" data-quiz-feedback="{i}" hidden></p></div>')
    return ('<section class="sec" id="quiz"><div class="sec-head fade"><div class="num-badge n11">?</div><h2 class="sec-title">Проверьте себя</h2>'
            f'<p class="sec-desc">{len(QUIZ)} вопросов с разбором. Правильный вариант подсвечивается после ответа.</p></div>'
            f'<div class="quiz fade">{"".join(out)}<p class="quiz-score" id="quiz-score">Отвечено: 0 / {len(QUIZ)}</p></div></section>')


HEAD = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Урок 4 · Подготовка данных для ИИ и правовые риски · 2 пары по 90 минут</title>
<!--
  Лонгрид урока 4 (ДПО-1, темы 2 и 3). Zero-build: весь CSS и JS встроены.
  Собрано скриптом tools/build_page.py — правьте tools/content_p1.py, content_p2.py и пересобирайте.
  Слайды: png/urok4_podgotovka_i_riski/NN_*.jpg (из png/urok4/N.png скриптом tools/build_slides.py).
-->
<style>
"""


def expand_prompts(body: str) -> str:
    for pid, p in P.PROMPT_BY_ID.items():
        body = body.replace(f"{{{{PROMPT:{pid}}}}}", prompt_box(p))
    left = re.findall(r"\{\{[^}]+\}\}", body)
    if left:
        raise SystemExit("нераскрытые плейсхолдеры: " + ", ".join(left))
    return body


def main() -> None:
    demos.build_all()
    body = (NAV + HERO + "<main>" + PAIR1 + pair1_sections() + PAIR_END + PAIR2 + pair2_sections()
            + DL + checklist() + quiz() + "</main>")
    body = expand_prompts(body)
    css = (TOOLS / "base_style.css").read_text(encoding="utf-8")
    tail = shell.TAIL_TMPL
    tail = re.sub(r"<footer>.*?</footer>", (
        "<footer><p>Урок 4 «Подготовка информации для ИИ и правовые риски» · ДПО-1 · Клуб «ИИ в образовании» · 2026</p>"
        "<p style=\"margin-top:6px\">Все данные на странице и в файлах вымышлены. Источники проверены по открытым материалам 21.09.2026; правила сервисов и нормы могут измениться — сверяйте актуальную редакцию.</p>"
        "<p style=\"margin-top:6px\">Учебный материал не заменяет политику информационной безопасности Концерна ВКО «Алмаз – Антей» и локальные акты предприятия и не является юридическим заключением.</p></footer>"),
        tail, flags=re.S)
    page = f"{HEAD}{css}{shell.EXTRA_CSS}{EXTRA_CSS_V4}</style>\n</head>\n<body>\n\n{body}\n{tail}\n<script>{SCRIPT}</script>\n</body>\n</html>\n"
    OUT.write_text(page, encoding="utf-8")
    print("  ✓", OUT.relative_to(ROOT).as_posix(), f"{len(page) // 1024} КБ")


if __name__ == "__main__":
    main()
