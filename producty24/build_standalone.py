#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает из producty24/index.html автономную страницу docs/index.html.

index.html написан как тело артефакта: claude.ai сам оборачивает его в документ
с doctype, charset и базовым сбросом стилей. Вне claude.ai этой обёртки нет,
поэтому здесь мы добавляем её сами — и получаем один файл, который открывается
и с диска, и с любого хостинга, без обращений к claude.ai.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
body = (ROOT / "producty24" / "index.html").read_text(encoding="utf-8")

TITLE = "Куда пойти на Продукты 24"
DESC = ("Расписание конференции «Продукты 24 × ffdd2d» — 12 сентября 2026, комплекс «Мечта». "
        "Три зала, 19 событий, личный план с проверкой накладок.")

# <title> уже есть в теле — переносим его в head, чтобы не было дубля
body = re.sub(r"^<title>.*?</title>\n", "", body, count=1, flags=re.S)

HEAD = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#FFDD2D">
<meta property="og:type" content="website">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23FFDD2D'/></svg>">
<style>
  /* базовый сброс — на claude.ai его добавляет обёртка артефакта */
  html{{-webkit-text-size-adjust:100%}}
  body{{margin:0}}
  img{{max-width:100%}}
  [hidden]:not([hidden="until-found"]){{display:none!important}}
</style>
</head>
<body>
"""

out = ROOT / "docs" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(HEAD + body + "\n</body>\n</html>\n", encoding="utf-8")
(ROOT / "docs" / ".nojekyll").write_text("", encoding="utf-8")
print("собрано:", out, "|", round(out.stat().st_size / 1024, 1), "КБ")
