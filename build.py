#!/usr/bin/env python3
"""Собирает index.html: шаблон src/app.template.html + данные data/program.json."""
import json, pathlib, sys

root = pathlib.Path(__file__).parent
tpl = (root / "src" / "app.template.html").read_text(encoding="utf-8")
data = json.loads((root / "data" / "program.json").read_text(encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
if "/*__DATA__*/" not in tpl:
    sys.exit("В шаблоне нет маркера /*__DATA__*/")
out = tpl.replace("/*__DATA__*/", payload)
(root / "index.html").write_text(out, encoding="utf-8")
print("index.html:", len(out), "байт,", len(data["events"]), "событий")
