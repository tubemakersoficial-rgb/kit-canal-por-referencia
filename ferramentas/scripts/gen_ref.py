"""Motor da animação em HTML (HyperFrames + GSAP): letreiro, recortes, setas e sinais no tempo de cada palavra.

Uso (na pasta videos/NN-tema/work):  python gen_ref.py [blocos...]   -> hf/mg_bNN.html + hf/blocks.json
Lê: scenes.json (build_scenes.py), projeto.json ({"spec": "spec", "blocos": [...]}), o spec do vídeo e,
se existir, canal/estilo.json (cores, fonte e cor do papel do canal).

Elementos (todos com o instante em segundos absolutos do áudio; veja o guia 06-animacao-html.md):
  T  letreiro escrito letra por letra (vermelho para NÃO/NUNCA/FALSO/ERRO)   TAG faixa de marca-texto com texto
  CUT recorte ilustrado (hf/cut/NOME.png)    FRAME quadro de borda tremida, com imagem dentro (ou só a borda, para clipe)
  ARROW seta pontilhada    NO proibido    XX X vermelho    CHECK selo de ok    ZOOM círculo de zoom    HALO mancha de aquarela
  MOVE recorte que anda    DROP gota que anda    NUM número do passo    CARD carta que vira    COUNTER contador
  BAR barra    LINE linha    PRESS mãos pressionando    FLASH clarão    DARK escurece    BTN botão    ROWS quadro-resumo
"""
import json, math, os, random, re, sys, unicodedata
from PIL import Image
_AR = {}
def ar(name):
    """altura/largura do recorte hf/cut/NOME.png"""
    if name not in _AR:
        w, h = Image.open(f'hf/cut/{name}.png').size
        _AR[name] = h / w
    return _AR[name]

W, H = 1920, 1080
scenes = json.load(open('scenes.json', encoding='utf-8'))
SC = {s['id']: s for s in scenes}
LAST = scenes[-1]['id']
AUDIO_END = scenes[-1]['end'] + 3.0
INK, RED, ORANGE, GREEN, GRAY, YELLOW = '#173f4f', '#b3261e', '#e8912e', '#3d8b3d', '#8a8f8f', '#f0b43c'
# estilo do canal (opcional): ../../../canal/estilo.json ou ./estilo.json  -> cores, fonte do letreiro e cor do papel
PAPER, FONT_NAME, FONT_FILE = '#fcf3e1', 'Chewy', 'Chewy-Regular.ttf'
for _p in ('estilo.json', os.path.join('..', '..', '..', 'canal', 'estilo.json')):
    if os.path.exists(_p):
        _e = json.load(open(_p, encoding='utf-8'))
        INK, RED, ORANGE, GREEN, GRAY, YELLOW = (_e.get(k, v) for k, v in
            (('tinta', INK), ('alerta', RED), ('destaque', ORANGE), ('ok', GREEN), ('neutro', GRAY), ('marca_texto', YELLOW)))
        PAPER, FONT_NAME, FONT_FILE = _e.get('papel', PAPER), _e.get('fonte_nome', FONT_NAME), _e.get('fonte_arquivo', FONT_FILE)
        break
_DEFAULT = {'#173f4f': 'INK', '#b3261e': 'RED', '#e8912e': 'ORANGE', '#3d8b3d': 'GREEN', '#f0b43c': 'YELLOW', '#fcf3e1': 'PAPER'}
def _estilo(html):
    for hx, name in _DEFAULT.items():
        html = html.replace(hx, globals()[name])
    return html.replace('assets/Chewy-Regular.ttf', 'assets/' + FONT_FILE).replace('font-family:Chewy', 'font-family:"%s"' % FONT_NAME).replace('Chewy,sans-serif', '"%s",sans-serif' % FONT_NAME)

def norm(w):
    w = unicodedata.normalize('NFD', w.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in w if unicodedata.category(c) != 'Mn'))

MISSING = []
def wt(sid, key, nth=1, d=0.0):
    s, k, c = SC[sid], norm(key), 0
    for w in s['words']:
        if norm(w['w']).startswith(k):
            c += 1
            if c == nth:
                return max(s['start'], w['start']) + d
    MISSING.append(f'{sid}:{key}:{nth}')
    return s['start'] + 0.5 + d

def st(i, d=0.15): return SC[i]['start'] + d
def en(i, d=0.0): return (SC[i]['end'] if i != LAST else AUDIO_END) - d

# ---------------------------------------------------------------- construtores
def T(text, x=960, y=130, px=118, at=None, ticks=True, color=None): return dict(k='T', text=text, x=x, y=y, px=px, at=at, ticks=ticks, color=color)
def TAG(text, x, y, px=64, at=None): return dict(k='TAG', text=text, x=x, y=y, px=px, at=at)
def CUT(name, x, y, w, at, css='', enter='wipe', flip=False, wiggle=False, beat=False, slide=None): return dict(k='CUT', name=name, x=x, y=y, w=w, at=at, css=css, enter=enter, flip=flip, wiggle=wiggle, beat=beat, slide=slide)
def FRAME(img, x, y, w, h, at, color='teal', pos='50% 50%'): return dict(k='FRAME', img=img, x=x, y=y, w=w, h=h, at=at, color=color, pos=pos)
def ARROW(x1, y1, x2, y2, at, bend=0.18, color=ORANGE, dur=0.6): return dict(k='ARROW', p=(x1, y1, x2, y2), at=at, bend=bend, color=color, dur=dur)
def NO(x, y, r, at): return dict(k='NO', x=x, y=y, r=r, at=at)
def XX(x, y, s, at): return dict(k='XX', x=x, y=y, s=s, at=at)
def CHECK(x, y, s, at): return dict(k='CHECK', x=x, y=y, s=s, at=at)
def HALO(x, y, w, h, at, color='#7fb7c9'): return dict(k='HALO', x=x, y=y, w=w, h=h, at=at, color=color)
def MOVE(name, pts, w, t0, dur, n=1, gap=0.25): return dict(k='MOVE', name=name, pts=pts, w=w, t0=t0, dur=dur, n=n, gap=gap)
def DROP(pts, t0, dur, s=34): return dict(k='DROP', pts=pts, t0=t0, dur=dur, s=s)
def NUM(n, x, y, at, px=150): return dict(k='NUM', n=n, x=x, y=y, at=at, px=px)
def CARD(n, x, y, w, at): return dict(k='CARD', n=n, x=x, y=y, w=w, at=at)
def ZOOM(img, cx, cy, r, at, fx=0.5, fy=0.5, fz=2.5, src=None): return dict(k='ZOOM', img=img, cx=cx, cy=cy, r=r, at=at, fx=fx, fy=fy, fz=fz, src=src)
def PRESS(x, y, at, gap=70, size=70): return dict(k='PRESS', x=x, y=y, at=at, gap=gap, size=size)
def PAIN(x, y, at, s=60): return dict(k='PAIN', x=x, y=y, at=at, s=s)
def DARK(x, y, w, h, at): return dict(k='DARK', x=x, y=y, w=w, h=h, at=at)
def BEAM(x1, y1, x2, y2, at, spread=170): return dict(k='BEAM', p=(x1, y1, x2, y2), at=at, spread=spread)
def REVEAL(name, x, y, w, at, dur=1.4): return dict(k='REVEAL', name=name, x=x, y=y, w=w, at=at, dur=dur)
def COUNTER(a, b, x, y, px, t0, t1, suf='', color=None): return dict(k='COUNTER', a=a, b=b, x=x, y=y, px=px, t0=t0, t1=t1, suf=suf, color=color)
def BAR(x, yb, w, h, at, color=ORANGE): return dict(k='BAR', x=x, yb=yb, w=w, h=h, at=at, color=color)
def LINE(x1, y1, x2, y2, at, color=INK, wd=8, dur=.6): return dict(k='LINE', p=(x1, y1, x2, y2), at=at, color=color, wd=wd, dur=dur)
def BG(img, at): return dict(k='BG', img=img, at=at)
def BTN(text, x, y, at): return dict(k='BTN', text=text, x=x, y=y, at=at)
def FLASH(at): return dict(k='FLASH', at=at)
def ROWS(rows, at, until, top=230, step=98): return dict(k='ROWS', rows=rows, at=at, until=until, top=top, step=step)
def pt(name, x, y, w, fx, fy):
    h = w * ar(name)
    return (round(x - w / 2 + fx * w), round(y - h / 2 + fy * h))

SPEC = {}

RED_WORDS = re.compile(r'^(NÃO|NUNCA|FALSOS?|ERRO|NADA)[,.!?]?$')

# ---------------------------------------------------------------- desenho
def jitter_rect(x, y, w, h, r=34, seed=1, amp=3.2, step=26):
    """retângulo arredondado com contorno tremido (traço à mão)"""
    rnd = random.Random(seed)
    pts = []
    def arc(cx, cy, a0, a1):
        for k in range(7):
            a = math.radians(a0 + (a1 - a0) * k / 6)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    def line(x0, y0, x1, y1):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / step))
        for k in range(1, n):
            t = k / n
            pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    arc(x + r, y + r, 180, 270); line(x + r, y, x + w - r, y)
    arc(x + w - r, y + r, 270, 360); line(x + w, y + r, x + w, y + h - r)
    arc(x + w - r, y + h - r, 0, 90); line(x + w - r, y + h, x + r, y + h)
    arc(x + r, y + h - r, 90, 180); line(x, y + h - r, x, y + r)
    pts = [(px + rnd.uniform(-amp, amp), py + rnd.uniform(-amp, amp)) for px, py in pts]
    d = 'M%.1f %.1f ' % pts[0]
    for k in range(1, len(pts)):
        mx, my = (pts[k - 1][0] + pts[k][0]) / 2, (pts[k - 1][1] + pts[k][1]) / 2
        d += 'Q%.1f %.1f %.1f %.1f ' % (pts[k - 1][0], pts[k - 1][1], mx, my)
    return d + 'Z'

def path_len(pts):
    return sum(math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]) for k in range(len(pts) - 1))

def curve(x1, y1, x2, y2, bend):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    nx, ny = -(y2 - y1), (x2 - x1)
    cx, cy = mx + nx * bend, my + ny * bend
    pts = [((1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t * t * x2, (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t * t * y2) for t in [k / 40 for k in range(41)]]
    return f'M{x1} {y1} Q{cx:.0f} {cy:.0f} {x2} {y2}', pts

CSS = '''
@font-face{font-family:Chewy;src:url(assets/Chewy-Regular.ttf)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:transparent}
#root{position:relative;width:1920px;height:1080px;font-family:Chewy,sans-serif}
.clip{position:absolute;inset:0}
.t{position:absolute;transform:translate(-50%,-50%);white-space:nowrap;line-height:1;letter-spacing:1px;filter:url(#rough)}
.t span{display:inline-block}
.tick{position:absolute;height:9px;border-radius:5px;background:#e8a23a}
.tag{position:absolute;transform:translate(-50%,-50%);white-space:nowrap;color:#173f4f;padding:10px 34px 14px}
.tag .b{position:absolute;inset:0;background:#f0b43c;border-radius:14px 30px 18px 34px/30px 14px 34px 18px;transform-origin:0 50%;filter:url(#rough2)}
.tag .x{position:relative}
.cut{position:absolute;transform-origin:50% 50%}
.cut img{width:100%;display:block;filter:drop-shadow(0 8px 10px rgba(80,60,30,.18))}
.svg{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}
.fr{position:absolute;overflow:hidden;border-radius:30px}
.fr img{width:100%;height:100%;object-fit:cover;transform-origin:50% 50%}
.card{position:absolute;transform-origin:50% 50%}
.card img{width:100%;display:block}
.card b{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;font-weight:400;color:#173f4f;filter:url(#rough)}
.halo{position:absolute;border-radius:50%;filter:blur(18px)}
'''

SVG_DEFS = '''<svg width="0" height="0" style="position:absolute"><defs>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="3.2"/></filter>
<filter id="rough2"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="3" seed="9"/><feDisplacementMap in="SourceGraphic" scale="9"/></filter>
<filter id="glow"><feGaussianBlur stdDeviation="5"/></filter>
</defs></svg>'''

def js(v): return json.dumps(v, ensure_ascii=False)

class Block:
    def __init__(self, t0, dur):
        self.t0, self.dur, self.els, self.tl, self.n = t0, dur, [], [], 0
    def r(self, t, a):            # instante relativo ao bloco, nunca antes do início da cena
        return round(max(a + .02, t - self.t0), 3)
    def uid(self, p):
        self.n += 1
        return f'{p}{self.n}'
    def tw(self, sel, fr, to, at):
        self.tl.append(f'tl.fromTo({js(sel)},{js(fr)},{js(to)},{at});')

    def add(self, e, a, b, sid):
        k = e['k']
        if k == 'T':
            self.letreiro(e, a, b, sid)
        elif k == 'TAG':
            i = self.uid('g'); at = self.r(e['at'], a)
            self.els.append(f'<div id="{i}" class="tag" style="left:{e["x"]}px;top:{e["y"]}px;font-size:{e["px"]}px"><div class="b"></div><div class="x">{e["text"]}</div></div>')
            self.tw(f'#{i} .b', {'scaleX': 0}, {'scaleX': 1, 'duration': .3, 'ease': 'power2.out'}, at)
            self.tw(f'#{i} .x', {'opacity': 0, 'x': -12}, {'opacity': 1, 'x': 0, 'duration': .3}, at + .15)
        elif k == 'CUT':
            i = self.uid('c'); at = self.r(e['at'], a)
            w = e['w']
            hh = w * ar(e['name'])
            if hh > 660:                       # nunca invade o título nem passa da borda de baixo
                w, hh = 660 / ar(e['name']), 660
            top = min(max(235, e['y'] - hh / 2), 1065 - hh)
            self.els.append(f'<div id="{i}" class="cut" style="left:{e["x"] - w / 2:.0f}px;top:{top:.0f}px;width:{w:.0f}px;height:{hh:.0f}px">'
                            f'<img src="cut/{e["name"]}.png" style="{e["css"]}{"transform:scaleX(-1);" if e["flip"] else ""}"></div>')
            if e['enter'] == 'pop':
                self.tw(f'#{i}', {'scale': .85, 'opacity': 0}, {'scale': 1, 'opacity': 1, 'duration': .35, 'ease': 'back.out(1.6)'}, at)
            else:   # pincelada: revela da esquerda para a direita com borda irregular
                self.tw(f'#{i}', {'clipPath': 'inset(-10% 100% -10% -10%)', 'opacity': 1}, {'clipPath': 'inset(-10% -10% -10% -10%)', 'duration': .55, 'ease': 'power2.out'}, at)
                self.tw(f'#{i}', {'scale': .97}, {'scale': 1, 'duration': .55, 'ease': 'power2.out'}, at)
            if e.get('beat'):
                self.tw(f'#{i} img', {'scale': 1}, {'scale': 1.09, 'duration': .22, 'repeat': max(1, int((b - at) / .22)), 'yoyo': True, 'ease': 'sine.inOut'}, at + .5)
            elif e.get('wiggle'):
                self.tw(f'#{i} img', {'rotation': -4}, {'rotation': 4, 'duration': .5, 'repeat': max(1, int((b - at) / .5)), 'yoyo': True, 'ease': 'sine.inOut'}, at + .5)
            else:
                self.tw(f'#{i} img', {'scale': 1}, {'scale': 1.03, 'duration': max(.5, b - at), 'ease': 'sine.inOut'}, at)
            if e.get('slide'):
                dx, dy, ts = e['slide']
                self.tw(f'#{i}', {'x': 0, 'y': 0}, {'x': dx, 'y': dy, 'duration': .9, 'ease': 'power2.inOut'}, self.r(ts, a))
        elif k == 'PAIN':
            i = self.uid('q'); at = self.r(e['at'], a); x, y, s = e['x'], e['y'], e['s']
            ls = ''
            for ang in (-150, -110, -70, -30, 10):
                ra = math.radians(ang)
                ls += (f'<line x1="{x + s * .6 * math.cos(ra):.0f}" y1="{y + s * .6 * math.sin(ra):.0f}" x2="{x + s * 1.3 * math.cos(ra):.0f}" y2="{y + s * 1.3 * math.sin(ra):.0f}" '
                       f'stroke="{ORANGE}" stroke-width="10" stroke-linecap="round"/>')
            self.els.append(f'<svg class="svg"><g id="{i}" style="transform-origin:{x}px {y}px">{ls}</g></svg>')
            self.tw(f'#{i}', {'scale': 0, 'opacity': 0}, {'scale': 1, 'opacity': 1, 'duration': .2, 'ease': 'back.out(3)'}, at)
            self.tw(f'#{i}', {'scale': 1}, {'scale': 1.25, 'duration': .2, 'repeat': max(1, int((b - at) / .2)), 'yoyo': True}, at + .2)
        elif k == 'DARK':
            i = self.uid('k'); at = self.r(e['at'], a)
            x, y = e['x'] - e['w'] / 2, e['y'] - e['h'] / 2
            self.els.append(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{e["w"]}px;height:{e["h"]}px;border-radius:30px;'
                            f'background:radial-gradient(ellipse at 50% 60%,#2a3257,#10142a);border:7px solid {INK};box-shadow:0 0 0 6px rgba(232,145,46,.35)"></div>')
            self.tw(f'#{i}', {'opacity': 0, 'scale': .96}, {'opacity': 1, 'scale': 1, 'duration': .4}, at)
        elif k == 'BEAM':
            i = self.uid('b'); at = self.r(e['at'], a); x1, y1, x2, y2 = e['p']; sp = e['spread']
            ang = math.atan2(y2 - y1, x2 - x1); nx, ny = -math.sin(ang), math.cos(ang)
            poly = f'{x1},{y1} {x2 + nx * sp:.0f},{y2 + ny * sp:.0f} {x2 - nx * sp:.0f},{y2 - ny * sp:.0f}'
            self.els.append(f'<svg class="svg"><defs><linearGradient id="{i}g" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
                            f'<stop offset="0" stop-color="#b04dff" stop-opacity=".85"/><stop offset="1" stop-color="#7a3cff" stop-opacity=".12"/></linearGradient></defs>'
                            f'<polygon id="{i}" points="{poly}" fill="url(#{i}g)" style="filter:blur(6px)"/></svg>')
            self.tw(f'#{i}', {'opacity': 0}, {'opacity': 1, 'duration': .35}, at)
            self.tw(f'#{i}', {'opacity': 1}, {'opacity': .75, 'duration': .3, 'repeat': max(1, int((b - at) / .3)), 'yoyo': True}, at + .4)
        elif k == 'REVEAL':
            i = self.uid('v'); at = self.r(e['at'], a); w = e['w']; hh = w * ar(e['name'])
            box = f'left:{e["x"] - w / 2:.0f}px;top:{e["y"] - hh / 2:.0f}px;width:{w}px;height:{hh:.0f}px'
            self.els.append(f'<div id="{i}a" class="cut" style="{box}"><img src="cut/{e["name"]}.png" style="filter:grayscale(1) opacity(.55)"></div>'
                            f'<div id="{i}b" class="cut" style="{box}"><img src="cut/{e["name"]}.png" style="filter:saturate(1.4) drop-shadow(0 0 10px rgba(240,180,60,.8))"></div>')
            self.tw(f'#{i}a', {'opacity': 0}, {'opacity': 1, 'duration': .3}, round(max(a + .02, at - .6), 3))
            self.tw(f'#{i}b', {'clipPath': 'inset(100% 0% 0% 0%)'}, {'clipPath': 'inset(0% 0% 0% 0%)', 'duration': e['dur'], 'ease': 'power1.inOut'}, at)
        elif k == 'COUNTER':
            i = self.uid('o'); t0 = self.r(e['t0'], a); t1 = max(t0 + .3, e['t1'] - self.t0)
            self.els.append(f'<div id="{i}" class="t" style="left:{e["x"]}px;top:{e["y"]}px;font-size:{e["px"]}px;color:{e["color"] or RED}">{e["a"]}{e["suf"]}</div>')
            self.tw(f'#{i}', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1, 'duration': .25}, t0)
            self.tl.append(f'(function(){{const el=document.getElementById("{i}");const o={{v:{e["a"]}}};tl.to(o,{{v:{e["b"]},duration:{round(t1 - t0, 3)},ease:"power1.out",'
                           f'onUpdate:()=>{{el.textContent=Math.round(o.v)+{js(e["suf"])}}}}},{t0});}})();')
        elif k == 'BAR':
            i = self.uid('r'); at = self.r(e['at'], a)
            self.els.append(f'<div id="{i}" style="position:absolute;left:{e["x"] - e["w"] / 2}px;top:{e["yb"] - e["h"]}px;width:{e["w"]}px;height:{e["h"]}px;'
                            f'background:{e["color"]};border:6px solid {INK};border-radius:14px 14px 4px 4px;transform-origin:50% 100%;filter:url(#rough)"></div>')
            self.tw(f'#{i}', {'scaleY': 0}, {'scaleY': 1, 'duration': .8, 'ease': 'power2.out'}, at)
        elif k == 'LINE':
            i = self.uid('l'); at = self.r(e['at'], a); x1, y1, x2, y2 = e['p']; L = math.hypot(x2 - x1, y2 - y1)
            self.els.append(f'<svg class="svg" style="filter:url(#rough)"><line id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{e["color"]}" stroke-width="{e["wd"]}" stroke-linecap="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"/></svg>')
            self.tw(f'#{i}', {'strokeDashoffset': L}, {'strokeDashoffset': 0, 'duration': e['dur'], 'ease': 'power1.inOut'}, at)
        elif k == 'BG':
            i = self.uid('w'); at = self.r(e['at'], a)
            self.els.append(f'<div id="{i}" style="position:absolute;inset:0;overflow:hidden"><img src="{e["img"]}" style="width:100%;height:100%;object-fit:cover"></div>')
            self.tw(f'#{i}', {'opacity': 0}, {'opacity': 1, 'duration': .35}, at)
            self.tw(f'#{i} img', {'scale': 1}, {'scale': 1.04, 'duration': max(.5, b - at), 'ease': 'none'}, at)
        elif k == 'BTN':
            i = self.uid('n'); at = self.r(e['at'], a)
            self.els.append(f'<div id="{i}" class="t" style="left:{e["x"]}px;top:{e["y"]}px;font-size:76px;color:#fff;background:{RED};padding:18px 50px 24px;border-radius:22px;box-shadow:0 10px 0 #7d1712;filter:none">{e["text"]}</div>')
            self.tw(f'#{i}', {'scale': 0}, {'scale': 1, 'duration': .4, 'ease': 'back.out(2)'}, at)
            self.tw(f'#{i}', {'scale': 1}, {'scale': 1.07, 'duration': .45, 'repeat': 5, 'yoyo': True, 'ease': 'sine.inOut'}, at + .45)
        elif k == 'FLASH':
            i = self.uid('h'); at = self.r(e['at'], a)
            self.els.append(f'<div id="{i}" style="position:absolute;inset:0;background:#fff;opacity:0"></div>')
            self.tw(f'#{i}', {'opacity': 0}, {'opacity': .85, 'duration': .08, 'yoyo': True, 'repeat': 1}, at)
        elif k == 'ROWS':
            i = self.uid('s'); at = self.r(e['at'], a)
            n = len(e['rows']); H2 = e['step'] * n + 40
            hh = ''.join(f'<div id="{i}r{j}" style="position:absolute;left:330px;top:{e["top"] + e["step"] * j}px;height:{e["step"]}px;display:flex;align-items:center;gap:26px;'
                         f'font-size:52px;color:{INK};white-space:nowrap"><img src="cut/{nm}.png" style="height:{e["step"] - 14}px;width:{e["step"] + 10}px;object-fit:contain">'
                         f'<span style="filter:url(#rough)">{tx}</span></div>' for j, (nm, tx) in enumerate(e['rows']))
            d = jitter_rect(270, e['top'] - 24, 1380, H2, seed=7)
            self.els.append(f'<svg class="svg"><path d="{d}" fill="#fffaf0" stroke="{INK}" stroke-width="7"/></svg>{hh}')
            stp = max(.18, (e['until'] - e['at'] - .3) / n)
            for j in range(n):
                self.tw(f'#{i}r{j}', {'opacity': 0, 'x': -40}, {'opacity': 1, 'x': 0, 'duration': .25}, round(at + stp * j, 3))
        elif k == 'FRAME':

            self.frame(e, a, b)
        elif k == 'ARROW':
            i = self.uid('a'); at = self.r(e['at'], a)
            x1, y1, x2, y2 = e['p']
            d, pts = curve(x1, y1, x2, y2, e['bend'])
            L = path_len(pts)
            (px, py), (qx, qy) = pts[-4], pts[-1]
            ang = math.atan2(qy - py, qx - px)
            h1 = (qx - 30 * math.cos(ang - .5), qy - 30 * math.sin(ang - .5))
            h2 = (qx - 30 * math.cos(ang + .5), qy - 30 * math.sin(ang + .5))
            self.els.append(f'<svg class="svg"><defs><mask id="{i}m" maskUnits="userSpaceOnUse"><path id="{i}mp" d="{d}" stroke="#fff" stroke-width="30" fill="none" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"/></mask></defs>'
                            f'<path d="{d}" stroke="{e["color"]}" stroke-width="9" fill="none" stroke-linecap="round" stroke-dasharray="1 20" mask="url(#{i}m)"/>'
                            f'<path id="{i}h" d="M{h1[0]:.0f} {h1[1]:.0f} L{qx:.0f} {qy:.0f} L{h2[0]:.0f} {h2[1]:.0f}" stroke="{e["color"]}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0"/></svg>')
            self.tw(f'#{i}mp', {'strokeDashoffset': L}, {'strokeDashoffset': 0, 'duration': e['dur'], 'ease': 'power1.inOut'}, at)
            self.tw(f'#{i}h', {'opacity': 0}, {'opacity': 1, 'duration': .12}, at + e['dur'] - .05)
        elif k == 'NO':
            i = self.uid('n'); at = self.r(e['at'], a); x, y, r = e['x'], e['y'], e['r']
            C = 2 * math.pi * r; dx = r * .7
            self.els.append(f'<svg class="svg" style="filter:url(#rough)"><circle id="{i}c" cx="{x}" cy="{y}" r="{r}" stroke="{RED}" stroke-width="20" fill="none" stroke-dasharray="{C:.0f}" stroke-dashoffset="{C:.0f}" transform="rotate(-120 {x} {y})" opacity=".92"/>'
                            f'<line id="{i}l" x1="{x - dx:.0f}" y1="{y - dx:.0f}" x2="{x + dx:.0f}" y2="{y + dx:.0f}" stroke="{RED}" stroke-width="20" stroke-linecap="round" stroke-dasharray="{2 * r:.0f}" stroke-dashoffset="{2 * r:.0f}" opacity=".92"/></svg>')
            self.tw(f'#{i}c', {'strokeDashoffset': C}, {'strokeDashoffset': 0, 'duration': .45, 'ease': 'power2.inOut'}, at)
            self.tw(f'#{i}l', {'strokeDashoffset': 2 * r}, {'strokeDashoffset': 0, 'duration': .25, 'ease': 'power2.out'}, at + .42)
        elif k == 'XX':
            i = self.uid('x'); at = self.r(e['at'], a); x, y, s = e['x'], e['y'], e['s'] / 2
            L = s * 2.9
            self.els.append(f'<svg class="svg" style="filter:url(#rough)">'
                            f'<path id="{i}1" d="M{x - s} {y - s} Q{x} {y + 6} {x + s} {y + s}" stroke="{RED}" stroke-width="{max(14, s * .28):.0f}" stroke-linecap="round" fill="none" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"/>'
                            f'<path id="{i}2" d="M{x + s} {y - s} Q{x + 4} {y} {x - s} {y + s}" stroke="{RED}" stroke-width="{max(14, s * .28):.0f}" stroke-linecap="round" fill="none" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"/></svg>')
            self.tw(f'#{i}1', {'strokeDashoffset': L}, {'strokeDashoffset': 0, 'duration': .18, 'ease': 'power2.out'}, at)
            self.tw(f'#{i}2', {'strokeDashoffset': L}, {'strokeDashoffset': 0, 'duration': .18, 'ease': 'power2.out'}, at + .17)
        elif k == 'CHECK':
            i = self.uid('k'); at = self.r(e['at'], a); x, y, s = e['x'], e['y'], e['s'] / 2
            self.els.append(f'<svg class="svg"><g id="{i}" style="transform-origin:{x}px {y}px"><circle cx="{x}" cy="{y}" r="{s}" fill="{GREEN}"/>'
                            f'<path id="{i}p" d="M{x - s * .45} {y + s * .02} L{x - s * .1} {y + s * .38} L{x + s * .5} {y - s * .35}" stroke="#fff" stroke-width="{s * .2:.0f}" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke-dasharray="{s * 2:.0f}" stroke-dashoffset="{s * 2:.0f}"/></g></svg>')
            self.tw(f'#{i}', {'scale': 0}, {'scale': 1, 'duration': .3, 'ease': 'back.out(2.2)'}, at)
            self.tw(f'#{i}p', {'strokeDashoffset': s * 2}, {'strokeDashoffset': 0, 'duration': .25}, at + .2)
        elif k == 'HALO':
            i = self.uid('h'); at = self.r(e['at'], a)
            self.els.append(f'<div id="{i}" class="halo" style="left:{e["x"] - e["w"] / 2}px;top:{e["y"] - e["h"] / 2}px;width:{e["w"]}px;height:{e["h"]}px;'
                            f'background:radial-gradient(closest-side,{e["color"]}cc,{e["color"]}00)"></div>')
            self.tw(f'#{i}', {'opacity': 0, 'scale': .6}, {'opacity': 1, 'scale': 1, 'duration': .5}, at)
            self.tw(f'#{i}', {'opacity': 1}, {'opacity': .55, 'duration': .45, 'repeat': 5, 'yoyo': True}, at + .5)
        elif k in ('MOVE', 'DROP'):
            pts = e['pts']
            for j in range(e.get('n', 1)):
                i = self.uid('m'); at = self.r(e['t0'] + j * e.get('gap', 0), a)
                if k == 'MOVE':
                    w = e['w']
                    hh = w * ar(e['name'])
                    self.els.append(f'<div id="{i}" class="cut" style="left:{pts[0][0] - w / 2:.0f}px;top:{pts[0][1] - hh / 2:.0f}px;width:{w}px;height:{hh:.0f}px;opacity:0"><img src="cut/{e["name"]}.png"></div>')
                else:
                    s = e['s']
                    self.els.append(f'<div id="{i}" style="position:absolute;left:{pts[0][0] - s / 2}px;top:{pts[0][1] - s * .65}px;width:{s}px;height:{s * 1.3:.0f}px;opacity:0;'
                                    f'border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:radial-gradient(circle at 35% 35%,#ffe58a,#e2a51c);border:3px solid #8a5a10"></div>')
                self.tw(f'#{i}', {'opacity': 0, 'scale': .4}, {'opacity': 1, 'scale': 1, 'duration': .25}, at)
                seg = e['dur'] / max(1, len(pts) - 1)
                for q in range(1, len(pts)):
                    self.tw(f'#{i}', {'x': pts[q - 1][0] - pts[0][0], 'y': pts[q - 1][1] - pts[0][1]},
                            {'x': pts[q][0] - pts[0][0], 'y': pts[q][1] - pts[0][1], 'duration': seg, 'ease': 'sine.inOut'}, round(at + .1 + seg * (q - 1), 3))
        elif k == 'NUM':
            i = self.uid('u'); at = self.r(e['at'], a)
            self.els.append(f'<div id="{i}" class="t" style="left:{e["x"]}px;top:{e["y"]}px;font-size:{e["px"]}px;color:{INK}">{e["n"]}</div>')
            self.tw(f'#{i}', {'scale': 0, 'opacity': 0}, {'scale': 1, 'opacity': 1, 'duration': .35, 'ease': 'back.out(2)'}, at)
        elif k == 'CARD':
            i = self.uid('d'); at = self.r(e['at'], a); w = e['w']
            hh = w * ar('carta')
            self.els.append(f'<div id="{i}" class="card" style="left:{e["x"] - w / 2}px;top:{e["y"] - hh / 2:.0f}px;width:{w}px;height:{hh:.0f}px">'
                            f'<img src="cut/carta.png"><b style="font-size:{w * .55:.0f}px">{e["n"]}</b></div>')
            self.tw(f'#{i}', {'rotationY': -180, 'opacity': 0}, {'rotationY': 0, 'opacity': 1, 'duration': .6, 'ease': 'back.out(1.3)'}, at)
        elif k == 'PRESS':
            i = self.uid('p'); at = self.r(e['at'], a); x, y, g, s = e['x'], e['y'], e['gap'], e['size']
            self.els.append(f'<svg class="svg"><g id="{i}t"><path d="M{x} {y - g - s * 2} L{x} {y - g}" stroke="{ORANGE}" stroke-width="16" stroke-linecap="round"/>'
                            f'<path d="M{x - 26} {y - g - 30} L{x} {y - g} L{x + 26} {y - g - 30}" stroke="{ORANGE}" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
                            f'<g id="{i}b"><path d="M{x} {y + g + s * 2} L{x} {y + g}" stroke="{ORANGE}" stroke-width="16" stroke-linecap="round"/>'
                            f'<path d="M{x - 26} {y + g + 30} L{x} {y + g} L{x + 26} {y + g + 30}" stroke="{ORANGE}" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></svg>')
            self.tw(f'#{i}t', {'opacity': 0, 'y': -60}, {'opacity': 1, 'y': 0, 'duration': .35, 'ease': 'power2.in'}, at)
            self.tw(f'#{i}b', {'opacity': 0, 'y': 60}, {'opacity': 1, 'y': 0, 'duration': .35, 'ease': 'power2.in'}, at)
            self.tw(f'#{i}t', {'y': 0}, {'y': 12, 'duration': .3, 'repeat': 7, 'yoyo': True}, at + .4)
            self.tw(f'#{i}b', {'y': 0}, {'y': -12, 'duration': .3, 'repeat': 7, 'yoyo': True}, at + .4)
        elif k == 'ZOOM':
            self.zoom(e, a, b)
        else:
            raise ValueError(k)

    def letreiro(self, e, a, b, sid):
        i = self.uid('t'); at = self.r(e['at'] if e['at'] is not None else st(sid, .05), a)
        words = e['text'].split(' ')
        html = []
        for wi, w in enumerate(words):
            col = e['color'] or (RED if RED_WORDS.match(w) else INK)
            html.append(''.join(f'<span style="color:{col}">{c}</span>' for c in w))
        self.els.append(f'<div id="{i}" class="t" style="left:{e["x"]}px;top:{e["y"]}px;font-size:{e["px"]}px">{"<span>&nbsp;</span>".join(html)}</div>')
        n = len(e['text'])
        stg = min(.045, .5 / max(1, n))
        self.tw(f'#{i} span', {'opacity': 0, 'y': 8, 'scale': .7}, {'opacity': 1, 'y': 0, 'scale': 1, 'duration': .16, 'stagger': stg, 'ease': 'back.out(2)'}, at)
        if e['ticks']:
            wpx = n * e['px'] * .5 + 40
            tk = ''
            for side in (-1, 1):
                for j, (dy, rot) in enumerate(((-30, -28), (0, 0), (30, 28))):
                    x = e['x'] + side * (wpx / 2 + 22) - (36 if side < 0 else 0)
                    tk += (f'<div class="tick {i}k" style="left:{x:.0f}px;top:{e["y"] + dy - 4}px;width:36px;'
                           f'transform:rotate({rot * -side}deg)"></div>')
            self.els.append(tk)
            self.tw(f'.{i}k', {'opacity': 0, 'scaleX': 0}, {'opacity': 1, 'scaleX': 1, 'duration': .2, 'stagger': .03}, at + stg * n + .05)

    def frame(self, e, a, b):
        i = self.uid('f'); at = self.r(e['at'], a)
        x, y, w, h = e['x'] - e['w'] / 2, e['y'] - e['h'] / 2, e['w'], e['h']
        d = jitter_rect(x, y, w, h, seed=self.n)
        L = 2 * (w + h)
        col = {'teal': INK, 'green': GREEN, 'red': RED, 'gray': GRAY}[e['color']]
        glow = ORANGE if e['color'] == 'teal' else col
        inner = f'<img src="{e["img"]}" style="object-position:{e["pos"]}">' if e['img'] else ''
        self.els.append(f'<div id="{i}" class="fr" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>'
                        f'<svg class="svg"><path id="{i}g" d="{d}" stroke="{glow}" stroke-width="20" fill="none" opacity=".55" filter="url(#glow)" stroke-dasharray="{L}" stroke-dashoffset="{L}"/>'
                        f'<path id="{i}p" d="{d}" stroke="{col}" stroke-width="7" fill="none" stroke-linecap="round" stroke-dasharray="{L}" stroke-dashoffset="{L}"/></svg>')
        self.tw(f'#{i}', {'clipPath': 'inset(0% 100% 0% 0% round 30px)'}, {'clipPath': 'inset(0% 0% 0% 0% round 30px)', 'duration': .55, 'ease': 'power2.out'}, at)
        self.tw(f'#{i}p', {'strokeDashoffset': L}, {'strokeDashoffset': 0, 'duration': .7, 'ease': 'power1.inOut'}, at)
        self.tw(f'#{i}g', {'strokeDashoffset': L}, {'strokeDashoffset': 0, 'duration': .7, 'ease': 'power1.inOut'}, at)
        if e['img']:
            self.tw(f'#{i} img', {'scale': 1}, {'scale': 1.06, 'duration': max(.5, b - at), 'ease': 'none'}, at)

    def zoom(self, e, a, b):
        i = self.uid('z'); at = self.r(e['at'], a)
        cx, cy, r = e['cx'], e['cy'], e['r']
        C = 2 * math.pi * r
        sz = r * 2 * e['fz']
        asp = ar(e['img'][4:-4]) if e['img'].startswith('cut/') else .5625
        line = ''
        if e['src']:
            sx, sy = e['src']
            line = f'<line id="{i}l" x1="{sx}" y1="{sy}" x2="{cx}" y2="{cy}" stroke="{ORANGE}" stroke-width="5" stroke-dasharray="10 9" opacity="0"/>'
        self.els.append(f'<svg class="svg">{line}</svg>'
                        f'<div id="{i}" style="position:absolute;left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;overflow:hidden;background:#fcf3e1">'
                        f'<img src="{e["img"]}" style="position:absolute;width:{sz:.0f}px;left:{r - sz * e["fx"]:.0f}px;top:{r - sz * e["fy"] * asp:.0f}px"></div>'
                        f'<svg class="svg"><circle id="{i}c" cx="{cx}" cy="{cy}" r="{r}" stroke="{ORANGE}" stroke-width="12" fill="none" stroke-dasharray="{C:.0f}" stroke-dashoffset="{C:.0f}" filter="url(#rough)"/></svg>')
        if e['src']:
            self.tw(f'#{i}l', {'opacity': 0}, {'opacity': 1, 'duration': .2}, at)
        self.tw(f'#{i}', {'scale': 0}, {'scale': 1, 'duration': .45, 'ease': 'back.out(1.5)'}, at + .1)
        self.tw(f'#{i}c', {'strokeDashoffset': C}, {'strokeDashoffset': 0, 'duration': .5}, at + .1)

    def html(self, cid):
        return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<script src="assets/gsap.min.js"></script><style>{CSS}</style></head>
<body>{SVG_DEFS}<div id="root" data-composition-id="{cid}" data-start="0" data-duration="{self.dur}" data-width="1920" data-height="1080" data-fps="30">
{chr(10).join(self.els)}
</div>
<script>
const tl=gsap.timeline({{paused:true}});
{chr(10).join(self.tl)}
window.__timelines=window.__timelines||{{}};window.__timelines["{cid}"]=tl;tl.seek(0);
</script></body></html>'''

def build(first, last, cid):
    t0 = SC[first]['start'] if first != 1 else 0.0
    t_end = en(last)
    B = Block(t0, round(t_end - t0, 3))
    for sid in range(first, last + 1):
        a, b = round(SC[sid]['start'] - t0, 3), round(en(sid) - t0, 3)
        B.els.append(f'<div class="clip" data-start="{a}" data-duration="{round(b - a, 3)}">')
        spec = SPEC.get(sid) or [T(SC[sid]['text'])]
        spec = [x for x in spec if x['k'] == 'BG'] + [x for x in spec if x['k'] != 'BG']   # fundo sempre atrás do título
        if not any(x['k'] == 'T' for x in spec):
            spec = [T(SC[sid]['text'])] + spec
        for e in spec:
            B.add(e, a, b, sid)
        B.els.append('</div>')
    open(f'hf/{cid}.html', 'w', encoding='utf-8').write(_estilo(B.html(cid)))
    return dict(first=first, last=last, start=round(t0, 3), duration=B.dur, file=f'{cid}.html')

if __name__ == '__main__':
    # projeto.json (na pasta work): {"spec": "spec", "blocos": [1, 18, 31, ...]}  -> primeira cena de cada bloco
    P = json.load(open('projeto.json', encoding='utf-8'))
    BLOCK_STARTS = P['blocos']
    sys.path.insert(0, os.path.abspath('.'))
    SPEC.update(__import__(P.get('spec', 'spec')).SPEC)
    n = len(BLOCK_STARTS)
    only = [int(x) for x in sys.argv[1:]] or range(1, n + 1)
    info = []
    for bnum in only:
        bi = bnum - 1
        first = BLOCK_STARTS[bi]
        last = BLOCK_STARTS[bi + 1] - 1 if bi + 1 < n else LAST
        d = build(first, last, f'mg_b{bnum:02d}')
        d['block'] = bnum
        info.append(d)
        print(d)
    if len(info) == n:
        json.dump(info, open('hf/blocks.json', 'w'), indent=1)
    import gen_ref as G
    print('PALAVRAS NÃO ENCONTRADAS:', G.MISSING + MISSING)
