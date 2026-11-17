# uso: python -I grid.py <pasta> <saida.jpg> [colunas] [largura]
import os, sys
from PIL import Image, ImageDraw, ImageFont
d, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 5
w = int(sys.argv[4]) if len(sys.argv) > 4 else 400
fs = sorted(f for f in os.listdir(d) if f.lower().endswith(('.png', '.jpg')))
h = w * 9 // 16
g = Image.new('RGB', (cols * w, ((len(fs) + cols - 1) // cols) * h), 'white')
try:
    font = ImageFont.truetype('arialbd.ttf', 24)
except OSError:
    font = ImageFont.load_default()
for k, f in enumerate(fs):
    im = Image.open(os.path.join(d, f)).convert('RGB').resize((w, h))
    ImageDraw.Draw(im).text((6, 4), f[:3], fill='red', font=font, stroke_width=3, stroke_fill='white')
    g.paste(im, ((k % cols) * w, (k // cols) * h))
g.save(out, quality=85)
print(len(fs), 'imagens ->', out)
