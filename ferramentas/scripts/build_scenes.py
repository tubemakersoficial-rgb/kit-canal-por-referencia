"""Lê o roteiro-cenas.md, alinha cada cena com a transcrição do áudio e gera scenes.json.

Uso: python -I build_scenes.py
Cada cena ganha start/end (s) no áudio original e a lista de palavras com tempos.
"""
import difflib, json, re, unicodedata

md = open('../roteiro-cenas.md', encoding='utf-8').read()
scenes = []
for line in md.splitlines():
    m = re.match(r'\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$', line)
    if not m:
        continue
    i, nar, img, txt, typ = m.groups()
    scenes.append(dict(id=int(i), narration=nar, image=img, text=txt,
                       clip=typ.startswith('🎬'), motion=typ))
assert [s['id'] for s in scenes] == list(range(1, len(scenes) + 1)), 'ids fora de ordem'

def norm(w):
    w = unicodedata.normalize('NFD', w.lower())
    w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', w)

tr = json.load(open('transcricao.json', encoding='utf-8'))
words = [w for s in tr['segments'] for w in s['words']]
wt = [norm(w['w']) for w in words]

st, owner = [], []
for k, s in enumerate(scenes):
    for w in s['narration'].replace('-', ' ').split():
        if norm(w):
            st.append(norm(w)); owner.append(k)

sm = difflib.SequenceMatcher(None, st, wt, autojunk=False)
amap = {}
for a, b, size in sm.get_matching_blocks():
    for d in range(size):
        amap[a + d] = b + d

first = {}
for p, k in enumerate(owner):
    first.setdefault(k, p)
starts = []
for k in range(len(scenes)):
    p0 = first[k]
    ps = [p for p in range(p0, len(owner)) if owner[p] == k and p in amap]
    if not ps:
        raise SystemExit('cena %d sem correspondência' % scenes[k]['id'])
    starts.append(max(0, amap[ps[0]] - (ps[0] - p0)))

dur = tr['duration']
for k, s in enumerate(scenes):
    a = starts[k]
    b = starts[k + 1] if k + 1 < len(scenes) else len(words)
    s['w0'], s['w1'] = a, b
    s['start'] = round(words[a]['start'], 2)
    s['speech_end'] = round(words[b - 1]['end'], 2)
    s['words'] = words[a:b]
# cada cena vai do início da sua fala até o início da próxima (a 1ª começa em 0)
scenes[0]['start'] = 0.0
for k, s in enumerate(scenes):
    s['end'] = scenes[k + 1]['start'] if k + 1 < len(scenes) else round(dur, 2)

json.dump(scenes, open('scenes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
bad = [s['id'] for s in scenes if s['end'] - s['start'] < 0.8]
print('%d cenas, %.1fs; curtas demais: %s' % (len(scenes), dur, bad))
for s in scenes:
    print('%3d %6.2f-%6.2f  %s | %s' % (s['id'], s['start'], s['end'], ' '.join(w['w'] for w in s['words'][:5]), s['narration'][:40]))
