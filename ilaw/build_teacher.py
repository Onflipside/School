# Builds iLaw Book ONE — TEACHER edition: all 145 pages + all 176 SG key questions + checklist + locator.
# Pages load from https://www.theinsuranceschool.com/pages/ (open the file in a browser).
import json, re, html, sys
sys.path.insert(0, '/home/claude/School/ilaw')
from master_toc import UNITS, OFFSET

qs = json.load(open('/tmp/claude-0/sg/sg.json'))
def clean_sec(s):
    s = re.sub(r'\s*p\. \d+\]\)', '', s or '')
    return s.strip(' –-')
for q in qs:
    q['sec'] = clean_sec(q['sec'])
    a = [re.sub(r'^\d+\.\s+', '', x) for x in q['a']]
    cut = [i for i, x in enumerate(a) if x.startswith('Statutes Rules & Regulations Pertinent')]
    if cut: a = a[:cut[0]]
    q['a'] = a

def fmt(t):
    t = html.escape(t)
    t = re.sub(r'(\*?DFS\.[A-Z0-9a-z().]+(?:,\s*\[\([\d.]+\)\s*p\.\s*\d+\])?|_?\(\*?\[\([\d.]+\)\s*p\.\s*\d+\]\)_?)', r'<span class="code">\1</span>', t)
    t = re.sub(r'(\[\s*(?:Identify|Define|Note|Contrast|Explain|Compare|iFLASH4u|iFlash4u|Discuss|Illustration)\s*\])', r'<span class="tag">\1</span>', t, flags=re.I)
    return t

# ---------- pages
pages = []
for p in range(1, 145):
    pages.append('%03d' % p)
    if p == 35: pages.append('035b')
# unit start pages for the jump menu
unit_starts = [('Table of Contents', '001')]
for ut, ss in UNITS:
    unit_starts.append((ut, '%03d' % (ss[0][2] - OFFSET)))
unit_starts[1] = (unit_starts[1][0], '008')

# ---------- checklist (TOC entries, by unit) and locator
check = []
loc = {}
for ut, ss in UNITS:
    rows = []
    for code, title, tp, items in ss:
        pg = tp - OFFSET
        rows.append((title, pg, True))
        for it, ip in items:
            rows.append((it, ip - OFFSET, False))
            key = re.sub(r'^\[\s*\w+\s*\]\s*', '', it).strip(' .')
            loc.setdefault(key, set()).add(ip - OFFSET)
        loc.setdefault(re.sub(r'^[\w.]+\s*\|\s*', '', title).strip(' .–-'), set()).add(pg)
    check.append((ut, rows))

sg_html = []
last = None
for q in qs:
    if q['sec'] != last:
        sg_html.append('<div class="sghead">%s</div>' % fmt(q['sec'])); last = q['sec']
    sg_html.append('<div class="qa"><div class="qbox" onclick="this.parentNode.classList.toggle(\'open\')"><span class="qn">%d</span><span class="qt">%s</span></div><div class="ans">%s</div></div>'
                   % (q['n'], fmt(q['q']), ''.join('<p>%s</p>' % fmt(a) for a in q['a'])))

ck_html = []
for ut, rows in check:
    ck_html.append('<div class="ckunit">%s</div>' % html.escape(ut))
    for t, pg, big in rows:
        ck_html.append('<div class="ckrow%s" data-pg="%d"><span class="ck">&#10003;</span><span class="ckt">%s</span><a class="pg" onclick="event.stopPropagation();go(%d)">p.%d</a></div>'
                       % (' big' if big else '', pg, html.escape(t), pg, pg))

loc_html = ''.join('<div class="lrow"><span>%s</span><span class="lp">%s</span></div>' %
                   (html.escape(k), ''.join('<a onclick="go(%d)">%d</a>' % (p, p) for p in sorted(v)))
                   for k, v in sorted(loc.items(), key=lambda x: x[0].lower()))

opts = ''.join('<option value="%s">%s</option>' % (p, html.escape(t)) for t, p in unit_starts)

page = open('/home/claude/School/ilaw/teacher_template.html').read()
page = (page.replace('%%PAGES%%', json.dumps(pages)).replace('%%UNITS%%', opts)
        .replace('%%SG%%', '\n'.join(sg_html)).replace('%%NQ%%', str(len(qs)))
        .replace('%%CHECK%%', '\n'.join(ck_html)).replace('%%NCK%%', str(sum(len(r) for _, r in check)))
        .replace('%%LOC%%', loc_html).replace('%%NLOC%%', str(len(loc))))
open('/home/claude/School/ilaw-teacher-book1.html', 'w').write(page)
print('ok', len(pages), 'pages', len(qs), 'questions', sum(len(r) for _, r in check), 'checklist', len(loc), 'locator', len(page))
