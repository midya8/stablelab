"""Separate truth-table/subset oracle. Does not import the generator.

Model intersection establishes the least definite reduct model. Bounded proof
height independently reconstructs the displayed rounds. Strict full JSON checks
reject missing, reordered and fabricated fields as well as bool/int coercions.
"""
from itertools import combinations
from functools import lru_cache
import json
from .model import parse


def verify(report):
    if not isinstance(report, dict) or 'program' not in report:
        raise ValueError('Expected evidence report')
    p=parse(report['program']); aa=p['atoms'];rr=p['rules']
    universe=[frozenset(c) for k in range(len(aa)+1) for c in combinations(aa,k)]
    mask=lambda s:sum(2**aa.index(a) for a in s)
    universe.sort(key=mask)
    def holds(r,s):return all(a in s for a in r['positive']) and all(a not in s for a in r['negative'])
    def model(s):return all(not holds(r,s) or r['head'] in s for r in rr)
    models=[s for s in universe if model(s)]; candidates=[]
    for m in universe:
        reduct=[r for r in rr if not any(a in m for a in r['negative'])]
        definite=[r for r in reduct if r['head'] is not None]
        posmodels=[s for s in universe if all(not all(a in s for a in r['positive']) or r['head'] in s for r in definite)]
        least=frozenset.intersection(*posmodels)
        @lru_cache(None)
        def proof(a,depth):
            return depth>0 and any(r['head']==a and all(proof(b,depth-1) for b in r['positive']) for r in definite)
        rounds=[]
        for depth in range(len(aa)+1):
            before=frozenset(a for a in aa if proof(a,depth))
            ready=[r for r in definite if all(a in before for a in r['positive'])]
            new=sorted({r['head'] for r in ready}-before)
            rounds.append({'before':sorted(before),'ready_rules':[r['id'] for r in ready],'new_atoms':new})
            if not new:break
        rows=[{'id':r['id'],'missing_positive':[a for a in r['positive'] if a not in m],'present_negative':[a for a in r['negative'] if a in m],'body_true':holds(r,m),'satisfied':not holds(r,m) or r['head'] in m} for r in rr]
        supports=[{'atom':a,'rules':[r['id'] for r in rr if r['head']==a and holds(r,m)]} for a in sorted(m)]
        unfounded=[]
        for u in universe:
            if not u or not u.issubset(m):continue
            relevant=[r for r in rr if r['head'] in u]
            if any(holds(r,m) and not any(a in u for a in r['positive']) for r in relevant):continue
            unfounded.append({'mask':mask(u),'atoms':sorted(u),'obligations':[{'rule':r['id'],'missing_positive':[a for a in r['positive'] if a not in m],'present_negative':[a for a in r['negative'] if a in m],'internal_positive':[a for a in r['positive'] if a in u]} for r in relevant]})
        # Check stability using ALL proper subset models of the reduct, not closure.
        reduct_models=[s for s in universe if all(not all(a in s for a in r['positive']) or r['head'] in s for r in reduct)]
        stable=m in reduct_models and not any(s<m for s in reduct_models)
        if stable != (m in models and not unfounded):raise AssertionError('independent unfounded characterization disagrees')
        candidates.append({'mask':mask(m),'atoms':sorted(m),'rules':rows,'reduct_rules':[{'id':r['id'],'head':r['head'],'positive':r['positive']} for r in reduct],'closure_rounds':rounds,'least_reduct_closure':sorted(least),'closure_violated_constraints':[r['id'] for r in reduct if r['head'] is None and all(a in least for a in r['positive'])],'missing_from_candidate':sorted(least-m),'ungrounded_candidate_atoms':sorted(m-least),'supports':supports,'unfounded_subsets':unfounded,'model':m in models,'supported':m in models and all(x['rules'] for x in supports),'stable':stable,'proper_subset_models':[mask(s) for s in models if s<m],'minimal_model':m in models and not any(s<m for s in models)})
    stable=[x for x in candidates if x['stable']]
    expected={'schema':'stablelab-evidence-v1','program':p,'candidates':candidates,'model_masks':[x['mask'] for x in candidates if x['model']],'supported_masks':[x['mask'] for x in candidates if x['supported']],'minimal_model_masks':[x['mask'] for x in candidates if x['minimal_model']],'stable_masks':[x['mask'] for x in stable],'queries':[{'atom':a,'brave':any(a in x['atoms'] for x in stable) if stable else None,'skeptical':all(a in x['atoms'] for x in stable) if stable else None,'stable_with':[x['mask'] for x in stable if a in x['atoms']],'stable_without':[x['mask'] for x in stable if a not in x['atoms']]} for a in aa]}
    if json.dumps(report,sort_keys=True,separators=(',',':'),allow_nan=False)!=json.dumps(expected,sort_keys=True,separators=(',',':'),allow_nan=False):raise ValueError('Evidence does not match independent reconstruction')
    return {'valid':True,'candidates':len(candidates),'stable_models':len(stable)}
