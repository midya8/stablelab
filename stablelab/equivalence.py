"""Complete finite SE interpretations and concrete separating contexts."""
from .comparison_model import parse_comparison
from .core import analyze



def compare(data):
    request=parse_comparison(data);aa=request['atoms'];sets=[set(a for i,a in enumerate(aa) if m&(1<<i)) for m in range(1<<len(aa))]
    def side(rules,x,y):
        rows=[]
        for r in rules:
            missy=sorted(set(r['positive'])-y);missx=sorted(set(r['positive'])-x);neg=sorted(set(r['negative'])&y)
            ys=bool(missy or neg or r['head'] in y);xs=bool(missx or r['head'] in x) if not neg else None
            rows.append({'id':r['id'],'y_missing_positive':missy,'y_present_negative':neg,'y_head_present':r['head'] in y,'y_rule_satisfied':ys,'reduct_kept':not neg,'x_missing_positive':missx,'x_head_present':r['head'] in x,'x_reduct_rule_satisfied':xs,'se_rule':ys and (xs if not neg else True)})
        ym=all(r['y_rule_satisfied'] for r in rows);xm=all(r['x_reduct_rule_satisfied'] is not False for r in rows)
        return {'y_model':ym,'x_reduct_model':xm,'se_model':ym and xm,'rules':rows}
    pairs=[]
    for ym,y in enumerate(sets):
        for xm,x in enumerate(sets):
            if not x<=y:continue
            left=side(request['left'],x,y);right=side(request['right'],x,y)
            pairs.append({'id':len(pairs),'x_mask':xm,'y_mask':ym,'x':sorted(x),'y':sorted(y),'left':left,'right':right,'different':left['se_model']!=right['se_model']})
    families={}
    for s in ('left','right'):
        classical=[ym for ym in range(len(sets)) if next(p for p in pairs if p['x_mask']==ym and p['y_mask']==ym)[s]['y_model']]
        stable=[ym for ym in classical if not any(p['y_mask']==ym and p['x_mask']!=ym and p[s]['se_model'] for p in pairs)]
        families[s]={'classical_masks':classical,'stable_masks':stable,'se_pair_ids':[p['id'] for p in pairs if p[s]['se_model']]}
    diff=[p['id'] for p in pairs if p['different']];witness=None
    if diff:
        p=pairs[diff[0]];inside='left' if p['left']['se_model'] else 'right';outside='right' if inside=='left' else 'left'
        x,y=sets[p['x_mask']],sets[p['y_mask']];facts=sorted(y if not p[outside]['y_model'] else x);d=sorted(y-x);kind='facts_y' if not p[outside]['y_model'] else 'facts_x_cycle'
        ids={r['id'] for s in ('left','right') for r in request[s]};context=[];counter=0
        def add(head,pos):
            nonlocal counter
            while 'ctx'+str(counter) in ids:counter+=1
            id='ctx'+str(counter);ids.add(id);counter+=1;context.append({'id':id,'head':head,'positive':pos,'negative':[]})
        for a in facts:add(a,[])
        if kind=='facts_x_cycle' and len(d)>1:
            for i,a in enumerate(d):add(a,[d[(i+1)%len(d)]])
        submodels=[i for i,z in enumerate(sets) if z<=y and all(not set(r['positive'])<=z or r['head'] in z for r in context)]
        augmented={s:analyze({'atoms':aa,'rules':request[s]+context}) for s in ('left','right')}
        ym=p['y_mask'];winner='left' if ym in augmented['left']['stable_masks'] else 'right'
        assert (ym in augmented['left']['stable_masks'])!=(ym in augmented['right']['stable_masks'])
        witness={'pair_id':p['id'],'kind':kind,'se_inside':inside,'context':context,'context_models_below_y':submodels,'distinguishing_y_mask':ym,'stable_in':winner,'left_augmented':augmented['left'],'right_augmented':augmented['right']}
    return {'schema':'stablelab-equivalence-v1','request':request,'pairs':pairs,'families':families,'classically_equivalent':families['left']['classical_masks']==families['right']['classical_masks'],'ordinarily_equivalent':families['left']['stable_masks']==families['right']['stable_masks'],'strongly_equivalent':not diff,'difference_pair_ids':diff,'witness':witness}
