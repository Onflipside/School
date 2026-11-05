# Builds the 15 iLaw unit Survival Guides (+ hub) into /home/claude/School/ilaw-guide/
import json, re, html, sys, os
sys.path.insert(0, '/home/claude/School/ilaw')
from master_toc import UNITS, OFFSET
from sg_pages import MAP, V
from build_teacher import qs, fmt   # reuses parsed SG key + formatter
OUT = '/home/claude/School/ilaw-guide'; os.makedirs(OUT, exist_ok=True)
tpl = open('/home/claude/School/ilaw/unit_template.html').read()
NUM = ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','TWELVE','THIRTEEN','FOURTEEN','FIFTEEN']
starts = [ss[0][2] - OFFSET for _, ss in UNITS]; starts[0] = 8
units = []
for i, (ut, ss) in enumerate(UNITS):
    s = starts[i]; e = starts[i+1] - 1 if i + 1 < len(UNITS) else 144
    title = re.sub(r'^[A-Z]+\s*\|\s*', '', ut).strip()
    units.append(dict(n=i+1, code=NUM[i], title=title, s=s, e=e, ss=ss, file='unit-%02d.html' % (i+1)))

def opts(cur):
    o = ['<option value="index.html">All 15 Units</option>']
    for u in units:
        o.append('<option value="%s"%s>Unit %s | %s</option>' % (u['file'], ' selected' if u is cur else '', u['code'], html.escape(u['title'])))
    return ''.join(o)

for i, u in enumerate(units):
    s, e = u['s'], u['e']
    pages = []
    for p in range(s, e + 1):
        pages.append('%03d' % p)
        if p == 35: pages.append('035b')
    uq = [q for q in qs if s <= int(MAP[q['n']]) <= e]
    sg = []; last = None
    for q in uq:
        if q['sec'] != last:
            sg.append('<div class="sghead">%s</div>' % fmt(q['sec'])); last = q['sec']
        pn = int(MAP[q['n']])
        flag = '<span class="vflag" title="Interpretation of delivered content — vocabulary">VOCAB</span>' if q['n'] in V else ''
        sg.append('<div class="qa" id="q%d" data-pg="%d"><div class="qbox" onclick="openQ(%d)"><span class="qn">%d</span><span class="qt">%s</span>%s<a class="pg" href="#q%d" onclick="event.stopPropagation();go(%d);mark(%d)">p.%d</a></div><div class="ans">%s</div></div>'
                  % (q['n'], pn, q['n'], q['n'], fmt(q['q']), flag, q['n'], pn, q['n'], pn, ''.join('<p>%s</p>' % fmt(a) for a in q['a'])))
    if not uq:
        sg.append('<div class="empty">This unit\'s keywords are covered in the checklist and locator below. Its Survival Guide questions live in the units they answer.</div>')
    ck = ['<div class="ckunit">Unit %s | %s</div>' % (u['code'], html.escape(u['title']))]; nck = 0; loc = {}
    for code, t, tp, items in u['ss']:
        pg = tp - OFFSET
        rows = [(t, pg, True)] + [(it, ip - OFFSET, False) for it, ip in items]
        for tt, p, big in rows:
            if not (s <= p <= e): continue
            ck.append('<div class="ckrow%s" data-pg="%d"><span class="ck">&#10003;</span><span class="ckt">%s</span><a class="pg" onclick="event.stopPropagation();hit(%d)">p.%d</a></div>' % (' big' if big else '', p, html.escape(tt), p, p)); nck += 1
            key = re.sub(r'^[\w.]+\s*\|\s*', '', tt) if big else re.sub(r'^\[\s*\w+\s*\]\s*', '', tt)
            loc.setdefault(key.strip(' .–-'), set()).add(p)
    lh = ''.join('<div class="lrow"><span>%s</span><span class="lp">%s</span></div>' % (html.escape(k), ''.join('<a onclick="hit(%d)">%d</a>' % (p, p) for p in sorted(v)))
                 for k, v in sorted(loc.items(), key=lambda x: x[0].lower()))
    prev = '<a href="%s">&larr; Unit %s</a>' % (units[i-1]['file'], units[i-1]['code']) if i else '<a href="index.html">&larr; All Units</a>'
    nxt = '<a href="%s">Unit %s &rarr;</a>' % (units[i+1]['file'], units[i+1]['code']) if i + 1 < len(units) else '<a href="index.html">All Units &rarr;</a>'
    unav = prev + '<span></span>' + nxt
    nv = sum(1 for q in uq if q['n'] in V)
    pg_html = (tpl.replace('%%TITLE%%', 'iLaw Unit %s | %s' % (u['code'], html.escape(u['title'])))
               .replace('%%DESC%%', 'iLaw Book ONE, Unit %s: %s. Survival Guide questions, checklist and locator. The Insurance School.' % (u['code'], html.escape(u['title'])))
               .replace('%%UNAME%%', 'Unit %s | %s' % (u['code'], html.escape(u['title'])))
               .replace('%%UNITS%%', opts(u)).replace('%%UNAV%%', unav)
               .replace('%%PAGES%%', json.dumps(pages)).replace('%%SG%%', '\n'.join(sg))
               .replace('%%NQ%%', str(len(uq))).replace('%%NV%%', str(nv))
               .replace('%%CHECK%%', '\n'.join(ck)).replace('%%NCK%%', str(nck))
               .replace('%%LOC%%', lh).replace('%%NLOC%%', str(len(loc))))
    open(os.path.join(OUT, u['file']), 'w').write(pg_html)
    u['nq'], u['nck'] = len(uq), nck
    print(u['file'], s, e, len(uq), nck, len(loc))

# hub
cards = ''.join('<a class="u" href="%s"><img src="https://www.theinsuranceschool.com/pages/page-%03d.png" alt="" loading="lazy"><div class="m"><small>UNIT %s · PAGES %d–%d</small><b>%s</b><span>%d Survival Guide questions · %d keywords</span></div></a>'
                % (u['file'], u['s'], u['code'], u['s'], u['e'], html.escape(u['title']), u['nq'], u['nck']) for u in units)
hub = '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>iLaw | Book ONE Survival Guide</title><meta name="description" content="iLaw Book ONE — Florida Insurance Laws & Professional Ethics. 15 unit Survival Guides with checklist and locator. The Insurance School.">
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@600;800&family=Lato:wght@400;700;900&display=swap" rel="stylesheet">
<style>:root{--navy:#1B2A44;--cream:#FAF6EC;--gold:#C99B2D;--pill:#F0C24B;--green:#3E9E4F}*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--cream);color:var(--navy);font-family:Lato,sans-serif}
header{background:var(--navy);color:#fff;padding:34px 22px;text-align:center}header h1{font-family:Bitter;font-weight:800;font-size:clamp(28px,5vw,44px)}header h1 b{color:var(--gold)}
header p{color:#D9D2BE;margin-top:8px;font-family:Bitter;font-style:italic;font-size:18px}
.grid{max-width:1200px;margin:30px auto;padding:0 18px;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}
.u{display:block;text-decoration:none;color:inherit;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 6px 18px rgba(24,40,83,.1);border-top:5px solid var(--gold);transition:transform .15s}
.u:hover{transform:translateY(-3px)}.u img{width:100%;aspect-ratio:4/3;object-fit:cover;object-position:top;background:#EFE7D2;display:block}
.m{padding:14px 16px}.m small{font-weight:900;font-size:11px;letter-spacing:2px;color:var(--green)}.m b{display:block;font-family:Bitter;font-size:18px;margin:4px 0}.m span{font-size:13px;color:#5a6680}
footer{text-align:center;padding:24px;font-size:13px;color:#7c8598}</style></head><body>
<header><h1><b>iLAW</b> | Book ONE Survival Guide</h1><p>Florida Insurance Laws &amp; Professional Ethics · 15 Units</p></header>
<div class="grid">''' + cards + '''</div><footer>The Insurance School · Florida's oldest &amp; largest private DFS-authorized insurance education provider</footer></body></html>'''
open(os.path.join(OUT, 'index.html'), 'w').write(hub)
print('hub ok')
