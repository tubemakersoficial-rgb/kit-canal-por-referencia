# baixa por job id tentando timestamps próximos: python dlp.py <tipo> <dir> <ext> idx=HHMMSS ...
import json, sys, os, subprocess
kind, d, ext = sys.argv[1:4]; jobs = json.load(open('jobs.json'))[kind]
# HF_URL_BASE = começo das URLs de resultado do Higgsfield da sua conta, até a data (copie de um result_url): https://.../user_XXXX/hf_AAAAMMDD_
B=os.environ['HF_URL_BASE']
os.makedirs(d, exist_ok=True)
for p in sys.argv[4:]:
    i, ts = p.split('='); f = os.path.join(d, '%03d.%s' % (int(i), ext))
    if os.path.exists(f) and os.path.getsize(f) > 0: continue
    base = int(ts[0:2])*3600+int(ts[2:4])*60+int(ts[4:6]); ok=False
    for dl in sorted(range(-20,21), key=abs):
        t=base+dl; s='%02d%02d%02d'%(t//3600,t//60%60,t%60)
        if subprocess.run(['curl','-sfL','%s%s_%s.%s'%(B,s,jobs[i],ext),'-o',f]).returncode==0: ok=True; break
    if not ok: print('FALHOU', i)
print(len(os.listdir(d)), 'em', d)
