from playwright.sync_api import sync_playwright
IDS = ["e081","e082","e083","e010","e011","e086","e012","e013","e087","e088","e089","e016","e092","e094","e020","e134","e038","e135","e097","e023","e136","e099","e069","e070","e139","e071","e027","e140","e043","e044","e046","e103","e047","e049","e079","e051"]
MOCK = """
window.__written = null;
window.claude = { use: async (n) => {
  if (n !== 'db') return null;
  return { doc: () => ({
    get: async () => ({ id:'main', exists:true, data:()=>({ids:%s, updated:1}), metadata:{} }),
    set: async (d) => { window.__written = d; },
    onSnapshot: (next) => { window.__push = next; return ()=>{}; }
  })};
}};
""" % IDS
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg=b.new_page(viewport={"width":1320,"height":950})
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(MOCK)
    pg.goto("file:///home/user/Sheduler/index.html"); pg.wait_for_timeout(1500)
    print("восстановлено из db:", pg.evaluate("state.plan.size"), "| ожидалось:", len(IDS))
    print("лишней записи в db нет:", pg.evaluate("window.__written === null"))
    print("localStorage:", len(pg.evaluate("JSON.parse(localStorage.getItem('g8-2026-plan')||'[]')")))
    # прилетело обновление с другого устройства
    pg.evaluate("window.__push({id:'main', exists:true, data:()=>({ids:['e010','e011']}), metadata:{}})")
    pg.wait_for_timeout(200)
    print("после onSnapshot:", pg.evaluate("state.plan.size"), "(ожидалось 2)")
    pg.evaluate("window.__push({id:'main', exists:false, data:()=>undefined, metadata:{}})")
    pg.wait_for_timeout(200)
    print("пустой снимок не стирает план:", pg.evaluate("state.plan.size"), "(ожидалось 2)")
    pg.click('[data-view="plan"]'); pg.wait_for_timeout(400)
    print("строк в плане:", pg.evaluate("document.querySelectorAll('#view-plan .prow').length"))
    print("ошибки:", errs)
    b.close()
