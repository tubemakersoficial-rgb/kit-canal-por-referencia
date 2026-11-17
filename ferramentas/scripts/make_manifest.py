# grava o manifesto que o script do DaVinci Resolve lê (~/.canal-por-referencia/manifest_atual.json)
# uso (na pasta work): python make_manifest.py
import json, os
here = os.path.abspath('.')
P = json.load(open('projeto.json', encoding='utf-8'))
blocks = json.load(open('hf/blocks.json'))
ov = []
for b in blocks:
    d = os.path.join(here, 'hf', 'out', 'b%02d' % b['block'])
    ov.append({'pattern': os.path.join(d, 'frame_%06d.png'), 'frames': len([f for f in os.listdir(d) if f.endswith('.png')]), 'start': b['start']})
nome = P.get('projeto_davinci', 'Canal_video')
pasta = os.path.join(os.path.expanduser('~'), '.canal-por-referencia')
os.makedirs(pasta, exist_ok=True)
m = {'project': nome, 'timeline': nome + ' - montagem', 'fps': 30, 'base': os.path.join(here, 'base.mp4'),
     'overlays': ov, 'voz': os.path.join(here, 'narracao.wav'), 'drp': os.path.join(os.path.dirname(here), nome + '.drp')}
out = os.path.join(pasta, 'manifest_atual.json')
json.dump(m, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(out, sum(o['frames'] for o in ov), 'quadros de motion graphics')
