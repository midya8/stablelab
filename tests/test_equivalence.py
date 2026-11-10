import copy,itertools,json,random,unittest
from pathlib import Path
from stablelab.equivalence import compare
from stablelab.equivalence_oracle import verify_comparison
from stablelab.comparison_model import parse_comparison
ROOT=Path(__file__).resolve().parents[1]
class EquivalenceTests(unittest.TestCase):
 def test_controls(self):
  for c in json.loads((ROOT/'docs/equivalence-controls.json').read_text()):
   r=compare(c['request']);verify_comparison(r)
   for key in ['classically_equivalent','ordinarily_equivalent','strongly_equivalent']:self.assertEqual(r[key],c['expected'][key],c['name'])
 def test_all_single_rule_pairs(self):
  atoms=['p','q'];bodies=[[],['p'],['q'],atoms];rules=[{'id':'rule','head':h,'positive':p,'negative':n} for h in [None]+atoms for p in bodies for n in bodies];programs=[[]]+[[r] for r in rules]
  for left in programs:
   for right in programs:verify_comparison(compare({'atoms':atoms,'left':left,'right':right}))
 def test_seeded_pairs(self):
  rng=random.Random(9903);aa=['a','b','c'];seen=set()
  for i in range(180):
   def rules():return [dict(id='r'+str(j),head=rng.choice([None]+aa),positive=[a for a in aa if rng.random()<.33],negative=[a for a in aa if rng.random()<.33]) for j in range(rng.randrange(7))]
   rep=compare(dict(atoms=aa,left=rules(),right=rules()));verify_comparison(rep)
   if rep['witness']:seen.add(rep['witness']['kind'])
  self.assertEqual(seen,{'facts_y','facts_x_cycle'})
 def test_every_field_forgery(self):
  rep=compare(dict(atoms=['p','q'],left=[dict(id='imply',head='p',positive=['q'],negative=[])],right=[dict(id='con',head=None,positive=['q'],negative=['p'])]));verify_comparison(rep)
  paths=[]
  def walk(v,path):
   if isinstance(v,dict):
    for k,z in v.items():walk(z,path+[k])
   elif isinstance(v,list):
    for i,z in enumerate(v):walk(z,path+[i])
    if not v:paths.append((path,['_forged']))
   elif isinstance(v,bool):paths.append((path,not v));paths.append((path,int(v)))
   elif isinstance(v,int):paths.append((path,v+1))
   elif v is None:paths.append((path,False))
   elif isinstance(v,str):paths.append((path,v+'_forged'))
  walk(rep,[])
  for path,val in paths:
   if path[:1]==['request']:continue
   forged=copy.deepcopy(rep);p=forged
   for key in path[:-1]:p=p[key]
   p[path[-1]]=val
   with self.assertRaises((ValueError,TypeError,KeyError,AssertionError)):verify_comparison(forged)
  self.assertGreater(len(paths),400)
 def test_parser_limits(self):
  for data in [dict(atoms=['a','b','c','d','e','f'],left=[],right=[]),dict(atoms=[],left=[],right=[],extra=1),dict(atoms=['p'],left=[dict(id='r'+str(i),head='p',positive=[],negative=[]) for i in range(25)],right=[])]:
   with self.assertRaises(ValueError):parse_comparison(data)
 def test_context_ids_collisions(self):
  r=compare(dict(atoms=['p','q'],left=[dict(id='ctx0',head='p',positive=[],negative=[])],right=[dict(id='ctx1',head='p',positive=[],negative=['q'])]));verify_comparison(r);self.assertEqual(r['witness']['context'][0]['id'],'ctx2')
 def test_empty_and_five_atom_bounds(self):
  for aa,count in [([],1),(['a','b','c','d','e'],243)]:
   r=compare(dict(atoms=aa,left=[],right=[]));verify_comparison(r);self.assertEqual(len(r['pairs']),count);self.assertTrue(r['strongly_equivalent'])
if __name__=='__main__':unittest.main()
