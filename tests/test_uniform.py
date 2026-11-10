import copy,itertools,json,random,unittest
from pathlib import Path
from stablelab.uniform import analyze_uniform
from stablelab.uniform_oracle import verify_uniform
ROOT=Path(__file__).resolve().parents[1]
class UniformTests(unittest.TestCase):
 def test_controls_and_strict_hierarchy(self):
  cs=json.loads((ROOT/'docs/uniform-controls.json').read_text())
  for c in cs:
   r=analyze_uniform(c['request']);v=verify_uniform(r)
   self.assertEqual(v['uniformly_equivalent'],c['expected']['uniform']);self.assertEqual(v['minimum_fact_count'],c['expected']['minimum_fact_count']);self.assertEqual(r['comparison']['ordinarily_equivalent'],c['expected']['ordinary']);self.assertEqual(r['comparison']['strongly_equivalent'],c['expected']['strong'])
   if r['comparison']['strongly_equivalent']:self.assertTrue(r['uniformly_equivalent'])
   if r['uniformly_equivalent']:self.assertTrue(r['comparison']['ordinarily_equivalent'])
  self.assertEqual(cs[0]['expected'],dict(ordinary=True,uniform=True,strong=False,fact_contexts=8,minimum_fact_count=None))
  self.assertEqual([cs[i]['expected']['minimum_fact_count'] for i in [4,1,2,3,9]],[0,1,2,3,4])
 def test_every_two_atom_single_rule_module_pair(self):
  aa=['p','q'];bodies=[[],['p'],['q'],aa];rr=[dict(id='rule',head=h,positive=p,negative=n) for h in [None]+aa for p in bodies for n in bodies];ps=[[]]+[[r] for r in rr]
  for left in ps:
   for right in ps:verify_uniform(analyze_uniform(dict(atoms=aa,left=left,right=right)))
 def test_seeded_three_atom_pairs(self):
  rng=random.Random(312);aa=['a','b','c']
  for _ in range(100):
   def rules():return [dict(id='r'+str(j),head=rng.choice([None]+aa),positive=[a for a in aa if rng.random()<.3],negative=[a for a in aa if rng.random()<.3]) for j in range(rng.randrange(6))]
   verify_uniform(analyze_uniform(dict(atoms=aa,left=rules(),right=rules())))
 def test_all_new_evidence_leaves_and_type_forgery(self):
  c=json.loads((ROOT/'docs/uniform-controls.json').read_text())[1];report=analyze_uniform(c['request']);paths=[]
  def walk(v,path):
   if path==['comparison']:return
   if isinstance(v,dict):
    for k,z in v.items():walk(z,path+[k])
   elif isinstance(v,list):
    if not v:paths.append((path,['_forged']))
    for i,z in enumerate(v):walk(z,path+[i])
   elif isinstance(v,bool):paths.extend([(path,not v),(path,int(v))])
   elif isinstance(v,int):paths.append((path,v+1))
   elif v is None:paths.append((path,False))
   else:paths.append((path,str(v)+'_forged'))
  walk(report,[])
  for path,new in paths:
   forged=copy.deepcopy(report);obj=forged
   for k in path[:-1]:obj=obj[k]
   obj[path[-1]]=new
   with self.assertRaises((ValueError,TypeError,KeyError,AssertionError)):verify_uniform(forged)
  self.assertGreater(len(paths),400)
 def test_swapped_or_truncated_context_rows(self):
  r=analyze_uniform(dict(atoms=['p'],left=[],right=[]));r['fact_contexts'].reverse()
  with self.assertRaises(ValueError):verify_uniform(r)
  r=analyze_uniform(dict(atoms=['p'],left=[],right=[]));r['fact_contexts'].pop()
  with self.assertRaises(ValueError):verify_uniform(r)
 def test_collision_and_no_generator_import(self):
  r=analyze_uniform(dict(atoms=['p'],left=[dict(id='fact0',head='p',positive=[],negative=[])],right=[dict(id='fact1',head='p',positive=['p'],negative=[])]));verify_uniform(r);self.assertEqual(r['fact_contexts'][1]['context'][0]['id'],'fact2')
  src=(ROOT/'stablelab/uniform_oracle.py').read_text();self.assertNotIn('from .uniform import',src);self.assertNotIn('from .equivalence import',src);self.assertNotIn('from .core import',src)
if __name__=='__main__':unittest.main()
