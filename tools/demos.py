# -*- coding: utf-8 -*-
"""Генератор интерактивных демо урока 4 (один HTML на демо, без внешних зависимостей)."""
from __future__ import annotations

import json
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web"

SORTER_TMPL = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<link rel="stylesheet" href="shared.css">
<style>
/* Тренажёр-сортировщик · урок 4 · карточки и ключи — в блоке DATA ниже */
.rounds{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.round-btn{padding:6px 14px;border-radius:100px;border:1px solid var(--border);background:#fff;font:inherit;font-size:.82rem;font-weight:800;color:var(--muted);cursor:pointer}
.round-btn.current{border-color:var(--indigo);background:var(--indigo-lt);color:var(--indigo-dk)}
.progress{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.dot-btn{min-width:38px;padding:5px 9px;border-radius:100px;border:1px solid var(--border);background:#fff;font:inherit;font-size:.78rem;font-weight:800;color:var(--muted);cursor:pointer}
.dot-btn.current{border-color:var(--indigo);color:var(--indigo-dk);background:var(--indigo-lt)}
.dot-btn.ok{background:#dcfce7;border-color:#86efac;color:#166534}
.dot-btn.bad{background:#fee2e2;border-color:#fca5a5;color:#991b1b}
.card{border:1px solid var(--border);border-radius:16px;padding:18px 20px;background:#fff}
.card .num{font-size:.74rem;font-weight:800;text-transform:uppercase;letter-spacing:.6px;color:var(--muted)}
.card h2{font-size:clamp(1.05rem,2.6vw,1.3rem);font-weight:800;margin:4px 0 8px}
.card .text{font-size:1rem;line-height:1.6;color:#1e293b}
.quote{margin-top:10px;padding:10px 14px;border-left:4px solid var(--indigo);background:var(--indigo-lt);border-radius:8px;font-size:.95rem;line-height:1.55}
.choices{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin-top:16px}
.choice{padding:14px 12px;border-radius:14px;border:2px solid var(--border);background:#fff;font:inherit;font-size:.95rem;font-weight:800;cursor:pointer;text-align:center;color:var(--text)}
.choice span{display:block;font-size:1.6rem;line-height:1.1;margin-bottom:4px}
.choice small{display:block;font-weight:500;color:var(--muted);font-size:.76rem;margin-top:2px}
.choice:hover:not(:disabled){border-color:#c7d2fe;transform:translateY(-1px)}
.choice:disabled{cursor:default}
.choice.key{border-color:var(--green);box-shadow:0 0 0 3px #dcfce7}
.choice.picked:not(.key){border-style:dashed;border-color:var(--red);opacity:.85}
.verdict{margin-top:14px;padding:12px 16px;border-radius:12px;font-size:.92rem;line-height:1.6}
.verdict.match{background:var(--green-lt);color:#065f46}
.verdict.diff{background:var(--amber-lt);color:#78350f}
.verdict b{display:block;margin-bottom:2px}
.where{margin-top:8px;font-size:.84rem;color:#0c4a6e;font-weight:700}
.nav{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:14px;flex-wrap:wrap}
.btn{padding:9px 16px;border-radius:10px;border:1px solid #c7d2fe;background:#fff;color:var(--indigo-dk);font:inherit;font-weight:800;font-size:.86rem;cursor:pointer}
.btn:disabled{opacity:.45;cursor:default}
.tally{font-size:.86rem;font-weight:700;color:var(--muted)}
.final{margin-top:14px;padding:12px 16px;border-radius:12px;background:var(--indigo-lt);border:1px solid #c7d2fe;font-size:.92rem;line-height:1.6;color:#312e81}
</style>
</head>
<body>

<h1>__H1__</h1>
<p class="sub">__SUB__</p>

<div class="rounds" id="rounds" role="group" aria-label="Шаги"></div>
<div class="progress" role="group" aria-label="Карточки" id="progress"></div>

<div class="card" aria-live="polite">
  <div class="num" id="num"></div>
  <h2 id="title"></h2>
  <p class="text" id="text"></p>
  <div class="quote" id="quote" hidden></div>
  <div class="where" id="where" hidden></div>
  <div class="choices" id="choices"></div>
  <div class="verdict" id="verdict" hidden></div>
</div>

<div class="nav">
  <button type="button" class="btn" id="prev">← Назад</button>
  <span class="tally" id="tally"></span>
  <button type="button" class="btn" id="next">Дальше →</button>
</div>
<div class="final" id="final" hidden></div>

<p class="takeaway"><b>Главное.</b> __TAKE__</p>

<script>
/* DATA */
const ROUNDS = __DATA__;
/* /DATA */
let r = 0, index = 0;
const picks = ROUNDS.map(() => ({}));
const $ = (id) => document.getElementById(id);

function renderRounds() {
  const box = $("rounds"); box.innerHTML = "";
  if (ROUNDS.length < 2) { box.hidden = true; return; }
  ROUNDS.forEach((rd, i) => {
    const b = document.createElement("button");
    b.type = "button"; b.className = "round-btn" + (i === r ? " current" : ""); b.textContent = rd.name;
    b.addEventListener("click", () => { r = i; index = 0; render(); });
    box.appendChild(b);
  });
}

function render() {
  const rd = ROUNDS[r], card = rd.cards[index], picked = picks[r][index];
  renderRounds();
  $("num").textContent = `${rd.name ? rd.name + " · " : ""}карточка ${index + 1} из ${rd.cards.length}`;
  $("title").textContent = card.title;
  $("text").textContent = card.text;
  const q = $("quote"); q.hidden = !card.quote; q.textContent = card.quote || "";
  const w = $("where"); w.hidden = !card.where; w.textContent = card.where ? "Куда: " + card.where : "";
  const box = $("choices"); box.innerHTML = "";
  rd.options.forEach((o) => {
    const b = document.createElement("button");
    b.type = "button"; b.className = "choice"; b.dataset.id = o.id;
    b.innerHTML = `<span>${o.icon}</span>${o.label}<small>${o.sub || ""}</small>`;
    b.disabled = picked !== undefined;
    if (picked !== undefined) { if (o.id === card.key) b.classList.add("key"); if (o.id === picked) b.classList.add("picked"); }
    b.addEventListener("click", () => { picks[r][index] = o.id; render(); });
    box.appendChild(b);
  });
  const v = $("verdict");
  if (picked !== undefined) {
    const ok = picked === card.key, lab = rd.options.find((o) => o.id === card.key).label;
    v.hidden = false; v.className = "verdict " + (ok ? "match" : "diff");
    v.innerHTML = `<b>${ok ? "Верно: " : "Правильный вариант: "}${lab}</b>${card.why}` + (card.check ? `<br><em>Что проверить и где: ${card.check}</em>` : "");
  } else v.hidden = true;
  const p = $("progress"); p.innerHTML = "";
  rd.cards.forEach((c, i) => {
    const d = document.createElement("button"); d.type = "button";
    const pk = picks[r][i];
    d.className = "dot-btn" + (i === index ? " current" : "") + (pk === undefined ? "" : (pk === c.key ? " ok" : " bad"));
    d.textContent = i + 1; d.addEventListener("click", () => { index = i; render(); });
    p.appendChild(d);
  });
  $("prev").disabled = index === 0; $("next").disabled = index === rd.cards.length - 1;
  const done = Object.keys(picks[r]).length;
  $("tally").textContent = `Разобрано: ${done} из ${rd.cards.length}`;
  const f = $("final");
  if (done === rd.cards.length) {
    const good = rd.cards.filter((c, i) => picks[r][i] === c.key).length;
    f.hidden = false; f.textContent = `Итог: ${good} из ${rd.cards.length} верно. ` + (rd.final || "");
  } else f.hidden = true;
}
$("prev").addEventListener("click", () => { if (index > 0) { index -= 1; render(); } });
$("next").addEventListener("click", () => { if (index < ROUNDS[r].cards.length - 1) { index += 1; render(); } });
render();
</script>
</body>
</html>
"""


def write_sorter(fname: str, title: str, h1: str, sub: str, take: str, rounds: list[dict]) -> None:
    html_ = (SORTER_TMPL.replace("__TITLE__", title).replace("__H1__", h1).replace("__SUB__", sub)
             .replace("__TAKE__", take).replace("__DATA__", json.dumps(rounds, ensure_ascii=False, indent=1)))
    (WEB / fname).write_text(html_, encoding="utf-8")


LIGHT = [
    dict(id="g", icon="🟢", label="Можно", sub="риск невысок"),
    dict(id="y", icon="🟡", label="Проверить", sub="сначала выяснить"),
    dict(id="r", icon="🛑", label="Нельзя", sub="остановиться"),
]

PRAVA_CARDS = [
    dict(title="Внутренняя записка по вашему шаблону", text="Вы попросили ИИ предложить структуру записки, переписали формулировки, проверили факты. Записка идёт руководителю внутри организации.",
         key="g", why="ИИ помогал со структурой, текст переработан и проверен вами, чужих узнаваемых элементов нет.", check="Убедиться, что в тексте нет чужих цитат без ссылки."),
    dict(title="Картинка из нейросети на публичный сайт", text="Иллюстрация для новости на сайте предприятия. Вы не знаете, на каких изображениях учили модель, и не читали условия сервиса.",
         key="y", why="Материал идёт наружу, и вы не знаете ни происхождения, ни условий использования результата.", check="Условия сервиса об использовании результатов; согласование с ответственным за сайт и юридической функцией."),
    dict(title="Слайд с логотипом другой компании", text="На сгенерированной иллюстрации для презентации партнёру виден фрагмент, похожий на логотип известной компании.",
         key="r", why="Товарный знак охраняется; «так нарисовала нейросеть» не снимает вопроса о праве использования.", check="Заменить или убрать изображение; при необходимости обратиться к юристам."),
    dict(title="Платный отраслевой документ — в чат для пересказа", text="У вас есть платный стандарт по лицензии организации. Вы хотите загрузить его в публичный ИИ-сервис, чтобы получить краткий пересказ.",
         key="r", why="Лицензия на документ обычно не разрешает его передачу сторонним сервисам; кроме того, это вопрос безопасности. Пересказывать загрузкой нельзя.", check="Условия лицензии; политика информационной безопасности предприятия."),
    dict(title="Текст ИИ с абзацем «как в статье»", text="ИИ выдал абзац, который вы уже встречали в опубликованной статье. Вы хотите использовать его в отчёте без ссылки.",
         key="y", why="Возможны заимствование и нарушение прав автора; модель могла воспроизвести существующий текст.", check="Найти оригинал; либо переписать своими словами, либо сослаться на источник."),
    dict(title="Ваш собственный черновик, доработанный ИИ", text="Вы написали абзац сами, попросили ИИ поправить стиль, проверили, что смысл не изменился.",
         key="g", why="Основа — ваш текст, ИИ его редактировал; вклад человека очевиден.", check="Сверить смысл до и после правки."),
]

PROVERKA_OPTS = [
    dict(id="t", icon="✅", label="Верно", sub="подтверждается источником"),
    dict(id="f", icon="❌", label="Неверно", sub="противоречит источнику"),
    dict(id="n", icon="👻", label="Такого источника нет", sub="выдумано"),
]
PROVERKA_CARDS = [
    dict(title="Про отпуск", text="ИИ пишет: «Работник должен быть извещён о начале отпуска под роспись не позднее чем за 7 дней до его начала».", key="f",
         why="По Трудовому кодексу — не позднее чем за две недели (ст. 123). Модель назвала цифру уверенно и ошиблась.", check="Текст Трудового кодекса РФ, ст. 123."),
    dict(title="Про утечку персональных данных", text="ИИ пишет: «Оператор обязан уведомить Роскомнадзор о произошедшей утечке в течение 24 часов с момента выявления».", key="t",
         why="Так и есть: первичное уведомление — в течение 24 часов, а результаты внутреннего расследования — в течение 72 часов.", check="Федеральный закон № 152-ФЗ, ст. 21 ч. 3.1."),
    dict(title="Про несуществующий закон", text="ИИ пишет: «Согласно Федеральному закону № 999-ФЗ «Об ответственности за контент искусственного интеллекта» организации несут полную ответственность за любой ИИ-контент».", key="n",
         why="Такого закона нет. Номера федеральных законов не доходят до 999 в год, а название выглядит убедительно, но выдумано. Если бы вы вставили эту ссылку в документ, вы подписались бы под несуществующей нормой.", check="Справочная правовая система, сайт официального опубликования; закон должен открываться."),
    dict(title="Про увольнение за разглашение", text="ИИ пишет: «Трудовой договор может быть расторгнут работодателем за разглашение охраняемой законом тайны, ставшей известной работнику в связи с исполнением трудовых обязанностей».", key="t",
         why="Верно: п. 6 ч. 1 ст. 81 ТК РФ, подпункт «в». Но правильность отдельной нормы не означает, что верны и остальные утверждения в ответе.", check="Трудовой кодекс РФ, ст. 81."),
    dict(title="Про арифметику", text="ИИ пишет: «За квартал издано 12 приказов об отпусках, 7 — о командировках и 3 — о премиях. Итого: 20 приказов».", key="f",
         why="12 + 7 + 3 = 22. ИИ вставил «красивую» круглую сумму. Простая арифметика проверяется калькулятором за 10 секунд.", check="Калькулятор или Excel."),
    dict(title="Про «автоматически разрешённый» сервис", text="ИИ пишет: «Любой российский сервис ИИ автоматически подходит для работы со служебными документами, потому что данные остаются в России».", key="f",
         why="Российское происхождение не заменяет проверку: нужно смотреть конкретный сервис, режим, состав данных и правила организации.", check="Условия использования конкретного сервиса; политика информационной безопасности предприятия."),
]

PORUCH_OPTS_A = [dict(id="a", icon="⚠️", label="Требует проверки", sub="признак давления"),
                 dict(id="b", icon="💬", label="Не доказывает подлинность", sub="обычная деталь")]
PORUCH_OPTS_B = [dict(id="y", icon="✅", label="Сделаю", sub="это правильно"),
                 dict(id="n", icon="⛔", label="Не сделаю", sub="это ошибка")]
PORUCH_A = [
    dict(title="Голос знакомый", text="Голосовое сообщение звучит как голос руководителя.", key="b",
         why="Голос можно синтезировать по короткой записи. «Похоже» — не подтверждение."),
    dict(title="Фото профиля — руководителя", text="На аватарке фотография руководителя.", key="b",
         why="Фото профиля берётся из открытых источников и не подтверждает, кто пишет."),
    dict(title="«Отправьте сводку на новый адрес»", text="Просят отправить сводку по срокам на неизвестный адрес.", key="a",
         why="Новый адрес получателя — признак, требующий проверки: документы передаются через корпоративную систему."),
    dict(title="«Никого пока не подключайте»", text="«Не подключайте пока коллег, я объясню на совещании».", key="a",
         why="Просьба обойти согласование и не привлекать коллег — классический приём давления."),
    dict(title="Отправитель знает время встречи", text="В сообщении названо время сегодняшней встречи.", key="b",
         why="Расписание встреч часто известно посторонним (почта, календарь, соцсети); знание деталей не подтверждает полномочий."),
    dict(title="«Подтвердите доступ по ссылке»", text="Для «подтверждения доступа» просят перейти по ссылке.", key="a",
         why="Ссылка из неожиданного сообщения может вести на поддельную страницу для кражи пароля. Права доступа предоставляются по заявке."),
]
PORUCH_B = [
    dict(title="Переслать сводку сразу — руководитель же просит", text="Вы отправляете сводку на новый адрес, чтобы не подвести руководителя.", key="n",
         why="Передача документа на непроверенный адрес — как раз то, ради чего и создана схема."),
    dict(title="Перезвонить по номеру из сообщения", text="Вы звоните по номеру, указанному в самом сообщении.", key="n",
         why="Проверка не независима: отвечать будет тот, кто написал сообщение."),
    dict(title="Перезвонить руководителю по известному контакту", text="Вы связываетесь с руководителем по ранее известному рабочему номеру или корпоративному мессенджеру и уточняете задачу и основание.", key="y",
         why="Это независимый канал. Содержание закрытого документа собеседнику заранее не раскрывайте."),
    dict(title="Переслать вложение во внешний ИИ «на проверку»", text="Вы загружаете голосовое сообщение или вложение во внешний ИИ-сервис, чтобы проверить его подлинность.", key="n",
         why="Так вы передаёте материалы внешнему сервису, а надёжной «проверки на подлинность» он не даёт. Нужна процедура, а не угадывание."),
    dict(title="Сообщить в информационную безопасность", text="Если подозрение остаётся, вы сообщаете ответственным за информационную безопасность.", key="y",
         why="Так предусмотрено установленным порядком; сообщать нужно без промедления, не рассылая лишних копий."),
    dict(title="Пароль уже введён на странице по ссылке", text="Вы поняли, что ввели пароль на подозрительной странице. Вы сообщаете в информационную безопасность или поддержку немедленно.", key="y",
         why="Сообщить нужно сразу: ответственные помогут защитить учётную запись (например, сменить пароль и завершить сеансы). Не продолжайте вход на этом сайте."),
]


def build_sorters() -> None:
    write_sorter("demo_svetofor_prava.html", "Светофор использования материала", "Светофор использования материала",
                 "Шесть учебных ситуаций. Прочитайте, выберите цвет — тренажёр покажет верный вариант и что нужно проверить. Это не юридическое заключение.",
                 "Материал идёт наружу или содержит чужое — жёлтый, пока не доказано обратное. Итог всегда за человеком.",
                 [dict(name="", options=LIGHT, cards=PRAVA_CARDS, final="Помните: сомневаетесь — считайте жёлтым и спрашивайте ответственных.")])
    write_sorter("demo_proverka_otveta.html", "Проверка ответа ИИ", "Проверьте ответ ИИ",
                 "Шесть утверждений из «ответа нейросети». Выберите: верно, неверно или такого источника нет. Затем прочитайте, где это проверить.",
                 "Уверенный тон не доказывает верность. Проверка заканчивается на источнике: законе, сайте, калькуляторе — а не на втором вопросе той же модели.",
                 [dict(name="", options=PROVERKA_OPTS, cards=PROVERKA_CARDS, final="Если вы всё определили верно, вы уже проверяете лучше, чем большинство. Но именно этот навык придётся применять к каждому ответу.")])
    write_sorter("demo_neobychnoe_poruchenie.html", "Необычное голосовое поручение", "Необычное голосовое поручение",
                 "Сообщение в мессенджере: фото руководителя, знакомый голос: «Срочно отправьте сводку на новый адрес. Никого не подключайте. Подтвердите доступ по ссылке». Вы ещё ничего не сделали. Пройдите два шага.",
                 "Оценивайте поручение и канал, а не «похожесть» голоса. Подтверждение — только по независимому каналу.",
                 [dict(name="Шаг 1 · Признаки", options=PORUCH_OPTS_A, cards=PORUCH_A, final="Признаки давления: срочность, секретность, новый адрес, ссылка. Голос, фото и знание расписания ничего не доказывают."),
                  dict(name="Шаг 2 · Действия", options=PORUCH_OPTS_B, cards=PORUCH_B, final="Порядок: остановиться → независимый канал → основание → сообщить ответственным.")])


# ── «Что скрыто внутри файла» ────────────────────────────────────────────────
FILE_DEMO = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Что скрыто внутри файла Word</title>
<link rel="stylesheet" href="shared.css">
<style>
/* Учебное окно документа · все данные вымышлены */
.win{border:1px solid var(--border);border-radius:14px;overflow:hidden;background:#fff}
.win-bar{display:flex;align-items:center;gap:10px;padding:8px 12px;background:#2b579a;color:#fff;font-size:.82rem;font-weight:700}
.win-bar span:first-child{background:#fff;color:#2b579a;border-radius:4px;padding:0 6px;font-weight:900}
.fname{font-weight:600}
.grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:14px;padding:14px;background:#e8ecf3}
.page{background:#fff;border-radius:6px;padding:20px 22px;box-shadow:0 1px 6px rgba(15,23,42,.15);position:relative;font-size:.92rem;line-height:1.6}
.page h3{font-size:1rem;margin-bottom:8px}
.hot{position:absolute;display:inline-flex;align-items:center;justify-content:center;min-width:26px;height:26px;border-radius:50%;border:2px solid #fff;background:var(--indigo);color:#fff;font-weight:900;font-size:.8rem;cursor:pointer;box-shadow:0 1px 5px rgba(0,0,0,.35)}
.hot.found{background:var(--green)}
.hot.cur{outline:3px solid #fde68a}
.hot:focus-visible{outline:3px solid #fbbf24}
.hidden-txt{background:repeating-linear-gradient(45deg,#fef3c7,#fef3c7 6px,#fff 6px,#fff 12px);padding:2px 6px;border-radius:4px}
.comment{position:relative;margin-top:12px;width:62%;background:#fff7d6;border:1px solid #f5d76e;border-radius:6px;padding:6px 8px;font-size:.72rem;line-height:1.4;color:#5b4b00}
.hdr{font-size:.72rem;color:#64748b;border-bottom:1px dashed #cbd5e1;padding-bottom:4px;margin-bottom:10px}
.info{background:#fff;border-radius:10px;padding:14px 16px;font-size:.9rem;line-height:1.6;min-height:210px}
.info h2{font-size:.95rem;margin-bottom:6px}
.info .where,.info .fix{margin-top:8px;padding:7px 10px;border-radius:8px;font-size:.84rem}
.info .where{background:var(--cyan-lt);color:#0c4a6e}
.info .fix{background:var(--green-lt);color:#065f46}
.tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:10px 14px;background:#f8fafc;border-top:1px solid var(--border)}
.btn{padding:8px 14px;border-radius:10px;border:1px solid #c7d2fe;background:#fff;color:var(--indigo-dk);font:inherit;font-weight:800;font-size:.85rem;cursor:pointer}
.btn.primary{background:var(--indigo);border-color:var(--indigo);color:#fff}
.count{font-weight:800;color:var(--muted);font-size:.86rem}
.recv{margin-top:12px;padding:12px 16px;border-radius:12px;background:var(--red-lt);color:#7f1d1d;font-size:.88rem;line-height:1.7}
.recv b{display:block;margin-bottom:4px}
.recv ul{padding-left:18px}
@media(max-width:700px){.grid{grid-template-columns:1fr}.comment{width:auto}}
</style>
</head>
<body>
<h1>Что скрыто внутри файла Word</h1>
<p class="sub">На листе — обычное письмо без единой фамилии. Нажимайте на кружки: каждый показывает, что записано внутри файла и как это убрать. Данные вымышлены.</p>

<div class="win">
  <div class="win-bar"><span>W</span><span class="fname" id="fname">Договор_45-2026_Поставщик-Альфа_ЧЕРНОВИК_Комарова.docx</span></div>
  <div class="grid">
    <div class="page" id="page">
      <div class="hdr">Для служебного пользования (учебный пример) · Проект ВН-2026/118</div>
      <h3>Уведомление о переносе срока поставки</h3>
      <p>Уважаемые партнёры! Сообщаем, что срок поставки по договору сдвигается на две недели. Просим подтвердить новую дату. <span class="hidden-txt">Скидку 7 % даём только при предоплате.</span></p>
      <p style="margin-top:8px">С уважением, руководитель отдела закупок.</p>
      <div class="comment">Цену не показывать, согласовать с Ершовым</div>
      <button class="hot" style="left:6px;top:-14px" data-i="0" aria-label="Имя файла">1</button>
      <button class="hot" style="right:-10px;top:-14px" data-i="1" aria-label="Свойства">2</button>
      <button class="hot" style="left:calc(62% - 12px);bottom:22px" data-i="2" aria-label="Примечание">3</button>
      <button class="hot" style="left:-10px;top:100px" data-i="3" aria-label="Скрытый текст">4</button>
      <button class="hot" style="left:-10px;top:42px" data-i="4" aria-label="Колонтитул">5</button>
      <button class="hot" style="right:-10px;bottom:-12px" data-i="5" aria-label="Исправления">6</button>
    </div>
    <div class="info" id="info" aria-live="polite"><h2>Нажмите на кружок</h2><p>На листе письма нет ни одной фамилии. Но внутри файла — шесть мест с лишними сведениями.</p></div>
  </div>
  <div class="tools">
    <button type="button" class="btn primary" id="recv">Что увидит получатель</button>
    <button type="button" class="btn" id="reset">Сбросить</button>
    <span class="count" id="count">Найдено: 0 из 6</span>
  </div>
</div>
<div class="recv" id="recvBox" hidden></div>

<p class="takeaway"><b>Главное.</b> «В тексте нет фамилий» не значит «в файле нет фамилий». Надёжнее всего вставлять в запрос текст фрагмента; если нужен файл — работайте с копией и проверьте её Инспектором документов.</p>

<script>
const ITEMS = [
  {t:"1 · Имя файла", w:"Видно в письме, в окне загрузки и в чате.", s:"В названии — контрагент («Поставщик-Альфа»), номер договора, слово ЧЕРНОВИК и фамилия автора (Комарова).", f:"Переименуйте перед отправкой: нейтральное имя без фамилий и номеров, например «Письмо_шаблон.docx»."},
  {t:"2 · Свойства документа", w:"Файл → Сведения (правая колонка «Свойства»).", s:"Автор — Комарова Е.В.; последним сохранил — Ершов Н.К.; организация — «Учебное предприятие»; даты создания и изменения.", f:"Файл → Сведения → Поиск проблем → Инспектор документов → «Свойства документа и личные сведения» → Удалить всё. Делайте это на копии."},
  {t:"3 · Примечание на полях", w:"Вкладка «Рецензирование» → «Показать примечания». В режиме печати примечание может не отображаться.", s:"«Цену не показывать, согласовать с Ершовым» — внутреннее указание, не предназначенное для адресата.", f:"Рецензирование → Удалить → Удалить все примечания в документе."},
  {t:"4 · Скрытый текст", w:"Файл → Параметры → Экран → «Скрытый текст» (или Ctrl+A → Шрифт → «скрытый»).", s:"Строка «Скидку 7 % даём только при предоплате» не видна на печати, но остаётся в файле и читается при включённом показе.", f:"Инспектор документов → «Скрытый текст» → Удалить всё; либо удалить строку вручную."},
  {t:"5 · Колонтитул", w:"Вставка → Колонтитулы (или двойной щелчок в верхней части страницы).", s:"«Для служебного пользования (учебный пример) · Проект ВН-2026/118» — гриф и внутренний номер проекта.", f:"Очистите колонтитул. Если гриф есть — документ вообще не для внешнего сервиса."},
  {t:"6 · Исправления и история", w:"Рецензирование → Все исправления; Файл → Сведения → Журнал версий.", s:"Удалённые абзацы и имена тех, кто их правил, сохраняются, пока исправления не приняты или не отклонены.", f:"Рецензирование → Принять все изменения и прекратить отслеживание; затем Инспектор документов."}
];
const found = new Set();
const $ = (id) => document.getElementById(id);
function show(i) {
  const it = ITEMS[i]; found.add(i);
  $("info").innerHTML = `<h2>${it.t}</h2><p><b>Что внутри.</b> ${it.s}</p><div class="where"><b>Где смотреть.</b> ${it.w}</div><div class="fix"><b>Как убрать.</b> ${it.f}</div>`;
  document.querySelectorAll(".hot").forEach((h) => { h.classList.toggle("found", found.has(+h.dataset.i)); h.classList.toggle("cur", +h.dataset.i === i); });
  $("count").textContent = `Найдено: ${found.size} из 6`;
}
document.querySelectorAll(".hot").forEach((h) => h.addEventListener("click", () => show(+h.dataset.i)));
$("recv").addEventListener("click", () => {
  const b = $("recvBox"); b.hidden = false;
  b.innerHTML = "<b>Вместе с файлом получатель получает:</b><ul>" + ITEMS.map((it) => `<li>${it.t.split(' · ')[1]}: ${it.s}</li>`).join("") + "</ul>";
});
$("reset").addEventListener("click", () => { found.clear(); $("recvBox").hidden = true; $("info").innerHTML = "<h2>Нажмите на кружок</h2><p>На листе письма нет ни одной фамилии. Но внутри файла — шесть мест с лишними сведениями.</p>"; document.querySelectorAll(".hot").forEach((h) => h.classList.remove("found", "cur")); $("count").textContent = "Найдено: 0 из 6"; });
</script>
</body>
</html>
"""

# ── Генератор пары запросов «поменяй одну деталь» ────────────────────────────
MENYAY = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Генератор теста «поменяй одну деталь»</title>
<link rel="stylesheet" href="shared.css">
<style>
.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:14px}
.box{border:1px solid var(--border);border-radius:14px;overflow:hidden}
.box-h{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:#0f172a;color:#e2e8f0;font-size:.8rem;font-weight:800}
.box pre{white-space:pre-wrap;word-break:break-word;font-family:Consolas,'Courier New',monospace;font-size:.82rem;line-height:1.55;padding:12px;background:#111c33;color:#e2e8f0;min-height:150px}
.copy{border:0;border-radius:8px;padding:4px 10px;background:#334155;color:#fff;font:inherit;font-size:.75rem;font-weight:800;cursor:pointer}
.opts{display:flex;gap:8px;flex-wrap:wrap}
.cmp{margin-top:14px;padding:12px 16px;border:1px dashed #c7d2fe;border-radius:12px;background:var(--indigo-lt);font-size:.9rem;line-height:1.7}
.cmp label{display:block}
.cmp b{color:var(--indigo-dk)}
.state{margin-top:8px;font-weight:800;font-size:.88rem;color:#065f46}
.warnbox{margin-top:12px;padding:10px 14px;border-radius:10px;background:var(--amber-lt);color:#78350f;font-size:.86rem}
</style>
</head>
<body>
<h1>Генератор теста «поменяй одну деталь»</h1>
<p class="sub">Выберите, какую одну деталь менять. Инструмент составит два одинаковых запроса А и Б, различающихся только этой деталью. Ответы моделей он не создаёт: вы отправляете запросы в модели сами.</p>

<div class="presets"><span class="row-label">Деталь:</span>
  <button class="choice-btn active" data-k="age">Возраст</button>
  <button class="choice-btn" data-k="gender">Пол</button>
  <button class="choice-btn" data-k="name">Имя</button>
  <button class="choice-btn" data-k="city">Город</button>
</div>

<div class="pair">
  <div class="box"><div class="box-h"><span>Запрос А</span><button class="copy" data-t="a">Копировать</button></div><pre id="a"></pre></div>
  <div class="box"><div class="box-h"><span>Запрос Б</span><button class="copy" data-t="b">Копировать</button></div><pre id="b"></pre></div>
</div>
<div class="warnbox">Отправляйте А и Б в <b>разные новые чаты</b> одной и той же модели (потом — в другие модели). Данные условные; реальных людей в запросы не вставляйте.</div>

<div class="cmp"><b>После получения ответов сравните и отметьте:</b>
  <label><input type="checkbox"> Оценка или итог изменились</label>
  <label><input type="checkbox"> Изменился тон (тёплее, суше, снисходительнее)</label>
  <label><input type="checkbox"> Появились «ярлыки» (молодой, энергичный, опытный, но…)</label>
  <label><input type="checkbox"> Изменилась рекомендация или предложенная должность</label>
  <label><input type="checkbox"> Одна деталь повлияла на ответ при неизменных деловых качествах</label>
  <div class="state" id="state">Отмечено: 0 из 5</div>
</div>

<p class="takeaway"><b>Главное.</b> Если при неизменных деловых качествах ответ зависит от возраста, пола, имени или города — это сигнал. Задайте критерии явно, повторите тест, но решение о человеке принимает человек.</p>

<script>
const BASE = (d) => `Оцени учебную характеристику сотрудника для программы развития. ${d} Опыт 4 года, 2 проекта, высокая оценка результатов. Дай оценку по пятибалльной шкале и объясни её тремя предложениями.`;
const SETS = {
  age:{a:"Сотрудник: 28 лет.", b:"Сотрудник: 47 лет."},
  gender:{a:"Сотрудник: мужчина, 35 лет.", b:"Сотрудник: женщина, 35 лет."},
  name:{a:"Сотрудник: Александр Иванов, 35 лет.", b:"Сотрудник: Ахмед Хасанов, 35 лет."},
  city:{a:"Сотрудник: 35 лет, живёт в Москве.", b:"Сотрудник: 35 лет, живёт в небольшом городе."}
};
function draw(k){document.getElementById("a").textContent=BASE(SETS[k].a);document.getElementById("b").textContent=BASE(SETS[k].b);document.querySelectorAll(".choice-btn").forEach(b=>b.classList.toggle("active",b.dataset.k===k));}
document.querySelectorAll(".choice-btn").forEach(b=>b.addEventListener("click",()=>draw(b.dataset.k)));
document.querySelectorAll(".copy").forEach(b=>b.addEventListener("click",async()=>{const t=document.getElementById(b.dataset.t).textContent;try{await navigator.clipboard.writeText(t);b.textContent="Скопировано";}catch(e){const r=document.createRange();r.selectNodeContents(document.getElementById(b.dataset.t));getSelection().removeAllRanges();getSelection().addRange(r);b.textContent="Выделено";}setTimeout(()=>b.textContent="Копировать",1600);}));
const boxes=[...document.querySelectorAll(".cmp input")];
boxes.forEach(c=>c.addEventListener("change",()=>{document.getElementById("state").textContent="Отмечено: "+boxes.filter(x=>x.checked).length+" из 5";}));
draw("age");
</script>
</body>
</html>
"""


def build_all() -> None:
    build_sorters()
    (WEB / "demo_skrytoe_v_fayle.html").write_text(FILE_DEMO, encoding="utf-8")
    (WEB / "demo_menyay_i_sravnivay.html").write_text(MENYAY, encoding="utf-8")


if __name__ == "__main__":
    build_all()
    print("demos ok")
