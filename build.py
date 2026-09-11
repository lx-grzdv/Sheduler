#!/usr/bin/env python3
"""Собирает index.html: шаблон src/app.template.html + данные data/program.json."""
import json, pathlib, sys

root = pathlib.Path(__file__).parent
tpl = (root / "src" / "app.template.html").read_text(encoding="utf-8")
data = json.loads((root / "data" / "program.json").read_text(encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
links_path = root / "data" / "afisha-links.json"
links = json.loads(links_path.read_text(encoding="utf-8")) if links_path.exists() else {}
if "/*__DATA__*/" not in tpl or "/*__LINKS__*/" not in tpl:
    sys.exit("В шаблоне нет маркеров /*__DATA__*/ и /*__LINKS__*/")
out = tpl.replace("/*__DATA__*/", payload)
out = out.replace("/*__LINKS__*/", json.dumps(links, ensure_ascii=False, separators=(",", ":")))
(root / "index.html").write_text(out, encoding="utf-8")
print("index.html:", len(out), "байт,", len(data["events"]), "событий,", len(links), "ссылок на профили")
