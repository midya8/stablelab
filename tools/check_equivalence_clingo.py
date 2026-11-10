"""Optional external clingo check: both base and concrete-context families."""
import itertools,random,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import clingo
from stablelab.equivalence import compare
from stablelab.equivalence_oracle import verify_comparison

def solve(atoms,rules):
    text='\n'.join((r['head'] or '')+' :- '+', '.join(r['positive']+['not '+a for a in r['negative']])+'.' if r['positive'] or r['negative'] else (r['head']+'.' if r['head'] else ':-.') for r in rules)
    ctl=clingo.Control(['0','--warn=none']);ctl.add('base',[],text);ctl.ground([('base',[])])
    with ctl.solve(yield_=True) as h:return sorted(sum(1<<atoms.index(str(a)) for a in m.symbols(atoms=True)) for m in h)
cs=json.loads((Path(__file__).resolve().parents[1]/'docs/equivalence-controls.json').read_text());requests=[c['request'] for c in cs];aa=['p','q'];body=[[],['p'],['q'],aa];rr=[dict(id='r',head=h,positive=p,negative=n) for h in [None]+aa for p in body for n in body];ps=[[]]+[[r] for r in rr]
requests.extend(dict(atoms=aa,left=l,right=r) for l in ps for r in ps)
rng=random.Random(9903)
for _ in range(180):
 aa=['a','b','c']
 def rules():return [dict(id='r'+str(j),head=rng.choice([None]+aa),positive=[a for a in aa if rng.random()<.33],negative=[a for a in aa if rng.random()<.33]) for j in range(rng.randrange(7))]
 requests.append(dict(atoms=aa,left=rules(),right=rules()))
counts={'comparisons':len(requests),'base_families':0,'augmented_families':0,'facts_y':0,'facts_x_cycle':0}
for req in requests:
 r=compare(req);verify_comparison(r)
 for s in ('left','right'):
  assert solve(req['atoms'],req[s])==r['families'][s]['stable_masks'];counts['base_families']+=1
 if r['witness']:
  w=r['witness'];counts[w['kind']]+=1
  for s in ('left','right'):
   assert solve(req['atoms'],req[s]+w['context'])==w[s+'_augmented']['stable_masks'];counts['augmented_families']+=1
print(json.dumps(dict(reference='clingo',version=clingo.__version__,**counts)))
