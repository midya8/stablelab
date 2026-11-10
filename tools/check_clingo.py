"""Optional external reference check. clingo is not a runtime dependency."""
import itertools,random,json
import clingo
from stablelab.core import analyze
from make_controls import controls,rule

def asp(p):
    return '\n'.join((r['head'] or '')+' :- '+', '.join(r['positive']+['not '+a for a in r['negative']])+'.' if r['positive'] or r['negative'] else (r['head']+'.' if r['head'] else ':-.') for r in p['rules'])
def check(p):
    ctl=clingo.Control(['0','--warn=none']);ctl.add('base',[],asp(p));ctl.ground([('base',[])])
    actual=[]
    with ctl.solve(yield_=True) as handle:
        for m in handle:actual.append(sum(1<<p['atoms'].index(str(a)) for a in m.symbols(atoms=True)))
    assert sorted(actual)==analyze(p)['stable_masks'],(p,actual)
ps=[c['program'] for c in controls];rr=[]
for head in [None,'p','q']:
 for states in itertools.product(range(4),repeat=2):rr.append(rule('r'+str(len(rr)),head,[a for a,s in zip(['p','q'],states) if s&1],[a for a,s in zip(['p','q'],states) if s&2]))
for k in range(3):ps.extend(dict(atoms=['p','q'],rules=list(rs)) for rs in itertools.combinations(rr,k))
rng=random.Random(731)
for _ in range(200):ps.append(dict(atoms=['a','b','c'],rules=[rule('r'+str(i),rng.choice([None,'a','b','c']),[a for a in ['a','b','c'] if rng.random()<.35],[a for a in ['a','b','c'] if rng.random()<.35]) for i in range(rng.randrange(10))]))
for p in ps:check(p)
print(json.dumps({'reference':'clingo','version':clingo.__version__,'programs':len(ps),'controls':len(controls),'two_atom_programs':1177,'seeded_three_atom_programs':200}))
