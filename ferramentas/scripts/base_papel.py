"""Monta o vídeo: base.mp4 (papel + quadros/clipes dentro do quadro) e depois o final (camada HTML + voz a -14 LUFS, sem música).

Uso (na pasta work):  python base_papel.py [--only-base]
Lê projeto.json: {"clipes": [cenas com clipe], "saida": "../tema-final.mp4"}. Clipes em clips/NNN.mp4; cena sem clipe usa hf/panels/NNN.jpg.
"""
import json, os, subprocess, sys

FPS = 30
TAIL = 3.0
P = json.load(open('projeto.json', encoding='utf-8'))
OUT = P.get('saida', os.path.join('..', 'video-final.mp4'))
X, Y, WC, HC = 340, 261, 1240, 698          # retângulo do quadro (igual ao CLIP_RECT do spec)
CLIPS = P.get('clipes', [])

scenes = {s['id']: s for s in json.load(open('scenes.json', encoding='utf-8'))}
LAST = max(scenes)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit('FALHOU: %s\n%s' % (' '.join(cmd[:6]), r.stderr[-2500:]))

def dur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))

TOTAL = dur('narracao.wav') + TAIL

def base():
    inp = ['-loop', '1', '-framerate', str(FPS), '-t', '%.3f' % TOTAL, '-i', os.path.join('hf', 'assets', 'papel.png')]
    chain, last = ['[0:v]scale=1920:1080,setsar=1,format=yuv420p[p0]'], 'p0'
    k = 1
    for sid in CLIPS:
        s = scenes[sid]
        a = s['start']
        b = s['end'] if sid != LAST else TOTAL
        d = b - a
        src = 'clips/%03d.mp4' % sid
        if os.path.exists(src):
            inp += ['-i', src]
            pre = '[%d:v]trim=0:%.3f,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=%.3f,trim=0:%.3f,setpts=PTS-STARTPTS' % (k, d, max(0, d - 14.9), d)
        else:                                   # o Flow recusou: quadro parado com zoom bem leve
            inp += ['-loop', '1', '-framerate', str(FPS), '-t', '%.3f' % d, '-i', 'hf/panels/%03d.jpg' % sid]
            pre = "[%d:v]scale=%d:%d,zoompan=z='1+0.04*on/%d':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=%dx%d:fps=%d" % (k, WC * 2, HC * 2, int(d * FPS), WC, HC, FPS)
        chain.append(pre + ',scale=%d:%d,fps=%d,format=yuva420p,fade=t=in:st=0:d=0.35:alpha=1,setpts=PTS+%.3f/TB[c%d]' % (WC, HC, FPS, a, k))
        chain.append('[%s][c%d]overlay=%d:%d:eof_action=pass:enable=\'between(t,%.3f,%.3f)\'[p%d]' % (last, k, X, Y, a, b, k))
        last = 'p%d' % k
        k += 1
    chain.append('[%s]format=yuv420p[vout]' % last)
    open('base_filter.txt', 'w').write(';\n'.join(chain))
    run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-/filter_complex', 'base_filter.txt', '-map', '[vout]', '-t', '%.3f' % TOTAL,
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-r', str(FPS), 'base.mp4'])
    print('base.mp4 pronto', flush=True)

def final():
    blocks = json.load(open('hf/blocks.json'))
    inp = ['-i', 'base.mp4', '-i', 'narracao.wav']
    chain, last = [], '0:v'
    for k, b in enumerate(blocks):
        inp += ['-framerate', str(FPS), '-i', 'hf/out/b%02d/frame_%%06d.png' % b['block']]
        chain.append('[%d:v]format=rgba,setpts=PTS+%f/TB[o%d]' % (2 + k, b['start'], k))
        chain.append('[%s][o%d]overlay=eof_action=pass:format=auto[v%d]' % (last, k, k))
        last = 'v%d' % k
    chain.append('[%s]format=yuv420p[vout]' % last)
    chain.append('[1:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=%f,loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.75:level=false:attack=3:release=60[aout]' % TOTAL)
    open('final_filter.txt', 'w').write(';\n'.join(chain))
    run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-/filter_complex', 'final_filter.txt', '-map', '[vout]', '-map', '[aout]',
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
         '-t', '%.3f' % TOTAL, '-movflags', '+faststart', OUT])
    print('PRONTO:', OUT, flush=True)

if __name__ == '__main__':
    base()
    if '--only-base' not in sys.argv:
        final()
