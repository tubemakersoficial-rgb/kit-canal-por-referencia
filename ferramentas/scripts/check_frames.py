# uso: python -I check_frames.py saida.jpg t1 t2 ...  -> compõe fundo + camada HTML nesses instantes
import json, subprocess, sys
from PIL import Image
blocks = json.load(open('hf/blocks.json'))
out, ts = sys.argv[1], [float(x) for x in sys.argv[2:]]
tiles = []
for t in ts:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', 'base.mp4', '-frames:v', '1', 'check/_b.png'], check=True)
    bg = Image.open('check/_b.png').convert('RGBA')
    b = [x for x in blocks if x['start'] <= t < x['start'] + x['duration']][-1]
    f = int(round((t - b['start']) * 30)) + 1
    try:
        bg.alpha_composite(Image.open('hf/out/b%02d/frame_%06d.png' % (b['block'], f)).convert('RGBA'))
    except FileNotFoundError:
        pass
    tiles.append(bg.convert('RGB').resize((640, 360)))
W = 3
im = Image.new('RGB', (W * 640, ((len(tiles) + W - 1) // W) * 360))
for k, t in enumerate(tiles):
    im.paste(t, ((k % W) * 640, (k // W) * 360))
im.save(out)
