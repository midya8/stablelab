"""Optional external clingo comparison for every fact input in bounded fixtures."""
import itertools,json,random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import clingo
from stablelab.uniform import analyze_uniform
from stablelab.uniform_oracle import verify_uniform

def solve(atoms,rules):
 text='\n'.join((r['head'] or '')+' :- '+', '.join(r['positive']+['not '+a for a in r['negative']])+'.' if r['positive'] or r['negative'] else (r['head']+'.' if r['head'] else ':-.') for r in rules);c=clingo.Control(['0','--warn=none']);c.add('base',[],text);c.ground([('base',[])])
 with c.solve(yield_=True) as h:return sorted(sum(1<<atoms.index(str(a)) for a in m.symbols(atoms=True)) for m in h)
root=Path(__file__).resolve().parents[1];requests=[c['request'] for c in json.loads((root/'docs/uniform-controls.json').read_text())];aa=['p','q'];bodies=[[],['p'],['q'],aa];rr=[dict(id='rule',head=h,positive=p,negative=n) for h in [None]+aa for p in bodies for n in bodies];ps=[[]]+[[r] for r in rr];requests.extend(dict(atoms=aa,left=l,right=r) for l in ps for r in ps);rng=random.Random(312)
for _ in range(100):
 aa=['a','b','c']
 def rules():return [dict(id='r'+str(j),head=rng.choice([None]+aa),positive=[a for a in aa if rng.random()<.3],negative=[a for a in aa if rng.random()<.3]) for j in range(rng.randrange(6))]
 requests.append(dict(atoms=aa,left=rules(),right=rules()))
count=0;inputs=0;mins=set()
for q in requests:
 r=analyze_uniform(q);verify_uniform(r)
 if r['minimum_fact_witness']:mins.add(r['minimum_fact_witness']['fact_count'])
 for f in r['fact_contexts']:
  for s in ('left','right'):
   assert solve(q['atoms'],q[s]+f['context'])==f[s]['stable_masks'];count+=1
  inputs+=1
print(json.dumps(dict(reference='clingo',version=clingo.__version__,comparisons=len(requests),fact_contexts=inputs,augmented_families=count,minimum_fact_counts=sorted(mins))))
