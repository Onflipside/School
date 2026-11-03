# Generates 2-40 / 2-14 funnel pages 1 & 2 from the 2-15 template pages.
import re,sys
L={
 '2-40':dict(code='240',hrs='40',std=219,mc=348,crumb='FL 2-40 Health',course='FL 2-40 Health',
   h2='<h2>Health Insurance</h2>',
   intro='<p class="scope"><b>New Health Insurance Careers Start Here.</b></p>\n    <p class="desc"><span class="st">&#9733;</span>Florida&rsquo;s 2-40 Health Insurance license is your direct path to a NEW Insurance Career.</p>',
   drop=['Types of Life Insurance Policies','Annuities &amp; Variable Contracts']),
 '2-14':dict(code='214',hrs='30',std=179,mc=308,crumb='FL 2-14 Life &amp; Annuities',course='FL 2-14 Life & Annuities',
   h2='<h2>Life &amp; Annuities</h2><div class="sub sub2"><span class="inc-w">Includes</span> Variable Contracts</div>',
   intro='<p class="scope"><b>New Life Insurance Careers Start Here.</b></p>\n    <p class="desc"><span class="st">&#9733;</span>Florida&rsquo;s 2-14 Life Insurance license, which includes Annuities and Variable Contracts, is your shortest path to a NEW Insurance Career.</p>',
   drop=['Types of Health Insurance Policies']),
}
H2_15='<h2>Health &amp; Life Insurance</h2><div class="sub sub2"><span class="inc-w">Includes</span> Annuities &amp; Variable Contracts</div>'
def must(s,a,b,n=None):
    c=s.count(a)
    if c==0: sys.exit('MISSING: '+a[:80])
    if n is not None and c!=n: sys.exit(f'COUNT {c}!={n}: '+a[:80])
    return s.replace(a,b)
for k,d in L.items():
    # ---- page 1
    s=open('2-15.html').read()
    s=must(s,'Florida 2-15 Health &amp; Life — ',f'Florida {k} {d["crumb"].replace("FL "+k+" ","")} — ',1)
    s=must(s,'FLASH4u 2-15 <span class="pipe">|</span> <span class="hrs">60-Hours',f'FLASH4u {k} <span class="pipe">|</span> <span class="hrs">{d["hrs"]}-Hours',1)
    s=must(s,H2_15,d['h2'])
    s=must(s,'<span class="price">$289</span>',f'<span class="price">${d["std"]}</span>',1)
    s,n=re.subn(r'<p class="desc"><span class="st">&#9733;</span>Florida&rsquo;s 2-15 license is your best choice.*?</p>\s*<p class="desc">Lastly,.*?</p>',d['intro'],s,flags=re.S)
    assert n==1
    for it in d['drop']: s=must(s,f'      <li>{it}</li>\n','',1)
    s=must(s,'value="FL 2-15 Health & Life"',f'value="{d["course"]}"',1)
    s=must(s,'Save My Seat &mdash; 2-15',f'Save My Seat &mdash; {k}',1)
    s=must(s,'2-15-enhance.html',f'{k}-enhance.html')
    s=s.replace('fl-215-',f'fl-{d["code"]}-')
    open(f'{k}.html','w').write(s)
    # ---- page 2
    s=open('2-15-enhance.html').read()
    s=must(s,'<title>Florida 2-15 Health &amp; Life |',f'<title>Florida {k} {d["crumb"].replace("FL "+k+" ","")} |',1)
    s=must(s,'href="2-15.html',f'href="{k}.html')
    s=must(s,'&larr; FL 2-15 Health &amp; Life',f'&larr; {d["crumb"]}',1)
    s=must(s,'FLORIDA 2-15 60-Hour Pre-Licensing Course',f'FLORIDA {k} {d["hrs"]}-Hour Pre-Licensing Course',1)
    s=must(s,H2_15,d['h2'])
    s=must(s,'<span class="price">$289</span>',f'<span class="price">${d["std"]}</span>')
    s=must(s,'<i>60 Hour Self-Study Course</i>',f'<i>{d["hrs"]} Hour Self-Study Course</i>',1)
    s=must(s,'<span class="ppr">$289</span>',f'<span class="ppr">${d["std"]}</span>',1)
    s=must(s,'id="ptamt">$289<',f'id="ptamt">${d["std"]}<',1)
    s=must(s,"'$418':'$289'",f"'${d['mc']}':'${d['std']}'")
    s=must(s,'2-15-cram.html',f'{k}-cram.html')
    s=s.replace('fl-215-',f'fl-{d["code"]}-')
    open(f'{k}-enhance.html','w').write(s)
print('ok')
