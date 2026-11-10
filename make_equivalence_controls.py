import json
from stablelab.equivalence import compare

def r(id,h,p=(),n=()):return {'id':id,'head':h,'positive':sorted(p),'negative':sorted(n)}
controls=[]
def add(name,description,atoms,left,right):
    req={'atoms':atoms,'left':left,'right':right};rep=compare(req);controls.append({'name':name,'description':description,'request':req,'expected':{'pairs':len(rep['pairs']),'classically_equivalent':rep['classically_equivalent'],'ordinarily_equivalent':rep['ordinarily_equivalent'],'strongly_equivalent':rep['strongly_equivalent'],'left_stable_masks':rep['families']['left']['stable_masks'],'right_stable_masks':rep['families']['right']['stable_masks'],'difference_pairs':len(rep['difference_pair_ids']),'context_kind':rep['witness']['kind'] if rep['witness'] else None}})
add('Same answers, different module','Fact p versus p unless q. Adding fact q breaks the apparent tie.',['p','q'],[r('fact','p')],[r('default','p',n=['q'])])
add('Classical agreement is still too weak','A positive cycle and two default constraints have identical classical and stable models. Their reducts disagree at proper SE pairs; a positive cycle context exposes it.',['p','q'],[r('forward','p',['q']),r('back','q',['p'])],[r('selfp','p',['p']),r('selfq','q',['q']),r('require',None,['p'],['q']),r('require2',None,['q'],['p'])])
add('Same models, different reducts','A default constraint forbids q without p. It is classically equivalent to p from q, but an SE pair separates them.',['p','q'],[r('imply','p',['q'])],[r('constraint',None,['q'],['p'])])
add('Positive cycle versus silence','Both have just the empty stable model. Facts can activate the positive cycle.',['p','q'],[r('pq','p',['q']),r('qp','q',['p'])],[])
add('Redundant transitive edge','Adding p from r to a two-edge chain is safe under every normal context over this vocabulary.',['p','q','r'],[r('pq','p',['q']),r('qr','q',['r'])],[r('pq','p',['q']),r('qr','q',['r']),r('pr','p',['r'])])
add('Tautology and duplicate rule','Rule IDs do not give rules new semantics. Positive self implication and a duplicate fact preserve strong equivalence.',['p','q'],[r('p','p')],[r('other','p'),r('duplicate','p'),r('tautology','q',['q'])])
add('Two inconsistent modules','An empty constraint and an odd default loop both have no stable models, but only one forbids every context.',['p'],[r('block',None)],[r('odd','p',n=['p'])])
add('Every context still inconsistent','Two differently written universally inconsistent programs have empty SE sets.',['p'],[r('block',None)],[r('p','p'),r('forbid',None,['p'])])
add('Empty vocabulary','There is one SE pair, not zero. Empty program and empty constraint disagree there.',[],[],[r('block',None)])
add('Five-atom complete pair atlas','243 SE interpretations, including all diagonal and proper pairs. Independent even default choices have the same base stable models, but a constraint is not a rule.',['a','b','c','d','e'],[r('ab','a',n=['b']),r('ba','b',n=['a']),r('cd','c',n=['d']),r('dc','d',n=['c']),r('e','e',['a'])],[r('ab','a',n=['b']),r('ba','b',n=['a']),r('cd','c',n=['d']),r('dc','d',n=['c']),r('e','e',['a']),r('safe',None,['e'],['a'])])
add('A real cycle gadget','Facts p and q versus constraints requiring both. The first proper pair differs at X empty and Y full; the separating context is the two-edge positive cycle.',['p','q'],[r('p','p'),r('q','q')],[r('needp',None,n=['p']),r('needq',None,n=['q'])])
open('docs/equivalence-controls.json','w').write(json.dumps(controls,indent=2)+'\n')
if __name__=='__main__':print(json.dumps([{ 'name':c['name'],**c['expected']} for c in controls],indent=2))
