"""Complete candidate/reduct/grounding evidence for bounded normal programs."""
from .model import parse


def analyze(data):
    p = parse(data); atoms, rules = p['atoms'], p['rules']; records = []
    sets = [set(a for i,a in enumerate(atoms) if mask & (1 << i)) for mask in range(1 << len(atoms))]
    for mask, m in enumerate(sets):
        rows=[]; kept=[]
        for r in rules:
            missing=sorted(set(r['positive'])-m); blocked=sorted(set(r['negative'])&m)
            active=not missing and not blocked
            rows.append({'id':r['id'],'missing_positive':missing,'present_negative':blocked,'body_true':active,'satisfied':not active or r['head'] in m})
            if not blocked: kept.append(r)
        closure=set(); rounds=[]
        while True:
            firings=[r for r in kept if r['head'] is not None and set(r['positive']) <= closure]
            new=set(r['head'] for r in firings)-closure
            rounds.append({'before':sorted(closure),'ready_rules':[r['id'] for r in firings],'new_atoms':sorted(new)})
            if not new: break
            closure |= new
        violated=[r['id'] for r in kept if r['head'] is None and set(r['positive']) <= closure]
        supports=[{'atom':a,'rules':[r['id'] for r,row in zip(rules,rows) if r['head']==a and row['body_true']]} for a in sorted(m)]
        unfounded=[]
        for sub,u in enumerate(sets):
            if not u or not u <= m:continue
            obligations=[];valid=True
            for r,row in zip(rules,rows):
                if r['head'] not in u:continue
                internal=sorted(set(r['positive'])&u)
                if row['body_true'] and not internal:valid=False;break
                obligations.append({'rule':r['id'],'missing_positive':row['missing_positive'],'present_negative':row['present_negative'],'internal_positive':internal})
            if valid:unfounded.append({'mask':sub,'atoms':sorted(u),'obligations':obligations})
        model=all(row['satisfied'] for row in rows)
        records.append({'mask':mask,'atoms':sorted(m),'rules':rows,'reduct_rules':[{'id':r['id'],'head':r['head'],'positive':r['positive']} for r in kept], 'closure_rounds':rounds,'least_reduct_closure':sorted(closure),'closure_violated_constraints':violated,'missing_from_candidate':sorted(closure-m),'ungrounded_candidate_atoms':sorted(m-closure),'supports':supports,'unfounded_subsets':unfounded,'model':model,'supported':model and all(s['rules'] for s in supports),'stable':model and m==closure and not violated})
    for rec,m in zip(records,sets):
        smaller=[r['mask'] for r,s in zip(records,sets) if r['model'] and s < m]
        rec['proper_subset_models']=smaller;rec['minimal_model']=rec['model'] and not smaller
    stable=[r for r in records if r['stable']]
    return {'schema':'stablelab-evidence-v1','program':p,'candidates':records,'model_masks':[r['mask'] for r in records if r['model']],'supported_masks':[r['mask'] for r in records if r['supported']],'minimal_model_masks':[r['mask'] for r in records if r['minimal_model']],'stable_masks':[r['mask'] for r in stable],'queries':[{'atom':a,'brave':any(a in r['atoms'] for r in stable) if stable else None,'skeptical':all(a in r['atoms'] for r in stable) if stable else None,'stable_with':[r['mask'] for r in stable if a in r['atoms']],'stable_without':[r['mask'] for r in stable if a not in r['atoms']]} for a in atoms]}
