# -*- coding: utf-8 -*-
"""Помощники разметки для страницы урока 4 (стиль пар 1–2)."""
from __future__ import annotations

import html
from typing import Iterable

E = html.escape

IMG_DIR = "../png/urok4_podgotovka_i_riski"

# Слайды: номер → (slug, заголовок). Имена файлов — NN_slug.jpg; исходник пользователя — png/urok4/N.png
SLIDES = {
    0: ("obzor_uroka", "Обзор урока: подготовка информации для работы с ИИ"),
    1: ("chto_uhodit_s_faylom", "Что уходит вместе с файлом"),
    2: ("pyat_voprosov_pered_zagruzkoy", "Пять вопросов перед загрузкой"),
    3: ("gde_zhivut_metadannye", "Где хранятся метаданные"),
    4: ("shest_mest_skrytyh_dannyh", "Шесть мест, где файл выдаёт лишнее"),
    5: ("pryamye_i_kosvennye_priznaki", "Прямые и косвенные признаки"),
    6: ("chetyre_priema_obezlichivaniya", "Четыре приёма подготовки данных"),
    7: ("shablon_zaprosa", "Шаблон запроса и роль"),
    8: ("kuda_popadaet_zapros", "Куда попадает запрос"),
    9: ("nastroyki_v_tryoh_modelyah", "Настройки в трёх моделях"),
    10: ("pasport_bezopasnoy_zadachi", "Паспорт безопасной задачи"),
    11: ("komu_prinadlezhit_rezultat", "Кому принадлежит результат ИИ"),
    12: ("svetofor_ispolzovaniya", "Светофор использования материала"),
    13: ("kak_ii_oshibaetsya", "Как ИИ ошибается"),
    14: ("chetyre_shaga_proverki_fakta", "Как проверить факт: четыре шага"),
    15: ("otkuda_predvzyatost", "Откуда берётся предвзятость"),
    16: ("test_pomenyay_odnu_detal", "Тест «поменяй одну деталь»"),
    17: ("chto_umeyut_poddelyvat", "Что умеют подделывать"),
    18: ("proverka_porucheniya", "Проверка поручения"),
    19: ("tsepochka_otvetstvennosti", "Цепочка ответственности"),
    20: ("pyat_proverok_rezultata", "Пять проверок результата ИИ"),
    21: ("otkrytie_uroka", "Открытие урока: цепочка от задачи до решения"),
    22: ("otkrytie_pary_2", "Открытие пары 2"),
    23: ("zaversheniye_uroka", "Итог урока и домашнее задание"),
    24: ("katalog_podelok", "Каталог подделок и вредоносных сценариев"),
    25: ("instruktsiya_vnutri_faila", "Инструкция внутри файла"),
    26: ("praktikum_poryadok_raboty", "Практикум: порядок работы"),
    27: ("rol_dlya_chego", "Роль в промпте: для чего она нужна"),
}


def img_name(n: int) -> str:
    return f"{n:02d}_{SLIDES[n][0]}.jpg"


def paras(text: str | Iterable[str], style: str = "font-size:.95rem;line-height:1.75") -> str:
    items = [text] if isinstance(text, str) else list(text)
    return "".join(f'<p style="{style}">{t}</p>' for t in items)


def slide(n: int, alt: str, explain: str | Iterable[str], example: str = "", takeaway: str = "") -> str:
    """Слайд-картинка + раскрытие темы «Пояснение к слайду» (как на странице урока 1)."""
    slug, title = SLIDES[n]
    ex = f'<div class="ex-box"><b>Пример.</b> {example}</div>' if example else ""
    tk = f'<p class="takeaway-line">{takeaway}</p>' if takeaway else ""
    return (
        f'<figure class="img-card fade" data-lightbox id="slide-{n:02d}">'
        f'<img src="{IMG_DIR}/{img_name(n)}" alt="{E(alt)}" loading="lazy" '
        f'onerror="this.closest(\'.img-card\').classList.add(\'img-missing\')">'
        f'<figcaption class="img-missing-caption">Слайд {n:02d} «{E(title)}»</figcaption></figure>'
        f'<div class="explain fade"><div class="explain-tag">Пояснение к слайду {n:02d}</div>'
        f'{paras(explain)}{ex}{tk}</div>'
    )


def card(title: str, body: str, cls: str = "") -> str:
    return f'<div class="card fade {cls}"><h3>{title}</h3>{body}</div>'


def table(caption: str, head: list[str], rows: list[list[str]]) -> str:
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join(
        "<tr>" + "".join((f'<td class="t">{c}</td>' if i == 0 else f"<td>{c}</td>") for i, c in enumerate(r)) + "</tr>"
        for r in rows
    )
    return (f'<div class="fine-table-wrap fade"><table class="fine-table"><caption>{caption}</caption>'
            f"<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>")


def sources(links: list[tuple[str, str]]) -> str:
    li = "".join(f'<li><a class="svc-link" href="{u}" target="_blank" rel="noopener">{E(t)}</a></li>' for t, u in links)
    return f'<ul class="src-list">{li}</ul>'


def real_case(title: str, when: str, what: str, lesson: str, links: list[tuple[str, str]], kind: str = "Реальный случай") -> str:
    return (f'<div class="case-real fade"><div class="case-real-head"><span class="case-tag">{kind}</span>'
            f'<span class="case-when">{E(when)}</span></div><h3>{title}</h3>'
            f'<p><b>Что произошло.</b> {what}</p><p><b>Что это значит для вас.</b> {lesson}</p>'
            f'<div class="case-src"><b>Источники:</b>{sources(links)}</div></div>')


def interactive(num: str, title: str, what: str, how: list[str], expect: str, demo: str, height: int, label: str) -> str:
    """Пояснение к интерактиву + встроенное демо. Слушателю сразу понятно, что это и что делать."""
    steps = "".join(f"<li>{s}</li>" for s in how)
    return (
        f'<div class="inter-card fade"><div class="inter-head"><span class="inter-tag">Интерактив {num}</span>'
        f'<b>{title}</b></div>'
        f'<div class="inter-grid"><div><h4>Что это</h4><p>{what}</p></div>'
        f'<div><h4>Как работать</h4><ol class="step-list">{steps}</ol></div>'
        f'<div><h4>Что вы должны увидеть</h4><p>{expect}</p></div></div></div>'
        f'<div class="viz fade"><div class="viz-bar"><div class="dots"><span class="dot dr"></span><span class="dot dy"></span>'
        f'<span class="dot dg"></span></div><span class="viz-lbl">{E(label)}</span>'
        f'<button type="button" class="viz-fs" data-fs-src="{demo}" data-fs-title="{E(label)}">⛶ На весь экран</button></div>'
        f'<iframe src="{demo}" height="{height}" data-autofit loading="lazy" title="{E(label)}"></iframe></div>'
    )


def practice(num: str, title: str, situation: str, steps: list[str], expect: list[str], extra: str = "", key: str = "") -> str:
    st = "".join(f"<li>{s}</li>" for s in steps)
    ex = "".join(f"<li>{s}</li>" for s in expect)
    k = ""
    if key:
        k = (f'<details class="details-key fade"><summary>Разбор практики {num} <span class="hint">откройте после выполнения</span>'
             f'</summary><div class="body">{key}</div></details>')
    return (
        f'<div class="prac fade"><div class="prac-head"><span class="prac-tag">Практика {num}</span><b>{title}</b></div>'
        f'<div class="prac-sit"><h4>Ситуация</h4>{situation}</div>'
        f'<div class="prac-cols"><div><h4>Что делаем</h4><ol class="step-list">{st}</ol></div>'
        f'<div><h4>Что должно получиться</h4><ul class="ok-list">{ex}</ul></div></div>{extra}</div>{k}'
    )


def pair_banner(n: int, title: str, theme: str, plan: list[tuple[str, str, str]]) -> str:
    rows = "".join(
        f'<tr><td class="t">{m}</td><td><a class="svc-link" href="#{a}">{E(t)}</a></td></tr>' for m, t, a in plan
    )
    return (f'<section class="pair-banner fade" id="pair{n}"><div class="pair-num">Пара {n}</div>'
            f'<div class="pair-body"><h2>{title}</h2><p>{theme}</p>'
            f'<table class="fine-table pair-plan"><caption>План пары {n} · 90 минут</caption>'
            f'<thead><tr><th>Минуты</th><th>Блок</th></tr></thead><tbody>{rows}</tbody></table></div></section>')


def sec(sid: str, num: str, title: str, desc: str, body: str, minutes: str = "") -> str:
    try:
        from content_extra import EXTRA
        body = body + EXTRA.get(sid, lambda: "")()
    except ImportError:
        pass
    chip = f' <span class="time-chip">{minutes}</span>' if minutes else ""
    return (f'<section class="sec" id="{sid}"><div class="sec-head fade"><div class="num-badge n{num if num.isdigit() else 0}">{num}</div>'
            f'<h2 class="sec-title">{title}{chip}</h2><p class="sec-desc">{desc}</p></div>{body}</section>')


def steps(items: list[str]) -> str:
    return '<ol class="step-list">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def bullets(items: list[str]) -> str:
    return '<ul class="q-bul">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def rule(title: str, text: str) -> str:
    return f'<div class="rule-card fade"><p><strong>{title}</strong>{text}</p></div>'


def note(title: str, text: str) -> str:
    return f'<div class="warn-callout fade"><p><strong>{title}</strong>{text}</p></div>'


def key(title: str, body: str) -> str:
    return (f'<details class="details-key fade"><summary>{title} <span class="hint">откройте после выполнения</span></summary>'
            f'<div class="body">{body}</div></details>')


EXTRA_CSS_V4 = r"""
/* УРОК 4 · пары, пояснения к слайдам, интерактивы, практики, реальные случаи */
code{font-family:Consolas,'Courier New',monospace;font-size:.86em;background:var(--indigo-lt);color:var(--indigo-dk);padding:1px 5px;border-radius:5px}
.prompt-desc{padding:8px 16px 0;color:#94a3b8;font-size:.8rem}
.pair-banner{display:flex;gap:22px;align-items:stretch;margin:56px auto 8px;max-width:1080px;padding:0 24px}
.pair-num{flex:0 0 120px;display:flex;align-items:center;justify-content:center;text-align:center;border-radius:20px;background:linear-gradient(135deg,var(--indigo),var(--cyan));color:#fff;font-size:1.35rem;font-weight:900;letter-spacing:.02em;padding:18px}
.pair-body{flex:1;background:var(--card);border:1px solid var(--border);border-radius:20px;padding:22px 26px;box-shadow:0 2px 10px rgba(15,23,42,.05)}
.pair-body h2{font-size:clamp(1.15rem,2.4vw,1.5rem);font-weight:900;margin-bottom:6px}
.pair-body p{color:var(--muted);line-height:1.65;margin-bottom:14px;font-size:.95rem}
.pair-plan{width:100%}
.pair-end{max-width:1080px;margin:40px auto 0;padding:0 24px;text-align:center;color:var(--muted);font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:.8rem}
.pair-end span{display:block;border-top:2px dashed #cbd5e1;padding-top:14px}
@media(max-width:700px){.pair-banner{flex-direction:column}.pair-num{flex:none;padding:12px}}
.explain{background:var(--card);border:1px solid var(--border);border-left:5px solid var(--indigo);border-radius:14px;padding:18px 22px;margin-top:14px}
.explain-tag{font-size:.74rem;font-weight:800;text-transform:uppercase;letter-spacing:.07em;color:var(--indigo-dk);margin-bottom:8px}
.explain p+p{margin-top:10px}
.ex-box{margin-top:12px;padding:12px 16px;background:var(--cyan-lt);border-radius:10px;font-size:.93rem;line-height:1.65;color:#0c4a6e}
.takeaway-line{margin-top:12px;font-weight:800;color:var(--indigo-dk);font-size:.95rem}
.takeaway-line::before{content:"➜ ";color:var(--cyan)}
.case-real{background:linear-gradient(180deg,#fffdf5,#fff);border:1px solid #fcd34d;border-radius:16px;padding:20px 24px;margin-top:20px}
.case-real-head{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:8px}
.case-tag{background:var(--amber);color:#fff;border-radius:100px;padding:2px 12px;font-size:.72rem;font-weight:800}
.case-when{font-size:.8rem;color:var(--muted);font-weight:700}
.case-real h3{font-size:1.02rem;font-weight:800;margin-bottom:8px}
.case-real p{font-size:.94rem;line-height:1.7;margin-top:6px}
.case-src{margin-top:12px;font-size:.84rem;color:var(--muted)}
.src-list{list-style:none;display:flex;flex-direction:column;gap:3px;margin-top:4px}
.inter-card{background:var(--card);border:1px solid #c7d2fe;border-radius:16px;padding:18px 22px;margin-top:22px}
.inter-head{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:12px}
.inter-tag{background:var(--indigo);color:#fff;border-radius:100px;padding:2px 12px;font-size:.72rem;font-weight:800}
.inter-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}
.inter-grid h4,.prac h4{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--indigo-dk);margin-bottom:6px}
.inter-grid p,.prac-sit p{font-size:.92rem;line-height:1.65}
.inter-card+.viz{margin-top:10px}
.prac{background:var(--card);border:2px solid var(--indigo);border-radius:18px;padding:20px 24px;margin-top:24px}
.prac-head{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:12px;font-size:1.02rem}
.prac-tag{background:linear-gradient(135deg,var(--indigo),var(--cyan));color:#fff;border-radius:100px;padding:3px 14px;font-size:.74rem;font-weight:800}
.prac-sit{background:var(--indigo-lt);border-radius:12px;padding:12px 16px;margin-bottom:14px}
.prac-sit p+p{margin-top:8px}
.prac-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}
.ok-list{list-style:none;display:flex;flex-direction:column;gap:8px}
.ok-list li{position:relative;padding-left:26px;font-size:.93rem;line-height:1.6}
.ok-list li::before{content:"✓";position:absolute;left:0;top:0;color:var(--green);font-weight:900}
.q-bul{padding-left:20px;display:flex;flex-direction:column;gap:6px;font-size:.94rem;line-height:1.65}
.mini-tbl{width:100%;border-collapse:collapse;font-size:.85rem;margin-top:10px}
.mini-tbl th,.mini-tbl td{border:1px solid var(--border);padding:6px 9px;text-align:left;vertical-align:top}
.mini-tbl th{background:#f8fafc}
.data-block{margin-top:12px;background:#0f172a;color:#e2e8f0;border-radius:12px;padding:14px 16px;font-family:Consolas,'Courier New',monospace;font-size:.8rem;line-height:1.6;overflow-x:auto;white-space:pre-wrap}
.pill-r{display:inline-block;padding:1px 9px;border-radius:100px;font-size:.74rem;font-weight:800;background:var(--red-lt);color:var(--red)}
.pill-g{display:inline-block;padding:1px 9px;border-radius:100px;font-size:.74rem;font-weight:800;background:var(--green-lt);color:var(--green)}
.pill-y{display:inline-block;padding:1px 9px;border-radius:100px;font-size:.74rem;font-weight:800;background:var(--amber-lt);color:#b45309}
.three-models{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:12px}
.three-models div{background:#f8fafc;border:1px solid var(--border);border-radius:12px;padding:12px 14px;font-size:.88rem;line-height:1.55}
.three-models b{display:block;margin-bottom:4px}
"""


def deep(title: str, cards: str) -> str:
    """Блок «Углублённый разбор» в конце раздела: материал для развёрнутого рассказа."""
    return (f'<div class="deep-bar fade"><span>🔎 Углублённый разбор</span><b>{title}</b></div>{cards}')


EXTRA_CSS_V4_2 = r"""
.deep-bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:34px 0 4px;padding:10px 16px;border-radius:12px;background:linear-gradient(90deg,#eef2ff,#e0f2fe);border:1px solid #c7d2fe}
.deep-bar span{font-size:.74rem;font-weight:800;text-transform:uppercase;letter-spacing:.07em;color:var(--indigo-dk)}
.deep-bar b{font-size:1rem}
.important{background:linear-gradient(180deg,#fff7ed,#fff);border:2px solid #fb923c;border-radius:16px;padding:18px 22px;margin-top:20px}
.important .imp-tag{display:inline-block;background:#f97316;color:#fff;border-radius:100px;padding:2px 12px;font-size:.74rem;font-weight:800;margin-bottom:8px}
.important p{font-size:.96rem;line-height:1.75}
.important p+p{margin-top:8px}
.copy-inline{float:right;margin:0 0 6px 10px}
.db-wrap{position:relative}
.db-wrap .copy-btn{position:absolute;right:10px;top:10px}
.pk-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:14px}
.pk-grid .prompt-box pre{max-height:320px;overflow:auto}
.case-mini{border:1px solid var(--border);border-radius:14px;background:#fff;padding:16px 20px;margin-top:14px}
.case-mini h4{font-size:.95rem;font-weight:800;margin-bottom:6px}
.case-mini .meta{font-size:.78rem;font-weight:800;color:var(--indigo-dk);text-transform:uppercase;letter-spacing:.06em}
"""
