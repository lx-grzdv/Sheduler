# Проверки синхронизации плана

Запускать после сборки `index.html`:

```
python3 test/test_plan_restore.py   # план приезжает из базы на чистом устройстве
python3 test/test_plan_merge.py     # локальные отметки сливаются с базой
```

Тесты подменяют `window.claude.use('db')` заглушкой, повторяющей контракт
capability: `get()` возвращает `DocumentSnapshot` с телом за `data()`,
а не сами поля. Именно на этом расхождении план не восстанавливался.
Нужен Playwright и Chromium: `pip install playwright`.
