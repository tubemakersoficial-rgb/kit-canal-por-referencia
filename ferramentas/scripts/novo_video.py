"""Cria a pasta de um vídeo novo com tudo o que a produção precisa.

Uso (na raiz do kit):  python ferramentas/scripts/novo_video.py 01-tema-do-video [caminho/do/audio.wav]
Cria videos/01-tema-do-video/ com work/ (scripts, hf/assets, hf/cut com a biblioteca de recortes do canal,
hf/panels) e, se você passar o áudio, copia para work/narracao.wav.
"""
import os, shutil, sys

KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
S = os.path.join(KIT, 'ferramentas', 'scripts')
A = os.path.join(KIT, 'ferramentas', 'assets')

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    nome = sys.argv[1]
    v = os.path.join(KIT, 'videos', nome)
    w = os.path.join(v, 'work')
    for d in ('hf/assets', 'hf/cut', 'hf/panels', 'clips', 'panels_raw', 'check'):
        os.makedirs(os.path.join(w, d), exist_ok=True)
    for f in ('transcrever.py', 'build_scenes.py', 'gen_ref.py', 'base_papel.py', 'check_frames.py', 'grid.py',
              'jobs.py', 'dlp.py', 'make_manifest.py'):
        shutil.copy(os.path.join(S, f), w)
    shutil.copy(os.path.join(S, 'render_blocos.sh'), os.path.join(w, 'hf'))
    shutil.copy(os.path.join(S, 'hyperframes.json'), os.path.join(w, 'hf'))
    for f in os.listdir(A):
        shutil.copy(os.path.join(A, f), os.path.join(w, 'hf', 'assets'))
    for f in ('papel.png', 'estilo.json'):                   # papel e cores próprios do canal, se existirem
        c = os.path.join(KIT, 'canal', f)
        if os.path.exists(c):
            shutil.copy(c, os.path.join(w, 'hf', 'assets') if f.endswith('.png') else w)
    for f in os.listdir(os.path.join(KIT, 'canal')) if os.path.isdir(os.path.join(KIT, 'canal')) else []:
        if f.lower().endswith(('.ttf', '.otf')):             # fonte própria do letreiro
            shutil.copy(os.path.join(KIT, 'canal', f), os.path.join(w, 'hf', 'assets'))
    lib = os.path.join(KIT, 'canal', 'recortes')            # biblioteca de recortes do canal (cresce a cada vídeo)
    if os.path.isdir(lib):
        for f in os.listdir(lib):
            if f.endswith('.png'):
                shutil.copy(os.path.join(lib, f), os.path.join(w, 'hf', 'cut'))
    pj = os.path.join(w, 'projeto.json')
    if not os.path.exists(pj):
        open(pj, 'w', encoding='utf-8').write('{\n "spec": "spec",\n "blocos": [1],\n "clipes": [],\n'
                                              ' "saida": "../%s-final.mp4",\n "projeto_davinci": "%s"\n}\n' % (nome.split('-', 1)[-1], nome))
    if len(sys.argv) > 2:
        shutil.copy(sys.argv[2], os.path.join(w, 'narracao.wav'))
    print('pronto:', v)

if __name__ == '__main__':
    main()
