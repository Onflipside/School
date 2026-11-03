import re,sys
SRC='/home/claude/School/2-15-cram.html'
LINES={
 '2-40':dict(hrs='40',course='Health Insurance',std=219,mc=348,tot=499,cram=379,
   links=('https://buy.stripe.com/28EcN72Szf4B1v13Wa8EM0x','https://buy.stripe.com/9B64gB78P8Gd6PleAO8EM0y','https://buy.stripe.com/6oUaEZdxd9Kha1xcsG8EM0z')),
 '2-14':dict(hrs='30',course='Life &amp; Annuities',std=179,mc=308,tot=459,cram=379,
   links=('https://buy.stripe.com/dRm5kFal14pXflRdwK8EM0A','https://buy.stripe.com/9B63cxbp5g8F7Tpaky8EM0B','https://buy.stripe.com/eVq9AVeBhe0x7TpfES8EM0C')),
}
def build(code,d):
    s=open(SRC).read()
    def rep(a,b,n=1):
        nonlocal s
        c=s.count(a)
        assert c==n,(code,a[:60],c)
        s=s.replace(a,b)
    val=d['std']+129+d['cram'];save=val-d['tot']
    i=s.index('var STRIPE_LINKS={');j=s.index('};',i)+2
    key=code.replace('-','')
    s=s[:i]+("var STRIPE_LINKS={\n    'fl-215-standard':'%s',    /* %s Standard $%d */\n    'fl-215-masterclass':'%s', /* %s Masterclass $%d */\n    'fl-215-cram8':'%s'  /* %s Orientation + 3-Day Cram bundle $%d */\n  };"%(d['links'][0],code,d['std'],d['links'][1],code,d['mc'],d['links'][2],code,d['tot']))+s[j:]
    rep('<title>FL 2-15 State Exam CRAM','<title>FL %s State Exam CRAM'%code)
    rep('href="2-15.html#dayone"','href="%s.html#dayone"'%code)
    rep('href="2-15-enhance.html"','href="%s-enhance.html"'%code)
    rep('FLORIDA 2-15 60-Hour Pre-Licensing Course','FLORIDA %s %s-Hour Pre-Licensing Course'%(code,d['hrs']))
    rep('absorbing 60-Hours of keywords','absorbing %s-Hours of keywords'%d['hrs'])
    rep('<div class="tt"><h2>Health &amp; Life Insurance</h2>','<div class="tt"><h2>%s</h2>'%d['course'])
    s=s.replace('FLORIDA | 2-15 ','FLORIDA | %s '%code)
    # prices
    rep('<span class="price" id="cartprice">$289</span>','<span class="price" id="cartprice">$%d</span>'%d['std'])
    rep('<span class="ppr" id="paybase">$289</span>','<span class="ppr" id="paybase">$%d</span>'%d['std'])
    rep('<span class="o3p" id="selfp">$289</span>','<span class="o3p" id="selfp">$%d</span>'%d['std'])
    s=s.replace("textContent='$418'","textContent='$%d'"%d['mc'])
    rep("el===ol?'$589':(mc?'$418':'$289')","el===ol?'$%d':(mc?'$%d':'$%d')"%(d['tot'],d['mc'],d['std']))
    rep('base=mc?418:289','base=mc?%d:%d'%(d['mc'],d['std']))
    rep('var TOT={none:0,c3:569,c4:589,both:589}','var TOT={none:0,c3:%d,c4:%d,both:%d}'%(d['tot'],d['tot'],d['tot']))
    rep('<span class="amtnum" id="ptamt">$589</span>','<span class="amtnum" id="ptamt">$%d</span>'%d['tot'])
    rep("$('a4').innerHTML=b?'$579<small>","$('a4').innerHTML=b?'$%d<small>"%d['cram'])
    rep('<span>Total Value</span><span>$997</span>','<span>Total Value</span><span>$%s</span>'%format(val,','))
    rep('<span>Save Today</span><span>&minus; $408</span>','<span>Save Today</span><span>&minus; $%d</span>'%save)
    rep('+ $300</span>','+ $%d</span>'%(d['tot']-d['std']))
    # names
    rep('<span class="o3l">8-Day LIVE Instructor Bundle</span><span class="o3p">$589</span>','<span class="o3l">Orientation + 3-Day Cram Bundle</span><span class="o3p">$%d</span>'%d['tot'])
    rep('Half Off 8-Day LIVE Instructor Bundle<span class="sv2">','Orientation + 3-Day State Exam Cram<span class="sv2">')
    rep('</span></b></span> LIVE Instructor Bundle<small class="p8d">8 DAYS</small>','</span></b></span> State Exam Cram<small class="p8d">ORIENTATION + 3 DAYS</small>')
    rep('Back to the 8-Day LIVE Instructor Bundle &ndash; $589','Back to the Orientation + 3-Day Cram Bundle &ndash; $%d'%d['tot'])
    rep('<span class="vb">|</span>8-Day Health, Life &amp; Annuity Bundle','<span class="vb">|</span>Orientation &amp; 3-Day State Exam Cram')
    rep('<div class="c1 t">Orientation, <span style="white-space:nowrap">4-Day Seminar</span> &amp; <span','<div class="c1 t">Orientation &amp; <span')
    rep('Start FAST - Gain Momentum - Finish Strong','Start FAST - Finish Strong')
    # remove 4-day section
    rep('<div class="corerow"><span class="coretag ckc">&#10003;</span></div>','')
    css='#diy{visibility:hidden!important;height:0!important;min-height:0!important;padding:0!important;margin:0!important;border:0!important;overflow:hidden!important;box-shadow:none!important;}#wk1,section.cmpx.mc{display:none!important;}'
    rep('</head>','<style>%s</style></head>'%css)
    open('/home/claude/School/%s-cram.html'%code,'w').write(s)
    print(code,'ok',val,save)
for c,d in LINES.items(): build(c,d)
