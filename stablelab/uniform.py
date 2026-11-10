"""Uniform equivalence: complete fact contexts and maximal proper SE pairs."""
from .comparison_model import parse_comparison
from .equivalence import compare
from .core import analyze


def fact_rules(request,mask):
    occupied={r['id'] for side in ('left','right') for r in request[side]};rules=[];j=0
    for i,a in enumerate(request['atoms']):
        if not mask&(1<<i):continue
        while 'fact'+str(j) in occupied:j+=1
        name='fact'+str(j);occupied.add(name);j+=1
        rules.append({'id':name,'head':a,'positive':[],'negative':[]})
    return rules


def analyze_uniform(data):
    request=parse_comparison(data);comparison=compare(request);pairs=comparison['pairs'];ue=[]
    for p in pairs:
        sides={}
        for s in ('left','right'):
            extensions=[q['id'] for q in pairs if q['y_mask']==p['y_mask'] and p['x_mask']!=q['x_mask'] and q['x_mask']!=p['y_mask'] and p['x_mask']&q['x_mask']==p['x_mask'] and q[s]['se_model']]
            sides[s]={'se_model':p[s]['se_model'],'proper_extensions':extensions,'ue_model':p[s]['se_model'] and not extensions}
        ue.append({'pair_id':p['id'],**sides,'different':sides['left']['ue_model']!=sides['right']['ue_model']})
    contexts=[]
    for mask in range(1<<len(request['atoms'])):
        facts=fact_rules(request,mask);families={}
        for side in ('left','right'):
            report=analyze({'atoms':request['atoms'],'rules':request[side]+facts})
            families[side]={'stable_masks':report['stable_masks'],'candidates':[{'mask':r['mask'],'model':r['model'],'least_reduct_closure':r['least_reduct_closure'],'closure_violated_constraints':r['closure_violated_constraints'],'stable':r['stable']} for r in report['candidates']]}
        contexts.append({'mask':mask,'facts':[r['head'] for r in facts],'context':facts,**families,'different':families['left']['stable_masks']!=families['right']['stable_masks']})
    differences=[c['mask'] for c in contexts if c['different']];ue_differences=[p['pair_id'] for p in ue if p['different']]
    assert bool(differences)==bool(ue_differences)
    witness=None
    if differences:
        chosen=min(differences,key=lambda m:(m.bit_count(),m));c=contexts[chosen]
        detail={s:analyze({'atoms':request['atoms'],'rules':request[s]+c['context']}) for s in ('left','right')}
        witness={'fact_mask':chosen,'fact_count':chosen.bit_count(),'no_smaller_separating_contexts':[c['mask'] for c in contexts if c['mask'].bit_count()<chosen.bit_count()],'left_augmented':detail['left'],'right_augmented':detail['right']}
    return {'schema':'stablelab-uniform-v1','comparison':comparison,'ue_pairs':ue,'ue_difference_pair_ids':ue_differences,'fact_contexts':contexts,'different_fact_masks':differences,'uniformly_equivalent':not differences,'minimum_fact_witness':witness}
