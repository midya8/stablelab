"""Independent finite fact-context checker. Imports no evidence generator."""
import itertools,json
from .comparison_model import parse_comparison
from .equivalence_oracle import verify_comparison
from .oracle import verify as verify_base


def verify_uniform(report):
    if not isinstance(report,dict) or not isinstance(report.get('comparison'),dict):raise ValueError('Expected uniform evidence')
    comparison=report['comparison'];verify_comparison(comparison);request=parse_comparison(comparison['request']);aa=request['atoms'];sets=[frozenset(a for i,a in enumerate(aa) if m&(1<<i)) for m in range(1<<len(aa))];mask=lambda z:sum(1<<aa.index(a) for a in z)
    # The comparison checker has independently reconstructed every pair with
    # three-valued implication. Only checked records are used for UE maximality.
    pairs=comparison['pairs'];ue=[]
    for p in pairs:
        sides={};x=frozenset(p['x']);y=frozenset(p['y'])
        for side in ('left','right'):
            ext=[q['id'] for q in pairs if q['y_mask']==p['y_mask'] and x<frozenset(q['x'])<y and q[side]['se_model']]
            sides[side]={'se_model':p[side]['se_model'],'proper_extensions':ext,'ue_model':p[side]['se_model'] and not ext}
        ue.append({'pair_id':p['id'],**sides,'different':sides['left']['ue_model']!=sides['right']['ue_model']})
    contexts=[]
    def facts_for(f):
        used={r['id'] for s in ('left','right') for r in request[s]};out=[]
        for a in sorted(f):
            j=0
            while 'fact'+str(j) in used:j+=1
            name='fact'+str(j);used.add(name);out.append(dict(id=name,head=a,positive=[],negative=[]))
        return out
    for fm,f in enumerate(sets):
        facts=facts_for(f);families={}
        for side in ('left','right'):
            rr=request[side]+facts;rows=[]
            for ym,y in enumerate(sets):
                reduct=[r for r in rr if set(r['negative']).isdisjoint(y)]
                def models(z,rules):return all(not set(r['positive'])<=z or r['head'] in z for r in rules)
                model=all(not(set(r['positive'])<=y and set(r['negative']).isdisjoint(y)) or r['head'] in y for r in rr)
                # Intersection of all definite reduct models gives its least
                # model; stability is independently proper-subset minimality.
                definite=[r for r in reduct if r['head'] is not None];dm=[z for z in sets if models(z,definite)];closure=set.intersection(*(set(z) for z in dm)) if dm else set()
                bad=[r['id'] for r in reduct if r['head'] is None and set(r['positive'])<=closure]
                stable=model and models(y,reduct) and not any(z<y and models(z,reduct) for z in sets)
                rows.append({'mask':ym,'model':model,'least_reduct_closure':sorted(closure),'closure_violated_constraints':bad,'stable':stable})
            families[side]={'stable_masks':[r['mask'] for r in rows if r['stable']],'candidates':rows}
        contexts.append({'mask':fm,'facts':sorted(f),'context':facts,**families,'different':families['left']['stable_masks']!=families['right']['stable_masks']})
    differences=[c['mask'] for c in contexts if c['different']];ue_differences=[p['pair_id'] for p in ue if p['different']]
    if bool(differences)!=bool(ue_differences):raise ValueError('Fact table and UE characterization disagree')
    witness=None
    if differences:
        chosen=min(differences,key=lambda m:(len(sets[m]),m));c=contexts[chosen];actual=report.get('minimum_fact_witness')
        if not isinstance(actual,dict):raise ValueError('Missing minimum fact witness')
        for side in ('left','right'):
            ev=actual.get(side+'_augmented');verify_base(ev)
            if ev['program']!={'atoms':aa,'rules':request[side]+c['context']}:raise ValueError('Wrong augmented fact context')
            if ev['stable_masks']!=c[side]['stable_masks']:raise ValueError('Augmented stable family differs')
        witness={'fact_mask':chosen,'fact_count':len(sets[chosen]),'no_smaller_separating_contexts':[c['mask'] for c in contexts if len(sets[c['mask']])<len(sets[chosen])],'left_augmented':actual['left_augmented'],'right_augmented':actual['right_augmented']}
    expected={'schema':'stablelab-uniform-v1','comparison':comparison,'ue_pairs':ue,'ue_difference_pair_ids':ue_differences,'fact_contexts':contexts,'different_fact_masks':differences,'uniformly_equivalent':not differences,'minimum_fact_witness':witness}
    if json.dumps(report,sort_keys=True,separators=(',',':'),allow_nan=False)!=json.dumps(expected,sort_keys=True,separators=(',',':'),allow_nan=False):raise ValueError('Uniform evidence differs from independent reconstruction')
    return {'valid':True,'uniformly_equivalent':not differences,'fact_contexts':len(contexts),'pairs':len(pairs),'minimum_fact_count':witness['fact_count'] if witness else None}
