import json,html
from master_toc import UNITS,OFFSET,LAST_PAGE
secs=[]
for ui,(ut,ss) in enumerate(UNITS):
    for code,title,tp,items in ss: secs.append([ui,code,title,tp-OFFSET,[(a,b-OFFSET) for a,b in items]])
for i,s in enumerate(secs):
    nxt = secs[i+1][3] if i+1<len(secs) else LAST_PAGE+1
    last = max([nxt-1]+[p for _,p in s[4]])
    s.append(list(range(s[3],last+1)))
def pages(lst):
    out=[]
    for p in lst:
        out.append('%03d'%p)
        if p==35: out.append('035b')
    return out
def body(s):
    parts=[]
    for pg in pages(s[5]):
        n=int(pg[:3]); items=[a for a,p in s[4] if p==n]
        h=f'<p><strong>PAGE {pg.lstrip("0").upper()}</strong></p>'
        if items: h+=f'<p><strong>LOOK OUT |</strong> Keywords &amp; Concepts: {html.escape(" · ".join(items))}</p>'
        parts.append(h+f'<p>[[page-{pg}]]</p>')
    return '<hr>'.join(parts)
mods=[{"title":"START HERE | Table of Contents","lessons":[{"title":"Table of Contents","body":body([0,'TOC','Table of Contents',1,[],list(range(1,8))])}]}]
for ui,(ut,ss) in enumerate(UNITS):
    mods.append({"title":ut,"lessons":[{"title":s[2],"body":body(s)} for s in secs if s[0]==ui]})
json.dump(mods,open('/tmp/claude-0/kmods.json','w'))
allp=[p for s in secs for p in s[5]]
print('lessons',sum(len(m['lessons']) for m in mods),'pages covered',len(set(allp)|set(range(1,8))),'min',min(allp),'max',max(allp))
for s in secs: print(s[1], s[5][0], s[5][-1])
