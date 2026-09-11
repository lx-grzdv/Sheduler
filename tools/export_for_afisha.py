#!/usr/bin/env python3
"""Выгрузка программы G8 в формате дизайн-афиши (lx-grzdv/design-events).

Слаги считаются тем же алгоритмом, что и slugifyEntityKey в
apps/calendar-web/src/app/utils/slugify.ts, поэтому ссылки вида
/speaker/<slug> совпадут с существующими страницами афиши.
"""
import csv, json, pathlib, re, sys, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
AFISHA = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/user/design-events')
OUT = ROOT / 'export'
OUT.mkdir(exist_ok=True)

RU_TO_LAT = {
    'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z',
    'и':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
    'с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sch',
    'ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',
}
RU_VOWELS = set('аеёиоуыэюя')

def strip_latin_diacritics(v):
    out = []
    for ch in unicodedata.normalize('NFD', v):
        if unicodedata.combining(ch) and out and 'a' <= out[-1].lower() <= 'z':
            continue
        out.append(ch)
    return unicodedata.normalize('NFC', ''.join(out))

def slugify(raw):
    lower = strip_latin_diacritics(re.sub(r'\s+', ' ', str(raw or '').lower().strip()))
    out = ''
    for i, ch in enumerate(lower):
        if ch == 'й':
            prev = lower[i-1] if i > 0 else ''
            out += 'i' if prev in RU_VOWELS else 'y'
        elif ch in RU_TO_LAT:
            out += RU_TO_LAT[ch]
        elif re.match(r'[a-z0-9]', ch):
            out += ch
        else:
            out += '-'
    return re.sub(r'^-+|-+$', '', re.sub(r'-+', '-', out))

def existing_profile_slugs():
    path = AFISHA / 'apps/calendar-web/src/app/data/entityProfiles.ts'
    if not path.exists(): return {}
    res, current = {}, None
    for line in path.read_text(encoding='utf-8').splitlines():
        m = re.match(r"\s{2}(speaker|venue|organizer):\s*\{", line)
        if m:
            current = m.group(1); res.setdefault(current, set()); continue
        if current:
            k = re.match(r"\s{4}'([^']+)':\s*\{", line)
            if k: res[current].add(k.group(1))
    return res

def existing_entity_keys():
    path = AFISHA / 'apps/calendar-web/src/app/data/generated/eventEntityMap.ts'
    if not path.exists(): return set()
    text = path.read_text(encoding='utf-8')
    keys = set()
    for block in re.findall(r'speakerIds:\[([^\]]*)\]', text):
        keys.update(re.findall(r'"([^"]+)"', block))
    return keys

profiles = existing_profile_slugs()
profile_slugs = profiles.get('speaker', set())
afisha_keys = existing_entity_keys()
afisha_slugs = {slugify(k) for k in afisha_keys}

data = json.loads((ROOT / 'data/program.json').read_text(encoding='utf-8'))
V = {v['id']: v for v in data['venues']}
F = data['festival']
SITE = 'https://www.design-events.fun'

sessions, speakers = [], {}
for e in data['events']:
    if e['kind'] == 'break':
        continue
    v = V[e['venue']]
    keys = []
    for s in e['speakers']:
        raw = s['name'].strip()
        key = raw.lower()
        slug = slugify(raw)
        keys.append(key)
        sp = speakers.setdefault(slug, {
            'name': raw, 'entityKey': key, 'slug': slug,
            'roles': [], 'sessions': 0, 'sessionIds': [], 'sections': set(), 'venues': set(),
        })
        if s['role'] and s['role'] not in sp['roles']:
            sp['roles'].append(s['role'])
        sp['sessions'] += 1
        sp['sessionIds'].append(e['id'])
        if e['section']: sp['sections'].add(e['section'])
        sp['venues'].add(v['name'])
    sessions.append({
        'sessionId': f"g8-2026-{e['id']}",
        'date': F['date'],
        'start': e['start'], 'end': e['end'],
        'title': e['title'],
        'kind': e['kind'],
        'track': e['section'] or '',
        'trackCurator': e['curator'] or '',
        'hall': v['name'],
        'venueKey': 'хлебозавод №9' if v['place'] == 'Хлебозавод' else 'дизайн-завод',
        'place': v['place'],
        'organizerKey': 'g8',
        'speakerKeys': keys,
        'speakerSlugs': [slugify(k) for k in keys],
        'speakerNames': [s['name'] for s in e['speakers']],
    })

rows = []
for slug, sp in sorted(speakers.items(), key=lambda kv: (-kv[1]['sessions'], kv[1]['name'])):
    rows.append({
        'name': sp['name'], 'entityKey': sp['entityKey'], 'slug': slug,
        'profileUrl': f'{SITE}/speaker/{slug}',
        'inAfishaGraph': slug in afisha_slugs,
        'hasProfilePage': slug in profile_slugs,
        'sessions': sp['sessions'], 'sessionIds': sp['sessionIds'],
        'role': sp['roles'][0] if sp['roles'] else '',
        'sections': sorted(sp['sections']), 'halls': sorted(sp['venues']),
    })

bundle = {
    'source': {
        'festival': F['name'], 'edition': F['edition'], 'date': F['date'],
        'site': F['site'], 'organizer': F['organizer'],
        'extractedFrom': 'G8_2026_PROGRAM.pdf — официальная программа, 16 полос без текстового слоя',
        'navigator': 'https://claude.ai/code/artifact/47e406bb-ca64-457e-8d17-7e3b6ffff889',
        'slugAlgorithm': 'apps/calendar-web/src/app/utils/slugify.ts · slugifyEntityKey',
    },
    'halls': [{'name': v['name'], 'place': v['place'],
               'venueKey': 'хлебозавод №9' if v['place'] == 'Хлебозавод' else 'дизайн-завод'}
              for v in data['venues']],
    'tracks': [{'name': s['name'], 'curator': s['curator'], 'hall': V[s['venue']]['name']}
               for s in data['sections']],
    'sessions': sessions,
    'speakers': rows,
}
(OUT / 'g8-2026-afisha.json').write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding='utf-8')

with (OUT / 'g8-2026-sessions.csv').open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['session_id','date','start','end','hall','venue_key','place','track','track_curator','kind','title','speaker_keys','speaker_slugs','organizer_key'])
    for s in sessions:
        w.writerow([s['sessionId'],s['date'],s['start'],s['end'] or '',s['hall'],s['venueKey'],s['place'],
                    s['track'],s['trackCurator'],s['kind'],s['title'],
                    '; '.join(s['speakerKeys']),'; '.join(s['speakerSlugs']),s['organizerKey']])

with (OUT / 'g8-2026-speakers.csv').open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['name','entity_key','slug','profile_url','in_afisha_graph','has_profile_page','sessions','role','sections','halls','session_ids'])
    for r in rows:
        w.writerow([r['name'],r['entityKey'],r['slug'],r['profileUrl'],
                    int(r['inAfishaGraph']),int(r['hasProfilePage']),r['sessions'],r['role'],
                    '; '.join(r['sections']),'; '.join(r['halls']),'; '.join(r['sessionIds'])])

known = [r for r in rows if r['inAfishaGraph']]
withpage = [r for r in rows if r['hasProfilePage']]
print(f"сессий: {len(sessions)}  спикеров: {len(rows)}")
print(f"уже есть в графе афиши: {len(known)}   из них с готовым профилем: {len(withpage)}")
print("\n— совпали с профилями афиши:")
for r in withpage:
    print(f"   {r['name']:<22} /speaker/{r['slug']:<22} {r['sessions']} выступл.")
print("\n— есть в графе, профиля пока нет:")
for r in [x for x in known if not x['hasProfilePage']]:
    print(f"   {r['name']:<22} /speaker/{r['slug']}")
