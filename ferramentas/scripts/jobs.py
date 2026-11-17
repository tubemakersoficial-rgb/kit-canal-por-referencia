import json, sys, os
# uso: python jobs.py <tipo> <idx:job_id> ...
kind = sys.argv[1]; f = 'jobs.json'
d = json.load(open(f)) if os.path.exists(f) else {}
d.setdefault(kind, {})
for p in sys.argv[2:]:
    i, j = p.split(':', 1); d[kind][i] = j
json.dump(d, open(f, 'w'), indent=1)
print(kind, len(d[kind]))
