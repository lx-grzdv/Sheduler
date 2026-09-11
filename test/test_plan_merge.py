from playwright.sync_api import sync_playwright
MOCK = """
window.__written = null;
const mockDoc = {
  get: async () => ({ id:'main', exists:true, data:()=>({ids:['e010','e011']}), metadata:{} }),
  set: async (d) => { window.__written = d; },
  onSnapshot: (next) => { window.__push = next; return ()=>{}; }
};
window.claude = { use: async (n) => (n === 'db' ? { doc: () => mockDoc } : null) };
try { localStorage.setItem('g8-2026-plan', JSON.stringify(['e055'])); } catch (e) {}
"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg=b.new_page()
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(MOCK)
    pg.goto("file:///home/user/Sheduler/index.html"); pg.wait_for_timeout(1500)
    print("слияние локального и базы:", sorted(pg.evaluate("[...state.plan]")), "— ожидалось ['e010','e011','e055']")
    w = pg.evaluate("window.__written")
    print("записано обратно в базу:", sorted(w["ids"]) if w else None, "— ожидалось 3 id")
    print("ошибки:", errs)
    b.close()
