"""Transcreve um áudio de narração com tempos por frase e por palavra.

Uso: python ferramentas/transcrever.py <audio> [saida.json] [modelo]
Gera um JSON com os segmentos (start/end/text/words) e imprime um resumo.
"""
import json
import subprocess
import sys
import time

import numpy as np
from faster_whisper import WhisperModel


def load_audio(path):
    # decodifica com o ffmpeg do sistema (o PyAV instalado é incompatível)
    raw = subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
        capture_output=True, check=True,
    ).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

audio = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else audio.rsplit(".", 1)[0] + "_transcricao.json"
model_name = sys.argv[3] if len(sys.argv) > 3 else "large-v3-turbo"

t0 = time.time()
model = WhisperModel(model_name, device="cpu", compute_type="int8")
segments, info = model.transcribe(load_audio(audio), language="pt", word_timestamps=True, vad_filter=True)

data = []
for s in segments:
    data.append({
        "start": round(s.start, 2),
        "end": round(s.end, 2),
        "text": s.text.strip(),
        "words": [{"w": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)} for w in s.words],
    })
    print(f"[{s.start:7.2f} -> {s.end:7.2f}] {s.text.strip()}", flush=True)

with open(out, "w", encoding="utf-8") as f:
    json.dump({"audio": audio, "duration": info.duration, "segments": data}, f, ensure_ascii=False, indent=1)

print(f"\n{len(data)} segmentos, {info.duration:.0f}s de áudio, {time.time() - t0:.0f}s de processamento -> {out}")
