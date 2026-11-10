import unittest,copy,itertools,random
from stablelab.core import analyze
from stablelab.oracle import verify
from make_controls import controls,rule

class Semantics(unittest.TestCase):
    def test_controls(self):
        expected=[[],[0],[1,2],[],[1],[15],[3],[0],[],[85,86,89,90,101,102,105,106,149,150,153,154,165,166,169,170]]
        for c,exp in zip(controls,expected):
            with self.subTest(c=c['title']):
                r=analyze(c['program']);self.assertEqual(r['stable_masks'],exp);self.assertTrue(verify(r)['valid'])
        r=analyze(controls[0]['program']);self.assertEqual(r['minimal_model_masks'],[3]);self.assertEqual(r['supported_masks'],[3]);self.assertFalse(r['stable_masks']);self.assertEqual(r['candidates'][3]['least_reduct_closure'],[])
    def test_all_two_atom_programs_up_to_two_rules(self):
        # Every signed body, including contradictory positive/negative occurrences;
        # every single head or constraint. All 1,177 sets of up to two such rules.
        rules=[]
        for head in [None,'p','q']:
            for states in itertools.product(range(4),repeat=2):
                rules.append(rule('r'+str(len(rules)),head,[a for a,s in zip(['p','q'],states) if s&1],[a for a,s in zip(['p','q'],states) if s&2]))
        count=0
        for k in range(3):
            for rs in itertools.combinations(rules,k):
                verify(analyze(dict(atoms=['p','q'],rules=list(rs))));count+=1
        self.assertEqual(count,1177)
    def test_seeded_three_atom_programs(self):
        rng=random.Random(731)
        for _ in range(200):
            rs=[rule('r'+str(i),rng.choice([None,'a','b','c']),[a for a in ['a','b','c'] if rng.random()<.35],[a for a in ['a','b','c'] if rng.random()<.35]) for i in range(rng.randrange(10))]
            verify(analyze(dict(atoms=['a','b','c'],rules=rs)))
    def test_all_unfounded_obligations_and_equivalence(self):
        for c in controls:
            r=analyze(c['program'])
            for row in r['candidates']:
                self.assertEqual(row['stable'], row['model'] and not row['unfounded_subsets'])
                for u in row['unfounded_subsets']:
                    for ob in u['obligations']:
                        self.assertTrue(ob['missing_positive'] or ob['present_negative'] or ob['internal_positive'])
    def test_synchronous_rounds_keep_all_ready_rules(self):
        r=analyze(controls[5]['program'])['candidates'][15]
        self.assertEqual([x['new_atoms'] for x in r['closure_rounds']],[['p'],['q'],['r'],['s'],[]])
        self.assertEqual(r['closure_rounds'][-1]['ready_rules'],['seed','pq','qp','qr','rs'])
    def test_forgery_rejection(self):
        orig=analyze(controls[0]['program'])
        for mutate in [lambda x:x.update(stable_masks=[3]),lambda x:x['candidates'][3]['closure_rounds'][0].update(new_atoms=['p']),lambda x:x['candidates'][3].update(unfounded_subsets=[]),lambda x:x['candidates'][0].update(mask=False),lambda x:x.update(extra='forged'),lambda x:x['candidates'][3]['unfounded_subsets'][0]['obligations'][-1].update(internal_positive=[])]:
            x=copy.deepcopy(orig);mutate(x)
            with self.assertRaises(ValueError):verify(x)
    def test_checker_does_not_call_generator(self):
        from unittest.mock import patch
        r=analyze(controls[2]['program'])
        with patch('stablelab.core.analyze',side_effect=AssertionError('generator disabled')):self.assertTrue(verify(r)['valid'])
    def test_strict_input(self):
        valid=controls[0]['program']
        invalid=[None,[],{},dict(atoms=['q','p'],rules=[]),dict(atoms=['p','p'],rules=[]),dict(atoms=['P'],rules=[]),dict(atoms=['p'],rules=[rule('r','q')]),dict(atoms=['p'],rules=[rule('r','p',pos=['q'])]),dict(atoms=['p'],rules=[dict(id='r',head='p',positive=[],negative=[],extra=1)]),dict(atoms=['p'],rules=[rule('r','p'),rule('r','p')]),dict(atoms=list('abcdefghi'),rules=[]),dict(atoms=['p'],rules=[rule('r'+str(i),'p') for i in range(33)])]
        for x in invalid:
            with self.assertRaises(ValueError):analyze(x)
    def test_no_stable_query_convention(self):
        r=analyze(controls[3]['program']);self.assertIsNone(r['queries'][0]['brave']);self.assertIsNone(r['queries'][0]['skeptical']);self.assertEqual(r['queries'][0]['stable_with'],[])
        self.assertEqual(analyze(controls[7]['program'])['stable_masks'],[0]);self.assertEqual(analyze(controls[8]['program'])['stable_masks'],[])
if __name__=='__main__':unittest.main()
