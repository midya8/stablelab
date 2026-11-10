"""Independent three-valued SE checker plus subset-model context checking.

Never imports comparison generator or base closure engine. Reuses strict parsing
and the existing independent base evidence verifier, explicitly disclosed.
"""
import itertools,json
from .comparison_model import parse_comparison
from .oracle import verify as verify_base


def verify_comparison(report):
    if not isinstance(report,dict) or 'request' not in report:raise ValueError('Expected comparison evidence')
    req=parse_comparison(report['request']);aa=req['atoms'];sets=[]
    for k in range(len(aa)+1):sets.extend(frozenset(z) for z in itertools.combinations(aa,k))
    mask=lambda s:sum(2**aa.index(a) for a in s);sets.sort(key=mask)
    triples=list(itertools.product(range(3),repeat=len(aa)));triples.sort(key=lambda t:(mask({a for a,v in zip(aa,t) if v>0}),mask({a for a,v in zip(aa,t) if v==2})))
    pairs=[]
    for t in triples:
        vals=dict(zip(aa,t));x={a for a,v in vals.items() if v==2};y={a for a,v in vals.items() if v>0};entry={'id':len(pairs),'x_mask':mask(x),'y_mask':mask(y),'x':sorted(x),'y':sorted(y)}
        for s in ('left','right'):
            rows=[]
            for r in req[s]:
                # Godel three-valued conjunction/implication for the actual rule.
                pos=min([vals[a] for a in r['positive']],default=2);neg=min([2 if vals[a]==0 else 0 for a in r['negative']],default=2);body=min(pos,neg);head=0 if r['head'] is None else vals[r['head']];ht=2 if body<=head else head
                ybody=all(vals[a]>0 for a in r['positive']) and all(vals[a]==0 for a in r['negative']);kept=all(vals[a]==0 for a in r['negative']);xs=(any(vals[a]<2 for a in r['positive']) or (r['head'] is not None and vals[r['head']]==2)) if kept else None;ys=not ybody or (r['head'] is not None and vals[r['head']]>0)
                rows.append({'id':r['id'],'y_missing_positive':[a for a in r['positive'] if vals[a]==0],'y_present_negative':[a for a in r['negative'] if vals[a]>0],'y_head_present':r['head'] is not None and vals[r['head']]>0,'y_rule_satisfied':ys,'reduct_kept':kept,'x_missing_positive':[a for a in r['positive'] if vals[a]<2],'x_head_present':r['head'] is not None and vals[r['head']]==2,'x_reduct_rule_satisfied':xs,'se_rule':ht==2})
            entry[s]={'y_model':all(r['y_rule_satisfied'] for r in rows),'x_reduct_model':all(r['x_reduct_rule_satisfied'] is not False for r in rows),'se_model':all(r['se_rule'] for r in rows),'rules':rows}
        entry['different']=entry['left']['se_model']!=entry['right']['se_model'];pairs.append(entry)
    def stable(rules):
        out=[]
        for y in sets:
            reduct=[r for r in rules if not any(a in y for a in r['negative'])]
            models=[z for z in sets if z<=y and all(not all(a in z for a in r['positive']) or r['head'] in z for r in reduct)]
            if y in models and not any(z<y for z in models):out.append(mask(y))
        return out
    families={}
    for s in ('left','right'):
        classical=[mask(y) for y in sets if all(not(all(a in y for a in r['positive']) and all(a not in y for a in r['negative'])) or r['head'] in y for r in req[s])]
        families[s]={'classical_masks':classical,'stable_masks':stable(req[s]),'se_pair_ids':[p['id'] for p in pairs if p[s]['se_model']]}
    diff=[p['id'] for p in pairs if p['different']];witness=None
    if diff:
        p=pairs[diff[0]];inside='left' if p['left']['se_model'] else 'right';outside='right' if inside=='left' else 'left';x=set(p['x']);y=set(p['y']);kind='facts_y' if not p[outside]['y_model'] else 'facts_x_cycle';facts=sorted(y if kind=='facts_y' else x);d=sorted(y-x);spec=[(a,[]) for a in facts]
        if kind=='facts_x_cycle' and len(d)>1:spec.extend((a,[d[(i+1)%len(d)]]) for i,a in enumerate(d))
        used={r['id'] for s in ('left','right') for r in req[s]};context=[]
        for a,pos in spec:
            j=0
            while 'ctx'+str(j) in used:j+=1
            name='ctx'+str(j);used.add(name);context.append({'id':name,'head':a,'positive':pos,'negative':[]})
        submodels=[mask(z) for z in sets if z<=y and all(not all(a in z for a in r['positive']) or r['head'] in z for r in context)]
        if submodels!=([mask(y)] if kind=='facts_y' else sorted({mask(x),mask(y)})):raise AssertionError('context gadget does not isolate X,Y')
        actual=report.get('witness')
        if not isinstance(actual,dict):raise ValueError('Missing separating context')
        for s in ('left','right'):
            ev=actual.get(s+'_augmented');verify_base(ev)
            if ev['program']!={'atoms':aa,'rules':req[s]+context}:raise ValueError('Augmented context uses wrong program')
            if ev['stable_masks']!=stable(req[s]+context):raise ValueError('Context family differs from subset table')
        ym=p['y_mask'];left=ym in stable(req['left']+context);right=ym in stable(req['right']+context)
        if left==right:raise ValueError('Context does not distinguish Y')
        witness={'pair_id':p['id'],'kind':kind,'se_inside':inside,'context':context,'context_models_below_y':submodels,'distinguishing_y_mask':ym,'stable_in':'left' if left else 'right','left_augmented':actual['left_augmented'],'right_augmented':actual['right_augmented']}
    expected={'schema':'stablelab-equivalence-v1','request':req,'pairs':pairs,'families':families,'classically_equivalent':families['left']['classical_masks']==families['right']['classical_masks'],'ordinarily_equivalent':families['left']['stable_masks']==families['right']['stable_masks'],'strongly_equivalent':not diff,'difference_pair_ids':diff,'witness':witness}
    if json.dumps(report,sort_keys=True,separators=(',',':'),allow_nan=False)!=json.dumps(expected,sort_keys=True,separators=(',',':'),allow_nan=False):raise ValueError('Comparison evidence differs from independent reconstruction')
    return {'valid':True,'pairs':len(pairs),'strongly_equivalent':not diff,'context_checked':bool(diff)}
