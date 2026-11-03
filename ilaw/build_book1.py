# Builds ilaw-book1.html (iLaw Book ONE web page) from the isg1.html layout.
# Pages: ilaw/book1/p<N>.png (N = page number circle). Content: ilaw/book1/content.py
import re, io, base64, glob, os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.abspath(__file__)) + '/..'
sys.path.insert(0, ROOT + '/ilaw/book1')
from content import SURVIVAL, CHECKLIST, LOCATOR

s = open(ROOT + '/isg1.html').read()

def one(pat, rep, flags=re.S):
    global s
    s, n = re.subn(pat, lambda m: rep, s, count=1, flags=flags)
    if n != 1: sys.exit('MISSING: ' + pat[:70])

# ---- pages, in page-number order
files = sorted(glob.glob(ROOT + '/ilaw/book1/p*.png'), key=lambda f: int(re.search(r'p(\d+)\.png', f).group(1)))
pages = []
for f in files:
    n = int(re.search(r'p(\d+)\.png', f).group(1))
    im = Image.open(f).convert('RGB')
    b = io.BytesIO(); im.save(b, 'JPEG', quality=86, optimize=True)
    pages.append((n, 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()))
nums = [n for n, _ in pages]
one(r'var PAGES=\[.*?\];', 'var PAGES=[\n' + ''.join('    {n:%d,img:"%s"},\n' % p for p in pages) + '  ];')
one(r'var cur=1;', 'var cur=0;')
one(r"document.getElementById\('pcur'\).textContent=\(cur\+1\);", "document.getElementById('pcur').textContent=PAGES[cur].n;")
one(r"document.getElementById\('plast'\).textContent=PAGES.length;", "document.getElementById('plast').textContent=PAGES[PAGES.length-1].n;document.getElementById('pfirst').textContent=PAGES[0].n;")
one(r'<span class="pend">1</span>', '<span class="pend" id="pfirst">%d</span>' % nums[0])
one(r'<span class="pcur" id="pcur">1</span>', '<span class="pcur" id="pcur">%d</span>' % nums[0])
one(r'<span class="pend" id="plast">14</span>', '<span class="pend" id="plast">%d</span>' % nums[-1])

# ---- Survival Guide rail
def qa(it):
    tag = it['tag']
    pg = '<a class="pglink" href="#book" onclick="goPage(%d)">p. %d</a>' % (it['p'], it['p'])
    head = '<div class="qtag">%s%s</div>' % ((tag + ' &nbsp;') if tag else '', pg)
    body = ''.join('<p>%s</p>' % a for a in it['a'])
    return ('      <div class="qa">\n        %s\n'
            '        <div class="qblock" onclick="qaToggle(this)"><div class="qbox"><span class="qt">%s</span></div></div>\n'
            '        <div class="ans">\n'
            '          <div class="ans-toggle" onclick="qaToggle(this)"><span class="ans-mark"><span class="am-q">?</span><span class="am-c">&#10003;</span></span></div>\n'
            '          <div class="ans-body"><div class="ans-pad"><div class="arow"><span class="astar">&#10033;</span><div class="atext">%s</div></div></div></div>\n'
            '        </div>\n      </div>\n') % (head, it['q'], body)
one(r'<div class="qslide">.*?</div>\s*<div class="qgoldrow">',
    '<div class="qslide">\n' + ''.join(qa(i) for i in SURVIVAL) + '      </div>\n      <div class="qgoldrow">')
one(r'<span id="rmdone">0</span> / 16 Identified', '<span id="rmdone">0</span> / %d Identified' % len(CHECKLIST))

# ---- Checklist
def js(t): return t.replace('\\', '\\\\').replace('"', '\\"')
one(r'var ROADS=\[.*?\];', 'var ROADS=[\n' + ''.join('    {t:"%s", p:%d, done:false},\n' % (js(t), p) for p, t in CHECKLIST) + '  ];')

# ---- Index / Locator
loc = ''.join('<div class="locrow"><span class="lockw">%s</span><span class="locpg">%s</span></div>' %
              (k, ''.join('<a href="#book" onclick="goPage(%d)">%d</a>' % (p, p) for p in ps)) for k, ps in LOCATOR)
locsec = ('\n  <div class="locwrap"><div class="locator">\n'
          '    <div class="rm-title-in"><span class="i-u">i</span>LAW <span style="color:var(--gold);">|</span> Keyword Index &amp; Locator</div>\n'
          '    <div class="rm-divider"></div>\n'
          '    <div class="locgrid">' + loc + '</div>\n'
          '    <div class="rmhint">Click a page number to jump straight to it.</div>\n'
          '  </div></div>\n\n  <!-- transition question')
one(r'\n  <!-- transition question', locsec)

css = ('  .locwrap{max-width:825px;margin:46px auto 0;padding:0 20px;}\n'
       '  .locator{background:var(--dfs-blue);border-radius:14px;padding:16px 22px;color:#fff;box-shadow:0 5px 16px rgba(24,40,83,.2);}\n'
       '  .locgrid{display:grid;grid-template-columns:1fr 1fr;column-gap:30px;}\n'
       '  .locrow{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.09);font-family:\'Bitter\';font-weight:600;font-size:13.5px;}\n'
       '  .locpg{display:flex;gap:6px;flex:0 0 auto;}\n'
       '  .locpg a{min-width:30px;height:26px;padding:0 6px;border-radius:7px;background:var(--gold-pill);color:var(--navy);font-weight:800;font-size:12px;display:flex;align-items:center;justify-content:center;text-decoration:none;transition:transform .15s,background .15s;}\n'
       '  .locpg a:hover{background:var(--green-bright);color:#fff;transform:translateY(-1px);}\n'
       '  .pglink{display:inline-block;margin-left:4px;font-family:\'Lato\';font-weight:900;font-size:11px;color:var(--navy);background:var(--gold-pill);border-radius:999px;padding:1px 9px;text-decoration:none;vertical-align:middle;}\n'
       '  .pglink:hover{background:var(--green-bright);color:#fff;}\n'
       '  @media(max-width:820px){.locgrid{grid-template-columns:1fr;}}\n'
       '</style>')
one(r'</style>', css)
one(r'<div class="lcap">', '<div class="lcap" id="book">')
one(r'  render\(\);\n', "  render();\n  function goPage(n){ var i=PAGES.findIndex(function(p){return p.n===n;}); if(i>=0){ cur=i; render(); } }\n")
one(r'<head>', '<head><title>iLAW | Book ONE &mdash; Florida Insurance Law Survival Guide</title>')

open(ROOT + '/ilaw-book1.html', 'w').write(s)
print('ok', nums, len(SURVIVAL), 'questions', len(CHECKLIST), 'checklist', len(LOCATOR), 'index', round(len(s)/1e6, 2), 'MB')
