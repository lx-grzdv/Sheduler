#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает статический сайт с расписаниями конференций для GitHub Pages.

Исходники расписаний написаны как тело артефакта: doctype, charset и базовый
сброс стилей добавляет сама площадка claude.ai. Здесь мы дописываем обёртку
и раскладываем страницы по своим адресам:

    /               указатель на оба расписания
    /producty24/    Продукты 24 × ffdd2d
    /g8/            G8 «Креативный фудкорт»

Рядом с каждой страницей кладётся пустой .nojekyll, иначе GitHub Pages
пропускает файлы через Jekyll и отдаёт отрендеренный README вместо страницы.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent

SITES = [
    {
        "slug": "producty24",
        "source": "src/producty24.html",
        "title": "Куда пойти на Продукты 24",
        "desc": "Расписание конференции «Продукты 24 × ffdd2d» — 12 сентября 2026, "
                "комплекс «Мечта». Три зала, 19 событий, личный план с проверкой накладок.",
        "theme": "#FFDD2D",
        "card": {
            "name": "Продукты 24 × ffdd2d",
            "when": "12 сентября 2026",
            "where": "Комплекс «Мечта», Москва",
            "stat": "3 зала · 19 событий · 39 спикеров",
            "accent": "#FFDD2D",
            "ink": "#14140F",
        },
    },
    {
        "slug": "g8",
        "source": "src/g8.html",
        "title": "Куда пойти на G8",
        "desc": "Расписание фестиваля креативных индустрий G8 «Креофудкорт» — "
                "11 сентября 2026, Хлебозавод и Дизайн-завод. Семь залов и личный план.",
        "theme": "#FE2627",
        "card": {
            "name": "G8 «Креофудкорт»",
            "when": "11 сентября 2026",
            "where": "Хлебозавод и Дизайн-завод, Москва",
            "stat": "7 залов · 22 секции",
            "accent": "#FE2627",
            "ink": "#FFFFFF",
        },
    },
]


def wrap(title, desc, theme, body):
    """Оборачивает тело артефакта в самостоятельный документ."""
    body = re.sub(r"^<title>.*?</title>\n", "", body, count=1, flags=re.S)
    icon = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
            "<rect width='32' height='32' rx='6' fill='%23" + theme.lstrip("#") + "'/></svg>")
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="{theme}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="{icon}">
<style>
  /* базовый сброс — на claude.ai его добавляет обёртка артефакта */
  html{{-webkit-text-size-adjust:100%}}
  body{{margin:0}}
  img{{max-width:100%}}
  [hidden]:not([hidden="until-found"]){{display:none!important}}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def landing():
    cards = "\n".join(f"""      <a class="card" href="{s['slug']}/" style="--accent:{s['card']['accent']}; --ink:{s['card']['ink']}">
        <span class="dot"></span>
        <span class="body">
          <span class="name">{s['card']['name']}</span>
          <span class="when">{s['card']['when']}</span>
          <span class="where">{s['card']['where']}</span>
          <span class="stat">{s['card']['stat']}</span>
        </span>
        <span class="go" aria-hidden="true">→</span>
      </a>""" for s in SITES)
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Расписания конференций</title>
<meta name="description" content="Расписания и планировщики конференций: Продукты 24 × ffdd2d и фестиваль G8.">
<meta name="theme-color" content="#FFDD2D">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23FFDD2D'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@700;800&family=Golos+Text:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
<style>
:root{{
  --bg:#F7F6F2; --surface:#FFFFFF; --ink:#14140F; --ink-2:#5C5B52; --ink-3:#8E8C80;
  --line:#E4E2DA; --line-2:#CFCCC1;
  color-scheme:light;
}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme="light"]){{
    --bg:#141413; --surface:#1D1D1B; --ink:#F7F6F2; --ink-2:#A8A69B; --ink-3:#807E74;
    --line:#302F2B; --line-2:#434138; color-scheme:dark;
  }}
}}
:root[data-theme="dark"]{{
  --bg:#141413; --surface:#1D1D1B; --ink:#F7F6F2; --ink-2:#A8A69B; --ink-3:#807E74;
  --line:#302F2B; --line-2:#434138; color-scheme:dark;
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0; background:var(--bg); color:var(--ink);
  font-family:"Golos Text",system-ui,-apple-system,sans-serif; font-size:15px; line-height:1.45}}
.wrap{{max-width:660px; margin:0 auto; padding-inline:16px; padding-block:56px 48px}}
h1{{font-family:"Unbounded","Golos Text",sans-serif; font-weight:800; letter-spacing:-.02em;
  font-size:clamp(26px,6vw,38px); line-height:1.08; margin:0; text-wrap:balance}}
.lead{{color:var(--ink-2); margin:12px 0 0; max-width:52ch}}
.list{{display:flex; flex-direction:column; gap:12px; margin-top:32px}}
.card{{display:flex; gap:14px; align-items:flex-start; text-decoration:none; color:inherit;
  background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:18px 18px 18px 16px}}
.card:hover{{border-color:var(--line-2)}}
.card:focus-visible{{outline:2px solid var(--ink); outline-offset:2px}}
.dot{{flex:none; width:12px; height:12px; border-radius:3px; background:var(--accent); margin-top:5px}}
.card .body{{flex:1; min-width:0; display:flex; flex-direction:column; gap:3px}}
.name{{font-family:"Unbounded","Golos Text",sans-serif; font-weight:700; font-size:17px; letter-spacing:-.02em}}
.when{{font-family:"JetBrains Mono",ui-monospace,monospace; font-size:13px; color:var(--ink-2)}}
.where{{font-size:13.5px; color:var(--ink-2)}}
.stat{{font-family:"JetBrains Mono",ui-monospace,monospace; font-size:11.5px; color:var(--ink-3); margin-top:5px}}
.go{{flex:none; color:var(--ink-3); font-size:18px; align-self:center}}
footer{{margin-top:36px; padding-top:18px; border-top:1px solid var(--line);
  color:var(--ink-3); font-size:12.5px}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style>
</head>
<body>
  <main class="wrap">
    <h1>Расписания конференций</h1>
    <p class="lead">Сетка залов, поиск по спикерам и личный план: отмечаете звёздочкой, что хотите
    послушать, а план предупреждает о накладках и перебежках между залами.</p>
    <div class="list">
{cards}
    </div>
    <footer>План хранится в браузере этого устройства. Программы взяты с официальных сайтов
    конференций — организаторы могут их менять, сверяйтесь на месте.</footer>
  </main>
</body>
</html>
"""


built = []
for s in SITES:
    body = (ROOT / s["source"]).read_text(encoding="utf-8")
    out = ROOT / s["slug"] / "index.html"
    assert out.resolve() != (ROOT / s["source"]).resolve(), \
        f"{s['slug']}: исходник и результат сборки — один файл"
    out.parent.mkdir(exist_ok=True)
    out.write_text(wrap(s["title"], s["desc"], s["theme"], body), encoding="utf-8")
    built.append(out)

(ROOT / "index.html").write_text(landing(), encoding="utf-8")
built.append(ROOT / "index.html")
(ROOT / ".nojekyll").write_text("", encoding="utf-8")

for p in built:
    print("собрано:", p.relative_to(ROOT), "|", round(p.stat().st_size / 1024, 1), "КБ")
