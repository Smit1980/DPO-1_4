# -*- coding: utf-8 -*-
"""Слайды урока 5 «Социальная инженерия и безопасность при использовании ИИ» — по образцу lib.py (урок 4)."""
from __future__ import annotations

import html
from typing import Iterable

from lib import paras

E = html.escape
IMG_DIR = "../png/urok5_socialnaya_inzheneriya"

SLIDES5 = {
    0: ("obzor_uroka", "Обзор урока: социальная инженерия и безопасность при использовании ИИ"),
    1: ("ekonomika_ii_atak", "Экономика ИИ-атак: 16 часов против 5 минут"),
    2: ("evolyutsiya_fishinga", "Эволюция фишинга: старые признаки не работают"),
    3: ("klonirovanie_golosa", "Клонирование голоса: три секунды звука"),
    4: ("mekhanika_dialoga", "Психологическая механика убедительного диалога"),
    5: ("krasnye_flagi", "Новые красные флаги ИИ-эры"),
    6: ("eshelonirovannaya_oborona", "Эшелонированная защита: OOB, кодовые слова, канал ИБ"),
    7: ("keys_arup", "Видеозвонок с подделками: разбор кейса на 25 млн $"),
    8: ("algoritm_deystviy", "Алгоритм действий при подозрении на ИИ-атаку"),
    9: ("osint_dose", "Как ИИ собирает досье: конвейер OSINT"),
    10: ("polimorfizm_rassylok", "Полиморфизм: почему каждое письмо уникальное"),
    11: ("temnye_boty", "Тёмные ИИ-боты ведут диалог в реальном времени"),
    12: ("razbor_dialoga", "Разбор диалога: раппорт, контекст, срочность"),
    13: ("priznaki_davleniya_opk", "Признаки давления в переписке предприятия ОПК"),
    14: ("vhod_ustoychivyy_k_fishingu", "Вход, устойчивый к фишингу"),
    15: ("kak_nastroit_kodovoe_slovo", "Как настроить кодовое слово: шаги"),
    16: ("chego_ne_delat", "Чего не делать при подозрении на атаку"),
    17: ("itog_uroka_5", "Итог урока 5 и домашнее задание"),
    18: ("most_k_uroku_4", "Мост к уроку 4: те же риски с точки зрения права"),
}


def img_name5(n: int) -> str:
    return f"{n:02d}_{SLIDES5[n][0]}.jpg"


def slide5(n: int, alt: str, explain: str | Iterable[str], example: str = "", takeaway: str = "") -> str:
    slug, title = SLIDES5[n]
    ex = f'<div class="ex-box"><b>Пример.</b> {example}</div>' if example else ""
    tk = f'<p class="takeaway-line">{takeaway}</p>' if takeaway else ""
    return (
        f'<figure class="img-card fade" data-lightbox id="slide-{n:02d}">'
        f'<img src="{IMG_DIR}/{img_name5(n)}" alt="{E(alt)}" loading="lazy" '
        f'onerror="this.closest(\'.img-card\').classList.add(\'img-missing\')">'
        f'<figcaption class="img-missing-caption">Слайд {n:02d} «{E(title)}»</figcaption></figure>'
        f'<div class="explain fade"><div class="explain-tag">Пояснение к слайду {n:02d}</div>'
        f'{paras(explain)}{ex}{tk}</div>'
    )
