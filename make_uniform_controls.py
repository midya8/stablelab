import json
from stablelab.uniform import analyze_uniform

def r(id,h,p=(),n=()):return dict(id=id,head=h,positive=sorted(p),negative=sorted(n))
controls=[]
def add(name,description,atoms,left,right):
    request=dict(atoms=atoms,left=left,right=right);report=analyze_uniform(request);controls.append({'name':name,'description':description,'request':request,'expected':{'ordinary':report['comparison']['ordinarily_equivalent'],'uniform':report['uniformly_equivalent'],'strong':report['comparison']['strongly_equivalent'],'fact_contexts':len(report['fact_contexts']),'minimum_fact_count':report['minimum_fact_witness']['fact_count'] if report['minimum_fact_witness'] else None}})
add('Facts agree, rules break the tie','Eiter/Fink 2003 Example2: a follows either b or not b, versus either c or not c. All eight fact contexts agree, but b from a separates.',['a','b','c'],[r('unlessb','a',n=['b']),r('fromb','a',['b'])],[r('unlessc','a',n=['c']),r('fromc','a',['c'])])
add('One fact is enough','Both base programs return p. Adding q separates a fact from a default.',['p','q'],[r('fact','p')],[r('default','p',n=['q'])])
add('Two facts are necessary','The left program derives p when q is absent or r is absent. Only facts q and r together expose the difference from fact p.',['p','q','r'],[r('unlessq','p',n=['q']),r('unlessr','p',n=['r'])],[r('fact','p')])
add('Three facts are necessary','All smaller fact contexts agree. The complete table proves minimum cardinality three, not just subset minimality.',['a','b','c','p'],[r('unlessa','p',n=['a']),r('unlessb','p',n=['b']),r('unlessc','p',n=['c'])],[r('fact','p')])
add('Already different without input','The empty context counts. A minimum separator can contain zero facts.',['p'],[r('fact','p')],[])
add('Safe transitive edge','Strong equivalence implies uniform equivalence. Every fact context agrees.',['p','q','r'],[r('pq','p',['q']),r('qr','q',['r'])],[r('pq','p',['q']),r('qr','q',['r']),r('pr','p',['r'])])
add('Constraint versus derivation','Equal base and classical models can still disagree on fact inputs.',['p','q'],[r('imply','p',['q'])],[r('constraint',None,['q'],['p'])])
add('Inconsistent until a fact arrives','An odd default loop and empty constraint both start without stable models. A fact repairs only the odd loop.',['p'],[r('odd','p',n=['p'])],[r('block',None)])
add('Empty vocabulary','One fact context and one SE pair still exist. Empty program and empty constraint differ.',[],[],[r('block',None)])
add('Five-atom complete input table','32 fact contexts and 243 SE pairs. Four facts are necessary to defeat all four defaults.',['a','b','c','d','p'],[r('r'+a,'p',n=[a]) for a in ['a','b','c','d']],[r('p','p')])
open('docs/uniform-controls.json','w').write(json.dumps(controls,indent=2)+'\n')
if __name__=='__main__':print(json.dumps([{'name':c['name'],**c['expected']} for c in controls],indent=2))
